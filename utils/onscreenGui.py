import pygame

class OnscreenGui:
    def __init__(self, screenWidth, screenHeight):
        self.time = 0
        self.font = pygame.font.Font("assets/Fonts/font.otf", 50)
        self.helpFont = pygame.font.Font("assets/Fonts/font.otf", 24)
        
        timerPlaceholder = "00:00"
        helpText = "r -> restart"

        self.textWidth, self.textHeight = self.font.size(timerPlaceholder)
        self.helpTextWidth, self.helpTextHeight = self.helpFont.size(helpText)

        self.x = screenWidth - self.textWidth - 50
        self.y = 50 - self.textHeight // 2

        self.helpTextX = self.x + (self.textWidth - self.helpTextWidth) // 2
        self.helpTextY = self.y + self.textHeight + 5
        self.helpText = helpText

    def reset(self):
        self.time = 0

    def formatTime(self):
        minutes = self.time // 60
        seconds = self.time % 60
        return f"{minutes:02}:{seconds:02}"

    def render(self, surf):
        timeText = self.font.render(self.formatTime(), True, (104, 104, 104))
        timeText.set_colorkey((0, 0, 0))
        surf.blit(timeText, (self.x, self.y))

        helpText = self.helpFont.render(self.helpText, True, (104, 104, 104))
        helpText.set_colorkey((0, 0, 0))
        surf.blit(helpText, (self.helpTextX, self.helpTextY))

    def tick(self, surf):
        self.time += 1
        self.render(surf)

