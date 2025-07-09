from zt2rw import Zotero2Readwise

def main():
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("readwise_token", help="Your Readwise API token")
    parser.add_argument("zotero_key", help="Your Zotero API key")
    parser.add_argument("zotero_library_id", help="Your Zotero library ID")
    parser.add_argument("--library_type", choices=["user", "group"], default="user", help="Zotero library type")
    parser.add_argument("--include_annotations", type=bool, default=True, help="Include annotations")
    parser.add_argument("--include_notes", type=bool, default=False, help="Include notes")
    parser.add_argument("--filter_color", choices=["#ffd400", "#ff6666", "#5fb236", "#2ea8e5", "#a28ae5", "#e56eee", "#f19837", "#aaaaaa"], help="Optional: filter by annotation color")
    parser.add_argument("--filter_tags", help="Optional: comma-separated tags to filter by")
    parser.add_argument("--include_filter_tags", action="store_true", help="Include highlights with specified tags (default excludes them)")
    parser.add_argument("--use_since", action="store_true", help="Sync only annotations updated since last run")
    parser.add_argument("--suppress_failures", action="store_true", help="Suppress exceptions for failed highlights")

    args = parser.parse_args()

    zotero2readwise = Zotero2Readwise(
        readwise_token=args.readwise_token,
        zotero_key=args.zotero_key,
        zotero_library_id=args.zotero_library_id,
        zotero_library_type=args.library_type,
        include_annotations=args.include_annotations,
        include_notes=args.include_notes,
        filter_color=args.filter_color,
        filter_tags=args.filter_tags.split(",") if args.filter_tags else None,
        include_filter_tags=args.include_filter_tags,
        use_since=args.use_since,
        suppress_failures=args.suppress_failures,
    )

    zotero2readwise.run()

if __name__ == "__main__":
    main()
