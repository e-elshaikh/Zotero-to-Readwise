from zotero2readwise.zt2rw import Zotero2Readwise
import sys

if __name__ == "__main__":
    readwise_token = sys.argv[1]
    zotero_key = sys.argv[2]
    zotero_library_id = sys.argv[3]
    zotero_library_type = sys.argv[4] if len(sys.argv) > 4 else "user"

    zt2rw = Zotero2Readwise(
        readwise_token=readwise_token,
        zotero_key=zotero_key,
        zotero_library_id=zotero_library_id,
        zotero_library_type=zotero_library_type,
        include_annotations=True,
        include_notes=False,
    )
    zt2rw.run()
