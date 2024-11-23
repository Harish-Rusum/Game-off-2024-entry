import pygame

class Timer:
    def __init__(self, screenwidth, screenheight):
        self.time = 0
        self.font = pygame.font.SysFont("Arial", 48)
        
        self.x = screenwidth // 2
        self.y = screenheight // 2
        
        self.textWidth, self.textHeight = self.font.size("00:00")
        self.x -= self.textWidth // 2
        self.y -= self.textHeight // 2

    def formattime(self):
        minutes = self.time // 60
        seconds = self.time % 60
        return f"{minutes:02}:{seconds:02}"

    def render(self, surf):
        timeText = self.font.render(self.formattime(), True, (104, 104, 104))
        
        self.textWidth, self.textHeight = self.font.size(self.formattime())
        timeText.set_colorkey((0,0,0))
        surf.blit(timeText, (self.x, self.y))

    def tick(self, surf):
        self.time += 1
        self.render(surf)
