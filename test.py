import sys
from array import array

import pygame
import moderngl

pygame.init()

from scripts.tilemap import Grid
from scripts.player import Player
from scripts.cursor import Cursor
from utils.fov import Overlay
from levels.thingy import matrix

TileSize = 35
ViewX, ViewY = 20, 15
TilesX, TilesY = 40, 40
ScreenX, ScreenY = TileSize * ViewX, TileSize * ViewY
Fps = 60
Black = "#000000"

screen = pygame.display.set_mode((ScreenX, ScreenY), pygame.OPENGL | pygame.DOUBLEBUF)
display = pygame.Surface((ScreenX, ScreenY))
ctx = moderngl.create_context()

pygame.display.set_caption("Tile Grid System")
clock = pygame.time.Clock()
pygame.mouse.set_visible(False)
grid = Grid(TilesX, TilesY, TileSize, matrix, ScreenX, ScreenY)
mousefov = Overlay(ScreenX, ScreenY, 250, [ScreenX // 2, ScreenY // 2])
player = Player(0, 0, TileSize, TileSize)
cursor = Cursor()

quad_buffer = ctx.buffer(data=array('f', [
    -1.0, 1.0, 0.0, 0.0,
    1.0, 1.0, 1.0, 0.0,
    -1.0, -1.0, 0.0, 1.0,
    1.0, -1.0, 1.0, 1.0,
]))

vert_shader = '''
#version 330 core
in vec2 vert;
in vec2 texCoord;
out vec2 uvs;
void main() {
    uvs = texCoord;
    gl_Position = vec4(vert, 0.0, 1.0);
}
'''

frag_shader = '''
#version 330 core

// The power of the barrel distortion
uniform float power = 1.1f;

// Texture Unit
uniform sampler2D textureUnit;

// Texture coordinate
in vec2 uvs;

// Final color
out vec4 fragColor;

vec2 BarrelDistortionCoordinates(vec2 uv)
{
    // Convert tex coord to the -1 to 1 range
    vec2 pos = 2.0 * uv - 1.0;

    float len = length(pos);
    len = pow(len, power);

    pos = normalize(pos);
    pos *= len;

    // Convert pos to the 0 to 1 range
    pos = 0.5 * (pos + 1.0);

    return pos;
}

void main()
{
    vec2 barrelUV = BarrelDistortionCoordinates(uvs);
    if (barrelUV.x < 0.0 || barrelUV.y < 0.0 || barrelUV.x > 1.0 || barrelUV.y > 1.0) discard;
    fragColor = texture(textureUnit, barrelUV);
}
'''
program = ctx.program(vertex_shader=vert_shader, fragment_shader=frag_shader)
render_object = ctx.vertex_array(program, [(quad_buffer, '2f 2f', 'vert', 'texCoord')])

has_time_uniform = 'time' in program

def surf_to_texture(surf):
    tex = ctx.texture(surf.get_size(), 4)
    tex.filter = (moderngl.NEAREST, moderngl.NEAREST)
    tex.swizzle = 'BGRA'
    tex.write(surf.get_view('1'))
    return tex

t = 0


while True:
    display.fill(Black)
    
    t += 1
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    jump = False
    keys = pygame.key.get_pressed()
    right = -1 if keys[pygame.K_a] else 1 if keys[pygame.K_d] else 0
    jump = True if keys[pygame.K_w] else False

    grid.render(display)
    player.update(right, grid, display,jump=jump)

    mouseX, mouseY = pygame.mouse.get_pos()
    cursor.render(display)


    frame_tex = surf_to_texture(display)
    frame_tex.use(0)
    program['textureUnit'] = 0
    
    if has_time_uniform:
        program['time'] = t / 60.0

    render_object.render(mode=moderngl.TRIANGLE_STRIP)
    pygame.display.flip()
    
    frame_tex.release()
    clock.tick(Fps)
