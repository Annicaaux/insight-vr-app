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

# Kartenwahl
status = st.radio("Versicherungsstatus wählen:", ["Gesetzlich versichert", "Privat versichert"])

# Joke je nach Auswahl
if status:
    st.divider()
    if status == "Gesetzlich versichert":
        st.subheader("🪪 Willkommen, gesetzlich versichert!")
        st.info("Deine Therapie beginnt – sobald ein Platz frei wird. Also… irgendwann zwischen BER-Eröffnung und Auferstehung von Freud.")
    else:
        st.subheader("💎 Willkommen, Privatpatient:in!")
        st.success("Dein VR-Raum wurde aufgewertet: Jetzt mit goldener Klangschale, Psycho-Butler und Dior-Traumaauflösung™.")

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
