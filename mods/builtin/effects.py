import sys
from engine.objects import *
import pygame


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

        trail_radius = max(1, int(self.radius * (0.95 + (self.alpha / 255) * 0.25)))
        diameter = trail_radius * 2 + 2
        trail_surf = pygame.Surface((diameter, diameter), pygame.SRCALPHA)

        for offset in range(2):
            radius = max(1, trail_radius - offset)
            alpha = max(8, int(self.alpha * 0.9) // (offset + 2))
            pygame.draw.circle(
                trail_surf,
                (self.color.r, self.color.g, self.color.b, alpha),
                (diameter // 2, diameter // 2),
                radius,
            )

        surface.blit(trail_surf, (self.x - trail_radius - 1, self.y - trail_radius - 1))

class TrailBall(Ball):
    def __init__(self, radius=20, x=0, y=0, vx=0, vy=0, color: pygame.Color = pygame.Color('red'), trailFade=5):
        super().__init__(radius=radius, x=x, y=y, vx=vx, vy=vy, color=color)
        self.trailFade = trailFade

    def move(self, dt):
        self.vy += settings.gravity * dt
        self.vx *= settings.friction
        self.vy *= settings.friction
        self.x += self.vx * dt
        self.y += self.vy * dt
        Trail(self.x, self.y, self.radius, self.color, fade_rate=self.trailFade)


