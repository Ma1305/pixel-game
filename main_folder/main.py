
import graphics
from shape_types import *
import user_input
import manager

manager.game_loop.make_screen(1600, 900)
manager.game_loop.fps = 60

import main_folder.game as game

# import main_folder.game_setup as game_setup
import main_folder.game_design as level1
import main_folder.player as player
# import main_folder.enemies


# manager.game_loop.fps = 40

level1.level1.start_level()

first_player = game.Player(level1.level1.game_graphics, player.player_info)
level1.level1.characters.append(first_player)
sword = player.DefaultSword(first_player, size=[15, 38])
first_player.y = player.player_info["size"][1]+100
player.start_single_player(first_player, level1.level1.game_graphics)

# level1.level2.start_level()

second_player = game.Player(level1.level2.game_graphics, player.player_info)
level1.level2.characters.append(second_player)
second_sword = player.DefaultSword(second_player, size=[15, 38])
second_player.y = player.player_info["size"][1]+100
player.start_single_player(second_player, level1.level2.game_graphics)


def change_game_graphics(event):
    if event.key == pygame.K_RETURN:
        manager.game_loop.set_main_game_graphics(level1.level2)
        level1.level1.leave_level()
        level1.level2.start_level()


change_trigger = user_input.InputFunc("change_trig", pygame.KEYDOWN, change_game_graphics, pass_event=True)
level1.level1.game_graphics.add_input_func(change_trigger)


def change_game_graphics(event):
    if event.key == pygame.K_RETURN:
        manager.game_loop.set_main_game_graphics(level1.level1)
        level1.level2.leave_level()
        level1.level1.start_level()


change_trigger = user_input.InputFunc("change_trig", pygame.KEYDOWN, change_game_graphics, pass_event=True)
level1.level2.game_graphics.add_input_func(change_trigger)