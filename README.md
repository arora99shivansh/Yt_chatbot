# 📺 YouTube RAG Chatbot

A production-ready RAG (Retrieval-Augmented Generation) chatbot that lets you load multiple YouTube videos and chat with their transcript content.

## 🚀 Features
- ✅ Load **multiple YouTube videos** simultaneously
- ✅ **Select specific videos** to query
- ✅ **Chat history** saved locally (JSON)
- ✅ Powered by **Groq (LLaMA 3.1)** + **FAISS** + **LangChain**
- ✅ Beautiful **custom UI** with Gradio

## 🛠️ Tech Stack
| Component | Technology |
|-----------|-----------|
| Embeddings | HuggingFace `all-MiniLM-L6-v2` |
| Vector Store | FAISS |
| LLM | Groq `llama-3.1-8b-instant` |
| Framework | LangChain |
| UI | Gradio |
| Deployment | Railway |

## ⚙️ Setup

### 1. Clone & install
```bash
git clone <your-repo>
cd yt_chatbot
pip install -r requirements.txt
```

### 2. Set environment variables
Create a `.env` file:
```
GROQ_API_KEY=gsk_xxxxxxxxxxxxxxxx
```

### 3. Add YouTube cookies (to bypass IP blocks)
Export cookies from your browser using "Get cookies.txt LOCALLY" Chrome extension and save as `cookies.txt` in the root folder.

### 4. Run
```bash
python app.py
```

## ☁️ Deploy on Railway
1. Push to GitHub
2. Go to [railway.app](https://railway.app) → New Project → Deploy from GitHub
3. Add environment variable: `GROQ_API_KEY`
4. Deploy! 🚀

## 📁 Project Structure
```
yt_chatbot/
├── app.py              # Main Gradio app
├── requirements.txt
├── Procfile            # Railway/Render config
├── railway.json        # Railway config
├── .gitignore
├── cookies.txt         # YouTube cookies (do NOT commit)
├── .env                # API keys (do NOT commit)
└── utils/
    ├── ingest.py       # YouTube transcript + FAISS
    └── retriever.py    # Groq LLM + RAG chain
```