import argparse
from zt2rw import Zotero2Readwise

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("readwise_token")
    parser.add_argument("zotero_key")
    parser.add_argument("zotero_library_id")
    parser.add_argument("--library_type", default="user")
    parser.add_argument("--include_annotations", type=bool, default=True)
    parser.add_argument("--include_notes", type=bool, default=False)
    parser.add_argument("--filter_tags", nargs="*", default=None)
    parser.add_argument("--include_filter_tags", action="store_true")
    parser.add_argument("--use_since", action="store_true")
    parser.add_argument("--suppress_failures", action="store_true")
    args = parser.parse_args()

    zotero2readwise = Zotero2Readwise(
        readwise_token=args.readwise_token,
        zotero_key=args.zotero_key,
        zotero_library_id=args.zotero_library_id,
        zotero_library_type=args.library_type,
        include_annotations=args.include_annotations,
        include_notes=args.include_notes,
        filter_tags=args.filter_tags,
        include_filter_tags=args.include_filter_tags,
        use_since=args.use_since,
        suppress_failures=args.suppress_failures
    )
    zotero2readwise.run()

if __name__ == "__main__":
    main()