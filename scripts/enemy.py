import pygame

class Enemy:
    def __init__(self, pos, moveRange, num, dir):
        self.x = pos[0]
        self.y = pos[1]
        self.characters = {
            1 : [
                pygame.transform.smoothscale(pygame.image.load('assets/Characters/tile_0018.png').convert_alpha(), (40,40)),
                pygame.transform.smoothscale(pygame.image.load('assets/Characters/tile_0019.png').convert_alpha(), (40,40)),
                pygame.transform.smoothscale(pygame.image.load('assets/Characters/tile_0020.png').convert_alpha(), (40,40)),
            ]
        }
        self.frames = self.characters[num]
        self.state = 0
        self.rect = self.frames[self.state].get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        self.rightMax = moveRange[1]
        self.leftMax = moveRange[0]
        self.direction = dir
        self.xVel = 0
        self.maxVel = 2
        self.acceleration = 0.05
        self.deceleration = 0.1
        self.dead = False
        self.deadTime = 0.1
        self.animationTimer = 0

    def render(self, surf):
        surf.blit(self.frames[self.state], self.rect)

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
        if self.animationTimer % 10 == 0:
            self.state = (self.state+1) % 2

        self.rect.x = round(self.x)
        self.rect.y = self.y

    def die(self):
        self.dead = True
        self.state = 2

    def update(self, surf):
        if self.dead == False:
            self.move()
        else:
            self.deadTime = max(0, self.deadTime - (1/60))
        if self.deadTime > 0:
            self.render(surf)
        self.animationTimer = (self.animationTimer + 1) % 1000
