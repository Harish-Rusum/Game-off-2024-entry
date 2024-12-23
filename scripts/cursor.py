import pygame
class Cursor:
    def __init__(self) -> None:
        self.img = pygame.image.load("assets/Cursor/cursor.png").convert_alpha()
        self.img = pygame.transform.smoothscale(self.img, (self.img.get_width() // 2, self.img.get_height() // 2))

    def render(self,surf):
        mousex,mousey = pygame.mouse.get_pos()
        if pygame.mouse.get_focused():
            mousex, mousey = pygame.mouse.get_pos()
            surf.blit(self.img, (mousex, mousey))
