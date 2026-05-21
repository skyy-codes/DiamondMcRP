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
  "key": { "I": { "item": "minecraft:iron_ingot" }, "D": { "item": "minecraft:diamond" } },
  "result": {
    "id": "minecraft:iron_ingot",
    "components": {
      "minecraft:custom_model_data": 1,
      "minecraft:item_name": { "text": "Reinforced Iron Ingot", "italic": False }
    }
  }
})

# Tool patterns
patterns = {
    "sword": ["R", "R", "S"], "pickaxe": ["RRR", " S ", " S "], "axe": ["RR ", "RS ", " S "],
    "shovel": ["R", "S", "S"], "hoe": ["RR ", " S ", " S "],
    "helmet": ["RRR", "R R"], "chestplate": ["R R", "RRR", "RRR"], "leggings": ["RRR", "R R", "R R"], "boots": ["R R", "R R"]
}

armor_stats = {"helmet": 2.5, "chestplate": 7, "leggings": 5.5, "boots": 2.5}
attack_stats = {"sword": 6.5, "pickaxe": 5, "axe": 9, "shovel": 4.5, "hoe": 1}

for name, pattern in patterns.items():
    res_comp = {
        "minecraft:custom_model_data": 1,
        "minecraft:item_name": { "text": "Reinforced Iron " + name.capitalize(), "italic": False },
        "minecraft:max_damage": 500,
        "minecraft:damage": 0
    }
    if name in ["helmet", "chestplate", "leggings", "boots"]:
        slot = name.replace("helmet", "head").replace("chestplate", "chest").replace("leggings", "legs").replace("boots", "feet")
        res_comp["minecraft:equippable"] = { "slot": slot, "asset_id": "minecraft:reinforced_iron" }
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

    write_json(f"data_pack/data/minecraft/recipe/reinforced_iron_{name}.json", {
        "type": "minecraft:crafting_shaped",
        "pattern": pattern,
        "key": { "R": { "item": "minecraft:iron_ingot", "components": { "minecraft:custom_model_data": 1 } }, "S": { "item": "minecraft:stick" } },
        "result": { "id": f"minecraft:iron_{name}", "components": res_comp }
    })

# Cleanup: remove stick from armor recipes
for name in ["helmet", "chestplate", "leggings", "boots"]:
    path = f"data_pack/data/minecraft/recipe/reinforced_iron_{name}.json"
    with open(path, 'r') as f: data = json.load(f)
    del data["key"]["S"]
    write_json(path, data)

write_json("data_pack/pack.mcmeta", { "pack": { "pack_format": 61, "description": "Reinforced Iron System" } })
