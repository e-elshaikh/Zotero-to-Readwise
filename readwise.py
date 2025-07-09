    def format_items(self, zotero_items):
        formatted = []
        for item in zotero_items:
            data = item.get("data", {})

            # Extract fields
            text   = data.get("annotationText") or data.get("note") or ""
            title  = data.get("title", "")
            author = data.get("creatorSummary", "")

            # Skip items missing any of these
            if not (text.strip() and title.strip() and author.strip()):
                continue

            # Truncate text if needed
            text = text[:MAX_TEXT_LEN]

            # Build source URL
            key = data.get("key")
            if self.lib_type == "user":
                source_url = f"https://www.zotero.org/users/{self.lib_id}/items/{key}"
            else:
                source_url = f"https://www.zotero.org/groups/{self.lib_id}/items/{key}"

            formatted.append({
                "text":       text,
                "title":      title,
                "author":     author,
                "source_url": source_url
            })

        return formatted
