from main_folder.game_tools import *


class DefaultSword(Sword):
    info = {
        "name": "default",
        "frames": {
            "up": {
                "right": pygame.image.load("images/default-sword/weapon_anime_sword_up_right.png"),
                "left": pygame.image.load("images/default-sword/weapon_anime_sword_up_left.png")
            },
            "side": {
                "right": pygame.image.load("images/default-sword/weapon_anime_sword_side_right.png"),
                "left": pygame.image.load("images/default-sword/weapon_anime_sword_side_left.png")
            }
        },
        "switching-wait-frame": int(manager.game_loop.fps/4),
        "size": [10, 25],
        "fix": [7, 5, 3, 0]
    }
    sword_name = info["name"]
    size = info["size"]
    frames = info["frames"]

    # resizing images
    for sword_frame in frames:
        for sword_direction in frames[sword_frame]:
            if sword_frame == "up":
                frames[sword_frame][sword_direction] = pygame.transform.scale(
                    frames[sword_frame][sword_direction], size)
            else:
                frames[sword_frame][sword_direction] = pygame.transform.scale(
                    frames[sword_frame][sword_direction], [size[1], size[0]])

    switching_wait_frame = info["switching-wait-frame"]
    fix = info["fix"]

    def __init__(self, player):
        super().__init__(player)
        self.setup()
