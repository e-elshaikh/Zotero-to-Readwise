from pyzotero import zotero
from readwise import Readwise

class Zotero2Readwise:
    def __init__(
        self,
        readwise_token,
        zotero_key,
        zotero_library_id,
        zotero_library_type="user",
        include_annotations=True,
        include_notes=False,
        suppress_failures=False
    ):
        self.zotero = zotero.Zotero(
            library_id=zotero_library_id,
            library_type=zotero_library_type,
            api_key=zotero_key
        )
        self.readwise = Readwise(
            token=readwise_token,
            suppress_failures=suppress_failures,
            library_id=zotero_library_id,
            library_type=zotero_library_type
        )
        self.include_annotations = include_annotations
        self.include_notes = include_notes

    def run(self):
        items = []
        if self.include_annotations:
            print("🔎 Retrieving annotations...")
            items.extend(self._retrieve_all("annotation"))
        if self.include_notes:
            print("🔎 Retrieving notes...")
            items.extend(self._retrieve_all("note"))

        print(f"✅ Retrieved {len(items)} Zotero items")

        # Enrich each entry with its parent item's data
        enriched = []
        for itm in items:
            data = itm.get("data", {})
            parent_key = data.get("parentItem")
            parent_data = {}
            if parent_key:
                try:
                    parent = self.zotero.item(parent_key)
                    parent_data = parent.get("data", {})
                except Exception:
                    parent_data = {}
            enriched.append((data, parent_data))

        formatted = self.readwise.format_items(enriched)
        print(f"→ {len(formatted)} items to upload")
        self.readwise.send_items(formatted)

    def _retrieve_all(self, item_type):
        all_items = []
        start = 0
        limit = 100
        while True:
            batch = self.zotero.items(itemType=item_type, start=start, limit=limit)
            if not batch:
                break
            all_items.extend(batch)
            start += limit
        return all_items
