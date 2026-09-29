import pygame
import math
from dataclasses import dataclass

# Definitions for the game constants
@dataclass
class PhysicsSettings:
    gravity: float = 0.2
    friction: float = 1.0
    restitution: float = 1.0
    sub_steps: int = 8 # how many physics calculations in between the frames
    screen_width: int = 1000
    screen_height: int = 1000
    fps: int = 60 # recommended to keep at 60
    SCREEN_WIDTH: int = 1000
    SCREEN_HEIGHT: int = 1000

# Only edit these if you know what you are doing!

settings = PhysicsSettings()

game_objects = []
balls = []
rings = []

class GameObject:
    def __init__(self):
        game_objects.append(self)

    def draw(self, surface: pygame.Surface):
        pass

class Ring(GameObject):
    def __init__(self, radius=(settings.SCREEN_WIDTH / 2), width=5, color: pygame.Color = pygame.Color('white')):
        super().__init__()
        self.radius = radius
        self.width = width
        self.color = color
        self.x = settings.SCREEN_WIDTH // 2
        self.y = settings.SCREEN_HEIGHT // 2

        rings.append(self)

    def draw(self, surface: pygame.Surface):
        if self.radius > self.width:
            pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), int(self.radius), self.width)

class Ball(GameObject):
    def __init__(self, radius=20, x=0, y=0, vx=0, vy=0, color: pygame.Color = pygame.Color('red'), hasTrail=False, trailFade=5):
        super().__init__()
        self.x = float(x)
        self.y = float(y)
        self.radius = radius
        self.vx = float(vx)
        self.vy = float(vy)
        self.color = color
        self.hasTrail = hasTrail
        self.trailFade = trailFade
        self.mass = math.pi * (radius ** 2)

        balls.append(self)

    def spawn_trail(self):
        if self.hasTrail:
            Trail(self.x, self.y, self.radius, self.color, fade_rate=self.trailFade)

    def move(self, dt):
        self.vy += settings.gravity * dt
        self.vx *= settings.friction
        self.vy *= settings.friction

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
                self.vx -= (1 + settings.restitution) * dot_product * nx
                self.vy -= (1 + settings.restitution) * dot_product * ny

    def draw(self, surface: pygame.Surface):
        pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), self.radius)

class Trail(GameObject):
    def __init__(self, x, y, radius, color, fade_rate=10):
        super().__init__()
        self.x = float(x)
        self.y = float(y)
        self.radius = radius
        self.color = color
        self.fade_rate = fade_rate
        self.alpha = 255

    def draw(self, surface: pygame.Surface):
        self.alpha = max(0, self.alpha - self.fade_rate)

        if self.alpha <= 0:
            if self in game_objects:
                game_objects.remove(self)
            return

        max_radius = max(1, int(self.radius * (0.98 + (self.alpha / 255) * 0.3)))
        diameter = max_radius * 2 + 2
        trail_surf = pygame.Surface((diameter, diameter), pygame.SRCALPHA)

        alpha = max(10, int(self.alpha * 0.9))

        for offset in range(2):
            r = max_radius - offset
            pygame.draw.circle(
                trail_surf,
                (self.color.r, self.color.g, self.color.b, alpha // (offset + 2)),
                (diameter // 2, diameter // 2),
                r,
            )

        surface.blit(trail_surf, (self.x - max_radius - 1, self.y - max_radius - 1))

def DrawAll(surface: pygame.Surface, *groups):
    if not groups:
        groups = (game_objects,)

    for group in groups:
        if group is None:
            continue

        if hasattr(group, "draw"):
            group.draw(surface)
            continue

        for obj in list(group):
            if hasattr(obj, "draw"):
                obj.draw(surface)
            elif isinstance(obj, (list, tuple, set)):
                for nested_obj in list(obj):
                    if hasattr(nested_obj, "draw"):
                        nested_obj.draw(surface)