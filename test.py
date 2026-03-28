import traceback
try:
    from youtube_transcript_api import YouTubeTranscriptApi
    from langchain_text_splitters import RecursiveCharacterTextSplitter
    from langchain_huggingface import HuggingFaceEmbeddings
    from langchain_community.vectorstores import FAISS
    from langchain.schema import Document

    video_id = "jNQXAC9IVRw" # me at the zoo
    transcript = YouTubeTranscriptApi.get_transcript(video_id)
    text = " ".join([t['text'] for t in transcript])
    docs = [Document(page_content=text, metadata={"source": video_id})]
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    splits = text_splitter.split_documents(docs)
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    vector_store = FAISS.from_documents(splits, embeddings)
    print("Vector store created successfully:", vector_store)
except Exception as e:
    traceback.print_exc()
