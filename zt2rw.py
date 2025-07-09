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
        filter_color=None,
        filter_tags=None,
        include_filter_tags=False,
        use_since=False,
        suppress_failures=False
    ):
        self.include_annotations = include_annotations
        self.include_notes = include_notes
        self.filter_color = filter_color
        self.filter_tags = filter_tags or []
        self.include_filter_tags = include_filter_tags
        self.use_since = use_since
        self.zotero_key = zotero_key
        self.zotero_library_id = zotero_library_id
        self.readwise = Readwise(readwise_token, suppress_failures)

        self.zotero_client = zotero.Zotero(
            library_id=zotero_library_id,
            library_type=zotero_library_type,
            api_key=zotero_key
        )

    def run(self):
        print("Retrieving ALL annotations from Zotero Database")
        items = self.get_all_zotero_items()

        if not items:
            print("No Zotero annotations or notes found.")
            return

        print(f"✅ Retrieved {len(items)} Zotero items")

        formatted_items = self.readwise.format_zotero_items(
            zotero_items=items,
            include_annotations=self.include_annotations,
            include_notes=self.include_notes,
            filter_color=self.filter_color,
            filter_tags=self.filter_tags,
            include_filter_tags=self.include_filter_tags
        )

        print(f"📦 Pushing {len(formatted_items)} formatted highlights to Readwise...")
        self.readwise.post_zotero_annotations_to_readwise(formatted_items)

        if self.use_since:
            self.readwise.save_latest_timestamp(items)

    def get_all_zotero_items(self):
        items = []

        if self.include_annotations:
            print("🔎 Retrieving annotations...")
            items.extend(self.retrieve_all("annotation"))

        if self.include_notes:
            print("🔎 Retrieving notes...")
            items.extend(self.retrieve_all("note"))

        return items

    def retrieve_all(self, item_type):
        start = 0
        limit = 100
        all_items = []

        while True:
            page = self.zotero_client.items(itemType=item_type, start=start, limit=limit)
            if not page:
                break
            all_items.extend(page)
            start += limit

        return all_items
