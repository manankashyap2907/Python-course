from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
import random
import math

app = Ursina()

window.title = "Python Block Craft"
window.borderless = False
window.fullscreen = False
window.exit_button.visible = False
window.fps_counter.enabled = True

Sky(color=color.rgb(120, 180, 255))

selected_block = "grass"
blocks = {}
world_size = 24

block_colors = {
    "grass": color.rgb(70, 170, 70),
    "dirt": color.rgb(120, 75, 35),
    "stone": color.rgb(120, 120, 120),
    "wood": color.rgb(125, 75, 35),
    "leaves": color.rgb(35, 140, 45),
    "sand": color.rgb(220, 205, 120),
    "water": color.rgba(40, 120, 255, 160),
    "brick": color.rgb(170, 60, 45),
    "gold": color.rgb(255, 210, 40)
}

hotbar_names = ["grass", "dirt", "stone", "wood", "leaves", "sand", "brick", "gold"]


class Block(Entity):
    def __init__(self, position=(0, 0, 0), block_type="grass"):
        super().__init__(
            model="cube",
            position=position,
            color=block_colors[block_type],
            texture="white_cube",
            collider="box"
        )

        self.block_type = block_type

        if block_type == "water":
            self.alpha = 0.65


def block_key(position):
    return (round(position[0]), round(position[1]), round(position[2]))


def add_block(position, block_type):
    key = block_key(position)

    if key in blocks:
        return

    block = Block(position=key, block_type=block_type)
    blocks[key] = block


def remove_block(block):
    key = block_key(block.position)

    if key in blocks:
        del blocks[key]

    destroy(block)


def terrain_height(x, z):
    height = (
        math.sin(x * 0.25) * 2
        + math.cos(z * 0.22) * 2
        + math.sin((x + z) * 0.12) * 2
    )

    return int(height + 4)


def make_tree(x, y, z):
    for i in range(4):
        add_block((x, y + i, z), "wood")

    leaves_positions = [
        (0, 4, 0),
        (1, 4, 0),
        (-1, 4, 0),
        (0, 4, 1),
        (0, 4, -1),
        (1, 5, 0),
        (-1, 5, 0),
        (0, 5, 1),
        (0, 5, -1),
        (0, 5, 0),
        (0, 6, 0)
    ]

    for lx, ly, lz in leaves_positions:
        add_block((x + lx, y + ly, z + lz), "leaves")


def generate_world():
    for x in range(-world_size, world_size):
        for z in range(-world_size, world_size):
            y = terrain_height(x, z)

            if y <= 3:
                add_block((x, 3, z), "sand")
                add_block((x, 2, z), "dirt")
                add_block((x, 1, z), "stone")
                add_block((x, 4, z), "water")
            else:
                add_block((x, y, z), "grass")
                add_block((x, y - 1, z), "dirt")
                add_block((x, y - 2, z), "dirt")
                add_block((x, y - 3, z), "stone")

                if random.randint(1, 70) == 1:
                    make_tree(x, y + 1, z)


generate_world()

player = FirstPersonController()
player.position = (0, 12, 0)
player.speed = 6
player.jump_height = 2
player.cursor.visible = True
mouse.locked = True

crosshair = Text(
    text="+",
    origin=(0, 0),
    scale=2,
    color=color.white
)

block_text = Text(
    text="Block: grass",
    position=(-0.86, 0.45),
    scale=1.4,
    color=color.white
)

help_text = Text(
    text="Left click break | Right click place | 1-8 blocks | R reset | ESC quit",
    origin=(0, 0),
    position=(0, -0.46),
    scale=1,
    color=color.white
)

hotbar = []

for i, name in enumerate(hotbar_names):
    slot = Entity(
        parent=camera.ui,
        model="quad",
        color=color.dark_gray,
        scale=(0.08, 0.08),
        position=(-0.32 + i * 0.09, -0.39)
    )

    icon = Entity(
        parent=camera.ui,
        model="quad",
        color=block_colors[name],
        scale=(0.055, 0.055),
        position=(-0.32 + i * 0.09, -0.39)
    )

    number = Text(
        text=str(i + 1),
        parent=camera.ui,
        position=(-0.345 + i * 0.09, -0.43),
        scale=0.75,
        color=color.white
    )

    hotbar.append((slot, icon))


def update_hotbar():
    for i, name in enumerate(hotbar_names):
        slot, icon = hotbar[i]

        if name == selected_block:
            slot.color = color.yellow
            slot.scale = (0.09, 0.09)
        else:
            slot.color = color.dark_gray
            slot.scale = (0.08, 0.08)

    block_text.text = f"Block: {selected_block}"


update_hotbar()


def input(key):
    global selected_block

    if key in ["1", "2", "3", "4", "5", "6", "7", "8"]:
        selected_block = hotbar_names[int(key) - 1]
        update_hotbar()

    if key == "left mouse down":
        hit = raycast(camera.world_position, camera.forward, distance=7, ignore=[player])

        if hit.hit and hit.entity in blocks.values():
            remove_block(hit.entity)

    if key == "right mouse down":
        hit = raycast(camera.world_position, camera.forward, distance=7, ignore=[player])

        if hit.hit:
            new_position = hit.entity.position + hit.normal
            add_block(new_position, selected_block)

    if key == "r":
        player.position = (0, 12, 0)

    if key == "escape":
        application.quit()


def update():
    if player.y < -20:
        player.position = (0, 12, 0)


app.run()