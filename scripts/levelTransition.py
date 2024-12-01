
import pygame
import time


class Transition:
    def __init__(self, duration=1, color=(0, 0, 0)):
        self.duration = duration
        self.startTime = None
        self.active = False
        self.color = color
        self.alpha = 255
        self.surface = None
        self.done = False
        self.font = pygame.font.Font("assets/Fonts/font.otf", 70)
        self.counter = 0
        self.showText = True

    def start(self, timeSpent):
        self.startTime = None 
        self.active = True
        self.alpha = 255
        self.timer = timeSpent
        self.done = False
        self.counter = 0
        self.showText = True

    def update(self):
        if self.active:
            self.counter += 1 

            if self.counter > 75:
                self.showText = False

            if self.counter > 75:
                if self.startTime is None: 
                    self.startTime = time.time()

                currentTime = time.time()
                elapsedTime = currentTime - self.startTime
                progress = min(elapsedTime / self.duration, 1.0)
                self.alpha = int(255 * (1 - progress))

                if progress >= 1.0:
                    self.active = False
                    self.done = True
                    self.counter = 0

    def render(self, surf):
        if self.active or self.done:
            if self.surface is None:
                self.surface = pygame.Surface(surf.get_size(), pygame.SRCALPHA)
            self.surface.fill(self.color + (self.alpha,))

            surf.blit(self.surface, (0, 0))

            if self.showText:
                minutes = self.timer // 60
                seconds = self.timer % 60
                timeText = self.font.render(
                    f"Level Cleared: {minutes:02}:{seconds:02}", True, (200, 200, 200)
                )
                textPos = (
                    surf.get_width() // 2 - timeText.get_width() // 2,
                    surf.get_height() // 2 - timeText.get_height() // 2 - 50,
                )
                surf.blit(timeText, textPos)
