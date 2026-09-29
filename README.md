# The ball sim
## How to use
This is a Pygame ball simulation and game engine, it is very featureful and it has a modding interface, its very fun to play with and it is somewhat realistic.
If you have any updates or anything you want to add (like optimise the engine, add a new built in mod) then you can just make a pull request!
## How to create a mod
To create a mod, create a new Python file in mods/custom/.

### 1. Create your mod

For example, create:
```
mods/custom/mymod.py
```
### 2. Import the engine

At the top of your mod, add:

import engine.objects as objects
from engine.hooks import register_update_hook

You can now access the balls in the simulation with:
```python
objects.balls
```
### 3. Add your code

For example, this mod makes every ball accelerate to the right:
```python
def move_balls():
    for ball in objects.balls:
        ball.vx += 0.01
```
### 4. Register your update function

At the bottom of your mod, add:
```python
register_update_hook(move_balls)
```
Your complete mod should now look like this:

```python
import engine.objects as objects
from engine.hooks import register_update_hook

def move_balls():
    for ball in objects.balls:
        ball.vx += 0.01
register_update_hook(move_balls)
```

### 5. Enable your mod
Open main.py and import your mod:
```python
import mods.custom.mymod
```
Then run the simulation!

## Making more advanced mods

You can also create your own types of balls by inheriting from objects.Ball:
```python
class MyBall(objects.Ball):
    def talk(self):
        print(":) hello")
    def jump(self):
        self.vx += 10
```
Then you can add your own behavior to your ball.
---
Try experimenting! Change the velocity, position, color, or anything else you can think of. You can even create completely new physics effects.

If you make something cool, consider opening a pull request so it can be added to the project!
