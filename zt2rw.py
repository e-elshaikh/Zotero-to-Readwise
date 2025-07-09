from zotero2readwise.readwise import Readwise
from pyzotero import zotero

class Zotero2Readwise:
    def __init__(self, readwise_token, zotero_key, zotero_library_id, zotero_library_type="user", include_annotations=True, include_notes=False):
        self.readwise = Readwise(readwise_token)
        self.zotero = zotero.Zotero(zotero_library_id, zotero_library_type, zotero_key)
        self.include_annotations = include_annotations
        self.include_notes = include_notes

    def run(self):
        items = []
        if self.include_annotations:
            items.extend(self.zotero.items(itemType="annotation"))
        if self.include_notes:
            items.extend(self.zotero.items(itemType="note"))
        formatted_items = self.readwise.format_items(items)
        self.readwise.create_highlights(formatted_items)
