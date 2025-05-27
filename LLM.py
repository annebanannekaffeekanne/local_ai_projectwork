import requests
import json
from retriever import retrieve_relevant_docs, retrieve_with_paths


def query_mistral(prompt):
    url = "http://localhost:11434/api/chat"
    payload = {
        "model": "mistral:latest",
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "stream": True  # wichtig: aktiviere Streaming
    }

    with requests.post(url, json=payload, stream=True) as response:
        response.raise_for_status()
        full_response = ""
        for line in response.iter_lines():
            if line:
                try:
                    data = json.loads(line.decode("utf-8"))
                    full_response += data.get("message", {}).get("content", "")
                except Exception as e:
                    print("⚠️ Fehler beim Parsen einer Zeile:", e)
        return full_response


def ask_mistral_with_context(user_query):
    relevant_docs = retrieve_with_paths(user_query)
    if not relevant_docs:
        return "no relevant docs found"
    context = "\n\n".join([doc["content"] for doc in relevant_docs])
    doc_links = "\n".join([f"- {doc['path']}" for doc in relevant_docs])

    prompt = f"""Du bist ein hilfreicher Assistent. Beantworte die folgende Frage basierend auf dem gegebenen Kontext.
    Wenn du keine Antwort finden kannst, sag dies ehrlich.

    Kontext:
    {context}

    Frage: {user_query}

    Antwort:"""

    response = query_mistral(prompt)
    return f"{response}\n\n🔗 Relevante Dokumente:\n{doc_links}"


# Optional: Interaktive CLI-Nutzung
if __name__ == "__main__":
    user_question = input("❓ Deine Frage: ")
    answer = ask_mistral_with_context(user_question)
    print("\n🧠 Antwort:")
    print(answer)




