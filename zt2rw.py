from pyzotero import zotero
from readwise import Readwise

class Zotero2Readwise:
    def __init__(self, readwise_token, zotero_key, zotero_library_id, zotero_library_type="user",
                 include_annotations=True, include_notes=False, filter_tags=None,
                 include_filter_tags=False, use_since=False, suppress_failures=False):
        self.readwise = Readwise(readwise_token)
        self.zotero = zotero.Zotero(zotero_library_id, zotero_library_type, zotero_key)
        self.include_annotations = include_annotations
        self.include_notes = include_notes
        self.filter_tags = filter_tags
        self.include_filter_tags = include_filter_tags
        self.use_since = use_since
        self.since = 0 if not use_since else self.zotero.last_modified_version()
        self.suppress_failures = suppress_failures

    def run(self):
        print("🔎 Retrieving annotations...")
        annotations = self.retrieve_all("annotation") if self.include_annotations else []
        print("🔎 Retrieving notes...")
        notes = self.retrieve_all("note") if self.include_notes else []
        print(f"✅ Retrieved {len(annotations) + len(notes)} Zotero items")
        items = annotations + notes
        formatted_items = self.readwise.format_items(items)
        self.readwise.send_items(formatted_items)

    def retrieve_all(self, item_type):
        items = []
        start = 0
        while True:
            batch = self.zotero.items(itemType=item_type, start=start, limit=100)
            if not batch:
                break
            items.extend(batch)
            start += 100
        return items