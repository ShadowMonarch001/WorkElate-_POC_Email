⚡ WorkElate: Living Project Inbox
WorkElate is an AI-powered project management experiment that turns a static vector database into a "living" project record. Unlike traditional RAG (Retrieval-Augmented Generation) which only reads data, WorkElate allows users to update project states through natural language, which are then re-indexed in real-time.

🚀 The Concept: "Living" RAG
Most AI assistants are read-only. WorkElate introduces a feedback loop where the AI can:

Classify Intent: Determine if a user is asking a question or providing an update.

State Modification: Fetch existing project metadata from Pinecone, inject the new update into the context, and re-embed the data.

Contextual Retrieval: Answer complex queries based on the most recent, "mutated" state of the project.

🛠️ Tech Stack
Frontend: Streamlit

LLM: Groq (Llama 3.3 70B)

Vector Database: Pinecone

Orchestration: LangChain

Embeddings: OpenAI text-embedding-3-small

📂 Project Structure
Plaintext
.
├── app.py              # Main Streamlit application (The UI)
├── ingest.py           # Script to push data.json to Pinecone
├── data.json           # Initial seed data for project records
├── .env                # API Keys (OpenAI, Pinecone, Groq)
├── requirements.txt    # Project dependencies
└── README.md           # Documentation
⚙️ Setup & Installation
Clone the Repository

Bash
git clone https://github.com/your-username/workelate.git
cd workelate
Install Dependencies

Bash
pip install -r requirements.txt
Configure Environment Variables
Create a .env file in the root directory:

Code snippet
OPENAI_API_KEY=your_openai_key
GROQ_API_KEY=your_groq_key
PINECONE_API_KEY=your_pinecone_key
Ingest Initial Data
Ensure your data.json is populated, then run the ingestion script to initialize your Pinecone index:

Bash
python ingest.py
Run the Application

Bash
streamlit run app.py
💡 Usage
📝 Updating a Project
Enter a Project ID (e.g., P-ALPHA-01) and type an update:

"The frontend is done"

The system will find the record, append the text to the "Details" section, and update the vector in Pinecone.

🔍 Querying a Project
Ask a question about the current state:

"What is the status?"

The system retrieves the updated context and provides a professional summary via Llama 3.3.
