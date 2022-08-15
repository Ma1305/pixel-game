from main_folder.game_setup import *
import main_folder.development_tools as dev


# grounds
# tile information
game.BrickGround.brick_size = [50, 50]
tile_size = game.BrickGround.brick_size
print(game.BrickGround.brick_size)

# left ground
left_ground = game.BrickGround(-tile_size[0]*16, tile_size[1]*10, 16, 10, game_graphics, top_wall=False, left_wall=False, bottom_wall=False)
# left_ground.set_all_image_sizes()
grounds.append(left_ground)

left_ground_filler = game.BrickGround(left_ground.x, left_ground.y-left_ground.height, left_ground.brick_width, 9, game_graphics, top_wall=False, left_wall=False, bottom_wall=False, right_wall=False)
grounds.append(left_ground_filler)

base_x_follow = 0
base_y_follow = 0

# base ground 1
base_ground1 = game.BrickGround(0, 0, 3, 2, game_graphics, left_wall=False, bottom_wall=False)
grounds.append(base_ground1)
base_x_follow += base_ground1.brick_width
base_y_follow -= base_ground1.brick_height

base_ground1_filler = game.BrickGround(0, -2*tile_size[1], 3, 7, game_graphics, top_wall=False, left_wall=False, bottom_wall=False, right_wall=False)
grounds.append(base_ground1_filler)

# base ground 2
base_ground2 = game.BrickGround(base_x_follow*tile_size[0], base_y_follow*tile_size[1], 15, 2, game_graphics, left_wall=False, bottom_wall=False)
grounds.append(base_ground2)
base_x_follow += base_ground2.brick_width
base_y_follow -= base_ground2.brick_height

base_ground2_filler = game.BrickGround(base_ground2.x, base_ground2.y-base_ground2.height, 15, 5, game_graphics, top_wall=False, left_wall=False, bottom_wall=False, right_wall=False)
grounds.append(base_ground2_filler)

# base ground 3
base_ground3 = game.BrickGround(base_x_follow*tile_size[0], base_y_follow*tile_size[1], 7, 1, game_graphics, left_wall=False, bottom_wall=False, right_wall=False)
grounds.append(base_ground3)
base_x_follow += base_ground3.brick_width

base_ground3_filler = game.BrickGround(base_ground3.x, base_ground3.y-base_ground3.height, 7, 8, game_graphics, top_wall=False, left_wall=False, bottom_wall=False, right_wall=False)
grounds.append(base_ground3_filler)

# base ground 4
base_ground4 = game.BrickGround(base_x_follow*tile_size[0], 2*tile_size[1], 10, -base_y_follow+2, game_graphics, bottom_wall=False)
grounds.append(base_ground4)
base_x_follow += base_ground4.brick_width
base_y_follow = -base_ground4.brick_height+2

# roof ground 1
roof_ground1 = game.BrickGround((base_x_follow+2)*tile_size[0], base_ground4.y, 19, 3, game_graphics, right_wall=False, bottom_wall=False)
grounds.append(roof_ground1)

roof_ground2 = game.BrickGround((base_x_follow+2)*tile_size[0], base_ground4.y-3*tile_size[1], 19, 7, game_graphics, top_wall=False)
grounds.append(roof_ground2)

roof_ground3 = game.BrickGround((base_x_follow+2)*tile_size[0]+roof_ground1.brick_width*tile_size[0], base_ground4.y, 24, 3, game_graphics, left_wall=False, right_wall=False)
grounds.append(roof_ground3)

# base ground 5
base_ground5 = game.BrickGround(base_ground4.x, base_y_follow*tile_size[1], base_ground4.brick_width, -base_y_follow+2, game_graphics, bottom_wall=False, top_wall=False, left_wall=False)
grounds.append(base_ground5)
base_y_follow -= base_ground5.brick_height

base_ground5_filler = game.BrickGround(base_ground5.x, base_ground5.y-base_ground5.height, 10, 3, game_graphics, top_wall=False, left_wall=False, bottom_wall=False, right_wall=False)
grounds.append(base_ground5_filler)

# base ground 6
base_ground6 = game.BrickGround(base_x_follow*tile_size[0], base_y_follow*tile_size[1], 30, 1, game_graphics, bottom_wall=False, right_wall=False, left_wall=False)
grounds.append(base_ground6)
base_x_follow += base_ground6.brick_width

base_ground6_filler = game.BrickGround(base_ground6.x, base_ground6.y-base_ground6.height, 30, 3, game_graphics, top_wall=False, left_wall=False, bottom_wall=False, right_wall=False)
grounds.append(base_ground6_filler)

# base ground 7
base_y_follow += 4
base_ground7 = game.BrickGround(base_x_follow*tile_size[0], base_y_follow*tile_size[1], 15, 4, game_graphics, bottom_wall=False, right_wall=False)
grounds.append(base_ground7)
base_x_follow += base_ground7.brick_width

base_ground7_filler = game.BrickGround(base_ground7.x, base_ground7.y-base_ground7.height, 15, 3, game_graphics, top_wall=False, left_wall=False, bottom_wall=False, right_wall=False)
grounds.append(base_ground7_filler)

# base ground 7
base_y_follow += 5
base_ground8 = game.BrickGround(base_x_follow*tile_size[0], base_y_follow*tile_size[1], 17, 5, game_graphics, bottom_wall=False, right_wall=False, top_wall=False)
grounds.append(base_ground8)
base_x_follow += base_ground8.brick_width

base_ground8_filler = game.BrickGround(base_ground8.x, base_ground8.y-base_ground8.height, 17, 7, game_graphics, top_wall=False, left_wall=False, bottom_wall=False, right_wall=False)
grounds.append(base_ground8_filler)

base_ground8_top_filler = game.BrickGround(base_ground8.x, base_ground8.y+(3*tile_size[1]), 17, 3, game_graphics, left_wall=False, bottom_wall=False, right_wall=False)
grounds.append(base_ground8_top_filler)


# enemies
demon1 = game.Demon(500, 100, game_graphics, random_movement=False)
characters.append(demon1)

demon2 = game.Demon(1000, 200, game_graphics)
characters.append(demon2)

demon3 = game.Demon(1860, -200, game_graphics, random_movement=False)
characters.append(demon3)

demon4 = game.Demon(2400, -200, game_graphics)
characters.append(demon4)


# triggers
def camera_down(character):
    global game_graphics
    if character.character_type == "player":
        game_graphics.camera.y = -200


camera_trigger = dev.Trigger(pygame.Rect(base_ground5.x+base_ground5.width, -(base_ground5.y + tile_size[1]*2), tile_size[0]*4, tile_size[1]*4), camera_down, pass_value=True)
triggers.append(camera_trigger)
