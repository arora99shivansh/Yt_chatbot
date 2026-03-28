from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
import re
import os
import requests
from http.cookiejar import MozillaCookieJar


def extract_video_id(url):
    """Extracts the video ID from a standard YouTube URL."""
    match = re.search(r"(?:v=|\/)([0-9A-Za-z_-]{11}).*", url)
    return match.group(1) if match else None


def get_ytt_client():
    """Returns YouTubeTranscriptApi instance with cookies if available."""
    cookie_file = "cookies.txt"
    if os.path.exists(cookie_file):
        try:
            session = requests.Session()
            jar = MozillaCookieJar(cookie_file)
            jar.load(ignore_discard=True, ignore_expires=True)
            session.cookies = jar
            return YouTubeTranscriptApi(http_client=session)
        except Exception:
            pass
    return YouTubeTranscriptApi()


def process_video(url):
    video_id = extract_video_id(url)
    if not video_id:
        return None, "❌ Invalid YouTube URL."

    try:
        ytt_api = get_ytt_client()
        transcript_data = ytt_api.fetch(video_id, languages=["en"])

        # Robust extraction: handles both dicts and custom objects
        transcript = " ".join([
            chunk["text"] if isinstance(chunk, dict) else getattr(chunk, "text", str(chunk))
            for chunk in transcript_data
        ])

    except TranscriptsDisabled:
        return None, "❌ No captions available for this video."
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