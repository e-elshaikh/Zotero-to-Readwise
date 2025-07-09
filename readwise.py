import requests
import time
import json
from requests.exceptions import RequestException

MAX_TEXT_LEN = 8191
API_URL = "https://readwise.io/api/v2/highlights/"

class Readwise:
    def __init__(self, token, suppress_failures=False, library_id=None, library_type="user"):
        self.token = token
        self.failed = []
        self.suppress = suppress_failures
        self.lib_id = library_id
        self.lib_type = library_type

    def format_items(self, enriched_items):
        """
        enriched_items: list of tuples (annotation_data, parent_data)
        """
        formatted = []
        for data, parent in enriched_items:
            # 1) Annotation text or note
            text = data.get("annotationText") or data.get("note") or ""
            # 2) Title from parent metadata
            title = parent.get("title") or ""
            # 3) Author summary from Zotero
            author = parent.get("creatorSummary") or ""

            # Skip if any of the three is blank
            if not (text.strip() and title.strip() and author.strip()):
                continue

            # Truncate text if needed
            text = text[:MAX_TEXT_LEN]

            # Build Zotero URL for this highlight’s parent item
            parent_key = data.get("parentItem")
            if self.lib_type == "user":
                source_url = f"https://www.zotero.org/users/{self.lib_id}/items/{parent_key}"
            else:
                source_url = f"https://www.zotero.org/groups/{self.lib_id}/items/{parent_key}"

            formatted.append({
                "text":       text,
                "title":      title,
                "author":     author,
                "source_url": source_url
            })

        return formatted

    def send_items(self, highlights):
        headers = {
            "Authorization": f"Token {self.token}",
            "Content-Type": "application/json"
        }

        for idx, hl in enumerate(highlights, start=1):
            try:
                resp = requests.post(API_URL, headers=headers, json={"highlights": [hl]}, timeout=30)
                resp.raise_for_status()
                print(f"✅ Uploaded {idx}/{len(highlights)}")
            except RequestException as e:
                try:
                    err = resp.json()
                except Exception:
                    err = str(e)
                print(f"❌ Failed {idx}: {err}")
                self.failed.append({"item": hl, "error": err})
                if not self.suppress:
                    raise
            time.sleep(1)  # throttle between requests

        if self.failed:
            with open("failed_readwise.json", "w", encoding="utf-8") as f:
                json.dump(self.failed, f, indent=2, ensure_ascii=False)
            print(f"📄 {len(self.failed)} failures logged to failed_readwise.json")
