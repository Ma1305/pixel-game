import pickle
# import main_folder.game
from main_folder.game_setup import *
import manager
import json
# import importlib
import sys
import inspect


def str_to_class(classname):
    return getattr(sys.modules[__name__], classname)


def str2bool(v):
    return v.lower().strip() in ("yes", "true", "t", "1")


'''name = input("enter the full level name (add main_folder.levels if necessarily): ")
level = importlib.import_module(name)
print("loaded successfully\n")

new_file_name = input("enter the new file name")

info = level.level.game_graphics.storage
pickle.dump(info, new_file_name)

demon4_info = {"name": "demon1", "type": "game.Demon", "add_to": "characters", "data": "{'x': 'follow_pos_x', 'y': 'follow_pos_y', 'game_graphics': 'None'}", "follow_pos": "{'x_attr':'x', 'y_attr':'y', 'cursor_filter': 10}"}
o
main_folder/levels/level2
change_name
main_folder/levels/level1
add
game.Demon
demon1
characters
100 int
150 int
false bool
ignore i
ignore i
false bool

'''

disable_input = False
get_mouse_pos = False

follow_pos = False
follow_object = None
info_object = None
x_attr = ""
y_attr = ""
info_x_attr = ""
info_y_attr = ""
cursor_filter = 1
follow_dimensions = False
camera_follow = False


def mouse_pos():
    global disable_input, get_mouse_pos, follow_pos, follow_object, cursor_filter, follow_dimensions, level
    pos = level.game_graphics.camera.real_to_vr(pygame.mouse.get_pos())
    if get_mouse_pos:
        print(pos)

    if follow_pos:
        setattr(follow_object, x_attr, int(pos[0] / cursor_filter) * cursor_filter)
        setattr(follow_object, y_attr, int(pos[1] / cursor_filter) * cursor_filter)
        info_object["data"][info_x_attr] = int(pos[0] / cursor_filter) * cursor_filter
        info_object["data"][info_y_attr] = int(pos[1] / cursor_filter) * cursor_filter

    if pygame.key.get_pressed()[pygame.K_RETURN]:
        disable_input = False
        get_mouse_pos = False

        follow_pos = False
        follow_object = None
        cursor_filter = 1
        follow_dimensions = False


def add_info():
    global x_attr, y_attr, follow_pos, follow_object, info_object, info_x_attr, info_y_attr, disable_input, cursor_filter
    while True:
        type_info = "q"
        try:
            type_info = input("Enter the type: ")
            if type_info != "set_info":
                type_info = eval(type_info)
        except Exception as e:
            print("Wrong type or:")
            print(e)

        if type_info == "q" or type_info == "exit":
            return False

        info_dict = {"data": {}}
        info_dict["type"] = type_info

        try:
            if type_info != "set_info":
                info_dict["name"] = input("Enter the name: ")
                info_dict["add_to"] = input("Enter the add_to: ")

                # parameters = type_info.__init__.__code__.co_varnames
                parameters = inspect.getfullargspec(type_info.__init__).args
                defaults = inspect.getfullargspec(type_info.__init__).defaults
                end = len(parameters) - len(defaults)
                counter = 0
                for pr in parameters:
                    counter += 1
                    if pr == "self":
                        continue
                    while True:
                        try:
                            if counter > end:
                                print("defaults - ", end="")
                            value, value_type = input(f"value for {pr}: ").split()
                            if value == "ignore" and counter <= end:
                                print("can't skip this one")
                                continue
                            elif value == "ignore" and counter > end:
                                break
                            else:
                                info_dict["data"][pr] = eval(value_type)(value)
                                break
                        except Exception as e:
                            print("probably forgot to enter both values or wrong type or: ")
                            print(e)

                while True:
                    response = input("Do you want to add follow pos (y ot n): ")
                    if response == "y":
                        follow_pos_dict = {}
                        follow_pos_dict["x_attr"] = input("Enter x attribute: ")
                        follow_pos_dict["y_attr"] = input("Enter y attribute: ")
                        follow_pos_dict["cursor_filter"] = int(input("Enter cursor filter: "))
                        info_dict["follow_pos"] = follow_pos_dict
                        print("successfully added the follow-pos")
                        break
                    elif response == "n":
                        break

                # info_dict = json.loads(information)
                # info_dict["type"] = eval(info_dict["type"])
                # print(info_dict, type(info_dict))
                if info_dict["type"] == "set_info":
                    for change in info_dict["data"]:
                        setattr(change["type"], change["var"], change["value"])
                    continue
                # object
                # info_dict["data"] = info_dict["data"].replace("'", "\"")
                # info_dict["data"] = json.loads(info_dict["data"])
                if "game_graphics" in info_dict["data"]:
                    info_dict["data"]["game_graphics"] = level.game_graphics

                for items in info_dict["data"]:
                    if info_dict["data"][items] == "follow_pos_x":
                        info_dict["data"][items] = 0
                        info_x_attr = items
                        follow_pos = True
                        info_object = info_dict
                        disable_input = True
                    elif info_dict["data"][items] == "follow_pos_y":
                        info_dict["data"][items] = 0
                        info_y_attr = items
                        follow_pos = True
                        info_object = info_dict
                        disable_input = True

                set_follow_object = False
                if "follow_pos" in info_dict:
                    x_attr = info_dict["follow_pos"]["x_attr"]
                    y_attr = info_dict["follow_pos"]["y_attr"]
                    cursor_filter = info_dict["follow_pos"]["cursor_filter"]
                    set_follow_object = True

                oj = info_dict["type"](**info_dict["data"])
                level.game_graphics.storage[info_dict["add_to"]].append(oj)
                if "game_graphics" in info_dict["data"]:
                    info_dict["data"]["game_graphics"] = None
                all_info.append(info_dict)

                if set_follow_object:
                    follow_object = oj
                break
        except Exception as e:
            print("oops something went wrong here!")
            print(e)

    print("successfully added the info!")


def modify_info():
    print_info()
    info = None
    while True:
        item_name = input("Enter the name of the item: ")
        if item_name == "cancel":
            return
        for item in all_info:
            if "name" in item:
                if item["name"] == item_name:
                    info = item
                    break
        if info:
            break
        else:
            print("couldn't find your name - (enter cancel to leave)")

    print("got this info: ", info)
    print("options for edit (remove or change): ")
    counter = 0
    for item in info:
        counter += 1
        print(f"{counter}. name: {item} - value: {info[item]}")

    while True:
        try:
            action, item = input("Enter the action and item name: ").split()
            break
        except ValueError:
            print("Don't forget to enter both parameters")

    if action == "change" and item == "data":
        parameters = inspect.getfullargspec(info["type"].__init__).args
        defaults = inspect.getfullargspec(info["type"].__init__).defaults
        end = len(parameters) - len(defaults)
        while True:
            print("options for edit (remove or change): ")
            counter = 0
            for pr in parameters:
                counter += 1
                if counter <= end:
                    print(f"{counter}. name: {pr} - value: mandatory")
                elif counter > end:
                    print(f"{counter}. name: {pr} - value: optional")

            while True:
                try:
                    second_action, second_item = input("Enter the action and item name: ").split()
                    break
                except ValueError:
                    print("don't forget to enter both parameters")

            if second_action == "remove" and second_item not in info["data"]:
                print("this parameter does not exist, and can not be removed")
            else:
                break

        if second_action == "change":
            value, value_type = input("enter the new value: ").split()
            info["data"][second_item] = eval(value_type)(value)
            print("successfully changed the value")
        elif second_action == "remove":
            info["data"].pop(second_item)

    elif action == "change":
        value, value_type = input("enter the new value: ").split()
        info[item] = eval(value_type)(value)
        print("successfully changed the value")
    elif action == "remove" and item == "item":
        all_info.remove(info)
    elif action == "remove":
        info.pop(item)


def camera():
    global disable_input, camera_follow
    disable_input = True
    camera_follow = True


def camera_follow_loop():
    global camera_follow, disable_input
    camera_speed = 4
    if camera_follow:
        if pygame.key.get_pressed()[pygame.K_RIGHT]:
            level.game_graphics.camera.x += camera_speed
        if pygame.key.get_pressed()[pygame.K_LEFT]:
            level.game_graphics.camera.x -= camera_speed
        if pygame.key.get_pressed()[pygame.K_DOWN]:
            level.game_graphics.camera.y -= camera_speed
        if pygame.key.get_pressed()[pygame.K_UP]:
            level.game_graphics.camera.y += camera_speed
        if pygame.key.get_pressed()[pygame.K_RETURN]:
            camera_follow = False
            disable_input = False


def save():
    pickle.dump(all_info, open(file_name, "wb"))


def change_name():
    global file_name
    file_name = input("enter the file name: ")
    print("saved file name: " + file_name)


def print_info():
    [print(info) for info in all_info]


def get_pos():
    global get_mouse_pos, disable_input
    disable_input = True
    get_mouse_pos = True


def reload_level():
    global level, all_info
    level.leave_level()
    x = level.game_graphics.camera.x
    y = level.game_graphics.camera.y
    level = Level()
    for info in all_info:
        if info["type"] == "set_info":
            for change in info["data"]:
                setattr(change["type"], change["var"], change["value"])
            continue
        # object
        if "game_graphics" in info["data"]:
            info["data"]["game_graphics"] = level.game_graphics
        oj = info["type"](**info["data"])
        if "game_graphics" in info["data"]:
            info["data"]["game_graphics"] = None
        level.game_graphics.storage[info["add_to"]].append(oj)
    level.start_level()
    level.game_graphics.camera.x = x
    level.game_graphics.camera.y = y

    start()


commands = {
    "add": add_info,
    "modify": modify_info,
    "camera": camera,
    "save": save,
    "change_name": change_name,
    "quit": quit,
    "print_info": print_info,
    "get_pos": get_pos,
    "reload": reload_level,

}

manager.game_loop.make_screen(1600, 900)
manager.game_loop.fps = 60

all_info = []
level = None

file_name = ""

# start
while True:
    response = input("Do you want to make a new file or open a file (n for new, o for open: ")

    if response == "new" or response == "n":
        file_name = input("Enter your file name: ")
        level = Level()
        set_info = {
            "type": "set_info",
            "data": [
            ]
        }
        all_info.append(set_info)
        break

    elif response == "open" or response == "o":
        while True:
            try:
                file_name = input("Enter the file name (add main_folder/levels/ if necessarily): ")
                all_info = pickle.load(open(file_name, "rb"))
                break
            except Exception as e:
                print("something went wrong!")
                print(e)
        # level_info = pickle.load(open("main_folder/levels/" + name, "rb"))
        level = Level()
        for info in all_info:
            if info["type"] == "set_info":
                for change in info["data"]:
                    setattr(change["type"], change["var"], change["value"])
                continue
            # object
            if "game_graphics" in info["data"]:
                info["data"]["game_graphics"] = level.game_graphics
            oj = info["type"](**info["data"])
            if "game_graphics" in info["data"]:
                info["data"]["game_graphics"] = None
            level.game_graphics.storage[info["add_to"]].append(oj)

        break

level.start_level()


def input_loop():
    global disable_input
    if not disable_input:
        command = input("Enter your command: ")
        try:
            commands[command]()
        except KeyError:
            pass


def start():
    input_looper = user_input.Looper("input-loop", input_loop)
    level.game_graphics.add_looper(input_looper)

    # mouse looper
    mouse_looper = user_input.Looper("mouse-pos", mouse_pos)
    level.game_graphics.add_looper(mouse_looper)

    # camera follow looper
    camera_follow_looper = user_input.Looper("camera-follow-looper", camera_follow_loop)
    level.game_graphics.add_looper(camera_follow_looper)

start()