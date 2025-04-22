import pygame
from utils.spritesheet import SpriteSheet

class Player:
    def __init__(self, playerX, playerY, charNum, spawnX, spawnY):
        self.playerX = playerX
        self.playerY = playerY
        self.charNum = charNum
        self.spawnX = spawnX
        self.spawnY = spawnY
        self.reset()

    def reset(self):
        self.x = self.spawnX
        self.y = self.spawnY
        self.state = "grounded"
        self.spriteSheet = SpriteSheet()
        self.sheet = self.spriteSheet.split(f"assets/Characters/character{self.charNum}.png", 1, 4, 24, 24)
        self.frame = 0
        self.animationFrames = 4
        self.direction = 0
        self.counter = 0
        self.img = self.sheet[self.frame]
        self.img = pygame.transform.smoothscale(self.img, (self.playerX, self.playerY))
        self.rect = self.img.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        self.acc = 0.8
        self.decc = 0.5
        self.maxspeed = 5
        self.xVel = 0
        self.yVel = 0
        self.gravityAcc = 0.6
        self.terminalVel = 8
        self.jumpStrength = -11
        self.maxJumps = 1
        self.jumpsRemaining = self.maxJumps
        self.jumpHeld = False
        self.coyoteTime = 0.15
        self.coyoteTimer = 0
        self.groundedBuffer = False
        self.extraJumpStrength = 1.5
        self.deadTime = 0.1
        self.dead = False

    def respawn(self):
        self.x = self.spawnX
        self.y = self.spawnY
        self.rect.x = self.x
        self.rect.y = self.y
        self.state = "grounded"
        self.yVel = 0

    def render(self, surf, offset=[0, 0]):
        img = self.sheet[self.frame]
        img = pygame.transform.smoothscale(img, (self.playerX, self.playerY))
        if self.direction == -1:
            img = pygame.transform.rotate(img, -180)
            img = pygame.transform.flip(img, False, True)
        surf.blit(img, (self.x + offset[0], self.y + offset[1]))

    def gravity(self, grid, enemies, deltaTime):
        self.yVel = min(self.yVel + self.gravityAcc, self.terminalVel)
        self.rect.y += int(self.yVel)

        surroundingTiles = grid.getSurroundingTiles(self.x, self.y)
        isGrounded = False

        for tile in surroundingTiles:
            tileRect = pygame.Rect(tile[2][0], tile[2][1], grid.tileSize, grid.tileSize)
            if tile[0][0] != -1 and self.rect.colliderect(tileRect):
                if self.yVel > 0: 
                    self.rect.bottom = tileRect.top
                    self.yVel = 0
                    isGrounded = True
                elif self.yVel < 0:
                    self.rect.top = tileRect.bottom
                    self.yVel = 0
                break

        if isGrounded:
            self.state = "grounded"
            self.jumpsRemaining = self.maxJumps
            self.coyoteTimer = 0
        else:
            if self.state == "grounded":
                self.coyoteTimer += deltaTime
            if self.coyoteTimer > self.coyoteTime:
                self.state = "airborne"

        for enemy in enemies:
            enemyMask = pygame.mask.from_surface(enemy.frames[enemy.state])
            playerMask = pygame.mask.from_surface(self.img)
            offset = (self.x - enemy.x, self.y - enemy.y)
            overlap = playerMask.overlap(enemyMask, offset)

            if overlap:
                if not enemy.dead:
                    if self.state == "airborne" and self.yVel > 0:
                        if enemy.enemyType != 3:
                            enemy.die()
                            self.yVel = self.jumpStrength - self.extraJumpStrength
                        else:
                            self.respawn()
                            self.dead = True
                            return
                    else:
                        self.respawn()
                        self.dead = True
                        return
        if self.deadTime == 0:
            self.dead = False
            self.deadTime = 0.1
        if self.dead:
            self.deadTime = max(self.deadTime - (1/60),0)
        self.y = self.rect.y

    def jump(self):
        canJump = (
            (self.state == "grounded" or self.coyoteTimer < self.coyoteTime)
            and self.jumpsRemaining > 0
        )

        if canJump:
            self.yVel = self.jumpStrength
            self.state = "airborne"
            if self.jumpsRemaining > 0:
                self.jumpsRemaining -= 1
            self.coyoteTimer = self.coyoteTime

    def moveX(self, dx, grid, screen):
        if dx != 0:
            self.xVel += self.acc * dx
            self.xVel = max(-self.maxspeed, min(self.xVel, self.maxspeed))
        else:
            if self.xVel > 0:
                self.xVel = max(self.xVel - self.decc, 0)
            elif self.xVel < 0:
                self.xVel = min(self.xVel + self.decc, 0)

        if dx > 0:
            self.direction = 0
        elif dx < 0:
            self.direction = -1

        if self.counter % 5 == 0:
            self.frame = (self.frame + 1) % self.animationFrames
        self.counter += 1

        newX = self.x + self.xVel
        self.rect.x = int(newX)
        surrounding = grid.getSurroundingTiles(self.x, self.y)

        for element in surrounding:
            tileRect = pygame.Rect(element[2][0], element[2][1], grid.tileSize, grid.tileSize)
            if element[0][0] != -1 and self.rect.colliderect(tileRect):
                if self.xVel > 0:
                    self.rect.right = tileRect.left
                elif self.xVel < 0:
                    self.rect.left = tileRect.right
                self.xVel = 0
                break

        self.x = self.rect.x
        self.x = max(0, min(self.x, screen.get_width() - self.playerX))

    def update(self, dx, grid, screen, enemies, delta_time, jump=False):
        self.render(screen)
        self.moveX(dx, grid, screen)
        self.gravity(grid, enemies, delta_time)
        if jump:
            if not self.jumpHeld:
                self.jumpHeld = True
                self.jump()
        else:
            self.jumpHeld = False
