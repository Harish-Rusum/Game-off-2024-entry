import pygame
import time

class Transition:
    def __init__(self, screen, duration=2):
        self.screen = screen
        self.duration = duration
        self.start_time = None
        self.active = False

    def start(self):
        """
        Starts the transition.
        """
        self.start_time = time.time()
        self.active = True

    def update(self):
        if self.active:
            current_time = time.time()
            elapsed_time = current_time - self.start_time
            if elapsed_time >= self.duration:
                self.active = False

    def render(self):
        if self.active:
            self.screen.fill("#000000")
            pygame.display.flip()
