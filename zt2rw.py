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
        suppress_failures=False,
        use_since=False,
    ):
        self.readwise = Readwise(readwise_token, suppress_failures)
        self.include_annotations = include_annotations
        self.include_notes = include_notes
        self.use_since = use_since
        self.since = 0
        self.zotero_client = zotero.Zotero(
            zotero_library_id, zotero_library_type, zotero_key
        )

    def run(self):
        print("Retrieving ALL annotations from Zotero Database")
        zotero_items = self.get_all_zotero_items()

        formatted_items = self.readwise.format_zotero_items(
            zotero_items,
            self.include_annotations,
            self.include_notes
        )

        self.readwise.post_zotero_annotations_to_readwise(formatted_items)
        self.readwise.save_failed_items_to_json("failed_readwise_highlights.json")

    def get_all_zotero_items(self):
        items = []

        if self.include_annotations:
            print("🔎 Retrieving annotations...")
            items.extend(self.retrieve_all("annotation"))

        if self.include_notes:
            print("🔎 Retrieving notes...")
            items.extend(self.retrieve_all("note"))

        print(f"✅ Retrieved {len(items)} Zotero items")
        return items

    def retrieve_all(self, item_type):
        items = []
        start = 0
        while True:
            batch = self.zotero_client.items(itemType=item_type, start=start, limit=100)
            if not batch:
                break
            items.extend(batch)
            start += 100
        return items
