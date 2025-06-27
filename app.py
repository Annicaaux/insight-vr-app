import streamlit as st
import time
import random
import datetime
import json

# App-Konfiguration
st.set_page_config(
    page_title="Traumatisierender Taschen-Therapeut", 
    page_icon="🎧", 
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Kompatibilitätsfunktion für verschiedene Streamlit-Versionen
def rerun_app():
    """Kompatible Funktion für App-Neustart"""
    try:
        st.rerun()
    except AttributeError:
        try:
            st.experimental_rerun()
        except AttributeError:
            st.legacy_caching.clear_cache()
            st.stop()

# Session State initialisieren
def init_session_state():
    """Initialisiert alle Session State Variablen"""
    defaults = {
        "insurance": None,
        "loading_done": False,
        "show_button": False,
        "diary_entries": [],
        "therapy_points": 0,
        "game_score": 0,
        "user_mood_history": [],
        "behavior_analyses": [],
        "current_module": None,
        "training_attempts": [],
        "confirm_reset": False
    }
    
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

# Session State initialisieren
init_session_state()

# Erweiterte CSS-Styling
def load_css():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Caveat:wght@400;600;700&display=swap');

    :root {
        --primary-color: #667eea;
        --secondary-color: #764ba2;
        --accent-color: #f093fb;
        --warm-color: #ffecd2;
        --success-color: #4ecdc4;
        --warning-color: #ffe66d;
        --danger-color: #ff6b6b;
        --text-primary: #2d3748;
        --text-secondary: #4a5568;
        --bg-primary: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        --bg-card: rgba(255, 255, 255, 0.95);
        --shadow: 0 10px 25px rgba(0,0,0,0.1);
        --shadow-hover: 0 20px 40px rgba(0,0,0,0.15);
    }

    html, body, [data-testid="stAppViewContainer"] {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        background-attachment: fixed;
        color: var(--text-primary);
    }

    .floating-shape {
        position: absolute;
        background: rgba(255, 255, 255, 0.1);
        border-radius: 50%;
        animation: float 6s ease-in-out infinite;
    }

    @keyframes float {
        0%, 100% { transform: translateY(0px) rotate(0deg); }
        50% { transform: translateY(-20px) rotate(180deg); }
    }

    .gradient-text {
        background: linear-gradient(45deg, #667eea, #764ba2, #f093fb);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        animation: gradient-shift 3s ease infinite;
    }

    @keyframes gradient-shift {
        0%, 100% { filter: hue-rotate(0deg); }
        50% { filter: hue-rotate(30deg); }
    }

    .main-title {
        text-align: center;
        font-family: 'Caveat', cursive;
        font-size: 3.5em;
        font-weight: 700;
        margin: 0.5em 0;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        animation: glow 2s ease-in-out infinite alternate;
    }

    @keyframes glow {
        from { text-shadow: 2px 2px 4px rgba(0,0,0,0.3), 0 0 10px rgba(255,255,255,0.2); }
        to { text-shadow: 2px 2px 4px rgba(0,0,0,0.3), 0 0 20px rgba(255,255,255,0.4); }
    }

    .subtitle {
        text-align: center;
        font-size: 1.4em;
        color: rgba(255, 255, 255, 0.9);
        margin-bottom: 2em;
        font-weight: 300;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.2);
    }

    .main-container {
        background: var(--bg-card);
        border-radius: 25px;
        padding: 2.5em;
        margin: 1em auto;
        max-width: 1200px;
        box-shadow: var(--shadow);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(255,255,255,0.3);
    }

    .stButton > button {
        background: linear-gradient(45deg, var(--primary-color), var(--secondary-color));
        color: white;
        border: none;
        padding: 15px 30px;
        font-size: 1.1em;
        font-weight: 500;
        border-radius: 50px;
        margin: 10px 5px;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
        width: 100%;
    }

    .stButton > button:hover {
        transform: translateY(-3px);
        box-shadow: var(--shadow-hover);
        background: linear-gradient(45deg, var(--secondary-color), var(--accent-color));
    }

    .info-box {
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.1), rgba(118, 75, 162, 0.1));
        border: 2px solid rgba(102, 126, 234, 0.2);
        padding: 2em;
        border-radius: 20px;
        margin: 1.5em 0;
        position: relative;
        overflow: hidden;
    }

    .quote-box {
        background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
        color: white;
        padding: 2em;
        border-radius: 20px;
        font-style: italic;
        font-size: 1.1em;
        margin: 1.5em 0;
        box-shadow: var(--shadow);
    }

    .diary-entry {
        background: linear-gradient(135deg, #f8f9ff, #e8f0ff);
        border-left: 5px solid var(--primary-color);
        padding: 1.5em;
        margin: 1em 0;
        border-radius: 0 15px 15px 0;
        box-shadow: 0 5px 15px rgba(0,0,0,0.1);
    }

    .module-card {
        background: var(--bg-card);
        border-radius: 20px;
        padding: 2em;
        text-align: center;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        cursor: pointer;
        border: 2px solid transparent;
        position: relative;
        overflow: hidden;
        min-height: 280px;
    }

    .module-card:hover {
        transform: translateY(-8px) scale(1.02);
        border-color: var(--primary-color);
        box-shadow: var(--shadow-hover);
    }

    .module-icon {
        font-size: 3em;
        margin-bottom: 0.5em;
        display: block;
        animation: bounce 2s infinite;
    }

    @keyframes bounce {
        0%, 20%, 50%, 80%, 100% { transform: translateY(0); }
        40% { transform: translateY(-10px); }
        60% { transform: translateY(-5px); }
    }

    .progress-container {
        background: rgba(255, 255, 255, 0.2);
        border-radius: 25px;
        padding: 0.5em;
        margin: 1em 0;
        backdrop-filter: blur(10px);
    }

    .progress-bar {
        background: linear-gradient(90deg, var(--success-color), var(--warning-color));
        height: 12px;
        border-radius: 25px;
        transition: width 0.5s ease;
    }

    @media (max-width: 768px) {
        .main-title {
            font-size: 2.5em;
        }
        
        .main-container {
            margin: 0.5em;
            padding: 1.5em;
        }
    }
    </style>
    """, unsafe_allow_html=True)

# CSS laden
load_css()

# Titel
st.markdown('<div class="main-title gradient-text">🎧 Traumatisierender Taschen-Therapeut</div>', unsafe_allow_html=True)

# Versicherungsauswahl Funktion
def versicherungswahl():
    """Zeigt die Versicherungsauswahl an"""
    st.markdown('<div class="subtitle">🏥 Bitte wähle deine Krankenversicherung</div>', unsafe_allow_html=True)
    st.markdown("*Diese lebenswichtige Entscheidung bestimmt die Qualität deiner digitalen Seelenhygiene*")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("""
        <div class="info-box" style="text-align: center; margin-bottom: 1em;">
            <div style="font-size: 4em; margin-bottom: 0.5em;">🪪</div>
            <h3>Gesetzlich versichert</h3>
            <p style="color: #666;">Standard-Leid mit Wartezeit-Bonus</p>
            <ul style="text-align: left; margin: 1em 0;">
                <li>6-18 Monate Wartezeit (Geduld ist eine Tugend)</li>
                <li>Grundversorgung der Verzweiflung</li>
                <li>Kostenloses Wartezimmer-Trauma</li>
                <li>Gruppentherapie mit anderen Hoffnungslosen</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("🪪 Gesetzlich versichert wählen", key="gkv"):
            st.session_state.insurance = "GKV"
            rerun_app()
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        st.markdown("""
        <div class="info-box" style="text-align: center;">
            <div style="font-size: 4em; margin-bottom: 0.5em;">💎</div>
            <h3>Privat versichert</h3>
            <p style="color: #666;">Premium-Trauma für Besserverdienende</p>
            <ul style="text-align: left; margin: 1em 0;">
                <li>24-48h Express-Verzweiflung</li>
                <li>Designer-Therapeuten mit LinkedIn-Profil</li>
                <li>Vergoldete Taschentücher inklusive</li>
                <li>Notfall-Hotline für Existenzkrisen</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("💎 Privat versichert wählen", key="pkv"):
            st.session_state.insurance = "PKV"
            rerun_app()

# Ladeanimation Funktion
def ladeanimation_mit_button():
    """Zeigt die Ladeanimation"""
    st.markdown("### 🔄 Ihre seelische Verfassung wird analysiert...")
    
    progress_col1, progress_col2, progress_col3 = st.columns([1, 2, 1])
    with progress_col2:
        progress_bar = st.progress(0)
        status_text = st.empty()
        
    botschaften = [
        "🧠 Scanne deine psychische Grundausstattung...",
        "📊 Berechne dein Leidens-Niveau...",
        "🔍 Analysiere deine Versicherungsklasse...",
        "💸 Vergleiche Verzweiflung mit Leistungsumfang...",
        "🎭 Kalibriere deine Erwartungen nach unten...",
        "🕳️ Reserviere deinen Platz im Wartezimmer...",
        "✨ Bereite mentale Erste-Hilfe-Ausrüstung vor...",
        "🎪 Fast geschafft - Vorhang auf für dein Drama!"
    ]
    
    # Simuliere erweiterten Ladevorgang
    for i in range(120):
        progress_bar.progress((i + 1) / 120)
        message_index = (i // 15) % len(botschaften)
        
        # Verschiedene Emojis für verschiedene Phasen
        if i < 30:
            emoji = "🔍"
        elif i < 60:
            emoji = "⚙️"
        elif i < 90:
            emoji = "📊"
        else:
            emoji = "✨"
            
        status_text.markdown(f"{emoji} **{botschaften[message_index]}**")
        time.sleep(0.03)
    
    st.markdown("""
    <div style="text-align: center; margin: 2em 0;">
        <p style="margin-top: 1em; font-style: italic;">
            "Der beste Zeitpunkt, einen Therapeuten zu pflanzen, war vor 20 Jahren.<br>
            Der zweitbeste Zeitpunkt ist jetzt." - Konfuzius (wahrscheinlich)
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("🎟️ 🚪 Wartezimmer B2.01 betreten", key="enter_therapy"):
        st.session_state.loading_done = True
        rerun_app()
