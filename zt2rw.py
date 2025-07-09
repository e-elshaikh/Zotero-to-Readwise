from readwise import Readwise
from pyzotero import zotero
from datetime import datetime
from typing import List
import logging

class Zotero2Readwise:
    def __init__(
        self,
        readwise_token,
        zotero_key,
        zotero_library_id,
        zotero_library_type="user",
        include_annotations=True,
        include_notes=False,
        include_filter_tags=False,
        filter_tags=None,
        filter_color=None,
        use_since=False,
        suppress_failures=False,
    ):
        self.readwise = Readwise(readwise_token, suppress_failures)
        self.zotero_client = zotero.Zotero(
            zotero_library_id, zotero_library_type, zotero_key
        )
        self.include_annotations = include_annotations
        self.include_notes = include_notes
        self.include_filter_tags = include_filter_tags
        self.filter_tags = filter_tags or []
        self.filter_color = filter_color
        self.use_since = use_since
        self.since = 0
        if self.use_since:
            self.since = self.readwise.get_latest_highlight_time()

    def run(self):
        logging.info("Retrieving ALL annotations from Zotero Database")
        items = self.get_all_zotero_items()
        logging.info(f"Retrieved {len(items)} total items")
        formatted_items = self.format_items_for_readwise(items)
        self.readwise.post_zotero_annotations_to_readwise(formatted_items)

    def get_all_zotero_items(self):
        items = []
        if self.include_annotations:
            items.extend(self.retrieve_all("annotation", self.since))
        if self.include_notes:
            items.extend(self.retrieve_all("note", self.since))
        return items

    def retrieve_all(self, item_type, since=0):
        logging.info(f"Fetching {item_type}s since {since}")
        query = self.zotero_client.items(itemType=item_type, since=since)
        items = query
        while "link" in self.zotero_client._last_response.headers:
            next_link = self.zotero_client._next_link()
            if not next_link:
                break
            self.zotero_client._update_request(next_link)
            next_items = self.zotero_client._get_json()
            items.extend(next_items)
        return items

    def format_items_for_readwise(self, items: List[dict]):
        formatted = []
        for item in items:
            try:
                rw_item = self.readwise.convert_zotero_item(item)
                if rw_item:
                    formatted.append(rw_item)
            except Exception as e:
                logging.error(f"Failed to convert item: {e}")
        return formatted
