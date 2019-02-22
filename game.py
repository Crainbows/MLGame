import pyglet
import math
from pyglet.window import key
from pyglet.window import FPSDisplay

window = pyglet.window.Window(width=1200, height=900, caption="Speed Racer", resizable=False)
fps_display = FPSDisplay(window)
fps_display.label.font_size = 50

main_batch = pyglet.graphics.Batch()
player_image = pyglet.image.load('res/car.png')
player = pyglet.sprite.Sprite(player_image, x=50, y=50, batch=main_batch)
player.scale_y = 0.08
player.scale_x = 0.08

player.image.anchor_x = player.image.width / 2
player.image.anchor_y = player.image.height / 2

right = False
left = False
forward = False
backward = False
player_max_speed = 400
player_speed = 0
player_turning_speed = 5

class Point():
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Line():
    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2

# Example line acting as a placeholder
left_center_of_screen = Point(300, 600)
right_center_of_screen = Point(900, 600)
mid_screen_line = Line(left_center_of_screen, right_center_of_screen)

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

    # Example line acting as a placeholder
    pyglet.graphics.draw(2, pyglet.gl.GL_LINES,
    ('v2f', (mid_screen_line.p1.x, mid_screen_line.p1.y, mid_screen_line.p2.x, mid_screen_line.p2.y))
    )

def update(dt):
    player_move(player, dt)
    player_drive(player, dt)
    check_player_bounds(player)
    print(line_collision(player, mid_screen_line))

def player_move(entity, dt):
    if player_speed > 0:
        entity.x += math.sin(math.radians(entity.rotation % 360)) * player_speed * dt
        entity.y += math.cos(math.radians(entity.rotation % 360)) * player_speed * dt
        if left:
            entity.rotation -= player_turning_speed
        if right:
            entity.rotation += player_turning_speed

    elif player_speed < 0:
        entity.x += math.sin(math.radians(entity.rotation % 360)) * player_speed * dt
        entity.y += math.cos(math.radians(entity.rotation % 360)) * player_speed * dt
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

def line_collision(P1, line=None):
    P2 = Point(P1.x + (math.sin(math.radians(P1.rotation % 360)) *100), P1.y + (math.cos(math.radians(P1.rotation % 360)) *100 ))
    P3 = line.p1
    P4 = line.p2
    denominator = (((P1.x-P2.x)*(P3.y-P4.y)) - ((P1.y-P2.y)*(P3.x-P4.x)))
    if denominator:
        x = ((((P1.x*P2.y)-(P1.y*P2.x)) * (P3.x-P4.x)) - ((P1.x-P2.x) * ((P3.x*P4.y)-(P3.y*P4.x)))) / denominator
        y = ((((P1.x*P2.y)-(P1.y*P2.x)) * (P3.y-P4.y)) - ((P1.y-P2.y) * ((P3.x*P4.y)-(P3.y*P4.x)))) / denominator
        
        if (x < min(P1.x, P2.x)) or (x < min(P3.x, P4.x)) or (y < min(P1.y, P2.y)) or (y < min(P3.y, P4.y)) or (x > max(P1.x, P2.x)) or (x > max(P3.x, P4.x)) or (y > max(P1.y, P2.y)) or (y > max(P3.y, P4.y)):
            return False
        else:
            return x, y
    else:
        return False

if __name__ == "__main__":
    pyglet.clock.schedule_interval(update, 1.0/60)
    pyglet.app.run()