import requests

class Readwise:
    def __init__(self, token):
        self.token = token

    def format_items(self, items):
        formatted = []
        for item in items:
            data = item["data"]
            content = data.get("annotationText") or data.get("note")
            title = data.get("title") or "Zotero Item"
            if content:
                formatted.append({
                    "text": content,
                    "title": title,
                    "source_type": "zotero",
                    "location_type": "manual",
                    "location": "zotero",
                })
        return formatted

    def create_highlights(self, highlights):
        url = "https://readwise.io/api/v2/highlights/"
        headers = {
            "Authorization": f"Token {self.token}",
            "Content-Type": "application/json"
        }
        for h in highlights:
            r = requests.post(url, json={"highlights": [h]}, headers=headers)
            if r.status_code != 200:
                print("Failed to send highlight:", h)
                print(r.text)
