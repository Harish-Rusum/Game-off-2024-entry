import pygame

class Menu:
    def __init__(self,surf):
        self.menuOpen = False
        self.overlay = pygame.surface.Surface(surf.get_size(), pygame.SRCALPHA)
        self.overlay.fill((0,0,0,128))
        self.surf = surf
        self.holdingEsc = False

    def render(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            if not self.holdingEsc:
                self.holdingEsc = True
                self.menuOpen = not self.menuOpen
        else:
            self.holdingEsc = False

        if self.menuOpen:
            self.surf.blit(self.overlay, (0,0))
