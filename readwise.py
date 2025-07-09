import requests
import json
import os

class Readwise:
    def __init__(self, readwise_token, suppress_failures=False):
        self.readwise_token = readwise_token
        self.suppress_failures = suppress_failures
        self.failed_items = []

    def create_highlights(self, highlights):
        url = "https://readwise.io/api/v2/highlights/"
        headers = {
            "Authorization": f"Token {self.readwise_token}",
            "Content-Type": "application/json"
        }

        try:
            resp = requests.post(url, headers=headers, json={"highlights": highlights})
            resp.raise_for_status()
        except requests.exceptions.RequestException as e:
            print(f"❌ Failed to POST highlights to Readwise: {e}")
            if not self.suppress_failures:
                raise
            self.failed_items.extend(highlights)
        else:
            if not resp.ok:
                print(f"❌ Readwise response error: {resp.status_code}")
                self.failed_items.extend(highlights)

    def post_zotero_annotations_to_readwise(self, highlights):
        batch_size = 200
        for i in range(0, len(highlights), batch_size):
            batch = highlights[i:i + batch_size]
            print(f"📦 Uploading batch {i // batch_size + 1} of {((len(highlights)-1)//batch_size)+1}...")
            self.create_highlights(batch)

    def save_failed_items_to_json(self, path="failed_readwise_highlights.json"):
        if self.failed_items:
            with open(path, "w", encoding="utf-8") as f:
                json.dump(self.failed_items, f, indent=2, ensure_ascii=False)
            print(f"📄 {len(self.failed_items)} failed highlights saved to {path}")
