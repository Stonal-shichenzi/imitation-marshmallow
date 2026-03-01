import json

class minecraft_template():
    class item_type():
        def __init__(self, id = "minecraft:air", count: int = 1):
            self.id = id
            self.num = count
            self.comp = dict()
        def components_push(self, name: str, value):
            if "!{}".format(name) in self.comp:
                del self.comp["!{}".format(name)]
            elif ("!minecraft:" + name) in self.comp:
                del self.comp["!minecraft:" + name]
            obj = name if (":" in name) else ("minecraft:" + name)
            self.comp[obj] = value
        def components_pop(self, name: str):
            if name in self.comp:
                del self.comp[name]
            elif ("minecraft:" + name) in self.comp:
                del self.comp["minecraft:" + name]
            else:
                self.comp["!{}".format(name if (":" in name) else ("minecraft:" + name))] = dict()
        def export(self):
            return {"id": self.id, "components": self.comp, "count": self.num}
        def give_export_item(self):
            give = self.id
            comp = list()
            for i in self.comp.keys():
                if i[0] == "!":
                    comp.append(i)
                else:
                    comp.append("{0}={1}".format(i, self.comp[i]))
            return "{0}[{1}]".format(give, ",".join(comp))
class ListLengthError(Exception):
    pass
class RootAdvencementError(Exception):
    pass
class tag():
    def __init__(self, type_name: str, id: str):
        self.path = "tags/{0}/{1}.json".format(type_name, id)
        self.data = list()
        self.replace = False
    def add_item(self, name: str):
        self.data.append(name)
        return len(self.data) - 1
    def add_required_item(self, name: str, required = True):
        self.data.append({"id": name, "required": required})
        return len(self.data) - 1
    def get_item(self):
        data = list()
        for i in self.data:
            if isinstance(i, dict):
                data.append(i["id"])
            else:
                data.append(i)
    def get_data(self):
        return {"replace": self.replace, "values": self.data}
    def get_json(self):
        return json.dumps(self.get_data())
    def get_arg_std(self):
        return {"path": self.path, "data": self.get_json(), "belong_to_data_pack": True}
class recipe():
    class __type():
        class __crafting_name():
            SHAPED = "crafting_shaped"
            SHAPLESS = "crafting_shapeless"
            TRANSMUTE = "crafting_transmute"
        class __smelting_name():
            SMELTING = "smelting"
            BLASTING = "blasting"
            SMOKING = "smoking"
            COOKING = "campfire_cooking"
            FURNACE = SMELTING
            CAMPFIRE = COOKING
            SOUL_CAMPFIRE = CAMPFIRE
            BLAST_FURNACE = BLASTING
            SMOKER = SMOKING
        class __smithing():
            TRANSFORM = "smithing_transform"
            TRIM = "smithing_trim"
        def __init__(self):
            self.crafting = self.__crafting_name()
            self.furnace = self.__smelting_name()
            self.smithing = self.__smithing()
            self.STONECUTTER = self.STONECUTTING = "stonecutting"
    class __category():
        BUILDING = "building"
        REDSTONE = "redstone"
        EQUIPMENT = "equipment"
        MISC = "misc"
    value = dict()
    type_all_real = type_all = ["crafting_shaped", "crafting_shapeless", "crafting_transmute", "blasting", "campfire_cooking", "smelting", "smithing_transform", "smithing_trim", "smoking", "stonecutting"]
    type_all_real.extend(["crafting_decorated_pot", "crafting_special_armordye", "crafting_special_bannerduplicate", "crafting_special_bookcloning", "crafting_special_firework_rocket", "crafting_special_firework_star", "crafting_special_firework_star_fade", "crafting_special_mapcloning", "crafting_special_mapextending", "crafting_special_repairitem", "crafting_special_shielddecoration", "crafting_special_tippedarrow"])
    def __init__(self, type_data, id):
        self.recipe_type = self.__type()
        self.category = self.__category()
        self.path = "recipe/{0}.json".format(id)
        if type_data in self.type_all:
            self.type = type_data
        else:
            raise TypeError("invalid recipe type '{}'".format(type_data))
    def set_result(self, item_data: minecraft_template.item_type):
        if self.type == "smithing_trim":
            raise TypeError("recipe '{0}' isn't able to set result".format(self.type))
        else:
            self.value["result"] = item_data.export()
    def set_group(self, value: str):
        if self.type == "smithing_trim" or self.type == "smithing_transform":
            raise TypeError("recipe '{0}' isn't able to set group".format(self.type))
        else:
            self.value["group"] = value
    def set_category(self, value: str):
        if self.type == "smithing_trim" or self.type == "smithing_transform" or self.type == "stonecutting":
            raise TypeError("recipe '{0}' isn't able to set category".format(self.type))
        else:
            self.value["category"] = value
    def set_experience(self, value: float):
        if self.type == "smelting" or self.type == "blasting" or self.type == "smoking" or self.type == "campfire_cooking":
            self.value["experience"] = value
        else:
            raise TypeError("recipe '{0}' isn't able to set experience".format(self.type))
    def set_single_ingredient(self, value: str):
        if self.type == "smelting" or self.type == "blasting" or self.type == "smoking" or self.type == "campfire_cooking":
            self.value["ingredient"] = value
        else:
            raise TypeError("recipe '{0}' isn't able to set ingredient".format(self.type))
    def set_multiple_ingredient(self, value: list):
        if self.type == "smelting" or self.type == "blasting" or self.type == "smoking" or self.type == "campfire_cooking":
            self.value["ingredient"] = value
        else:
            raise TypeError("recipe '{0}' isn't able to set ingredient".format(self.type))
    def set_cooking_time(self, value: int):
        if self.type == "smelting" or self.type == "blasting" or self.type == "smoking" or self.type == "campfire_cooking":
            self.value["cookingtime"] = value
        else:
            raise TypeError("recipe '{0}' isn't able to set cooking time".format(self.type))
    def set_input(self, value: list):
        if self.type == "crafting_transmute":
            self.value["input"] = value
        else:
            raise TypeError("recipe '{0}' isn't able to set input".format(self.type))
    def set_material(self, value: list):
        if self.type == "crafting_transmute":
            self.value["material"] = value
        else:
            raise TypeError("recipe '{0}' isn't able to set material".format(self.type))
    def set_multiple_ingredient_crafting(self, value: list):
        if self.type == "crafting_shapeless":
            self.value["ingredients"] = value
        else:
            raise TypeError("recipe '{0}' isn't able to set ingredients".format(self.type))
    def set_show_notification(self, value: bool):
        if self.type == "crafting_shaped":
            self.value["show_notification"] = value
        else:
            raise TypeError("recipe '{0}' isn't able to set showing notification".format(self.type))
    def set_crafting_shaped_key(self, value: dict):
        if self.type == "crafting_shaped":
            self.value["key"] = value
        else:
            raise TypeError("recipe '{0}' isn't able to set key".format(self.type))
    def set_crafting_pattern(self, value: list):
        if self.type == "crafting_shaped":
            max_length = max(map(len, value))
            if len(value) > 3 or max_length > 3:
                raise ListLengthError("'{0}' can't be in 3x3 grid".format(value))
            else:
                self.value["pattern"] = value
        else:
            raise TypeError("recipe '{0}' isn't able to set pattern".format(self.type))
    def get_data(self):
        value = self.value
        value["type"] = self.type
        return value
    def get_json(self):
        return json.dumps(self.get_data())
    def get_arg_std(self):
        return {"path": self.path, "data": self.get_json(), "belong_to_data_pack": True}
class advancement():
    class __frame():
        CHALLENGE = "challenge"
        GOAL = "goal"
        TASK = "task"
    def __init__(self, id):
        self.frame_type = self.__frame()
        self.path = "advancement/{0}.json".format(id)
        self.data = {"criteria": dict()}
        # HARD but possible
    def criteria_add(self, key: str, value):
        self.data["criteria"][key] = value
    def criteria_del(self, key: str):
        del self.data["criteria"][key]
    def value_parent(self, value: str):
        self.data["parent"] = value
        if not self.data["parent"]:
            del self.data["parent"]
        elif "background" in self.data["display"]:
            del self.data["display"]["background"]
    def value_requirements(self, value: list):
        self.data["requirements"] = value
    def value_sends_telemetry_event(self, value: bool):
        self.data["sends_telemetry_event"] = value
    def rewards_experience(self, value: int):
        if "rewards" not in self.data:
            self.data["rewards"] = dict()
        self.data["rewards"]["experience"] = value
    def rewards_function(self, value: str):
        if "rewards" not in self.data:
            self.data["rewards"] = dict()
        self.data["rewards"]["function"] = value
    def value_loot(self, value: list):
        self.data["loot"] = value
    def value_recipes(self, value: list):
        self.data["recipes"] = value
    def display_announce_to_chat(self, value: bool):
        if "display" not in self.data:
            self.data["display"] = dict()
        self.data["display"]["announce_to_chat"] = value
    def display_background(self, value: bool):
        if "display" not in self.data:
            self.data["display"] = dict()
        if "parent" not in self.data:
            self.data["display"]["background"] = value
        else:
            raise RootAdvencementError("only a root advencement has a background")
    def display_description(self, value: str):
        if "display" not in self.data:
            self.data["display"] = dict()
        self.data["display"]["description"] = value
    def display_frame(self, value: str):
        if "display" not in self.data:
            self.data["display"] = dict()
        self.data["display"]["frame"] = value
    def display_hidden(self, value: bool):
        if "display" not in self.data:
            self.data["display"] = dict()
        self.data["display"]["hidden"] = value
    def display_icon(self, value: minecraft_template.item_type):
        if "display" not in self.data:
            self.data["display"] = dict()
        self.data["display"]["icon"] = value.export()
    def display_show_toast(self, value: bool):
        if "display" not in self.data:
            self.data["display"] = dict()
        self.data["display"]["show_toast"] = value
    def display_title(self, value: str):
        if "display" not in self.data:
            self.data["display"] = dict()
        self.data["display"]["title"] = value
    def display_title(self, value: str):
        if "display" not in self.data:
            self.data["display"] = dict()
        self.data["display"]["title"] = value
    def get_data(self):
        return self.data
    def get_json(self):
        return json.dumps(self.get_data())
    def get_arg_std(self):
        return {"path": self.path, "data": self.get_json(), "belong_to_data_pack": True}