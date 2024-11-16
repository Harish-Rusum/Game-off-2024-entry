import pygame
class Menu:
    def __init__(self, surf):
        self.menuOpen = False
        self.overlay = pygame.Surface(surf.get_size(), pygame.SRCALPHA)
        self.overlay.fill((0, 0, 0, 200))
        self.surf = surf
        self.holdingEsc = False
        self.buttons = [
            pygame.image.load("assets/Buttons/back.png").convert_alpha(),
            pygame.image.load("assets/Buttons/exit.png").convert_alpha(),
            pygame.image.load("assets/Buttons/mute.png").convert_alpha(),
            pygame.image.load("assets/Buttons/unmute.png").convert_alpha(),
            pygame.image.load("assets/Buttons/volUp.png").convert_alpha(),
            pygame.image.load("assets/Buttons/volDown.png").convert_alpha(),
        ]
        self.exit = False
        self.mute = False
        self.muteHeld = False
        self.volUpHeld = False
        self.volDownHeld = False
        self.soundChange = 0
        self.directions = [
            (-2, -2), (-2, -1), (-2, 0), (-2, 1), (-2, 2),
            (-1, -2), (-1, -1), (-1, 0), (-1, 1), (-1, 2),
            (0, -2), (0, -1), (0, 1), (0, 2),
            (1, -2), (1, -1), (1, 0), (1, 1), (1, 2),
            (2, -2), (2, -1), (2, 0), (2, 1), (2, 2),
        ]

    def outline(self, img, pos, color=(255, 255, 255)):
        mask = pygame.mask.from_surface(img)
        outline_points = mask.outline()

        for offset in self.directions:
            for point in outline_points:
                x, y = point
                outlinePos = (pos[0] + x + offset[0], pos[1] + y + offset[1])
                self.overlay.set_at(outlinePos, color)

    def click(self, i):
        if i == 0:
            self.menuOpen = False
        elif i == 1:
            self.exit = True
        elif i == 2:
            if not self.muteHeld:
                self.mute = not self.mute
                self.muteHeld = True
        elif i == 3:
            if not self.volUpHeld:
                self.soundChange += 0.1
                self.volUpHeld = True
        elif i == 4:
            if not self.volDownHeld:
                self.soundChange -= 0.1
                self.volDownHeld = True
        return

    def render(self):
        mouseX, mouseY = pygame.mouse.get_pos()
        keys = pygame.key.get_pressed()

        if keys[pygame.K_ESCAPE]:
            if not self.holdingEsc:
                self.holdingEsc = True
                self.menuOpen = not self.menuOpen
        else:
            self.holdingEsc = False

        self.overlay.fill((0, 0, 0, 200))

        for i, button in enumerate(self.buttons[:3] + self.buttons[4:] if not self.mute else self.buttons[:2] + self.buttons[3:]):
            button_scaled = pygame.transform.smoothscale(button, (button.get_width() * 1.5, button.get_height() * 1.5))
            button_x, button_y = 20, (i * 60 + 20)
            if button_x <= mouseX <= button_x + button_scaled.get_width() and \
               button_y <= mouseY <= button_y + button_scaled.get_height():
                self.outline(button_scaled, (button_x, button_y))
                if self.menuOpen and pygame.mouse.get_pressed()[0]:
                    self.click(i)
            else:
                self.outline(button_scaled, (button_x, button_y), color=(100, 100, 100))

            self.overlay.blit(button_scaled, (button_x, button_y))

        if not pygame.mouse.get_pressed()[0]:
            self.muteHeld = False
            self.volUpHeld = False
            self.volDownHeld = False

        if self.menuOpen:
            self.surf.blit(self.overlay, (0, 0))
