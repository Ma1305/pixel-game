import graphics
from shape_types import *
import user_input
import manager
import main_folder.game as game


# setting up the actual game
game.Character.jump_wait_frame = int(manager.game_loop.fps/2.5)


# game variables


class Level:
    game_graphics = False
    width = 1600
    height = 900
    gravity_force = 6

    def __init__(self, game_graphics=None):
        self.characters = []
        self.surfaces = []
        self.ground_images = []
        self.ground_colliders = []
        self.items = []
        self.grounds = []
        self.traps = []
        self.triggers = []

        if not game_graphics:
            screen = graphics.Screen(self.width, self.height)
            self.game_graphics = graphics.GameGraphics(screen, None)
            camera = graphics.Camera(0, 0, 1, self.game_graphics)

            self.game_graphics.camera = camera
            self.game_graphics.storage["characters"] = self.characters
            self.game_graphics.storage["surfaces"] = self.surfaces
            self.game_graphics.storage["ground_images"] = self.ground_images
            self.game_graphics.storage["ground_colliders"] = self.ground_colliders
            self.game_graphics.storage["items"] = self.items
            self.game_graphics.storage["grounds"] = self.grounds

    def setup_level(self, gravity=True, animate_traps=True, trigger_loops=True):
        # setting up gravity
        if gravity:
            gravity_looper = user_input.Looper("gravity", self.gravity)
            self.game_graphics.add_looper(gravity_looper)

        # setting up the trap animation
        if animate_traps:
            trap_animation_looper = user_input.Looper("trap", self.animate_traps)
            self.game_graphics.add_looper(trap_animation_looper)

        # setting up the trigger loops
        if trigger_loops:
            triggers_looper = user_input.Looper("trigger-loops", self.trigger_loops)
            self.game_graphics.add_looper(triggers_looper)

    def gravity(self):
        for character in self.characters:

            character.velocity[1] -= self.gravity_force

        # setting up gravity for items
        '''for item in self.items:
            if not item.onGround:
                item.y -= gravity_force'''

    def animate_traps(self):
        for trap in self.traps:
            trap.animate()

    def trigger_loops(self):
        for character in self.characters:
            character_collider = character.get_box_collider()

            for trigger in self.triggers:
                if trigger.collide(character_collider):
                    trigger.trig(character)

    def start_level(self):
        self.game_graphics.start()
        manager.game_loop.set_main_game_graphics(self.game_graphics)

    def leave_level(self):
        self.game_graphics.pause()

    def restart_level(self):
        pass
