# Zotero2Readwise Sync

A GitHub Action to sync your Zotero annotations to Readwise.

## Setup

1. Fork or clone this repo.
2. Add these secrets to your repo:
   - `READWISE_TOKEN`
   - `ZOTERO_KEY`
   - `ZOTERO_ID`
   - `ZOTERO_LIBRARY_TYPE` (e.g., `user`)
3. Go to the "Actions" tab and run the workflow manually.

## Notes

- Only highlights (annotations) are sent by default.
- Uses PyZotero to access your library and Readwise's API.
