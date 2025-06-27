import streamlit as st
import time
import random
import datetime
import json

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
def init_session_state():
    """Initialisiert alle Session State Variablen"""
    defaults = {
        "insurance": None,
        "loading_done": False,
        "show_button": False,
        "diary_entries": [],
        "therapy_points": 0,
        "game_score": 0,
        "user_mood_history": [],
        "behavior_analyses": [],
        "current_module": None,
        "training_attempts": [],
        "confirm_reset": False
    }
    
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

# Session State initialisieren
init_session_state()

# Erweiterte CSS-Styling
def load_css():
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

# CSS laden
load_css()

# Titel
st.markdown('<div class="main-title gradient-text">🎧 Traumatisierender Taschen-Therapeut</div>', unsafe_allow_html=True)

# Versicherungsauswahl Funktion
def versicherungswahl():
    """Zeigt die Versicherungsauswahl an"""
    st.markdown('<div class="subtitle">🏥 Bitte wähle deine Krankenversicherung</div>', unsafe_allow_html=True)
    st.markdown("*Diese lebenswichtige Entscheidung bestimmt die Qualität deiner digitalen Seelenhygiene*")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("""
        <div class="info-box" style="text-align: center; margin-bottom: 1em;">
            <div style="font-size: 4em; margin-bottom: 0.5em;">🪪</div>
            <h3>Gesetzlich versichert</h3>
            <p style="color: #666;">Standard-Leid mit Wartezeit-Bonus</p>
            <ul style="text-align: left; margin: 1em 0;">
                <li>6-18 Monate Wartezeit (Geduld ist eine Tugend)</li>
                <li>Grundversorgung der Verzweiflung</li>
                <li>Kostenloses Wartezimmer-Trauma</li>
                <li>Gruppentherapie mit anderen Hoffnungslosen</li>
            </ul>
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
            <ul style="text-align: left; margin: 1em 0;">
                <li>24-48h Express-Verzweiflung</li>
                <li>Designer-Therapeuten mit LinkedIn-Profil</li>
                <li>Vergoldete Taschentücher inklusive</li>
                <li>Notfall-Hotline für Existenzkrisen</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("💎 Privat versichert wählen", key="pkv"):
            st.session_state.insurance = "PKV"
            rerun_app()

# Ladeanimation Funktion
def ladeanimation_mit_button():
    """Zeigt die Ladeanimation"""
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
    
    # Simuliere erweiterten Ladevorgang
    for i in range(120):
        progress_bar.progress((i + 1) / 120)
        message_index = (i // 15) % len(botschaften)
        
        # Verschiedene Emojis für verschiedene Phasen
        if i < 30:
            emoji = "🔍"
        elif i < 60:
            emoji = "⚙️"
        elif i < 90:
            emoji = "📊"
        else:
            emoji = "✨"
            
        status_text.markdown(f"{emoji} **{botschaften[message_index]}**")
        time.sleep(0.03)
    
    st.markdown("""
    <div style="text-align: center; margin: 2em 0;">
        <p style="margin-top: 1em; font-style: italic;">
            "Der beste Zeitpunkt, einen Therapeuten zu pflanzen, war vor 20 Jahren.<br>
            Der zweitbeste Zeitpunkt ist jetzt." - Konfuzius (wahrscheinlich)
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("🎟️ 🚪 Wartezimmer B2.01 betreten", key="enter_therapy"):
        st.session_state.loading_done = True
        rerun_app()
        # Module-Handler Funktionen

def handle_diary_module():
    """Erweitetes Tagebuch-Modul"""
    st.markdown("### 📝 Digitales Seelen-Archiv")
    
    tab1, tab2, tab3 = st.tabs(["✍️ Neuer Eintrag", "📚 Meine Einträge", "📊 Stimmungs-Analytics"])
    
    with tab1:
        st.markdown("### 📝 Was bewegt dich heute?")
        
        # Erweiterte Stimmungsauswahl
        col1, col2 = st.columns([1, 2])
        
        with col1:
            st.markdown("**Aktuelle Stimmung:**")
            mood_options = {
                "💀": {"name": "Existenzkrise", "value": 1, "color": "#ff6b6b"},
                "😭": {"name": "Emotional Overload", "value": 2, "color": "#ffa8a8"},
                "😐": {"name": "Zombie-Modus", "value": 3, "color": "#74b9ff"},
                "🙂": {"name": "Geht so", "value": 4, "color": "#00cec9"},
                "✨": {"name": "Überraschend okay", "value": 5, "color": "#00b894"}
            }
            
            selected_mood = None
            for emoji, data in mood_options.items():
                if st.button(f"{emoji} {data['name']}", key=f"mood_{emoji}"):
                    selected_mood = f"{emoji} {data['name']}"
                    st.session_state.current_mood = data
        
        with col2:
            if hasattr(st.session_state, 'current_mood'):
                mood_data = st.session_state.current_mood
                st.markdown(f"""
                <div style="background: {mood_data['color']}; color: white; padding: 2em; border-radius: 15px; text-align: center;">
                    <h3>Stimmungs-Level: {mood_data['value']}/5</h3>
                    <p>Du hast "{mood_data['name']}" gewählt</p>
                    <div style="background: rgba(255,255,255,0.2); height: 10px; border-radius: 5px; margin: 1em 0;">
                        <div style="background: white; height: 100%; width: {mood_data['value']*20}%; border-radius: 5px;"></div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Kategorien für Einträge
        entry_category = st.selectbox(
            "Was für ein Eintrag wird das?",
            ["🎭 Allgemeines Chaos", "💼 Arbeitsfrust", "❤️ Beziehungsdrama", 
             "🏠 Familien-Theater", "🎯 Lebensziele", "🌙 Nächtliche Gedanken",
             "🎉 Positive Momente", "🤔 Selbstreflexion"]
        )
        
        # Intelligente Prompts basierend auf Kategorie
        prompts = {
            "🎭 Allgemeines Chaos": "Was geht gerade in deinem Kopf vor? Lass alles raus...",
            "💼 Arbeitsfrust": "Was war heute besonders nervig im Job?",
            "❤️ Beziehungsdrama": "Erzähl von deinen zwischenmenschlichen Abenteuern...",
            "🏠 Familien-Theater": "Was ist in der Familie los?",
            "🎯 Lebensziele": "Wo willst du hin? Was beschäftigt dich?",
            "🌙 Nächtliche Gedanken": "Was hält dich wach oder beschäftigt dich vor dem Schlafen?",
            "🎉 Positive Momente": "Was war heute schön oder hat dich gefreut?",
            "🤔 Selbstreflexion": "Was hast du über dich gelernt?"
        }
        
        entry_text = st.text_area(
            "Deine Gedanken:", 
            placeholder=prompts.get(entry_category, "Schreib einfach drauf los..."),
            height=200,
            help="Hier ist Platz für alles - das Chaos, die Klarheit, die Widersprüche."
        )
        
        # Tags hinzufügen
        tags = st.text_input(
            "Tags (durch Komma getrennt):",
            placeholder="z.B. stress, müde, hoffnung, arbeit",
            help="Tags helfen dir später beim Wiederfinden ähnlicher Einträge"
        )
        
        if st.button("💾 Eintrag speichern", type="primary") and entry_text:
            new_entry = {
                "date": datetime.datetime.now().isoformat(),
                "mood": selected_mood or "😐 Neutral",
                "category": entry_category,
                "text": entry_text,
                "tags": [tag.strip() for tag in tags.split(",") if tag.strip()],
                "id": len(st.session_state.diary_entries) + 1,
                "word_count": len(entry_text.split())
            }
            st.session_state.diary_entries.append(new_entry)
            st.session_state.user_mood_history.append({
                "date": datetime.datetime.now().isoformat(),
                "mood_value": getattr(st.session_state, 'current_mood', {}).get('value', 3)
            })
            
            st.success("🎉 Eintrag gespeichert! Deine Gedanken sind jetzt digital unsterblich.")
            st.balloons()
            
            # Statistik Update
            total_words = sum(entry.get('word_count', 0) for entry in st.session_state.diary_entries)
            st.info(f"📊 Das waren {len(entry_text.split())} Wörter. Insgesamt hast du schon {total_words} Wörter deiner Seele anvertraut!")
    
    with tab2:
        st.markdown("### 📚 Dein persönliches Seelen-Archiv")
        
        if st.session_state.diary_entries:
            # Filter Optionen
            col1, col2, col3 = st.columns(3)
            
            with col1:
                all_categories = list(set([entry.get('category', 'Unbekannt') for entry in st.session_state.diary_entries]))
                selected_categories = st.multiselect("Nach Kategorie filtern:", all_categories, default=all_categories)
            
            with col2:
                all_tags = list(set([tag for entry in st.session_state.diary_entries for tag in entry.get('tags', [])]))
                if all_tags:
                    selected_tags = st.multiselect("Nach Tags filtern:", all_tags)
                else:
                    selected_tags = []
            
            with col3:
                sort_option = st.selectbox("Sortieren nach:", ["Neueste zuerst", "Älteste zuerst"])
            
            # Gefilterte Einträge
            filtered_entries = [
                entry for entry in st.session_state.diary_entries
                if entry.get('category', 'Unbekannt') in selected_categories
                and (not selected_tags or any(tag in entry.get('tags', []) for tag in selected_tags))
            ]
            
            if sort_option == "Neueste zuerst":
                filtered_entries = sorted(filtered_entries, key=lambda x: x['date'], reverse=True)
            else:
                filtered_entries = sorted(filtered_entries, key=lambda x: x['date'])
            
            st.markdown(f"**{len(filtered_entries)} Einträge gefunden**")
            
            # Einträge anzeigen
            for i, entry in enumerate(filtered_entries[:10]):
                date_str = datetime.datetime.fromisoformat(entry["date"]).strftime("%d.%m.%Y um %H:%M")
                
                with st.expander(f"📅 {date_str} | {entry.get('category', 'Unbekannt')} | {entry['mood']}"):
                    st.markdown(f"**{entry['text'][:100]}{'...' if len(entry['text']) > 100 else ''}**")
                    
                    if st.button(f"📖 Vollständig lesen", key=f"read_full_{i}"):
                        st.markdown(f"""
                        <div class="diary-entry">
                            <h4>{entry.get('category', 'Eintrag')} vom {date_str}</h4>
                            <p><strong>Stimmung:</strong> {entry['mood']}</p>
                            <p><strong>Text:</strong><br>{entry['text']}</p>
                            {f"<p><strong>Tags:</strong> {', '.join(entry.get('tags', []))}</p>" if entry.get('tags') else ""}
                            <p><strong>Wörter:</strong> {entry.get('word_count', 'Unbekannt')}</p>
                        </div>
                        """, unsafe_allow_html=True)
        else:
            st.info("📝 Noch keine Einträge vorhanden. Zeit, deine erste digitale Seelen-Expedition zu starten!")
    
    with tab3:
        st.markdown("### 📊 Deine Stimmungs-Reise")
        
        if st.session_state.diary_entries:
            # Stimmungsverteilung
            mood_counts = {}
            category_counts = {}
            
            for entry in st.session_state.diary_entries:
                mood = entry['mood']
                category = entry.get('category', 'Unbekannt')
                mood_counts[mood] = mood_counts.get(mood, 0) + 1
                category_counts[category] = category_counts.get(category, 0) + 1
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**🎭 Stimmungsverteilung:**")
                for mood, count in mood_counts.items():
                    percentage = (count / len(st.session_state.diary_entries)) * 100
                    st.markdown(f"{mood}: {count}x ({percentage:.1f}%)")
            
            with col2:
                st.markdown("**📁 Kategorien-Verteilung:**")
                for category, count in category_counts.items():
                    percentage = (count / len(st.session_state.diary_entries)) * 100
                    st.markdown(f"{category}: {count}x ({percentage:.1f}%)")
            
            # Schreibstatistiken
            total_words = sum(entry.get('word_count', 0) for entry in st.session_state.diary_entries)
            avg_words = total_words / len(st.session_state.diary_entries) if st.session_state.diary_entries else 0
            
            st.markdown("---")
            st.markdown("### 📈 Deine Schreib-Statistiken")
            
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("Einträge gesamt", len(st.session_state.diary_entries))
            col2.metric("Wörter gesamt", total_words)
            col3.metric("⌀ Wörter/Eintrag", f"{avg_words:.0f}")
            col4.metric("Längster Eintrag", max([entry.get('word_count', 0) for entry in st.session_state.diary_entries]) if st.session_state.diary_entries else 0)
        else:
            st.info("📊 Noch keine Daten für Analysen. Schreib ein paar Einträge und komm zurück!")

def handle_humor_module():
    """Galgenhumor-Modus mit mehr Interaktivität"""
    st.markdown("### 😅 Therapie durch Sarkasmus")
    
    tab1, tab2 = st.tabs(["🎲 Zufallsweisheiten", "🎭 Interaktiver Humor"])
    
    with tab1:
        st.markdown("### 😅 Digitale Weisheiten für die Seele")
        
        humor_categories = {
            "🔥 Sarkastisch": [
                "Schön, dass du es heute geschafft hast, nicht komplett durchzudrehen. Fortschritt ist relativ.",
                "Deine Probleme sind einzigartig - genau wie die von 8 Milliarden anderen Menschen.",
                "Wartezeit ist Therapie-Zeit! Du übst schon mal das Warten auf Besserung.",
                "Vergiss nicht: Auch Sisyphos hatte schlechte Tage. Aber er hatte wenigstens einen Stein.",
                "Deine Selbstzweifel sind berechtigt - das ist schon mal ein Fortschritt in der Selbstwahrnehmung.",
                "Perfektionismus ist der Versuch, den unmöglichen Standard zu erreichen, den niemand verlangt hat.",
                "Du bist nicht verrückt. Die Welt ist es. Du bemerkst es nur als einer der wenigen."
            ],
            "💪 Motivational (aber ehrlich)": [
                "Du bist stärker als du denkst. Wahrscheinlich. Vielleicht. Hoffen wir es mal.",
                "Heute ist ein neuer Tag voller neuer Möglichkeiten... zu versagen. Aber auch zu wachsen!",
                "Remember: Even professional therapists need therapy. Du bist in guter Gesellschaft.",
                "Jeder Schritt zählt, auch wenn er rückwärts ist - du bewegst dich wenigstens.",
                "Du machst das Beste aus deiner Situation. Dass das nicht viel ist, ist nicht deine Schuld.",
                "Authentizität bedeutet, ehrlich über dein Chaos zu sein. Du bist sehr authentisch!",
                "Du überlebst 100% deiner schlechtesten Tage. Das ist eine beeindruckende Erfolgsquote."
            ],
            "🏥 Therapie-Insider": [
                "Dein Therapeut googelt auch erstmal deine Symptome. Ihr seid quitt.",
                "50 Minuten Therapie, 10 Minuten Notizen: 'Patient lebt noch. Fortschritt unklar.'",
                "Therapie ist bezahlte Freundschaft mit professioneller Schweigepflicht.",
                "Dein Therapeut denkt auch manchmal 'Was zur Hölle mache ich hier?'",
                "Die beste Therapie ist oft einfach jemand, der zuhört, ohne sofort Lösungen anzubieten.",
                "Therapieerfolg wird daran gemessen, dass du deine Probleme besser erträgst, nicht dass sie verschwinden."
            ]
        }
        
        col1, col2 = st.columns([1, 2])
        
        with col1:
            selected_category = st.selectbox(
                "Wähle deinen Humor-Style:",
                list(humor_categories.keys())
            )
            
            mood_modifier = st.slider(
                "Sarkasmus-Level:",
                1, 10, 5,
                help="1 = Sanft ironisch, 10 = Brutal ehrlich"
            )
        
        with col2:
            if st.button("🎲 Neue Weisheit generieren", type="primary"):
                quotes = humor_categories[selected_category]
                selected_quote = random.choice(quotes)
                
                # Modifiziere Quote basierend auf Sarkasmus-Level
                if mood_modifier <= 3:
                    prefix = "💝 Sanfte Erinnerung: "
                elif mood_modifier <= 7:
                    prefix = "💭 Kleine Wahrheit: "
                else:
                    prefix = "🔥 Harte Realität: "
                
                st.markdown(f"""
                <div class="quote-box">
                    <h4>{prefix}</h4>
                    <p style="font-size: 1.2em; margin: 1em 0;">"{selected_quote}"</p>
                    <div style="text-align: right; opacity: 0.8;">
                        — Dein digitaler Seelen-Klempner<br>
                        <small>Sarkasmus-Level: {mood_modifier}/10</small>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                # Bonus-Features basierend auf Level
                if mood_modifier >= 8:
                    st.warning("⚠️ Das war jetzt ziemlich direkt. Brauchst du eine virtuelle Umarmung? 🤗")
                elif mood_modifier <= 2:
                    st.info("🌸 Das war jetzt sehr sanft. Du bist heute in liebevoller Stimmung!")
    
    with tab2:
        st.markdown("### 🎭 Interaktiver Sarkasmus-Generator")
        
        # Situation eingeben
        situation = st.text_input(
            "Beschreib deine aktuelle Situation:",
            placeholder="z.B. 'Mein Chef nervt', 'Ich bin müde', 'Alles ist zu viel'"
        )
        
        if situation and st.button("🎯 Maßgeschneiderten Kommentar generieren"):
            # Intelligente Antworten basierend auf Keywords
            responses = {
                "chef": [
                    f"Ah, {situation}? Schockierend! Ein Chef, der nervt. Das ist ja noch nie dagewesen.",
                    f"'{situation}' - Vielleicht ist dein Chef auch nur ein Mensch mit eigenen Problemen. Aber heute nervt er trotzdem.",
                    f"Pro-Tipp: Stell dir vor, dein Chef ist ein NPC in deinem Lebensspiel. Macht ihn weniger real, aber nicht weniger nervig."
                ],
                "müde": [
                    f"'{situation}' - Join the club! Müdigkeit ist der neue Normalzustand der Menschheit.",
                    f"Müde sein ist ein Zeichen dafür, dass du lebst und arbeitest. Oder einfach existierst. Das reicht schon.",
                    f"Fun Fact: Auch Kaffee wird irgendwann müde. Du bist in guter Gesellschaft."
                ],
                "viel": [
                    f"'{situation}' - Das Leben hat vergessen, dass du nur ein Mensch bist, kein Superheld.",
                    f"Zu viel ist das neue Normal. Willkommen in der Überforderungs-Gesellschaft!",
                    f"Plot Twist: 'Zu viel' ist subjektiv. Für eine Ameise wäre dein Tag unmöglich."
                ]
            }
            
            # Finde passende Kategorie
            situation_lower = situation.lower()
            if any(word in situation_lower for word in ["chef", "boss", "arbeit", "job"]):
                category_responses = responses["chef"]
            elif any(word in situation_lower for word in ["müde", "erschöpft", "schlaf"]):
                category_responses = responses["müde"]
            elif any(word in situation_lower for word in ["viel", "stress", "überfordert", "chaos"]):
                category_responses = responses["viel"]
            else:
                category_responses = [
                    f"'{situation}' - Klingt herausfordernd! Aber hey, du bist hier und beschreibst es. Das ist schon was.",
                    f"'{situation}' - Manchmal ist das Leben wie ein schlechter Film, nur dass du nicht gehen kannst.",
                    f"'{situation}' - Das klingt nach einem typischen Menschlichkeits-Problem. Du bist sehr menschlich!"
                ]
            
            response = random.choice(category_responses)
            
            st.markdown(f"""
            <div class="quote-box">
                <h4>🎯 Maßgeschneiderter Kommentar:</h4>
                <p style="font-size: 1.1em;">"{response}"</p>
                <small>— Dein persönlicher Sarkasmus-Assistent</small>
            </div>
            """, unsafe_allow_html=True)

def handle_game_module():
    """Erweiterte Gamification mit mehr Spielelementen"""
    st.markdown("### 🎮 Existenzkrise: Das Spiel")
    st.markdown("*Level up deine mentale Gesundheit mit Style!*")
    
    # Aktueller Score und Level
    level = st.session_state.game_score // 100 + 1
    progress_in_level = st.session_state.game_score % 100
    next_level_points = 100 - progress_in_level
    
    col1, col2, col3 = st.columns(3)
    col1.metric("🎯 Aktuelle Punkte", st.session_state.game_score)
    col2.metric("⭐ Level", level)
    col3.metric("📈 Bis nächstes Level", next_level_points)
    
    # Level Progress Bar
    st.markdown(f"""
    <div class="progress-container">
        <div class="progress-bar" style="width: {progress_in_level}%"></div>
    </div>
    <p style="text-align: center; margin-top: 0.5em;">Level {level} Progress: {progress_in_level}/100</p>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Tägliche Challenges
    st.markdown("### 🌟 Heute verfügbare Missionen")
    
    challenges = {
        "Anfänger": [
            {"text": "Steh auf, ohne den Wecker zu verfluchen", "points": 10, "icon": "🌅"},
            {"text": "Trink ein Glas Wasser (nicht nur Kaffee)", "points": 10, "icon": "💧"},
            {"text": "Mach das Bett (oder tu wenigstens so)", "points": 15, "icon": "🛏️"},
            {"text": "Sag 'Danke' zu jemandem", "points": 15, "icon": "🙏"}
        ],
        "Fortgeschritten": [
            {"text": "Geh 15 Minuten spazieren", "points": 25, "icon": "🚶"},
            {"text": "Ruf einen Freund an (nicht für eine Krise)", "points": 30, "icon": "📞"},
            {"text": "Mach etwas, was du aufgeschoben hast", "points": 35, "icon": "✅"},
            {"text": "Meditiere 5 Minuten", "points": 25, "icon": "🧘"}
        ],
        "Experte": [
            {"text": "Geh vor 23 Uhr ins Bett", "points": 40, "icon": "🌙"},
            {"text": "Koche etwas Gesundes", "points": 45, "icon": "👨‍🍳"},
            {"text": "Mach Sport (auch 5 Liegestütze zählen)", "points": 50, "icon": "💪"},
            {"text": "Schreib jemandem eine nette Nachricht", "points": 35, "icon": "💌"}
        ]
    }
    
    for difficulty, challenge_list in challenges.items():
        with st.expander(f"🎲 {difficulty}-Missionen", expanded=(difficulty == "Anfänger")):
            challenge = random.choice(challenge_list)
            
            col1, col2 = st.columns([3, 1])
            
            with col1:
                st.markdown(f"""
                <div style="background: rgba(255,255,255,0.1); padding: 1em; border-radius: 10px; margin: 0.5em 0;">
                    <h4>{challenge['icon']} {challenge['text']}</h4>
                    <p>Belohnung: <strong>{challenge['points']} Punkte</strong></p>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                if st.button("✅ Geschafft!", key=f"{difficulty}_success"):
                    st.session_state.game_score += challenge["points"]
                    
                    # Level-up Check
                    new_level = st.session_state.game_score // 100 + 1
                    if new_level > level:
                        st.balloons()
                        st.success(f"🎉 LEVEL UP! Du bist jetzt Level {new_level}!")
                    else:
                        st.success(f"🌟 +{challenge['points']} Punkte! Gut gemacht!")
                
                if st.button("❌ Nicht heute", key=f"{difficulty}_fail"):
                    encouraging_messages = [
                        "Auch okay! Morgen ist ein neuer Tag zum Versagen... äh, Versuchen!",
                        "Kein Problem! Selbsterkenntnis ist auch eine Art von Fortschritt.",
                        "Ehrlichkeit ist die beste Politik. Auch gegenüber dir selbst!",
                        "Das Leben ist kein Sprint. Manchmal ist es ein sehr langsamer Spaziergang."
                    ]
                    st.info(random.choice(encouraging_messages))
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
            
            # Speichere Emotionsdaten
            emotion_entry = {
                "timestamp": datetime.datetime.now().isoformat(),
                "emotions": emotions,
                "intensities": {emotion: st.session_state[emotion] for emotion in emotions}
            }
            st.session_state.user_mood_history.append(emotion_entry)

def handle_cognitive_module():
    """Kognitives Modul"""
    st.markdown("### 🧠 Gedanken-Detektiv")
    
    thought = st.text_input("Was geht dir durch den Kopf?", 
                           placeholder="z.B. 'Ich schaffe das nie'")
    
    if thought:
        distortions = st.multiselect(
            "Welche Denkfallen erkennst du?",
            ["🔮 Gedankenlesen", "🌍 Katastrophisieren", 
             "⚫ Schwarz-Weiß-Denken", "🔍 Verallgemeinern",
             "🎯 Personalisierung", "📊 Emotional Reasoning"]
        )
        
        if st.button("🔍 Realitätscheck"):
            st.success("Gut! Gedanken sind nicht immer Fakten. 🧠")
            
            # Hilfreiche Fragen
            questions = [
                "Welche Beweise sprechen DAFÜR?",
                "Welche Beweise sprechen DAGEGEN?", 
                "Was würdest du einem Freund in derselben Lage sagen?",
                "Wie wahrscheinlich ist das wirklich (0-100%)?"
            ]
            
            for question in questions:
                st.markdown(f"**💭 {question}**")
                answer = st.text_input(f"Antwort:", key=f"q_{question[:10]}")

def handle_parts_module():
    """Innere Anteile Modul"""
    st.markdown("### 🎭 Innere WG-Bewohner")
    
    parts = {
        "👨‍💼 Der Perfektionist": {
            "description": "Alles muss perfekt sein!",
            "positive": "Sorgt für Qualität",
            "shadow": "Kann zu Selbstkritik führen"
        },
        "😰 Der Ängstliche": {
            "description": "Was wenn alles schief geht?",
            "positive": "Beschützt vor Gefahren", 
            "shadow": "Kann übervorsichtig machen"
        },
        "🎨 Der Kreative": {
            "description": "Lass uns was Schönes machen!",
            "positive": "Bringt Freude ins Leben",
            "shadow": "Kann impulsiv sein"
        },
        "😡 Der Wütende": {
            "description": "Das ist unfair!",
            "positive": "Setzt Grenzen",
            "shadow": "Kann verletzend sein"
        },
        "👶 Das innere Kind": {
            "description": "Ich will Spaß haben!",
            "positive": "Bringt Spontaneität",
            "shadow": "Kann unreif reagieren"
        }
    }
    
    selected_part = st.selectbox("Wer meldet sich?", list(parts.keys()))
    
    if selected_part:
        part_info = parts[selected_part]
        
        st.markdown(f"""
        <div class="info-box">
            <h4>{selected_part}</h4>
            <p><strong>Sagt:</strong> "{part_info['description']}"</p>
            <p><strong>Positive Funktion:</strong> {part_info['positive']}</p>
            <p><strong>Schattenseite:</strong> {part_info['shadow']}</p>
        </div>
        """, unsafe_allow_html=True)
        
        response = st.text_area("Was antwortest du diesem Anteil?")
        
        if response and st.button("💬 Antworten"):
            st.success("Dialog gestartet! 🗣️")
            
            # Speichere Dialog
            if "inner_dialogues" not in st.session_state:
                st.session_state.inner_dialogues = []
            
            st.session_state.inner_dialogues.append({
                "timestamp": datetime.datetime.now().isoformat(),
                "part": selected_part,
                "user_response": response
            })

def handle_behavior_analysis_module():
    """Verhaltensanalyse-Modul mit vollständigem SORKC"""
    st.markdown("### 🔬 Verhaltensanalyse (SORKC-Modell)")
    st.markdown("*Verstehe deine Reaktionsmuster wissenschaftlich*")
    
    # Informationsbox über SORKC
    with st.expander("ℹ️ Was ist eine Verhaltensanalyse?"):
        st.markdown("""
        **SORKC-Modell:**
        - **S**ituation: Was war der Auslöser?
        - **O**rganismus: Deine Tagesform und Grundeinstellungen  
        - **R**eaktion: Gedanken, Gefühle, Körper, Verhalten
        - **K**onsequenzen: Kurzfristige Folgen
        - **C**onsequences: Langfristige Folgen
        
        Ziel: Verstehe deine automatischen Reaktionen und entwickle Alternativen.
        """)
    
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["📝 Neue Analyse", "📊 Meine Analysen", "🔍 Analysieren", "📋 Planen", "🎯 Trainieren"])
    
    with tab1:
        st.markdown("### 📝 Neue Verhaltensanalyse erstellen")
        
        with st.form("behavior_analysis_form"):
            st.markdown("**📍 SITUATION (Auslöser)**")
            col1, col2 = st.columns(2)
            
            with col1:
                situation_when = st.text_input("Wann?", placeholder="z.B. Heute Morgen, 14:30 Uhr")
                situation_where = st.text_input("Wo?", placeholder="z.B. Im Büro, zu Hause")
            
            with col2:
                situation_who = st.text_input("Wer war dabei?", placeholder="z.B. Kollegen, Familie, allein")
                situation_what = st.text_area("Was ist passiert?", height=80)
            
            st.markdown("**🧠 ORGANISMUS-VARIABLEN (Deine Verfassung)**")
            col1, col2 = st.columns(2)
            
            with col1:
                mood_scale = st.slider("Stimmung (0-10)", 0, 10, 5)
                energy_level = st.selectbox("Energielevel", ["Sehr müde", "Etwas müde", "Normal", "Energetisch", "Sehr energetisch"])
                stress_level = st.selectbox("Stress-Level", ["Entspannt", "Leicht angespannt", "Gestresst", "Sehr gestresst", "Überwältigt"])
            
            with col2:
                belief_patterns = st.multiselect(
                    "Aktive Denkmuster:",
                    ["Perfektionismus", "Katastrophisieren", "Schwarz-Weiß-Denken", 
                     "Selbstkritik", "Sorgen um andere", "Kontrollbedürfnis"]
                )
                other_beliefs = st.text_input("Andere Denkmuster:")
            
            st.markdown("**🧩 REAKTIONEN**")
            
            # Gedanken
            thoughts = st.text_area("💭 Gedanken:", height=100)
            
            # Gefühle
            col1, col2 = st.columns(2)
            with col1:
                primary_emotions = st.multiselect("💙 Hauptgefühle:", 
                    ["Angst", "Traurigkeit", "Wut", "Freude", "Scham", "Schuld", "Enttäuschung", "Frustration"])
            with col2:
                emotion_intensity = st.slider("Intensität (0-100)", 0, 100, 50)
            
            # Körperempfindungen
            col1, col2 = st.columns(2)
            with col1:
                body_sensations = st.multiselect("🫀 Körperliche Reaktionen:",
                    ["Herzklopfen", "Schwitzen", "Zittern", "Bauchschmerzen", "Kopfschmerzen", "Muskelverspannungen"])
            with col2:
                tension_level = st.slider("Anspannung (0-100)", 0, 100, 50)
            
            # Verhalten
            behavior_description = st.text_area("🎭 Beobachtbares Verhalten:", height=100)
            
            st.markdown("**⚡ KONSEQUENZEN**")
            short_term_consequences = st.text_area("🔄 Kurzfristige Konsequenzen (sofort):", height=80)
            long_term_consequences = st.text_area("📈 Langfristige Folgen (Stunden/Tage):", height=80)
            
            # Submit Button
            submitted = st.form_submit_button("💾 Analyse speichern", type="primary")
            
            if submitted and situation_what and thoughts and behavior_description:
                new_analysis = {
                    "id": len(st.session_state.behavior_analyses) + 1,
                    "timestamp": datetime.datetime.now().isoformat(),
                    "situation": {
                        "when": situation_when,
                        "where": situation_where, 
                        "who": situation_who,
                        "what": situation_what
                    },
                    "organism_variables": {
                        "mood_scale": mood_scale,
                        "energy_level": energy_level,
                        "stress_level": stress_level,
                        "belief_patterns": belief_patterns,
                        "other_beliefs": other_beliefs
                    },
                    "reactions": {
                        "thoughts": thoughts,
                        "emotions": primary_emotions,
                        "emotion_intensity": emotion_intensity,
                        "body_sensations": body_sensations,
                        "tension_level": tension_level,
                        "behavior": behavior_description
                    },
                    "consequences": {
                        "short_term": short_term_consequences,
                        "long_term": long_term_consequences
                    },
                    "analysis_phase": "documented"
                }
                
                st.session_state.behavior_analyses.append(new_analysis)
                st.success("🎉 Verhaltensanalyse gespeichert!")
                st.balloons()
            elif submitted:
                st.error("⚠️ Bitte fülle mindestens 'Situation', 'Gedanken' und 'Verhalten' aus.")
    
    with tab2:
        st.markdown("### 📊 Meine Verhaltensanalysen")
        
        if st.session_state.behavior_analyses:
            total_analyses = len(st.session_state.behavior_analyses)
            analyzed_count = len([a for a in st.session_state.behavior_analyses if a.get('analysis_phase') != 'documented'])
            
            col1, col2 = st.columns(2)
            col1.metric("📝 Gesamt", total_analyses)
            col2.metric("🔍 Bearbeitet", analyzed_count)
            
            st.markdown("**📋 Deine Analysen:**")
            
            for analysis in reversed(st.session_state.behavior_analyses):
                timestamp = datetime.datetime.fromisoformat(analysis['timestamp'])
                date_str = timestamp.strftime("%d.%m.%Y %H:%M")
                
                phase = analysis.get('analysis_phase', 'documented')
                phase_colors = {'documented': '#74b9ff', 'analyzed': '#fdcb6e', 'planned': '#e17055', 'trained': '#00b894'}
                phase_names = {'documented': '📝 Dokumentiert', 'analyzed': '🔍 Analysiert', 'planned': '📋 Geplant', 'trained': '🎯 Trainiert'}
                
                with st.expander(f"#{analysis['id']} | {date_str} | {analysis['situation']['what'][:50]}..."):
                    # Status Badge
                    st.markdown(f"""
                    <div style="background: {phase_colors.get(phase, '#ddd')}; color: white; padding: 0.5em 1em; border-radius: 20px; display: inline-block; margin-bottom: 1em;">
                        {phase_names.get(phase, 'Unbekannt')}
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Zusammenfassung
                    st.markdown("**📍 Situation:**")
                    st.write(f"• {analysis['situation']['what']}")
                    st.markdown("**🧠 Gedanken:**")
                    st.write(f"• {analysis['reactions']['thoughts'][:100]}...")
                    st.markdown("**🎭 Verhalten:**")
                    st.write(f"• {analysis['reactions']['behavior'][:100]}...")
        else:
            st.info("📝 Noch keine Verhaltensanalysen erstellt.")
    
    with tab3:
        st.markdown("### 🔍 Analyse bewerten")
        
        if st.session_state.behavior_analyses:
            # Auswahl einer Analyse
            analysis_options = []
            for analysis in st.session_state.behavior_analyses:
                timestamp = datetime.datetime.fromisoformat(analysis['timestamp'])
                date_str = timestamp.strftime("%d.%m.%Y")
                analysis_options.append(f"#{analysis['id']} - {date_str} - {analysis['situation']['what'][:30]}...")
            
            if analysis_options:
                selected_idx = st.selectbox("Welche Analyse bewerten?", range(len(analysis_options)), 
                                          format_func=lambda x: analysis_options[x])
                
                selected_analysis = st.session_state.behavior_analyses[selected_idx]
                
                st.markdown("**✅❌ Bewerte deine Reaktionen:**")
                
                # Bewertungskategorien
                categories = ["Gedanken", "Gefühle", "Verhalten", "Kurzfristige Folgen", "Langfristige Folgen"]
                
                helpful_ratings = {}
                for category in categories:
                    col1, col2, col3 = st.columns([2, 1, 1])
                    
                    with col1:
                        st.markdown(f"**{category}**")
                    
                    with col2:
                        if st.button(f"✅ Hilfreich", key=f"helpful_{category}"):
                            helpful_ratings[category] = "helpful"
                            st.success(f"{category} als hilfreich markiert!")
                    
                    with col3:
                        if st.button(f"❌ Weniger hilfreich", key=f"unhelpful_{category}"):
                            helpful_ratings[category] = "unhelpful"
                            st.warning(f"{category} als weniger hilfreich markiert!")
                
                # Ausstiegspunkte
                st.markdown("**🚪 Ausstiegspunkte identifizieren:**")
                exit_points = st.multiselect("Wo hättest du aussteigen können?", 
                    ["🔔 Frühwarnung", "🧠 Gedanken stoppen", "💙 Gefühle regulieren", 
                     "🫀 Körper beruhigen", "🎭 Verhalten ändern", "⏸️ Pause einlegen"])
                
                if st.button("💾 Bewertung speichern"):
                    selected_analysis['helpful_aspects'] = helpful_ratings
                    selected_analysis['exit_points'] = exit_points
                    selected_analysis['analysis_phase'] = 'analyzed'
                    st.success("🎯 Analyse bewertet!")
        else:
            st.info("Erstelle erst eine Analyse!")
    
    with tab4:
        st.markdown("### 📋 Alternative Reaktionen planen")
        
        analyzed_analyses = [a for a in st.session_state.behavior_analyses if a.get('analysis_phase') in ['analyzed', 'planned', 'trained']]
        
        if analyzed_analyses:
            st.markdown("**🔄 Entwickle bessere Alternativen:**")
            
            alternative_thoughts = st.text_area("Alternative Gedanken:", 
                                              placeholder="z.B. 'Ich kann das Schritt für Schritt angehen'")
            alternative_behavior = st.text_area("Alternatives Verhalten:", 
                                              placeholder="z.B. 'Tief durchatmen und um Hilfe bitten'")
            implementation_plan = st.text_area("Umsetzungsplan:",
                                             placeholder="Wie willst du das konkret üben?")
            
            if st.button("💾 Plan speichern") and alternative_thoughts and alternative_behavior:
                # Speichere bei der letzten analysierten Analyse
                analyzed_analyses[-1]['planned_alternatives'] = {
                    "thoughts": alternative_thoughts,
                    "behavior": alternative_behavior,
                    "implementation": implementation_plan
                }
                analyzed_analyses[-1]['analysis_phase'] = 'planned'
                
                st.success("🎯 Alternativen geplant! Bereit für die Umsetzung!")
                st.balloons()
        else:
            st.info("Analysiere erst eine Verhaltensanalyse!")
    
    with tab5:
        st.markdown("### 🎯 Veränderungen trainieren")
        
        planned_analyses = [a for a in st.session_state.behavior_analyses if a.get('analysis_phase') in ['planned', 'trained']]
        
        if planned_analyses:
            st.markdown("**📋 Dokumentiere deine Trainingsversuche:**")
            
            training_situation = st.text_area("In welcher Situation hast du es versucht?")
            what_tried = st.text_area("Was hast du ausprobiert?")
            success_rating = st.slider("Wie gut hat es funktioniert? (0-100%)", 0, 100, 50)
            
            what_learned = st.text_area("Was hast du gelernt?", 
                                      placeholder="z.B. 'Ich brauche mehr Übung' oder 'Es hat besser funktioniert als erwartet'")
            
            if st.button("⭐ Trainingsversuch dokumentieren") and training_situation and what_tried:
                new_attempt = {
                    "date": datetime.datetime.now().strftime("%d.%m.%Y"),
                    "situation": training_situation,
                    "what_tried": what_tried,
                    "success_rating": success_rating,
                    "learned": what_learned,
                    "timestamp": datetime.datetime.now().isoformat()
                }
                st.session_state.training_attempts.append(new_attempt)
                
                # Update Analysis Phase
                planned_analyses[-1]['analysis_phase'] = 'trained'
                
                st.success("🌟 Trainingsversuch dokumentiert!")
                st.balloons()
                
                # Motivierendes Feedback
                if success_rating >= 70:
                    st.success("🎉 Das war ein großer Erfolg!")
                elif success_rating >= 40:
                    st.info("👍 Guter Versuch! Jeder Schritt zählt!")
                else:
                    st.info("💪 Dranbleiben! Veränderung braucht Zeit!")
                
                # Erfolgs-Stern
                st.markdown("### ⭐ Trainings-Stern erhalten! ⭐")
            
            # Bisherige Versuche anzeigen
            if st.session_state.training_attempts:
                st.markdown("---")
                st.markdown("**📈 Deine Trainings-Historie:**")
                
                for attempt in reversed(st.session_state.training_attempts[-3:]):
                    st.markdown(f"""
                    <div class="diary-entry">
                        <strong>{attempt['date']}</strong> | Erfolg: {attempt['success_rating']}%<br>
                        <strong>Situation:</strong> {attempt['situation'][:100]}...<br>
                        <strong>Versucht:</strong> {attempt['what_tried'][:100]}...<br>
                        <strong>Gelernt:</strong> {attempt['learned'][:100]}...
                    </div>
                    """, unsafe_allow_html=True)
                
                # Erfolgsstatistiken
                if len(st.session_state.training_attempts) >= 2:
                    avg_success = sum(a['success_rating'] for a in st.session_state.training_attempts) / len(st.session_state.training_attempts)
                    st.metric("📊 Durchschnittlicher Erfolg", f"{avg_success:.0f}%")
        else:
            st.info("Plane erst alternative Reaktionen!")
            # Hauptlogik der App
def main_app_logic():
    """Hauptlogik basierend auf App-Status"""
    
    if st.session_state.insurance is None:
        # Versicherungsauswahl anzeigen
        versicherungswahl()
        
    elif not st.session_state.loading_done:
        # Ladeanimation anzeigen
        ladeanimation_mit_button()
        
    else:
        # Hauptbereich mit Modulen anzeigen
        zeige_modulbereich()

def zeige_modulbereich():
    """Hauptbereich mit allen verfügbaren Modulen"""
    st.markdown('<div class="main-container">', unsafe_allow_html=True)
    
    # Begrüßung basierend auf Versicherung
    status = st.session_state.insurance
    ticket = f"{status}-{random.randint(100000, 999999)}"
    
    # Tageszeit-abhängige Begrüßung
    current_hour = datetime.datetime.now().hour
    if current_hour < 12:
        greeting = "Guten Morgen"
        mood_comment = "Früh übt sich, was ein Meister werden will!"
    elif current_hour < 18:
        greeting = "Guten Tag"
        mood_comment = "Die Hälfte des Tages ist geschafft!"
    else:
        greeting = "Guten Abend"
        mood_comment = "Zeit für Selbstreflexion und Entspannung."
    
    if status == "GKV":
        st.markdown(f"## 🪪 {greeting}, geschätzter Kassenbeitragszahler!")
        st.markdown(f"""
        <div class="info-box">
            <div style="display: flex; align-items: center; margin-bottom: 1em;">
                <div style="font-size: 3em; margin-right: 0.5em;">🎟️</div>
                <div>
                    <h3 style="margin: 0;">Ticket: {ticket}</h3>
                    <p style="margin: 0; color: #666;">Öffentlich-rechtliche Seelenheilkunde</p>
                </div>
            </div>
            <p style="margin-top: 1em; font-style: italic;">
                💡 <strong>Heute:</strong> {mood_comment}<br>
                Wartezeit: 6-18 Monate (perfekt für Gedulds-Training)
            </p>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"## 💎 {greeting}, Premium-Leidender!")
        st.markdown(f"""
        <div class="info-box">
            <div style="display: flex; align-items: center; margin-bottom: 1em;">
                <div style="font-size: 3em; margin-right: 0.5em;">🏆</div>
                <div>
                    <h3 style="margin: 0;">VIP-Ticket: {ticket}</h3>
                    <p style="margin: 0; color: #666;">Exklusive Seelen-Couture</p>
                </div>
            </div>
            <p style="margin-top: 1em; font-style: italic;">
                💡 <strong>Heute:</strong> {mood_comment}<br>
                Express-Service: 24-48h Wartezeit
            </p>
        </div>
        """, unsafe_allow_html=True)
    
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
    
    # Tägliches Motivations-Zitat
    motivational_quotes = [
        "Heute ist ein guter Tag, um nicht komplett durchzudrehen! 🌟",
        "Du bist stärker als deine stärkste Ausrede. Wahrscheinlich. 💪",
        "Perfektion ist überbewertet. Chaos ist authentisch! 🎨",
        "Auch Therapeuten haben Therapeuten. Du bist in guter Gesellschaft! 🤝",
        "Fortschritt ist Fortschritt, auch wenn er rückwärts ist! 🚀"
    ]
    
    daily_quote = motivational_quotes[datetime.datetime.now().day % len(motivational_quotes)]
    st.markdown(f"""
    <div class="quote-box" style="margin: 2em 0;">
        {daily_quote}
        <div style="text-align: right; margin-top: 1em; font-size: 0.9em;">
            — Dein digitaler Seelen-Coach
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.divider()
    
    # Module-Auswahl
    st.markdown("### 🎯 Deine heutige Therapie-Session")
    st.markdown("*Wähle dein therapeutisches Abenteuer – jedes Modul wurde von Experten entwickelt*")
    
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
        
        # Module Header
        module_info = modules_data[module]
        st.markdown(f"""
        <div style="background: {module_info['color']}; color: white; text-align: center; padding: 2em; border-radius: 20px; margin: 2em 0;">
            <div style="font-size: 4em; margin-bottom: 0.5em;">{module.split()[0]}</div>
            <h2 style="margin: 0;">{module.split(' ', 1)[1] if ' ' in module else module}</h2>
            <p style="opacity: 0.9; font-size: 1.1em;">{module_info['subtitle']}</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Route zu entsprechenden Handlern
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

# Footer
def show_footer():
    """Zeigt den Footer mit Disclaimer und Notfall-Kontakten"""
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; padding: 2em; background: rgba(255,255,255,0.1); border-radius: 15px; margin: 2em 0;">
        <p style="font-style: italic; margin-bottom: 1em;">
            *Disclaimer: Diese App ersetzt keine echte Therapie. Bei ernsten Problemen wende dich an professionelle Hilfe! 🏥*
        </p>
        <p style="font-size: 0.9em; opacity: 0.8;">
            <strong>Notfall-Kontakte:</strong><br>
            Telefonseelsorge: 0800 111 0 111 | Nummer gegen Kummer: 116 123 | Notfall: 112
        </p>
    </div>
    """, unsafe_allow_html=True)

# Sidebar
def show_sidebar():
    """Zeigt die Sidebar mit Einstellungen und Statistiken"""
    with st.sidebar:
        st.markdown("### 🔧 Einstellungen")
        
        # Theme Selector
        theme = st.selectbox("🎨 Theme:", ["Standard", "Dunkel", "Energisch", "Beruhigend"], key="theme_selector")
        
        # Stats
        if (st.session_state.diary_entries or st.session_state.behavior_analyses or 
            st.session_state.therapy_points > 0):
            st.markdown("---")
            st.markdown("📊 **Deine Statistiken:**")
            
            if st.session_state.diary_entries:
                st.markdown(f"• 📔 Tagebuch-Einträge: {len(st.session_state.diary_entries)}")
            
            st.markdown(f"• ⭐ Therapie-Punkte: {st.session_state.therapy_points}")
            st.markdown(f"• 🎮 Game-Score: {st.session_state.game_score}")
            
            if st.session_state.behavior_analyses:
                st.markdown(f"• 🔬 Verhaltensanalysen: {len(st.session_state.behavior_analyses)}")
            
            if st.session_state.training_attempts:
                st.markdown(f"• 🎯 Trainingsversuche: {len(st.session_state.training_attempts)}")
                
                # Erfolgsrate berechnen
                if st.session_state.training_attempts:
                    avg_success = sum(a['success_rating'] for a in st.session_state.training_attempts) / len(st.session_state.training_attempts)
                    st.markdown(f"• 📈 ⌀ Erfolgsrate: {avg_success:.0f}%")
        
        # Zurück zum Hauptmenü
        if st.session_state.current_module:
            st.markdown("---")
            if st.button("🏠 Zurück zum Hauptmenü", use_container_width=True):
                st.session_state.current_module = None
                rerun_app()
        
        # Hilfe & Info
        st.markdown("---")
        with st.expander("ℹ️ Hilfe & Info"):
            st.markdown("""
            **🎯 So funktioniert die App:**
            
            1. **Module wählen** - Klicke auf eine Modul-Karte
            2. **Features nutzen** - Tagebuch schreiben, Spiele spielen
            3. **Fortschritt verfolgen** - Deine Punkte steigen automatisch
            4. **Zurück** - Nutze den Zurück-Button für das Hauptmenü
            
            **🔬 Verhaltensanalyse:**
            - Dokumentiere problematische Situationen
            - Analysiere was hilfreich/nicht hilfreich war
            - Plane alternative Reaktionen
            - Trainiere neue Verhaltensweisen
            
            **📱 Technische Hinweise:**
            - Daten werden nur während der Session gespeichert
            - Bei Seiten-Reload gehen Daten verloren
            - Für dauerhafte Speicherung nutze den Export
            """)
        
        # Export-Funktion
        st.markdown("---")
        if st.button("📥 Daten exportieren"):
            # Erstelle einen Export der wichtigsten Daten
            export_data = {
                "diary_entries": st.session_state.diary_entries,
                "behavior_analyses": st.session_state.behavior_analyses,
                "training_attempts": st.session_state.training_attempts,
                "stats": {
                    "therapy_points": st.session_state.therapy_points,
                    "game_score": st.session_state.game_score
                },
                "export_date": datetime.datetime.now().isoformat()
            }
            
            json_string = json.dumps(export_data, indent=2, ensure_ascii=False)
            
            st.download_button(
                label="💾 JSON-Export herunterladen",
                data=json_string,
                file_name=f"therapie_export_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json"
            )
        
        # Reset mit Bestätigung
        st.markdown("---")
        if not st.session_state.confirm_reset:
            if st.button("🔄 Alles zurücksetzen", use_container_width=True):
                st.session_state.confirm_reset = True
                rerun_app()
        else:
            st.warning("⚠️ Wirklich alles löschen?")
            col1, col2 = st.columns(2)
            
            with col1:
                if st.button("✅ Ja", type="primary"):
                    # Alles löschen außer der Bestätigung
                    keys_to_keep = ["confirm_reset"]
                    for key in list(st.session_state.keys()):
                        if key not in keys_to_keep:
                            del st.session_state[key]
                    st.session_state.confirm_reset = False
                    rerun_app()
            
            with col2:
                if st.button("❌ Abbrechen"):
                    st.session_state.confirm_reset = False
                    rerun_app()

# Easter Egg
def show_easter_egg():
    """Zeigt gelegentliche motivierende Nachrichten"""
    if st.session_state.therapy_points >= 50:
        if random.random() < 0.1:  # 10% Chance
            st.toast("🎉 Du bist auf einem guten Weg! Keep going!", icon="🌟")

# Hauptausführung
def main():
    """Hauptfunktion der App"""
    # Hauptlogik ausführen
    main_app_logic()
    
    # Footer anzeigen
    show_footer()
    
    # Sidebar anzeigen
    show_sidebar()
    
    # Easter Egg prüfen
    show_easter_egg()

# App starten
if __name__ == "__main__":
    main()

# Zusätzliche Hilfsfunktionen für bessere Benutzererfahrung
def get_user_progress_summary():
    """Gibt eine Zusammenfassung des Benutzerfortschritts zurück"""
    summary = {
        "total_diary_entries": len(st.session_state.diary_entries),
        "total_behavior_analyses": len(st.session_state.behavior_analyses),
        "therapy_level": st.session_state.therapy_points // 10 + 1,
        "game_level": st.session_state.game_score // 100 + 1,
        "training_attempts": len(st.session_state.training_attempts)
    }
    return summary

def calculate_overall_engagement():
    """Berechnet das Gesamtengagement des Benutzers"""
    engagement_score = 0
    
    # Punkte für verschiedene Aktivitäten
    engagement_score += len(st.session_state.diary_entries) * 10
    engagement_score += len(st.session_state.behavior_analyses) * 25
    engagement_score += len(st.session_state.training_attempts) * 15
    engagement_score += st.session_state.game_score
    
    return engagement_score

# App-weite Konstanten
APP_VERSION = "1.0.0"
EMERGENCY_CONTACTS = {
    "Telefonseelsorge": "0800 111 0 111",
    "Nummer gegen Kummer": "116 123", 
    "Notfall": "112"
}

# Debugging-Hilfsfunktion (nur für Entwicklung)
def debug_session_state():
    """Zeigt den aktuellen Session State für Debugging"""
    if st.checkbox("🔧 Debug Mode (nur für Entwicklung)"):
        st.json(dict(st.session_state))

# Ausführung
main()
