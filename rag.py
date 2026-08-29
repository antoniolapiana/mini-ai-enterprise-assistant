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


def get_company_info():
    return "Company headquarters: Dublin. Employees: 1200."


def route_question(question):
    response = ollama.chat(
        model="qwen2.5:7b",
        messages=[
            {
                "role": "user",
                "content": f"""
Classify the user question into exactly one category.

RAG:
Use RAG when the question asks about company policies, rules,
procedures, or information contained in company documents.

TOOL:
Use TOOL when the question asks for basic company information
such as headquarters, employee count, or company details.

Examples:

Question: Can I work remotely from another country?
Answer: RAG

Question: How long do I have to submit travel expenses?
Answer: RAG

Question: What is the company headquarters?
Answer: TOOL

Question: How many employees does the company have?
Answer: TOOL

Return only RAG or TOOL.

Question:
{question}
"""
            }
        ]
    )

    return response["message"]["content"].strip()


question = input("Ask a question: ")

route = route_question(question)

print(f"Route: {route}")


if route == "RAG":

    question_embedding = create_embedding(question)

    results = collection.query(
        query_embeddings=[question_embedding],
        n_results=1
    )

    context = results["documents"][0][0]

    prompt = f"""
You are an internal company assistant.

Answer the user's question using the context provided.

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


elif route == "TOOL":

    tool_result = get_company_info()

    print("\nTool result:")
    print(tool_result)


else:

    print("\nUnknown route.")