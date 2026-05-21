import json
import os

def write_json(path, data):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w') as f:
        json.dump(data, f, indent=2)

items = ["sword", "pickaxe", "axe", "shovel", "hoe", "helmet", "chestplate", "leggings", "boots"]

# Resource Pack: items/prismarine_shard.json
write_json("resource_pack/assets/minecraft/items/prismarine_shard.json", {
  "model": {
    "type": "minecraft:select",
    "property": "minecraft:custom_model_data",
    "cases": [
      { "when": 1, "model": { "type": "minecraft:model", "model": "minecraft:item/reinforced_iron_ingot" } },
      { "when": 2, "model": { "type": "minecraft:model", "model": "minecraft:item/reinforced_iron_sword" } },
      { "when": 3, "model": { "type": "minecraft:model", "model": "minecraft:item/reinforced_iron_pickaxe" } },
      { "when": 4, "model": { "type": "minecraft:model", "model": "minecraft:item/reinforced_iron_axe" } },
      { "when": 5, "model": { "type": "minecraft:model", "model": "minecraft:item/reinforced_iron_shovel" } },
      { "when": 6, "model": { "type": "minecraft:model", "model": "minecraft:item/reinforced_iron_hoe" } },
      { "when": 7, "model": { "type": "minecraft:model", "model": "minecraft:item/reinforced_iron_helmet" } },
      { "when": 8, "model": { "type": "minecraft:model", "model": "minecraft:item/reinforced_iron_chestplate" } },
      { "when": 9, "model": { "type": "minecraft:model", "model": "minecraft:item/reinforced_iron_leggings" } },
      { "when": 10, "model": { "type": "minecraft:model", "model": "minecraft:item/reinforced_iron_boots" } }
    ],
    "fallback": { "type": "minecraft:model", "model": "minecraft:item/prismarine_shard" }
  }
})

for item in items:
    write_json(f"resource_pack/assets/minecraft/models/item/reinforced_iron_{item}.json", {
        "parent": "minecraft:item/generated",
        "textures": { "layer0": f"minecraft:item/reinforced_iron_{item}" }
    })
write_json("resource_pack/assets/minecraft/models/item/reinforced_iron_ingot.json", {
    "parent": "minecraft:item/generated",
    "textures": { "layer0": "minecraft:item/reinforced_iron_ingot" }
})

# Data Pack Recipes
# Ingot
write_json("data_pack/data/minecraft/recipe/reinforced_iron_ingot.json", {
  "type": "minecraft:crafting_shaped",
  "pattern": ["IDI"],
  "key": {
    "I": { "item": "minecraft:iron_ingot" },
    "D": { "item": "minecraft:diamond" }
  },
  "result": {
    "id": "minecraft:prismarine_shard",
    "components": {
      "minecraft:item_model": "minecraft:prismarine_shard",
      "minecraft:custom_model_data": 1,
      "minecraft:item_name": { "text": "Reinforced Iron Ingot", "italic": False }
    }
  }
})

reinforced_ingredient = { "item": "minecraft:prismarine_shard", "components": { "minecraft:custom_model_data": 1 } }
tool_patterns = {
    "sword": ["R", "R", "S"], "pickaxe": ["RRR", " S ", " S "], "axe": ["RR ", "RS ", " S "],
    "shovel": ["R", "S", "S"], "hoe": ["RR ", " S ", " S "],
    "helmet": ["RRR", "R R"], "chestplate": ["R R", "RRR", "RRR"], "leggings": ["RRR", "R R", "R R"], "boots": ["R R", "R R"]
}
cmd_map = { "sword": 2, "pickaxe": 3, "axe": 4, "shovel": 5, "hoe": 6, "helmet": 7, "chestplate": 8, "leggings": 9, "boots": 10 }

for name, pattern in tool_patterns.items():
    res_comp = {
        "minecraft:custom_model_data": cmd_map[name],
        "minecraft:item_name": { "text": "Reinforced Iron " + name.capitalize(), "italic": False },
        "minecraft:max_damage": 450,
        "minecraft:damage": 0
    }

    recipe = {
        "type": "minecraft:crafting_shaped",
        "pattern": pattern,
        "key": { "R": reinforced_ingredient, "S": { "item": "minecraft:stick" } },
        "result": { "id": "minecraft:prismarine_shard", "components": res_comp }
    }

    if name in ["helmet", "chestplate", "leggings", "boots"]:
        del recipe["key"]["S"]
        slot = name.replace("helmet", "head").replace("chestplate", "chest").replace("leggings", "legs").replace("boots", "feet")
        res_comp["minecraft:equippable"] = { "slot": slot, "equipment_model": "minecraft:reinforced_iron" }
        stats = {"helmet": 2.5, "chestplate": 7, "leggings": 5.5, "boots": 2.5}
        res_comp["minecraft:attribute_modifiers"] = {
            "modifiers": [{
                "type": "minecraft:player.armor", "amount": stats[name], "operation": "add_value",
                "id": "minecraft:armor", "slot": slot
            }]
        }
    else:
        dmg = {"sword": 6.5, "pickaxe": 5, "axe": 9, "shovel": 4.5, "hoe": 1}[name]
        res_comp["minecraft:attribute_modifiers"] = {
            "modifiers": [{
                "type": "minecraft:player.attack_damage", "amount": dmg, "operation": "add_value",
                "id": "minecraft:attack_damage", "slot": "mainhand"
            }]
        }

    write_json(f"data_pack/data/minecraft/recipe/reinforced_iron_{name}.json", recipe)

write_json("resource_pack/pack.mcmeta", { "pack": { "pack_format": 84, "description": "Black & White Diamond + Reinforced Iron" } })
write_json("data_pack/pack.mcmeta", { "pack": { "pack_format": 101, "description": "Reinforced Iron System" } })
