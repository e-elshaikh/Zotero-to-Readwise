import requests

class Readwise:
    def __init__(self, token):
        self.token = token
        self.base_url = "https://readwise.io/api/v2/highlights/"

    def format_items(self, items):
        formatted = []
        for item in items:
            title = item.get("data", {}).get("title", "Untitled")
            highlights = item.get("data", {}).get("note", "")
            if highlights:
                formatted.append({
                    "title": title,
                    "text": highlights,
                    "source_type": "book",
                    "location_type": "manual",
                })
        return formatted

    def send_items(self, items):
        headers = {"Authorization": f"Token {self.token}"}
        for item in items:
            response = requests.post(self.base_url, headers=headers, json={"highlights": [item]})
            if response.status_code != 200:
                print(f"❌ Failed to send highlight: {response.text}")
            else:
                print("✅ Highlight sent successfully.")