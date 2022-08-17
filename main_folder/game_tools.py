import graphics
from shape_types import *
import manager
import random
import user_input


class Character:
    # character information
    shape = None  # the image
    size = []
    x = 0
    y = 0
    jump_speed = 15
    velocity = [0, 0]  # resets every loading time
    character_type = ""  # to differentiate between players and enemies or others
    collider_info = None  # more accurate box collider [offset x, offset y, width, length]

    # animation information

    # idle animation
    idle_right_file_names = []
    idle_right_frames = []
    idle_right_frames_length = 0
    idle_left_file_names = []
    idle_left_frames = []
    idle_left_frames_length = 0
    idle_wait_frames = 0
    idle_frame = 0

    # right and left movement and animation
    run_right_file_names = []
    run_right_frames = []
    run_right_frames_length = 0
    run_left_file_names = []
    run_left_frames = []
    run_left_frames_length = 0
    run_wait_frames = 0
    run_frame = 0

    # jumping movement and animation
    jumping = False
    jump_count = 0
    jump_wait_frame = 0

    falling = False  # used to know when on ground

    frame = 0
    animation_state = "idle"  # what animation is happening
    facing = "right"  # where is the character facing

    run_speed = 0

    animation_looper = None
    movement_looper = None

    def image_animation(self):
        self.frame += 1

        # idle animation
        if self.animation_state == "idle":
            if self.frame % self.idle_wait_frames == 0:
                if self.facing == "right":
                    self.idle_frame += 1
                    if self.idle_frame == self.idle_right_frames_length:
                        self.idle_frame = 0

                    self.shape.image = self.idle_right_frames[self.idle_frame]
                elif self.facing == "left":
                    self.idle_frame += 1
                    if self.idle_frame == self.idle_left_frames_length:
                        self.idle_frame = 0

                    self.shape.image = self.idle_left_frames[self.idle_frame]

        # run right animation
        elif self.animation_state == "run-right":
            self.facing = "right"
            if self.frame % self.run_wait_frames == 0:
                self.run_frame += 1
                if self.run_frame == self.run_right_frames_length:
                    self.run_frame = 0
                self.shape.image = self.run_right_frames[self.run_frame]

        # run left animation
        elif self.animation_state == "run-left":
            self.facing = "left"
            if self.frame % self.run_wait_frames == 0:
                self.run_frame += 1
                if self.run_frame == self.run_left_frames_length:
                    self.run_frame = 0
                self.shape.image = self.run_left_frames[self.run_frame]

        # sprint right animation
        elif self.animation_state == "sprint-right":
            self.facing = "right"
            if self.frame % int(self.run_wait_frames/2) == 0:
                self.run_frame += 1
                if self.run_frame == self.run_right_frames_length:
                    self.run_frame = 0
                self.shape.image = self.run_right_frames[self.run_frame]

        # sprint left animation
        elif self.animation_state == "sprint-left":
            self.facing = "left"
            if self.frame % int(self.run_wait_frames/2) == 0:
                self.run_frame += 1
                if self.run_frame == self.run_left_frames_length:
                    self.run_frame = 0
                self.shape.image = self.run_left_frames[self.run_frame]

        # adjusting the x and y position of the image
        self.shape.x = self.x
        self.shape.y = self.y

        # resetting the frame counter every 20 seconds
        if self.frame > manager.game_loop.fps * 20:
            self.frame = 0

        # jumping state checker
        if self.jumping:
            self.jump_count += 1
            if self.jump_count >= self.jump_wait_frame:
                self.finish_jump()

    def setup_character_from_dict(self, information):
        self.idle_right_file_names = []
        self.idle_right_frames = []
        self.idle_right_frames_length = 0
        self.idle_left_file_names = []
        self.idle_left_frames = []
        self.idle_left_frames_length = 0
        self.idle_wait_frames = 0
        self.idle_frame = 0

        self.run_right_file_names = []
        self.run_right_frames = []
        self.run_right_frames_length = 0
        self.run_left_file_names = []
        self.run_left_frames = []
        self.run_left_frames_length = 0
        self.run_wait_frames = 0
        self.run_frame = 0

        self.size = information["size"]

        self.idle_right_file_names = information["idle-right-files"]
        for file_name in self.idle_right_file_names:
            idle_image = pygame.transform.scale(pygame.image.load(file_name), self.size).convert_alpha()
            self.idle_right_frames.append(idle_image)
        self.idle_right_frames_length = len(self.idle_right_frames)
        self.shape.image = self.idle_right_frames[self.idle_frame]

        self.idle_left_file_names = information["idle-left-files"]
        for file_name in self.idle_left_file_names:
            idle_image = pygame.transform.scale(pygame.image.load(file_name), self.size).convert_alpha()
            self.idle_left_frames.append(idle_image)
        self.idle_left_frames_length = len(self.idle_left_frames)

        self.run_right_file_names = information["run-right-files"]
        for file_name in self.run_right_file_names:
            run_image = pygame.transform.scale(pygame.image.load(file_name), self.size).convert_alpha()
            self.run_right_frames.append(run_image)
        self.run_right_frames_length = len(self.run_right_frames)

        self.run_left_file_names = information["run-left-files"]
        for file_name in self.run_left_file_names:
            run_image = pygame.transform.scale(pygame.image.load(file_name), self.size).convert_alpha()
            self.run_left_frames.append(run_image)
        self.run_left_frames_length = len(self.run_left_frames)

        self.idle_wait_frames = information["idle-wait-frame"]

        self.run_wait_frames = information["run-wait-frame"]

        if "box-collider" in information:
            self.collider_info = information["box-collider"]
        else:
            self.collider_info = [0, 0, self.size[0], self.size[1]]

    def surfaces_to_string(self):
        counter = 0
        frames = self.idle_right_frames
        for frame in frames:
            frames[counter] = None
            counter += 1

        counter = 0
        frames = self.idle_left_frames
        for frame in frames:
            frames[counter] = None
            counter += 1

        counter = 0
        frames = self.run_right_frames
        for frame in frames:
            frames[counter] = None
            counter += 1

        counter = 0
        frames = self.run_left_frames
        for frame in frames:
            frames[counter] = None
            counter += 1

        self.shape.image = None
        self.shape.game_graphics = None

    def jump(self):
        if not self.jumping and not self.falling:
            self.jumping = True
            self.jump_count = 0

    def finish_jump(self):
        self.jumping = False
        self.jump_count = 0
        self.jump_speed = Character.jump_speed

        # remove later
        self.falling = True

    def movement(self):
        self.before_movement()
        grounds = self.shape.game_graphics.storage["grounds"]
        characters = self.shape.game_graphics.storage["characters"]

        # run right
        if self.animation_state == "run-right":
            self.velocity[0] += self.run_speed
            self.extra_run_right()
        elif self.animation_state == "sprint-right":
            self.velocity[0] += 2 * self.run_speed
            self.extra_sprint_right()

        # run left
        if self.animation_state == "run-left":
            self.velocity[0] -= self.run_speed
            self.extra_run_left()
        elif self.animation_state == "sprint-left":
            self.velocity[0] -= 2 * self.run_speed
            self.extra_sprint_left()

        # jumping
        if self.jumping:
            if self.jump_count < int(self.jump_wait_frame):
                self.velocity[1] += self.jump_speed

                self.extra_jump()
        else:
            self.jump_speed = Character.jump_speed

        self.x += self.velocity[0]
        self.y += self.velocity[1]

        velocity = self.velocity.copy()
        self.velocity = [0, 0]

        # ground collision
        box_collider = self.get_box_collider()
        collided = False
        for ground in grounds:
            if box_collider.colliderect(ground.box_collider):
                collided = True

                # jumping ground collision
                if velocity[1] > 0:
                    box_collider.y -= -velocity[1]
                    if not box_collider.colliderect(ground.box_collider):
                            self.falling = True
                            self.finish_jump()
                            # self.y += -velocity[1]
                            self.y = -ground.box_collider[1] - ground.box_collider[3] + self.collider_info[1]

                    box_collider.y += -velocity[1]

                # right ground collision
                if velocity[0] > 0:
                    box_collider.x -= velocity[0]
                    if not box_collider.colliderect(ground.box_collider):
                            self.falling = False
                            # self.x += -velocity[0]
                            self.x = ground.box_collider[0] - box_collider[2] - self.collider_info[0]

                    box_collider.x += velocity[0]

                # left ground collision
                if velocity[0] < 0:
                    box_collider.x -= velocity[0]
                    if not box_collider.colliderect(ground.box_collider):
                            self.falling = False
                            # self.x += -velocity[0]
                            self.x = ground.box_collider[0] + ground.box_collider[2] - self.collider_info[0]

                    box_collider.x += velocity[0]

                # bottom ground collision
                if velocity[1] < 0:
                    box_collider.y -= -velocity[1]
                    if not box_collider.colliderect(ground.box_collider):
                        self.falling = False
                        # self.y += -velocity[1]
                        self.y = -ground.box_collider[1] + box_collider[3] + self.collider_info[1]

                    else:
                        self.falling = True

                    box_collider.y += -velocity[1]
                else:
                    self.falling = True
        if not collided and velocity[1] < 0:
            self.falling = True

        # character collision
        minimum_bits = 10
        side_minimum = 15
        for character in characters:
            if character == self:
                continue
            # other_character_collider = character.get_box_collider()
            if self.mask_collide(character.get_mask(), character.x, character.y) >= minimum_bits:
                # jump character collision
                if velocity[1] > 0:
                    if self.mask_collide(character.get_mask(), character.x, character.y + velocity[1]) < minimum_bits:
                        # self.y = -other_character_collider[1] - other_character_collider[3] + self.collider_info[1]
                        self.on_character_collision(character)
                        self.top_character_collision(character)
                        character.stump(self)
                        character.on_character_collision(self)

                # right character collision
                if velocity[0] > 0:
                    if self.mask_collide(character.get_mask(), character.x + velocity[0], character.y) < side_minimum:
                        # self.x = other_character_collider[0] - box_collider[2] - self.collider_info[0]
                        self.on_character_collision(character)
                        self.side_character_collision(character)
                        self.right_character_collision(character)
                        character.side_character_collision(self)
                        character.left_character_collision(self)
                        character.on_character_collision(self)

                # left character collision
                if velocity[0] < 0:
                    if self.mask_collide(character.get_mask(), character.x + velocity[0], character.y) < side_minimum:
                        # self.x = other_character_collider[0] + other_character_collider[2] - self.collider_info[0]
                        self.on_character_collision(character)
                        self.side_character_collision(character)
                        self.left_character_collision(character)
                        character.side_character_collision(self)
                        character.right_character_collision(self)
                        character.on_character_collision(self)

                # bottom character collision
                if velocity[1] < 0:
                    if self.mask_collide(character.get_mask(), character.x, character.y + velocity[1]) < minimum_bits:
                        # self.y = -other_character_collider[1] + box_collider[3]
                        self.on_character_collision(character)
                        self.stump(character)
                        character.top_character_collision(self)
                        character.on_character_collision(self)

        self.after_movement()

    def on_character_collision(self, character):
        if character.character_type != self.character_type:
            self.falling = False
            self.jump()
            self.jump_count = self.jump_wait_frame/4

    def side_character_collision(self, character):
        pass

    def stump(self, character):
        pass

    def top_character_collision(self, character):
        pass

    def right_character_collision(self, character):
        pass

    def left_character_collision(self, character):
        pass

    def die(self):
        self.shape.game_graphics.shape_list.remove(self.shape)
        self.shape.game_graphics.storage["characters"].remove(self)
        if self.animation_looper:
            self.shape.game_graphics.looper_list.remove(self.animation_looper)
        if self.movement_looper:
            self.shape.game_graphics.looper_list.remove(self.movement_looper)
        self.after_death()

    def after_death(self):
        pass

    def get_box_collider(self):
        return pygame.Rect(self.x + self.collider_info[0], -self.y + self.collider_info[1], self.collider_info[2], self.collider_info[3])

    def extra_run_right(self):
        pass

    def extra_run_left(self):
        pass

    def extra_sprint_right(self):
        pass

    def extra_sprint_left(self):
        pass

    def extra_jump(self):
        pass

    def before_movement(self):
        pass

    def after_movement(self):
        pass

    def mask_collide(self, second_mask, x, y):
        first_mask = pygame.mask.from_surface(self.shape.image)
        offset = [x - self.x, -y - -self.y]
        return first_mask.overlap_area(second_mask, offset)

    def get_mask(self):
        mask = pygame.mask.from_surface(self.shape.image)
        return mask


class Ground:
    images = []
    box_collider = None
    ground_type = "basic"

    def __init__(self, images, box_collider):
        self.images = images
        self.box_collider = box_collider


class Player(Character):
    character_type = "player"
    dashed = False
    dash_cool_down = False
    dash_frame = 0
    original_dash_force = 6
    dash_force = original_dash_force
    dash_wait_frame = int(manager.game_loop.fps/3)
    dash_frame_reset = manager.game_loop.fps*3
    dash_cloud = None
    weapon = None
    run_speed = 3

    def __init__(self, game_graphics, player_info):
        # setting up player image
        player_shape = graphics.Shape(game_graphics, image)
        change_to_image(player_shape, 0, 0, "player frames", load=False)

        # setting player info
        self.shape = player_shape
        self.setup_character_from_dict(player_info)

        game_graphics.add_shape(player_shape)

        # player movement loop
        player_movement_looper = user_input.Looper("player-movement", self.movement)
        game_graphics.add_looper(player_movement_looper)
        self.animation_looper = player_movement_looper

        # setting up the animation loop
        player_image_animation_looper = user_input.Looper("player-image-animation", self.image_animation)
        game_graphics.add_looper(player_image_animation_looper)
        self.animation_looper = player_image_animation_looper

    def stump(self, character):
        if character.character_type == "enemy":
            character.die()
            self.velocity[1] += 10

    def side_character_collision(self, character):
        if character.character_type == "enemy":
            character.side_character_collision(self)

    def right_character_collision(self, character):
        if character.character_type == "enemy":
            character.left_character_collision(self)

    def left_character_collision(self, character):
        if character.character_type == "enemy":
            character.right_character_collision(self)

    def on_character_collision(self, character):
        pass

    def dash_animation(self):
        if self.dashed:
            self.dash_frame += 1
            if self.dash_frame % self.dash_wait_frame == 0:
                self.dashed = False
                self.dash_cool_down = True
                self.dash_frame = 0
                self.dash_cloud.delete_cloud()
                self.dash_cloud = None
        if self.dash_cool_down:
            self.dash_frame += 1
            self.dash_force = self.dash_force * 0.5 - int(self.run_speed*3/4)
            if self.dash_frame % int(self.dash_wait_frame*2) == 0:
                self.dash_frame = 0
                self.dash_cool_down = False
                self.dash_force = self.original_dash_force

    def extra_run_right(self):
        if self.dashed:
            self.x += self.dash_force

    def extra_run_left(self):
        if self.dashed:
            self.x -= self.dash_force

    def extra_sprint_right(self):
        if self.dashed:
            self.x += self.dash_force

    def extra_sprint_left(self):
        if self.dashed:
            self.x -= self.dash_force

    def extra_jump(self):
        if self.dashed:
            self.y += self.dash_force

    def dash(self, reset=False):
        if (not self.dashed and not self.dash_cool_down) or reset:
            self.dash_frame = 0
            self.dashed = True
            self.dash_force = self.original_dash_force
            self.dash_cloud = Cloud(self.x, self.y-self.size[1]*0.9, self.shape.game_graphics, size=[Cloud.size[0], Cloud.size[1]*0.5])

    def setup_dash(self, game_graphics):
        game_graphics.add_looper(user_input.Looper("player-dash", self.dash_animation))

    def before_movement(self):
        if self.dash_cloud:
            self.dash_cloud.x = self.x
            self.dash_cloud.y = self.y - self.size[1] + self.dash_cloud.size[1]
            self.dash_cloud.animate()

    def die(self):
        now = self.after_movement
        def dying():
            self.y += 80
            self.after_movement = now
        self.after_movement = dying


class Enemy(Character):
    character_type = "enemy"
    enemy_type = ""
    random_movement_frame = 0
    random_movement_wait_frame = 0
    random_movement_looper = None
    attacking = False
    attacking_frame = 0
    attacking_wait_frame = int(manager.game_loop.fps*0.5)

    def stump(self, character):
        if character.character_type == "player":
            character.die()

    def random_movement(self):
        pass

    def side_character_collision(self, character):
        if character.character_type == "player":
            self.attacking = True
            character.die()
            if self.attacking_wait_frame < self.attacking_frame < (self.attacking_wait_frame*1.1):
                self.enemy_specific_attack(character)

    def before_movement(self):
        self.attacking_frame += 1
        if self.attacking:
            if self.attacking_frame >= (self.attacking_wait_frame*1.1):
                self.attacking_frame = 0
                self.attacking = False

    def enemy_specific_attack(self, character):
        character.die()

    def on_character_collision(self, character):
        pass


class Cloud:
    frames = [pygame.image.load("images/cloud/t2.png"), pygame.image.load("images/cloud/t3.png")]
    size = [30, 12]
    frame = 0
    frame_on = 0
    frame_length = 2
    wait_frame = manager.game_loop.fps/8

    def __init__(self, x, y, game_graphics, size=size):
        self.x = x
        self.y = y
        self.shape = graphics.Shape(game_graphics, image)

        if size != self.size:
            self.size = size
            self.frames = [pygame.transform.scale(frame, size) for frame in self.frames]

        change_to_image(self.shape, x, y, "cloud image", self.frames[0])
        game_graphics.add_shape(self.shape)
        # self.animation_looper = user_input.Looper("cloud animation", self.animate)
        # game_graphics.add_looper(self.animation_looper)

    def animate(self):
        self.frame += 1
        self.shape.x = self.x
        self.shape.y = self.y
        if self.frame % self.wait_frame == 0:
            self.frame_on += 1
            if self.frame_on >= self.frame_length:
                self.frame_on = 0
            self.shape.image = self.frames[self.frame_on]

    def delete_cloud(self):
        self.shape.game_graphics.shape_list.remove(self.shape)
        # self.shape.game_graphics.looper_list.remove(self.animation_looper)


class Item:
    state = "stationary"
    x = 0
    y = 0


class Sword(Item):
    size = [0, 0]
    fix = [0, 0, 0, 0]
    frames = []
    sword_name = "default"
    frame = 0
    attacking = False
    cool_down = False
    cool_down_wait_frame = int(manager.game_loop.fps*3/4)
    up_or_side = "up"
    switching_wait_frame = int(manager.game_loop.fps/2)
    image_shape = None
    loop_looper = None
    collider_info = [0, 0, 0, 0]
    weapon_type = "sword"

    def __init__(self, player):
        self.player = player

    def setup(self):
        self.image_shape = graphics.Shape(self.player.shape.game_graphics, image)
        change_to_image(self.image_shape, 0, 0, "sword-pic", self.frames[self.up_or_side][self.player.facing])
        self.player.weapon = self
        self.loop_looper = user_input.Looper("sword-loop", self.loop)
        self.player.shape.game_graphics.add_looper(self.loop_looper)
        self.player.shape.game_graphics.add_shape(self.image_shape)

    def loop(self):
        pos = self.player.get_box_collider()
        if self.player.facing == "right":
            if self.up_or_side == "up":
                self.image_shape.x = pos[0] + pos[2] - self.fix[0]
            else:
                self.image_shape.x = pos[0] + pos[2] - self.fix[1]
        else:
            if self.up_or_side == "up":
                self.image_shape.x = pos[0] - self.size[0] + self.fix[0]
            else:
                self.image_shape.x = pos[0] - self.size[1] + self.fix[1]

        if self.up_or_side == "up":
            self.image_shape.y = -pos[1] - self.fix[2]
        else:
            self.image_shape.y = -pos[1] - (pos[3]/2) - self.fix[3]

        # do the attacking animation
        if self.attacking:
            self.frame += 1

            # switching between two frames
            if self.frame % self.switching_wait_frame == 0:
                if self.up_or_side == "up":
                    self.up_or_side = "side"
                else:
                    self.up_or_side = "up"
            # start cool down
            if self.frame == (self.switching_wait_frame*2):
                self.attacking = False
                self.cool_down = True
                self.frame = 0

        # end cool down
        if self.cool_down:
            self.frame += 1
            if self.frame >= self.cool_down_wait_frame:
                self.cool_down = False
                self.frame = 0

        self.image_shape.image = self.frames[self.up_or_side][self.player.facing]

    def attack(self, ignore=False):
        if (not self.attacking and not self.cool_down) or ignore:
            self.attacking = True
            self.frame = 0

    # info: {"name", "frames", "size", "switching-wait-frame", "fix"}
    def setup_sword_from_info(self, info):
        self.sword_name = info["name"]
        self.size = info["size"]
        self.frames = info["frames"]

        # resizing images
        for sword_frame in self.frames:
            for sword_direction in self.frames[sword_frame]:
                if sword_frame == "up":
                    self.frames[sword_frame][sword_direction] = pygame.transform.scale(self.frames[sword_frame][sword_direction], self.size)
                else:
                    self.frames[sword_frame][sword_direction] = pygame.transform.scale(self.frames[sword_frame][sword_direction], [self.size[1], self.size[0]])

        self.switching_wait_frame = info["switching-wait-frame"]
        self.fix = info["fix"]
        if "collider-info" in info:
            self.collider_info = info["collider-info"]
        if "cool-down-wait-frame" in info:
            self.cool_down_wait_frame = info["cool-down-wait-frame"]

    def get_box_collider(self):
        if self.up_or_side == "up":
            return pygame.Rect(self.image_shape.x + self.collider_info[0], -(self.image_shape.y-self.collider_info[1]), self.size[0]-self.collider_info[2], self.size[1]-self.collider_info[3])
        else:
            return pygame.Rect(self.image_shape.x + self.collider_info[0], -(self.image_shape.y - self.collider_info[1]), self.size[0] - self.collider_info[2], self.size[1] - self.collider_info[3])

    def get_mask(self):
        return pygame.mask.from_surface(self.image_shape.image)