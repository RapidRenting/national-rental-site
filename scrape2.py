import requests
from bs4 import BeautifulSoup
import json, re

HEADERS = {"User-Agent": "Mozilla/5.0"}

def get_product_details(url):
    resp = requests.get(url, headers=HEADERS)
    resp.raise_for_status()

    soup = BeautifulSoup(resp.text, "html.parser")

    # Find the Product JSON‑LD block
    ld = None
    for js in soup.find_all("script", type="application/ld+json"):
        try:
            data = json.loads(js.string)
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
        print("❌ No JSON‑LD Product block found")
        return

    # Extract fields
    name = ld.get("name", "❌ Name not found")
    desc = ld.get("description", "❌ Description not found")
    raw_sku = ld.get("sku", "")

    # Cleanup SKU: grab only the trailing alphanumeric part
    m = re.search(r"([A-Z0-9]+)$", raw_sku)
    sku = m.group(1) if m else raw_sku or "❌ SKU not found"

    print(f"\n🛏️ Product Name: {name}")
    print(f"\n📝 Description:\n{desc}")
    print(f"\n🆔 Vendor SKU: {sku}")

if __name__ == "__main__":
    url = input("🔗 Enter Ashley product URL: ").strip()
    get_product_details(url)
