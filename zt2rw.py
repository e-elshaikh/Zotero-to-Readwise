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
        self.readwise = Readwise(readwise_token, suppress_failures)
        self.zotero = zotero.Zotero(
            zotero_library_id,
            zotero_library_type,
            zotero_key
        )
        self.include_annotations = include_annotations
        self.include_notes = include_notes

    def run(self):
        print("🔎 Retrieving annotations...")
        annotations = self._retrieve_all("annotation") if self.include_annotations else []
        print("🔎 Retrieving notes...")
        notes = self._retrieve_all("note") if self.include_notes else []
        all_items = annotations + notes
        print(f"✅ Retrieved {len(all_items)} Zotero items")

        formatted = self.readwise.format_items(all_items)
        self.readwise.send_items(formatted)

    def _retrieve_all(self, item_type):
        items = []
        start = 0
        limit = 100
        while True:
            batch = self.zotero.items(
                itemType=item_type,
                start=start,
                limit=limit
            )
            if not batch:
                break
            items.extend(batch)
            start += limit
        return items
