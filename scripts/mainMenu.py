import pygame
import sys

class MainMenu:
    def __init__(self, screen_width, screen_height):
        self.active = True
        self.options = ["Start Game", "Instructions", "Quit"]
        self.selectedOption = 0
        self.font = pygame.font.Font(None, 48)
        self.titleFont = pygame.font.Font(None, 72)
        self.screenWidth = screen_width
        self.screenHeight = screen_height

    def render(self, surf):
        surf.fill("#000000")
        title_text = self.titleFont.render("Untitled game", True, "#FFFFFF")
        surf.blit(title_text, (self.screenWidth // 2 - title_text.get_width() // 2, 50))

        for index, option in enumerate(self.options):
            if index == self.selectedOption:
                pygame.draw.rect(
                    surf,
                    "#3c9349",
                    (
                        self.screenWidth // 2 - 150,
                        200 + index * 60 - 10,
                        300,
                        50,
                    ),
                    border_radius=10,
                )
            text = self.font.render(option, True, "#FFFFFF")
            x = self.screenWidth // 2 - text.get_width() // 2
            y = 200 + index * 60
            surf.blit(text, (x, y))

    def navigate(self, direction):
        self.selectedOption = (self.selectedOption + direction) % len(self.options)

    def select(self):
        if self.selectedOption == 0:
            self.active = False
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
            "    - You can jump on enemies to kill them",
            "    - (If they dont have a spike on their head)",
            "Press enter to return..."
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
                surf.blit(text, (50, 100 + i * 40))
            pygame.display.flip()
