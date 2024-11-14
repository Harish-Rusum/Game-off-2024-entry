import pygame

class Menu:
    def __init__(self, surf):
        self.menuOpen = False
        self.overlay = pygame.Surface(surf.get_size(), pygame.SRCALPHA)
        self.overlay.fill((0, 0, 0, 200))
        self.surf = surf
        self.holdingEsc = False
        self.buttons = [
            pygame.image.load("assets/Buttons/back.png").convert_alpha(),
        ]
        self.directions = [
            (-1, -1), (-1, 0), (-1, 1),
            (0, -1), (0, 1),
            (1, -1), (1, 0), (1, 1),
        ]
    
    def outline(self, img, pos, color=(255, 255, 255)):
        mask = pygame.mask.from_surface(img)
        outline_points = mask.outline()
        
        for offset in self.directions:
            for point in outline_points:
                x, y = point
                outlinePos = (pos[0] + x + offset[0], pos[1] + y + offset[1])
                self.overlay.set_at(outlinePos, color)
    
    def render(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            if not self.holdingEsc:
                self.holdingEsc = True
                self.menuOpen = not self.menuOpen
        else:
            self.holdingEsc = False
            
        for i, button in enumerate(self.buttons):
            button_scaled = pygame.transform.scale2x(button)
            button_x, button_y = 20, (i * 64 + 20)
            
            self.outline(button_scaled, (button_x, button_y))
            self.overlay.blit(button_scaled, (button_x, button_y))

        if self.menuOpen:
            self.surf.blit(self.overlay, (0, 0))
