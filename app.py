import streamlit as st
import time
import random

# App-Konfiguration
st.set_page_config(page_title="Traumatisierender Taschen-Therapeut", page_icon="🎧", layout="centered")

# Farb- und Stildefinition
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
    .stButton button {
        background-color: #e0cfee;
        color: #4a148c;
        border: none;
        padding: 10px 16px;
        font-size: 1.1em;
        border-radius: 10px;
        margin-top: 10px;
        transition: 0.3s;
    }
    .stButton button:hover {
        background-color: #d1bce2;
        color: black;
        transform: scale(1.03);
    }
    .custom-button {
        background-color: #FF6F61;
        color: white;
        padding: 14px 28px;
        font-size: 18px;
        border: none;
        border-radius: 50px;
        text-align: center;
        display: block;
        margin: 20px auto;
        cursor: pointer;
    }
    textarea {
        background-color: #e6f7f9 !important;
        color: #000000 !important;
        border-radius: 10px;
        padding: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# Titel
st.markdown('<div class="title">Traumatisierender Taschen-Therapeut</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Bitte scanne deine Versichertenkarte, um zu starten</div>', unsafe_allow_html=True)

# Initialisierung
if "insurance" not in st.session_state:
    st.session_state.insurance = None
if "scan_complete" not in st.session_state:
    st.session_state.scan_complete = False
if "show_button" not in st.session_state:
    st.session_state.show_button = False
if "show_modules" not in st.session_state:
    st.session_state.show_modules = False

# Versicherungswahl
if st.session_state.insurance is None:
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🪪 Gesetzlich versichert", use_container_width=True):
            st.session_state.insurance = "GKV"
            st.session_state.start_time = time.time()
    with col2:
        if st.button("💳 Privat versichert", use_container_width=True):
            st.session_state.insurance = "PKV"
            st.session_state.start_time = time.time()

# Ladeanimation
elif not st.session_state.scan_complete:
    st.image("glockenkurve_ladeanimation.gif", use_container_width=True)
    ladeplatz = st.empty()
    ladebotschaften = [
        "🧠 Analysiere deine Versichertenzugehörigkeit…",
        "📑 Prüfe Wartezeit im seelischen Wartezimmer…",
        "💸 Vergleichst du Leistungen oder nur Leidensdruck?",
        "🤡 Was kostet eine Sitzung? Deine letzte Hoffnung.",
        "🕳️ Du fällst in die Warteliste… bitte lächeln!"
    ]
    elapsed = time.time() - st.session_state.start_time

    index = int((elapsed // 2.5) % len(ladebotschaften))
    ladeplatz.markdown(f"<div style='text-align: center'>{ladebotschaften[index]}</div>", unsafe_allow_html=True)

    if elapsed >= 5 and not st.session_state.show_button:
        st.session_state.show_button = True

    if st.session_state.show_button:
        if st.button("🎟️ B2.01 besuchen", key="go", help="Weiter zur Modulauswahl"):
            st.session_state.scan_complete = True
    st.stop()

# Hauptinhalt nach Scan
elif st.session_state.scan_complete and not st.session_state.show_modules:
    st.session_state.show_modules = True
    ticket = f"{st.session_state.insurance}-{random.randint(100000, 999999)}"

    if st.session_state.insurance == "GKV":
        st.subheader("🪪 Willkommen, Pöbel!")
        st.markdown(f"""
        <div style="background-color: #96CDCD; padding: 1em; border-radius: 10px;">
        <b>🎟️ Ticketnummer: {ticket}</b><br><br>
        Deine Wartezeit beträgt ca. 6–18 Monate.<br><br>
        Aber hey: immerhin reicht die Wartezeit noch nicht aus, um Psychologie einfach selbst zu studieren.
        </div>
        """, unsafe_allow_html=True)
        st.caption("Tipp: Wenn du beim Scannen deiner Karte weinst, zählt das bereits als Erstgespräch.")
    else:
        st.subheader("💎 Willkommen, oberer Mittelschichtler!")
        st.markdown(f"""
        <div style="background-color: #96CDCD; padding: 1em; border-radius: 10px;">
        <b>🎟️ Ticketnummer: {ticket}</b><br><br>
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
