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


question = input("Ask a question: ")

question_embedding = create_embedding(question)

results = collection.query(
    query_embeddings=[question_embedding],
    n_results=1
)

context = results["documents"][0][0]

prompt = f"""
You are an internal company assistant.

Answer the user's question using only the information provided in the context.

If the answer is not contained in the context, say that you do not have enough information.

Context:
{context}

Question:
{question}
"""

response = ollama.chat(
    model="qwen2.5:7b",
    messages=[
        {
            "role": "user",
            "content": prompt
        }
    ]
)

print("\nAnswer:")
print(response["message"]["content"])