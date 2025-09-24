# local_ai_projectwork
The project titled ”Design and Implementation of a Personal Data Management System using
Embedding-based Retrieval Augmented Generation with a local Large Language Model” focuses
on the conception and development of a locally operating Retrieval-Augmented Generation (RAG)
system. Its objective is to generate context-specific responses to user queries by leveraging a large
language model (LLM). To extend the model’s knowledge base, personal files are preprocessed
and converted into vector embeddings using Sentence Transformers, which are then stored in
a ChromaDB vector database. Information retrieval is conducted via cosine similarity search,
where the vector embeddings of stored documents are compared against the query vector. The
system returns the k most relevant documents, which are subsequently linked and utilized to
generate answers. This approach enables both precise searches within personal documents and
automatic summarization of their content.
