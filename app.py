import streamlit as st

# App-Konfiguration
st.set_page_config(page_title="traumatisierender Taschen-Therapeut", page_icon="🎧", layout="centered")

# 🌈 Farbdesign: Hintergrund + Titel
st.markdown("""
    <style>
    html, body, [data-testid="stAppViewContainer"] {
        font-family: 'Segoe UI', sans-serif;
        background-color: #FFF8DC;
        color: #2c2c2c;
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

    .stAlert {
        border-radius: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# Titel & Untertitel
st.markdown('<div class="title">Traumatisierender Taschen-Therapeut</div>', unsafe_allow_html=True)
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
    show_insurance_choice()
else:
    st.divider()
    status = st.session_state["insurance"]

    if status == "GKV":
        st.subheader("🪪 Willkommen, gesetzlich versichert!")
        st.markdown("""
<div style="background-color: #f8d7da; padding: 1em; border-radius: 10px; color: #000000;">
<b>🪪 Willkommen, gesetzlich versichert!</b><br>
Deine Wartezeit beträgt ca. 6–18 Monate.<br><br>
Aber hey: immerhin reicht die Wartezeit noch nicht aus, um Psychologie einfach selbst zu studieren.
</div>
""", unsafe_allow_html=True)
        st.caption("Tipp: Wenn du beim Scannen deiner Karte weinst, zählt das bereits als Erstgespräch.")
    elif status == "PKV":
        st.subheader("💎 Willkommen, Privatpatient:in!")
        st.markdown("""
<div style="background-color: #d4edda; padding: 1em; border-radius: 10px; color: #000000;">
<b>💎 Willkommen, Privatpatient:in!</b><br>
Du hast jetzt Zugang zu:<br><br>
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
