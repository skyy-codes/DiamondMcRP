import json
import os

def write_json(path, data):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w') as f:
        json.dump(data, f, indent=2)

items = ["sword", "pickaxe", "axe", "shovel", "hoe", "helmet", "chestplate", "leggings", "boots"]

# Resource Pack: items/iron_*.json
# Use the first float in Custom Model Data for the select property
for item in items:
    write_json(f"resource_pack/assets/minecraft/items/iron_{item}.json", {
      "model": {
        "type": "minecraft:select",
        "property": "minecraft:custom_model_data",
        "cases": [
          {
            "when": 1.0,
            "model": { "type": "minecraft:model", "model": f"minecraft:item/reinforced_iron_{item}" }
          }
        ],
        "fallback": { "type": "minecraft:model", "model": f"minecraft:item/iron_{item}" }
      }
    })

write_json("resource_pack/assets/minecraft/items/iron_ingot.json", {
  "model": {
    "type": "minecraft:select",
    "property": "minecraft:custom_model_data",
    "cases": [
      {
        "when": 1.0,
        "model": { "type": "minecraft:model", "model": "minecraft:item/reinforced_iron_ingot" }
      }
    ],
    "fallback": { "type": "minecraft:model", "model": "minecraft:item/iron_ingot" }
  }
})

write_json("resource_pack/pack.mcmeta", { "pack": { "pack_format": 46, "description": "B&W Diamond + Reinforced Iron" } })
write_json("data_pack/pack.mcmeta", { "pack": { "pack_format": 61, "description": "Reinforced Iron System" } })
