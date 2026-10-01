# 🤖 Enterprise Multi-Agent Knowledge System

> **Production-Grade RAG Architecture with Groq Dynamic LLMs, ChromaDB Vector Store & Self-Correction Guardrails.**

---

## 📄 Case Study & Architecture Documentation

A comprehensive 20-section technical report detailing problem analysis, system trade-offs, metrics, and safety guardrails is available:

- 📑 **[Download / View Case Study PDF](./Enterprise_MultiAgent_CaseStudy.pdf)**

---

## 🚀 Key Features & Architecture

• **Agent 1 (Retriever):** Vector-based semantic document search using ChromaDB.
• **Agent 2 (Quality Assurance):** Strict anti-hallucination guardrails and context validation.
• **Agent 3 (Responder):** Ultra-fast inference powered by Groq LPU Engine.
• **Observability:** Built-in latency timing metrics, chunk count tracking, and trace logs via Streamlit UI.

---

## 🛠️ Tech Stack

- **Language:** Python
- **Orchestration:** LangChain
- **Vector Store:** ChromaDB
- **LLM Engine:** Groq API (Dynamic Model Resolution)
- **UI Framework:** Streamlit

---

## 📊 Empirical Performance Matrix

| Test Scenario | Retrieval | Guardrail | Synthesis | Total Latency | Security Verdict |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Valid Technical Query** | 0.12s | 0.85s | 1.28s | **2.25s** | `PASSED` |
| **Adversarial Injection** | 0.11s | 0.94s | Bypassed | **1.05s** | `REJECTED` |
| **Out-of-Scope Query** | 0.10s | 0.88s | Bypassed | **0.98s** | `REJECTED` |

## 💻 How to Run Locally

1. **Clone the Repository:**

   ```bash
   git clone
   https://github.com/Vithun06/Enterprise-MultiAgent-AI-System.git
   cd Enterprise-MultiAgent-AI-System
   ```

2. **Set Up Environment Variables:**
   Create a
   .env file in the root folder and add your Groq API key:

   ```env
   GROQ_API_KEY=your_actual_groq_api_key_here
   ```

3. **Install Dependencies:**

   ```bash
   pip install -r requirements.txt

   ```

4. **Run the Application:**

   ```bash
   python -m streamlit run app.py

   ```
🚀 Live Demo & Author
🌐 Live Streamlit Application: Enterprise Multi-Agent System
👤 Author & Creator: Vithun T R (AI Systems Engineer | Multi-Agent RAG Architect)
🔗 Professional Profiles: LinkedIn | GitHub

