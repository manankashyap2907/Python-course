from ursina import *
import random
import math

app = Ursina()

window.title = "Roblox Style Mega Racing"
window.borderless = False
window.fullscreen = False
window.exit_button.visible = False
window.fps_counter.enabled = True

Sky(color=color.rgb(120, 190, 255))
camera.fov = 82

ROAD_WIDTH = 22
TOTAL_LAPS = 3

game_started = False
game_finished = False
countdown = 3
race_time = 0

player_speed = 0
player_lap = 1
player_checkpoint = 0
boost_cooldown = 0
boost_timer = 0

walls = []
checkpoints = []
boost_pads = []
bots = []

track_points = [
    Vec3(0, 0.1, -105),
    Vec3(0, 0.1, -60),
    Vec3(40, 0.1, -35),
    Vec3(90, 0.1, -10),
    Vec3(105, 0.1, 45),
    Vec3(65, 0.1, 90),
    Vec3(5, 0.1, 110),
    Vec3(-55, 0.1, 88),
    Vec3(-100, 0.1, 35),
    Vec3(-85, 0.1, -25),
    Vec3(-38, 0.1, -70),
    Vec3(0, 0.1, -105),
]

speed_text = Text(text="Speed: 0 km/h", position=(-0.86, 0.45), scale=1.3)
lap_text = Text(text="Lap: 1 / 3", position=(-0.86, 0.39), scale=1.3)
place_text = Text(text="Place: 1st", position=(-0.86, 0.33), scale=1.3, color=color.azure)
time_text = Text(text="Time: 0.0", position=(-0.86, 0.27), scale=1.2)
boost_text = Text(text="Boost: Ready", position=(-0.86, 0.21), scale=1.2, color=color.lime)
checkpoint_text = Text(text="Checkpoint: 1", position=(-0.86, 0.15), scale=1.1, color=color.yellow)

Text(
    text="W drive | S brake | A/D steer | SPACE boost | R reset | ESC quit",
    origin=(0, 0),
    position=(0, -0.46),
    scale=1,
    color=color.white
)

big_message = Text(text="3", origin=(0, 0), scale=4, color=color.yellow, background=True)

ground = Entity(
    model="plane",
    scale=(330, 1, 330),
    texture="grass",
    color=color.rgb(50, 155, 65),
    collider="box"
)


def flat_distance(a, b):
    return math.sqrt((a.x - b.x) ** 2 + (a.z - b.z) ** 2)


def angle_between(a, b):
    d = b - a
    return math.degrees(math.atan2(d.x, d.z))


def make_road(start, end):
    middle = (start + end) / 2
    direction = end - start
    length = direction.length()
    angle = angle_between(start, end)

    Entity(
        model="cube",
        position=middle,
        scale=(ROAD_WIDTH, 0.18, length),
        rotation_y=angle,
        color=color.rgb(35, 35, 38),
        collider="box"
    )

    side_x = math.cos(math.radians(angle))
    side_z = -math.sin(math.radians(angle))

    left_wall = Entity(
        model="cube",
        position=middle + Vec3(side_x * 13, 1.1, side_z * 13),
        scale=(0.8, 2.2, length),
        rotation_y=angle,
        color=color.rgb(230, 40, 40),
        collider="box"
    )

    right_wall = Entity(
        model="cube",
        position=middle - Vec3(side_x * 13, -1.1, side_z * 13),
        scale=(0.8, 2.2, length),
        rotation_y=angle,
        color=color.rgb(245, 245, 245),
        collider="box"
    )

    walls.append(left_wall)
    walls.append(right_wall)

    dash_count = max(1, int(length / 9))

    for i in range(dash_count):
        t = (i + 0.5) / dash_count
        pos = start + direction * t

        Entity(
            model="cube",
            position=pos + Vec3(0, 0.24, 0),
            scale=(0.5, 0.05, 3.5),
            rotation_y=angle,
            color=color.yellow
        )

    for side in [-1, 1]:
        Entity(
            model="cube",
            position=middle + Vec3(side_x * side * 9.8, 0.25, side_z * side * 9.8),
            scale=(0.35, 0.05, length),
            rotation_y=angle,
            color=color.white
        )


for i in range(len(track_points) - 1):
    make_road(track_points[i], track_points[i + 1])

Entity(model="cube", position=(0, 0.35, -94), scale=(ROAD_WIDTH, 0.12, 3), color=color.white, collider="box")
Entity(model="cube", position=(-14, 4, -94), scale=(1.2, 8, 1.2), color=color.white)
Entity(model="cube", position=(14, 4, -94), scale=(1.2, 8, 1.2), color=color.white)
finish_top = Entity(model="cube", position=(0, 8.3, -94), scale=(29, 1.3, 1.3), color=color.red)
Text(text="FINISH", parent=finish_top, origin=(0, 0), position=(0, 0.45, -0.65), scale=3, color=color.black)

for i in range(1, len(track_points)):
    point = track_points[i]
    previous = track_points[i - 1]

    cp = Entity(
        model="cube",
        position=point + Vec3(0, 3.2, 0),
        scale=(ROAD_WIDTH - 2, 6.4, 1.2),
        rotation_y=angle_between(previous, point),
        color=color.rgba(0, 230, 255, 70),
        collider="box",
        visible=False
    )

    checkpoints.append(cp)

checkpoints[0].visible = True

for i in range(1, len(track_points) - 1):
    point = track_points[i]
    next_point = track_points[i + 1]
    angle = angle_between(point, next_point)

    arrow = Entity(
        model="cube",
        position=point + Vec3(0, 0.35, 0),
        scale=(8, 0.08, 4),
        rotation_y=angle,
        color=color.rgb(45, 45, 45)
    )

    Text(text=">>>", parent=arrow, origin=(0, 0), scale=3, color=color.orange, rotation_x=90, position=(0, 0.12, 0))

for pos in [
    Vec3(42, 0.36, -34),
    Vec3(88, 0.36, 35),
    Vec3(40, 0.36, 98),
    Vec3(-80, 0.36, 48),
    Vec3(-45, 0.36, -65),
]:
    pad = Entity(model="cube", position=pos, scale=(8, 0.15, 5), color=color.rgb(0, 230, 255), collider="box")
    boost_pads.append(pad)
    Text(text="BOOST", parent=pad, origin=(0, 0), scale=1.8, color=color.black, rotation_x=90, position=(0, 0.13, 0))


def close_to_track(x, z):
    test = Vec3(x, 0, z)

    for point in track_points:
        if flat_distance(test, point) < 26:
            return True

    return False


for i in range(120):
    x = random.randint(-150, 150)
    z = random.randint(-150, 150)

    if close_to_track(x, z):
        continue

    Entity(model="cube", position=(x, 1.6, z), scale=(0.8, 3.2, 0.8), color=color.rgb(95, 55, 25))
    Entity(model="sphere", position=(x, 4.2, z), scale=(3.6, 3.6, 3.6), color=color.rgb(35, 125, 45))

for i in range(40):
    x = random.randint(-145, 145)
    z = random.randint(-145, 145)

    if close_to_track(x, z):
        continue

    Entity(
        model="sphere",
        position=(x, 0.7, z),
        scale=(random.uniform(1.3, 3), random.uniform(0.7, 1.4), random.uniform(1.3, 3)),
        color=color.rgb(95, 95, 95)
    )

for data in [
    (135, -25, 18, 18, 18),
    (140, 45, 14, 22, 14),
    (-138, -20, 16, 20, 16),
    (-135, 60, 22, 14, 18),
    (40, 140, 18, 18, 18),
    (-45, 140, 14, 24, 14),
]:
    x, z, sx, sy, sz = data

    Entity(
        model="cube",
        position=(x, sy / 2, z),
        scale=(sx, sy, sz),
        color=color.rgb(random.randint(85, 150), random.randint(85, 150), random.randint(110, 175))
    )


def create_wheel(parent, x, z):
    wheel = Entity(
        parent=parent,
        model="sphere",
        position=(x, -0.45, z),
        scale=(0.58, 0.58, 0.32),
        color=color.black
    )

    wheel.rotation_z = 90

    Entity(
        parent=wheel,
        model="sphere",
        position=(0, 0, -0.08),
        scale=(0.45, 0.45, 0.18),
        color=color.rgb(185, 185, 185)
    )

    return wheel


def create_car(position, car_color, car_name, is_player=False):
    car = Entity(
        model="cube",
        position=position,
        scale=(2.7, 0.62, 4.8),
        color=car_color,
        collider="box"
    )

    car.car_name = car_name
    car.speed = 0
    car.max_speed = 50
    car.lap = 1
    car.checkpoint = 0
    car.finished = False
    car.wheels = []

    Entity(parent=car, model="cube", position=(0, 0.12, 1.2), scale=(0.92, 0.34, 0.55), color=car_color)
    Entity(parent=car, model="cube", position=(0, 0.1, -1.35), scale=(0.92, 0.28, 0.48), color=car_color)
    Entity(parent=car, model="cube", position=(0, 0.65, -0.25), scale=(0.78, 0.58, 0.72), color=color.rgb(30, 160, 220))

    Entity(parent=car, model="cube", position=(0, 0.9, 0.35), scale=(0.66, 0.07, 0.16), color=color.white)
    Entity(parent=car, model="cube", position=(0, 0.86, -0.9), scale=(0.66, 0.07, 0.16), color=color.white)

    Entity(parent=car, model="cube", position=(-0.56, 0.08, 2.45), scale=(0.34, 0.18, 0.08), color=color.yellow)
    Entity(parent=car, model="cube", position=(0.56, 0.08, 2.45), scale=(0.34, 0.18, 0.08), color=color.yellow)
    Entity(parent=car, model="cube", position=(-0.58, 0.08, -2.45), scale=(0.34, 0.18, 0.08), color=color.red)
    Entity(parent=car, model="cube", position=(0.58, 0.08, -2.45), scale=(0.34, 0.18, 0.08), color=color.red)

    Entity(parent=car, model="cube", position=(0, 0.55, -2.15), scale=(1.35, 0.12, 0.12), color=color.black)
    Entity(parent=car, model="cube", position=(-0.85, 0.34, -2.15), scale=(0.08, 0.42, 0.08), color=color.black)
    Entity(parent=car, model="cube", position=(0.85, 0.34, -2.15), scale=(0.08, 0.42, 0.08), color=color.black)

    for x in [-1.08, 1.08]:
        for z in [-1.55, 1.55]:
            wheel = create_wheel(car, x, z)
            car.wheels.append(wheel)

    if is_player:
        Entity(parent=car, model="cube", position=(0, -0.55, 0), scale=(1.3, 0.05, 1.2), color=color.rgba(0, 180, 255, 95))
    else:
        Text(text=car_name, parent=car, y=1.75, origin=(0, 0), scale=1.5, color=color.white, billboard=True)

    return car


player = create_car(Vec3(-4, 1, -99), color.rgb(20, 90, 255), "YOU", True)

for start_pos, bot_color, bot_name, bot_speed in [
    (Vec3(4, 1, -99), color.rgb(235, 55, 55), "BOLT", 50),
    (Vec3(-8, 1, -108), color.rgb(255, 175, 35), "FLASH", 48),
    (Vec3(8, 1, -108), color.rgb(145, 70, 230), "NOVA", 52),
    (Vec3(-12, 1, -117), color.rgb(40, 210, 90), "TURBO", 47),
    (Vec3(12, 1, -117), color.rgb(240, 70, 170), "VIPER", 49),
]:
    bot = create_car(start_pos, bot_color, bot_name)
    bot.max_speed = bot_speed
    bot.speed = random.randint(24, 30)
    bots.append(bot)


def reset_race():
    global player_speed, player_lap, player_checkpoint, boost_cooldown, boost_timer

    player.position = Vec3(-4, 1, -99)
    player.rotation = Vec3(0, 0, 0)

    player_speed = 0
    player_lap = 1
    player_checkpoint = 0
    boost_cooldown = 0
    boost_timer = 0

    for cp in checkpoints:
        cp.visible = False

    checkpoints[0].visible = True


def camera_follow():
    target_position = player.position + player.back * 15 + Vec3(0, 8.5, 0)
    camera.position = lerp(camera.position, target_position, time.dt * 5)
    camera.look_at(player.position + Vec3(0, 1.6, 0))


def bounce_from_walls(car, speed_value):
    for wall in walls:
        if car.intersects(wall).hit:
            car.position -= car.forward * 2.2
            return -speed_value * 0.45

    return speed_value


def check_boost(car, speed_value):
    for pad in boost_pads:
        if car.intersects(pad).hit:
            return min(speed_value + 15, 80)

    return speed_value


def advance_player_checkpoint():
    global player_checkpoint, player_lap, game_finished

    target = track_points[player_checkpoint + 1]

    if flat_distance(player.position, target) < 13:
        checkpoints[player_checkpoint].visible = False
        player_checkpoint += 1

        if player_checkpoint >= len(checkpoints):
            player_checkpoint = 0
            player_lap += 1

            if player_lap > TOTAL_LAPS:
                game_finished = True
                big_message.text = "YOU FINISHED!"
                return

        checkpoints[player_checkpoint].visible = True


def advance_bot_checkpoint(bot):
    target = track_points[bot.checkpoint + 1]

    if flat_distance(bot.position, target) < 13:
        bot.checkpoint += 1

        if bot.checkpoint >= len(checkpoints):
            bot.checkpoint = 0
            bot.lap += 1

            if bot.lap > TOTAL_LAPS:
                bot.finished = True
                bot.speed = 0


def update_place():
    racers = [("YOU", player_lap, player_checkpoint)]

    for bot in bots:
        racers.append((bot.car_name, bot.lap, bot.checkpoint))

    racers.sort(key=lambda r: (r[1], r[2]), reverse=True)

    place = 1

    for i in range(len(racers)):
        if racers[i][0] == "YOU":
            place = i + 1

    if place == 1:
        place_text.text = "Place: 1st"
    elif place == 2:
        place_text.text = "Place: 2nd"
    elif place == 3:
        place_text.text = "Place: 3rd"
    else:
        place_text.text = f"Place: {place}th"


def move_player():
    global player_speed, boost_timer

    max_speed_now = 62

    if boost_timer > 0:
        boost_timer -= time.dt
        max_speed_now = 84

    if held_keys["w"]:
        player_speed += 36 * time.dt
    elif held_keys["s"]:
        player_speed -= 46 * time.dt
    else:
        if player_speed > 0:
            player_speed -= 10 * time.dt
        elif player_speed < 0:
            player_speed += 10 * time.dt

    player_speed = clamp(player_speed, -22, max_speed_now)

    if abs(player_speed) < 0.2:
        player_speed = 0

    steer = 0

    if held_keys["a"]:
        steer = -1

    if held_keys["d"]:
        steer = 1

    if player_speed != 0:
        player.rotation_y += steer * 105 * time.dt * (player_speed / 62)

    player.position += player.forward * player_speed * time.dt

    for wheel in player.wheels:
        wheel.rotation_x += player_speed * time.dt * 120

    player_speed = bounce_from_walls(player, player_speed)
    player_speed = check_boost(player, player_speed)

    advance_player_checkpoint()


def move_bots():
    global player_speed

    for bot in bots:
        if bot.finished:
            continue

        target = track_points[bot.checkpoint + 1]
        direction = target - bot.position
        direction.y = 0

        if direction.length() > 0:
            target_angle = angle_between(bot.position, target)
            bot.rotation_y = lerp(bot.rotation_y, target_angle, time.dt * 4)

        bot.speed += 13 * time.dt
        bot.speed = clamp(bot.speed, 18, bot.max_speed)
        bot.position += bot.forward * bot.speed * time.dt

        for wheel in bot.wheels:
            wheel.rotation_x += bot.speed * time.dt * 120

        bot.speed = bounce_from_walls(bot, bot.speed)
        bot.speed = check_boost(bot, bot.speed)

        advance_bot_checkpoint(bot)

        if bot.intersects(player).hit:
            player_speed = -18
            player.position -= player.forward * 2.5
            bot.speed *= 0.5


def update_countdown():
    global countdown, game_started

    countdown -= time.dt

    if countdown > 2:
        big_message.text = "3"
    elif countdown > 1:
        big_message.text = "2"
    elif countdown > 0:
        big_message.text = "1"
    else:
        big_message.text = "GO!"
        game_started = True
        invoke(setattr, big_message, "text", "", delay=0.8)


def update_ui():
    speed_text.text = f"Speed: {int(abs(player_speed) * 3.6)} km/h"
    lap_text.text = f"Lap: {min(player_lap, TOTAL_LAPS)} / {TOTAL_LAPS}"
    time_text.text = f"Time: {race_time:.1f}"
    checkpoint_text.text = f"Checkpoint: {player_checkpoint + 1} / {len(checkpoints)}"

    if boost_cooldown > 0:
        boost_text.text = f"Boost: {boost_cooldown:.1f}s"
        boost_text.color = color.orange
    else:
        boost_text.text = "Boost: Ready"
        boost_text.color = color.lime


def update():
    global race_time, boost_cooldown

    camera_follow()

    if boost_cooldown > 0:
        boost_cooldown -= time.dt

    if not game_started:
        update_countdown()
        update_ui()
        return

    if not game_finished:
        race_time += time.dt
        move_player()
        move_bots()
        update_place()

    update_ui()


def input(key):
    global boost_timer, boost_cooldown, player_speed

    if key == "space" and game_started and not game_finished:
        if boost_cooldown <= 0:
            boost_timer = 1.2
            boost_cooldown = 5
            player_speed = min(player_speed + 25, 84)

    if key == "r":
        reset_race()

    if key == "escape":
        application.quit()


reset_race()
app.run()