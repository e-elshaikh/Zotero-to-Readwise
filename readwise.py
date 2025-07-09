import requests
import json


class Readwise:
    def __init__(self, readwise_token):
        self.token = readwise_token
        self.api_url = "https://readwise.io/api/v2/highlights/"
        self.failed_items = []

    def format_zotero_items(self, items):
        highlights = []
        for item in items:
            if "annotations" not in item:
                continue
            for annotation in item["annotations"]:
                highlight = {
                    "text": annotation.get("annotationText", ""),
                    "title": item.get("title", "Untitled"),
                    "author": item.get("author", ""),
                    "source_url": item.get("url", ""),
                }
                highlights.append(highlight)
        return highlights

    def create_highlights(self, highlights):
        headers = {
            "Authorization": f"Token {self.token}",
            "Content-Type": "application/json",
        }

        BATCH_SIZE = 100
        for i in range(0, len(highlights), BATCH_SIZE):
            batch = highlights[i:i + BATCH_SIZE]
            response = requests.post(self.api_url, headers=headers, json={"highlights": batch})
            if response.status_code != 200:
                print(f"❌ Failed batch {i // BATCH_SIZE + 1}: {response.status_code}")
                self.failed_items.extend(batch)
            else:
                print(f"✅ Uploaded batch {i // BATCH_SIZE + 1}")

    def save_failed_items_to_json(self, path="failed_readwise_highlights.json"):
        if self.failed_items:
            with open(path, "w", encoding="utf-8") as f:
                json.dump(self.failed_items, f, indent=2, ensure_ascii=False)
            print(f"📄 {len(self.failed_items)} failed highlights saved to {path}")
