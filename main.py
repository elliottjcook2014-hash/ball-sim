import pygame
import math

pygame.init()

SCREEN_WIDTH = SCREEN_HEIGHT = 1000
FPS = 60

screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
clock = pygame.time.Clock()

GRAVITY = 0.2
FRICTION = 1.0 
RESTITUTION = 1

class Ring():
    def __init__(self, radius=(SCREEN_WIDTH / 2), width=5, color: pygame.Color = pygame.Color('white')):
        self.radius = radius
        self.width = width
        self.color = color
        self.x = SCREEN_WIDTH // 2
        self.y = SCREEN_HEIGHT // 2

    def draw(self):
        if self.radius > self.width:
            pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), int(self.radius), self.width)

class Ball():
    def __init__(self, radius=20, x=0, y=0, vx=0, vy=0, color: pygame.Color = pygame.Color('red')):
        self.x = float(x)
        self.y = float(y)
        self.radius = radius
        self.vx = float(vx)
        self.vy = float(vy)
        self.color = color
        
        self.mass = math.pi * (radius ** 2)

    def move(self, dt):
        self.vy += GRAVITY * dt
        
        self.vx *= FRICTION
        self.vy *= FRICTION

        self.x += self.vx * dt
        self.y += self.vy * dt

    def collide_with_ball(self, other):
        dx = other.x - self.x
        dy = other.y - self.y
        distance = math.hypot(dx, dy)
        min_dist = self.radius + other.radius

        if distance < min_dist and distance > 0:
            nx = dx / distance
            ny = dy / distance
            overlap = min_dist - distance
            
            m_total = self.mass + other.mass
            self.x -= nx * overlap * (other.mass / m_total)
            self.y -= ny * overlap * (other.mass / m_total)
            other.x += nx * overlap * (self.mass / m_total)
            other.y += ny * overlap * (self.mass / m_total)

            kx = self.vx - other.vx
            ky = self.vy - other.vy

            p = 2 * (nx * kx + ny * ky) / (self.mass + other.mass)

            self.vx -= p * other.mass * nx
            self.vy -= p * other.mass * ny
            other.vx += p * self.mass * nx
            other.vy += p * self.mass * ny

    def collide_with_ring(self, ring):
        dx = self.x - ring.x
        dy = self.y - ring.y
        distance = math.hypot(dx, dy)
        max_dist = ring.radius - self.radius

        if distance > max_dist and distance > 0:
            nx = dx / distance
            ny = dy / distance

            self.x = ring.x + nx * max_dist
            self.y = ring.y + ny * max_dist

            dot_product = self.vx * nx + self.vy * ny
            if dot_product > 0:
                self.vx -= (1 + RESTITUTION) * dot_product * nx
                self.vy -= (1 + RESTITUTION) * dot_product * ny

    def draw(self):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)

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

    for ring in rings:
        ring.draw()
    for ball in balls:
        ball.draw()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(pygame.Color('black'))
    update()
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()