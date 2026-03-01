import pack_data.json_file as json_file
import pack_data.pack as pack
import os, json

def mkdir(dir: str):
    if not os.path.exists(dir):
        os.mkdir(dir)
# 原视频 - BV1v1iFBEEVK
# 指定路径
path_code = "D:/Java/MinecraftPython/PackCreator/main.py" # 程序路径，根据实际情况更改
os.chdir(os.path.dirname(path_code))
# 纹理/材质
texture = [0] * 4
texture_cache_1 = open("res/marshmallow_in_hand.png", mode="rb")
texture_cache_2 = open("res/marshmallow.png", mode="rb")
texture[0] = texture_cache_1.read()
texture[1] = texture_cache_2.read()
texture_cache_1.close()
texture_cache_2.close()
texture_cache_3 = open("res/cooked_marshmallow_in_hand.png", mode="rb")
texture_cache_4 = open("res/cooked_marshmallow.png", mode="rb")
texture[2] = texture_cache_3.read()
texture[3] = texture_cache_4.read()
texture_cache_3.close()
texture_cache_4.close()
# 初始化
plus = False
name = ("MarshmallowPlus" if plus else "Marshmallow")
id_ = "imitation"
path_ = "result_pack"
imitation = pack.pack(os.path.abspath(path_), name, id_)
mcmeta = dict()
mcmeta["pack"] = {"description": "Imitation by Stonal\nFrom MC LtB.", "max_format": 95, "min_format": 75}
imitation.mcmeta.write_all(mcmeta)
# 跨行数据
item_model = {
    "model": {
        "type": "minecraft:select",
        "cases": [
            {
                "model": {
                    "type": "minecraft:model",
                    "model": "{}:item/marshmallow".format(id_)
                },
                "when": [
                    "gui",
                    "ground",
                    "fixed",
                    "on_shelf"
                ]
            }
        ],
        "fallback": {
            "type": "minecraft:model",
            "model": "{}:item/marshmallow_in_hand".format(id_)
        },
        "property": "minecraft:display_context"
    },
    "swap_animation_scale": 1.95
}
cooked_item_model = {
    "model": {
        "type": "minecraft:select",
        "cases": [
            {
                "model": {
                    "type": "minecraft:model",
                    "model": "{}:item/cooked_marshmallow".format(id_)
                },
                "when": [
                    "gui",
                    "ground",
                    "fixed",
                    "on_shelf"
                ]
            }
        ],
        "fallback": {
            "type": "minecraft:model",
            "model": "{}:item/cooked_marshmallow_in_hand".format(id_)
        },
        "property": "minecraft:display_context"
    },
    "swap_animation_scale": 1.95
}
marshmallow_using_condiction = {
    "trigger": "player_hurt_entity",
    "conditions": {
        "player": {
            "equipment": {
                "mainhand": {
                    "components": {
                        "minecraft:custom_data": {
                            "type": "marshmallow"
                        }
                    }
                }
            }
        }
    }
}
cooked_marshmallow_using_condiction = {
    "trigger": "player_hurt_entity",
    "conditions": {
        "player": {
            "equipment": {
                "mainhand": {
                    "components": {
                        "minecraft:custom_data": {
                            "type": "cooked_marshmallow"
                        }
                    }
                }
            }
        }
    }
}
debug_txt_info = {
    "type": "translatable",
    "translate": "commands.random.sample.success",
    "fallback": "Random Value: %s",
    "with": [
        {
            "type": "scoreboard",
            "score": {
                "name": "@s",
                "objective": "attacking_data"
            }
        }
    ]
}
attacking_marshmallow = """# 对攻击和被攻击的生物添加标签
tag @s add marshmallow_attacking_source
# say [DEBUG] Add Tag -> Player
tag @n[type=!minecraft:player] add marshmallow_attacking
# say [DEBUG] Add Tag -> Entity
# 处理被添加标签的生物
execute as @e[tag=marshmallow_attacking] store result score @s attacking_data run random value 0..4
# execute as @e[tag=cooked_marshmallow_attacking] run tellraw @a {1}
# say [DEBUG] Random Value Stored
execute as @e[tag=marshmallow_attacking] at @s if biome ~ ~ ~ #{0}:can_snow if score @s attacking_data matches 0 \\
    if predicate {{condition:weather_check,raining:true}} run data modify entity @s TicksFrozen set value 2000
execute as @e[tag=marshmallow_attacking] if score @s attacking_data matches 0 run effect give @s levitation 10 1 false
# 消耗棉花糖
execute as @e[tag=marshmallow_attacking] if score @s attacking_data matches 0 run clear \\
    @a[tag=marshmallow_attacking_source] minecraft:wooden_spear[minecraft:custom_data={{"type":"marshmallow"}}] 1
execute as @e[tag=marshmallow_attacking] if score @s attacking_data matches 0 run give \\
    @a[tag=marshmallow_attacking_source] stick 2
# 移除标签
tag @e[tag=marshmallow_attacking] remove marshmallow_attacking
tag @a[tag=marshmallow_attacking_source] remove marshmallow_attacking_source
# 移除进度
function {0}:anti_cheating""".format(id_, json.dumps(debug_txt_info))
attacking_cooked_marshmallow = """# 对攻击和被攻击的生物添加标签
tag @s add cooked_marshmallow_attacking_source
# say [DEBUG] Add Tag -> Player
tag @n[type=!minecraft:player] add cooked_marshmallow_attacking
# say [DEBUG] Add Tag -> Entity
# 处理被添加标签的生物
execute as @e[tag=cooked_marshmallow_attacking] store result score @s attacking_data run random value 0..4
# say [DEBUG] Random Value Stored
# execute as @e[tag=cooked_marshmallow_attacking] run tellraw @a {2}
execute as @e[tag=cooked_marshmallow_attacking] if score @s attacking_data matches 0 run effect give @s levitation \\
    10 2 false
execute as @e[tag=cooked_marshmallow_attacking] if score @s attacking_data matches 0 run effect give @s slowness 30 \\
    1 false
execute as @e[tag=cooked_marshmallow_attacking] if score @s attacking_data matches 0 run effect give @s saturation \\
    6 1 false
# 消耗棉花糖
execute as @e[tag=cooked_marshmallow_attacking] if score @s attacking_data matches 0 run clear {1} \\
    minecraft:wooden_spear[minecraft:custom_data={{"type":"cooked_marshmallow"}}] 1
execute as @e[tag=cooked_marshmallow_attacking] if score @s attacking_data matches 0 run give {1} stick 2
# 移除标签
tag @e[tag=cooked_marshmallow_attacking] remove cooked_marshmallow_attacking
tag @a[tag=marshmallow_attacking_source] remove marshmallow_attacking_source
# 移除进度
advancement revoke @a only {0}:cooked_marshmallow_using""".format(
    id_,
    "@a[tag=cooked_marshmallow_attacking_source]",
    json.dumps(debug_txt_info)
)
# 数据
marshmallow_recipe = json_file.recipe("crafting_shaped", "marshmallow")
marshmallow_recipe.set_category(marshmallow_recipe.category.EQUIPMENT)
marshmallow_recipe.set_crafting_shaped_key({"0": "minecraft:sugar", "1": "minecraft:stick"})
marshmallow_recipe.set_crafting_pattern(["  0", " 1 ", "1  "])
marshmallow = json_file.minecraft_template.item_type("minecraft:wooden_spear", 1)
attribute_modifiers = list()
attribute_modifiers.append({"amount": 0, "id":"base_attack_damage", "operation": "add_value", "type":"attack_damage"})
attribute_modifiers.append({"amount":-2.46,"id": "base_attack_speed","operation": "add_value","type": "attack_speed"})
attribute_modifiers.append({"amount": 3, "id": "knockback", "operation": "add_value","type": "attack_knockback"})
marshmallow.components_push("minecraft:attribute_modifiers", attribute_modifiers)
marshmallow.components_push("minecraft:item_name", {"type":"translatable","translate":"item.imitation.marshmallow"})
marshmallow.components_push("minecraft:item_model", "{}:marshmallow".format(id_))
marshmallow.components_push("minecraft:max_stack_size", 16)
marshmallow.components_push("minecraft:rarity", "rare")
marshmallow.components_push("minecraft:custom_data", {"type": "marshmallow"})
marshmallow.components_pop("minecraft:max_damage")
cooked_marshmallow_recipe = json_file.recipe("smelting", "cooked_marshmallow")
cooked_marshmallow = json_file.minecraft_template.item_type("minecraft:wooden_spear", 1)
cooked_attribute_modifiers = attribute_modifiers
cooked_attribute_modifiers[0]["amount"] = 1.5
cooked_attribute_modifiers[1]["amount"] = -2.46
cooked_attribute_modifiers[2]["amount"] = 1
cooked_marshmallow.components_push("minecraft:attribute_modifiers", cooked_attribute_modifiers)
cooked_marshmallow.components_push("minecraft:item_name", {"translate":"item.imitation.cooked_marshmallow"})
cooked_marshmallow.components_push("minecraft:item_model", "{}:cooked_marshmallow".format(id_))
cooked_marshmallow.components_push("minecraft:max_stack_size", 16)
cooked_marshmallow.components_push("minecraft:rarity", "rare")
cooked_marshmallow.components_push("minecraft:custom_data", {"type": "cooked_marshmallow"})
cooked_marshmallow.components_pop("minecraft:max_damage")
cooked_marshmallow_recipe.set_single_ingredient("minecraft:wooden_spear")
a = {"parent": "minecraft:item/generated", "textures": {"layer0": "{}:item/marshmallow".format(id_)}}
b = {"parent": "minecraft:item/spear_in_hand","textures": {"layer0": "{}:item/marshmallow_in_hand".format(id_)}}
c = {"parent": "minecraft:item/generated", "textures": {"layer0": "{}:item/cooked_marshmallow".format(id_)}}
d = {"parent": "minecraft:item/spear_in_hand","textures":{"layer0": "{}:item/cooked_marshmallow_in_hand".format(id_)}}
marshmallow_using = json_file.advancement("marshmallow_using")
marshmallow_using.criteria_add("player_used_marshmallow", marshmallow_using_condiction)
marshmallow_using.rewards_function("{}:attack".format(id_))
marshmallow_using = json_file.advancement("cooked_marshmallow_using")
marshmallow_using.criteria_add("player_used_cooked_marshmallow", cooked_marshmallow_using_condiction)
marshmallow_using.rewards_function("{}:cooked_attack".format(id_))
# marshmallow_using.criteria_add("impossible_awa", {"trigger": "impossible"})
mcfunction = list()
mcfunction.append({"path": "function/get_marshmallow.mcfunction", "belong_to_data_pack": True})
mcfunction[0]["data"] = "give @s " + marshmallow.give_export_item()
mcfunction.append({"path": "function/attack.mcfunction", "belong_to_data_pack": True})
mcfunction[1]["data"] = attacking_marshmallow
mcfunction.append({"path": "function/init.mcfunction", "belong_to_data_pack": True})
mcfunction[2]["data"] = "scoreboard objectives add attacking_data dummy"
mcfunction.append({"path": "function/anti_cheating.mcfunction", "belong_to_data_pack": True})
mcfunction[3]["data"] = "advancement revoke @a only {}:marshmallow_using".format(id_)
mcfunction.append({"path": "function/reporting.mcfunction", "belong_to_data_pack": True})
mcfunction[4]["data"] = "execute if entity {{}} as run function {}:attack".format(id_)
user_debug = "@a[advancements={{{}:marshmallow_using={{player_used_marshmallow=true}}}}]".format(id_)
mcfunction[4]["data"] = str(mcfunction[4]["data"]).format(user_debug)
mcfunction.append({"path": "function/cooked_attack.mcfunction", "belong_to_data_pack": True})
mcfunction[5]["data"] = attacking_cooked_marshmallow
tag_snowy = json_file.tag("worldgen/biome", "can_snow")
tag_snowy.replace = False
tag_snowy.add_item("frozen_ocean")
tag_snowy.add_item("frozen_river")
tag_snowy.add_item("snowy_plains")
tag_snowy.add_item("ice_spikes")
tag_snowy.add_item("grove")
tag_snowy.add_item("frozen_peaks")
tag_snowy.add_item("jagged_peaks")
tag_snowy.add_item("snowy_slopes")
tag_snowy.add_item("snowy_taiga")
tag_snowy.add_item("snowy_plains")
mcfunction_load = json_file.tag("function", "load")
mcfunction_load.replace = False
mcfunction_load.add_item("{}:init".format(id_))
mcfunction_tick = json_file.tag("function", "tick")
mcfunction_tick.replace = False
mcfunction_tick.add_item("{}:reporting".format(id_))
mcfunction_tick.add_item("{}:anti_cheating".format(id_))
mcfunction_load_argv = mcfunction_load.get_arg_std()
mcfunction_tick_argv = mcfunction_tick.get_arg_std()
mcfunction_load_argv.update({"vanilla": True})
mcfunction_tick_argv.update({"vanilla": True})
x = {"item.imitation.marshmallow": "Marshmallow", "item.imitation.cooked_marshmallow": "Cooked Marshllow"}
y = {"item.imitation.marshmallow": "棉花糖", "item.imitation.cooked_marshmallow": "烤棉花糖"}
marshmallow_recipe.set_result(marshmallow)
# 文件结构
mkdir("assets")
mkdir("assets/{}".format(id_))
mkdir("assets/{}/models".format(id_))
mkdir("assets/{}/models/item".format(id_))
mkdir("assets/{}/items".format(id_))
mkdir("assets/{}/lang".format(id_))
mkdir("assets/{}/textures".format(id_))
mkdir("assets/{}/textures/item".format(id_))
mkdir("data")
mkdir("data/{}".format(id_))
mkdir("data/{}/function".format(id_))
mkdir("data/{}/recipe".format(id_))
mkdir("data/{}/tags".format(id_))
mkdir("data/{}/tags/worldgen".format(id_))
mkdir("data/{}/tags/worldgen/biome".format(id_))
mkdir("data/{}/advancement".format(id_))
mkdir("data/minecraft".format(id_))
mkdir("data/minecraft/tags".format(id_))
mkdir("data/minecraft/tags/function".format(id_))
# 写入文件
imitation.write_json("models/item/marshmallow.json", a, False)
imitation.write_json("models/item/marshmallow_in_hand.json", b, False)
imitation.write_json("models/item/cooked_marshmallow.json", c, False)
imitation.write_json("models/item/cooked_marshmallow_in_hand.json", d, False)
imitation.write_json("lang/en_us.json", x, False)
imitation.write_json("lang/zh_cn.json", y, False)
imitation.write_json("items/marshmallow.json", item_model, False)
imitation.write_json("items/cooked_marshmallow.json", cooked_item_model, False)
imitation.write_bool("textures/item/marshmallow.png", texture[1], False)
imitation.write_bool("textures/item/marshmallow_in_hand.png", texture[0], False)
imitation.write_bool("textures/item/cooked_marshmallow.png", texture[3], False)
imitation.write_bool("textures/item/cooked_marshmallow_in_hand.png", texture[2], False)
imitation.write_arg(marshmallow_recipe.get_arg_std())
cooked_marshmallow_recipe.set_result(cooked_marshmallow)
imitation.write_arg(cooked_marshmallow_recipe.get_arg_std())        # 我至今仍然没有想通为什么换个位置写入的是后面那个物品
imitation.write_arg(tag_snowy.get_arg_std())                        # 可能是因为指向的是同一个内存地址
imitation.write_arg(marshmallow_using.get_arg_std())                # 别动这三行，否则运行肯定有bug
imitation.write_arg(mcfunction_load_argv)
for i in mcfunction:
    imitation.write_arg(i)