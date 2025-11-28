import streamlit as st
import requests
from streamlit_lottie import st_lottie
import time
from PIL import Image

# === 1. Configuration & Utilities ===

def load_lottieurl(url: str):
    try:
        r = requests.get(url)
        if r.status_code != 200:
            return None
        return r.json()
    except:
        return None

import os

# ... imports ...

logo_path = os.path.join(os.path.dirname(__file__), "logo_no_bg.png")
logo = Image.open(logo_path)
st.set_page_config(
    page_title="NOVA - AI Log Analyzer",
    page_icon=logo,
    layout="wide",
    initial_sidebar_state="expanded",
)

# === 2. New Animated Assets ===

# This one is very lively and friendly
url_nova_avatar = "https://lottie.host/955e4680-e816-43f9-a3b0-27943501700b/2X1X1X1X1X.json"

# Static Avatar Image (For the Chat Bubbles to match)
nova_static_icon = "https://cdn-icons-png.flaticon.com/512/4712/4712109.png"
user_static_icon = "https://cdn-icons-png.flaticon.com/512/9131/9131529.png"

# Processing Animation (High Tech Ring)
url_processing = "https://assets7.lottiefiles.com/packages/lf20_w51pcehl.json" 

lottie_avatar = load_lottieurl(url_nova_avatar)
lottie_processing = load_lottieurl(url_processing)

# === 3. Deep Cyberpunk/Purple Theme CSS ===
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600&family=Orbitron:wght@500;700&family=Rajdhani:wght@500;600;700&display=swap');

    :root {
        --primary-color: #BF00FF;
        --secondary-color: #00ffea;
        --bg-dark: #0a0a12;
    }

    /* Main Background & Text */
    .stApp {
        background: linear-gradient(160deg, #050505 0%, #1a0b2e 50%, #110022 100%);
        background-attachment: fixed;
        color: #e0e0e0 !important;
    }

    /* Sidebar Styling */
    section[data-testid="stSidebar"] {
        background-color: rgba(10, 8, 20, 0.95);
        border-right: 1px solid rgba(191, 0, 255, 0.2);
        box-shadow: 5px 0 15px rgba(0,0,0,0.5);
    }

    /* Fonts */
    h1, h2, h3 { font-family: 'Orbitron', sans-serif !important; color: #fff !important; text-shadow: 0 0 10px rgba(191,0,255,0.5); }
    p, li, label, div, span { font-family: 'Rajdhani', sans-serif !important; color: #e0e0e0 !important; }

    /* --- CHAT STYLING (Friendly "Nova" Theme) --- */
    
    /* User Message Bubble */
    div[data-testid="stChatMessage"]:nth-child(odd) {
        background-color: rgba(191, 0, 255, 0.15);
        border: 1px solid rgba(191, 0, 255, 0.3);
        border-radius: 15px 15px 0 15px;
    }

    /* Nova (Bot) Message Bubble */
    div[data-testid="stChatMessage"]:nth-child(even) {
        background-color: rgba(0, 255, 234, 0.08);
        border: 1px solid rgba(0, 255, 234, 0.2);
        border-radius: 15px 15px 15px 0;
    }

    /* Avatars in Chat - Circular & Styled */
    div[data-testid="stChatMessageAvatar"] img {
        background-color: #1a0b2e;
        border: 2px solid #BF00FF;
        border-radius: 50%;
        padding: 2px;
    }

    /* Chat Input Area */
    .stChatInput textarea {
        background-color: rgba(255, 255, 255, 0.05) !important;
        color: #fff !important;
        border: 1px solid #BF00FF !important;
        border-radius: 20px !important;
    }

    /* --- UI ELEMENTS --- */
    .stTextInput > div > div > input, .stFileUploader > div > div > button {
        background-color: rgba(255, 255, 255, 0.05) !important;
        color: #00ffea !important;
        border: 1px solid rgba(191, 0, 255, 0.3) !important;
        border-radius: 8px;
    }
    
    .stButton > button {
        background: linear-gradient(90deg, #6200EA, #B00020) !important;
        color: white !important;
        font-family: 'Orbitron', sans-serif !important;
        box-shadow: 0 0 20px rgba(98, 0, 234, 0.4);
        border-radius: 8px;
    }
    
    .stButton > button:hover {
        transform: scale(1.02);
        background: linear-gradient(90deg, #7c4dff, #ff4081) !important;
    }

    /* Result Cards */
    .result-card {
        background: linear-gradient(135deg, rgba(255, 255, 255, 0.03), rgba(255, 255, 255, 0.01));
        border: 1px solid rgba(191, 0, 255, 0.3);
        border-left: 4px solid var(--primary-color);
        border-radius: 8px;
        padding: 20px;
        margin-bottom: 20px;
        animation: slideIn 0.5s ease-out forwards;
    }
    @keyframes slideIn { to { opacity: 1; transform: translateY(0); } }
    </style>
    """,
    unsafe_allow_html=True
)

# === 4. Sidebar: "NOVA" The Friendly Assistant ===
with st.sidebar:
    # A. The Motionable Avatar (Nova)
    if lottie_avatar:
        # loop=True makes it "motionable" forever
        st_lottie(lottie_avatar, height=220, key="nova_avatar", loop=True)
    else:
        st.image(nova_static_icon, width=150)

    # Friendly Title
    st.markdown(
        """
        <div style="text-align: center; margin-bottom: 10px;">
            <h2 style="color: #BF00FF !important; margin:0; letter-spacing: 2px;">NOVA</h2>
            <p style="color: #bbb; font-size: 0.9rem; margin-top: -5px;">Your AI Log Companion</p>
            <div style="font-size: 0.7rem; color: #00ffea !important; background: rgba(0, 255, 234, 0.1); border: 1px solid #00ffea; display: inline-block; padding: 2px 10px; border-radius: 12px;">● ACTIVE</div>
        </div>
        """, 
        unsafe_allow_html=True
    )
    
    st.divider()

    # B. Chat Session Logic
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant", "content": "Hi! I'm Nova. I can help you debug logs. Upload a file to get started!"}
        ]

    # C. Display Chat History inside Sidebar
    chat_container = st.container()
    with chat_container:
        for message in st.session_state.messages:
            # Use specific image icons for Avatar
            avatar_icon = nova_static_icon if message["role"] == "assistant" else user_static_icon
            
            with st.chat_message(message["role"], avatar=avatar_icon):
                st.markdown(message["content"])

    # D. Sidebar Input
    if prompt := st.chat_input("Talk to Nova...", key="sidebar_chat"):
        # Add user message
        st.session_state.messages.append({"role": "user", "content": prompt})
        with chat_container:
            with st.chat_message("user", avatar=user_static_icon):
                st.markdown(prompt)

        # Call Backend for Chat
        try:
            # Assuming backend is running on localhost:8000
            response = requests.post("http://localhost:8000/chat", data={"message": prompt})
            
            if response.status_code == 200:
                response_text = response.json()["response"]
            else:
                response_text = f"I'm having trouble thinking right now. (Error: {response.status_code})"
        except Exception as e:
            response_text = f"I can't reach my brain! (Connection Error: {e})"
        
        # Add assistant message
        st.session_state.messages.append({"role": "assistant", "content": response_text})
        with chat_container:
            with st.chat_message("assistant", avatar=nova_static_icon):
                st.markdown(response_text)
    st.markdown("<p style='color: #bbb;'>Powered by Nova AI Engine</p>", unsafe_allow_html=True)

st.markdown("---")

# Main Dashboard Form
with st.container():
    uploaded = st.file_uploader("📂 Source File", type=["log", "txt", "json"])
    
    context = st.text_input("📝 Analysis Context", placeholder="Optional")

if st.button("ASK NOVA TO SCAN"):
    # Animation
    if lottie_processing:
        with st.columns([1,2,1])[1]:
            st_lottie(lottie_processing, height=150, key="proc_main")
            st.markdown("<p style='text-align:center; color:#BF00FF; letter-spacing:2px; font-weight:bold;'>NOVA IS THINKING...</p>", unsafe_allow_html=True)

    # Fake Delay & Result
    time.sleep(2.5)
    
    # Call Backend
    try:
        if uploaded is not None:
            files = {"file": (uploaded.name, uploaded, uploaded.type)}
            data = {"context": context}
            
            # Assuming backend is running on localhost:8000
            response = requests.post("http://localhost:8000/analyze", files=files, data=data)
            
            if response.status_code == 200:
                result = response.json()
            else:
                st.error(f"Error: {response.status_code} - {response.text}")
                st.stop()
        else:
            st.warning("Please upload a file first.")
            st.stop()
    except Exception as e:
        st.error(f"Connection Error: {e}")
        st.stop()

    # Display Results
    def render_card(title, icon, content, code=False):
        html = ""
        if isinstance(content, list):
            for item in content:
                if code: html += f"<div style='background:#181825; color:#00ffea; padding:8px 12px; margin:5px 0; font-family:monospace; border-radius:4px; border:1px solid #333;'>$ {item}</div>"
                else: html += f"<li style='color:#e0e0e0; margin-bottom:5px;'>{item}</li>"
            if not code: html = f"<ul>{html}</ul>"
        else:
            html = f"<p style='color:#e0e0e0;'>{content}</p>"
            
        st.markdown(f"""
            <div class="result-card">
                <div style="color:#BF00FF; font-family:'Orbitron'; font-size:1.1rem; margin-bottom:10px; border-bottom:1px solid rgba(191,0,255,0.2); padding-bottom:5px;">
                    {icon} {title}
                </div>
                {html}
            </div>
        """, unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        render_card("Summary", "📄", result["summary"])
        render_card("Root Causes", "🔍", result["root_causes"])
    with c2:
        render_card("Anomalies", "⚠️", result["issues"])
        render_card("Fixes", "🛠️", result["remediation"])
    
    render_card("Recommended Commands", "💻", result["commands"], code=True)

    # Chat update
    st.session_state.messages.append({"role": "assistant", "content": "I've finished scanning! Check the dashboard for the results. I found some database issues you should look at. 👀"})
    st.rerun()
