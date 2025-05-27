from encodings import normalize_encoding
#from scanner import scan_directory
import chromadb
from sentence_transformers import SentenceTransformer
from sentence_transformers.util import normalize_embeddings
import os


## _____________________________________________________________________________________________________________
# connect to chroma persistent database in the given directory
chroma_client = chromadb.PersistentClient(path="./chroma_db")
# fetch existing collection or create new
collection = chroma_client.get_or_create_collection(name="documents")
# loads language model for the embeddings
model = SentenceTransformer("/Users/anne/PycharmProjects/local_ai/models/sentence-transformers/all-MiniLM-L6-v2")

## _____________________________________________________________________________________________________________
# function that adds new docs to the database
def index_documents(docs):
    for doc in docs:
        print(f"➕ Indexiere: {doc['path']}")
        # use path as id
        doc_id = doc["path"]
        # create embedding fot the text
        embedding = model.encode(doc['content'], normalize_embeddings=True)
        collection.add(
            # save actual text
            documents=[doc["content"]],
            # save additional information (here: path)
            metadatas=[{"path": doc["path"], "last_modified": doc["last_modified"]}],
            # unambiguous id
            ids=[doc_id],
            # vector embedding for search
            embeddings=[embedding]
        )
        print("dokumente in der collection:", len(collection.get()['documents']))
    print(f"📦 Insgesamt in Collection: {len(collection.get()['documents'])}")
    return

# ------------------------------------------------------------------------
# function to delete doc from database based on its path
def delete_doc_path(path):
    collection.delete(ids=[path])

# ------------------------------------------------------------------------
# returns list of all documented paths of the database
def list_paths():
    return [m["path"] for m in collection.get()["metadatas"]]

## ------------------------------------------------------------------------
# function to update the database
def update_docs(docs):
    # docs already being in the db
    existing_paths = set(list_paths())
    # current docs existing
    new_paths = set(doc["path"] for doc in docs)

    # newly added docs
    new_docs = [doc for doc in docs if doc["path"] not in existing_paths]
    # removed docs
    to_delete = list(existing_paths - new_paths)
    # update
    to_update = [doc for doc in docs if doc["path"] in existing_paths]
    print(f"🔍 Neue Dokumente: {len(new_docs)}")
    print(f"🧹 Zu löschende Dokumente: {len(to_delete)}")
    print(f"♻️ Zu aktualisierende Dokumente: {len(to_update)}")
    for path in to_delete:
        delete_doc_path(path)

    for doc in to_update:
        # delete old version
        delete_doc_path(doc["path"])
        # create new version
        index_documents([doc])
    # insert new docs
    index_documents(new_docs)
    print("✅ Update abgeschlossen.")
    return



if __name__ == '__main__':
    print("test")
    from scanner import scan_directory
    BASE_PATH = os.environ.get("DOC_BASE_PATH", "/Users/anne/Documents")
    #collection.delete()
    docs = scan_directory(BASE_PATH)
    #docs = index_documents(docs)
    print(len(docs))
