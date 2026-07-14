print("Starting 3D Gun Game...")
from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
import random
import math

app = Ursina()

window.title = "Python 3D Gun Game"
window.borderless = False
window.fullscreen = False
window.exit_button.visible = False
window.fps_counter.enabled = True

Sky()

ground = Entity(
    model="plane",
    scale=(60, 1, 60),
    texture="grass",
    collider="box"
)

player = FirstPersonController()
player.position = (0, 2, 0)
player.speed = 6
player.cursor.visible = True

gun = Entity(
    parent=camera,
    model="cube",
    color=color.dark_gray,
    scale=(0.25, 0.18, 0.8),
    position=(0.45, -0.35, 0.75)
)

gun_barrel = Entity(
    parent=gun,
    model="cube",
    color=color.black,
    scale=(0.4, 0.45, 1.4),
    position=(0, 0, 0.6)
)

crosshair = Text(text="+", origin=(0, 0), scale=2, color=color.white, position=(0, 0))

score = 0
health = 100
game_finished = False
enemies = []

score_text = Text(text="Score: 0", position=(-0.85, 0.45), scale=1.5)
health_text = Text(text="Health: 100", position=(-0.85, 0.39), scale=1.5, color=color.red)
enemy_text = Text(text="Enemies: 0", position=(-0.85, 0.33), scale=1.5, color=color.yellow)


def update_enemy_text():
    enemy_text.text = f"Enemies: {len(enemies)}"


def spawn_enemy():
    x = random.choice([-1, 1]) * random.randint(8, 18)
    z = random.choice([-1, 1]) * random.randint(8, 18)

    enemy = Entity(
        model="cube",
        color=color.red,
        scale=(2, 3, 2),
        position=(x, 1.5, z),
        collider="box"
    )

    enemy.health = 3

    eye = Entity(
        parent=enemy,
        model="sphere",
        color=color.white,
        scale=(0.25, 0.25, 0.25),
        position=(0.35, 0.3, -0.55)
    )

    eye2 = Entity(
        parent=enemy,
        model="sphere",
        color=color.white,
        scale=(0.25, 0.25, 0.25),
        position=(-0.35, 0.3, -0.55)
    )

    enemies.append(enemy)
    update_enemy_text()


for i in range(6):
    spawn_enemy()


def reset_gun():
    gun.position = (0.45, -0.35, 0.75)


def shoot():
    global score

    if game_finished:
        return

    gun.position = (0.45, -0.38, 0.65)
    invoke(reset_gun, delay=0.08)

    hit = raycast(
        camera.world_position,
        camera.forward,
        distance=100,
        ignore=[player, gun, gun_barrel]
    )

    if hit.hit and hit.entity in enemies:
        hit.entity.health -= 1
        hit.entity.color = color.orange
        invoke(setattr, hit.entity, "color", color.red, delay=0.1)

        if hit.entity.health <= 0:
            enemies.remove(hit.entity)
            destroy(hit.entity)
            score += 1
            score_text.text = f"Score: {score}"
            update_enemy_text()
            spawn_enemy()


def game_over():
    global game_finished

    if game_finished:
        return

    game_finished = True
    mouse.locked = False
    player.enabled = False

    Text(text="GAME OVER", origin=(0, 0), scale=4, color=color.red, background=True)
    Text(text="Press ESC to quit", origin=(0, 0), y=-0.1, scale=1.5, color=color.white)


def update():
    global health

    if game_finished:
        return

    for enemy in enemies:
        direction = player.position - enemy.position
        distance = direction.length()

        if distance > 2:
            enemy.position += direction.normalized() * time.dt * 2.5
            enemy.look_at(player.position)
        else:
            health -= 12 * time.dt
            health_text.text = f"Health: {int(health)}"

        if health <= 0:
            health = 0
            health_text.text = "Health: 0"
            game_over()


def input(key):
    if key == "left mouse down":
        shoot()

    if key == "escape":
        application.quit()


app.run()