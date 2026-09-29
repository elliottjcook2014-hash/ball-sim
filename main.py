import pygame
import engine.objects as objects
import engine.physics as physics
import mods.builtin.effects as effects

# To add a mod type in "import mods.builtin.effects" for example to add the effects mod,
# add a mod to custom, if it is your own, and type import mods.custom.modname

pygame.init()

settings = objects.PhysicsSettings()
Ring = objects.Ring
Ball = objects.Ball
TrailBall = effects.TrailBall

# Edit these to add balls and stuff in between these comments.

TrailBall(radius=20, x=450, y=400, vx=6, vy=0, color=pygame.Color('red'), trailFade=50)
Ball(radius=35, x=550, y=400, vx=-4, vy=2, color=pygame.Color('blue'))
Ball(radius=15, x=500, y=300, vx=2, vy=-5, color=pygame.Color('green'))
TrailBall(radius=50, x=500, y=400, vx=0, vy=0, color=pygame.Color('purple'), trailFade=20)

Ring(radius=450, width=5, color=pygame.Color('white'))

# Start simulation!

physics.start_sim()
