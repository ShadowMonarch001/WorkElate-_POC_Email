# ⚡ WorkElate: Living Project Inbox  

WorkElate is an **AI-powered project management experiment** that transforms a static vector database into a **“living” project record**.  

Unlike traditional RAG (Retrieval-Augmented Generation) systems that only *read* data, WorkElate enables **real-time project updates via natural language**, re-indexing changes instantly to keep the system state fresh and queryable.

---

## 🚀 The Concept: “Living” RAG

Most AI assistants operate in **read-only mode**. WorkElate introduces a **closed feedback loop**, allowing the AI to both read and mutate structured project state.

### 🔎 1. Intent Classification  
The system determines whether the user is:
- Asking a question (Query)
- Providing a project update (Mutation)

### 🔄 2. State Modification  
If it's an update:
- Fetch existing project metadata from Pinecone  
- Inject new update into structured context  
- Re-embed the updated project record  
- Upsert back into Pinecone  

This creates a **mutable vector state**.

### 🧠 3. Contextual Retrieval  
For queries:
- Retrieve the most recent vector state  
- Pass enriched context into Llama 3.3  
- Generate a professional, up-to-date summary  

The result:  
A vector database that behaves like a **living project memory** instead of static storage.

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|------------|
| **Frontend** | Streamlit |
| **LLM** | Groq (Llama 3.3 70B) |
| **Vector Database** | Pinecone |
| **Orchestration** | LangChain |
| **Embeddings** | OpenAI `text-embedding-3-small` |

---

## 📂 Project Structure


.
├── app.py # Main Streamlit application (UI)
├── ingest.py # Script to push data.json to Pinecone
├── data.json # Initial seed data for project records
├── .env # API Keys (OpenAI, Pinecone, Groq)
├── requirements.txt # Project dependencies
└── README.md # Documentation


---

## ⚙️ Setup & Installation

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/your-username/workelate.git
cd workelate
```
2️⃣ Install Dependencies
pip install -r requirements.txt
3️⃣ Configure Environment Variables

Create a .env file in the root directory:

OPENAI_API_KEY=your_openai_key
GROQ_API_KEY=your_groq_key
PINECONE_API_KEY=your_pinecone_key
4️⃣ Ingest Initial Data

Ensure data.json is populated, then initialize your Pinecone index:

python ingest.py
5️⃣ Run the Application
streamlit run app.py
💡 Usage
📝 Updating a Project

Enter a Project ID (e.g., P-ALPHA-01) and provide a natural language update:

"The frontend is done"

Internal Flow:

Project record is retrieved

Update appended to the Details field

New embedding generated

Updated vector upserted into Pinecone

Your project state is now mutated and persisted.

🔍 Querying a Project

Ask contextual questions like:

"What is the current status?"

The system:

Retrieves the latest vector

Injects updated context into Llama 3.3

Returns a professional summary

🧩 Why This Matters

WorkElate demonstrates how to move beyond static RAG into:

Stateful AI systems

Mutable vector memory

Real-time semantic re-indexing

Natural language-driven project management

It’s a practical exploration of stateful AI applications using modern LLM infrastructure.


If you found this interesting, consider ⭐ starring the repo and experimenting with your own “Living RAG” workflows.
