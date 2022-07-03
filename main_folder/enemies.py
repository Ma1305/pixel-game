from main_folder.game_setup import *
import random


demon_info = {
    "size": (48, 54),
    "idle-right-files": [
        "images/demon/big_demon_right_idle_anim_f0.png",
        "images/demon/big_demon_right_idle_anim_f1.png",
        "images/demon/big_demon_right_idle_anim_f2.png",
        "images/demon/big_demon_right_idle_anim_f3.png"
    ],
    "idle-left-files": [
        "images/demon/big_demon_left_idle_anim_f0.png",
        "images/demon/big_demon_left_idle_anim_f1.png",
        "images/demon/big_demon_left_idle_anim_f2.png",
        "images/demon/big_demon_left_idle_anim_f3.png"
    ],
    "idle-wait-frame": int(manager.game_loop.fps/8),
    "run-left-files": [
        "images/demon/big_demon_run_left_anim_f0.png",
        "images/demon/big_demon_run_left_anim_f1.png",
        "images/demon/big_demon_run_left_anim_f2.png",
        "images/demon/big_demon_run_left_anim_f3.png"
    ],
    "run-right-files": [
        "images/demon/big_demon_run_right_anim_f0.png",
        "images/demon/big_demon_run_right_anim_f1.png",
        "images/demon/big_demon_run_right_anim_f2.png",
        "images/demon/big_demon_run_right_anim_f3.png"
    ],
    "run-wait-frame": int(manager.game_loop.fps/10),
    "box-collider": [4, 4, 40, 46]
}

'''# demon1
demon1 = game.Demon(-100, 400, game_graphics)
characters.append(demon1)'''


# generating enemies
counter = 0


def generate_enemy():
    global counter
    counter += 1
    if counter % (manager.game_loop.fps*5) == 0:
        x = random.randint(-300, 200)
        demon = game.Demon(x, 200, game_graphics)
        characters.append(demon)
        demon.random_movement_frame = int(demon.random_movement_wait_frame*3/4)


# game_graphics.add_looper(user_input.Looper("generate-demon", generate_enemy))


# 1 trap
# trap = game.Trap(0, -190, game_graphics)
# traps.append(trap)