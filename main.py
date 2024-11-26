import pygame
import random
import sys

from pygame.mixer_music import play
from scripts.levelManager import LevelManager
from scripts.levelTransition import Transition
from scripts.player import Player
from scripts.cursor import Cursor
from utils.fov import Overlay
from utils.menu import Menu
from utils.timer import Timer

pygame.init()
pygame.mixer.init()

TileSize = 40
ViewX, ViewY = 20, 15
ScreenX, ScreenY = TileSize * ViewX, TileSize * ViewY
Fps = 60
Black = "#000000"

display = pygame.display.set_mode((ScreenX, ScreenY))
screen = pygame.surface.Surface((ScreenX,ScreenY))
pygame.display.set_caption("Tile Grid System")
clock = pygame.time.Clock()
pygame.mouse.set_visible(False)

lManager = LevelManager(screen)
player = Player(TileSize, TileSize, 1, 0, 400)
cursor = Cursor()
fov = Overlay(ScreenX, ScreenY, 200, [ScreenX // 2, ScreenY // 2])
timer = Timer(ScreenX, ScreenY)
transition = Transition()
pygame.mixer.music.load("assets/Music/bgm.mp3")
pygame.mixer.music.play(loops=-1)
pygame.mixer.music.set_volume(0.2)

def main():
    running = True
    pauseMenu = False
    holdingEsc = False
    menu = Menu(screen)
    renderOffset = [0, 0]
    screenShake = False
    screenShakeTimer = 0.5

    while running:
        screen.fill(Black)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        jump = keys[pygame.K_w] or keys[pygame.K_k] or keys[pygame.K_UP]

        right = 0
        if keys[pygame.K_a] or keys[pygame.K_h] or keys[pygame.K_LEFT]:
            right = -1
        elif keys[pygame.K_d] or keys[pygame.K_l] or keys[pygame.K_RIGHT]:
            right = 1

        if keys[pygame.K_ESCAPE]:
            if not holdingEsc:
                holdingEsc = True
                pauseMenu = not pauseMenu
        else:
            holdingEsc = False

        lManager.grid.render(screen)
        player.render(screen)

        if menu.exit:
            running = False

        if not menu.menuOpen and not transition.active:
            player.update(right, lManager.grid, screen, lManager.enemies, jump=jump)
            for enemy in lManager.enemies:
                if enemy.deadTime < 0.5 and enemy.deadTime != 0:
                    screenShake = True
                enemy.update(screen)

            timer.tick(screen)

            if not menu.mute:
                pygame.mixer.music.set_volume(0.2 + menu.soundChange)
            else:
                pygame.mixer.music.set_volume(0.0 + menu.soundChange)
            if player.rect.colliderect(lManager.goalRect):
                transition.start(timer.time)
                lManager.nextLevel()
                player.reset()
                menu.reset = True
            lManager.drawGoal(screen)
        else:
            if not menu.mute:
                pygame.mixer.music.set_volume(0.5 + menu.soundChange)
            else:
                pygame.mixer.music.set_volume(0.0)

        if menu.reset:
            player.reset()
            lManager.resetLevel()
            timer.reset()
            menu.reset = False

        fov.render(screen, [player.x + player.img.get_width() // 2, player.y + player.img.get_height() // 2])
        timer.render(screen)

        transition.update()
        transition.render(screen)
        menu.render()


        if screenShake:
            renderOffset[0] = random.randint(0, 8) - 4
            renderOffset[1] = random.randint(0, 8) - 4
            screenShakeTimer -= 0.5

        if screenShakeTimer <= 0:
            screenShake = False
            screenShakeTimer = 2
            renderOffset = [0, 0]

        cursor.render(screen)
        display.blit(screen, renderOffset)


        pygame.display.flip()
        clock.tick(Fps)
        print(player.x,player.y)
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
