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


. ├── app.py # Main Streamlit application (UI)
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
# 4️⃣ Ingest Initial Data
Make sure `data.json` is populated with your project records, then run:

```bash
python ingest.py
```
This initializes your Pinecone index with the initial project data.

# 5️⃣ Run the Application

```bash
streamlit run app.py
```
Open your browser at the URL shown (usually [http://localhost:8501](http://localhost:8501)).

# 💡 Usage

# 📝 Updating a Project
- Enter a **Project ID** (example: `P-ALPHA-01`) 
- Write a natural language update, e.g.: _"The frontend is done"_

**Internal flow:**
1. Project record is retrieved from Pinecone 
2. Update is appended to the Details field 
3. New embedding is generated 
4. Updated vector is upserted into Pinecone 

→ **Project state is now mutated and persisted.**

# 🔍 Querying a Project
Ask natural questions like:
- "What is the current status?"
- "Whats the progress so far?"
- "Any blockers?"

**Internal flow:**
1. Retrieves the latest vector state 
2. Injects updated context into Llama 3.3 
3. Returns a professional, up-to-date summary
