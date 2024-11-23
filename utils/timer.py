import pygame

class Timer:
    def __init__(self, screenwidth, screenheight):
        self.time = 0
        self.font = pygame.font.Font("assets/Fonts/font.ttf", 50)
        
        self.y = 50
        self.x = screenwidth
        
        self.textWidth, self.textHeight = self.font.size("00:00")

        self.x -= self.textWidth + 50
        self.y -= self.textHeight // 2

    def reset(self):
        self.time = 0

    def formatTime(self):
        minutes = self.time // 60
        seconds = self.time % 60
        return f"{minutes:02}:{seconds:02}"

    def render(self, surf):
        timeText = self.font.render(self.formatTime(), True, (104, 104, 104))
        
        self.textWidth, self.textHeight = self.font.size(self.formatTime())
        timeText.set_colorkey((0,0,0))
        surf.blit(timeText, (self.x, self.y))

    def tick(self, surf):
        self.time += 1
        self.render(surf)
