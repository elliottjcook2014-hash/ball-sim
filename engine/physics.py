import sys
from engine.objects import *
from engine.hooks import update_hooks


def update():
    dt = 1.0 / settings.sub_steps

    for _ in range(settings.sub_steps):
        for hook in update_hooks:
            hook()
        for ball in balls:
            ball.move(dt)
        check_collisions()


def start_sim():
    screen = pygame.display.set_mode([settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT])
    clock = pygame.time.Clock()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill(pygame.Color('black'))
        update()
        DrawAll(screen)
        pygame.display.flip()
        clock.tick(settings.fps)

    pygame.quit()

def check_collisions():
    for i in range(len(balls)):
        for j in range(i + 1, len(balls)):
            balls[i].collide_with_ball(balls[j])

    for ball in balls:
        for ring in rings:
            ball.collide_with_ring(ring)