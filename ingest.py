import json
import os
from dotenv import load_dotenv
from pinecone import Pinecone, ServerlessSpec

from langchain_core.documents import Document
from langchain_openai import OpenAIEmbeddings
from langchain_pinecone import PineconeVectorStore


# -----------------------------
# Load ENV
# -----------------------------
load_dotenv()

INDEX_NAME = "workelate-index"

# -----------------------------
# Initialize Pinecone (v3 SDK)
# -----------------------------
pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))

if INDEX_NAME not in pc.list_indexes().names():
    pc.create_index(
        name=INDEX_NAME,
        dimension=1536,
        metric="cosine",
        spec=ServerlessSpec(cloud="aws", region="us-east-1")
    )

# -----------------------------
# Load Data
# -----------------------------
with open("data.json", "r") as f:
    data = json.load(f)

print("Loaded:", data)

# -----------------------------
# Initialize Embeddings (v1)
# -----------------------------
embeddings = OpenAIEmbeddings()

# -----------------------------
# Initialize Vector Store
# -----------------------------
vectorstore = PineconeVectorStore(
    index_name=INDEX_NAME,
    embedding=embeddings
)

# -----------------------------
# Prepare Documents
# -----------------------------
documents = []
ids = []

for item in data:
    content = f"""
Client: {item['client_name']}
Project ID: {item['project_id']}
Details: {item['project_details']}
Last Interaction: {item['last_interaction']}
"""

    doc = Document(
    page_content=content,
    metadata={
        "project_id": item["project_id"],
        "customer_id": item["customer_id"],
        "dev_id": item["dev_id"],
        "client_name": item["client_name"],
        "text": content
    }
)

    documents.append(doc)
    ids.append(item["project_id"])  # 🔑 Unique key

# -----------------------------
# UPSERT
# -----------------------------
vectorstore.add_documents(documents=documents, ids=ids)

print("✅ LangChain v1 ingestion complete.")