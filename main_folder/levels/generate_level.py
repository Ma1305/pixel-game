import pickle
import importlib


name = input("enter the full level name (add main_folder.levels if necessarily): ")
level = importlib.import_module(name)
print("loaded successfully\n")

new_file_name = input("enter the new file name")

info = level.level.game_graphics.storage
pickle.dump(info, new_file_name)

