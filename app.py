import os
import html
import tempfile
import streamlit as st

from modules.transcription import transcribe_audio
from modules.scam_analysis import analyze_transcript

# =====================================================
# STEP 1: PAGE CONFIGURATION
# =====================================================

st.set_page_config(
    page_title="AWAaz SHIELD | AI Security",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =====================================================
# STEP 2: CUSTOM DESIGN (CSS + ANIMATED BACKGROUND)
# =====================================================

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

/* ---------- BACKGROUND: glows + grid + base ---------- */
.stApp {
    color: #edf4ff;
    font-family: 'Inter', sans-serif;
    background:
        radial-gradient(circle at 85% 8%, rgba(22, 185, 202, 0.22), transparent 40%),
        radial-gradient(circle at 10% 90%, rgba(22, 125, 206, 0.20), transparent 45%),
        linear-gradient(rgba(80, 216, 233, 0.045) 1px, transparent 1px),
        linear-gradient(90deg, rgba(80, 216, 233, 0.045) 1px, transparent 1px),
        linear-gradient(160deg, #060a14 0%, #0a1224 50%, #07101d 100%);
    background-size: auto, auto, 46px 46px, 46px 46px, auto;
    background-attachment: fixed;
}

/* ---------- BACKGROUND: sound-wave strip ---------- */
.stApp::before {
    content: "";
    position: fixed;
    left: 0; right: 0; bottom: 0;
    height: 140px;
    pointer-events: none;
    z-index: 0;
    opacity: 0.35;
    background: repeating-linear-gradient(
        90deg,
        rgba(80, 216, 233, 0.55) 0px, rgba(80, 216, 233, 0.55) 3px,
        transparent 3px, transparent 14px
    );
    -webkit-mask-image: linear-gradient(to top, black, transparent);
            mask-image: linear-gradient(to top, black, transparent);
    transform-origin: bottom;
    animation: pulseWave 4s ease-in-out infinite;
}

@keyframes pulseWave {
    0%, 100% { opacity: 0.18; transform: scaleY(0.85); }
    50%      { opacity: 0.40; transform: scaleY(1.05); }
}

/* ---------- BACKGROUND: scanner line ---------- */
.stApp::after {
    content: "";
    position: fixed;
    left: 0; right: 0; top: -2px;
    height: 2px;
    pointer-events: none;
    z-index: 0;
    background: linear-gradient(90deg, transparent, rgba(80, 216, 233, 0.5), transparent);
    animation: scan 9s linear infinite;
}

@keyframes scan {
    from { top: -2px; }
    to   { top: 100vh; }
}

/* ---------- BACKGROUND: aurora blobs ---------- */
.aurora {
    position: fixed; inset: 0;
    z-index: 0; pointer-events: none; overflow: hidden;
}
.aurora b {
    position: absolute; border-radius: 50%;
    filter: blur(90px); opacity: 0.35;
    animation: drift 18s ease-in-out infinite alternate;
}
.aurora b:nth-child(1) { width: 520px; height: 520px; left: -120px; top: -100px; background: #167dce; }
.aurora b:nth-child(2) { width: 460px; height: 460px; right: -100px; top: 20%; background: #16b9ca; animation-duration: 23s; }
.aurora b:nth-child(3) { width: 420px; height: 420px; left: 35%; bottom: -180px; background: #5b3fd0; opacity: 0.25; animation-duration: 27s; }

@keyframes drift {
    from { transform: translate(0, 0) scale(1); }
    to   { transform: translate(60px, 40px) scale(1.18); }
}

/* ---------- BACKGROUND: hologram shield + radar ---------- */
.holo {
    position: fixed; right: 6%; top: 50%;
    width: min(520px, 60vw); margin-top: -260px;
    z-index: 0; pointer-events: none; opacity: 0.18;
}
.holo .r1    { transform-origin: 260px 260px; animation: spin 40s linear infinite; }
.holo .r2    { transform-origin: 260px 260px; animation: spin 26s linear infinite reverse; }
.holo .sweep { transform-origin: 260px 260px; animation: spin 7s linear infinite; }
@keyframes spin { to { transform: rotate(360deg); } }

@media (prefers-reduced-motion: reduce) {
    .stApp::before, .stApp::after, .aurora b, .holo g { animation: none; }
}

/* ---------- LAYOUT ---------- */
header[data-testid="stHeader"] { background: transparent; }

[data-testid="stSidebar"] {
    background: rgba(13, 20, 35, 0.92);
    border-right: 1px solid #1c2940;
}
[data-testid="stSidebar"] * { color: #dce7f8; }

.block-container {
    position: relative;
    z-index: 1;
    padding-top: 2rem;
    padding-bottom: 3rem;
    max-width: 1450px;
}

/* ---------- COMPONENTS ---------- */
.hero {
    background:
        radial-gradient(circle at 90% 20%, rgba(75, 216, 232, 0.18), transparent 45%),
        linear-gradient(120deg, rgba(17, 29, 53, 0.9), rgba(16, 44, 67, 0.9), rgba(23, 32, 59, 0.9));
    border: 1px solid #263d5c;
    border-radius: 22px;
    padding: 35px;
    margin-bottom: 25px;
    box-shadow: 0 0 40px rgba(22, 185, 202, 0.10);
}
.eyebrow { color: #50d8e9; font-size: 12px; font-weight: 800; letter-spacing: 3px; text-transform: uppercase; }
.hero h1 { color: #ffffff; font-size: clamp(32px, 4vw, 48px); font-weight: 800; margin: 12px 0; }
.hero p  { color: #a9bad3; font-size: 15px; line-height: 1.8; max-width: 700px; }

.badge {
    display: inline-block;
    background: #102d36; border: 1px solid #1d5963; color: #65e8dc;
    border-radius: 30px; padding: 8px 13px; font-size: 12px; margin-bottom: 10px;
}

.section-title    { color: #f2f6ff; font-size: 21px; font-weight: 750; margin: 15px 0 6px 0; }
.section-subtitle { color: #8fa3bf; font-size: 13px; margin-bottom: 20px; }

.panel {
    background: rgba(14, 22, 38, 0.60);
    backdrop-filter: blur(10px);
    -webkit-backdrop-filter: blur(10px);
    border: 1px solid rgba(80, 216, 233, 0.16);
    border-radius: 17px;
    padding: 22px;
    margin-bottom: 15px;
    box-shadow: 0 8px 30px rgba(0, 0, 0, 0.35);
}
.panel-title { color: #eaf2ff; font-size: 16px; font-weight: 700; margin-bottom: 8px; }
.muted       { color: #91a4bf; font-size: 13px; line-height: 1.7; }

.metric-card {
    background: rgba(14, 22, 38, 0.60);
    backdrop-filter: blur(10px);
    -webkit-backdrop-filter: blur(10px);
    border: 1px solid rgba(80, 216, 233, 0.16);
    border-radius: 15px;
    padding: 19px;
    min-height: 112px;
    box-shadow: 0 8px 30px rgba(0, 0, 0, 0.35);
}
.metric-label { color: #91a4bf; font-size: 12px; margin-bottom: 12px; }
.metric-value { color: #ffffff; font-size: 25px; font-weight: 800; }

div[data-testid="stFileUploader"] {
    background: rgba(16, 25, 41, 0.65);
    border: 1px dashed #3a577a;
    border-radius: 15px;
    padding: 18px;
}
div[data-testid="stFileUploader"] section { background: transparent; }

.stButton > button {
    background: linear-gradient(100deg, #167dce, #16b9ca);
    color: white; border: none; border-radius: 10px;
    padding: 12px 20px; font-weight: 700; width: 100%; min-height: 48px;
}
.stButton > button:hover { border: 1px solid #64e7f0; color: white; filter: brightness(1.12); }

div[data-testid="stAudio"] { margin: 10px 0 20px 0; }
hr { border-color: #24334b; }

.footer { color: #657994; text-align: center; font-size: 12px; padding: 30px 0 5px 0; }
</style>

<div class="aurora"><b></b><b></b><b></b></div>

<svg class="holo" viewBox="0 0 520 520" aria-hidden="true">
  <defs>
    <linearGradient id="sg" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="#50d8e9"/><stop offset="1" stop-color="#167dce"/>
    </linearGradient>
    <radialGradient id="sw">
      <stop offset="0" stop-color="#50d8e9" stop-opacity="0"/>
      <stop offset="1" stop-color="#50d8e9" stop-opacity="0.55"/>
    </radialGradient>
  </defs>
  <g class="r1" fill="none" stroke="#50d8e9" stroke-width="1.5" stroke-dasharray="4 10"><circle cx="260" cy="260" r="250"/></g>
  <g class="r2" fill="none" stroke="#167dce" stroke-width="2" stroke-dasharray="40 18 6 18"><circle cx="260" cy="260" r="215"/></g>
  <g fill="none" stroke="#50d8e9" stroke-width="1" opacity="0.6"><circle cx="260" cy="260" r="170"/><circle cx="260" cy="260" r="120"/></g>
  <g class="sweep"><path d="M260 260 L260 10 A250 250 0 0 1 430 80 Z" fill="url(#sw)"/></g>
  <path d="M260 120 L360 160 V260 C360 322 317 366 260 392 C203 366 160 322 160 260 V160 Z"
        fill="rgba(80,216,233,0.06)" stroke="url(#sg)" stroke-width="4"/>
  <path d="M205 262 h18 l10 -38 l18 78 l14 -56 l10 16 h26"
        fill="none" stroke="#50d8e9" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/>
</svg>
""", unsafe_allow_html=True)


# =====================================================
# STEP 3: SIDEBAR
# =====================================================

with st.sidebar:
    st.markdown("""
    <div style="padding:12px 0 25px 0">
        <div style="font-size:34px">🛡️</div>
        <div style="font-size:22px;font-weight:800;color:white">
            AWAaz <span style="color:#43d7e8">SHIELD</span>
        </div>
        <div style="font-size:11px;color:#8fa3bf;letter-spacing:2px">
            VOICE SECURITY PLATFORM
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### 🧭 Navigation")
    st.markdown("🔹  Voice Analysis")
    st.markdown("🔹  Security Center")
    st.markdown("🔹  Safety Guidelines")

    st.markdown("---")
    st.markdown("### 🛡️ Protection Status")
    st.success("Analysis system ready")

    st.markdown("""
    <div style="font-size:12px;color:#8fa3bf;line-height:1.8">
        <b>Current capabilities</b><br>
        • Audio transcription<br>
        • Scam warning indicators<br>
        • Safety recommendations
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    st.caption("AWAaz SHIELD · Student Project")


# =====================================================
# STEP 4: PAGE STATE (which page is showing)
# =====================================================

if "page" not in st.session_state:
    st.session_state.page = "upload"      # "upload" or "results"

if "result" not in st.session_state:
    st.session_state.result = None


def new_analysis():
    """Clear the saved result and go back to the upload page."""
    st.session_state.result = None
    st.session_state.page = "upload"


# =====================================================
# STEP 5: PAGE 1 - UPLOAD
# =====================================================

if st.session_state.page == "upload":

    # ---------- Hero ----------
    st.markdown("""
    <div class="hero">
        <div class="badge">● AI-ASSISTED VOICE SECURITY</div>
        <div class="eyebrow">VOICE THREAT INTELLIGENCE</div>
        <h1>Every Voice Has a Story.<br>
        <span style="color:#4bd8e8">Verify Before You Trust.</span></h1>
        <p>
            Analyze voice recordings for potential scam warning signs.
            Transcribe audio, inspect suspicious language, and discover
            practical steps to protect yourself from voice-based fraud.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # ---------- Metrics ----------
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-label">🎙️ INPUT TYPE</div>
            <div class="metric-value" style="font-size:20px">Voice Audio</div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-label">🧠 ANALYSIS ENGINE</div>
            <div class="metric-value" style="font-size:20px">Whisper + Rules</div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-label">🔐 SECURITY MODE</div>
            <div class="metric-value" style="font-size:20px">Risk Indicators</div>
        </div>
        """, unsafe_allow_html=True)

    # ---------- Upload area ----------
    st.markdown('<div class="section-title">🎧 Voice Analysis Center</div>',
                unsafe_allow_html=True)
    st.markdown("""
    <div class="section-subtitle">
    Upload a recording to begin your security analysis.
    </div>
    """, unsafe_allow_html=True)

    left, right = st.columns([1.15, 0.85], gap="large")

    with left:
        st.markdown("""
        <div class="panel">
            <div class="panel-title">📂 Upload Audio Recording</div>
            <div class="muted">
                Supported formats: WAV, MP3, M4A and OGG.
                Choose a recording and start the analysis.
            </div>
        </div>
        """, unsafe_allow_html=True)

        uploaded_file = st.file_uploader(
            "Choose your audio file",
            type=["wav", "mp3", "m4a", "ogg"],
            key="audio_upload"
        )

        if uploaded_file:
            st.audio(uploaded_file)

        analyze_button = st.button(
            "🔍  Analyze Voice Recording",
            use_container_width=True,
            disabled=uploaded_file is None
        )

    with right:
        st.markdown("""
        <div class="panel">
            <div class="panel-title">⚙️ Analysis Pipeline</div>
            <p class="muted">01 &nbsp; Audio ingestion</p>
            <p class="muted">02 &nbsp; Speech-to-text transcription</p>
            <p class="muted">03 &nbsp; Scam warning phrase analysis</p>
            <p class="muted">04 &nbsp; Safety recommendations</p>
            <hr>
            <div class="muted">
                Each stage contributes information to help you
                assess the recording. Results are preliminary.
            </div>
        </div>
        """, unsafe_allow_html=True)

    # ---------- Run analysis, then open the results page ----------
    if analyze_button and uploaded_file:
        temp_path = None
        success = False

        try:
            suffix = os.path.splitext(uploaded_file.name)[1]

            with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as temp_file:
                temp_file.write(uploaded_file.getvalue())
                temp_path = temp_file.name

            with st.spinner("🎧 Transcribing audio and examining warning signs..."):
                transcript, language = transcribe_audio(temp_path)
                findings = analyze_transcript(transcript or "")

            # Save everything the results page needs
            st.session_state.result = {
                "filename": uploaded_file.name,
                "audio_bytes": uploaded_file.getvalue(),
                "transcript": transcript,
                "language": language,
                "findings": findings,
            }
            success = True

        except Exception as error:
            st.error("Analysis failed. Please check the terminal for details.")
            print(f"Analysis error: {error}")

        finally:
            if temp_path and os.path.exists(temp_path):
                os.remove(temp_path)

        if success:
            st.session_state.page = "results"
            try:
                st.rerun()
            except AttributeError:
                st.experimental_rerun()     # for older Streamlit versions     # for older Streamlit versions


# =====================================================
# STEP 6: PAGE 2 - RESULTS
# =====================================================

else:
    result = st.session_state.result

    # Safety net: no data means go back to the upload page
    if result is None:
        new_analysis()
        st.rerun()

    transcript = result["transcript"]
    language = result["language"]
    findings = result["findings"]

    # ---------- Header ----------
    st.markdown(f"""
    <div class="hero">
        <div class="badge">● ANALYSIS COMPLETE</div>
        <div class="eyebrow">SECURITY REPORT</div>
        <h1>Voice Analysis <span style="color:#4bd8e8">Report</span></h1>
        <p>File analysed: <b>{html.escape(result["filename"])}</b></p>
    </div>
    """, unsafe_allow_html=True)

    st.button("⬅️  Analyze another recording", on_click=new_analysis, key="back_top")

    # ---------- Summary cards ----------
    m1, m2, m3 = st.columns(3)

    with m1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">DETECTED LANGUAGE</div>
            <div class="metric-value" style="font-size:22px">{language or "Unknown"}</div>
        </div>
        """, unsafe_allow_html=True)

    with m2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">WARNING CATEGORIES MATCHED</div>
            <div class="metric-value" style="font-size:22px">{len(findings)}</div>
        </div>
        """, unsafe_allow_html=True)

    with m3:
        if not findings:
            level, color = "Low", "#5fe3a1"
        elif len(findings) == 1:
            level, color = "Medium", "#f5c451"
        else:
            level, color = "High", "#ff6b6b"

        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">INDICATOR LEVEL</div>
            <div class="metric-value" style="font-size:22px;color:{color}">{level}</div>
        </div>
        """, unsafe_allow_html=True)

    # ---------- Transcription ----------
    st.markdown('<div class="section-title">📝 Transcription</div>',
                unsafe_allow_html=True)
    st.audio(result["audio_bytes"])

    if transcript:
        st.text_area("Recognized speech", value=transcript, height=150)
    else:
        st.info("No speech was detected in this recording.")

    # ---------- Warning signs ----------
    st.markdown('<div class="section-title">🚨 Potential Warning Signs</div>',
                unsafe_allow_html=True)

    if findings:
        st.error(
            f"{len(findings)} warning categor"
            f"{'y' if len(findings) == 1 else 'ies'} matched."
        )

        for finding in findings:
            with st.expander(f"⚠️ {finding['category']}", expanded=True):
                st.write("**Matched terms:**")
                st.write(", ".join(finding["matched_terms"]))

        st.warning(
            "These indicators do not prove that the recording "
            "is fraudulent. Verify the request independently."
        )
    else:
        st.success("No warning categories matched the current rules.")
        st.info(
            "This does not guarantee that the recording is safe. "
            "The current system checks a limited set of phrases."
        )

    # ---------- Safety actions ----------
    st.markdown('<div class="section-title">🛡️ Recommended Safety Actions</div>',
                unsafe_allow_html=True)

    tips1, tips2 = st.columns(2)

    with tips1:
        st.markdown("""
        <div class="panel">
            <div class="panel-title">🔑 Protect Your Information</div>
            <div class="muted">
                • Never share OTPs or banking PINs.<br>
                • Never disclose passwords.<br>
                • Avoid unexpected payment links.
            </div>
        </div>
        """, unsafe_allow_html=True)

    with tips2:
        st.markdown("""
        <div class="panel">
            <div class="panel-title">📞 Verify the Caller</div>
            <div class="muted">
                • Call back using a trusted number.<br>
                • Confirm urgent requests independently.<br>
                • Be cautious about secrecy and pressure.
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.button("⬅️  Analyze another recording", on_click=new_analysis, key="back_bottom")


# =====================================================
# STEP 7: FOOTER (shown on both pages)
# =====================================================

st.markdown("""
<div class="footer">
    AWAaz SHIELD · AI-Assisted Voice Scam Analysis<br>
    Built for awareness and preliminary risk assessment.
    Not a substitute for independent verification.
</div>
""", unsafe_allow_html=True)