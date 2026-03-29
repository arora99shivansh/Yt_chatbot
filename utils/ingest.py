from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
import re
import os
import requests


def extract_video_id(url):
    match = re.search(r"(?:v=|\/)([0-9A-Za-z_-]{11}).*", url)
    return match.group(1) if match else None


def fetch_transcript(video_id):
    """Fetch transcript via Supadata API — works on all cloud IPs."""
    api_key = os.environ.get("SUPADATA_API_KEY")
    if not api_key:
        raise Exception("SUPADATA_API_KEY not set in environment.")

    url = f"https://api.supadata.ai/v1/youtube/transcript"
    headers = {"x-api-key": api_key}
    params = {"videoId": video_id, "text": True}

    response = requests.get(url, headers=headers, params=params, timeout=30)

    if response.status_code == 200:
        data = response.json()
        # Supadata returns either plain text (text=True) or list of chunks
        if isinstance(data, str):
            return data
        elif isinstance(data, dict) and "content" in data:
            content = data["content"]
            if isinstance(content, str):
                return content
            elif isinstance(content, list):
                return " ".join([
                    c["text"] if isinstance(c, dict) else str(c)
                    for c in content
                ])
        elif isinstance(data, list):
            return " ".join([
                c["text"] if isinstance(c, dict) else str(c)
                for c in data
            ])
        return str(data)
    else:
        raise Exception(f"Supadata API error {response.status_code}: {response.text}")


def process_video(url):
    video_id = extract_video_id(url)
    if not video_id:
        return None, "❌ Invalid YouTube URL."

    try:
        transcript = fetch_transcript(video_id)
        if not transcript or len(transcript.strip()) < 50:
            return None, "❌ Transcript is empty or too short."
    except Exception as e:
        return None, f"❌ Could not fetch transcript: {str(e)}"

    try:
        splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        chunks = splitter.create_documents([transcript])

        embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
        vector_store = FAISS.from_documents(chunks, embeddings)

        return vector_store, "✅ Video loaded and processed successfully! You can now ask questions."

    except Exception as e:
        return None, f"❌ Error during processing or embedding: {str(e)}"