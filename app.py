import streamlit as st
import time
import random

# App-Konfiguration
st.set_page_config(page_title="Traumatisierender Taschen-Therapeut", page_icon="🎧", layout="centered")

# CSS-Styling
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
.red-button {
    background-color: #f08080;
    border: none;
    color: white;
    padding: 12px 24px;
    text-align: center;
    font-size: 16px;
    border-radius: 50px;
    display: block;
    margin: 0 auto;
}
</style>
""", unsafe_allow_html=True)

# Titel & Untertitel
st.markdown('<div class="title">Traumatisierender Taschen-Therapeut</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Bitte scanne deine Versichertenkarte, um zu starten</div>', unsafe_allow_html=True)

# Auswahl der Versicherung
def versicherungswahl():
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🪪 Gesetzlich versichert", use_container_width=True):
            st.session_state["insurance"] = "GKV"
            st.session_state["loading_done"] = False
    with col2:
        if st.button("💳 Privat versichert", use_container_width=True):
            st.session_state["insurance"] = "PKV"
            st.session_state["loading_done"] = False

# Ladeanimation + Text + Button
def ladeanimation_mit_button():
    st.image("glockenkurve_ladeanimation.gif", use_container_width=True)
    lade_text = st.empty()
    button_container = st.empty()

    botschaften = [
        "🧠 Analysiere deine Versichertenzugehörigkeit…",
        "📑 Prüfe Wartezeit im seelischen Wartezimmer…",
        "💸 Vergleichst du Leistungen oder nur Leidensdruck?",
        "🤡 Was kostet eine Sitzung? Deine letzte Hoffnung.",
        "🕳️ Du fällst in die Warteliste… bitte lächeln!"
    ]

    startzeit = time.time()
    i = 0
    while time.time() - startzeit < 10:
        lade_text.markdown(f"<div style='text-align: center;'>{botschaften[i % len(botschaften)]}</div>", unsafe_allow_html=True)
        time.sleep(2.5)
        i += 1

        if time.time() - startzeit >= 5 and "show_button" not in st.session_state:
            st.session_state["show_button"] = True

        if st.session_state.get("show_button"):
            if button_container.button("🎟️ B2.01 besuchen", key="weiterleitung_button"):
                st.session_state["loading_done"] = True
                break

# Nach dem Laden: Ticket + Witz + Module
def zeige_modulbereich():
    status = st.session_state["insurance"]
    ticket = f"{status}-{random.randint(100000, 999999)}"

    if status == "GKV":
        st.subheader("🪪 Willkommen, Pöbel!")
        st.markdown(f"""
        <div style="background-color: #96CDCD; padding: 1em; border-radius: 10px; color: #000000;">
        <b>🎟️ Ticketnummer: {ticket}</b><br><br>
        Deine Wartezeit beträgt ca. 6–18 Monate.<br><br>
        Aber hey: immerhin reicht die Wartezeit noch nicht aus, um Psychologie einfach selbst zu studieren.
        </div>
        """, unsafe_allow_html=True)
        st.caption("Tipp: Wenn du beim Scannen deiner Karte weinst, zählt das bereits als Erstgespräch.")
    else:
        st.subheader("💎 Willkommen, oberer Mittelschichtler!")
        st.markdown(f"""
        <div style="background-color: #96CDCD; padding: 1em; border-radius: 10px; color: #000000;">
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
    auswahl = st.selectbox("Modul auswählen", [
        "Etwas verstehen",
        "Etwas fühlen",
        "Innere Anteile besuchen",
        "Therapie-Minispiel",
        "Tagebuch öffnen",
        "Galgenhumor-Modus"
    ])

    if auswahl == "Tagebuch öffnen":
        st.text_area("Was geht gerade in dir vor?", placeholder="Hier ist Raum für alles, was du fühlst...")
    elif auswahl == "Galgenhumor-Modus":
        st.caption("„Schön, dass du es heute geschafft hast, nicht komplett durchzudrehen. Fortschritt ist relativ.“")
    else:
        st.markdown(f"Du hast **{auswahl}** gewählt. Dieses Modul wird bald freigeschaltet.")

# Ablaufsteuerung
if "insurance" not in st.session_state:
    versicherungswahl()
elif not st.session_state.get("loading_done", False):
    ladeanimation_mit_button()
else:
    zeige_modulbereich()
