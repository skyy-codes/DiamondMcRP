import os
from PIL import Image

def tint_cyan(pix, factor=0.4):
    r, g, b, a = pix
    if a == 0: return pix
    nr = int(r * (1 - factor))
    ng = int(g * (1 - factor) + 255 * factor)
    nb = int(b * (1 - factor) + 255 * factor)
    return (nr, min(255, ng), min(255, nb), a)

def process_diamond(input_path, output_path, cyan_ratio=0.6):
    if not os.path.exists(input_path): return
    img = Image.open(input_path).convert("RGBA")
    pixels = img.load()
    width, height = img.size
    all_pixels = []
    for y in range(height):
        for x in range(width):
            r, g, b, a = pixels[x, y]
            if a > 0:
                brightness = (r + g + b) / 3
                all_pixels.append((brightness, x, y))
    all_pixels.sort(key=lambda x: x[0], reverse=True)
    num_cyan = int(len(all_pixels) * cyan_ratio)
    cyan_indices = set((p[1], p[2]) for p in all_pixels[:num_cyan])
    for y in range(height):
        for x in range(width):
            r, g, b, a = pixels[x, y]
            if a == 0: continue
            if (x, y) not in cyan_indices:
                avg = int(0.299 * r + 0.587 * g + 0.114 * b)
                pixels[x, y] = (avg, avg, avg, a)
    img.save(output_path)

def process_reinforced(input_path, output_path, factor=0.3):
    if not os.path.exists(input_path): return
    img = Image.open(input_path).convert("RGBA")
    pixels = img.load()
    width, height = img.size
    all_pixels = []
    for y in range(height):
        for x in range(width):
            r, g, b, a = pixels[x, y]
            if a > 0:
                brightness = (r + g + b) / 3
                all_pixels.append((brightness, x, y))
    all_pixels.sort(key=lambda x: x[0], reverse=True)
    num_cyan = int(len(all_pixels) * 0.3)
    cyan_indices = set((p[1], p[2]) for p in all_pixels[:num_cyan])
    for y in range(height):
        for x in range(width):
            r, g, b, a = pixels[x, y]
            if a == 0: continue
            if (x, y) in cyan_indices:
                pixels[x, y] = tint_cyan((r, g, b, a), factor=factor)
    img.save(output_path)

items = ["sword", "pickaxe", "axe", "shovel", "hoe", "helmet", "chestplate", "leggings", "boots"]
for item in items:
    ratio = 0.7 if item in ["pickaxe", "hoe"] else 0.6
    process_diamond(f"originals/item/diamond_{item}.png", f"resource_pack/assets/minecraft/textures/item/diamond_{item}.png", cyan_ratio=ratio)
process_diamond("originals/item/diamond.png", "resource_pack/assets/minecraft/textures/item/diamond.png", cyan_ratio=0.6)
process_diamond("originals/entity/equipment/diamond.png", "resource_pack/assets/minecraft/textures/entity/equipment/humanoid/diamond.png", cyan_ratio=0.15)
process_diamond("originals/entity/equipment/diamond_leggings.png", "resource_pack/assets/minecraft/textures/entity/equipment/humanoid_leggings/diamond.png", cyan_ratio=0.15)

for item in items:
    process_reinforced(f"originals/item/iron_{item}.png", f"resource_pack/assets/minecraft/textures/item/reinforced_iron_{item}.png")
process_reinforced("originals/item/iron_ingot.png", "resource_pack/assets/minecraft/textures/item/reinforced_iron_ingot.png")
process_reinforced("originals/entity/equipment/iron.png", "resource_pack/assets/minecraft/textures/entity/equipment/humanoid/reinforced_iron.png")
process_reinforced("originals/entity/equipment/iron_leggings.png", "resource_pack/assets/minecraft/textures/entity/equipment/humanoid_leggings/reinforced_iron.png")
