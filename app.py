from datetime import datetime
import streamlit as st
st.set_page_config(page_title="SamtalsBot", layout="wide")

# Tvinga rätt färger i expanders och body med theme-variabler
st.markdown(
    """
    <style>
      .streamlit-expanderContent {
        color: #FAFAFA !important;
        background-color: var(--secondaryBackgroundColor) !important;
      }
      .block-container {
        background-color: var(--backgroundColor);
      }
    </style>
    """,
    unsafe_allow_html=True
)

import os
from transcription import Transcriber
from analysis import ConversationAnalyzer

# Endast accentfärg på expanderHeader, ingen textfärg eller bakgrund
st.markdown(
    """
    <style>
      .streamlit-expanderHeader { color: #E91E63 !important; }
    </style>
    """,
    unsafe_allow_html=True
)

# Försök importera AudioRecorder, annars mock
try:
    from audio_capture import AudioRecorder
    LOCAL_RECORDING = True
except ImportError:
    LOCAL_RECORDING = False
    class AudioRecorder:
        def __init__(self, *args, **kwargs):
            raise RuntimeError("Local recording inte tillgängligt i molnet. Välj \"Upload audio file\" istället.")

# --- Ta bort sidomeny och flytta input till huvudflödet ---
input_method = st.selectbox(
    "Välj inmatningsmetod:",
    options=["Upload audio file"]
)

audio_path = None
if input_method.startswith("Upload"):
    uploaded = st.file_uploader("Ladda upp ljudfil (wav/mp3)", type=["wav","mp3"])
    if uploaded is not None:
        # Spara temporärt
        temp_file = os.path.join("/tmp", uploaded.name)
        with open(temp_file, "wb") as f:
            f.write(uploaded.getbuffer())
        audio_path = temp_file
elif input_method.startswith("Local recording") and LOCAL_RECORDING:
    duration = st.sidebar.slider("Spela in i sekunder", min_value=5, max_value=120, value=30)
    if st.sidebar.button("Starta inspelning"):
        st.sidebar.info("Inspelning pågår... vänta tills klar")
        recorder = AudioRecorder()
        thread = recorder.start_recording(filename="/tmp/recording.wav", duration=duration)
        thread.join()
        st.sidebar.success("Inspelning klar!")
        audio_path = "/tmp/recording.wav"

# När vi har en ljudfil: transkribera och analysera
if audio_path:
    st.subheader("Förslag enligt samtalsmodellen")
    transcriber = Transcriber()
    with st.spinner("Transkriberar..."):
        transcript = transcriber.transcribe(audio_path)

    # Dölj transkriptet i en expander
    with st.expander("Visa transkription", expanded=False):
        st.text_area("Transcript:", transcript, height=200)

    analyzer = ConversationAnalyzer()
    with st.spinner("Analyserar enligt samtalsmodellens fyra faser..."):
        analysis = analyzer.analyze(transcript)

    # Visa varje fas i en egen expander
    for phase, content in analysis.items():
        with st.expander(phase, expanded=False):
            st.write(content)

    # TTS-knappen kommenteras ut tills implementation finns
    # if st.button("Spela upp hela analysen med TTS"):
    #     from tts import speak
    #     speak("\n\n".join(analysis.values()))
else:
    st.info("Välj en inmatningsmetod och ladda upp eller spela in ljud för analys.")

# --- Färgtema (Lunds kommun-inspirerat) ---
PRIMARY_COLOR = "#6A226A"
ACCENT_COLOR = "#B57EB6"

# --- Custom CSS för mörkt tema och accentfärger ---
st.markdown(f"""
    <style>
    .main-header {{
        background: {PRIMARY_COLOR};
        color: white;
        padding: 1.5rem 2rem 1rem 2rem;
        border-radius: 0 0 16px 16px;
        margin-bottom: 2rem;
    }}
    .gdpr-box {{
        background: #222;
        border-left: 6px solid {PRIMARY_COLOR};
        color: #FAFAFA;
        padding: 1rem 1.5rem;
        margin-bottom: 1.5rem;
        border-radius: 8px;
    }}
    .step-box {{
        background: #18191A;
        border: 1px solid #333;
        border-radius: 10px;
        color: #FAFAFA;
        padding: 2rem 2rem 1.5rem 2rem;
        margin-bottom: 2rem;
        box-shadow: 0 2px 8px #0003;
    }}
    .footer-gdpr {{
        color: #AAA;
        font-size: 0.9rem;
        margin-top: 2rem;
        border-top: 1px solid #333;
        padding-top: 1rem;
    }}
    .stButton>button {{
        background: {PRIMARY_COLOR};
        color: white;
        border-radius: 6px;
        border: none;
        font-weight: bold;
        padding: 0.6rem 1.5rem;
        margin: 0.2rem 0.5rem 0.2rem 0;
    }}
    .stButton>button:disabled {{
        background: #444;
        color: #888;
    }}
    .streamlit-expanderContent {{
        color: #FAFAFA !important;
        background-color: #18191A !important;
    }}
    .streamlit-expanderHeader {{
        color: {ACCENT_COLOR} !important;
    }}
    </style>
""", unsafe_allow_html=True)

# --- Byt ut header-boxen mot enkel rubrik ---
st.markdown(f"""
<div style='font-size:2.2rem;font-weight:bold;margin-bottom:2rem;'>
AI-driven samtalsassistent för Lunds kommun
</div>
""", unsafe_allow_html=True)

# --- Ta bort GDPR-knappen, visa bara info och gå vidare automatiskt ---
gdpr_accepted = st.session_state.get("gdpr_accepted", False)
if not gdpr_accepted:
    st.markdown(f"""
    <div class="gdpr-box">
        <b>GDPR & Dataskydd</b><br>
        Denna app hanterar ljud och textdata för samtalsanalys. All data raderas automatiskt efter analys. Genom att fortsätta godkänner du att data kan skickas till OpenAI (USA) för språkmodellanalys. <br><br>
        <i>Ingen data sparas på servern. Allt sker temporärt och anonymiserat.</i>
    </div>
    """, unsafe_allow_html=True)
    st.session_state["gdpr_accepted"] = True
    st.rerun()

# --- Steg 1: Ljudinspelning eller uppladdning ---
st.markdown(f"<div class='step-box'><h3>1. Spela in eller ladda upp samtal</h3>", unsafe_allow_html=True)
col1, col2 = st.columns(2)
with col1:
    if LOCAL_RECORDING:
        if st.button("🎤 Starta inspelning", key="start_rec"):
            st.session_state["recording"] = True
            st.session_state["recorder"] = AudioRecorder()
            st.session_state["thread"] = st.session_state["recorder"].start_recording(filename="temp_recording.wav")
            st.success("Inspelning pågår... Klicka 'Stoppa inspelning' när du är klar.")
        if st.button("⏹️ Stoppa inspelning", key="stop_rec") and st.session_state.get("recording", False):
            st.session_state["recording"] = False
            st.session_state["recorder"].stop_recording()
            st.success("Inspelning klar!")
    else:
        st.info("Ljudinspelning är inte tillgänglig i denna miljö. Ladda upp en WAV-fil istället.")

with col2:
    uploaded_file = st.file_uploader("Eller ladda upp en WAV-fil", type=["wav"])
    if uploaded_file:
        with open("temp_recording.wav", "wb") as f:
            f.write(uploaded_file.read())
        st.success("Ljudfil uppladdad!")

st.markdown("</div>", unsafe_allow_html=True)

# --- Steg 2: Transkribering och anonymisering ---
if os.path.exists("temp_recording.wav"):
    st.markdown(f"<div class='step-box'><h3>2. Transkribera och anonymisera</h3>", unsafe_allow_html=True)
    if st.button("Transkribera samtal"):
        with st.spinner("Transkriberar ljudet..."):
            transcriber = Transcriber(model_name="small")
            transcript = transcriber.transcribe("temp_recording.wav")
            st.session_state["transcript"] = transcript
        st.success("Transkription klar!")
    if "transcript" in st.session_state:
        st.subheader("Transkript")
        st.write(st.session_state["transcript"])
        # Anonymisering (valfritt)
        anonymize = st.checkbox("Anonymisera transkript (ta bort namn och känsliga ord)")
        if anonymize:
            import re
            anonymized = re.sub(r"\b([A-ZÅÄÖ][a-zåäö]+)\b", "[ANONYM]", st.session_state["transcript"])
            st.session_state["transcript"] = anonymized
            st.info("Transkriptet är nu anonymiserat.")
    st.markdown("</div>", unsafe_allow_html=True)

# --- Steg 3: Analys ---
if "transcript" in st.session_state:
    st.markdown(f"<div class='step-box'><h3>3. Analys av samtalet</h3>", unsafe_allow_html=True)
    if st.button("Analysera samtal"):
        with st.spinner("Analyserar samtalet med AI..."):
            analyzer = ConversationAnalyzer()
            analysis = analyzer.analyze(st.session_state["transcript"])
            st.session_state["analysis"] = analysis["analysis"]
        st.success("Analys klar!")
    if "analysis" in st.session_state:
        st.subheader("Analys")
        st.write(st.session_state["analysis"])
        # Ladda ner rapport
        st.download_button(
            label="Ladda ner rapport som text",
            data=st.session_state["analysis"],
            file_name=f"samtalsanalys_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
            mime="text/plain"
        )
    st.markdown("</div>", unsafe_allow_html=True)

# --- Automatisk radering av temporära filer ---
if os.path.exists("temp_recording.wav") and "analysis" in st.session_state:
    try:
        os.remove("temp_recording.wav")
    except Exception:
        pass

# --- Footer med GDPR-info ---
st.markdown(f"""
<div class="footer-gdpr">
    <b>GDPR & Dataskydd:</b> Ingen data sparas på servern. Allt raderas automatiskt efter analys. <br>
    <i>SamtalsBot för Lunds kommun &copy; {datetime.now().year}</i>
</div>
""", unsafe_allow_html=True) 