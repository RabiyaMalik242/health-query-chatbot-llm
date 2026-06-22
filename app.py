import streamlit as st

# ── Import everything from chatbot.py ─────────────────────────────────────────
from chatbot import client, chat, chat_with_stats, safety_check, SYSTEM_PROMPT

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="MediBot — Health Assistant",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&family=DM+Serif+Display&display=swap');

html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding-top: 1.5rem; padding-bottom: 1rem; }
.stApp { background: #0f1117; }

[data-testid="stSidebar"] {
    background: #141820;
    border-right: 1px solid #1e2530;
}
[data-testid="stSidebar"] .stMarkdown p { color: #8892a4; font-size: 0.82rem; }

.medibot-header {
    background: linear-gradient(135deg, #0d7377 0%, #14a085 50%, #0d7377 100%);
    border-radius: 16px;
    padding: 28px 32px;
    margin-bottom: 24px;
    display: flex;
    align-items: center;
    gap: 18px;
    box-shadow: 0 4px 24px rgba(13, 115, 119, 0.35);
}
.medibot-header h1 {
    font-family: 'DM Serif Display', serif;
    font-size: 2rem;
    color: #ffffff;
    margin: 0;
    letter-spacing: -0.02em;
}
.medibot-header p {
    color: rgba(255,255,255,0.78);
    font-size: 0.88rem;
    margin: 4px 0 0 0;
    font-weight: 300;
}
.medibot-icon { font-size: 2.8rem; line-height: 1; }

.chat-wrapper { display: flex; flex-direction: column; gap: 16px; margin-bottom: 16px; }
.msg-user { display: flex; justify-content: flex-end; gap: 10px; align-items: flex-start; }
.msg-bot  { display: flex; justify-content: flex-start; gap: 10px; align-items: flex-start; }

.bubble-user {
    background: #0d7377;
    color: #ffffff;
    padding: 12px 16px;
    border-radius: 18px 18px 4px 18px;
    max-width: 72%;
    font-size: 0.9rem;
    line-height: 1.55;
    box-shadow: 0 2px 8px rgba(13,115,119,0.3);
}
.bubble-bot {
    background: #1a2130;
    color: #d4dce8;
    padding: 12px 16px;
    border-radius: 18px 18px 18px 4px;
    max-width: 75%;
    font-size: 0.9rem;
    line-height: 1.6;
    border: 1px solid #1e2a3a;
    box-shadow: 0 2px 8px rgba(0,0,0,0.2);
}
.bubble-bot strong { color: #4ecdc4; }
.bubble-bot ul { margin: 6px 0; padding-left: 18px; }
.bubble-bot li { margin: 3px 0; }

.avatar-user {
    width: 32px; height: 32px;
    background: #0d7377;
    border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
    font-size: 0.85rem; flex-shrink: 0; margin-top: 2px;
    color: white; font-weight: 600;
}
.avatar-bot {
    width: 32px; height: 32px;
    background: #14a085;
    border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
    font-size: 1rem; flex-shrink: 0; margin-top: 2px;
}

.msg-label-user {
    font-size: 0.72rem;
    color: #5a9a9a;
    margin-bottom: 4px;
    font-weight: 600;
    text-align: right;
}
.msg-label-bot {
    font-size: 0.72rem;
    color: #2a9a7a;
    margin-bottom: 4px;
    font-weight: 600;
}

.banner-emergency {
    background: linear-gradient(135deg, #7b1c1c, #b02a2a);
    border: 1px solid #c0392b;
    border-radius: 12px;
    padding: 14px 18px;
    color: #fce4e4;
    font-size: 0.88rem;
    line-height: 1.6;
    margin-bottom: 12px;
}
.banner-blocked {
    background: #1e1a10;
    border: 1px solid #7a6320;
    border-radius: 12px;
    padding: 14px 18px;
    color: #d4b96a;
    font-size: 0.88rem;
    line-height: 1.6;
    margin-bottom: 12px;
}

.stTextInput > div > div > input {
    background: #141820 !important;
    border: 1px solid #1e2a3a !important;
    border-radius: 12px !important;
    color: #d4dce8 !important;
    font-size: 0.92rem !important;
    padding: 12px 16px !important;
}
.stTextInput > div > div > input:focus {
    border-color: #0d7377 !important;
    box-shadow: 0 0 0 2px rgba(13,115,119,0.2) !important;
}
.stTextInput > div > div > input::placeholder { color: #4a5568 !important; }

.stButton > button {
    background: #0d7377 !important;
    color: white !important;
    border: none !important;
    border-radius: 10px !important;
    font-weight: 500 !important;
    font-size: 0.88rem !important;
    padding: 10px 20px !important;
    transition: all 0.2s ease !important;
}
.stButton > button:hover {
    background: #14a085 !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 4px 12px rgba(13,115,119,0.35) !important;
}

.metric-row { display: flex; gap: 10px; margin-bottom: 20px; }
.metric-card {
    flex: 1; background: #141820;
    border: 1px solid #1e2530;
    border-radius: 12px; padding: 14px 16px; text-align: center;
}
.metric-card .val { font-size: 1.4rem; font-weight: 600; color: #4ecdc4; }
.metric-card .lbl {
    font-size: 0.72rem; color: #5a6a80; margin-top: 2px;
    text-transform: uppercase; letter-spacing: 0.06em;
}

.section-label {
    font-size: 0.72rem; font-weight: 600; color: #4a5568;
    text-transform: uppercase; letter-spacing: 0.1em; margin-bottom: 8px;
}

.disclaimer {
    background: #141820;
    border: 1px solid #1e2530;
    border-left: 3px solid #0d7377;
    border-radius: 8px;
    padding: 10px 14px;
    font-size: 0.78rem;
    color: #5a6a80;
    margin-top: 10px;
    line-height: 1.5;
}

.safety-badge {
    display: inline-block;
    background: #0d2e1a;
    border: 1px solid #1a5c35;
    border-radius: 6px;
    padding: 3px 10px;
    font-size: 0.72rem;
    color: #4ecdc4;
    margin: 2px 0;
}

.chat-scroll {
    max-height: 55vh; overflow-y: auto;
    padding-right: 4px; margin-bottom: 12px;
}
.chat-scroll::-webkit-scrollbar { width: 4px; }
.chat-scroll::-webkit-scrollbar-track { background: transparent; }
.chat-scroll::-webkit-scrollbar-thumb { background: #1e2a3a; border-radius: 4px; }
</style>
""", unsafe_allow_html=True)

# ── Quick questions ───────────────────────────────────────────────────────────
QUICK_QUESTIONS = [
    "What causes a sore throat?",
    "Is paracetamol safe for children?",
    "Symptoms of dehydration?",
    "How to improve sleep?",
    "What is hypertension?",
    "How to reduce stress?",
]

# ── Session state init ────────────────────────────────────────────────────────
if 'messages'      not in st.session_state: st.session_state.messages      = []
if 'history'       not in st.session_state: st.session_state.history       = []
if 'total_tokens'  not in st.session_state: st.session_state.total_tokens  = 0
if 'query_count'   not in st.session_state: st.session_state.query_count   = 0
if 'quick_q'       not in st.session_state: st.session_state.quick_q       = None
if 'enter_pressed' not in st.session_state: st.session_state.enter_pressed = False

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### 🩺 MediBot")
    st.markdown("---")

    st.markdown("**Response Settings**")
    temperature = 0.4
    max_tokens = 512

    st.markdown("---")
    st.markdown("**Session Stats**")
    st.markdown(f"""
    <div class="metric-row">
        <div class="metric-card">
            <div class="val">{st.session_state.query_count}</div>
            <div class="lbl">Queries</div>
        </div>
        <div class="metric-card">
            <div class="val">{st.session_state.total_tokens:,}</div>
            <div class="lbl">Tokens Used</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    if st.button("🗑️ Clear Conversation", use_container_width=True):
        st.session_state.messages     = []
        st.session_state.history      = []
        st.session_state.total_tokens = 0
        st.session_state.query_count  = 0
        st.session_state.user_input = ""
        st.rerun()
        

    st.markdown("---")
    st.markdown("**Safety Filters Active**")
    st.markdown("""
    <div class="safety-badge">✓ Emergency detection</div><br>
    <div class="safety-badge">✓ Harmful query filter</div><br>
    <div class="safety-badge">✓ Medical scope limits</div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("""
    <p>⚕️ MediBot provides general health information only.
    Always consult a qualified healthcare professional.</p>
    """, unsafe_allow_html=True)

# ── Header ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="medibot-header">
    <div class="medibot-icon">🩺</div>
    <div>
        <h1>MediBot</h1>
        <p>General Health Assistant &nbsp;·&nbsp; LLaMA 3.3 70B via Groq &nbsp;·&nbsp</p>
    </div>
</div>
""", unsafe_allow_html=True)

# ── Quick questions ───────────────────────────────────────────────────────────
st.markdown('<div class="section-label">Quick Questions</div>', unsafe_allow_html=True)
cols = st.columns(len(QUICK_QUESTIONS))
for i, (col, q) in enumerate(zip(cols, QUICK_QUESTIONS)):
    with col:
        if st.button(q, key=f"qq_{i}", use_container_width=True):
            st.session_state.quick_q = q

st.markdown("---")

# ── Chat display ──────────────────────────────────────────────────────────────
chat_html = '<div class="chat-wrapper">'

if not st.session_state.messages:
    chat_html += """
    <div style="text-align:center; padding:40px 20px; color:#4a5568;">
        <div style="font-size:2.5rem; margin-bottom:12px;">👋</div>
        <div style="font-size:1rem; color:#5a6a80;">Ask me any general health question</div>
        <div style="font-size:0.8rem; color:#3a4a5a; margin-top:6px;">or pick one from the quick questions above</div>
    </div>"""
else:
    for msg in st.session_state.messages:
        if msg['role'] == 'user':
            chat_html += f"""
            <div class="msg-user">
                <div style="text-align:right;">
                    <div class="msg-label-user">👤 You</div>
                    <div class="bubble-user">{msg['content']}</div>
                </div>
                <div class="avatar-user">U</div>
            </div>"""
        elif msg['role'] == 'emergency':
            chat_html += """
            <div class="banner-emergency">
                🚨 <strong>This sounds like a medical emergency.</strong><br>
                Please call emergency services immediately:<br>
                🇵🇰 Pakistan: <strong>115</strong> (Rescue) or <strong>1122</strong> (Edhi)<br>
                🌍 International: <strong>112</strong> or your local emergency number<br>
                Do not wait — get professional help right now.
            </div>"""
        elif msg['role'] == 'blocked':
            chat_html += """
            <div class="banner-blocked">
                ⚠️ <strong>I can't help with that request.</strong><br>
                MediBot is designed for general health information only.
                Please consult a qualified healthcare professional.
            </div>"""
        else:
            content = msg['content'].replace('\n', '<br>')
            chat_html += f"""
            <div class="msg-bot">
                <div class="avatar-bot">🩺</div>
                <div>
                    <div class="msg-label-bot">🤖 MediBot</div>
                    <div class="bubble-bot">{content}</div>
                </div>
            </div>"""

chat_html += '</div>'
st.markdown(f'<div class="chat-scroll">{chat_html}</div>', unsafe_allow_html=True)

# ── Input ─────────────────────────────────────────────────────────────────────
st.markdown('<div class="section-label">Your Question</div>', unsafe_allow_html=True)
col_input, col_btn = st.columns([5, 1])

with col_input:
    user_input = st.text_input(
        label="",
        placeholder="e.g. What are the symptoms of anemia?",
        key="user_input",
        label_visibility="collapsed",
        on_change=lambda: st.session_state.update({'enter_pressed': True})
    )

with col_btn:
    send = st.button("Send →", use_container_width=True)

# Enter key or button both trigger send
send = send or st.session_state.enter_pressed
st.session_state.enter_pressed = False

# ── Handle quick question ─────────────────────────────────────────────────────
if st.session_state.quick_q:
    user_input = st.session_state.quick_q
    send = True
    st.session_state.quick_q = None

# ── Process ───────────────────────────────────────────────────────────────────
if send and user_input.strip():
    st.session_state.messages.append({'role': 'user', 'content': user_input.strip()})

    with st.spinner("MediBot is thinking..."):
        try:
            result = chat_with_stats(
                user_input.strip(),
                st.session_state.history.copy(),
                temperature=temperature,
                max_tokens=max_tokens
            )

            status = result['status']

            if status == 'emergency':
                st.session_state.messages.append({'role': 'emergency', 'content': ''})
            elif status == 'blocked':
                st.session_state.messages.append({'role': 'blocked', 'content': ''})
            else:
                st.session_state.history       = result['history']
                st.session_state.messages.append({'role': 'assistant', 'content': result['response']})
                st.session_state.total_tokens += result['total_tokens']
                st.session_state.query_count  += 1
                st.session_state.user_input = ""

        except Exception as e:
            st.error(f"Error: {str(e)}")

    st.rerun()

# ── Disclaimer ────────────────────────────────────────────────────────────────
st.markdown("""
<div class="disclaimer">
    ⚕️ <strong>Disclaimer:</strong> MediBot provides general health information for educational purposes only.
    It is not a substitute for professional medical advice, diagnosis, or treatment.
    Always consult a qualified healthcare professional for medical concerns.
</div>
""", unsafe_allow_html=True)