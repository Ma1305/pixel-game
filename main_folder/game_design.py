from main_folder.game_setup import *


# tile information
tile_size = (22, 22)

# left ground
left_ground = game.BrickGround(-440, 440, 20, 20, game_graphics, top_wall=False, left_wall=False, bottom_wall=False, set_sizes=True)
left_ground.set_all_image_sizes()
grounds.append(left_ground)

base_x_follow = 0
base_y_follow = 0

# base ground 1
base_ground1 = game.BrickGround(0, 0, 5, 2, game_graphics, left_wall=False, bottom_wall=False)
grounds.append(base_ground1)
base_x_follow += base_ground1.brick_width
base_y_follow -= base_ground1.brick_height

# base ground 2
base_ground2 = game.BrickGround(base_x_follow*tile_size[0], base_y_follow*tile_size[1], 20, 4, game_graphics, left_wall=False, bottom_wall=False)
grounds.append(base_ground2)
base_x_follow += base_ground2.brick_width
base_y_follow -= base_ground2.brick_height

# base ground 3
base_ground3 = game.BrickGround(base_x_follow*tile_size[0], base_y_follow*tile_size[1], 10, 1, game_graphics, left_wall=False, bottom_wall=False, right_wall=False)
grounds.append(base_ground3)
base_x_follow += base_ground3.brick_width

# base ground 4
base_ground4 = game.BrickGround(base_x_follow*tile_size[0], 2*tile_size[1], 15, -base_y_follow+2, game_graphics, bottom_wall=False)
grounds.append(base_ground4)
base_x_follow += base_ground4.brick_width
base_y_follow = -base_ground4.brick_height+2

# roof ground 1
roof_ground1 = game.BrickGround((base_x_follow+2)*tile_size[0], base_ground4.y, 24, 13, game_graphics, top_wall=True)
grounds.append(roof_ground1)

# base ground 5
base_ground5 = game.BrickGround(base_ground4.x, base_y_follow*tile_size[1], base_ground4.brick_width, -base_y_follow+2, game_graphics, bottom_wall=False, top_wall=False, left_wall=False)
grounds.append(base_ground5)
base_y_follow -= base_ground5.brick_height

# base ground 6
base_ground6 = game.BrickGround(base_x_follow*tile_size[0], base_y_follow*tile_size[1], 30, 1, game_graphics, bottom_wall=False, right_wall=False, left_wall=False)
grounds.append(base_ground6)
base_x_follow += base_ground6.brick_width

# base ground 7
base_y_follow += 4
base_ground7 = game.BrickGround(base_x_follow*tile_size[0], base_y_follow*tile_size[1], 15, 4, game_graphics, bottom_wall=False, right_wall=False)
grounds.append(base_ground7)
base_x_follow += base_ground7.brick_width
