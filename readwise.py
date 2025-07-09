import requests
import json
from datetime import datetime

class Readwise:
    def __init__(self, readwise_token, suppress_failures=False):
        self.token = readwise_token
        self.api_url = "https://readwise.io/api/v2/highlights/"
        self.failed_items = []
        self.suppress_failures = suppress_failures

    def format_zotero_items(self, zotero_items):
        formatted = []

        for item in zotero_items:
            try:
                highlight = {
                    "text": item.get("text", ""),
                    "title": item.get("title", "Zotero Highlight"),
                    "source_type": "book",
                    "source_url": item.get("source_url", ""),
                    "location": item.get("location", ""),
                    "highlighted_at": item.get("highlighted_at", datetime.utcnow().isoformat()),
                    "note": item.get("note", ""),
                    "tags": item.get("tags", [])
                }
                formatted.append(highlight)
            except Exception as e:
                self.failed_items.append({
                    "error": str(e),
                    "item": item
                })
                if not self.suppress_failures:
                    raise

        return formatted

    def create_highlights(self, highlights):
        headers = {
            "Authorization": f"Token {self.token}",
            "Content-Type": "application/json"
        }

        batch_size = 100
        for i in range(0, len(highlights), batch_size):
            batch = highlights[i:i + batch_size]
            try:
                resp = requests.post(
                    self.api_url,
                    headers=headers,
                    data=json.dumps({"highlights": batch})
                )
                if resp.status_code != 200:
                    self.failed_items.extend(batch)
            except Exception as e:
                self.failed_items.extend(batch)
                if not self.suppress_failures:
                    raise

    def save_failed_items_to_json(self, path):
        if self.failed_items:
            with open(path, "w", encoding="utf-8") as f:
                json.dump(self.failed_items, f, indent=2, ensure_ascii=False)
            print(f"📄 {len(self.failed_items)} failed highlights saved to {path}")
