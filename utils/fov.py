import pygame

class Overlay:
    def __init__(self, screenX, screenY, rad, center):
        self.ScreenX = screenX
        self.ScreenY = screenY
        self.ScreenSize = (screenX, screenY)
        self.FovRad = rad
        self.Center = center

    def update(self, new_center):
        """Update the center of the overlay to follow the character's position."""
        self.Center = new_center

    def render(self, screen):
        overlay = pygame.Surface(self.ScreenSize, pygame.SRCALPHA)  
        overlay.fill((0, 0, 0, 255))

        for i in range(self.FovRad):
            alpha = int(255 * (1 - (i / self.FovRad))) 
            pygame.draw.circle(overlay, (0, 0, 0, alpha), self.Center, self.FovRad - i)
        
        screen.blit(overlay, (0, 0))
        return overlay
