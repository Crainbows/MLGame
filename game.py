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
player.scale_y = 0.03
player.scale_x = 0.03

player.image.anchor_x = player.image.width / 2
player.image.anchor_y = player.image.height / 2

right = False
left = False
forward = False
backward = False
player_max_speed = 400
player_speed = 0
player_turning_speed = 5


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
    player_drive(player, dt)
    check_player_bounds(player)

def player_move(entity, dt):
    if player_speed > 0:
        entity.y += math.cos(math.radians(entity.rotation % 360)) * player_speed * dt
        entity.x += math.sin(math.radians(entity.rotation % 360)) * player_speed * dt
        if left:
            entity.rotation -= player_turning_speed
        if right:
            entity.rotation += player_turning_speed

    elif player_speed < 0:
        entity.y += math.cos(math.radians(entity.rotation % 360)) * player_speed * dt
        entity.x += math.sin(math.radians(entity.rotation % 360)) * player_speed * dt
        if right:
            entity.rotation -= player_turning_speed
        if left:
            entity.rotation += player_turning_speed

def player_drive(entity, dt):
    global player_speed
    if forward and player_speed < player_max_speed:
        player_speed += 20
    elif backward and player_speed > -player_max_speed:
        player_speed -= 20
    elif player_speed != 0:
        player_speed -= int(math.copysign(5, player_speed))

def check_player_bounds(entity):
    min_x = -(entity.image.width * entity.scale_x) / 2
    min_y = -(entity.image.height * entity.scale_y) / 2
    max_x = 1200 + (entity.image.width * entity.scale_x) / 2
    max_y = 900 + (entity.image.height * entity.scale_y) / 2
    if entity.x < min_x:
        entity.x = max_x
    elif entity.x > max_x:
        entity.x = min_x
    if entity.y < min_y:
        entity.y = max_y
    elif entity.y > max_y:
        entity.y = min_y


if __name__ == "__main__":
    pyglet.clock.schedule_interval(update, 1.0/60)
    pyglet.app.run()