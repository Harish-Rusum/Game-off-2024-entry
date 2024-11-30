import pygame
import sys

class MainMenu:
    def __init__(self, screenWidth, screenHeight):
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

    def render(self, surf):
        titleText = self.titleFont.render("A dark escape", True, "#FFFFFF")
        surf.blit(titleText, (self.screenWidth // 2 - titleText.get_width() // 2, 50))

        mousePos = pygame.mouse.get_pos()
        self.optionRects = []

        for index, option in enumerate(self.options):
            optionRect = pygame.Rect(
                self.screenWidth // 2 - 150,
                200 + index * 60 - 7,
                300,
                50,
            )
            self.optionRects.append(optionRect)

            if optionRect.collidepoint(mousePos):
                self.selectedOption = index

            if index == self.selectedOption:
                pygame.draw.rect(
                    surf,
                    "#3c9349",
                    optionRect,
                    border_radius=10,
                )
            else:
                pygame.draw.rect(
                    surf,
                    "#2a2a2a",
                    optionRect,
                    border_radius=10,
                )

            text = self.font.render(option, True, "#FFFFFF")
            x = self.screenWidth // 2 - text.get_width() // 2
            y = 200 + index * 60
            surf.blit(text, (x, y))

        fadeSurface = pygame.Surface((self.screenWidth, self.screenHeight))
        # fadeSurface.fill((0, 0, 0))

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

    def handleMouseClick(self, mousePos):
        for index, rect in enumerate(self.optionRects):
            if rect.collidepoint(mousePos):
                self.selectedOption = index
                self.select()

    def handleKeyboardInput(self, event):
        if event.key in [pygame.K_UP, pygame.K_w]:
            self.navigate(-1)
        elif event.key in [pygame.K_DOWN, pygame.K_s]:
            self.navigate(1)
        elif event.key == pygame.K_RETURN:
            self.select()

    def select(self):
        if self.selectedOption == 0:
            self.fadingOut = True
        elif self.selectedOption == 1:
            self.showInstructions(pygame.display.get_surface())
        elif self.selectedOption == 2:
            pygame.quit()
            sys.exit()

    def showInstructions(self, surf):
        instructionScreen = True
        instructions = [
            "Instructions:",
            "    - Use Arrow Keys or WASD to move.",
            "    - Press ESC to pause.",
            "    - Avoid enemies and reach the goal!",
            "    - You can jump on enemies to kill them.",
            "    - (All enemies except spiked enemies)",
            "",
            "    - VERY important : Use the pause menu to :",
            "          - Next level",
            "          - Previous level",
            "          - Retry level",
            "          - All music related settings",
            "",
            "Press Enter to return..."
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
                surf.blit(text, (50, 100 + i * 30))
            pygame.display.flip()
