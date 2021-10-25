import pygame

pygame.font.init()
screen = pygame.display.set_mode((500, 600))
pygame.display.set_caption("Sudoku")
# img = pygame.image.load('icon.png')
# pygame.display.set_icon(img)

run = True

while run:
    screen.fill((255, 255, 255))

pygame.quit()