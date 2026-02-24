import streamlit as st
import os
from dotenv import load_dotenv

from langchain_openai import OpenAIEmbeddings
from langchain_pinecone import PineconeVectorStore
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from pinecone import Pinecone

# -----------------------------
# Load ENV & Config
# -----------------------------
load_dotenv()
INDEX_NAME = "workelate-index"

# -----------------------------
# Streamlit UI Setup
# -----------------------------
st.set_page_config(page_title="WorkElate LPU", page_icon="⚡")
st.title("⚡ WorkElate: Living Project Inbox")

# -----------------------------
# Initialize AI Components
# -----------------------------
@st.cache_resource
def init_components():
    embeddings = OpenAIEmbeddings()
    vectorstore = PineconeVectorStore(
        index_name=INDEX_NAME,
        embedding=embeddings
    )
    llm = ChatGroq(
        model="llama-3.3-70b-versatile",
        temperature=0
    )
    pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
    index = pc.Index(INDEX_NAME)
    return embeddings, vectorstore, llm, index

embeddings, vectorstore, llm, index = init_components()

# -----------------------------
# Inputs
# -----------------------------
user_input = st.text_area(
    "Enter update, query, or email:",
    placeholder="e.g., 'The SSL cert is deployed' or paste full email here"
)

project_id = st.text_input(
    "Enter Project ID (optional)",
    placeholder="Leave empty to auto-detect via RAG"
)

# -----------------------------
# Processing Logic
# -----------------------------
if st.button("Process"):

    if not user_input:
        st.warning("Provide input.")
        st.stop()

    # 1️⃣ Intent Classification
    intent_prompt = f"""
    Classify the following user input into one word only:
    UPDATE -> if the user is modifying project state
    QUERY -> if the user is asking about project status
    EMAIL -> if this looks like an email requiring a reply draft

    User Input: {user_input}
    Answer only: UPDATE, QUERY, or EMAIL
    """

    intent_raw = llm.invoke(intent_prompt).content.strip().upper()
    is_update = "UPDATE" in intent_raw
    is_email = "EMAIL" in intent_raw

    # ==========================================================
    # 📝 CASE A: UPDATE
    # ==========================================================
    if is_update:

        if not project_id:
            st.error("Project ID required for updates.")
            st.stop()

        fetch_response = index.fetch(ids=[project_id])
        existing_vector = fetch_response.vectors.get(project_id)

        if not existing_vector:
            st.error("❌ Project not found.")
            st.stop()

        old_text = existing_vector.metadata.get("text", "")

        # Append inside Details
        lines = old_text.split("\n")
        updated_lines = []
        found_details = False

        for line in lines:
            if line.strip().startswith("Details:"):
                updated_line = line + f" | Update: {user_input}"
                updated_lines.append(updated_line)
                found_details = True
            else:
                updated_lines.append(line)

        if not found_details:
            updated_lines.append(f"Details: {user_input}")

        updated_text = "\n".join(updated_lines)

        new_embedding = embeddings.embed_query(updated_text)

        index.upsert([
            (
                project_id,
                new_embedding,
                {
                    "project_id": project_id,
                    "text": updated_text
                }
            )
        ])

        st.success(f"✅ Project {project_id} updated.")

        with st.expander("📄 Updated Record"):
            st.markdown(f"```\n{updated_text}\n```")

    # ==========================================================
    # 👤 CASE B: QUERY or EMAIL
    # ==========================================================
    else:

        # 🔹 If project_id provided → Direct Fetch
        if project_id:
            fetch_response = index.fetch(ids=[project_id])
            vector = fetch_response.vectors.get(project_id)

            if not vector:
                st.error("❌ Project not found.")
                st.stop()

            context = vector.metadata.get("text", "")

        # 🔹 If NO project_id → Use RAG to auto-detect
        else:
            results = vectorstore.similarity_search(user_input, k=2)

            if not results:
                st.error("❌ No relevant project found.")
                st.stop()

            context = "\n\n---\n\n".join([doc.page_content for doc in results])

        # 🧠 Build Prompt
        if is_email:
            system_msg = "You are a professional AI project assistant. Draft a professional email reply using the context."
        else:
            system_msg = "You are a professional project assistant. Use the context to answer."

        prompt = ChatPromptTemplate.from_messages([
            ("system", system_msg),
            ("human", "Context:\n{context}\n\nUser Input:\n{question}")
        ])

        chain = prompt | llm
        response = chain.invoke({
            "context": context,
            "question": user_input
        })

        st.markdown("### 🤖 AI Response")
        st.info(response.content)

        with st.expander("📂 Retrieved Context"):
            st.write(context)