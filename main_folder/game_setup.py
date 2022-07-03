import graphics
from shape_types import *
import user_input
import manager
import main_folder.game as game

# setting up the game graphics
screen = graphics.Screen(900, 700)
game_graphics = graphics.GameGraphics(screen, None)
camera = graphics.Camera(0, 0, 1, game_graphics)
game_graphics.camera = camera

graphics.add_game_graphics(game_graphics)

# setting up the actual game
manager.game_loop.make_screen(900, 700)
manager.game_loop.set_main_game_graphics(game_graphics)
manager.game_loop.fps = 60

game.Character.jump_wait_frame = int(manager.game_loop.fps/2.5)


# game variables
characters = []

grounds = []

traps = []

game_graphics.storage["characters"] = characters
game_graphics.storage["grounds"] = grounds


gravity_force = 5


def gravity():
    global characters
    for character in characters:
        if character.falling:
            character.y -= gravity_force
            box_collider = character.get_box_collider()
            character_collider = pygame.Rect(box_collider[0], box_collider[1], box_collider[2], box_collider[3]+1)
            for other_character in characters:
                if other_character == character:
                    continue
                other_character_collider = other_character.get_box_collider()
                if character_collider.colliderect(other_character_collider):
                    character.y = -other_character_collider[1] + box_collider[3]
                    character.on_character_collision(other_character)
                    character.stump(other_character)

        # checking if character is on the ground
        box_collider = character.get_box_collider()
        character_collider = pygame.Rect(box_collider[0], box_collider[1], box_collider[2], box_collider[3]+1)
        on_ground = False
        for ground in grounds:
            if character_collider.colliderect(ground.box_collider):
                character.falling = False
                character.y = -ground.box_collider[1] + box_collider[3] + character.collider_info[1]
                on_ground = True
                break
        if not on_ground and not character.jumping:
            character.falling = True

        for trap in traps:
            if character_collider.colliderect(trap.box_collider) and character.character_type == "player":
                trap.attack()


gravity_looper = user_input.Looper("gravity", gravity)
game_graphics.add_looper(gravity_looper)


def animate_traps():
    global traps
    for trap in traps:
        trap.animate()


trap_animation_looper = user_input.Looper("trap", animate_traps)
game_graphics.add_looper(trap_animation_looper)