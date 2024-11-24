import pygame
import time

class Transition:
    def __init__(self, duration=2, color="#000000"):
        self.duration = duration
        self.startTime = None
        self.active = False
        self.color = color
        self.alpha = 255  
        self.surface = None

    def start(self):
        self.startTime = time.time()
        self.active = True
        self.alpha = 255  

    def update(self):
        if self.active:
            currentTime = time.time()
            if self.startTime != None:
                elapsedTime = currentTime - self.startTime
                progress = elapsedTime / self.duration

                if progress >= 1.0:
                    self.active = False
                    self.alpha = 0  
                else:
                    
                    self.alpha = int(255 * (1 - progress))

    def render(self, surf):
        if self.active:
            if self.surface is None:
                self.surface = pygame.Surface(surf.get_size()).convert_alpha()
            self.surface.fill(self.color)
            self.surface.set_alpha(self.alpha)
            surf.blit(self.surface, (0, 0))
