import streamlit as st
import time
import random
import datetime
import json
from typing import Dict, List

# App-Konfiguration
st.set_page_config(
    page_title="Traumatisierender Taschen-Therapeut", 
    page_icon="🎧", 
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Initialisierung der Session States
def init_session_state():
    """Initialisiert alle benötigten Session State Variablen"""
    defaults = {
        "insurance": None,
        "loading_done": False,
        "show_button": False,
        "ticket": None,
        "diary_entries": [],
        "therapy_points": 0,
        "current_module": None,
        "user_name": "Anonymer Leidender",
        "session_count": 0
    }
    
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

# CSS-Styling (erweitert und verbessert)
def load_css():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');
    
    html, body, [data-testid="stAppViewContainer"] {
        font-family: 'Inter', 'Segoe UI', sans-serif;
        background: linear-gradient(135deg, #FFF8DC 0%, #F0F8DC 100%);
        color: #2c3e50;
    }
    
    .main-title {
        text-align: center;
        font-size: 3em;
        font-weight: 700;
        background: linear-gradient(45deg, #20B2AA, #48CAE4);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 10px;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }
    
    .subtitle {
        text-align: center;
        font-size: 1.3em;
        color: #5a6c7d;
        margin-bottom: 40px;
        font-weight: 300;
    }
    
    .stButton > button {
        background: linear-gradient(45deg, #e0cfee, #f0e6ff);
        color: #4a148c;
        border: none;
        padding: 12px 24px;
        font-size: 1.1em;
        font-weight: 600;
        border-radius: 15px;
        margin: 8px 0;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(160, 90, 220, 0.2);
    }
    
    .stButton > button:hover {
        background: linear-gradient(45deg, #d1bce2, #e6d7ff);
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(160, 90, 220, 0.3);
    }
    
    .info-card {
        background: rgba(255, 255, 255, 0.9);
        padding: 2em;
        border-radius: 20px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        border: 1px solid rgba(255,255,255,0.5);
        backdrop-filter: blur(10px);
        margin: 1em 0;
    }
    
    .therapy-progress {
        background: linear-gradient(90deg, #4CAF50, #8BC34A);
        height: 10px;
        border-radius: 5px;
        margin: 10px 0;
        transition: width 0.3s ease;
    }
    
    .quote-box {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1.5em;
        border-radius: 15px;
        font-style: italic;
        margin: 1em 0;
        box-shadow: 0 8px 20px rgba(102, 126, 234, 0.3);
    }
    
    .diary-entry {
        background: #f8f9ff;
        border-left: 4px solid #667eea;
        padding: 1em;
        margin: 0.5em 0;
        border-radius: 0 10px 10px 0;
    }
    
    .module-card {
        background: rgba(255, 255, 255, 0.8);
        padding: 1.5em;
        border-radius: 15px;
        margin: 1em 0;
        transition: transform 0.3s ease;
        cursor: pointer;
        border: 2px solid transparent;
    }
    
    .module-card:hover {
        transform: translateY(-5px);
        border-color: #667eea;
        box-shadow: 0 15px 35px rgba(102, 126, 234, 0.2);
    }
    </style>
    """, unsafe_allow_html=True)

# Datenstrukturen
class TherapyQuotes:
    SARCASTIC = [
        "Schön, dass du es heute geschafft hast, nicht komplett durchzudrehen. Fortschritt ist relativ.",
        "Deine Probleme sind einzigartig - genau wie die von 8 Milliarden anderen Menschen.",
        "Wartezeit ist Therapie-Zeit! Du übst schon mal das Warten auf Besserung.",
        "Vergiss nicht: Auch Sisyphos hatte schlechte Tage. Aber er hatte wenigstens einen Stein.",
        "Deine Selbstzweifel sind berechtigt - das ist schon mal ein Fortschritt in der Selbstwahrnehmung."
    ]
    
    MOTIVATIONAL = [
        "Jeder Schritt zählt, auch wenn er rückwärts ist - du bewegst dich wenigstens.",
        "Du bist stärker als du denkst. Wahrscheinlich. Vielleicht. Hoffen wir es mal.",
        "Heute ist ein neuer Tag voller neuer Möglichkeiten... zu versagen. Aber auch zu wachsen!",
        "Remember: Even professional therapists need therapy. Du bist in guter Gesellschaft."
    ]

class ModuleData:
    MODULES = {
        "Etwas verstehen": {
            "icon": "🧠",
            "description": "Kognitive Verhaltenstherapie für Dummies",
            "activities": ["Gedankenprotokoll", "Kognitive Verzerrungen entdecken", "Realitätscheck"]
        },
        "Etwas fühlen": {
            "icon": "💙", 
            "description": "Emotionsregulation ohne Regulation",
            "activities": ["Gefühls-Wetter", "Emotions-Skala", "Akzeptanz-Übung"]
        },
        "Innere Anteile besuchen": {
            "icon": "🎭",
            "description": "Systemische Familientherapie im Kopf",
            "activities": ["Innere Familie kennenlernen", "Anteil-Dialog", "Ressourcen-Mapping"]
        },
        "Therapie-Minispiel": {
            "icon": "🎮",
            "description": "Gamification der Existenzkrise",
            "activities": ["Angst-Level Boss", "Selbstwert-Sammeln", "Coping-Challenge"]
        },
        "Tagebuch öffnen": {
            "icon": "📔",
            "description": "Digitales Jammern mit Struktur",
            "activities": ["Freies Schreiben", "Dankbarkeits-Journal", "Problem-Analyse"]
        },
        "Galgenhumor-Modus": {
            "icon": "😅",
            "description": "Lachen über das Unlachbare",
            "activities": ["Sarkasmus-Generator", "Ironie-Therapie", "Absurditäts-Check"]
        }
    }

# Hauptfunktionen
def versicherungswahl():
    """Versicherungsauswahl mit verbessertem UI"""
    st.markdown("### Bitte wähle deine Krankenversicherung")
    st.markdown("*Diese Entscheidung bestimmt die Qualität deiner digitalen Verzweiflung*")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🪪 Gesetzlich versichert\n*Standard-Leid*", use_container_width=True):
            st.session_state["insurance"] = "GKV"
            st.session_state["loading_done"] = False
            st.session_state["show_button"] = False
            st.rerun()
    
    with col2:
        if st.button("💳 Privat versichert\n*Premium-Trauma*", use_container_width=True):
            st.session_state["insurance"] = "PKV"
            st.session_state["loading_done"] = False
            st.session_state["show_button"] = False
            st.rerun()

def ladeanimation_mit_button():
    """Verbesserte Ladeanimation ohne externe GIF"""
    st.markdown("### 🔄 Verarbeitung läuft...")
    
    # Fortschrittsbalken statt GIF
    progress_bar = st.progress(0)
    status_text = st.empty()
    button_container = st.empty()
    
    botschaften = [
        "🧠 Analysiere deine Versichertenzugehörigkeit…",
        "📑 Prüfe Wartezeit im seelischen Wartezimmer…",
        "💸 Vergleiche Leistungen mit deinem Leidensdruck…",
        "🤡 Kalkuliere Kosten für deine letzte Hoffnung…",
        "🕳️ Du fällst in die Warteliste… bitte lächeln!",
        "✨ Fast geschafft - bereite Taschentücher vor…"
    ]
    
    if "loading_start_time" not in st.session_state:
        st.session_state["loading_start_time"] = time.time()
    
    elapsed_time = time.time() - st.session_state["loading_start_time"]
    progress = min(elapsed_time / 8.0, 1.0)
    
    progress_bar.progress(progress)
    message_index = int(elapsed_time / 1.5) % len(botschaften)
    status_text.markdown(f"**{botschaften[message_index]}**")
    
    if elapsed_time >= 4 and not st.session_state.get("show_button"):
        st.session_state["show_button"] = True
    
    if st.session_state.get("show_button"):
        if button_container.button("🎟️ Wartezimmer B2.01 betreten", key="weiterleitung_button"):
            st.session_state["loading_done"] = True
            st.session_state["ticket"] = generate_ticket()
            st.rerun()
    
    if elapsed_time < 8:
        time.sleep(0.1)
        st.rerun()

def generate_ticket() -> str:
    """Generiert ein Ticket basierend auf der Versicherung"""
    status = st.session_state["insurance"]
    number = random.randint(100000, 999999)
    return f"{status}-{number}"

def zeige_modulbereich():
    """Hauptbereich nach dem Laden"""
    status = st.session_state["insurance"]
    ticket = st.session_state["ticket"]
    
    # Begrüßung basierend auf Versicherung
    if status == "GKV":
        st.markdown("## 🪪 Willkommen, geschätzter Kassenbeitragszahler!")
        st.markdown(f"""
        <div class="info-card">
        <h3>🎟️ Dein Ticket: {ticket}</h3>
        <p><strong>Wartezeit:</strong> 6-18 Monate (je nach Mondphase)</p>
        <p><strong>Leistungen:</strong> Grundversorgung + existenzielle Krise</p>
        <p><strong>Bonus:</strong> Kostenloses Warten als Achtsamkeitsübung</p>
        <br>
        <em>💡 Tipp: Wenn du beim Kartenscannen weinst, zählt das bereits als Erstgespräch!</em>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("## 💎 Willkommen, oberer Mittelschichtler!")
        st.markdown(f"""
        <div class="info-card">
        <h3>🎟️ VIP-Ticket: {ticket}</h3>
        <p><strong>Wartezeit:</strong> 24-48 Stunden (bei akuter Krise: sofort)</p>
        <p><strong>Premium-Leistungen:</strong></p>
        <ul>
        <li>🛋️ Einzeltherapie mit Designer-Sitzsäcken</li>
        <li>🍦 Funktionierende McDonalds-Eismaschine</li>
        <li>🔔 24/7 Notfall-Hotline</li>
        <li>🥇 Vergoldete Klangschale oder Ego-Streicheln</li>
        </ul>
        <br>
        <em>💡 Fun Fact: Dein Therapeut hat deinen LinkedIn-Profile bereits studiert!</em>
        </div>
        """, unsafe_allow_html=True)
    
    # Therapie-Fortschritt
    st.session_state["therapy_points"] += 1
    progress = min(st.session_state["therapy_points"] * 2, 100)
    
    st.markdown("### 📊 Dein Therapie-Fortschritt")
    st.progress(progress / 100)
    st.caption(f"Level: {st.session_state['therapy_points']} | Nächstes Ziel: Nicht mehr weinen beim Netflix schauen")
    
    st.divider()
    
    # Module auswählen
    st.markdown("### 🎯 Was brauchst du heute?")
    st.markdown("*Wähle dein Gift... äh, deine Therapie-Methode*")
    
    # Module als Cards anzeigen
    for module_name, module_info in ModuleData.MODULES.items():
        col1, col2 = st.columns([1, 4])
        with col1:
            st.markdown(f"## {module_info['icon']}")
        with col2:
            if st.button(f"**{module_name}**\n{module_info['description']}", key=f"module_{module_name}"):
                st.session_state["current_module"] = module_name
                handle_module_selection(module_name)

def handle_module_selection(module_name: str):
    """Behandelt die Auswahl eines Moduls"""
    st.markdown(f"## {ModuleData.MODULES[module_name]['icon']} {module_name}")
    
    if module_name == "Tagebuch öffnen":
        handle_diary_module()
    elif module_name == "Galgenhumor-Modus":
        handle_humor_module()
    elif module_name == "Therapie-Minispiel":
        handle_game_module()
    elif module_name == "Etwas fühlen":
        handle_emotions_module()
    elif module_name == "Etwas verstehen":
        handle_cognitive_module()
    elif module_name == "Innere Anteile besuchen":
        handle_parts_module()

def handle_diary_module():
    """Tagebuch-Modul mit erweiterten Funktionen"""
    st.markdown("### 📝 Digitales Seelen-Archiv")
    
    tab1, tab2, tab3 = st.tabs(["✍️ Neuer Eintrag", "📚 Alte Einträge", "📊 Stimmungsanalyse"])
    
    with tab1:
        st.markdown("**Was geht gerade in dir vor?**")
        mood = st.select_slider(
            "Aktuelle Stimmung:",
            options=["💀 Existenzkrise", "😭 Heulkrampf", "😐 Zombie-Modus", "🙂 Geht so", "✨ Überraschend okay"],
            value="😐 Zombie-Modus"
        )
        
        entry_text = st.text_area(
            "Deine Gedanken:", 
            placeholder="Hier ist Raum für alles... wirklich alles. Auch das Chaos.",
            height=150
        )
        
        if st.button("💾 Eintrag speichern"):
            if entry_text:
                new_entry = {
                    "date": datetime.datetime.now().isoformat(),
                    "mood": mood,
                    "text": entry_text,
                    "id": len(st.session_state["diary_entries"]) + 1
                }
                st.session_state["diary_entries"].append(new_entry)
                st.success("Eintrag gespeichert! Dein Schmerz wurde digitalisiert. 📱")
                st.balloons()
    
    with tab2:
        if st.session_state["diary_entries"]:
            st.markdown("**Deine Gedanken-Sammlung:**")
            for entry in reversed(st.session_state["diary_entries"][-5:]):  # Letzte 5 Einträge
                date_str = datetime.datetime.fromisoformat(entry["date"]).strftime("%d.%m.%Y %H:%M")
                st.markdown(f"""
                <div class="diary-entry">
                <strong>{date_str}</strong> | {entry['mood']}<br>
                <em>{entry['text'][:100]}{'...' if len(entry['text']) > 100 else ''}</em>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("Noch keine Einträge. Zeit, das zu ändern! 🎭")
    
    with tab3:
        if st.session_state["diary_entries"]:
            mood_counts = {}
            for entry in st.session_state["diary_entries"]:
                mood = entry["mood"]
                mood_counts[mood] = mood_counts.get(mood, 0) + 1
            
            st.markdown("**Deine Stimmungs-Statistik:**")
            for mood, count in mood_counts.items():
                st.write(f"{mood}: {count}x")
        else:
            st.info("Keine Daten für Analyse verfügbar.")

def handle_humor_module():
    """Galgenhumor-Modul"""
    st.markdown("### 😅 Therapie durch Sarkasmus")
    
    quote_type = st.radio("Wähle dein Gift:", ["🔥 Sarkastisch", "💪 Motivational (aber ehrlich)"])
    
    if st.button("🎲 Neue Weisheit"):
        if quote_type == "🔥 Sarkastisch":
            quote = random.choice(TherapyQuotes.SARCASTIC)
        else:
            quote = random.choice(TherapyQuotes.MOTIVATIONAL)
        
        st.markdown(f"""
        <div class="quote-box">
        "{quote}"
        <br><br>
        <small>- Dein digitaler Seelen-Klempner</small>
        </div>
        """, unsafe_allow_html=True)

def handle_game_module():
    """Therapie-Minispiel"""
    st.markdown("### 🎮 Existenzkrise: Das Spiel")
    
    if "game_score" not in st.session_state:
        st.session_state["game_score"] = 0
    
    st.markdown(f"**Score: {st.session_state['game_score']} Überlebens-Punkte**")
    
    challenges = [
        {"text": "Du stehst auf, ohne den Wecker zu verfluchen", "points": 10},
        {"text": "Du trinkst Wasser statt nur Kaffee", "points": 15},
        {"text": "Du gehst vor Mitternacht ins Bett", "points": 20},
        {"text": "Du rufst einen Freund an (nicht für eine Krise)", "points": 25},
        {"text": "Du gehst raus, ohne dass es ein Notfall ist", "points": 30}
    ]
    
    challenge = random.choice(challenges)
    
    st.markdown(f"**Heutige Challenge:** {challenge['text']}")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("✅ Geschafft!"):
            st.session_state["game_score"] += challenge["points"]
            st.success(f"+{challenge['points']} Punkte! Du lebst noch!")
            st.rerun()
    
    with col2:
        if st.button("❌ Versagt"):
            st.info("Auch okay. Morgen ist ein neuer Tag zum Versagen!")

def handle_emotions_module():
    """Emotions-Modul"""
    st.markdown("### 💙 Gefühls-Wirrwarr entwirren")
    
    st.markdown("**Wie geht es dir gerade? (ehrlich!)**")
    
    emotions = st.multiselect(
        "Wähle alle zutreffenden Gefühle:",
        ["😢 Traurig", "😰 Ängstlich", "😡 Wütend", "😴 Müde", "🤗 Einsam", 
         "😖 Überfordert", "😕 Verwirrt", "🙄 Genervt", "😌 Ruhig", "✨ Hoffnungsvoll"]
    )
    
    if emotions:
        st.markdown("**Deine Gefühlslage:**")
        for emotion in emotions:
            intensity = st.slider(f"Intensität {emotion}:", 1, 10, 5, key=f"intensity_{emotion}")
        
        if st.button("💡 Emotion verstehen"):
            st.info("Alle Gefühle sind okay! Auch die blöden. Du fühlst, also bist du. 🧠")

def handle_cognitive_module():
    """Kognitives Modul"""
    st.markdown("### 🧠 Gedanken-Detektiv")
    
    st.markdown("**Was geht dir durch den Kopf?**")
    thought = st.text_input("Dein aktueller Gedanke:", placeholder="z.B. 'Ich schaffe das nie'")
    
    if thought:
        st.markdown("**Lass uns das mal analysieren:**")
        
        distortions = st.multiselect(
            "Welche Denkfallen erkennst du?",
            ["🔮 Gedankenlesen", "🌍 Katastrophisieren", "⚫ Schwarz-Weiß-Denken", 
             "🔍 Verallgemeinern", "🎯 Personalisieren", "📊 Emotional reasoning"]
        )
        
        if st.button("🔍 Realitätscheck"):
            st.success("Gut erkannt! Gedanken sind nicht immer Fakten. Manchmal lügt unser Gehirn. 🧠")

def handle_parts_module():
    """Innere Anteile Modul"""
    st.markdown("### 🎭 Innere WG-Bewohner")
    
    st.markdown("**Wer meldet sich heute zu Wort?**")
    
    parts = {
        "👨‍💼 Der Perfektionist": "Alles muss perfect sein!",
        "😰 Der Ängstliche": "Was wenn alles schief geht?",
        "🎨 Der Kreative": "Lass uns was Schönes machen!",
        "😡 Der Wütende": "Das ist unfair!",
        "🛡️ Der Beschützer": "Ich passe auf uns auf.",
        "👶 Das innere Kind": "Ich will Spaß haben!"
    }
    
    selected_part = st.selectbox("Welcher Anteil ist aktiv?", list(parts.keys()))
    
    if selected_part:
        st.markdown(f"**{selected_part} sagt:** '{parts[selected_part]}'")
        
        response = st.text_area("Was möchtest du diesem Anteil antworten?")
        
        if response and st.button("💬 Antworten"):
            st.success("Dialog gestartet! Manchmal hilft es, mit sich selbst zu reden. 🗣️")

# Hauptlogik
def main():
    init_session_state()
    load_css()
    
    # Header
    st.markdown('<div class="main-title">Traumatisierender Taschen-Therapeut</div>', unsafe_allow_html=True)
    
    # Navigation basierend auf Status
    if not st.session_state.get("insurance"):
        st.markdown('<div class="subtitle">Bitte scanne deine Versichertenkarte, um zu starten</div>', unsafe_allow_html=True)
        versicherungswahl()
    elif not st.session_state.get("loading_done"):
        ladeanimation_mit_button()
    else:
        zeige_modulbereich()
    
    # Footer
    st.markdown("---")
    st.markdown("*Disclaimer: Diese App ersetzt keine echte Therapie. Bei ernsten Problemen wende dich an professionelle Hilfe! 🏥*")
    
    # Reset Button (versteckt)
    if st.button("🔄 Neustart", help="Alles zurücksetzen"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()

if __name__ == "__main__":
    main()
