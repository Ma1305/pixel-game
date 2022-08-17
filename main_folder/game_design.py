from main_folder.game_setup import *
import main_folder.development_tools as dev
# import main_folder.levels.level1
# import importlib
import pickle

# mod = importlib.import_module("main_folder.levels.level1")
levels_reference = {}

levels_name = [
    "level1",
    "level2",
]


def load_level(name):
    level_info = pickle.load(open("main_folder/levels/" + name, "rb"))
    new_level = Level()
    for info in level_info:
        if info["type"] == "set_info":
            for change in info["data"]:
                setattr(change["type"], change["var"], change["value"])
            continue
        # object
        if "game_graphics" in info["data"]:
            info["data"]["game_graphics"] = new_level.game_graphics
        oj = info["type"](**info["data"])
        new_level.game_graphics.storage[info["add_to"]].append(oj)

    print(level_info)
    levels_reference[name] = new_level
    new_level.setup_level()


for level in levels_name:
    load_level(level)


