import json
import os

def write_json(path, data):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w') as f:
        json.dump(data, f, indent=2)

items = ["sword", "pickaxe", "axe", "shovel", "hoe", "helmet", "chestplate", "leggings", "boots"]

# Data Pack Recipes for 1.21.4
# We use 'item_model' component to tell the item exactly which model to use.
# This avoids needing to modify the base 'iron_sword.json' etc.

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
      "minecraft:item_model": "minecraft:reinforced_iron_ingot",
      "minecraft:item_name": { "text": "Reinforced Iron Ingot", "italic": False }
    }
  }
})

# Ingredient for tools/armor (matches iron_ingot with the specific item_model)
reinforced_ing_item = {
    "item": "minecraft:iron_ingot",
    "components": {
        "minecraft:item_model": "minecraft:reinforced_iron_ingot"
    }
}

tool_patterns = {
    "sword": ["R", "R", "S"], "pickaxe": ["RRR", " S ", " S "], "axe": ["RR ", "RS ", " S "],
    "shovel": ["R", "S", "S"], "hoe": ["RR ", " S ", " S "],
    "helmet": ["RRR", "R R"], "chestplate": ["R R", "RRR", "RRR"], "leggings": ["RRR", "R R", "R R"], "boots": ["R R", "R R"]
}

armor_stats = {"helmet": 2.5, "chestplate": 7, "leggings": 5.5, "boots": 2.5}
attack_stats = {"sword": 6.5, "pickaxe": 5, "axe": 9, "shovel": 4.5, "hoe": 1}

for name, pattern in tool_patterns.items():
    res_comp = {
        "minecraft:item_model": f"minecraft:reinforced_iron_{name}",
        "minecraft:item_name": { "text": "Reinforced Iron " + name.capitalize(), "italic": False },
        "minecraft:max_damage": 500,
        "minecraft:damage": 0
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
            "asset_id": "minecraft:reinforced_iron"
        }
        res_comp["minecraft:attribute_modifiers"] = {
            "modifiers": [{
                "type": "minecraft:player.armor", "amount": armor_stats[name], "operation": "add_value",
                "id": "minecraft:armor", "slot": slot
            }]
        }
    else:
        # For tools, we need to add tool component for mining speed if it's a tool
        # but for simplicity and inheriting iron properties, iron_* base is good.
        # We manually add attack damage because iron tools have it.
        res_comp["minecraft:attribute_modifiers"] = {
            "modifiers": [{
                "type": "minecraft:player.attack_damage", "amount": attack_stats[name], "operation": "add_value",
                "id": "minecraft:attack_damage", "slot": "mainhand"
            }]
        }

    write_json(f"data_pack/data/minecraft/recipe/reinforced_iron_{name}.json", recipe)

# Resource Pack Models (standard path)
for item in items:
    write_json(f"resource_pack/assets/minecraft/models/item/reinforced_iron_{item}.json", {
        "parent": "minecraft:item/generated",
        "textures": { "layer0": f"minecraft:item/reinforced_iron_{item}" }
    })
write_json("resource_pack/assets/minecraft/models/item/reinforced_iron_ingot.json", {
    "parent": "minecraft:item/generated",
    "textures": { "layer0": "minecraft:item/reinforced_iron_ingot" }
})

# MCMeta
write_json("resource_pack/pack.mcmeta", { "pack": { "pack_format": 46, "description": "B&W Diamond + Reinforced Iron" } })
write_json("data_pack/pack.mcmeta", { "pack": { "pack_format": 61, "description": "Reinforced Iron System" } })

# Remove the potentially glitchy items/ overrides
import shutil
if os.path.exists("resource_pack/assets/minecraft/items"):
    shutil.rmtree("resource_pack/assets/minecraft/items")
