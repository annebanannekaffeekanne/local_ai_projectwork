from db import model, collection

# semantic search: fetch most relevant docs for user inquiry
def retrieve_relevant_docs(query, top_k=3):
    # convert inquiry to embedding
    query_embedding = model.encode(f"query: {query}").tolist()
    results = collection.query(query_embeddings=[query_embedding], n_results=top_k)
    # return best docs if existing.. if not empty list
    if results["documents"]:
        return results["documents"][0]
    else:
        return []

docs = retrieve_relevant_docs("suche dokumente in denen das wort 'annika' steht", top_k=3)
print(docs)