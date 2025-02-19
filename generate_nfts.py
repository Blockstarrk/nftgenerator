from PIL import Image
import os
import random
import json
from datetime import datetime
import uuid

# Ensure directories exist globally
output_dir = "generated_nfts"
metadata_dir = "metadata"

for directory in [output_dir, metadata_dir]:
    if not os.path.exists(directory):
        os.makedirs(directory)

class Trait:
    def __init__(self, name, rarity, category):
        self.name = name
        self.rarity = rarity
        self.category = category

    def __repr__(self):
        return f"Trait(name={self.name}, rarity={self.rarity}, category={self.category})"

def load_traits_with_rarity(directory, category):
    traits = []
    rarity_file = os.path.join(directory, "rarity.txt")
    
    rarity_data = {}
    if os.path.exists(rarity_file):
        with open(rarity_file, 'r') as f:
            for line in f:
                name, rarity = line.strip().split(',')
                rarity_data[name] = float(rarity)
    
    for file in os.listdir(directory):
        if file.endswith(('.png', '.jpg', '.jpeg')):
            traits.append(Trait(file, rarity_data.get(file, 1.0), category))
    
    return traits

def select_trait_by_rarity(traits):
    if not traits:
        return None
    total_rarity = sum(t.rarity for t in traits)
    r = random.uniform(0, total_rarity)
    for trait in traits:
        r -= trait.rarity
        if r <= 0:
            return trait
    return traits[-1]

def compose_nft(traits, noise_file="noise.png", output_dir="generated_nfts", metadata_dir="metadata"):
    size = 256
    images = [Image.open(os.path.join("assets", trait.category, trait.name)).resize((size, size), Image.LANCZOS) for trait in traits if trait]

    if not images:
        return None, None

    combined = images[0].copy()
    for img in images[1:]:
        combined.paste(img, (0, 0), img)

    try:
        noise = Image.open(noise_file).resize((size, size), Image.LANCZOS)
        combined.paste(noise, (0, 0), noise)
    except IOError:
        pass

    nft_id = str(uuid.uuid4())[:8]
    output_file = f"nft_{nft_id}.png"
    output_path = os.path.join(output_dir, output_file)
    combined.save(output_path)

    metadata = {
        "name": f"NFT #{nft_id}",
        "description": "A unique 1/1 NFT generated with various traits",
        "image": os.path.relpath(output_path, metadata_dir),
        "attributes": [{"trait_type": trait.category.capitalize(), "value": trait.name.split('.')[0]} for trait in traits if trait],
        "timestamp": datetime.now().isoformat()
    }

    metadata_path = os.path.join(metadata_dir, f"nft_{nft_id}.json")
    with open(metadata_path, 'w') as outfile:
        json.dump(metadata, outfile, indent=4)

    return output_path, metadata

def generate_unique_nft(categories):
    all_traits = [load_traits_with_rarity(path, category) for category, path in categories.items()]
    selected_traits = [select_trait_by_rarity(category) for category in all_traits if category]
    if selected_traits:
        return compose_nft([t for t in selected_traits if t])
    return None, None

# Categories
categories = {
    "background": "C:/Users/user/Autogen/Assets/Background",
    "body": "C:/Users/user/Autogen/Assets/Body",
    "head": "C:/Users/user/Autogen/Assets/Head",
    "eyes": "C:/Users/user/Autogen/Assets/Eyes",
    "mouth": "C:/Users/user/Autogen/Assets/Mouth",
    "glasses": "C:/Users/user/Autogen/Assets/Glasses",
    "hat": "C:/Users/user/Autogen/Assets/Hat"
}