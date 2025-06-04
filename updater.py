# import necessary libraries
import time
import os
import sys
import logging
from pathlib import Path
from scanner import scan_directory
from db import update_docs, delete_doc_path, collection

## _____________________________________________________________________________________________________________
# logging setup
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("background_update.log"),
        logging.StreamHandler(sys.stdout)
    ]
)
## _____________________________________________________________________________________________________________
#
BASE_PATH = os.environ.get("DOC_BASE_PATH")
if not BASE_PATH:
    BASE_PATH = str(Path.home() / "Documents")
    logging.warning(f"DOC_BASE_PATH not set. falling back to default: {BASE_PATH}")
else:
    logging.info(f"using DOC_BASE_PATH from environment: {BASE_PATH}")

#
if not os.path.isdir(BASE_PATH):
    logging.error(f"base path '{BASE_PATH}' is not a directory or not accessible.")
    sys.exit(1)
else:
    logging.info(f"base path '{BASE_PATH}' exists and is accessible.")

## _____________________________________________________________________________________________________________
def run_update():
    logging.info("ENTERED run_update() function")
    logging.info("scheduled update started...")
    try:
        docs = scan_directory(BASE_PATH)

        existing = collection.get()
        existing_docs = existing.get("metadatas", [])
        existing_ids = existing.get("ids", [])

        existing_map = {}
        for i, doc_meta in enumerate(existing_docs):
            path = doc_meta.get("path")
            lm = doc_meta.get("last_modified", 0)
            existing_map[path] = lm

        # lists for docs to index / delete
        docs_to_index = []
        docs_to_delete = []

        scanned_paths = set()
        for doc in docs:
            path = doc["path"]
            lm = doc.get("last_modified", 0)
            scanned_paths.add(path)
            if path not in existing_map:

                docs_to_index.append(doc)
            else:
                # test if last_modified changed
                if lm > existing_map[path]:
                    docs_to_index.append(doc)

        #
        for path in existing_map.keys():
            if path not in scanned_paths:
                docs_to_delete.append(path)

        # delete
        for path in docs_to_delete:
            logging.info(f"deleting removed doc from db: {path}")
            delete_doc_path(path)

        # update
        if docs_to_index:
            logging.info(f"indexing {len(docs_to_index)} new/updated docs")
            update_docs(docs_to_index)
        else:
            logging.info("no docs to index")

        logging.info(f"scheduled update complete, {len(docs)} docs scanned")
    except Exception as e:
        logging.error(f"error during scheduled update: {e}")

## _____________________________________________________________________________________________________________
if __name__ == "__main__":
    logging.info("background updater running. press ctrl+c to stop")
    logging.info("running initial update...")
    run_update()
    logging.info(f"checking BASE_PATH: {BASE_PATH}")
    logging.info(f"files in BASE_PATH: {os.listdir(BASE_PATH)}")
    logging.info("starting scheduler loop...")

    # ------------------------------------------------------------------------
    while True:
        try:
            time.sleep(3600*24)
            run_update()
        except Exception as e:
            logging.error(f"error in main loop: {e}")
            time.sleep(3660)

