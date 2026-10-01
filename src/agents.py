import os
import time
from dotenv import load_dotenv
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from groq import Groq

# Load environment variables
load_dotenv()
groq_api_key = os.getenv("GROQ_API_KEY")

def query_vector_db(user_query):
    """Agent 1: Vector Database Retrieval & Metadata Extraction"""
    try:
        # Version Mismatch தவிர்க்க Embedding Function இணைக்கப்பட்டுள்ளது
        embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        db = Chroma(persist_directory="vector_db", embedding_function=embeddings)
        docs = db.similarity_search(user_query, k=2)
        
        if not docs:
            return "", 0

        context = "\n\n".join([f"[Source: {doc.metadata.get('source', 'tech_manual.txt')}]:\n{doc.page_content}" for doc in docs])
        return context, len(docs)
    except Exception as e:
        print(f"Vector DB Search Error: {e}")
        return "", 0

def get_active_groq_model(client):
    """Groq-ல் தற்போது இயங்கும் சிறந்த மாடலை தானாகவே தேர்ந்தெடுக்கும் ஃபங்க்ஷன்"""
    try:
        models = client.models.list()
        active_ids = [m.id for m in models.data]
        
        # Priority List for Groq models
        preferred_models = [
            "llama-3.3-70b-versatile",
            "llama-3.1-8b-instant",
            "mixtral-8x7b-32768",
            "openai/gpt-oss-20b"
        ]
        
        for model in preferred_models:
            if model in active_ids:
                return model
                
        return active_ids[0] if active_ids else "llama-3.3-70b-versatile"
    except Exception:
        return "llama-3.3-70b-versatile"

def ask_groq_llm_with_guardrails(context, user_query):
    """Agent 2 & 3: LLM Reasoning + Intelligent Dynamic Fallback Guardrail"""
    if not groq_api_key or groq_api_key == "your_groq_api_key_here":
        return "Error: GROQ_API_KEY .env கோப்பில் சரியாக அமைக்கப்படவில்லை!"

    try:
        client = Groq(api_key=groq_api_key)
        selected_model = get_active_groq_model(client)
        
        # 🌟 HYBRID INTELLIGENT FALLBACK PROMPT (ENTERPRISE STANDARD)
        prompt = f"""
You are an Enterprise AI Quality Assurance Specialist and Support Engineer.
Your task is to analyze the retrieved context and answer the user's query accurately.

CRITICAL HYBRID GUARDRAIL RULES:
1. Analyze the retrieved context carefully.
2. IF THE ANSWER IS PRESENT IN THE CONTEXT: Derive your answer strictly from it and cite the source as [Source: tech_manual.txt].
3. IF THE ANSWER IS NOT IN THE CONTEXT: DO NOT fail or say 'Information not available in official documentation'. Instead, begin your response clearly with:
   "📌 Note: Specific resolution not found in indexed official documentation. Providing answer based on General Enterprise System Architecture Knowledge:"
   Then provide a logical, highly accurate technical step-by-step resolution based on standard AI/Enterprise practices.

Context:
{context}

User Query:
{user_query}

Provide a structured, step-by-step resolution plan with an Enterprise Technical Quality Assurance check.
"""

        response = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model=selected_model,
            temperature=0.2
        )
        
        return response.choices[0].message.content
    except Exception as e:
        return f"Error connecting to Groq API: {str(e)}"

def run_enterprise_pipeline(user_query):
    start_time = time.time()
    
    # Step 1: Retrieval
    retrieved_data, chunk_count = query_vector_db(user_query)
    
    # Step 2: Intelligent Generation (Pass query even if retrieved_data is empty for general fallback)
    ai_response = ask_groq_llm_with_guardrails(retrieved_data if retrieved_data else "No Context Found", user_query)
    
    end_time = time.time()
    execution_time = round(end_time - start_time, 2)
    
    return ai_response, execution_time, chunk_count, retrieved_data if retrieved_data else "No Official Context Found"