import json
import os

def write_json(path, data):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w') as f:
        json.dump(data, f, indent=2)

items = ["sword", "pickaxe", "axe", "shovel", "hoe", "helmet", "chestplate", "leggings", "boots"]

# Reinforced Ingot Recipe
write_json("data_pack/data/minecraft/recipe/reinforced_iron_ingot.json", {
  "type": "minecraft:crafting_shaped",
  "pattern": ["IDI"],
  "key": {
    "I": { "item": "minecraft:iron_ingot" },
    "D": { "item": "minecraft:diamond" }
  },
  "result": {
    "id": "minecraft:iron_ingot",
    "components": {
      "minecraft:custom_model_data": 1,
      "minecraft:item_name": { "text": "Reinforced Iron Ingot", "italic": False }
    }
  }
})

reinforced_ing_item = { "item": "minecraft:iron_ingot", "components": { "minecraft:custom_model_data": 1 } }
tool_patterns = {
    "sword": ["R", "R", "S"], "pickaxe": ["RRR", " S ", " S "], "axe": ["RR ", "RS ", " S "],
    "shovel": ["R", "S", "S"], "hoe": ["RR ", " S ", " S "],
    "helmet": ["RRR", "R R"], "chestplate": ["R R", "RRR", "RRR"], "leggings": ["RRR", "R R", "R R"], "boots": ["R R", "R R"]
}

# Values for Reinforced Iron (between Iron and Diamond)
# Iron Max Damage: 250. Diamond Max Damage: 1561. Let's pick ~500.
# Iron Armor: 2, 5, 6, 2. Diamond Armor: 3, 6, 8, 3. Let's pick 2.5, 5.5, 7, 2.5.
armor_stats = {"helmet": 2.5, "chestplate": 7, "leggings": 5.5, "boots": 2.5}
attack_stats = {"sword": 6.5, "pickaxe": 5, "axe": 9, "shovel": 4.5, "hoe": 1}

for name, pattern in tool_patterns.items():
    res_comp = {
        "minecraft:custom_model_data": 1,
        "minecraft:item_name": { "text": "Reinforced Iron " + name.capitalize(), "italic": False },
        "minecraft:max_damage": 500
    }

    recipe = {
        "type": "minecraft:crafting_shaped",
        "pattern": pattern,
        "key": { "R": reinforced_ing_item, "S": { "item": "minecraft:stick" } },
        "result": { "id": f"minecraft:iron_{name}", "components": res_comp }
    }

    if name in ["helmet", "chestplate", "leggings", "boots"]:
        del recipe["key"]["S"]
        slot = name.replace("helmet", "head").replace("chestplate", "chest").replace("leggings", "legs").replace("boots", "feet")
        res_comp["minecraft:equippable"] = {
            "slot": slot,
            "equipment_model": "minecraft:reinforced_iron",
            "asset_id": "minecraft:reinforced_iron"
        }
        res_comp["minecraft:attribute_modifiers"] = {
            "modifiers": [{
                "type": "minecraft:player.armor", "amount": armor_stats[name], "operation": "add_value",
                "id": "minecraft:armor", "slot": slot
            }]
        }
    else:
        res_comp["minecraft:attribute_modifiers"] = {
            "modifiers": [{
                "type": "minecraft:player.attack_damage", "amount": attack_stats[name], "operation": "add_value",
                "id": "minecraft:attack_damage", "slot": "mainhand"
            }]
        }

    write_json(f"data_pack/data/minecraft/recipe/reinforced_iron_{name}.json", recipe)
