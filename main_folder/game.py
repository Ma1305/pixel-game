import graphics
from shape_types import *
import manager
import random
import user_input
from main_folder.game_tools import *


class Demon(Enemy):
    enemy_type = "demon"
    demon_info = {
        "size": (72, 81),
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
        "box-collider": [20, 20, 32, 61]
    }
    random_movement_wait_frame = manager.game_loop.fps*5
    run_speed = 1

    def __init__(self, x, y, game_graphics, demon_info=demon_info, add_shape=True, random_movement=True):
        self.x = x
        self.y = y
        self.random_movement_frame = 0
        self.shape = graphics.Shape(game_graphics, image)
        change_to_image(self.shape, x, y, "demon frames", load=False)
        self.setup_character_from_dict(self.demon_info)
        self.y = y
        self.x = x

        if add_shape:
            game_graphics.add_shape(self.shape)

        demon_image_animation_looper = user_input.Looper("demon-image-animation", self.image_animation)
        game_graphics.add_looper(demon_image_animation_looper)

        self.animation_looper = demon_image_animation_looper

        self.random_movement_looper = user_input.Looper("demon-random-movement", self.random_movement)
        if random_movement:
            self.add_random_movement()

        self.movement_looper = user_input.Looper("demon-movement-looper", self.movement)
        game_graphics.add_looper(self.movement_looper)

    def add_random_movement(self):
        self.shape.game_graphics.add_looper(self.random_movement_looper)

    def random_movement(self):
        self.random_movement_frame += 1
        if self.random_movement_frame % self.random_movement_wait_frame == 0:
            movement_number = random.randint(1, 4)
            move_mode = ""
            if movement_number == 1:
                move_mode = "run-right"
            elif movement_number == 2:
                move_mode = "run-left"
            elif movement_number == 3:
                move_mode = "sprint-right"
            elif movement_number == 4:
                move_mode = "sprint-left"

            self.animation_state = move_mode

    def after_death(self):
        if self.random_movement_looper in self.shape.game_graphics.looper_list:
            self.shape.game_graphics.looper_list.remove(self.random_movement_looper)


class Trap(Ground, Enemy):
    ground_type = "trap"
    size = [30, 30]
    frames = [
        pygame.image.load("images/trap/muddy_idle_anim_f0.png"),
        pygame.image.load("images/trap/muddy_idle_anim_f1.png"),
        pygame.image.load("images/trap/muddy_idle_anim_f2.png"),
        pygame.image.load("images/trap/muddy_idle_anim_f3.png")
    ]
    frames = [pygame.transform.scale(frame, [30, 30]) for frame in frames]
    frame = 0
    frame_on = 0
    frames_length = 4
    state = "idle"  # idle, attack, cool-down
    attack_wait_frame = int(manager.game_loop.fps/10)
    cool_down_wait_frame = int(manager.game_loop.fps*1.5)

    before_attack = 0
    before_attack_wait_frame = int(manager.game_loop.fps)

    def __init__(self, x, y, game_graphics):
        self.x = x
        self.y = y
        self.box_collider = [x, -y, self.size[0], self.size[1]]
        self.shape = graphics.Shape(game_graphics, image)
        change_to_image(self.shape, x, y, "trap-image", image=self.frames[self.frame_on])
        game_graphics.add_shape(self.shape)

    def animate(self):
        if self.before_attack >= self.before_attack_wait_frame:
            self.frame += 1
            if self.state == "attack":
                for character in self.shape.game_graphics.storage["characters"]:
                    if character.character_type == "player":
                        other_character_collider = character.get_box_collider()
                        box_collider = pygame.Rect(self.x, -self.y, self.size[0], self.size[1])
                        if box_collider.colliderect(other_character_collider):
                            character.die()
        else:
            self.before_attack += 1

        if self.state == "attack":
            if self.frame % self.attack_wait_frame == 0:
                self.frame_on += 1
                self.shape.image = self.frames[self.frame_on]

                if self.frame_on == 2:
                    self.state = "cool-down"

        elif self.state == "cool-down":
            if self.frame % self.cool_down_wait_frame == 0:
                self.frame_on += 1
                if self.frame_on == 4:
                    self.frame_on = 0
                self.shape.image = self.frames[self.frame_on]
                if self.frame_on == 0:
                    self.state = "idle"
                    self.frame += 1
                    self.before_attack = 0

    def attack(self, ignore=False):
        if (self.state != "attack" and self.state != "cool-down") or ignore:
            self.state = "attack"
            self.before_attack = 0


class BrickGround(Ground):
    ground_type = "basic-brick"
    brick_size = [30, 30]
    top_image = pygame.image.load("images/frames/wall_top_mid.png")
    right_image = pygame.image.load("images/frames/wall_corner_right.png")
    left_image = pygame.image.load("images/frames/wall_corner_left.png")
    bottom_image = pygame.image.load("images/frames/wall_top_mid.png")
    middle_image = pygame.image.load("images/frames/wall_mid.png")

    def __init__(self, x, y, brick_width, brick_height, game_graphics, right_wall=True, top_wall=True, left_wall=True, bottom_wall=True, set_sizes=True):
        self.x = x
        self.y = y
        self.width = brick_width * self.brick_size[0]
        self.height = brick_height * self.brick_size[1]
        self.brick_width = brick_width
        self.brick_height = brick_height
        self.game_graphics = game_graphics
        self.right_wall = right_wall
        self.top_wall = top_wall
        self.left_wall = left_wall
        self.bottom_wall = bottom_wall
        if self.brick_size != self.brick_size and not set_sizes:
            self.brick_size = self.brick_size
            self.top_image = pygame.transform.scale(self.top_image, self.brick_size)
            self.right_image = pygame.transform.scale(self.right_image, self.brick_size)
            self.left_image = pygame.transform.scale(self.left_image, self.brick_size)
            self.bottom_image = pygame.transform.scale(self.bottom_image, self.brick_size)
            self.middle_image = pygame.transform.scale(self.middle_image, self.brick_size)
        self.brick_size = self.brick_size

        self.box_collider = pygame.Rect(x, -y, self.width, self.height)
        self.images = []
        if set_sizes:
            self.set_image_sizes()
        else:
            self.create_images()

    def create_images(self):
        self.images = []
        # print(self.brick_size)

        # top
        if self.top_wall:
            for x in range(self.brick_width):
                tile = graphics.Shape(self.game_graphics, image)
                change_to_image(tile, self.brick_size[0]*x + self.x, self.y+int(self.brick_size[1]/1.1), "top-wall", image=self.top_image)
                self.game_graphics.add_shape(tile)
                self.images.append(tile)

        # middle
        for y in range(self.brick_height):
            for x in range(1, self.brick_width-1):
                tile = graphics.Shape(self.game_graphics, image)
                change_to_image(tile, self.x + self.brick_size[0] * x, self.y - self.brick_size[1] * y, "middle-wall", image=self.middle_image)
                self.game_graphics.add_shape(tile)
                self.images.append(tile)

        # left
        if self.left_wall:
            for y in range(self.brick_height):
                tile = graphics.Shape(self.game_graphics, image)
                change_to_image(tile, self.x, self.y-self.brick_size[1]*y, "left-wall", image=self.left_image)
                self.game_graphics.add_shape(tile)
                self.images.append(tile)
        else:
            for y in range(self.brick_height):
                tile = graphics.Shape(self.game_graphics, image)
                change_to_image(tile, self.x, self.y-self.brick_size[1]*y, "left-wall", image=self.middle_image)
                self.game_graphics.add_shape(tile)
                self.images.append(tile)

        # right
        if self.right_wall:
            for y in range(self.brick_height):
                tile = graphics.Shape(self.game_graphics, image)
                change_to_image(tile, self.x + self.width - self.brick_size[0], self.y - self.brick_size[1] * y, "right-wall", image=self.right_image)
                self.game_graphics.add_shape(tile)
                self.images.append(tile)
        else:
            for y in range(self.brick_height):
                tile = graphics.Shape(self.game_graphics, image)
                change_to_image(tile, self.x + self.width - self.brick_size[0], self.y - self.brick_size[1] * y, "right-wall", image=self.middle_image)
                self.game_graphics.add_shape(tile)
                self.images.append(tile)

        # bottom
        if self.bottom_wall:
            for x in range(self.brick_width):
                tile = graphics.Shape(self.game_graphics, image)
                change_to_image(tile, self.brick_size[0]*x + self.x, self.y+self.brick_size[1]-self.height, "top-wall", image=self.top_image)
                self.game_graphics.add_shape(tile)
                self.images.append(tile)

    def set_image_sizes(self):
        self.top_image = pygame.transform.scale(self.top_image, self.brick_size)
        self.right_image = pygame.transform.scale(self.right_image, self.brick_size)
        self.left_image = pygame.transform.scale(self.left_image, self.brick_size)
        self.bottom_image = pygame.transform.scale(self.bottom_image, self.brick_size)
        self.middle_image = pygame.transform.scale(self.middle_image, self.brick_size)
        self.create_images()

    def set_current_sizes(self):
        counter = 0
        for i in self.images:
            self.images[counter] = pygame.transform.scale(i, self.brick_size)
            counter += 1

    def set_all_image_sizes(self):
        # print(self.brick_size)
        BrickGround.top_image = pygame.transform.scale(self.top_image, self.brick_size).convert_alpha()
        BrickGround.right_image = pygame.transform.scale(self.right_image, self.brick_size).convert_alpha()
        BrickGround.left_image = pygame.transform.scale(self.left_image, self.brick_size).convert_alpha()
        BrickGround.bottom_image = pygame.transform.scale(self.bottom_image, self.brick_size).convert_alpha()
        BrickGround.middle_image = pygame.transform.scale(self.middle_image, self.brick_size).convert_alpha()


def set_all_image_sizes(brick_size):
    # print(self.brick_size)
    BrickGround.top_image = pygame.transform.scale(BrickGround.top_image, brick_size)
    BrickGround.right_image = pygame.transform.scale(BrickGround.right_image, brick_size)
    BrickGround.left_image = pygame.transform.scale(BrickGround.left_image, brick_size)
    BrickGround.bottom_image = pygame.transform.scale(BrickGround.bottom_image, brick_size)
    BrickGround.middle_image = pygame.transform.scale(BrickGround.middle_image, brick_size)
