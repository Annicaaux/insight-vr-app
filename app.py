# app.py
import streamlit as st

# App-Konfiguration
st.set_page_config(page_title="InSight VR", page_icon="🎧", layout="centered")

# Überschrift & Stil
st.markdown("""
    <style>
    .title {
        text-align: center;
        font-size: 2.5em;
        color: #6a1b9a;
        margin-bottom: 10px;
    }
    .subtitle {
        text-align: center;
        font-size: 1.2em;
        color: #555;
        margin-bottom: 40px;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="title">🎧 InSight VR – Dein innerer Kompass</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Bitte scanne deine Versichertenkarte, um zu starten</div>', unsafe_allow_html=True)

# Visuelle Auswahl & Witze
def show_insurance_choice():
    col1, col2 = st.columns(2)

    with col1:
        if st.button("🪪 Gesetzlich versichert", use_container_width=True):
            st.session_state["insurance"] = "GKV"
    with col2:
        if st.button("💳 Privat versichert", use_container_width=True):
            st.session_state["insurance"] = "PKV"

# Zeige Auswahl oder Witz je nach Status
if "insurance" not in st.session_state:
    st.markdown("## Bitte scanne deine Versichertenkarte:")
    show_insurance_choice()
else:
    st.divider()
    status = st.session_state["insurance"]

    if status == "GKV":
        st.subheader("🪪 Willkommen, gesetzlich versichert!")
        st.error("**Deine Wartezeit beträgt ca. 6–18 Monate.**\n\nAber hey: Dafür darfst du kostenlos in der Ecke deines psychischen Ausnahmezustands sitzen. Und dein Therapeut sieht dich... irgendwann.")
        st.caption("Tipp: Wenn du beim Scannen deiner Karte weinst, zählt das bereits als Erstgespräch.")
    elif status == "PKV":
        st.subheader("💎 Willkommen, Privatpatient:in!")
        st.success("Du hast jetzt Zugang zu:\n\n- Einzeltherapie mit Designer-Sitzsäcken\n- psychoanalytischem Latte Macchiato\n- Notfalltermin innerhalb von 24 Sekunden\n\nWahlweise mit Klangschale oder Ego-Streicheln.")
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
