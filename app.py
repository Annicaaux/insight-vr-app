import streamlit as st
import time
import random

# App-Konfiguration
st.set_page_config(page_title="Traumatisierender Taschen-Therapeut", page_icon="🎧", layout="centered")

# 🌈 Farbdesign und Button-Stil
st.markdown("""
    <style>
    html, body, [data-testid="stAppViewContainer"] {
        font-family: 'Segoe UI', sans-serif;
        background-color: #FFF8DC;
        color: #000000;
    }
    .title {
        text-align: center;
        font-size: 2.5em;
        color: #20B2AA;
        margin-bottom: 10px;
    }
    .subtitle {
        text-align: center;
        font-size: 1.2em;
        color: #000000;
        margin-bottom: 40px;
    }
    .stButton>button {
        background-color: #f4cccc !important;
        color: black !important;
        border-radius: 30px !important;
        padding: 12px 24px !important;
        font-size: 1.1em !important;
        display: block;
        margin: 0 auto;
    }
    textarea {
        background-color: #e6f7f9 !important;
        color: #000000 !important;
        border-radius: 10px;
        padding: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# Titel & Untertitel
st.markdown('<div class="title">Traumatisierender Taschen-Therapeut</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Bitte scanne deine Versichertenkarte, um zu starten</div>', unsafe_allow_html=True)

# Funktions-Initialisierung
if "insurance" not in st.session_state:
    st.session_state.insurance = None
if "scan_step" not in st.session_state:
    st.session_state.scan_step = 0
if "continue_clicked" not in st.session_state:
    st.session_state.continue_clicked = False

# Versicherungs-Auswahl
if st.session_state.insurance is None:
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🪪 Gesetzlich versichert", use_container_width=True):
            st.session_state.insurance = "GKV"
            st.session_state.scan_step = 1
    with col2:
        if st.button("💳 Privat versichert", use_container_width=True):
            st.session_state.insurance = "PKV"
            st.session_state.scan_step = 1

# Ladeanimation
if st.session_state.scan_step == 1 and not st.session_state.continue_clicked:
    st.image("glockenkurve_ladeanimation.gif", use_container_width=True)
    platzhalter = st.empty()
    ladebotschaften = [
        "🧠 Analysiere deine Versichertenzugehörigkeit…",
        "📑 Prüfe Wartezeit im seelischen Wartezimmer…",
        "💸 Vergleichst du Leistungen oder nur Leidensdruck?",
        "🤡 Was kostet eine Sitzung? Deine letzte Hoffnung.",
        "🕳️ Du fällst in die Warteliste… bitte lächeln!"
    ]
    for botschaft in ladebotschaften:
        platzhalter.markdown(f"<div style='text-align:center;'>{botschaft}</div>", unsafe_allow_html=True)
        time.sleep(1.1)
    st.session_state.scan_step = 2

# Button zur Weiterleitung
if st.session_state.scan_step == 2 and not st.session_state.continue_clicked:
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("B2.01 besuchen"):
        st.session_state.continue_clicked = True

# Ergebnisanzeige
if st.session_state.continue_clicked:
    status = st.session_state.insurance
    ticket_number = f"{status}-{random.randint(100000, 999999)}"
    if status == "GKV":
        st.subheader("🪪 Willkommen, Pöbel!")
        st.markdown(f"""
        <div style="background-color: #96CDCD; padding: 1em; border-radius: 10px;">
        <b>🎟️ Ticketnummer: {ticket_number}</b><br><br>
        Deine Wartezeit beträgt ca. 6–18 Monate.<br><br>
        Aber hey: immerhin reicht die Wartezeit noch nicht aus, um Psychologie einfach selbst zu studieren.
        </div>
        """, unsafe_allow_html=True)
        st.caption("Tipp: Wenn du beim Scannen deiner Karte weinst, zählt das bereits als Erstgespräch.")
    elif status == "PKV":
        st.subheader("💎 Willkommen, oberer Mittelschichtler!")
        st.markdown(f"""
        <div style="background-color: #96CDCD; padding: 1em; border-radius: 10px;">
        <b>🎟️ Ticketnummer: {ticket_number}</b><br><br>
        Du hast jetzt Zugang zu:<br>
        – Einzeltherapie mit Designer-Sitzsäcken<br>
        – funktionierender McDonalds Eismaschine<br>
        – Notfalltermin innerhalb von 24 Sekunden<br><br>
        Wahlweise mit vergoldeter Klangschale oder Ego-Streicheln.
        </div>
        """, unsafe_allow_html=True)
        st.caption("Fun Fact: Dein Therapeut hat deinen Lebenslauf gegoogelt – und dich sofort auf LinkedIn verlinkt.")

    st.divider()
    st.markdown("### Was brauchst du heute?")
    choice = st.selectbox("Modul auswählen", [
        "Etwas verstehen",
        "Etwas fühlen",
        "Innere Anteile besuchen",
        "Therapie-Minispiel",
        "Tagebuch öffnen",
        "Galgenhumor-Modus"
    ])
    if choice == "Tagebuch öffnen":
        st.text_area("Was geht gerade in dir vor?", placeholder="Hier ist Raum für alles, was du fühlst...")
    elif choice == "Galgenhumor-Modus":
        st.caption("„Schön, dass du es heute geschafft hast, nicht komplett durchzudrehen. Fortschritt ist relativ.“")
    else:
        st.markdown(f"Du hast **{choice}** gewählt. Dieses Modul wird bald freigeschaltet.")
