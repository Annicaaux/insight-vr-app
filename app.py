import streamlit as st
import time
import random
import datetime

# App-Konfiguration
st.set_page_config(
    page_title="Traumatisierender Taschen-Therapeut", 
    page_icon="🎧", 
    layout="centered"
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
            # Fallback für sehr alte Versionen
            st.legacy_caching.clear_cache()
            st.stop()

# Session State initialisieren
if "insurance" not in st.session_state:
    st.session_state.insurance = None
if "loading_done" not in st.session_state:
    st.session_state.loading_done = False
if "show_button" not in st.session_state:
    st.session_state.show_button = False
if "diary_entries" not in st.session_state:
    st.session_state.diary_entries = []
if "therapy_points" not in st.session_state:
    st.session_state.therapy_points = 0
if "game_score" not in st.session_state:
    st.session_state.game_score = 0

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
.stButton > button {
    background-color: #e0cfee;
    color: #4a148c;
    border: none;
    padding: 10px 16px;
    font-size: 1.1em;
    border-radius: 10px;
    margin-top: 10px;
    transition: 0.3s;
    width: 100%;
}
.stButton > button:hover {
    background-color: #d1bce2;
    color: black;
    transform: scale(1.03);
}
.info-box {
    background-color: #96CDCD;
    padding: 1.5em;
    border-radius: 10px;
    color: #000000;
    margin: 1em 0;
}
.quote-box {
    background-color: #f0f0f0;
    padding: 1em;
    border-radius: 10px;
    border-left: 4px solid #20B2AA;
    font-style: italic;
    margin: 1em 0;
}
.diary-entry {
    background-color: #f8f9ff;
    border-left: 4px solid #667eea;
    padding: 1em;
    margin: 0.5em 0;
    border-radius: 0 10px 10px 0;
}
</style>
""", unsafe_allow_html=True)

# Titel & Untertitel
st.markdown('<div class="title">Traumatisierender Taschen-Therapeut</div>', unsafe_allow_html=True)

# Hauptlogik
if st.session_state.insurance is None:
    # Versicherungsauswahl
    st.markdown('<div class="subtitle">Bitte scanne deine Versichertenkarte, um zu starten</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🪪 Gesetzlich versichert", key="gkv"):
            st.session_state.insurance = "GKV"
            rerun_app()
    
    with col2:
        if st.button("💳 Privat versichert", key="pkv"):
            st.session_state.insurance = "PKV"
            rerun_app()

elif not st.session_state.loading_done:
    # Ladeanimation
    st.markdown("### 🔄 Verarbeitung läuft...")
    
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    botschaften = [
        "🧠 Analysiere deine Versichertenzugehörigkeit…",
        "📑 Prüfe Wartezeit im seelischen Wartezimmer…",
        "💸 Vergleiche Leistungen mit deinem Leidensdruck…",
        "🤡 Kalkuliere Kosten für deine letzte Hoffnung…",
        "🕳️ Du fällst in die Warteliste… bitte lächeln!"
    ]
    
    # Simuliere Ladevorgang
    for i in range(100):
        progress_bar.progress(i + 1)
        message_index = (i // 20) % len(botschaften)
        status_text.markdown(f"**{botschaften[message_index]}**")
        time.sleep(0.05)
    
    if st.button("🎟️ Wartezimmer B2.01 betreten"):
        st.session_state.loading_done = True
        rerun_app()

else:
    # Hauptbereich
    status = st.session_state.insurance
    ticket = f"{status}-{random.randint(100000, 999999)}"
    
    # Begrüßung
    if status == "GKV":
        st.markdown("## 🪪 Willkommen, geschätzter Kassenbeitragszahler!")
        st.markdown(f"""
        <div class="info-box">
        <h3>🎟️ Dein Ticket: {ticket}</h3>
        <p><strong>Wartezeit:</strong> 6-18 Monate</p>
        <p><strong>Leistungen:</strong> Grundversorgung + existenzielle Krise</p>
        <br>
        <em>💡 Tipp: Wenn du beim Kartenscannen weinst, zählt das bereits als Erstgespräch!</em>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("## 💎 Willkommen, Premium-Leidender!")
        st.markdown(f"""
        <div class="info-box">
        <h3>🎟️ VIP-Ticket: {ticket}</h3>
        <p><strong>Wartezeit:</strong> 24-48 Stunden</p>
        <p><strong>Premium-Leistungen:</strong></p>
        <ul>
        <li>🛋️ Designer-Sitzsäcke</li>
        <li>🍦 Funktionierende Eismaschine</li>
        <li>🔔 24/7 Notfall-Hotline</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)
    
    # Therapie-Fortschritt
    st.session_state.therapy_points += 1
    progress = min(st.session_state.therapy_points * 2, 100)
    st.markdown("### 📊 Dein Therapie-Fortschritt")
    st.progress(progress / 100)
    st.caption(f"Level: {st.session_state.therapy_points}")
    
    st.divider()
    
    # Module
    st.markdown("### 🎯 Was brauchst du heute?")
    
    module = st.selectbox("Modul auswählen", [
        "Tagebuch öffnen",
        "Galgenhumor-Modus", 
        "Therapie-Minispiel",
        "Etwas fühlen",
        "Etwas verstehen",
        "Innere Anteile besuchen"
    ])
    
    # Module-Inhalte
    if module == "Tagebuch öffnen":
        st.markdown("### 📝 Digitales Seelen-Archiv")
        
        # Stimmung wählen
        mood = st.select_slider(
            "Aktuelle Stimmung:",
            options=["💀 Existenzkrise", "😭 Heulkrampf", "😐 Zombie-Modus", "🙂 Geht so", "✨ Okay"],
            value="😐 Zombie-Modus"
        )
        
        # Tagebucheintrag
        entry_text = st.text_area(
            "Was geht gerade in dir vor?", 
            placeholder="Hier ist Raum für alles, was du fühlst...",
            height=150
        )
        
        if st.button("💾 Eintrag speichern"):
            if entry_text:
                new_entry = {
                    "date": datetime.datetime.now().strftime("%d.%m.%Y %H:%M"),
                    "mood": mood,
                    "text": entry_text
                }
                st.session_state.diary_entries.append(new_entry)
                st.success("Eintrag gespeichert! Dein Schmerz wurde digitalisiert. 📱")
        
        # Alte Einträge anzeigen
        if st.session_state.diary_entries:
            st.markdown("**Deine letzten Einträge:**")
            for entry in reversed(st.session_state.diary_entries[-3:]):
                st.markdown(f"""
                <div class="diary-entry">
                <strong>{entry['date']}</strong> | {entry['mood']}<br>
                <em>{entry['text'][:100]}{'...' if len(entry['text']) > 100 else ''}</em>
                </div>
                """, unsafe_allow_html=True)
    
    elif module == "Galgenhumor-Modus":
        st.markdown("### 😅 Therapie durch Sarkasmus")
        
        quotes = [
            "Schön, dass du es heute geschafft hast, nicht komplett durchzudrehen. Fortschritt ist relativ.",
            "Deine Probleme sind einzigartig - genau wie die von 8 Milliarden anderen Menschen.",
            "Wartezeit ist Therapie-Zeit! Du übst schon mal das Warten auf Besserung.",
            "Vergiss nicht: Auch Sisyphos hatte schlechte Tage. Aber er hatte wenigstens einen Stein.",
            "Deine Selbstzweifel sind berechtigt - das ist schon mal ein Fortschritt."
        ]
        
        if st.button("🎲 Neue Weisheit"):
            quote = random.choice(quotes)
            st.markdown(f"""
            <div class="quote-box">
            "{quote}"<br><br>
            <small>- Dein digitaler Seelen-Klempner</small>
            </div>
            """, unsafe_allow_html=True)
    
    elif module == "Therapie-Minispiel":
        st.markdown("### 🎮 Existenzkrise: Das Spiel")
        st.markdown(f"**Score: {st.session_state.game_score} Überlebens-Punkte**")
        
        challenges = [
            {"text": "Du stehst auf, ohne den Wecker zu verfluchen", "points": 10},
            {"text": "Du trinkst Wasser statt nur Kaffee", "points": 15},
            {"text": "Du gehst vor Mitternacht ins Bett", "points": 20},
            {"text": "Du rufst einen Freund an", "points": 25}
        ]
        
        challenge = random.choice(challenges)
        st.markdown(f"**Challenge:** {challenge['text']}")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("✅ Geschafft!"):
                st.session_state.game_score += challenge["points"]
                st.success(f"+{challenge['points']} Punkte!")
        
        with col2:
            if st.button("❌ Versagt"):
                st.info("Auch okay. Morgen ist ein neuer Tag!")
    
    elif module == "Etwas fühlen":
        st.markdown("### 💙 Gefühls-Check")
        
        emotions = st.multiselect(
            "Wie geht es dir gerade?",
            ["😢 Traurig", "😰 Ängstlich", "😡 Wütend", "😴 Müde", 
             "🤗 Einsam", "😖 Überfordert", "😌 Ruhig", "✨ Hoffnungsvoll"]
        )
        
        if emotions:
            st.markdown("**Deine Gefühlslage:**")
            for emotion in emotions:
                intensity = st.slider(f"Wie stark? {emotion}", 1, 10, 5, key=emotion)
            
            if st.button("💡 Verstehen"):
                st.info("Alle Gefühle sind okay! Auch die blöden. 🧠")
    
    elif module == "Etwas verstehen":
        st.markdown("### 🧠 Gedanken-Detektiv")
        
        thought = st.text_input("Was geht dir durch den Kopf?", 
                               placeholder="z.B. 'Ich schaffe das nie'")
        
        if thought:
            distortions = st.multiselect(
                "Welche Denkfallen erkennst du?",
                ["🔮 Gedankenlesen", "🌍 Katastrophisieren", 
                 "⚫ Schwarz-Weiß-Denken", "🔍 Verallgemeinern"]
            )
            
            if st.button("🔍 Realitätscheck"):
                st.success("Gut! Gedanken sind nicht immer Fakten. 🧠")
    
    elif module == "Innere Anteile besuchen":
        st.markdown("### 🎭 Innere WG-Bewohner")
        
        parts = {
            "👨‍💼 Der Perfektionist": "Alles muss perfect sein!",
            "😰 Der Ängstliche": "Was wenn alles schief geht?",
            "🎨 Der Kreative": "Lass uns was Schönes machen!",
            "😡 Der Wütende": "Das ist unfair!",
            "👶 Das innere Kind": "Ich will Spaß haben!"
        }
        
        selected_part = st.selectbox("Wer meldet sich?", list(parts.keys()))
        
        if selected_part:
            st.markdown(f"**{selected_part} sagt:** '{parts[selected_part]}'")
            response = st.text_area("Was antwortest du?")
            
            if response and st.button("💬 Antworten"):
                st.success("Dialog gestartet! 🗣️")

# Footer
st.markdown("---")
st.markdown("*Disclaimer: Diese App ersetzt keine echte Therapie! 🏥*")

# Reset (versteckt in Sidebar)
with st.sidebar:
    if st.button("🔄 Alles zurücksetzen"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        rerun_app()
