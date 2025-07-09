import requests
import time
from requests.exceptions import RequestException

MAX_TEXT_LEN = 8191
API_URL = "https://readwise.io/api/v2/highlights/"

class Readwise:
    def __init__(self, token, suppress_failures=False):
        self.token = token
        self.failed = []
        self.suppress = suppress_failures

    def format_items(self, zotero_items):
        formatted = []
        for item in zotero_items:
            data = item.get("data", {})
            text = data.get("annotationText") or data.get("note") or ""
            if not text:
                continue
            # truncate to max allowed
            text = text[:MAX_TEXT_LEN]
            formatted.append({
                "text": text,
                "title": data.get("title", ""),
                "author": data.get("creatorSummary", ""),
                "source_url": data.get("url", "")
            })
        return formatted

    def send_items(self, highlights):
        headers = {
            "Authorization": f"Token {self.token}",
            "Content-Type": "application/json"
        }

        for idx, hl in enumerate(highlights, 1):
            try:
                resp = requests.post(
                    API_URL,
                    headers=headers,
                    json={"highlights": [hl]},
                    timeout=30
                )
                resp.raise_for_status()
                print(f"✅ Uploaded highlight {idx}/{len(highlights)}")
            except RequestException as e:
                err = None
                try:
                    err = resp.json()
                except Exception:
                    err = str(e)
                print(f"❌ Failed {idx}: {err}")
                self.failed.append({"item": hl, "error": err})
                if not self.suppress:
                    raise
            time.sleep(1)  # simple throttle

        if self.failed:
            with open("failed_readwise.json", "w", encoding="utf-8") as f:
                import json
                json.dump(self.failed, f, indent=2, ensure_ascii=False)
            print(f"📄 {len(self.failed)} failed highlights logged to failed_readwise.json")
