import streamlit as st
import datetime
from collections import Counter

# App-Konfiguration
st.set_page_config(
    page_title="Taschen-Therapeut Pro", 
    page_icon="🧠", 
    layout="wide"
)

# Session State initialisieren
def init_session_state():
    """Initialisiert die wichtigsten Session State Variablen"""
    if "initialized" not in st.session_state:
        st.session_state.initialized = True
        st.session_state.page = "home"  # Aktuelle Seite
        st.session_state.insurance = None  # Versicherungsstatus
        st.session_state.entries = []  # Speicher für alle Einträge

# CSS für grundlegendes Styling
def load_css():
    """Lädt das CSS für die App"""
    st.markdown("""
    <style>
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
    
    .info-card {
        background: #f8f9fa;
        border: 1px solid #e1e8ed;
        border-radius: 8px;
        padding: 1.5rem;
        margin: 1rem 0;
    }
    </style>
    """, unsafe_allow_html=True)

# Header-Komponente
def show_header():
    """Zeigt den App-Header"""
    st.markdown("""
    <div class="main-header">
        <div class="main-title">🧠 Taschen-Therapeut Pro</div>
        <div class="subtitle">Professionelle Selbsthilfe mit einer Prise Humor</div>
    </div>
    """, unsafe_allow_html=True)

# Versicherungsauswahl
def show_insurance_selection():
    """Zeigt die Versicherungsauswahl"""
    st.markdown("### 🏥 Versicherungsauswahl")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="info-card">
            <h4>🪪 Gesetzlich versichert</h4>
            <p>Standard-Paket mit Grundfunktionen</p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("GKV wählen", key="gkv", use_container_width=True):
            st.session_state.insurance = "GKV"
            st.session_state.page = "dashboard"
            st.rerun()
    
    with col2:
        st.markdown("""
        <div class="info-card">
            <h4>💳 Privat versichert</h4>
            <p>Premium-Paket mit allen Features</p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("PKV wählen", key="pkv", use_container_width=True):
            st.session_state.insurance = "PKV"
            st.session_state.page = "dashboard"
            st.rerun()

# Dashboard (Hauptmenü)
def show_dashboard():
    """Zeigt das Hauptdashboard"""
    # Status anzeigen
    if st.session_state.insurance == "GKV":
        st.info("🪪 Status: Gesetzlich versichert")
    else:
        st.success("💳 Status: Privat versichert - Premium")
    
    st.markdown("### 🎯 Module")
    
    # Module in 2 Spalten
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("📔 Digitales Tagebuch", use_container_width=True):
            st.session_state.page = "diary"
            st.rerun()
            
        if st.button("🧠 Gedanken-Check", use_container_width=True):
            st.session_state.page = "thoughts"
            st.rerun()
            
    
    with col2:
         if st.button("🔬 Verhaltensanalyse", use_container_width=True):
            st.session_state.page = "analysis"
            st.rerun()
              
         if st.button("📊 Statistiken", use_container_width=True):
            st.session_state.page = "stats"
            st.rerun()
   

# Einfaches Tagebuch-Modul
def show_diary():
    """Zeigt das Tagebuch-Modul"""
    st.markdown("## 📔 Digitales Tagebuch")
    
    # Neuer Eintrag
    with st.form("diary_entry"):
        mood = st.selectbox(
            "Wie fühlst du dich?",
            ["😊 Gut", "😐 Neutral", "😔 Schlecht"]
        )
        
        entry = st.text_area("Was beschäftigt dich heute?", height=150)
        
        if st.form_submit_button("Speichern"):
            if entry:
                new_entry = {
                    "date": datetime.datetime.now(),
                    "mood": mood,
                    "text": entry
                }
                st.session_state.entries.append(new_entry)
                st.success("✅ Eintrag gespeichert!")

    # Letzte Einträge anzeigen
    if st.session_state.entries:
        st.markdown("### 📚 Letzte Einträge")
        for entry in reversed(st.session_state.entries[-3:]):
            with st.expander(f"{entry['mood']} - {entry['date'].strftime('%d.%m.%Y %H:%M')}"):
                st.write(entry['text'])

# Placeholder für andere Module
def show_thoughts():
    st.markdown("## 🧠 Gedanken-Check")
    st.info("Dieses Modul wird noch entwickelt...")

# Verhaltensanalyse-Modul (SORKC) - korrigierte Version
def show_behavior_analysis():
    """Zeigt das Verhaltensanalyse-Modul"""
    st.markdown("## 🔬 Verhaltensanalyse (SORKC-Modell)")
    
    # Info-Box
    with st.expander("ℹ️ Was ist das SORKC-Modell?"):
        st.markdown("""
        **SORKC** steht für:
        - **S** = Situation (Was ist passiert?)
        - **O** = Organismus (Wie war deine Verfassung?)
        - **R** = Reaktion (Gedanken, Gefühle, Verhalten)
        - **K** = Konsequenzen (Kurz- und langfristig)
        - **C** = Kontingenzen (Wie oft/unter welchen Bedingungen?)
        """)
    
    tab1, tab2 = st.tabs(["📝 Neue Analyse", "📊 Meine Analysen"])
    
    with tab1:
        with st.form("sorkc_form"):
            st.markdown("### S - Situation")
            situation = st.text_area(
                "Was ist passiert? Beschreibe die Situation:",
                placeholder="z.B. Streit mit Partner, Präsentation auf Arbeit...",
                height=100
            )
            
            st.markdown("### O - Organismus (Deine Verfassung)")
            col1, col2 = st.columns(2)
            with col1:
                stress_level = st.slider("Stress-Level", 1, 10, 5)
                energy_level = st.select_slider(
                    "Energie-Level", 
                    options=["Sehr niedrig", "Niedrig", "Mittel", "Hoch", "Sehr hoch"]
                )
            with col2:
                sleep_quality = st.selectbox(
                    "Schlafqualität letzte Nacht",
                    ["Sehr schlecht", "Schlecht", "OK", "Gut", "Sehr gut"]
                )
                health = st.selectbox(
                    "Gesundheitszustand",
                    ["Krank", "Angeschlagen", "Normal", "Gut", "Sehr gut"]
                )
            
            st.markdown("### R - Reaktion")
            
            # Gedanken
            thoughts = st.text_area(
                "Gedanken (Was ging dir durch den Kopf?):",
                placeholder="z.B. 'Das schaffe ich nie', 'Alle sind gegen mich'...",
                height=80
            )
            
            # Gefühle
            emotions = st.multiselect(
                "Gefühle (Was hast du gefühlt?):",
                ["Angst", "Wut", "Trauer", "Freude", "Scham", "Schuld", 
                 "Ekel", "Überraschung", "Enttäuschung", "Frustration"]
            )
            
            emotion_intensity = st.slider("Gefühls-Intensität", 1, 10, 5)
            
            # Verhalten
            behavior = st.text_area(
                "Verhalten (Was hast du getan?):",
                placeholder="z.B. 'Bin aus dem Raum gegangen', 'Habe geschrien'...",
                height=80
            )
            
            st.markdown("### K - Konsequenzen")
            
            consequences_short = st.text_area(
                "Kurzfristige Konsequenzen (Was passierte direkt danach?):",
                placeholder="z.B. 'Fühlte mich erleichtert', 'Konflikt eskalierte'...",
                height=70  # Geändert von 60 auf 70
            )
            
            consequences_long = st.text_area(
                "Langfristige Konsequenzen (Was könnten Folgen sein?):",
                placeholder="z.B. 'Beziehung belastet', 'Vertrauen verloren'...",
                height=70  # Geändert von 60 auf 70
            )
            
            st.markdown("### C - Kontingenzen")
            frequency = st.selectbox(
                "Wie oft kommt diese Situation vor?",
                ["Einmalig", "Selten", "Gelegentlich", "Häufig", "Täglich"]
            )
            
            # Submit Button
            submitted = st.form_submit_button("💾 Analyse speichern", type="primary")
            
            if submitted:
                if situation and thoughts and behavior:
                    analysis = {
                        "id": len(st.session_state.analyses) + 1,
                        "date": datetime.datetime.now(),
                        "situation": situation,
                        "organism": {
                            "stress": stress_level,
                            "energy": energy_level,
                            "sleep": sleep_quality,
                            "health": health
                        },
                        "reaction": {
                            "thoughts": thoughts,
                            "emotions": emotions,
                            "emotion_intensity": emotion_intensity,
                            "behavior": behavior
                        },
                        "consequences": {
                            "short_term": consequences_short,
                            "long_term": consequences_long
                        },
                        "frequency": frequency
                    }
                    
                    st.session_state.analyses.append(analysis)
                    st.success("✅ Analyse gespeichert! Du kannst sie im Tab 'Meine Analysen' einsehen.")
                    st.balloons()
                else:
                    st.error("⚠️ Bitte fülle mindestens Situation, Gedanken und Verhalten aus.")
    
    with tab2:
        if not st.session_state.analyses:
            st.info("📊 Noch keine Analysen vorhanden. Erstelle deine erste Analyse im anderen Tab!")
        else:
            st.markdown(f"### 📚 {len(st.session_state.analyses)} Analysen gespeichert")
            
            # Filter
            filter_emotion = st.selectbox(
                "Nach Gefühl filtern:",
                ["Alle"] + ["Angst", "Wut", "Trauer", "Freude", "Scham", "Schuld"]
            )
            
            # Analysen anzeigen
            for analysis in reversed(st.session_state.analyses):
                # Filter anwenden
                if filter_emotion != "Alle" and filter_emotion not in analysis["reaction"]["emotions"]:
                    continue
                
                date_str = analysis["date"].strftime("%d.%m.%Y %H:%M")
                emotions_str = ", ".join(analysis["reaction"]["emotions"]) if analysis["reaction"]["emotions"] else "Keine"
                
                with st.expander(f"Analyse #{analysis['id']} - {date_str} | Gefühle: {emotions_str}"):
                    col1, col2 = st.columns([2, 1])
                    
                    with col1:
                        st.markdown("**🎬 Situation:**")
                        st.write(analysis["situation"])
                        
                        st.markdown("**💭 Gedanken:**")
                        st.write(analysis["reaction"]["thoughts"])
                        
                        st.markdown("**🎭 Verhalten:**")
                        st.write(analysis["reaction"]["behavior"])
                        
                        if analysis["consequences"]["short_term"]:
                            st.markdown("**⚡ Kurzfristige Konsequenzen:**")
                            st.write(analysis["consequences"]["short_term"])
                        
                        if analysis["consequences"]["long_term"]:
                            st.markdown("**🔮 Langfristige Konsequenzen:**")
                            st.write(analysis["consequences"]["long_term"])
                    
                    with col2:
                        st.markdown("**📊 Verfassung:**")
                        st.write(f"Stress: {analysis['organism']['stress']}/10")
                        st.write(f"Energie: {analysis['organism']['energy']}")
                        st.write(f"Schlaf: {analysis['organism']['sleep']}")
                        
                        st.markdown("**🎯 Häufigkeit:**")
                        st.write(analysis["frequency"])
                        
                        st.markdown("**💡 Gefühls-Intensität:**")
                        st.write(f"{analysis['reaction']['emotion_intensity']}/10")
            
            # Insights
            if len(st.session_state.analyses) >= 3:
                st.markdown("### 💡 Muster & Insights")
                
                # Häufigste Emotionen
                all_emotions = []
                for a in st.session_state.analyses:
                    all_emotions.extend(a["reaction"]["emotions"])
                
                if all_emotions:
                    emotion_counts = Counter(all_emotions)
                    most_common = emotion_counts.most_common(3)
                    
                    st.info(f"**Häufigste Gefühle:** {', '.join([f'{e[0]} ({e[1]}x)' for e in most_common])}")
                
                # Durchschnittlicher Stress
                avg_stress = sum(a["organism"]["stress"] for a in st.session_state.analyses) / len(st.session_state.analyses)
                st.info(f"**Durchschnittlicher Stress-Level:** {avg_stress:.1f}/10")
def show_stats():
    st.markdown("## 📊 Statistiken")
    total_entries = len(st.session_state.entries)
    st.metric("Tagebuch-Einträge", total_entries)

# Sidebar mit Navigation
def show_sidebar():
    """Zeigt die Sidebar mit Navigation"""
    with st.sidebar:
        st.markdown("### 🧭 Navigation")
        
        if st.button("🏠 Hauptmenü", use_container_width=True):
            st.session_state.page = "dashboard"
            st.rerun()
        
        if st.session_state.insurance:
            st.markdown("---")
            st.markdown(f"**Status:** {st.session_state.insurance}")
            
            if st.button("🔄 Neu starten", use_container_width=True):
                # Reset alles
                for key in list(st.session_state.keys()):
                    del st.session_state[key]
                st.rerun()

# Hauptfunktion
def main():
    # Initialisierung
    init_session_state()
    load_css()
    
    # Header immer anzeigen
    show_header()
    
    # Sidebar anzeigen (wenn eingeloggt)
    if st.session_state.insurance:
        show_sidebar()
    
    # Routing - welche Seite anzeigen?
    if not st.session_state.insurance:
        show_insurance_selection()
    elif st.session_state.page == "dashboard":
        show_dashboard()
    elif st.session_state.page == "diary":
        show_diary()
    elif st.session_state.page == "thoughts":
        show_thoughts()
    elif st.session_state.page == "analysis":
        show_behavior_analysis()
    elif st.session_state.page == "stats":
        show_stats()
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #666;">
        <em>⚠️ Diese App ersetzt keine professionelle Therapie!</em>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
