import base64
import streamlit as st
import spacy
from gtts import gTTS

# Page setup
st.set_page_config(
    page_title="ML Chinese Grammar Visualizer",
    page_icon="🇨🇳",
    layout="centered"
)

st.title("ML-Powered Chinese Grammar Visualizer")
st.write("Using SpaCy Neural Networks for deep linguistic parsing.")

# Load SpaCy Chinese model (Cached so it only loads once)
@st.cache_resource
def load_spacy():
    return spacy.load("zh_core_web_sm")

nlp = load_spacy()

# Color mapping for SpaCy coarse POS tags (Universal POS)
POS_COLORS = {
    "NOUN": "#FF9999",   # Noun
    "PROPN": "#FF7777",  # Proper Noun
    "VERB": "#99FF99",   # Verb
    "AUX": "#CCFFCC",    # Auxiliary Verb
    "ADJ": "#9999FF",    # Adjective
    "ADV": "#FFFF99",    # Adverb
    "PRON": "#FFCC99",   # Pronoun
    "ADP": "#CC99FF",    # Adposition (Preposition)
    "CCONJ": "#FF99FF",  # Coordinating Conjunction
    "SCONJ": "#FF66FF",  # Subordinating Conjunction
    "PART": "#E0B0FF",   # Particle
    "other": "#E0E0E0"
}

# Simplified dictionary mapping for quick demonstration
DICT_MAPPING = {
    "我": "I / me", "今天": "today", "在": "at / in / on", "学校": "school",
    "吃": "eat", "了": "[completed action]", "一个": "one / a", "苹果": "apple",
    "他": "he / him", "她": "she / her", "喜欢": "like", "看": "read / watch",
    "书": "book", "买": "buy", "车": "car", "猫": "cat", "抓": "catch / scratch",
    "老鼠": "mouse / rat"
}

def generate_audio(text):
    """Generates gTTS audio and embeds it as HTML."""
    try:
        tts = gTTS(text=text, lang='zh-cn')
        tts.save("speech.mp3")
        with open("speech.mp3", "rb") as f:
            audio_bytes = f.read()
        b64_audio = base64.b64encode(audio_bytes).decode()
        return f'<audio src="data:audio/mp3;base64,{b64_audio}" controls style="width: 100%; margin-bottom: 20px;"></audio>'
    except Exception:
        return "<p style='color:red;'>Audio generation failed. Check connection.</p>"

def extract_ml_svo(doc):
    """
    Extracts Subject, Verb, and Object using SpaCy structural dependency parsing.
    Looks for nominal subjects (nsubj) and direct objects (obj) tied to root verbs.
    """
    subject = "Unknown"
    verb = "Unknown"
    obj = "Unknown"
    
    # 1. Find the root verb of the sentence
    root_token = None
    for token in doc:
        if token.dep_ == "ROOT" or token.pos_ == "VERB":
            root_token = token
            verb = token.text
            break
            
    # 2. Find subject and object linked directly to that verb structure
    if root_token:
        for token in doc:
            # Check for nominal subject pointing to our verb
            if token.dep_ in ("nsubj", "nsubj:pass") and (token.head == root_token or token.head.pos_ == "VERB"):
                subject = token.text
            # Check for direct object pointing to our verb
            elif token.dep_ in ("obj", "dobj") and (token.head == root_token or token.head.pos_ == "VERB"):
                obj = token.text
                
    return subject, verb, obj

# User input
default_text = "猫抓了老鼠。"
user_text = st.text_input("Enter a Chinese sentence:", default_text)

if user_text:
    # Process text through SpaCy Neural Network Pipeline
    doc = nlp(user_text)

    # 1. Audio Pronunciation
    st.subheader("🔊 Audio Pronunciation")
    audio_html = generate_audio(user_text)
    st.markdown(audio_html, unsafe_allow_html=True)

    # 2. Machine Learning SVO Breakdown
    st.subheader("📊 ML Sentence Structure Breakdown")
    subj, vrb, objc = extract_ml_svo(doc)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(label="👤 Subject (nsubj)", value=subj)
    with col2:
        st.metric(label="🏃‍♂️ Root Verb (VERB)", value=vrb)
    with col3:
        st.metric(label="📦 Object (obj)", value=objc)

    # 3. Word Segmentation & Universal POS Tag Visualizer
    st.subheader("🧩 Tokenization & Linguistic Features")
    
    html_code = '<div style="font-size: 20px; line-height: 3; display: flex; flex-wrap: wrap; gap: 12px;">'
    for token in doc:
        # Determine background color based on Universal POS tag
        color = POS_COLORS.get(token.pos_, POS_COLORS["other"])
        translation = DICT_MAPPING.get(token.text, "[Unknown]")
        
        # Display word, part of speech, dependency relationship, and definition
        html_code += f"""
        <div style="background-color: {color}; padding: 10px; border-radius: 8px; text-align: center; min-width: 90px; box-shadow: 1px 1px 3px rgba(0,0,0,0.1);">
            <div style="font-weight: bold; font-size: 22px; color: #111;">{token.text}</div>
            <div style="font-size: 11px; color: #333; margin: -2px 0 0 0;"><b>{token.pos_}</b></div>
            <div style="font-size: 10px; color: #555; margin: -4px 0 4px 0;">dep: {token.dep_}</div>
            <div style="font-size: 13px; color: #222; border-top: 1px solid rgba(0,0,0,0.1); padding-top: 2px;">{translation}</div>
        </div>
        """
    html_code += '</div>'
    st.markdown(html_code, unsafe_allow_html=True)

    # Legend Map
    st.subheader("Legend (Universal POS Tags)")
    legend_html = ""
    for label, color in POS_COLORS.items():
        legend_html += f'<span style="background-color: {color}; padding: 4px 10px; margin: 4px; border-radius: 4px; display: inline-block; font-size: 12px; font-weight: bold;">{label}</span> '
    st.markdown(legend_html, unsafe_allow_html=True)

        
    # 4. Initialize Database Engine & Log Transaction Data
    from database import GrammarLogDatabase
    db = GrammarLogDatabase()
    db.log_transaction(user_input, svo_data)
        
    # 5. Render Historical Analytical Telemetry logs directly in the UI
    st.subheader("📜 System Telemetry Logs (SQLite Persistence)")
    recent_logs = db.fetch_recent_logs()
    for log in recent_logs:
    st.caption(f"🕒 **{log[0]}** | Input: `{log[1]}` → Subj: `{log[2]}`, Verb: `{log[3]}`, Obj: `{log[4]}`")
