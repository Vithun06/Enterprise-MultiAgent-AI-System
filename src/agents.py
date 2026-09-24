import os
import time
from dotenv import load_dotenv
from langchain_chroma import Chroma
from groq import Groq

# Load environment variables
load_dotenv()
groq_api_key = os.getenv("GROQ_API_KEY")

def query_vector_db(user_query):
    """Agent 1: Vector Database Retrieval & Metadata Extraction"""
    try:
        db = Chroma(persist_directory="vector_db")
        docs = db.similarity_search(user_query, k=2)
        
        if not docs:
            return "", 0

        context = "\n\n".join([f"[Source: {doc.metadata.get('source', 'Unknown')}]:\n{doc.page_content}" for doc in docs])
        return context, len(docs)
    except Exception as e:
        print(f"Vector DB Search Error: {e}")
        return "", 0

def get_active_groq_model(client):
    """Groq-ல் தற்போது இயங்கும் சிறந்த மாடலை தானாகவே தேர்ந்தெடுக்கும் ஃபங்க்ஷன்"""
    try:
        models = client.models.list()
        active_ids = [m.id for m in models.data]
        
        # முன்னுரிமைப் பட்டியல் (Priority List)
        preferred_models = [
            "openai/gpt-oss-120b",
            "openai/gpt-oss-20b",
            "qwen/qwen3.8-27b"
        ]
        
        for model in preferred_models:
            if model in active_ids:
                return model
                
        # ஒருவேளை மேலே உள்ளவை இல்லை எனில் கிடைக்கும் முதல் மாடலை எடுக்கும்
        return active_ids[0] if active_ids else "openai/gpt-oss-20b"
    except Exception:
        return "openai/gpt-oss-20b"

def ask_groq_llm_with_guardrails(context, user_query):
    """Agent 2 & 3: LLM Reasoning + Self-Correction Guardrail"""
    if not groq_api_key or groq_api_key == "your_groq_api_key_here":
        return "Error: GROQ_API_KEY .env கோப்பில் சரியாக அமைக்கப்படவில்லை!"

    try:
        client = Groq(api_key=groq_api_key)
        
        # தானாகவே இயங்கும் மாடலைக் கண்டறிதல்
        selected_model = get_active_groq_model(client)
        
        prompt = f"""
You are an Enterprise AI Quality Assurance Specialist and Support Engineer.
Your task is to analyze the retrieved context and answer the user's query accurately.

CRITICAL GUARDRAIL RULES:
1. Base your answer ONLY on the provided context below. 
2. If the answer is NOT present in the context, clearly state: "Information not available in official documentation."
3. Do NOT hallucinate or make up error codes or steps.
4. Include source citations where relevant.

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
    
    if not retrieved_data:
        end_time = time.time()
        return "No relevant documentation found in Vector DB.", round(end_time - start_time, 2), 0, "No Context Found"
    
    # Step 2: Guardrailed Generation
    ai_response = ask_groq_llm_with_guardrails(retrieved_data, user_query)
    
    end_time = time.time()
    execution_time = round(end_time - start_time, 2)
    
    return ai_response, execution_time, chunk_count, retrieved_data