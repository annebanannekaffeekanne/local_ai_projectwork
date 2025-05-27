# import necessary libraries and methods from files
from db import model, collection
from pprint import pprint
import subprocess

## _____________________________________________________________________________________________________________
def retrieve_relevant_docs(query, top_k=3):
    all_docs = collection.get()
    print("\ndatabase content:")
    for i, (doc, meta) in enumerate(zip(all_docs["documents"], all_docs["metadatas"])):
        print(f"{i+1}. {meta['path']} | {doc[:80]}...")

    query_embedding = model.encode(query, normalize_embeddings=True).tolist()

    print("\nquery:", query)
    print("query-vector example:", query_embedding[:5], "...")

    results = collection.query(query_embeddings=[query_embedding], n_results=top_k)

    print("\nresults:")
    pprint(results)

    if results["documents"]:
        return results["documents"][0]
    else:
        return []

## _____________________________________________________________________________________________________________
def retrieve_with_paths(query, top_k=5):
    query_embedding = model.encode(query, normalize_embeddings=True)
    results = collection.query(query_embeddings=[query_embedding], n_results=top_k)

    docs = results["documents"][0]
    paths = results["metadatas"][0]
    scores = results["distances"][0]

    combined = []
    for doc, meta, score in zip(docs, paths, scores):
        combined.append({
            "content": doc,
            "path": meta.get("path", "unknown"),
            "score": score
        })
    return combined



#docs = retrieve_relevant_docs("werkstoffkunde skript", top_k=3)
#for i, doc in enumerate(docs):
#    print(f"[{i+1}] {doc[:200]}...")
if __name__ == '__main__':
    for i, res in enumerate(retrieve_with_paths("thailand flight"), 1):
        print(f"{i}. {res['path']}")
        print(f"score: {res['score']:.4f}")
        print(f"preview: {res['content'][:120]}...\n")
        subprocess.run(["open", res['path']])