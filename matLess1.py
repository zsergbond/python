import pygame

FPS = 60

pygame.init()
screen = pygame.display.set_mode((800,600))
pygame.display.set_caption('Diskretnay Matematika')
clock = pygame.time.Clock()

run = True

while run:
    for i in pygame.event.get():
        if i.type == pygame.QUIT:
            exit()