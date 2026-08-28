import chromadb
from ollama import Client

ollama = Client(host="http://localhost:11434")

chroma = chromadb.PersistentClient(path="./chroma_db")

collection = chroma.get_collection(
    name="company_knowledge"
)


def create_embedding(text):
    response = ollama.embeddings(
        model="nomic-embed-text",
        prompt=text
    )

    return response["embedding"]


question = "Can I work remotely from another country?"

question_embedding = create_embedding(question)

results = collection.query(
    query_embeddings=[question_embedding],
    n_results=1
)

print(results["documents"][0][0])