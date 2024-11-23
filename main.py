import pygame
import sys
from scripts.tilemap import Grid
from scripts.player import Player
from scripts.cursor import Cursor
from scripts.enemy import Enemy
from utils.fov import Overlay
from utils.menu import Menu
# from levels.thing import matrix

pygame.init()
pygame.mixer.init()

TileSize = 40
ViewX, ViewY = 20, 15
TilesX, TilesY = 40, 40
ScreenX, ScreenY = TileSize * ViewX, TileSize * ViewY
Fps = 60
Black = "#000000"

# matrix = [[[(-1, -1), (-1, -1), (0,0), (-1, -1)] for _ in range(TilesX)] for _ in range(TilesY)]
from levels.thing import matrix

screen = pygame.display.set_mode((ScreenX, ScreenY))
pygame.display.set_caption("Tile Grid System")
clock = pygame.time.Clock()
pygame.mouse.set_visible(False)
grid = Grid(TilesX, TilesY, TileSize, matrix, ScreenX, ScreenY)
fov = Overlay(ScreenX, ScreenY, 200, [ScreenX // 2, ScreenY // 2])
player = Player(TileSize, TileSize,1,0,360)
cursor = Cursor()

enemies = [
    Enemy((240,520),(240,360),1,"right")
]
pygame.mixer.music.load("assets/Music/bgm.mp3")
pygame.mixer.music.play(loops=-1)
pygame.mixer.music.set_volume(0.2)

def main():
    running = True
    pauseMenu = False
    holdingEsc = False
    menu = Menu(screen)
    while running:
        screen.fill(Black)
        right = 0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        jump = False
        if keys[pygame.K_a] or keys[pygame.K_h] or keys[pygame.K_LEFT]:
            right = -1
        elif keys[pygame.K_d] or keys[pygame.K_l] or keys[pygame.K_RIGHT]:
            right = 1
        else:
            right = 0

        if keys[pygame.K_w] or keys[pygame.K_k] or keys[pygame.K_UP]:
            jump = True
        else:
            jump = False
        if keys[pygame.K_ESCAPE]:
            if not holdingEsc:
                holdingEsc = True
                pauseMenu = not pauseMenu
        else:
            holdingEsc = False

        screen.fill("#000000")
        grid.render(screen)
        player.render(screen)


        if menu.exit:
            running = False
        if not menu.menuOpen:
            player.update(right,grid,screen,enemies,jump=jump)
            if not menu.mute:
                pygame.mixer.music.set_volume(0.2+menu.soundChange)
            else:
                pygame.mixer.music.set_volume(0.0+menu.soundChange)
        else:
            if not menu.mute:
                pygame.mixer.music.set_volume(0.5+menu.soundChange)
            else:
                pygame.mixer.music.set_volume(0.0)

        if menu.reset:
            player.reset()
            for enemy in enemies:
                enemy.reset()
            menu.reset = False

        for entity in enemies:
            entity.update(screen)
        fov.render(screen,[player.x+player.img.get_width() // 2,player.y + player.img.get_height() // 2])

        menu.render()

        cursor.render(screen)
        pygame.display.flip()
        clock.tick(Fps)
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
