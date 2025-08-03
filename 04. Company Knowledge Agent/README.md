# 🤖 LLM Deliveries Internal Chat

> Lightweight LLM-based chat with vector RAG and supervised feedback, designed to democratize internal company knowledge — with a focus on efficiency, security, and future scalability.

---

## 🎯 Objective

This project addresses the need to facilitate autonomous access to institutional knowledge without overloading the technical team. It delivers an interactive interface where any employee can ask questions about the company's operating model, services, team, or guidelines — with contextualized answers based on internal documents.

---

## 🧠 Strategic Decisions

### ⚡ Using the `phi3` model via Ollama

> The `phi3` model was chosen for being lightweight, efficient, and sufficient for simple document-based QA tasks. Instead of using heavier LLMs like GPT-4 or Gemini — which would increase cost and latency — we opted for an **intelligent and economical** solution.

Additionally, by running locally via Ollama, we ensure **data security**, as **no information is sent to external servers via API**.

---

### 🧠 Architecture without `memory`

Although `ConversationBufferMemory` is instantiated in the code, it is **not used** in the pipeline — an intentional choice to ensure:

- Faster responses  
- Lower coupling  
- Simpler inference flow

As the system is designed to answer **independent questions**, omitting memory is an optimization, not a limitation.

---

### 👍👎 Structured supervised feedback

The interface allows users to rate each answer as **good** (👍) or **bad** (👎). Feedback is saved in a structured `jsonl` format along with:

- User question  
- Generated response  
- Source documents used  
- Timestamp

This enables, in the future:

- Supervised learning from real usage  
- Fine-tuning document ranking  
- Analyzing user behavior

---

## 🔧 Tech Stack

| Layer         | Technology                         |
|---------------|------------------------------------|
| UI            | Gradio                             |
| Embeddings    | `all-MiniLM-L6-v2` (HuggingFace)   |
| Vector Store  | Persistent ChromaDB                |
| RAG           | LangChain                          |
| LLM           | `phi3` via Ollama                  |
| Logging       | Pydantic + JSONL                   |
| Visualization | t-SNE (optional notebook)          |

---

## 📁 Project Structure

```
├── app.py                    # Main script
├── chat_explain_model.ipynb  # System explanation notebook
├── feedback_log.jsonl        # Structured feedback log
├── knowledge-base/           # Documents for RAG
└── vector_db/                # Persistent vector store
```

---

## 💬 Example Use Case

> **Question**: "How does the service distribution model work?"  
> **Expected Answer**: Explanation based on internal documents, with transparency about which sources were used.

---

## 📊 Real-Time Feedback

- 👍 Marks the answer as good  
- 👎 Marks the answer as bad  

All feedback is saved with full context and will support future improvements such as:
- Filtering low-value documents  
- Retriever adjustments  
- Answer quality analysis by topic

---

## 🔮 Next Steps

### ☁️ 1. Deploy on GCP (Cloud Run)

Deploy the application on Google Cloud Run to make it accessible via browser without requiring local execution. The Gradio interface will serve as a lightweight front-end for non-technical users.

### 📈 2. Metrics Dashboard

Implement a dashboard with:

- Number of questions over time  
- % of positive vs negative answers  
- Most used vs rejected sources  
- Average response time

> These improvements prepare the system for expansion and AI governance at scale.

---

## 🧠 What this project demonstrates

- Ability to **translate business problems into applied AI solutions**  
- Mastery of modern tools for **lightweight and efficient RAG**  
- Strategic thinking: technically sound decisions based on cost, performance, and security  
- Vision for continuous evolution (supervised feedback + metrics + deploy)  
- Clear communication of technical value and practical impact