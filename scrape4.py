import requests, os, json, re
from bs4 import BeautifulSoup

# for Excel upload mode
import pandas as pd

# === Configuration ===
HEADERS   = {"User-Agent": "Mozilla/5.0"}
BASE_URL  = "https://res.cloudinary.com/shared-furniture/image/upload/f_png,q_auto,w_800/v1/products/AFI"
JSON_PATH = "data/furniture.json"

# === Helpers from before ===

def get_product_details(url):
    resp = requests.get(url, headers=HEADERS)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")

    ld = None
    for tag in soup.find_all("script", type="application/ld+json"):
        try:
            data = json.loads(tag.string)
            entries = data if isinstance(data, list) else [data]
            for entry in entries:
                if entry.get("@type") == "Product":
                    ld = entry
                    break
        except:
            continue
        if ld:
            break

    if not ld:
        raise RuntimeError("❌ JSON‑LD Product block not found")

    name    = ld.get("name", "").strip()
    desc    = ld.get("description", "").strip()
    raw_sku = ld.get("sku", "").strip()

    # Strip any leading 4-letter prefix + dash
    sku = re.sub(r'^[A-Za-z]{4}-', '', raw_sku)

    return name, desc, sku

def get_valid_image_links(sku, max_images=50):
    links = []
    for i in range(1, max_images + 1):
        url = f"{BASE_URL}/{sku}/images/{i}"
        if requests.head(url, headers=HEADERS).status_code == 200:
            links.append(url)
    return links

def download_images(links, folder, base_name="image"):
    os.makedirs(folder, exist_ok=True)
    local_paths = []
    for idx, url in enumerate(links, 1):
        local_path = os.path.join(folder, f"{base_name}_{idx}.png")
        r = requests.get(url, headers=HEADERS)
        r.raise_for_status()
        with open(local_path, 'wb') as f:
            f.write(r.content)
        local_paths.append(local_path.replace("\\", "/"))
    return local_paths

def create_product_json(name, sku, category, description, image_paths):
    return {
        "name":        name,
        "sku":         sku,
        "brand":       "Ashley",
        "category":    category,
        "description": description,
        "images":      image_paths
    }

def append_to_master_json(entry, json_path=JSON_PATH):
    os.makedirs(os.path.dirname(json_path), exist_ok=True)
    if os.path.exists(json_path):
        with open(json_path, "r", encoding="utf-8") as f:
            try:
                data = json.load(f)
                if not isinstance(data, list):
                    data = []
            except:
                data = []
    else:
        data = []

    # remove old entry for same SKU
    data = [item for item in data if item.get("sku") != entry["sku"]]
    data.append(entry)

    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

# === Modes ===

def add_individually():
    url      = input("🔗 Enter Ashley product URL: ").strip()
    category = input("📂 Enter product category: ").strip()
    print("\n🔍 Scraping product details…")
    name, desc, sku = get_product_details(url)
    print(f"🛏️ Name: {name}\n🆔 SKU: {sku}\n")

    print("📸 Finding images…")
    links = get_valid_image_links(sku)
    if not links:
        print("❌ No valid images found. Skipping.")
        return

    print(f"⬇️ Downloading {len(links)} images…")
    folder = f"images/furniture/{sku}"
    image_paths = download_images(links, folder)

    print("💾 Saving entry to JSON…")
    entry = create_product_json(name, sku, category, desc, image_paths)
    append_to_master_json(entry)

    print("✅ Done! Added:", name)

def upload_from_excel():
    path = input("📑 Enter path to Excel file: ").strip()
    df = pd.read_excel(path)
    # Expect columns "URL" and "Category"
    for idx, row in df.iterrows():
        url = str(row.get("URL", "")).strip()
        category = str(row.get("Category", "")).strip()
        if not url or not category:
            print(f"⚠️ Row {idx+2}: Missing URL or Category, skipping.")
            continue
        print(f"\n▶️ Processing row {idx+2}: {url} / {category}")
        try:
            name, desc, sku = get_product_details(url)
            print(f"   🛏️ {name} (SKU: {sku})")
            links = get_valid_image_links(sku)
            if not links:
                print("   ❌ No images found, skipping.")
                continue
            folder = f"images/furniture/{sku}"
            download_images(links, folder)
            entry = create_product_json(name, sku, category, desc, [f"{folder}/image_{i+1}.png" for i in range(len(links))])
            append_to_master_json(entry)
            print("   ✅ Added successfully.")
        except Exception as e:
            print(f"   ❌ Failed at row {idx+2}: {e}")

if __name__ == "__main__":
    mode = input("Choose mode: (a)dd individually or (u)pload Excel [a/u]: ").strip().lower()
    if mode == 'a':
        add_individually()
    elif mode == 'u':
        upload_from_excel()
    else:
        print("Invalid choice. Exiting.")
