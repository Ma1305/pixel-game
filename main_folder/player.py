from main_folder.game_setup import *
from main_folder.weapons import *

# player
player_info = {
    "size": (48, 84),
    "idle-right-files": [
        "images/knight/knight_m_right_idle_anim_f0.png",
        "images/knight/knight_m_right_idle_anim_f1.png",
        "images/knight/knight_m_right_idle_anim_f2.png",
        "images/knight/knight_m_right_idle_anim_f3.png"
    ],
    "idle-left-files": [
        "images/knight/knight_m_left_idle_anim_f0.png",
        "images/knight/knight_m_left_idle_anim_f1.png",
        "images/knight/knight_m_left_idle_anim_f2.png",
        "images/knight/knight_m_left_idle_anim_f3.png"
    ],
    "idle-wait-frame": int(manager.game_loop.fps/8),
    "run-left-files": [
        "images/knight/knight_m_run_left_anim_f0.png",
        "images/knight/knight_m_run_left_anim_f1.png",
        "images/knight/knight_m_run_left_anim_f2.png",
        "images/knight/knight_m_run_left_anim_f3.png"
    ],
    "run-right-files": [
        "images/knight/knight_m_run_right_anim_f0.png",
        "images/knight/knight_m_run_right_anim_f1.png",
        "images/knight/knight_m_run_right_anim_f2.png",
        "images/knight/knight_m_run_right_anim_f3.png"
    ],
    "run-wait-frame": int(manager.game_loop.fps/10),
    "box-collider": [0, 20, 48, 64]
}
player = game.Player(game_graphics, player_info)
player.y = player_info["size"][1]+10

characters.append(player)


def player_movement():
    keys = pygame.key.get_pressed()
    pygame.key.get_mods()

    # set animation
    if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        if pygame.key.get_mods() and pygame.KMOD_SHIFT:
            player.animation_state = "sprint-right"
        else:
            player.animation_state = "run-right"
    elif keys[pygame.K_LEFT] or keys[pygame.K_a]:
        if pygame.key.get_mods() and pygame.KMOD_SHIFT:
            player.animation_state = "sprint-left"
        else:
            player.animation_state = "run-left"
    else:
        player.animation_state = "idle"

    # move player
    run_speed = player.run_speed

    if keys[pygame.K_DOWN] or keys[pygame.K_s]:
        if player.jumping:
            player.finish_jump()
        player.velocity[1] -= run_speed*2

    game_graphics.camera.x = player.x
    # game_graphics.camera.y = player.y

    # attacking
    if keys[pygame.K_f]:
        player.weapon.attack()


player_movement_looper = user_input.Looper("player-movement", player_movement)
game_graphics.add_looper(player_movement_looper)
player.movement_looper = player_movement_looper

# player.setup_dash(game_graphics)


dashed = False


def player_jump(event):
    global dashed
    if event.key == pygame.K_SPACE or event.key == pygame.K_w:
        player.jump()
    elif event.mod == pygame.KMOD_LSHIFT or event.mod == pygame.KMOD_RSHIFT or event.mod == pygame.KMOD_SHIFT:
        player.jump_speed = int(game.Character.jump_speed * 1.5)

    '''# dash
    if event.key == pygame.K_RETURN:
        player.dash()'''


player_jump_input = user_input.InputFunc("player_jump", pygame.KEYDOWN, player_jump, pass_event=True)
game_graphics.add_input_func(player_jump_input)

sword = DefaultSword(player, size=[15, 38])


def compare_player():
    global player, characters
    for character in characters:
        if character == player:
            continue
        if player.weapon.attacking:
            if character.mask_collide(player.weapon.get_mask(), player.weapon.image_shape.x, player.weapon.image_shape.y):
                character.die()


player_compare_looper = user_input.Looper("compare-player", compare_player)
game_graphics.add_looper(player_compare_looper)