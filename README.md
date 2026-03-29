# 📺 YouTube RAG Chatbot

[![HuggingFace Spaces](https://img.shields.io/badge/🤗%20Hugging%20Face-Spaces-blue)](https://huggingface.co/spaces/Shivansharora2631/yt_rag_chatbot)
[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?logo=python&logoColor=white)](https://python.org)
[![Gradio](https://img.shields.io/badge/Gradio-6.x-orange)](https://gradio.app)
[![LangChain](https://img.shields.io/badge/LangChain-0.3-green)](https://langchain.com)
[![Groq](https://img.shields.io/badge/Groq-LLaMA%203.1-purple)](https://groq.com)

A production-ready **Retrieval-Augmented Generation (RAG)** chatbot that lets you load multiple YouTube videos and have intelligent conversations about their content — entirely powered by open-source models and free APIs.

---

## 🚀 Live Demo

👉 **[Try it on Hugging Face Spaces](https://huggingface.co/spaces/Shivansharora2631/yt_rag_chatbot)**

---

## ✨ Features

- 🎬 **Multiple Videos** — Load and query multiple YouTube videos simultaneously
- 💬 **Intelligent Chat** — Ask questions, get summaries, extract insights from video content
- 🧠 **RAG Pipeline** — FAISS vector store + semantic search for accurate, context-aware answers
- 💾 **Chat History** — Conversations are saved locally as JSON
- ☁️ **Cloud Ready** — Deployed on Hugging Face Spaces with Supadata API for transcript fetching
- 🎨 **Dark UI** — YouTube-inspired dark theme built with Gradio

---

## 🛠️ Tech Stack

| Component | Technology |
|-----------|-----------|
| **Transcript Fetching** | Supadata API |
| **Text Splitting** | LangChain `RecursiveCharacterTextSplitter` |
| **Embeddings** | HuggingFace `sentence-transformers/all-MiniLM-L6-v2` |
| **Vector Store** | FAISS (Facebook AI Similarity Search) |
| **LLM** | Groq `llama-3.1-8b-instant` |
| **RAG Framework** | LangChain LCEL |
| **UI** | Gradio 6.x |
| **Deployment** | Hugging Face Spaces |

---

## 📁 Project Structure

```
yt_rag_chatbot/
├── app.py                  # Main Gradio application
├── requirements.txt        # Python dependencies
├── .env                    # API keys (do NOT commit)
├── .gitignore
└── utils/
    ├── __init__.py
    ├── ingest.py           # Transcript fetching + FAISS vector store
    └── retriever.py        # Groq LLM + RAG chain
```

---

## ⚙️ Local Setup

### 1. Clone the repository
```bash
git clone https://github.com/Shivansh/yt-rag-chatbot.git
cd yt-rag-chatbot
```

### 2. Create virtual environment
```bash
python -m venv venv
venv\Scripts\activate      # Windows
source venv/bin/activate   # Mac/Linux
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Set up API keys
Create a `.env` file in the root directory:
```env
GROQ_API_KEY=gsk_xxxxxxxxxxxxxxxxxxxxxxxx
SUPADATA_API_KEY=your_supadata_key_here
```

Get your free API keys:
- **Groq** → [console.groq.com](https://console.groq.com) — Free, fast LLaMA 3.1 inference
- **Supadata** → [supadata.ai](https://supadata.ai) — YouTube transcript API (100 req/day free)

### 5. Run the app
```bash
python app.py
```

Open `http://127.0.0.1:7860` in your browser.

---

## ☁️ Deploy on Hugging Face Spaces

1. Create a new Space at [huggingface.co/spaces](https://huggingface.co/spaces)
   - SDK: **Gradio**
   - Hardware: **CPU Basic** (free)

2. Upload these files:
   ```
   app.py
   requirements.txt
   utils/__init__.py
   utils/ingest.py
   utils/retriever.py
   ```

3. Add secrets in **Settings → Variables and Secrets**:
   ```
   GROQ_API_KEY = gsk_xxxxxxxxxxxxxxxxxxxxxxxx
   SUPADATA_API_KEY = your_supadata_key_here
   ```

4. Your app will be live at:
   ```
   https://huggingface.co/spaces/YOUR_USERNAME/yt_rag_chatbot
   ```

---

## 🧠 How It Works

```
YouTube URL
    │
    ▼
Supadata API ──► Transcript Text
    │
    ▼
RecursiveCharacterTextSplitter ──► Text Chunks (1000 tokens, 200 overlap)
    │
    ▼
HuggingFace Embeddings ──► Dense Vectors
    │
    ▼
FAISS Vector Store ──► Semantic Index
    │
    ▼
User Question ──► Similarity Search (top-4 chunks)
    │
    ▼
Groq LLaMA 3.1 ──► Context-Aware Answer
```

---

## 📦 Requirements

```
langchain
langchain-community
langchain-huggingface
langchain-groq
langchain-text-splitters
sentence-transformers
faiss-cpu
gradio
python-dotenv
huggingface_hub
requests
```

---

## 🔒 Security Notes

- Never commit `.env` or `cookies.txt` to version control
- Add both to `.gitignore`
- Use HuggingFace Secrets for cloud deployment

---

## 🙋 Author

**Shivansh Arora**
- GitHub: [@Shivansh](https://github.com/Shivansh)

---

## ⭐ Support

If you found this project useful, please consider giving it a ⭐ on GitHub and a ❤️ on Hugging Face Spaces!

---

## 📄 License

This project is licensed under the MIT License.