import chromadb
from ollama import Client

ollama = Client(host="http://localhost:11434")

chroma = chromadb.PersistentClient(path="./chroma_db")

collection = chroma.get_or_create_collection(
    name="company_knowledge"
)


def create_embedding(text):
    response = ollama.embeddings(
        model="nomic-embed-text",
        prompt=text
    )

    return response["embedding"]


documents = [
    {
        "id": "remote_work",
        "text": open("data/remote_work.md", encoding="utf-8").read()
    },
    {
        "id": "ai_policy",
        "text": open("data/ai_policy.md", encoding="utf-8").read()
    },
    {
        "id": "expenses",
        "text": open("data/expenses.md", encoding="utf-8").read()
    }
]

for document in documents:
    embedding = create_embedding(document["text"])

    collection.add(
        ids=[document["id"]],
        documents=[document["text"]],
        embeddings=[embedding]
    )

print("Knowledge base created!")