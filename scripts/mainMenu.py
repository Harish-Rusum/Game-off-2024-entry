import pygame
import sys

class MainMenu:
    def __init__(self, screenWidth, screenHeight):
        pygame.font.init()
        self.active = True
        self.options = ["Start Game", "Instructions", "Quit"]
        self.selectedOption = 0
        self.font = pygame.font.Font("assets/Fonts/font.otf", 35)
        self.titleFont = pygame.font.Font("assets/Fonts/font.otf", 72)
        self.screenWidth = screenWidth
        self.screenHeight = screenHeight
        self.optionRects = []
        self.fadeAlpha = 255
        self.fadeSpeed = 7
        self.fadingOut = False

        self.buttonImage = pygame.transform.scale(
            pygame.image.load("assets/Buttons/button.png"), (300, 50)
        )

        self.directions = [(dx, dy) for dx in range(-1, 2)
                                      for dy in range(-1, 2)
                                      if (dx, dy) != (0, 0)]

        self.overlay = pygame.Surface((screenWidth, screenHeight), pygame.SRCALPHA)

    def outline(self, img, pos, color=(255, 255, 255)):
        mask = pygame.mask.from_surface(img)
        outlinePoints = mask.outline()
        for dx, dy in self.directions:
            for x, y in outlinePoints:
                if 0 <= pos[0] + x + dx < self.screenWidth and 0 <= pos[1] + y + dy < self.screenHeight:
                    self.overlay.set_at((pos[0] + x + dx, pos[1] + y + dy), color)

    def render(self, surf):
        surf.fill((0, 0, 0))
        self.overlay.fill((0, 0, 0, 0))

        titleText = self.titleFont.render("A dark escape", True, "#FFFFFF")
        surf.blit(titleText, (self.screenWidth // 2 - titleText.get_width() // 2, 50))

        mousePos = pygame.mouse.get_pos()
        self.optionRects = []

        for index, option in enumerate(self.options):
            optionRect = pygame.Rect(
                self.screenWidth // 2 - 150,
                200 + index * 70 - 7,
                300,
                50,
            )
            self.optionRects.append(optionRect)

            if optionRect.collidepoint(mousePos):
                self.selectedOption = index

            if index == self.selectedOption:
                self.outline(self.buttonImage, optionRect.topleft)
            else:
                self.outline(self.buttonImage, optionRect.topleft, color=(100, 100, 100))

            surf.blit(self.buttonImage, optionRect)

            text = self.font.render(option, True, "#FFFFFF")
            x = self.screenWidth // 2 - text.get_width() // 2
            y = 200 + index * 70
            surf.blit(text, (x, y))

        # Blit overlay (outlines)
        surf.blit(self.overlay, (0, 0))

        fadeSurface = pygame.Surface((self.screenWidth, self.screenHeight))
        fadeSurface.fill((0, 0, 0))
        if self.fadingOut:
            fadeSurface.set_alpha(self.fadeAlpha)
            surf.blit(fadeSurface, (0, 0))
            self.fadeAlpha += self.fadeSpeed
            if self.fadeAlpha >= 255:
                self.active = False
        elif self.fadeAlpha > 0:
            fadeSurface.set_alpha(self.fadeAlpha)
            surf.blit(fadeSurface, (0, 0))
            self.fadeAlpha -= self.fadeSpeed

    def navigate(self, direction):
        self.selectedOption = (self.selectedOption + direction) % len(self.options)

    def handleMouseClick(self, mousePos, cursor):
        for index, rect in enumerate(self.optionRects):
            if rect.collidepoint(mousePos):
                self.selectedOption = index
                self.select(cursor)

    def handleKeyboardInput(self, event, cursor):
        if event.key in [pygame.K_UP, pygame.K_w]:
            self.navigate(-1)
        elif event.key in [pygame.K_DOWN, pygame.K_s]:
            self.navigate(1)
        elif event.key == pygame.K_RETURN:
            self.select(cursor)

    def select(self, cursor):
        if self.selectedOption == 0:
            self.fadingOut = True
        elif self.selectedOption == 1:
            self.showInstructions(pygame.display.get_surface(), cursor)
        elif self.selectedOption == 2:
            pygame.quit()
            sys.exit()

    def showInstructions(self, surf, cursor):
        instructionScreen = True
        instructions = [
            "Instructions:",
            "    - Use Arrow Keys or WASD to move.",
            "    - Use the 'R' key to retry level (quick restart).",
            "    - Press ESC to pause.",
            "    - Avoid enemies and reach the goal!",
            "    - You can jump on enemies to kill them.",
            "    - (All enemies except spiked enemies)",
            "",
            "    - VERY important : Use the pause menu to :",
            "          - Go to next level",
            "          - Go to previous level",
            "          - Retry level",
            "          - Adjust all music related settings",
            "",
            "Press Enter to go back..."
        ]

        while instructionScreen:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        instructionScreen = False

            surf.fill("#000000")
            for i, line in enumerate(instructions):
                text = self.font.render(line, True, "#FFFFFF")
                surf.blit(text, (80, 80 + i * 30))
            cursor.render(surf)
            pygame.display.flip()

