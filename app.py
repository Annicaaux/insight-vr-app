import streamlit as st
import time
import random
import datetime

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
if "user_mood_history" not in st.session_state:
    st.session_state.user_mood_history = []
if "behavior_analyses" not in st.session_state:
    st.session_state.behavior_analyses = []
if "current_module" not in st.session_state:
    st.session_state.current_module = None

# Erweiterte CSS-Styling
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

# Titel
st.markdown('<div class="main-title gradient-text">🎧 Traumatisierender Taschen-Therapeut</div>', unsafe_allow_html=True)

# Hauptlogik
if st.session_state.insurance is None:
    # Versicherungsauswahl
    st.markdown('<div class="subtitle">🏥 Bitte wähle deine Krankenversicherung</div>', unsafe_allow_html=True)
    st.markdown("*Diese lebenswichtige Entscheidung bestimmt die Qualität deiner digitalen Seelenhygiene*")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("""
        <div class="info-box" style="text-align: center; margin-bottom: 1em;">
            <div style="font-size: 4em; margin-bottom: 0.5em;">🪪</div>
            <h3>Gesetzlich versichert</h3>
            <p style="color: #666;">Standard-Leid mit Wartezeit-Bonus</p>
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
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("💎 Privat versichert wählen", key="pkv"):
            st.session_state.insurance = "PKV"
            rerun_app()

elif not st.session_state.loading_done:
    # Ladeanimation
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
    
    for i in range(120):
        progress_bar.progress((i + 1) / 120)
        message_index = (i // 15) % len(botschaften)
        status_text.markdown(f"✨ **{botschaften[message_index]}**")
        time.sleep(0.03)
    
    if st.button("🎟️ 🚪 Wartezimmer B2.01 betreten", key="enter_therapy"):
        st.session_state.loading_done = True
        rerun_app()

else:
    # Hauptbereich - Module anzeigen
    st.markdown('<div class="main-container">', unsafe_allow_html=True)
    
    # Begrüßung
    status = st.session_state.insurance
    ticket = f"{status}-{random.randint(100000, 999999)}"
    
    if status == "GKV":
        st.markdown("## 🪪 Willkommen, geschätzter Kassenbeitragszahler!")
    else:
        st.markdown("## 💎 Willkommen, Premium-Leidender!")
    
    # Therapie-Fortschritt
    st.session_state.therapy_points += 1
    progress = min(st.session_state.therapy_points * 1.5, 100)
    
    st.markdown("### 📊 Dein seelischer Entwicklungsstand")
    col1, col2, col3 = st.columns([2, 1, 1])
    with col1:
        st.markdown(f"""
        <div class="progress-container">
            <div class="progress-bar" style="width: {progress}%"></div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.metric("Level", st.session_state.therapy_points, delta=1)
    with col3:
        next_milestone = ((st.session_state.therapy_points // 10) + 1) * 10
        remaining = next_milestone - st.session_state.therapy_points
        st.metric("Bis Level-Up", remaining)
    
    st.divider()
    
    # Module-Auswahl
    st.markdown("### 🎯 Deine heutige Therapie-Session")
    st.markdown("*Wähle dein therapeutisches Abenteuer*")
    
    # Module-Daten
    modules_data = {
        "📔 Tagebuch öffnen": {
            "description": "Digitales Seelen-Archiv",
            "subtitle": "Verwandle deine Gedanken in lesbare Verzweiflung",
            "color": "linear-gradient(135deg, #667eea, #764ba2)"
        },
        "😅 Galgenhumor-Modus": {
            "description": "Therapie durch Sarkasmus",
            "subtitle": "Lachen über das Unlachbare",
            "color": "linear-gradient(135deg, #f093fb, #f5576c)"
        },
        "🎮 Therapie-Minispiel": {
            "description": "Gamification der Existenzkrise",
            "subtitle": "Level up deine mentale Gesundheit",
            "color": "linear-gradient(135deg, #4facfe, #00f2fe)"
        },
        "💙 Etwas fühlen": {
            "description": "Emotionsregulation ohne Regulation",
            "subtitle": "Gefühls-Chaos professionell sortieren",
            "color": "linear-gradient(135deg, #a8edea, #fed6e3)"
        },
        "🧠 Etwas verstehen": {
            "description": "Kognitive Verhaltenstherapie für Dummies",
            "subtitle": "Gedanken-Detektiv werden",
            "color": "linear-gradient(135deg, #ffecd2, #fcb69f)"
        },
        "🎭 Innere Anteile besuchen": {
            "description": "Systemische Familientherapie im Kopf",
            "subtitle": "Meet & Greet mit deiner inneren WG",
            "color": "linear-gradient(135deg, #fa709a, #fee140)"
        },
        "🔬 Verhaltensanalyse": {
            "description": "Professionelle SORKC-Analyse",
            "subtitle": "Verstehe deine Reaktionsmuster wissenschaftlich",
            "color": "linear-gradient(135deg, #667eea, #764ba2)"
        }
    }
    
    # Module Grid (3x3 Layout, mittlere Spalte der letzten Reihe für Verhaltensanalyse)
    row1_cols = st.columns(3)
    row2_cols = st.columns(3)
    row3_cols = st.columns([1, 1, 1])
    
    all_cols = row1_cols + row2_cols + [row3_cols[1]]  # 7 Module total
    module_names = list(modules_data.keys())
    
    for i, (col, module_name) in enumerate(zip(all_cols, module_names)):
        module_info = modules_data[module_name]
        
        with col:
            # Module Card
            card_html = f"""
            <div class="module-card" style="background: {module_info['color']}; color: white;">
                <div class="module-icon">{module_name.split()[0]}</div>
                <h4 style="margin: 0.5em 0; font-size: 1.2em;">{module_name.split(' ', 1)[1] if ' ' in module_name else module_name}</h4>
                <p style="font-size: 0.9em; opacity: 0.9; margin: 0.5em 0;">{module_info['subtitle']}</p>
            </div>
            """
            st.markdown(card_html, unsafe_allow_html=True)
            
            if st.button(f"Starten", key=f"start_{i}", help=f"{module_info['description']}"):
                st.session_state.current_module = module_name
                rerun_app()
    
    # Modul-Inhalte anzeigen basierend auf Auswahl
    if st.session_state.current_module:
        st.markdown("---")
        module = st.session_state.current_module
        
        if "Tagebuch" in module:
            handle_diary_module()
        elif "Galgenhumor" in module:
            handle_humor_module()
        elif "Minispiel" in module:
            handle_game_module()
        elif "fühlen" in module:
            handle_emotions_module()
        elif "verstehen" in module:
            handle_cognitive_module()
        elif "Anteile" in module:
            handle_parts_module()
        elif "Verhaltensanalyse" in module:
            handle_behavior_analysis_module()
    
    st.markdown('</div>', unsafe_allow_html=True)

# Module-Handler Funktionen
def handle_diary_module():
    """Tagebuch-Modul"""
    st.markdown("### 📝 Digitales Seelen-Archiv")
    
    tab1, tab2 = st.tabs(["✍️ Neuer Eintrag", "📚 Meine Einträge"])
    
    with tab1:
        mood = st.select_slider(
            "Aktuelle Stimmung:",
            options=["💀 Existenzkrise", "😭 Heulkrampf", "😐 Zombie-Modus", "🙂 Geht so", "✨ Okay"],
            value="😐 Zombie-Modus"
        )
        
        entry_text = st.text_area(
            "Was geht gerade in dir vor?", 
            placeholder="Hier ist Raum für alles, was du fühlst...",
            height=150
        )
        
        if st.button("💾 Eintrag speichern") and entry_text:
            new_entry = {
                "date": datetime.datetime.now().strftime("%d.%m.%Y %H:%M"),
                "mood": mood,
                "text": entry_text
            }
            st.session_state.diary_entries.append(new_entry)
            st.success("Eintrag gespeichert! 📱")
            st.balloons()
    
    with tab2:
        if st.session_state.diary_entries:
            for entry in reversed(st.session_state.diary_entries[-5:]):
                st.markdown(f"""
                <div class="diary-entry">
                    <strong>{entry['date']}</strong> | {entry['mood']}<br>
                    <em>{entry['text'][:100]}{'...' if len(entry['text']) > 100 else ''}</em>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("Noch keine Einträge. Zeit, deine erste digitale Seelen-Expedition zu starten!")

def handle_humor_module():
    """Galgenhumor-Modus"""
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

def handle_game_module():
    """Therapie-Minispiel"""
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

def handle_emotions_module():
    """Emotions-Modul"""
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

def handle_cognitive_module():
    """Kognitives Modul"""
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

def handle_parts_module():
    """Innere Anteile Modul"""
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

def handle_behavior_analysis_module():
    """Verhaltensanalyse-Modul"""
    st.markdown("### 🔬 Verhaltensanalyse (SORKC-Modell)")
    st.markdown("*Verstehe deine Reaktionsmuster wissenschaftlich*")
    
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["📝 Neue Analyse", "📊 Meine Analysen", "🔍 Analysieren", "📋 Planen", "🎯 Trainieren"])
    
    with tab1:
        st.markdown("**📍 Situation (Auslöser)**")
        situation_what = st.text_area("Was ist passiert?", height=80)
        situation_when = st.text_input("Wann?", placeholder="z.B. Heute Morgen")
        situation_where = st.text_input("Wo?", placeholder="z.B. Im Büro")
        
        st.markdown("**🧠 Gedanken**")
        thoughts = st.text_area("Welche Gedanken gingen dir durch den Kopf?", height=100)
        
        st.markdown("**💙 Gefühle**")
        emotions = st.multiselect("Hauptgefühle:", ["Angst", "Traurigkeit", "Wut", "Freude", "Scham"])
        emotion_intensity = st.slider("Intensität (0-100)", 0, 100, 50)
        
        st.markdown("**🎭 Verhalten**")
        behavior = st.text_area("Was hast du konkret getan?", height=100)
        
        st.markdown("**⚡ Konsequenzen**")
        short_consequences = st.text_area("Kurzfristige Folgen:", height=60)
        long_consequences = st.text_area("Langfristige Folgen:", height=60)
        
        if st.button("💾 Analyse speichern") and situation_what and thoughts and behavior:
            new_analysis = {
                "id": len(st.session_state.behavior_analyses) + 1,
                "timestamp": datetime.datetime.now().isoformat(),
                "situation": {"what": situation_what, "when": situation_when, "where": situation_where},
                "thoughts": thoughts,
                "emotions": emotions,
                "emotion_intensity": emotion_intensity,
                "behavior": behavior,
                "short_consequences": short_consequences,
                "long_consequences": long_consequences
            }
            st.session_state.behavior_analyses.append(new_analysis)
            st.success("🎉 Verhaltensanalyse gespeichert!")
            st.balloons()
    
    with tab2:
        if st.session_state.behavior_analyses:
            st.markdown(f"**📋 {len(st.session_state.behavior_analyses)} Analyse(n) erstellt**")
            
            for analysis in reversed(st.session_state.behavior_analyses):
                timestamp = datetime.datetime.fromisoformat(analysis['timestamp'])
                date_str = timestamp.strftime("%d.%m.%Y %H:%M")
                
                with st.expander(f"#{analysis['id']} | {date_str} | {analysis['situation']['what'][:50]}..."):
                    st.markdown(f"**Situation:** {analysis['situation']['what']}")
                    st.markdown(f"**Gedanken:** {analysis['thoughts'][:100]}...")
                    st.markdown(f"**Gefühle:** {', '.join(analysis['emotions'])}")
                    st.markdown(f"**Verhalten:** {analysis['behavior'][:100]}...")
        else:
