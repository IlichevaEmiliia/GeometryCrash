import pygame
from gc_proj import game_function

if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((1900, 600))
    game_function()