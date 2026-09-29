import time
import pygame
import engine.objects as objects
import engine.physics as physics
import mods.builtin.effects as effects
import mods.builtin.magnetmod as magnetmod

# To add a mod type in "import mods.builtin.effects" for example to add the effects mod,
# add a mod to custom, if it is your own, and type import mods.custom.modname

pygame.init()

settings = objects.PhysicsSettings()
Ring = objects.Ring
Ball = objects.Ball
TrailBall = effects.TrailBall
MagnetBall = magnetmod.MagnetBall

# Edit these to add balls and stuff in between these comments.

TrailBall(radius=20, x=450, y=400, vx=6, vy=0, color=pygame.Color('red'), trailFade=50)
Sucker = MagnetBall(radius=20, x=500, y=400, vx=0, vy=0, color=pygame.Color('blue'))
Ring(radius=450, width=5, color=pygame.Color('white'))

# Start simulation!

physics.start_sim()