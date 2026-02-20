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
product_ids = {}


shoes = {}
bags = {}
clothing = {}
accessories = {}

count = 0
for product in products_slice:
        product_ids[product["product_id"]] = product

print(f"Loaded {len(product_ids)} products")

selected_product_id = input("\nEnter a product_id to find similar items: ")

selected_product = product_ids[selected_product_id]
selected_emb = get_embedding_for_image(selected_product["image_url"])

for category in [bags, clothing, accessories]:
    for product_id, product in category.items():
        emb = get_embedding_for_image(product["image_url"])
        if emb is not None:
            print(f"Computing embedding for {product['product_id']}...")
            product["image_embedding"] = emb
        else:
            print(f"Skipping {product['product_id']} due to failed embedding")

similarities = []

for p_id, product in product_ids.items():

    if p_id == selected_product_id:
        continue

    emb = get_embedding_for_image(product["image_url"])
    if emb is None:
        continue

    sim = cosine_similarity(selected_emb, emb)

    similarities.append((p_id, sim, product["product_type"], product["name"]))

print(similarities)