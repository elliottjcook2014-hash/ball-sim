import pygame
import math
import library

pygame.init()

settings = library.PhysicsSettings()

SCREEN_WIDTH = SCREEN_HEIGHT = settings.SCREEN_WIDTH
FPS = settings.fps

screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
clock = pygame.time.Clock()
Ring = library.Ring
Ball = library.Ball

rings = [Ring(450, 5, pygame.Color('white'))]
balls = [
    Ball(radius=20, x=450, y=400, vx=6, vy=0, color=pygame.Color('red')),
    Ball(radius=35, x=550, y=400, vx=-4, vy=2, color=pygame.Color('blue')),
    Ball(radius=15, x=500, y=300, vx=2, vy=-5, color=pygame.Color('green'))
]

def check_collisions():
    for i in range(len(balls)):
        for j in range(i + 1, len(balls)):
            balls[i].collide_with_ball(balls[j])

    for ball in balls:
        for ring in rings:
            ball.collide_with_ring(ring)

def update():
    SUB_STEPS = 8
    dt = 1.0 / SUB_STEPS
    
    for _ in range(SUB_STEPS):
        for ball in balls:
            ball.move(dt)
        check_collisions()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(pygame.Color('black'))
    update()
    library.DrawAll(screen)
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()