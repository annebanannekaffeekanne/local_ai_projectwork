import requests
import json
from retriever import retrieve_relevant_docs, retrieve_with_paths


def query_mistral(prompt):
    # url to local ollama-api for the model mistral
    url = "http://localhost:11434/api/chat"
    # json payload: contains model, user-message and advice to answer in stream-mode
    payload = {
        "model": "mistral:latest",
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "stream": True
    }
    # http-post-request to local api
    with requests.post(url, json=payload, stream=True) as response:
        # exception if http-error
        response.raise_for_status()
        # puts response together
        full_response = ""
        # iterate over all streamed lines of the response
        for line in response.iter_lines():
            if line:
                try:
                    # decode json-line
                    data = json.loads(line.decode("utf-8"))
                    # extract textcontent of response and add
                    full_response += data.get("message", {}).get("content", "")
                except Exception as e:
                    print("error parsing in line:", e)
        return full_response


def ask_mistral_with_context(user_query):
    # search relevant documents based on user-query
    relevant_docs = retrieve_with_paths(user_query)
    # if no relevant doc found, stop
    if not relevant_docs:
        return "no relevant docs found"
    # put context together: contents of docs found
    context = "\n\n".join([doc["content"] for doc in relevant_docs])
    # list doc paths for reference
    doc_links = "\n".join([f"- {doc['path']}" for doc in relevant_docs])
    # prompt for LLM
    prompt = f"""Du bist ein hilfreicher Assistent. Beantworte die folgende Frage basierend auf dem gegebenen Kontext.
    Wenn du keine Antwort finden kannst, sag dies ehrlich.

    Kontext:
    {context}

    Frage: {user_query}

    Antwort:"""
    # send request to mistral
    response = query_mistral(prompt)
    # return of the model with a list of the document-paths used
    return f"{response}\n\nrelevant documents:\n{doc_links}"


if __name__ == "__main__":
    user_question = input("your question: ")
    answer = ask_mistral_with_context(user_question)
    print("\nresponse:")
    print(answer)




