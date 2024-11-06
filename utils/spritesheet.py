import pygame

class SpriteSheet:
    def __init__(self) -> None:
        pass

    def split(self, sheetPath, rows, cols, tileWidth, tileHeight):
        images = []
        sheet = pygame.image.load(sheetPath).convert_alpha()

        for j in range(rows):
            for i in range(cols):
                sliceRect = pygame.Rect(i * tileWidth, j * tileHeight, tileWidth, tileHeight)
                
                if sliceRect.right <= sheet.get_width() and sliceRect.bottom <= sheet.get_height():
                    sliceImage = sheet.subsurface(sliceRect).copy()
                    images.append(sliceImage)
                else:
                    print(f"Skipping tile at ({i}, {j}) - outside surface area")
                
        return images
