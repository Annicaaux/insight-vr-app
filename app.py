import streamlit as st
import time
import random
import datetime
import json

# App-Konfiguration
st.set_page_config(
    page_title="Taschen-Therapeut Pro", 
    page_icon="🧠", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# Session State initialisieren
def init_session_state():
    defaults = {
        "insurance": None,
        "loading_done": False,
        "diary_entries": [],
        "behavior_analyses": [],
        "therapy_points": 0,
        "game_score": 0,
        "current_module": None,
        "training_attempts": []
    }
    
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

init_session_state()

# Professionelles CSS
st.markdown("""
<style>
/* Basis-Styling */
.main {
    padding-top: 1rem;
}

/* Header */
.main-header {
    background: linear-gradient(90deg, #2c3e50, #3498db);
    color: white;
    padding: 2rem;
    border-radius: 10px;
    margin-bottom: 2rem;
    text-align: center;
}

.main-title {
    font-size: 2.5rem;
    font-weight: 600;
    margin-bottom: 0.5rem;
}

.subtitle {
    font-size: 1.1rem;
    opacity: 0.9;
}

/* Cards */
.info-card {
    background: white;
    border: 1px solid #e1e8ed;
    border-radius: 12px;
    padding: 1.5rem;
    margin: 1rem 0;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.module-card {
    background: white;
    border: 2px solid #e1e8ed;
    border-radius: 12px;
    padding: 1.5rem;
    margin: 1rem 0;
    text-align: center;
    transition: all 0.3s ease;
    cursor: pointer;
}

.module-card:hover {
    border-color: #3498db;
    box-shadow: 0 4px 12px rgba(52, 152, 219, 0.15);
    transform: translateY(-2px);
}

/* Buttons */
.stButton > button {
    border-radius: 8px;
    border: none;
    padding: 0.6rem 1.2rem;
    font-weight: 500;
    transition: all 0.3s ease;
}

.primary-btn {
    background: #3498db;
    color: white;
}

.secondary-btn {
    background: #95a5a6;
    color: white;
}

.success-btn {
    background: #27ae60;
    color: white;
}

/* Progress */
.progress-container {
    background: #ecf0f1;
    border-radius: 10px;
    height: 20px;
    margin: 1rem 0;
}

.progress-bar {
    background: linear-gradient(90deg, #27ae60, #2ecc71);
    height: 100%;
    border-radius: 10px;
    transition: width 0.5s ease;
}

/* Quotes */
.quote-box {
    background: #f8f9fa;
    border-left: 4px solid #3498db;
    padding: 1rem 1.5rem;
    margin: 1rem 0;
    border-radius: 0 8px 8px 0;
    font-style: italic;
}

/* Entry cards */
.entry-card {
    background: #f8f9fa;
    border: 1px solid #dee2e6;
    border-radius: 8px;
    padding: 1rem;
    margin: 0.5rem 0;
}

/* Responsive */
@media (max-width: 768px) {
    .main-title {
        font-size: 2rem;
    }
    
    .module-card {
        margin: 0.5rem 0;
    }
}
</style>
""", unsafe_allow_html=True)

# Header
def show_header():
    st.markdown("""
    <div class="main-header">
        <div class="main-title">🧠 Taschen-Therapeut Pro</div>
        <div class="subtitle">Professionelle Selbsthilfe mit einer Prise Humor</div>
    </div>
    """, unsafe_allow_html=True)

# Versicherungsauswahl
def show_insurance_selection():
    st.markdown("### 🏥 Versicherungsauswahl")
    st.markdown("*Bestimmt die Qualität deiner digitalen Betreuung*")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="info-card">
            <h4>🪪 Gesetzlich versichert</h4>
            <p><strong>Standard-Paket:</strong></p>
            <ul>
                <li>Wartezeit: 6-18 Monate</li>
                <li>Grundfunktionen verfügbar</li>
                <li>Gruppentherapie-Simulator</li>
                <li>Kostenloses Warten als Achtsamkeitsübung</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("🪪 GKV wählen", key="gkv", use_container_width=True):
            st.session_state.insurance = "GKV"
            st.rerun()
    
    with col2:
        st.markdown("""
        <div class="info-card">
            <h4>💳 Privat versichert</h4>
            <p><strong>Premium-Paket:</strong></p>
            <ul>
                <li>Wartezeit: 24-48 Stunden</li>
                <li>Alle Premium-Features</li>
                <li>Einzeltherapie-Simulation</li>
                <li>24/7 Krisenhotline-Bot</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("💳 PKV wählen", key="pkv", use_container_width=True):
            st.session_state.insurance = "PKV"
            st.rerun()

# Ladebildschirm
def show_loading():
    st.markdown("### 🔄 Analyse läuft...")
    
    messages = [
        "Scanne deine psychische Verfassung...",
        "Kalibriere Sarkasmus-Detektor...",
        "Lade Motivationssprüche...",
        "Bereite virtuelle Taschentücher vor...",
        "Fast fertig - Hoffnung wird installiert..."
    ]
    
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    for i in range(100):
        progress_bar.progress(i + 1)
        message_idx = (i // 20) % len(messages)
        status_text.text(messages[message_idx])
        time.sleep(0.02)
    
    if st.button("🚪 Praxis betreten", type="primary"):
        st.session_state.loading_done = True
        st.rerun()

# Hauptdashboard
def show_dashboard():
    # Begrüßung
    status = st.session_state.insurance
    
    if status == "GKV":
        st.success("🪪 **Status:** Kassenpatientin - Standardbetreuung aktiv")
        st.info("*Wartezeit: 6-18 Monate (nutze die Zeit für Selbstreflexion)*")
    else:
        st.success("💳 **Status:** Privatpatientin - Premium-Service aktiv")
        st.info("*Express-Termine verfügbar - Luxus-Leiden inklusive*")
    
    # Fortschritt
    progress = min(st.session_state.therapy_points * 2, 100)
    
    st.markdown("#### 📊 Therapie-Fortschritt")
    st.markdown(f"""
    <div class="progress-container">
        <div class="progress-bar" style="width: {progress}%"></div>
    </div>
    <p><strong>Level:</strong> {st.session_state.therapy_points} | <strong>Fortschritt:</strong> {progress}%</p>
    """, unsafe_allow_html=True)
    
    # Module
    st.markdown("#### 🎯 Verfügbare Module")
    
    modules = {
        "📔 Digitales Tagebuch": {
            "desc": "Strukturierte Selbstreflexion",
            "icon": "📔"
        },
        "🎮 Therapie-Spiel": {
            "desc": "Gamification für mentale Gesundheit", 
            "icon": "🎮"
        },
        "🔬 Verhaltensanalyse": {
            "desc": "SORKC-Modell für Profis",
            "icon": "🔬"
        },
        "😄 Humor-Therapie": {
            "desc": "Heilung durch gezielten Sarkasmus",
            "icon": "😄"
        },
        "🧠 Gedanken-Check": {
            "desc": "Kognitive Verzerrungen entlarven",
            "icon": "🧠"
        },
        "💙 Gefühls-Radar": {
            "desc": "Emotionale Intelligenz stärken",
            "icon": "💙"
        }
    }
    
    # Module in 2er Spalten
    cols = st.columns(2)
    
    for i, (name, info) in enumerate(modules.items()):
        with cols[i % 2]:
            if st.button(f"{info['icon']} {name}", key=f"module_{i}", use_container_width=True):
                st.session_state.current_module = name
                st.rerun()
            st.caption(info['desc'])

# Tagebuch-Modul
def show_diary_module():
    st.markdown("## 📔 Digitales Tagebuch")
    
    tab1, tab2 = st.tabs(["✍️ Neuer Eintrag", "📚 Einträge"])
    
    with tab1:
        mood = st.selectbox(
            "Aktuelle Stimmung:",
            ["😊 Gut", "😐 Neutral", "😔 Schlecht", "😤 Genervt", "🤯 Überfordert"]
        )
        
        category = st.selectbox(
            "Kategorie:",
            ["💼 Arbeit", "❤️ Beziehungen", "🏠 Familie", "🎯 Persönlich", "🎉 Positives"]
        )
        
        entry = st.text_area("Was beschäftigt dich?", height=150)
        
        if st.button("💾 Speichern", type="primary") and entry:
            new_entry = {
                "date": datetime.datetime.now().isoformat(),
                "mood": mood,
                "category": category,
                "text": entry,
                "word_count": len(entry.split())
            }
            st.session_state.diary_entries.append(new_entry)
            st.session_state.therapy_points += 1
            st.success("✅ Eintrag gespeichert!")
            st.balloons()
    
    with tab2:
        if st.session_state.diary_entries:
            st.markdown(f"**{len(st.session_state.diary_entries)} Einträge gefunden**")
            
            for entry in reversed(st.session_state.diary_entries[-5:]):
                date_str = datetime.datetime.fromisoformat(entry["date"]).strftime("%d.%m.%Y %H:%M")
                
                with st.expander(f"{entry['mood']} | {entry['category']} | {date_str}"):
                    st.write(entry['text'])
                    st.caption(f"Wörter: {entry['word_count']}")
        else:
            st.info("📝 Noch keine Einträge vorhanden.")

# Spiel-Modul
def show_game_module():
    st.markdown("## 🎮 Therapie-Spiel")
    
    level = st.session_state.game_score // 100 + 1
    points_in_level = st.session_state.game_score % 100
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Score", st.session_state.game_score)
    col2.metric("Level", level)
    col3.metric("Bis nächstes Level", 100 - points_in_level)
    
    st.markdown("#### 🎯 Tägliche Challenges")
    
    challenges = [
        {"text": "10 Minuten spazieren gehen", "points": 20},
        {"text": "Einem Freund schreiben", "points": 15},
        {"text": "Gesund kochen", "points": 25},
        {"text": "Vor 23 Uhr schlafen", "points": 30},
        {"text": "5 Minuten meditieren", "points": 15}
    ]
    
    challenge = random.choice(challenges)
    
    st.markdown(f"""
    <div class="info-card">
        <h4>🎯 Heutige Challenge</h4>
        <p><strong>{challenge['text']}</strong></p>
        <p>Belohnung: {challenge['points']} Punkte</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("✅ Geschafft!", type="primary"):
            st.session_state.game_score += challenge["points"]
            st.session_state.therapy_points += 1
            st.success(f"🎉 +{challenge['points']} Punkte!")
            st.rerun()
    
    with col2:
        if st.button("❌ Heute nicht"):
            st.info("Kein Problem! Morgen ist ein neuer Tag.")

# Verhaltensanalyse-Modul
def show_behavior_analysis():
    st.markdown("## 🔬 Verhaltensanalyse")
    st.markdown("*Wissenschaftliche Selbstanalyse nach dem SORKC-Modell*")
    
    tab1, tab2 = st.tabs(["📝 Neue Analyse", "📊 Meine Analysen"])
    
    with tab1:
        with st.form("behavior_form"):
            st.markdown("**Situation (S)**")
            situation = st.text_area("Was ist passiert?", height=100)
            
            st.markdown("**Organismus (O) - Deine Verfassung**")
            col1, col2 = st.columns(2)
            with col1:
                mood = st.slider("Stimmung (1-10)", 1, 10, 5)
                stress = st.slider("Stress-Level (1-10)", 1, 10, 5)
            with col2:
                energy = st.selectbox("Energie", ["Niedrig", "Mittel", "Hoch"])
                sleep = st.selectbox("Schlaf", ["Schlecht", "OK", "Gut"])
            
            st.markdown("**Reaktion (R)**")
            thoughts = st.text_area("Gedanken:", height=80)
            emotions = st.multiselect("Gefühle:", ["Wut", "Angst", "Trauer", "Freude", "Überraschung"])
            behavior = st.text_area("Verhalten:", height=80)
            
            st.markdown("**Konsequenzen (KC)**")
            short_term = st.text_area("Kurzfristige Folgen:", height=60)
            long_term = st.text_area("Langfristige Folgen:", height=60)
            
            if st.form_submit_button("💾 Analyse speichern", type="primary"):
                if situation and thoughts and behavior:
                    analysis = {
                        "id": len(st.session_state.behavior_analyses) + 1,
                        "date": datetime.datetime.now().isoformat(),
                        "situation": situation,
                        "mood": mood,
                        "stress": stress,
                        "energy": energy,
                        "sleep": sleep,
                        "thoughts": thoughts,
                        "emotions": emotions,
                        "behavior": behavior,
                        "short_term": short_term,
                        "long_term": long_term
                    }
                    st.session_state.behavior_analyses.append(analysis)
                    st.session_state.therapy_points += 2
                    st.success("✅ Analyse gespeichert!")
                else:
                    st.error("Bitte fülle mindestens Situation, Gedanken und Verhalten aus.")
    
    with tab2:
        if st.session_state.behavior_analyses:
            for analysis in reversed(st.session_state.behavior_analyses):
                date_str = datetime.datetime.fromisoformat(analysis["date"]).strftime("%d.%m.%Y %H:%M")
                
                with st.expander(f"Analyse #{analysis['id']} - {date_str}"):
                    st.markdown(f"**Situation:** {analysis['situation']}")
                    st.markdown(f"**Gedanken:** {analysis['thoughts']}")
                    st.markdown(f"**Verhalten:** {analysis['behavior']}")
                    st.markdown(f"**Stimmung:** {analysis['mood']}/10 | **Stress:** {analysis['stress']}/10")
        else:
            st.info("📊 Noch keine Analysen erstellt.")

# Humor-Modul
def show_humor_module():
    st.markdown("## 😄 Humor-Therapie")
    
    categories = {
        "Sarkastisch": [
            "Deine Probleme sind einzigartig - genau wie die von 8 Milliarden anderen Menschen.",
            "Schön, dass du heute nicht komplett durchgedreht bist. Kleine Erfolge zählen auch.",
            "Wartezeit ist Therapiezeit. Du übst schon mal Geduld - eine wichtige Lebensskill.",
            "Perfektionismus ist der Versuch, unmögliche Standards zu erreichen, die niemand verlangt hat."
        ],
        "Motivational": [
            "Du überlebst 100% deiner schlechtesten Tage. Beeindruckende Statistik!",
            "Auch Therapeuten haben Therapeuten. Du bist in bester Gesellschaft.",
            "Jeder Schritt zählt - auch die rückwärts. Bewegung ist Bewegung.",
            "Du machst das Beste aus deiner Situation. Dass das nicht viel ist, liegt nicht an dir."
        ],
        "Therapie-Insider": [
            "Therapeuten googeln auch manchmal deine Symptome. Ihr seid quitt.",
            "50 Minuten Therapie, 10 Minuten Notizen: 'Patient lebt noch. Status unklar.'",
            "Therapie-Erfolg: Du hältst deine Probleme besser aus, sie verschwinden nicht unbedingt.",
            "Die beste Therapie ist oft jemand, der zuhört ohne sofort Lösungen anzubieten."
        ]
    }
    
    category = st.selectbox("Humor-Stil:", list(categories.keys()))
    
    if st.button("🎲 Neue Weisheit", type="primary"):
        quote = random.choice(categories[category])
        
        st.markdown(f"""
        <div class="quote-box">
            <strong>💭 Weisheit des Tages:</strong><br>
            "{quote}"<br><br>
            <small>— Dein digitaler Therapeut</small>
        </div>
        """, unsafe_allow_html=True)

# Gedanken-Modul
def show_cognitive_module():
    st.markdown("## 🧠 Gedanken-Check")
    
    thought = st.text_input("Welcher Gedanke beschäftigt dich?", 
                           placeholder="z.B. 'Das schaffe ich nie'")
    
    if thought:
        st.markdown("#### 🔍 Denkfallen-Check")
        
        distortions = {
            "Katastrophisieren": "Du stellst dir das Schlimmste vor",
            "Schwarz-Weiß-Denken": "Alles ist entweder perfekt oder katastrophal", 
            "Gedankenlesen": "Du denkst, du weißt was andere denken",
            "Übertreibung": "Du machst aus einer Mücke einen Elefanten"
        }
        
        selected = st.multiselect("Welche Denkfallen erkennst du?", list(distortions.keys()))
        
        if selected:
            for distortion in selected:
                st.info(f"**{distortion}:** {distortions[distortion]}")
        
        if st.button("💡 Hilfreiche Alternative finden"):
            alternatives = [
                f"Statt '{thought}' könntest du denken: 'Das ist herausfordernd, aber machbar.'",
                f"Alternative zu '{thought}': 'Ich kann um Hilfe bitten und es Schritt für Schritt angehen.'",
                f"Realistischer: 'Ich habe schon schwierige Situationen gemeistert.'",
                f"Hilfreich wäre: 'Was ist das Schlimmste, was wirklich passieren kann?'"
            ]
            
            st.success(random.choice(alternatives))

# Gefühls-Modul
def show_emotions_module():
    st.markdown("## 💙 Gefühls-Radar")
    
    emotions = st.multiselect(
        "Welche Gefühle spürst du gerade?",
        ["😢 Traurig", "😰 Ängstlich", "😡 Wütend", "😊 Fröhlich", 
         "😴 Müde", "🤗 Einsam", "😌 Ruhig", "😖 Gestresst"]
    )
    
    if emotions:
        st.markdown("#### 📊 Intensität bewerten")
        
        intensities = {}
        for emotion in emotions:
            intensities[emotion] = st.slider(f"Wie stark? {emotion}", 1, 10, 5, key=emotion)
        
        if st.button("💾 Gefühle dokumentieren"):
            emotion_entry = {
                "date": datetime.datetime.now().isoformat(),
                "emotions": intensities
            }
            # Hier würdest du normalerweise speichern
            st.success("✅ Gefühle dokumentiert!")
            
            # Feedback
            avg_intensity = sum(intensities.values()) / len(intensities)
            if avg_intensity > 7:
                st.warning("🔥 Hohe emotionale Intensität! Vielleicht ist eine Pause angesagt?")
            elif avg_intensity < 4:
                st.info("😌 Relativ ausgeglichen. Das ist eine gute Basis!")
            else:
                st.info("⚖️ Moderate Intensität - das ist völlig normal!")

# Sidebar
def show_sidebar():
    with st.sidebar:
        st.markdown("### 📊 Deine Statistiken")
        
        # Fortschritt
        if st.session_state.therapy_points > 0:
            st.metric("Therapie-Punkte", st.session_state.therapy_points)
            st.metric("Game-Score", st.session_state.game_score)
        
        if st.session_state.diary_entries:
            st.metric("Tagebuch-Einträge", len(st.session_state.diary_entries))
            
        if st.session_state.behavior_analyses:
            st.metric("Verhaltensanalysen", len(st.session_state.behavior_analyses))
        
        # Navigation
        if st.session_state.current_module:
            st.markdown("---")
            if st.button("🏠 Hauptmenü", use_container_width=True):
                st.session_state.current_module = None
                st.rerun()
        
        # Export
        st.markdown("---")
        if st.button("📥 Daten exportieren"):
            export_data = {
                "diary_entries": st.session_state.diary_entries,
                "behavior_analyses": st.session_state.behavior_analyses,
                "stats": {
                    "therapy_points": st.session_state.therapy_points,
                    "game_score": st.session_state.game_score
                },
                "export_date": datetime.datetime.now().isoformat()
            }
            
            json_string = json.dumps(export_data, indent=2, ensure_ascii=False)
            
            st.download_button(
                "💾 JSON herunterladen",
                json_string,
                f"therapie_export_{datetime.datetime.now().strftime('%Y%m%d')}.json",
                "application/json"
            )
        
        # Reset
        st.markdown("---")
        if st.button("🔄 Zurücksetzen", type="secondary"):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()

# Footer
def show_footer():
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #666; padding: 1rem;">
        <p><em>⚠️ Diese App ersetzt keine professionelle Therapie!</em></p>
        <p><strong>Notfall:</strong> Telefonseelsorge 0800 111 0 111 | Notfall 112</p>
    </div>
    """, unsafe_allow_html=True)

# Hauptlogik
def main():
    show_header()
    
    # Navigation
    if not st.session_state.insurance:
        show_insurance_selection()
    elif not st.session_state.loading_done:
        show_loading()
    elif st.session_state.current_module:
        # Module anzeigen
        if "Tagebuch" in st.session_state.current_module:
            show_diary_module()
        elif "Spiel" in st.session_state.current_module:
            show_game_module()
        elif "Verhaltensanalyse" in st.session_state.current_module:
            show_behavior_analysis()
        elif "Humor" in st.session_state.current_module:
            show_humor_module()
        elif "Gedanken" in st.session_state.current_module:
            show_cognitive_module()
        elif "Gefühls" in st.session_state.current_module:
            show_emotions_module()
    else:
        show_dashboard()
    
    show_sidebar()
    show_footer()

if __name__ == "__main__":
    main()
