import streamlit as st
import time
import random

# App-Konfiguration
st.set_page_config(page_title="Traumatisierender Taschen-Therapeut", page_icon="🎧", layout="centered")

# 🌈 Stildefinition
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
    textarea {
        background-color: #e6f7f9 !important;
        color: #000000 !important;
        border-radius: 10px;
        padding: 10px;
    }
    .continue-button {
        display: flex;
        justify-content: center;
        margin-top: 2em;
    }
    .continue-button button {
        background-color: #ff9999 !important;
        color: black !important;
        border-radius: 50px !important;
        font-weight: bold;
        font-size: 1.1em;
        padding: 10px 24px;
    }
    </style>
""", unsafe_allow_html=True)

# Überschrift
st.markdown('<div class="title">Traumatisierender Taschen-Therapeut</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Bitte scanne deine Versichertenkarte, um zu starten</div>', unsafe_allow_html=True)

# Versicherungswahl
def show_insurance_choice():
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🪪 Gesetzlich versichert", use_container_width=True):
            st.session_state["insurance"] = "GKV"
            st.session_state["show_loading"] = True
            st.session_state["show_button"] = False
            st.session_state["show_result"] = False
    with col2:
        if st.button("💳 Privat versichert", use_container_width=True):
            st.session_state["insurance"] = "PKV"
            st.session_state["show_loading"] = True
            st.session_state["show_button"] = False
            st.session_state["show_result"] = False

def show_loading_animation():
    st.image("glockenkurve_ladeanimation.gif", caption="Versicherungsstatus wird analysiert...", use_container_width=True)
    ladeplatz = st.empty()
    ladebotschaften = [
        "🧠 Analysiere deine Versichertenzugehörigkeit…",
        "📑 Prüfe Wartezeit im seelischen Wartezimmer…",
        "💸 Vergleichst du Leistungen oder nur Leidensdruck?",
        "🤡 Was kostet eine Sitzung? Deine letzte Hoffnung.",
        "🕳️ Du fällst in die Warteliste… bitte lächeln!"
    ]
    for botschaft in ladebotschaften:
        ladeplatz.markdown(f'<div style="text-align: center;">{botschaft}</div>', unsafe_allow_html=True)
        time.sleep(2)

    st.session_state["show_button"] = True

def show_continue_button():
    st.markdown('<div class="continue-button">', unsafe_allow_html=True)
    if st.button("B2.01 besuchen"):
        st.session_state["show_result"] = True
        st.session_state["show_loading"] = False
    st.markdown('</div>', unsafe_allow_html=True)

def show_result():
    status = st.session_state["insurance"]
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

# Ablaufsteuerung
if "insurance" not in st.session_state:
    show_insurance_choice()
elif st.session_state.get("show_loading", False) and not st.session_state.get("show_button", False):
    show_loading_animation()
elif st.session_state.get("show_button", False) and not st.session_state.get("show_result", False):
    show_continue_button()
elif st.session_state.get("show_result", False):
    show_result()
