from PIL import Image
import requests
from transformers import AutoProcessor, AutoModel
from filter import load_products
import numpy as np
from io import BytesIO

model = AutoModel.from_pretrained("patrickjohncyh/fashion-clip")
processor = AutoProcessor.from_pretrained("patrickjohncyh/fashion-clip")


# Functions
def get_embedding_for_image(image_url):
    """
    Downloads the image, computes embedding via FashionCLIP, returns 1D numpy array.
    Returns None if anything fails.
    """
    try:
        response = requests.get(image_url, timeout=10)
        response.raise_for_status()
        image = Image.open(BytesIO(response.content)).convert("RGB")
        inputs = processor(images=image, return_tensors="pt")
        outputs = model.get_image_features(**inputs)
        # Check if outputs is a model output object or tensor
        if hasattr(outputs, "pooler_output"):
            embedding = outputs.pooler_output
        else:
            embedding = outputs

        return embedding.detach().cpu().numpy().squeeze()

    except Exception as e:
        print(f"Failed to process {image_url}: {e}")
        return None

def cosine_similarity(vec_a, vec_b):
    return np.dot(vec_a, vec_b) / (np.linalg.norm(vec_a) * np.linalg.norm(vec_b))


products = load_products()
products_slice = products[:10]  

shoes = {}
bags = {}
clothing = {}
accessories = {}

count = 0
for product in products_slice:
    if product["product_type"] == "shoes":
        count += 1
        shoes[count] = product
    elif product["product_type"] == "bags":
        count += 1
        bags[count] = product
    elif product["product_type"] == "clothing":
        count += 1
        clothing[count] = product
    elif product["product_type"] == "accessories":
        count += 1
        accessories[count] = product

print(f"Loaded {len(shoes)} shoes, {len(bags)} bags, {len(clothing)} clothing items, {len(accessories)} accessories")



selected_shoe_id = 1

shoe_emb = get_embedding_for_image(shoes[selected_shoe_id]["image_url"])
if shoe_emb is None:
    raise ValueError("Failed to compute embedding for selected shoe")
shoes[selected_shoe_id]["image_embedding"] = shoe_emb

for category in [bags, clothing, accessories]:
    for product_id, product in category.items():
        emb = get_embedding_for_image(product["image_url"])
        if emb is not None:
            print(f"Computing embedding for {product['product_id']}...")
            product["image_embedding"] = emb
        else:
            print(f"Skipping {product['product_id']} due to failed embedding")



all_products = {**bags, **clothing, **accessories}

similarities = []
for prod_id, product in all_products.items():
    if "image_embedding" in product:
        sim = cosine_similarity(shoes[selected_shoe_id]["image_embedding"], product["image_embedding"])
        similarities.append((prod_id, sim, product["product_type"], product["product_id"]))

print(similarities)