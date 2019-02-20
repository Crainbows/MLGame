import pyglet
import math
from pyglet.window import key
from pyglet.window import FPSDisplay

window = pyglet.window.Window(width=1200, height=900, caption="Speed Racer", resizable=False)
# window.set_location(400, 100)
fps_display = FPSDisplay(window)
fps_display.label.font_size = 50

main_batch = pyglet.graphics.Batch()
player_image = pyglet.image.load('res/Car_1_01.png')
player = pyglet.sprite.Sprite(player_image, x=50, y=50, batch=main_batch)
player.scale_y = 0.1
player.scale_x = 0.1

player.image.anchor_x = player.image.width / 2
player.image.anchor_y = player.image.height / 2

right = False
left = False
forward = False
backward = False
player_speed = 300


@window.event
def on_key_press(symbol, modifiers):
    global  forward, backward, right, left
    if symbol == key.UP:
        forward = True
    if symbol == key.DOWN:
        backward = True
    if symbol == key.RIGHT:
        right = True
    if symbol == key.LEFT:
        left = True


@window.event
def on_key_release(symbol, modifiers):
    global forward, backward, right, left
    if symbol == key.UP:
        forward = False
    if symbol == key.DOWN:
        backward = False
    if symbol == key.RIGHT:
        right = False
    if symbol == key.LEFT:
        left = False

@window.event
def on_draw():
    window.clear()
    main_batch.draw()
    fps_display.draw()

def update(dt):
    player_move(player, dt)

def player_move(entity, dt):
    if forward and entity.y < 785:
        entity.y += math.cos(math.radians(entity.rotation % 360)) * player_speed * dt
        entity.x += math.sin(math.radians(entity.rotation % 360)) * player_speed * dt
    if backward and entity.y > 0:
        entity.y += math.sin(math.radians(entity.rotation % 360)) * player_speed * dt
        entity.x += math.cos(math.radians(entity.rotation % 360)) * player_speed * dt
    if (left and forward) or (right and backward):
        entity.rotation -= 1
    if (right and forward) or (left and backward):
        entity.rotation += 1



if __name__ == "__main__":
    pyglet.clock.schedule_interval(update, 1.0/60)
    pyglet.app.run()