import pygame

class Enemy:
    def __init__(self, pos, moveRange, num, dir):
        self.x = pos[0]
        self.y = pos[1]
        self.img = pygame.image.load(f"assets/Characters/tile_{num}.png").convert_alpha()
        self.img = pygame.transform.smoothscale(self.img, (40, 40))
        self.rect = self.img.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        self.rightMax = moveRange[1]
        self.leftMax = moveRange[0]
        self.direction = dir
        self.xVel = 0
        self.maxVel = 2
        self.acceleration = 0.05
        self.deceleration = 0.1

    def render(self, surf):
        surf.blit(self.img, self.rect)

    def move(self):
        if self.direction == "right":
            self.xVel = min(self.xVel + self.acceleration, self.maxVel)
            self.x += self.xVel
            if self.x >= self.rightMax:
                self.x = self.rightMax
                self.direction = "left"
                self.xVel = max(self.xVel - self.deceleration, 0)
        elif self.direction == "left":
            self.xVel = min(self.xVel + self.acceleration, self.maxVel)
            self.x -= self.xVel
            if self.x <= self.leftMax:
                self.x = self.leftMax
                self.direction = "right"
                self.xVel = max(self.xVel - self.deceleration, 0)

        self.rect.x = round(self.x)
        self.rect.y = self.y

    def update(self, surf):
        self.move()
        self.render(surf)
