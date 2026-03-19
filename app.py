import streamlit as st
import streamlit.components.v1 as components
import requests
import os
from dotenv import load_dotenv
from groq import Groq

# ---------------- Load API Keys ----------------
load_dotenv()

# --- Initialize Credits ---
if "credits" not in st.session_state:
    st.session_state.credits = 3000

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
MURF_API_KEY = os.getenv("MURF_API_KEY")

client = Groq(api_key=GROQ_API_KEY)

# ---------------- Page Setup ----------------
st.set_page_config(page_title="AI Voice Assistant", layout="wide")

# ---------------- Theme-Aware Styles ----------------
st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600&display=swap');

html, body, [class*="css"] {
    font-family: 'Outfit', sans-serif;
}

/* --- LIGHT MODE --- */
@media (prefers-color-scheme: light) {
    html, body, [class*="css"], label, p, div, span, small {
        color: #0f172a !important;
    }
    
    [data-testid="stAppViewContainer"] {
        background: radial-gradient(circle at top center, #e0e7ff 0%, #f1f5f9 100%) !important;
    }
    
    [data-testid="stForm"] {
        background: rgba(226, 232, 240, 0.5) !important;
        border: 1px solid rgba(71, 85, 105, 0.2) !important;
        box-shadow: 0 20px 40px -10px rgba(0, 0, 0, 0.05) !important;
    }
    
    [data-testid="stSidebar"] {
        background: rgba(241, 245, 249, 0.9) !important;
        border-right: 1px solid rgba(71, 85, 105, 0.1) !important;
    }
    
    .sidebar-heading { color: #1e1b4b !important; text-shadow: none !important; }
    
    .credit-box {
        background: #f1f5f9 !important;
        border: 1px solid #cbd5e1 !important;
        box-shadow: 0 4px 12px rgba(0,0,0,0.03) !important;
    }
    
    .credit-box p { color: #111827 !important; }
    
    .stTextInput input {
        color: #1e293b !important;
        background-color: #e2e8f0 !important;
        border: 1px solid #cbd5e1 !important;
    }

    [data-testid="stSegmentedControl"] {
        background: #cbd5e1 !important;
        border: 1px solid #94a3b8 !important;
    }
    
    [data-testid="stSegmentedControl"] button {
        color: #1e293b !important;
    }
    
    [data-testid="stSelectbox"] div[role="button"] {
        background-color: #e2e8f0 !important;
        border: 1px solid #cbd5e1 !important;
        color: #1e293b !important;
    }
    
    [data-testid="stSelectbox"] div[role="button"] div { color: #1e293b !important; }
}

/* --- DARK MODE / GLOBAL DEFAULTS --- */
html, body, [class*="css"], label, p, div, span, small {
    color: #e2e8f0 !important;
}

h1, h2, h3 {
    background: linear-gradient(135deg, #f8fafc 0%, #c084fc 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent ;
    font-weight: 600 !important;
}

.footer {
position: fixed;
bottom: 0;
left: 0;
width: 100%;
background: rgba(15, 23, 42, 0.95);
color: #e2e8f0;
text-align: center;
padding: 12px;
font-size: 14px;
border-top: 1px solid rgba(139, 92, 246, 0.3);
z-index: 999;
backdrop-filter: blur(15px);
}

.footer b { color: #c084fc; }
.footer a { color:#60a5fa; text-decoration:none; margin:0 10px; font-weight: 600; }
.footer a:hover { color: #fb7185; text-decoration:underline; }

[data-testid="stAppViewContainer"] {
    background: radial-gradient(circle at top center, #1e1b4b 0%, #030712 100%) !important;
}

[data-testid="stHeader"] { background: transparent !important; }

[data-testid="stForm"] {
    background: rgba(30, 41, 59, 0.3) !important;
    border-radius: 28px !important;
    padding: 50px !important;
    border: 1px solid rgba(139, 92, 246, 0.3) !important;
    box-shadow: 0 30px 60px -12px rgba(0, 0, 0, 0.7) !important;
    backdrop-filter: blur(25px) !important;
    width: 95% !important;
    margin: 0 auto 60px auto !important;
}

div.stButton > button {
    background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%) !important;
    color: #f8fafc !important;
    border: none !important;
    border-radius: 12px !important;
    padding: 12px 30px !important;
    font-weight: 600 !important;
    box-shadow: 0 4px 15px rgba(139, 92, 246, 0.4) !important;
    transition: all 0.3s ease !important;
    width: 100% !important;
}

div.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 6px 20px rgba(139, 92, 246, 0.6) !important;
    filter: brightness(1.1) !important;
}

div[data-testid="stSelectbox"] div[role="button"] {
    background-color: rgba(255, 255, 255, 0.05) !important;
    border: 1px solid rgba(139, 92, 246, 0.3) !important;
    border-radius: 12px !important;
    color: #e2e8f0 !important;
}

div[data-testid="stSelectbox"] div[role="button"] div { color: #e2e8f0 !important; }

[data-testid="stSegmentedControl"] {
    background: rgba(0, 0, 0, 0.4) !important;
    border-radius: 12px !important;
    padding: 4px !important;
    border: 1px solid rgba(139, 92, 246, 0.1) !important;
}

[data-testid="stSegmentedControl"] button {
    color: #94a3b8 !important;
    background: transparent !important;
    border-radius: 8px !important;
    padding: 8px 15px !important;
    border: none !important;
}

[data-testid="stSegmentedControl"] button[aria-checked="true"] {
    background: #8b5cf6 !important;
    color: #f8fafc !important;
    box-shadow: 0 0 15px rgba(139, 92, 246, 0.4) !important;
}

.stTextInput input {
    color: #f8fafc !important;
    background-color: rgba(255, 255, 255, 0.05) !important;
    border: 1px solid rgba(139, 92, 246, 0.2) !important;
    border-radius: 14px !important;
    padding: 15px !important;
    font-size: 1.2rem !important;
    margin-bottom: 20px !important;
}

.stTextInput input::placeholder { color: #64748b !important; opacity: 0.7 !important; }
.stTextInput input:focus { border-color: #c084fc !important; box-shadow: 0 0 20px rgba(139, 92, 246, 0.4) !important; }

[data-testid="stSidebar"] {
    background: rgba(15, 23, 42, 0.7) !important;
    backdrop-filter: blur(25px) !important;
    border-right: 1px solid rgba(139, 92, 246, 0.2) !important;
}

.sidebar-heading {
    color: #f8fafc;
    font-size: 1.4rem;
    font-weight: 700;
    margin-bottom: 25px;
    letter-spacing: 1px;
    text-shadow: 0 0 10px rgba(192, 132, 252, 0.3);
}

.credit-box {
    background: linear-gradient(135deg, rgba(139, 92, 246, 0.15), rgba(30, 41, 59, 0.3));
    border-radius: 20px;
    padding: 25px;
    border: 1px solid rgba(139, 92, 246, 0.3);
    margin-top: 25px;
    box-shadow: 0 10px 40px 0 rgba(0, 0, 0, 0.5);
}

.credit-box h4 { color: #e2e8f0 !important; font-size: 0.8rem; margin: 0 0 12px 0; text-transform: uppercase; letter-spacing: 2px; }
.credit-box p { color: #f8fafc !important; font-size: 1.6rem; font-weight: 800; margin: 0 0 15px 0; }

.token-container { background: rgba(0, 0, 0, 0.7); height: 14px; border-radius: 7px; width: 100%; border: 1px solid rgba(255, 255, 255, 0.1); overflow: hidden; position: relative; }
.token-bar {
    height: 100%;
    background: linear-gradient(90deg, #818cf8 0%, #c084fc 50%, #f472b6 100%);
    box-shadow: 0 0 20px rgba(192, 132, 252, 0.6);
    border-radius: 7px;
    transition: width 0.8s cubic-bezier(0.16, 1, 0.3, 1);
}

</style>
""", unsafe_allow_html=True)

# ---------------- Sidebar Navbar ----------------
def render_credit_box():
    # Calculate percentage for progress bar (max 3000)
    credits_pct = max(0, min(100, (st.session_state.credits / 3000) * 100))
    
    return f"""
    <div class="credit-box">
        <h4>User Balance</h4>
        <p>{st.session_state.credits:,} Tokens</p>
        <div class="token-container">
            <div class="token-bar" style="width: {credits_pct}%;"></div>
        </div>
    </div>
    """

with st.sidebar:
    st.markdown("### 🎙️ Voice Agents")
    st.markdown("---")
    
    # Murf Voice Selection in Sidebar
    voice_options = {
        "Natalie": "en-US-natalie",
        "Miles": "en-US-miles",
        "Sarah": "en-UK-sarah",
        "Marcus": "en-US-marcus",
        "Cooper": "en-US-cooper"
    }
    
    selected_voice_name = st.selectbox(
        "🎧 Select Voice Agent",
        options=list(voice_options.keys()),
        index=0
    )
    selected_voice_id = voice_options[selected_voice_name]
    
    st.write("---")
    
    # Response Size Toggle in Sidebar
    response_size = st.segmented_control(
        "📏 Response Detail", 
        options=["Small", "Medium", "Large"], 
        default="Medium",
        selection_mode="single"
    )
    
    st.markdown("---")
    st.markdown('<div class="sidebar-heading">👤 User Account</div>', unsafe_allow_html=True)
    
    # Placeholder for real-time updates
    credit_placeholder = st.empty()
    credit_placeholder.markdown(render_credit_box(), unsafe_allow_html=True)

# ---------------- Animated Voice UI ----------------
with st.container():
    components.html("""
<!DOCTYPE html>
<html>
<head>
<style>
body, html {
margin:0;
padding:0;
width:100%;
height:100%;
background-color:transparent;
display:flex;
flex-direction:column;
align-items:center;
justify-content:center;
font-family:'Segoe UI',sans-serif;
overflow:hidden;
}

h1{
color:white;
font-weight:300;
font-size:2.8rem;
margin-bottom:50px;
letter-spacing:2px;
opacity:0.95;
text-shadow: 0 0 20px rgba(139, 92, 246, 0.4);
}

canvas{
position:absolute;
bottom:20%;
left:0;
width:100%;
height:200px;
}
</style>
</head>

<body>

<h1>What can I help you with?</h1>

<canvas id="waveCanvas"></canvas>

<script>

const canvas = document.getElementById('waveCanvas');
const ctx = canvas.getContext('2d');

let width,height,amplitude,frequency,speed;
let step = 0;

function resize(){
width = canvas.width = window.innerWidth;
height = canvas.height = 200;
amplitude = 40;
frequency = 0.01;
speed = 0.05;
}

window.addEventListener('resize',resize);
resize();

function drawWave(color,opacity,offset,speedModifier){
ctx.beginPath();
ctx.lineWidth = 2;
ctx.strokeStyle = color;
ctx.globalAlpha = opacity;

for(let x=0;x<width;x++){

const y = height/2 +
Math.sin(x*frequency + step*speedModifier + offset)
* amplitude * Math.sin(step*0.02);

if(x===0){ctx.moveTo(x,y);}
else{ctx.lineTo(x,y);}

}

ctx.stroke();
}

function animate(){
ctx.clearRect(0,0,width,height);

drawWave('#8b5cf6',0.8,0,1);
drawWave('#6366f1',0.5,2,0.8);
drawWave('#d946ef',0.3,4,1.2);

step += speed;
requestAnimationFrame(animate);
}

animate();

</script>

</body>
</html>
""", height=350)

# ---------------- Input Form ----------------
with st.form("question_form"):
    question = st.text_input("Ask your AI assistant...")
    
    submitted = st.form_submit_button("Ask AI")

# ---------------- AI + Voice ----------------
if submitted and question:

    if st.session_state.credits <= 0:
        st.error("Insufficient tokens! Please top up.")
        st.stop()

    # Define character limits and guidance
    size_guidance = {
        "Small": "Provide a very brief response (approx. 1-2 short sentences). Keep it simple and punchy.",
        "Medium": "Provide a concise but informative response (approx. 60-100 words). Stick to the core points.",
        "Large": "Provide a detailed and comprehensive response (approx. 200-300 words). Elaborate and offer depth."
    }
    
    size_limits = {
        "Small": 300,
        "Medium": 1000,
        "Large": 3000
    }

    # Ensure a selection
    if not response_size: response_size = "Medium"

    with st.spinner("Thinking..."):

        chat = client.chat.completions.create(
            messages=[
                {"role": "system", "content": f"You are a helpful AI assistant. {size_guidance[response_size]}"},
                {"role": "user", "content": question}
            ],
            model="llama-3.1-8b-instant"
        )

        answer = chat.choices[0].message.content[:size_limits[response_size]]
        
        # -- Real-time credit deduction ---
        tokens_used = len(answer)
        st.session_state.credits = max(0, st.session_state.credits - tokens_used)
        credit_placeholder.markdown(render_credit_box(), unsafe_allow_html=True)

    st.write("### 🤖 AI Response")
    st.write(answer)


    # ---------------- Murf Voice Generation ----------------

    url = "https://api.murf.ai/v1/speech/generate"

    payload = {
        "text": answer,
        "voiceId": selected_voice_id,
        "format": "mp3"
    }

    headers = {
        "api-key": MURF_API_KEY,
        "Content-Type": "application/json"
    }

    audio_url = None

    status = st.status("🔊 Generating AI voice...", expanded=False)

    for attempt in range(3):

        try:
            res = requests.post(url,json=payload,headers=headers)

            if res.status_code == 200:
                audio_url = res.json()["audioFile"]
                break

        except:
            pass

    if audio_url:

        status.update(label="✅ Voice generated successfully", state="complete")
        st.audio(audio_url)
        
        # Deduct remaining tokens for voice processing
        voice_processing_fee = 200
        st.session_state.credits = max(0, st.session_state.credits - voice_processing_fee)
        credit_placeholder.markdown(render_credit_box(), unsafe_allow_html=True)

    else:

        status.update(label="⚠ Voice generation failed", state="error")

# ---------------- Footer ----------------
st.markdown("""
<div class="footer">
Built by <b>Team Delta</b> | B.Tech Students |
<a href="https://github.com/harshadev1428" target="_blank">GitHub</a>
<a href="https://linkedin.com/in/harsha-d-9aba27372" target="_blank">LinkedIn</a>
<a href="mailto:hharshadev2006@gmail.com">Email</a>
<br>
© 2026 AI Voice Assistance
</div>
""", unsafe_allow_html=True)
