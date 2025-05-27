from db import model, collection, list_paths

# semantic search: fetch most relevant docs for user inquiry
def _retrieve_relevant_docs(query, top_k=3):
    # convert inquiry to embedding
    query_embedding = model.encode(query, normalize_embeddings=True).tolist()
    results = collection.query(query_embeddings=[query_embedding], n_results=top_k)
    # return best docs if existing.. if not empty list

    documents = results.get("documents", [[]])
    if documents and documents[0]:
        return documents[0]
    else:
        return []
from pprint import pprint

def retrieve_relevant_docs(query, top_k=3):
    # DEBUG: Gib aktuelle Collection-Inhalte aus
    all_docs = collection.get()
    print("\n🧠 Datenbankinhalte:")
    for i, (doc, meta) in enumerate(zip(all_docs["documents"], all_docs["metadatas"])):
        print(f"{i+1}. {meta['path']} | {doc[:80]}...")

    # Query-Vektor erzeugen (ohne "query:"-Prefix)
    query_embedding = model.encode(query).tolist()

    print("\n🔍 Query:", query)
    print("📏 Query-Vektor Beispiel:", query_embedding[:5], "...")

    # Ähnliche Dokumente abrufen
    results = collection.query(query_embeddings=[query_embedding], n_results=top_k)

    print("\n📊 Treffer-Ergebnisse:")
    pprint(results)

    if results["documents"]:
        return results["documents"][0]
    else:
        return []


docs = retrieve_relevant_docs("werkstoffkunde skript", top_k=3)
for i, doc in enumerate(docs):
    print(f"[{i+1}] {doc[:200]}...")