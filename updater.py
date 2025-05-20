import time
import logging
import sys
import os
from scanner import scan_directory
from db import update_docs, delete_doc_path, list_paths, collection

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("background_update.log"),
        logging.StreamHandler(sys.stdout)
    ]
)

BASE_PATH = "/data"
if not os.path.exists(BASE_PATH):
    try:
        os.makedirs(BASE_PATH)
        logging.info(f"created documents directory at {BASE_PATH}")
    except Exception as e:
        logging.error(f"failed to create documents directory: {e}")

def run_update():
    logging.info("scheduled update started...")
    try:
        # docs sind jetzt dicts mit path, content und last_modified
        docs = scan_directory(BASE_PATH)

        # existierende Pfade aus der DB holen, inkl. gespeicherter last_modified
        # Annahme: Du hast Metadaten-Support für last_modified in collection!
        existing = collection.get()
        existing_docs = existing.get("metadatas", [])
        existing_ids = existing.get("ids", [])

        existing_map = {}
        for i, doc_meta in enumerate(existing_docs):
            path = doc_meta.get("path")
            lm = doc_meta.get("last_modified", 0)
            existing_map[path] = lm

        # Listen für docs zum indizieren / löschen
        docs_to_index = []
        docs_to_delete = []

        scanned_paths = set()
        for doc in docs:
            path = doc["path"]
            lm = doc.get("last_modified", 0)
            scanned_paths.add(path)
            if path not in existing_map:
                # neu
                docs_to_index.append(doc)
            else:
                # prüfen ob last_modified sich geändert hat
                if lm > existing_map[path]:
                    docs_to_index.append(doc)

        # docs, die in DB sind, aber nicht mehr im Dateisystem
        for path in existing_map.keys():
            if path not in scanned_paths:
                docs_to_delete.append(path)

        # löschen
        for path in docs_to_delete:
            logging.info(f"deleting removed doc from DB: {path}")
            delete_doc_path(path)

        # updaten / neu hinzufügen
        if docs_to_index:
            logging.info(f"indexing {len(docs_to_index)} new/updated docs")
            update_docs(docs_to_index)
        else:
            logging.info("no docs to index")

        logging.info(f"scheduled update complete, {len(docs)} docs scanned")
    except Exception as e:
        logging.error(f"error during scheduled update: {e}")

if __name__ == "__main__":
    logging.info("background updater running. press ctrl+c to stop")
    logging.info("running initial update...")
    run_update()
    logging.info("starting scheduler loop...")

    while True:
        try:
            # Einfach alle 24h
            time.sleep(3600*24)
            run_update()
        except Exception as e:
            logging.error(f"error in main loop: {e}")
            time.sleep(3660)

