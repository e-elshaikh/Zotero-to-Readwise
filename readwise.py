import requests
import json

class Readwise:
    def __init__(self, readwise_token, suppress_failures=False):
        self.token = readwise_token
        self.api_url = "https://readwise.io/api/v2/highlights/"
        self.failed_items = []
        self.suppress_failures = suppress_failures

    def format_zotero_items(self, items, include_annotations=True, include_notes=False):
        formatted = []
        for item in items:
            if item["type"] == "annotation" and include_annotations:
                formatted.append({
                    "text": item.get("annotation", ""),
                    "title": item.get("title", ""),
                    "author": item.get("author", ""),
                    "source_url": item.get("source_url", ""),
                    "location": item.get("location", ""),
                })
            elif item["type"] == "note" and include_notes:
                formatted.append({
                    "text": item.get("note", ""),
                    "title": item.get("title", ""),
                    "author": item.get("author", ""),
                    "source_url": item.get("source_url", ""),
                    "location": item.get("location", ""),
                })
        return formatted

    def create_highlights(self, highlights):
        headers = {
            "Authorization": f"Token {self.token}",
            "Content-Type": "application/json"
        }
        for highlight in highlights:
            try:
                resp = requests.post(self.api_url, headers=headers, data=json.dumps({"highlights": [highlight]}))
                resp.raise_for_status()
            except requests.exceptions.RequestException as e:
                if not self.suppress_failures:
                    raise
                self.failed_items.append(highlight)

    def save_failed_items_to_json(self, path):
        if self.failed_items:
            with open(path, "w", encoding="utf-8") as f:
                json.dump(self.failed_items, f, indent=2, ensure_ascii=False)
            print(f"📄 {len(self.failed_items)} failed highlights saved to {path}")
