import requests, os, json

BASE_URL = "https://res.cloudinary.com/shared-furniture/image/upload/f_png,q_auto,w_800/v1/products/AFI"

def get_valid_image_links(sku, max_images=50):
    links = []
    for i in range(1, max_images + 1):
        url = f"{BASE_URL}/{sku}/images/{i}"
        if requests.head(url).status_code == 200:
            links.append(url)
    return links

def download_images(links, folder, base_name="image"):
    os.makedirs(folder, exist_ok=True)
    local_paths = []
    for idx, url in enumerate(links, 1):
        local_path = os.path.join(folder, f"{base_name}_{idx}.png")
        response = requests.get(url)
        with open(local_path, 'wb') as f:
            f.write(response.content)
        local_paths.append(local_path.replace("\\", "/"))
    return local_paths

def create_product_json(name, sku, category, description, image_paths):
    return {
        "name": name,
        "sku": sku,
        "brand": "Ashley",
        "category": category,
        "description": description,
        "images": image_paths
    }

def append_to_master_json(entry, json_path="data/furniture.json"):
    os.makedirs(os.path.dirname(json_path), exist_ok=True)

    if os.path.exists(json_path):
        with open(json_path, "r") as f:
            try:
                data = json.load(f)
                if not isinstance(data, list):
                    print("⚠️ furniture.json is not a list — resetting.")
                    data = []
            except json.JSONDecodeError:
                print("⚠️ Invalid JSON — resetting.")
                data = []
    else:
        data = []

    data = [item for item in data if item.get("sku") != entry["sku"]]
    data.append(entry)

    with open(json_path, "w") as f:
        json.dump(data, f, indent=2)

def run_product_entry():
    sku = input("🔢 Enter SKU / Model Number: ").strip()
    name = input("🛋️ Enter Product Name: ").strip()
    category = input("📦 Enter Category (e.g., Bedroom, Living Room): ").strip()
    description = input("📝 Enter Description: ").strip()

    print(f"\n🔎 Checking images for SKU: {sku}")
    links = get_valid_image_links(sku)
    if not links:
        print("❌ No valid images found. Skipping this product.")
        return

    print(f"⬇️ Downloading {len(links)} images...")
    local_folder = f"images/furniture/{sku}"
    image_paths = download_images(links, local_folder)

    print("📄 Generating JSON entry...")
    entry = create_product_json(name, sku, category, description, image_paths)
    append_to_master_json(entry)

    print(f"✅ Done! Entry for '{name}' added.\n")

# === Main Loop ===
if __name__ == "__main__":
    while True:
        run_product_entry()
        cont = input("➕ Add another product? (y/n): ").strip().lower()
        if cont != 'y':
            print("👋 Exiting product importer.")
            break
