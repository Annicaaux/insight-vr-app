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
