import json
import os

def write_json(path, data):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w') as f:
        json.dump(data, f, indent=2)

items = ["sword", "pickaxe", "axe", "shovel", "hoe", "helmet", "chestplate", "leggings", "boots"]

# Diamond items/ overrides
for item in items:
    write_json(f"resource_pack/assets/minecraft/items/diamond_{item}.json", {
        "model": { "type": "minecraft:model", "model": f"minecraft:item/diamond_{item}" }
    })
    write_json(f"resource_pack/assets/minecraft/models/item/diamond_{item}.json", {
        "parent": "minecraft:item/generated", "textures": { "layer0": f"minecraft:item/diamond_{item}" }
    })

# Iron items/ overrides to support Reinforced Iron
for item in items:
    write_json(f"resource_pack/assets/minecraft/items/iron_{item}.json", {
        "model": {
            "type": "minecraft:select", "property": "minecraft:custom_model_data",
            "cases": [{ "when": 1, "model": { "type": "minecraft:model", "model": f"minecraft:item/reinforced_iron_{item}" } }],
            "fallback": { "type": "minecraft:model", "model": f"minecraft:item/iron_{item}" }
        }
    })
    write_json(f"resource_pack/assets/minecraft/models/item/reinforced_iron_{item}.json", {
        "parent": "minecraft:item/generated", "textures": { "layer0": f"minecraft:item/reinforced_iron_{item}" }
    })

write_json("resource_pack/assets/minecraft/items/iron_ingot.json", {
    "model": {
        "type": "minecraft:select", "property": "minecraft:custom_model_data",
        "cases": [{ "when": 1, "model": { "type": "minecraft:model", "model": "minecraft:item/reinforced_iron_ingot" } }],
        "fallback": { "type": "minecraft:model", "model": "minecraft:item/iron_ingot" }
    }
})
write_json("resource_pack/assets/minecraft/models/item/reinforced_iron_ingot.json", {
    "parent": "minecraft:item/generated", "textures": { "layer0": "minecraft:item/reinforced_iron_ingot" }
})

# Equipment
write_json("resource_pack/assets/minecraft/equipment/diamond.json", {
  "layers": { "humanoid": [{"texture": "minecraft:humanoid/diamond"}], "humanoid_leggings": [{"texture": "minecraft:humanoid_leggings/diamond"}] }
})
write_json("resource_pack/assets/minecraft/equipment/reinforced_iron.json", {
  "layers": { "humanoid": [{"texture": "minecraft:humanoid/reinforced_iron"}], "humanoid_leggings": [{"texture": "minecraft:humanoid_leggings/reinforced_iron"}] }
})

write_json("resource_pack/pack.mcmeta", { "pack": { "pack_format": 46, "description": "B&W Diamond + Reinforced Iron" } })
