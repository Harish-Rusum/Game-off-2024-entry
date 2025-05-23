import pygame
class Menu:
    def __init__(self, surf):
        self.menuOpen = False
        self.font = pygame.font.Font("assets/Fonts/font.otf", 25)
        self.surf = surf
        self.overlay = pygame.Surface(surf.get_size(), pygame.SRCALPHA)
        self.overlay.fill((0, 0, 0, 200))
        self.holdingEsc = False
        self.reset = False
        self.gameOver = False

        rawButtons = [
            "button.png","button.png","button.png","button.png","button.png","button.png","button.png","button.png","button.png",
        ]
        self.buttons = [
            pygame.transform.smoothscale(
                pygame.image.load(f"assets/Buttons/{name}").convert_alpha(),
                (118 * 1.5, 16*1.5)
            ) for name in rawButtons
        ]
        self.exit = False
        self.mute = False
        self.buttonStates = [
            (self.buttons[:3] + self.buttons[4:]),
            (self.buttons[:2] + self.buttons[3:])
        ]
        self.selected = 0
        self.muteHeld = False
        self.volUpHeld = False
        self.volDownHeld = False
        self.upHeld = False
        self.downHeld = False
        self.enterHeld = False
        self.soundChange = 0
        self.nextLevel = False
        self.prevLevel = False
        self.holdingNext = False
        self.holdingPrev = False

        self.directions = [(dx, dy) for dx in range(-1, 2) for dy in range(-1, 2) if (dx, dy) != (0, 0)]

    def outline(self, img, pos, color=(255, 255, 255)):
        mask = pygame.mask.from_surface(img)
        outlinePoints = mask.outline()
        for dx, dy in self.directions:
            for x, y in outlinePoints:
                self.overlay.set_at((pos[0] + x + dx, pos[1] + y + dy), color)

    def click(self, i):
        if i == 0:
            self.menuOpen = False
        elif i == 1:
            self.exit = True
        elif i == 2 and not self.muteHeld:
            self.mute = not self.mute
            self.muteHeld = True
        elif i == 3 and not self.volUpHeld:
            self.soundChange += 0.1
            self.volUpHeld = True
        elif i == 4 and not self.volDownHeld:
            self.soundChange -= 0.1
            self.volDownHeld = True
        if i == 5:
            self.reset = True
            self.menuOpen = False
        if i == 6:
            if not self.holdingPrev:
                self.prevLevel = True
                self.holdingPrev = True
        if i == 7:
            if not self.holdingNext:
                self.nextLevel = True
                self.holdingNext = True

    def render(self):
        mouseX, mouseY = pygame.mouse.get_pos()
        keys = pygame.key.get_pressed()

        if keys[pygame.K_UP]:
            if self.upHeld == False:
                self.selected = (self.selected - 1) % (len(self.buttons) - 1)
                self.upHeld = True
        else:
            self.upHeld = False

        if keys[pygame.K_DOWN]:
            if self.downHeld == False:
                self.selected = (self.selected + 1) % (len(self.buttons) - 1)
                self.downHeld = True
        else:
            self.downHeld = False

        if keys[pygame.K_RETURN]:
            if self.enterHeld == False:
                self.click(self.selected)
                self.enterHeld = True
        else:
            self.enterHeld = False

        if keys[pygame.K_ESCAPE]:
            if not self.holdingEsc:
                self.menuOpen = not self.menuOpen
                self.holdingEsc = True
        else:
            self.holdingEsc = False

        if self.menuOpen:
            self.overlay.fill((0, 0, 0, 200))

            activeButtons = self.buttonStates[self.mute]
            labels = ["Back", "Quit", "Mute", "Volume up", "Volume down", "Restart", "Prev Level", "Next Level"]

            for i, button in enumerate(activeButtons):
                buttonX, buttonY = 20, (i * 50 + 20)

                buttonRect = pygame.Rect(buttonX, buttonY, button.get_width(), button.get_height())
                if buttonRect.collidepoint(mouseX, mouseY):
                    self.selected = i
                    if pygame.mouse.get_pressed()[0]:
                        self.click(i)
                else:
                    self.outline(button, (buttonX, buttonY), color=(100, 100, 100))

                self.overlay.blit(button, (buttonX, buttonY))

                labelText = labels[i] if i < len(labels) else "button"
                label = self.font.render(labelText, True, (104, 104, 104))
                label.set_colorkey((0, 0, 0))
                self.overlay.blit(label, (buttonX + 15, buttonY))

            if self.selected is not None:
                self.outline(self.buttonStates[self.mute][self.selected], (20, self.selected * 50 + 20))

            if not pygame.mouse.get_pressed()[0]:
                self.muteHeld = self.volUpHeld = self.volDownHeld = False

            self.surf.blit(self.overlay, (0, 0))
