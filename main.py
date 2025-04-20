import pygame
import random
import sys
import asyncio

from scripts.mainMenu import MainMenu
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

display = pygame.display.set_mode((ScreenX, ScreenY),pygame.SRCALPHA)
screen = pygame.surface.Surface((ScreenX, ScreenY),pygame.SRCALPHA)
pygame.display.set_caption("A dark escape")
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

bg = pygame.image.load("assets/Backgrounds/bg.png").convert_alpha()
bg = pygame.transform.scale_by(bg, (0.812, 0.82))

playerDeath = pygame.mixer.Sound('assets/Music/playerDeath.mp3')
playerDeath.set_volume(0.2)
channel1 = pygame.mixer.Channel(2)

nextLevel = pygame.mixer.Sound('assets/Music/nextLevel.mp3')
nextLevel.set_volume(0.5)
channel2 = pygame.mixer.Channel(3)

async def main():
    running = True
    pauseMenu = False
    holdingEsc = False
    menu = Menu(screen)
    renderOffset = [0, 0]
    screenShake = False
    screenShakeTimer = 0.5
    mainMenu = MainMenu(ScreenX, ScreenY)

    previous_time = pygame.time.get_ticks() / 1000

    while mainMenu.active:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                mainMenu.handleKeyboardInput(event,cursor)
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mainMenu.handleMouseClick(pygame.mouse.get_pos(),cursor)

        screen.blit(bg, (0,0))
        mainMenu.render(screen)
        cursor.render(screen)
        display.blit(screen, (0, 0))
        pygame.display.flip()
        clock.tick(Fps)


    cursor.render(screen)

    while running:
        current_time = pygame.time.get_ticks() / 1000
        deltaTime = current_time - previous_time
        previous_time = current_time

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
        t = True 
        if not menu.menuOpen and not transition.active:
            player.update(right, lManager.grid, screen, lManager.enemies, deltaTime, jump=jump)
            for enemy in lManager.enemies:
                if enemy.deadTime < 0.5 and enemy.deadTime != 0:
                    screenShake = True
                    t = False
                enemy.update(screen, deltaTime)
            if t:
                screenShake = False

            timer.tick(screen)

            if not menu.mute:
                pygame.mixer.music.set_volume(0.2 + menu.soundChange)
            else:
                pygame.mixer.music.set_volume(0.0 + menu.soundChange)
            if lManager.checkNextLevel(player):
                transition.start(timer.time)
                lManager.nextLevel()
                channel2.play(nextLevel)
                player.reset()
                menu.reset = True

            if player.dead:
                if not channel1.get_busy():
                    channel1.play(playerDeath)
        else:
            if not menu.mute:
                pygame.mixer.music.set_volume(0.5 + menu.soundChange)
            else:
                pygame.mixer.music.set_volume(0.0)
            for enemy in lManager.enemies:
                enemy.render(screen, [0,0])

        if menu.nextLevel:
            if lManager.currentLevel != len(list(lManager.levels.keys())):
                lManager.nextLevel()
                # channel2.play(nextLevel)
                player.reset()
                menu.nextLevel = False
                menu.menuOpen = False
                timer.reset()
                menu.holdingNext = False

        if menu.prevLevel:
            if lManager.currentLevel > 1:
                lManager.prevLevel()
                player.reset()
                menu.prevLevel = False
                menu.menuOpen = False
                timer.reset()
                menu.holdingPrev = False

        lManager.drawGoal(screen)
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
            screenShakeTimer -= deltaTime

        if screenShakeTimer <= 0:
            screenShake = False
            screenShakeTimer = 2
            renderOffset = [0, 0]

        cursor.render(screen)
        display.blit(screen, renderOffset)

        pygame.display.flip()
        clock.tick(Fps)

    await asyncio.sleep(0)

if __name__ == "__main__":
    asyncio.run(main())
