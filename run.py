import argparse
from zt2rw import Zotero2Readwise

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("readwise_token", help="Your Readwise API token")
    parser.add_argument("zotero_key", help="Your Zotero API key")
    parser.add_argument("zotero_library_id", help="Your Zotero library ID")
    parser.add_argument(
        "--library_type",
        choices=["user", "group"],
        default="user",
        help="Zotero library type"
    )
    parser.add_argument(
        "--include_annotations",
        action="store_true",
        default=True,
        help="Include annotations"
    )
    parser.add_argument(
        "--include_notes",
        action="store_true",
        default=False,
        help="Include notes"
    )
    parser.add_argument(
        "--suppress_failures",
        action="store_true",
        help="Continue on individual highlight failures"
    )

    args = parser.parse_args()

    syncer = Zotero2Readwise(
        readwise_token=args.readwise_token,
        zotero_key=args.zotero_key,
        zotero_library_id=args.zotero_library_id,
        zotero_library_type=args.library_type,
        include_annotations=args.include_annotations,
        include_notes=args.include_notes,
        suppress_failures=args.suppress_failures
    )
    syncer.run()

if __name__ == "__main__":
    main()
