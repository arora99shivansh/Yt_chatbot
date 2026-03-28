from dotenv import load_dotenv
load_dotenv()

import gradio as gr
import json
import os
from datetime import datetime
from utils.ingest import process_video
from utils.retriever import get_answer

# ─── State ────────────────────────────────────────────────────────────────────
vector_stores = {}
video_metadata = {}
chat_histories = {}
HISTORY_FILE = "chat_history.json"


# ─── Persistence ──────────────────────────────────────────────────────────────
def save_history():
    try:
        with open(HISTORY_FILE, "w") as f:
            json.dump(chat_histories, f, indent=2)
    except Exception:
        pass


def load_history():
    global chat_histories
    if os.path.exists(HISTORY_FILE):
        try:
            with open(HISTORY_FILE, "r") as f:
                chat_histories = json.load(f)
        except Exception:
            chat_histories = {}


load_history()


# ─── Video loading ─────────────────────────────────────────────────────────────
def load_video(url, current_videos_state):
    if not url.strip():
        return current_videos_state, "⚠️ Please enter a YouTube URL.", gr.update()

    import re
    match = re.search(r"(?:v=|\/)([0-9A-Za-z_-]{11}).*", url)
    if not match:
        return current_videos_state, "❌ Invalid YouTube URL.", gr.update()

    video_id = match.group(1)

    if video_id in vector_stores:
        labels = [f"🎬 {vid} ({video_metadata[vid]['added_at']})" for vid in video_metadata]
        return list(video_metadata.keys()), "ℹ️ Already loaded!", gr.update(choices=labels, value=labels)

    vs, message = process_video(url)
    if not vs:
        return current_videos_state, message, gr.update()

    vector_stores[video_id] = vs
    video_metadata[video_id] = {"url": url, "added_at": datetime.now().strftime("%H:%M:%S")}

    labels = [f"🎬 {vid} ({video_metadata[vid]['added_at']})" for vid in video_metadata]
    return list(video_metadata.keys()), f"✅ Loaded `{video_id}`! Total: {len(video_metadata)}", gr.update(
        choices=labels, value=labels
    )


# ─── Chat ──────────────────────────────────────────────────────────────────────
def chat(message, history, selected_videos):
    if not message.strip():
        return history, ""

    if not vector_stores:
        history.append({"role": "user", "content": message})
        history.append({"role": "assistant", "content": "⚠️ Please load at least one YouTube video first!"})
        return history, ""

    import re
    if not selected_videos:
        selected_ids = list(vector_stores.keys())
    else:
        selected_ids = []
        for label in selected_videos:
            m = re.search(r"🎬 ([0-9A-Za-z_-]{11})", label)
            if m and m.group(1) in vector_stores:
                selected_ids.append(m.group(1))
        if not selected_ids:
            selected_ids = list(vector_stores.keys())

    try:
        if len(selected_ids) == 1:
            answer = get_answer(vector_stores[selected_ids[0]], message)
        else:
            answers = []
            for vid in selected_ids:
                ans = get_answer(vector_stores[vid], message)
                answers.append(f"**Video `{vid}`:**\n{ans}")
            answer = "\n\n---\n\n".join(answers)

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if "default" not in chat_histories:
            chat_histories["default"] = []
        chat_histories["default"].append({"role": "user", "content": message, "timestamp": timestamp})
        chat_histories["default"].append({"role": "assistant", "content": answer, "timestamp": timestamp})
        save_history()

        history.append({"role": "user", "content": message})
        history.append({"role": "assistant", "content": answer})
        return history, ""

    except Exception as e:
        history.append({"role": "user", "content": message})
        history.append({"role": "assistant", "content": f"❌ Error: {str(e)}"})
        return history, ""


def clear_chat():
    return [], ""


def get_history_display():
    if "default" not in chat_histories or not chat_histories["default"]:
        return "No history yet."
    lines = []
    for msg in chat_histories["default"][-20:]:
        role = "🧑 You" if msg["role"] == "user" else "🤖 Bot"
        lines.append(f"**{role}** [{msg.get('timestamp','')}]:\n{msg['content']}")
    return "\n\n---\n\n".join(lines)


# ─── UI ────────────────────────────────────────────────────────────────────────
with gr.Blocks(title="YouTube RAG Chatbot", theme=gr.themes.Soft()) as demo:

    gr.HTML("""
    <div style="text-align:center;padding:20px;background:linear-gradient(135deg,#667eea,#764ba2);border-radius:12px;margin-bottom:20px;">
        <h1 style="color:white;font-size:2em;margin:0;">📺 YouTube RAG Chatbot</h1>
        <p style="color:rgba(255,255,255,0.85);margin:8px 0 0 0;">
            Load multiple YouTube videos and chat with their content — powered by Groq & LangChain
        </p>
    </div>
    """)

    videos_state = gr.State([])

    with gr.Row():
        with gr.Column(scale=1):
            gr.Markdown("### 🎬 Video Manager")
            url_input = gr.Textbox(label="YouTube URL", placeholder="https://www.youtube.com/watch?v=...")
            load_btn = gr.Button("➕ Load Video", variant="primary")
            status_box = gr.Textbox(label="Status", interactive=False, lines=2)

            gr.Markdown("#### 📋 Loaded Videos")
            video_selector = gr.CheckboxGroup(choices=[], value=[], label="Select to query", interactive=True)

            with gr.Accordion("📜 Chat History", open=False):
                history_btn = gr.Button("🔄 Refresh", size="sm")
                history_display = gr.Markdown("Click Refresh to load.")

        with gr.Column(scale=2):
            gr.Markdown("### 💬 Chat")
            # ✅ Gradio 6.10 compatible — no type, no bubble_full_width
            chatbot = gr.Chatbot(value=[], height=500, show_label=False)

            with gr.Row():
                msg_input = gr.Textbox(placeholder="Ask anything about the video(s)...", show_label=False, scale=5)
                send_btn = gr.Button("Send ➤", variant="primary", scale=1)

            clear_btn = gr.Button("🗑️ Clear Chat", variant="secondary")

    # ── Wiring ──
    load_btn.click(
        fn=load_video, inputs=[url_input, videos_state], outputs=[videos_state, status_box, video_selector]
    ).then(lambda: "", outputs=url_input)

    url_input.submit(
        fn=load_video, inputs=[url_input, videos_state], outputs=[videos_state, status_box, video_selector]
    ).then(lambda: "", outputs=url_input)

    send_btn.click(fn=chat, inputs=[msg_input, chatbot, video_selector], outputs=[chatbot, msg_input])
    msg_input.submit(fn=chat, inputs=[msg_input, chatbot, video_selector], outputs=[chatbot, msg_input])
    clear_btn.click(fn=clear_chat, outputs=[chatbot, msg_input])
    history_btn.click(fn=get_history_display, outputs=history_display)


if __name__ == "__main__":
    demo.launch(share=True)