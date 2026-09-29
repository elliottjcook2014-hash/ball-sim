import pygame
import math
import engine.objects as objects
from engine.hooks import register_update_hook

# Sample magnet mod

balls = objects.balls


class MagnetBall(objects.Ball):
    def suck(self):
        for ball in balls:
            if ball is self:
                continue
            dx = ball.x - self.x
            dy = ball.y - self.y
            distance = math.hypot(dx, dy)
            if distance > 0:
                nx = dx / distance
                ny = dy / distance
                force = .1
                self.vx += nx * force
                self.vy += ny * force


def update():
    for ball in balls:
        if isinstance(ball, MagnetBall):
            ball.suck()


register_update_hook(update)
