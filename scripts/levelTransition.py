import pygame
import time


class Transition:
    def __init__(self, duration=2, color=(0, 0, 0)):
        self.duration = duration
        self.startTime = None
        self.active = False
        self.color = color
        self.alpha = 255
        self.surface = None
        self.continuePressed = False

        # Load and scale images
        self.image1 = pygame.image.load("assets/Buttons/retry.png").convert_alpha()
        self.image1 = pygame.transform.smoothscale(
            self.image1,
            (int(2.5 * self.image1.get_width()), int(2.5 * self.image1.get_height())),
        )
        self.image2 = pygame.image.load("assets/Buttons/continue.png").convert_alpha()
        self.image2 = pygame.transform.smoothscale(
            self.image2,
            (int(2.5 * self.image2.get_width()), int(2.5 * self.image2.get_height())),
        )

        self.directions = [
            (dx, dy) for dx in range(-1, 2) for dy in range(-1, 2) if (dx, dy) != (0, 0)
        ]
        self.timer = 0
        self.font = pygame.font.Font("assets/Fonts/font.ttf", 70)

    def outline(self, surf, img, pos, color=(255, 255, 255)):
        mask = pygame.mask.from_surface(img)
        outlinePoints = mask.outline()
        for dx, dy in self.directions:
            for x, y in outlinePoints:
                outlinePos = (pos[0] + x + dx, pos[1] + y + dy)
                if (
                    0 <= outlinePos[0] < surf.get_width()
                    and 0 <= outlinePos[1] < surf.get_height()
                ):
                    surf.set_at(outlinePos, color)

    def start(self, timeSpent):
        self.startTime = time.time()
        self.active = True
        self.alpha = 255
        self.timer = timeSpent

    def update(self):
        if self.active and self.continuePressed:
            currentTime = time.time()
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
                self.surface = pygame.Surface(surf.get_size(), pygame.SRCALPHA)
            self.surface.fill(self.color + (self.alpha,))
            surf.blit(self.surface, (0, 0))
            if not self.continuePressed:
                image1_pos = (
                    surf.get_width() // 2 - self.image1.get_width() // 2,
                    surf.get_height() // 2 - self.image1.get_height() // 2,
                )
                image2_pos = (
                    surf.get_width() // 2 - self.image2.get_width() // 2,
                    surf.get_height() // 2 - self.image2.get_height() // 2 + 100,
                )

                mouseX, mouseY = pygame.mouse.get_pos()
                mousePressed = pygame.mouse.get_pressed()

                if (
                    image1_pos[0] < mouseX < image1_pos[0] + self.image1.get_width()
                    and image1_pos[1] < mouseY < image1_pos[1] + self.image1.get_height()
                ):
                    self.outline(surf, self.image1, image1_pos, color=(255, 255, 255))
                else:
                    self.outline(surf, self.image1, image1_pos, color=(100, 100, 100))

                if (
                    image2_pos[0] < mouseX < image2_pos[0] + self.image2.get_width()
                    and image2_pos[1] < mouseY < image2_pos[1] + self.image2.get_height()
                ):
                    self.outline(surf, self.image2, image2_pos, color=(255, 255, 255))
                    if mousePressed[0] and not self.continuePressed:
                        self.continuePressed = True
                        self.startTime = time.time()
                        self.active = True
                else:
                    self.outline(surf, self.image2, image2_pos, color=(100, 100, 100))

                surf.blit(self.image1, image1_pos)
                surf.blit(self.image2, image2_pos)
                minutes = self.timer // 60
                seconds = self.timer % 60
                timeText = self.font.render(
                    f"Time : {minutes:02}:{seconds:02}", True, (104, 104, 104)
                )
                textPos = (
                    surf.get_width() // 2 - timeText.get_width() // 2,
                    surf.get_height() // 2 - timeText.get_height() // 2 - 150,
                )
                surf.blit(timeText, textPos)
        if not self.active:
            self.continuePressed = False
