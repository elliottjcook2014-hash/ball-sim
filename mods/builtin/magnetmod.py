import math
import engine.objects as objects
from engine.hooks import register_update_hook

# Sample magnet mod

class MagnetBall(objects.Ball):
    def suck(self):
        for ball in objects.balls: # Get all balls
            if ball is self: # Don't attract yourself
                continue

            dx = ball.x - self.x # Difference in X position
            dy = ball.y - self.y # Difference in Y position
            distance = math.hypot(dx, dy) # Total distance to the ball

            if distance > 0:
                nx = dx / distance # Normalized X direction
                ny = dy / distance # Normalized Y direction

                force = .1 # Strength of the attraction
                self.vx += nx * force # Add attraction to X velocity
                self.vy += ny * force # Add attraction to Y velocity


def update():
    for ball in objects.balls:
        if isinstance(ball, MagnetBall):
            ball.suck()


register_update_hook(update)
