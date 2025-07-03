import streamlit as st
import datetime
from collections import Counter

from collections import Counter
import json
from datetime import datetime

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
        st.session_state.analyses = []  # Speicher für Verhaltensanalysen  # 

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

# Verhaltensanalyse-Modul nach SORKC (basierend auf PDF)
def show_behavior_analysis():
    """Zeigt das erweiterte Verhaltensanalyse-Modul mit 4 Phasen"""
    st.markdown("## 🔬 Verhaltensanalyse (SORKC-Modell)")
    
    # Info aus dem PDF
    with st.expander("ℹ️ Was ist eine Verhaltensanalyse?"):
        st.markdown("""
        Die Verhaltensanalyse hilft dir, deine Reaktionsmuster zu verstehen und zu verändern.
        
        **4 Schritte:**
        1. **Wahrnehmen** - Situation und Reaktionen beschreiben
        2. **Analysieren** - Hilfreiche/nicht hilfreiche Muster erkennen
        3. **Planen** - Alternative Reaktionen entwickeln
        4. **Trainieren** - Neue Verhaltensweisen üben
        
        **SORKC steht für:**
        - **S** = Situation (Auslöser)
        - **O** = Organismus (Tagesform & Grundannahmen)
        - **R** = Reaktion (Gedanken, Gefühle, Körper, Verhalten)
        - **K** = Konsequenzen (kurz- und langfristig)
        - **C** = Kontingenzen (Häufigkeit)
        """)
    
    # Tabs für die 4 Phasen
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "1️⃣ Wahrnehmen", 
        "2️⃣ Analysieren", 
        "3️⃣ Planen", 
        "4️⃣ Trainieren",
        "📊 Übersicht"
    ])
    
    # Phase 1: WAHRNEHMEN
    with tab1:
        st.markdown("### Phase 1: Wahrnehmen")
        st.info("Beschreibe rückblickend dein Reaktionsverhalten, die auslösende Situation und die Folgen.")
        
        with st.form("phase1_wahrnehmen", clear_on_submit=False):
            # SITUATION
            st.markdown("#### 📍 Situation")
            st.caption("Wann, was, wer & wo? Was führte zu deiner Reaktion?")
            situation = st.text_area(
                "Beschreibe die Situation:",
                height=100,
                key="wa_situation"
            )
            
            # ORGANISMUS
            st.markdown("#### 🧍 Ich (O-Variable)")
            col1, col2 = st.columns(2)
            
            with col1:
                st.caption("Aktuelle Tagesform")
                stimmung = st.slider("Stimmung", 0, 10, 5, key="wa_stimmung")
                tagesform = st.text_input("Besonderheiten (Müdigkeit, Stress, etc.)", key="wa_tagesform")
            
            with col2:
                st.caption("Glaubenssätze/Denkmuster")
                denkmuster = st.text_area(
                    "Welche Grundannahmen spielten eine Rolle?",
                    height=68,
                    key="wa_denkmuster"
                )
            
            # REAKTION
            st.markdown("#### 💭 Reaktion")
            
            # Gedanken
            gedanken = st.text_area(
                "Gedanken (Was ging dir durch den Kopf?):",
                height=80,
                key="wa_gedanken"
            )
            
            # Gefühle
            col1, col2 = st.columns([3, 1])
            with col1:
                gefuehle = st.multiselect(
                    "Gefühle:",
                    ["Angst", "Wut", "Trauer", "Freude", "Scham", "Schuld", 
                     "Ekel", "Überraschung", "Enttäuschung", "Frustration", "Eifersucht"],
                    key="wa_gefuehle"
                )
            with col2:
                gefuehl_intensitaet = st.number_input(
                    "Intensität (0-100)",
                    0, 100, 50,
                    key="wa_gefuehl_int"
                )
            
            # Körperempfindungen
            col1, col2 = st.columns([3, 1])
            with col1:
                koerper = st.text_input(
                    "Körperempfindungen (z.B. Herzrasen, Schwitzen):",
                    key="wa_koerper"
                )
            with col2:
                anspannung = st.number_input(
                    "Anspannung (0-100)",
                    0, 100, 50,
                    key="wa_anspannung"
                )
            
            # Verhalten
            verhalten = st.text_area(
                "Beobachtbares Verhalten (Was hast du getan?):",
                height=80,
                key="wa_verhalten"
            )
            
            # KONSEQUENZEN
            st.markdown("#### ⚡ Konsequenzen")
            
            konseq_kurz = st.text_area(
                "Kurzfristige Konsequenzen (Was passierte sofort?):",
                height=70,
                key="wa_konseq_kurz"
            )
            
            konseq_lang = st.text_area(
                "Langfristige Folgen (Minuten bis Jahre später):",
                height=70,
                key="wa_konseq_lang"
            )
            
            # Speichern
            if st.form_submit_button("💾 Phase 1 speichern", type="primary"):
                if situation and verhalten:
                    analyse_id = len(st.session_state.analyses) + 1
                    
                    # Neue Analyse erstellen
                    neue_analyse = {
                        "id": analyse_id,
                        "datum": datetime.now(),
                        "phase1": {
                            "situation": situation,
                            "organismus": {
                                "stimmung": stimmung,
                                "tagesform": tagesform,
                                "denkmuster": denkmuster
                            },
                            "reaktion": {
                                "gedanken": gedanken,
                                "gefuehle": gefuehle,
                                "gefuehl_intensitaet": gefuehl_intensitaet,
                                "koerper": koerper,
                                "anspannung": anspannung,
                                "verhalten": verhalten
                            },
                            "konsequenzen": {
                                "kurz": konseq_kurz,
                                "lang": konseq_lang
                            }
                        },
                        "phase2": None,
                        "phase3": None,
                        "phase4": None
                    }
                    
                    st.session_state.analyses.append(neue_analyse)
                    st.success("✅ Phase 1 gespeichert! Weiter mit Phase 2: Analysieren")
                    st.balloons()
                else:
                    st.error("Bitte fülle mindestens Situation und Verhalten aus.")
    
    # Phase 2: ANALYSIEREN
    with tab2:
        st.markdown("### Phase 2: Analysieren")
        st.info("Bewerte deine Reaktionen als hilfreich oder weniger hilfreich und finde Ausstiegspunkte.")
        
        # Analyse auswählen
        if st.session_state.analyses:
            analyse_ids = [f"Analyse #{a['id']} vom {a['datum'].strftime('%d.%m.%Y')}" 
                          for a in st.session_state.analyses if a['phase1']]
            
            if analyse_ids:
                selected = st.selectbox("Wähle eine Analyse:", analyse_ids)
                analyse_idx = int(selected.split('#')[1].split(' ')[0]) - 1
                current_analyse = st.session_state.analyses[analyse_idx]
                
                if current_analyse['phase1']:
                    # Zusammenfassung anzeigen
                    with st.expander("📋 Zusammenfassung Phase 1", expanded=True):
                        p1 = current_analyse['phase1']
                        st.write(f"**Situation:** {p1['situation']}")
                        st.write(f"**Verhalten:** {p1['reaktion']['verhalten']}")
                        st.write(f"**Gefühle:** {', '.join(p1['reaktion']['gefuehle'])}")
                    
                    with st.form("phase2_analysieren"):
                        st.markdown("#### 🎯 Bewertung")
                        
                        # Bewertungen
                        hilfreich_situation = st.checkbox("✅ Situation war unvermeidbar/neutral")
                        hilfreich_gedanken = st.checkbox("✅ Gedanken waren hilfreich/realistisch")
                        hilfreich_verhalten = st.checkbox("✅ Verhalten war angemessen")
                        hilfreich_kurz = st.checkbox("✅ Kurzfristige Folgen waren positiv")
                        hilfreich_lang = st.checkbox("✅ Langfristige Folgen sind positiv")
                        
                        st.markdown("#### 🚪 Ausstiegspunkt")
                        ausstieg = st.radio(
                            "Wo könntest du die Reaktionskette unterbrechen?",
                            ["Situation verändern", "Gedanken hinterfragen", 
                             "Verhalten ändern", "Tagesform verbessern"],
                            key="ausstieg"
                        )
                        
                        ausstieg_wie = st.text_area(
                            "Was würdest du konkret verändern?",
                            key="ausstieg_wie"
                        )
                        
                        st.markdown("#### 🛡️ Prävention & Wiedergutmachung")
                        praevention = st.text_area(
                            "Prävention: Wie könntest du dich auf ähnliche Situationen vorbereiten?",
                            key="praevention"
                        )
                        
                        wiedergutmachung = st.text_area(
                            "Wiedergutmachung: Was könntest du tun, um die Situation zu verbessern?",
                            key="wiedergutmachung"
                        )
                        
                        if st.form_submit_button("💾 Phase 2 speichern", type="primary"):
                            current_analyse['phase2'] = {
                                "bewertung": {
                                    "situation": hilfreich_situation,
                                    "gedanken": hilfreich_gedanken,
                                    "verhalten": hilfreich_verhalten,
                                    "kurz": hilfreich_kurz,
                                    "lang": hilfreich_lang
                                },
                                "ausstieg": ausstieg,
                                "ausstieg_wie": ausstieg_wie,
                                "praevention": praevention,
                                "wiedergutmachung": wiedergutmachung
                            }
                            st.success("✅ Phase 2 gespeichert! Weiter mit Phase 3: Planen")
        else:
            st.info("Bitte erstelle zuerst eine Analyse in Phase 1.")
    
    # Phase 3: PLANEN
    with tab3:
        st.markdown("### Phase 3: Planen")
        st.info("Entwirf eine alternative Reaktionskette ab deinem Ausstiegspunkt.")
        
        if st.session_state.analyses:
            # Analysen mit Phase 2 filtern
            phase2_analyses = [a for a in st.session_state.analyses if a['phase2']]
            
            if phase2_analyses:
                analyse_ids = [f"Analyse #{a['id']} vom {a['datum'].strftime('%d.%m.%Y')}" 
                              for a in phase2_analyses]
                
                selected = st.selectbox("Wähle eine Analyse:", analyse_ids, key="phase3_select")
                analyse_idx = int(selected.split('#')[1].split(' ')[0]) - 1
                current_analyse = next(a for a in st.session_state.analyses if a['id'] == analyse_idx + 1)
                
                # Info anzeigen
                with st.expander("📋 Bisherige Erkenntnisse", expanded=True):
                    st.write(f"**Ausstiegspunkt:** {current_analyse['phase2']['ausstieg']}")
                    st.write(f"**Geplante Veränderung:** {current_analyse['phase2']['ausstieg_wie']}")
                
                with st.form("phase3_planen"):
                    st.markdown("#### 🔄 Alternative Reaktionskette")
                    
                    # Je nach Ausstiegspunkt unterschiedliche Felder
                    alt_situation = st.text_area(
                        "Alternative Situation (falls veränderbar):",
                        value=current_analyse['phase1']['situation'] if current_analyse['phase2']['ausstieg'] != "Situation verändern" else "",
                        key="alt_situation"
                    )
                    
                    alt_gedanken = st.text_area(
                        "Alternative Gedanken:",
                        key="alt_gedanken"
                    )
                    
                    alt_gefuehle = st.text_area(
                        "Erwartete Gefühle:",
                        key="alt_gefuehle"
                    )
                    
                    alt_koerper = st.text_area(
                        "Erwartete Körperempfindungen:",
                        key="alt_koerper"
                    )
                    
                    alt_verhalten = st.text_area(
                        "Alternatives Verhalten:",
                        key="alt_verhalten"
                    )
                    
                    alt_konseq_kurz = st.text_area(
                        "Erwartete kurzfristige Konsequenzen:",
                        key="alt_konseq_kurz"
                    )
                    
                    alt_konseq_lang = st.text_area(
                        "Erwartete langfristige Folgen:",
                        key="alt_konseq_lang"
                    )
                    
                    if st.form_submit_button("💾 Phase 3 speichern", type="primary"):
                        current_analyse['phase3'] = {
                            "alternative": {
                                "situation": alt_situation,
                                "gedanken": alt_gedanken,
                                "gefuehle": alt_gefuehle,
                                "koerper": alt_koerper,
                                "verhalten": alt_verhalten,
                                "konseq_kurz": alt_konseq_kurz,
                                "konseq_lang": alt_konseq_lang
                            }
                        }
                        st.success("✅ Phase 3 gespeichert! Jetzt kannst du mit dem Training beginnen.")
            else:
                st.info("Bitte schließe erst Phase 2 ab.")
        else:
            st.info("Bitte beginne mit Phase 1.")
    
    # Phase 4: TRAINIEREN
    with tab4:
        st.markdown("### Phase 4: Trainieren")
        st.info("Dokumentiere deine Veränderungsversuche und Fortschritte.")
        
        if st.session_state.analyses:
            # Analysen mit Phase 3 filtern
            phase3_analyses = [a for a in st.session_state.analyses if a['phase3']]
            
            if phase3_analyses:
                analyse_ids = [f"Analyse #{a['id']} vom {a['datum'].strftime('%d.%m.%Y')}" 
                              for a in phase3_analyses]
                
                selected = st.selectbox("Wähle eine Analyse:", analyse_ids, key="phase4_select")
                analyse_idx = int(selected.split('#')[1].split(' ')[0]) - 1
                current_analyse = next(a for a in st.session_state.analyses if a['id'] == analyse_idx + 1)
                
                # Geplante Alternative anzeigen
                with st.expander("📋 Geplante Alternative", expanded=False):
                    alt = current_analyse['phase3']['alternative']
                    st.write(f"**Verhalten:** {alt['verhalten']}")
                    st.write(f"**Gedanken:** {alt['gedanken']}")
                
                with st.form("phase4_trainieren"):
                    st.markdown("#### 📝 Trainings-Dokumentation")
                    
                    # Neue Situation
                    training_situation = st.text_area(
                        "Situation (wann hast du es versucht?):",
                        key="training_situation"
                    )
                    
                    # Fortschritt
                    fortschritt = st.slider(
                        "Fortschritt (0 = gar nicht, 100 = vollständig umgesetzt)",
                        0, 100, 50,
                        key="fortschritt"
                    )
                    
                    # Was hat geklappt?
                    geklappt = st.text_area(
                        "Was hat gut geklappt? ⭐",
                        key="geklappt"
                    )
                    
                    # Schwierigkeiten
                    schwierig = st.text_area(
                        "Was war schwierig?",
                        key="schwierig"
                    )
                    
                    # Tatsächliche Reaktionen
                    tats_gedanken = st.text_area(
                        "Tatsächliche Gedanken:",
                        key="tats_gedanken"
                    )
                    
                    tats_gefuehle = st.text_area(
                        "Tatsächliche Gefühle:",
                        key="tats_gefuehle"
                    )
                    
                    tats_verhalten = st.text_area(
                        "Tatsächliches Verhalten:",
                        key="tats_verhalten"
                    )
                    
                    # Erkenntnisse
                    erkenntnisse = st.text_area(
                        "Neue Erkenntnisse:",
                        key="erkenntnisse"
                    )
                    
                    if st.form_submit_button("💾 Training speichern", type="primary"):
                        if not current_analyse.get('phase4'):
                            current_analyse['phase4'] = []
                        
                        current_analyse['phase4'].append({
                            "datum": datetime.now(),
                            "situation": training_situation,
                            "fortschritt": fortschritt,
                            "geklappt": geklappt,
                            "schwierig": schwierig,
                            "reaktionen": {
                                "gedanken": tats_gedanken,
                                "gefuehle": tats_gefuehle,
                                "verhalten": tats_verhalten
                            },
                            "erkenntnisse": erkenntnisse
                        })
                        
                        st.success("✅ Training dokumentiert! Weiter so! 🌟")
                        
                        # Motivations-Feedback
                        if fortschritt >= 80:
                            st.balloons()
                            st.info("🎉 Wow! Über 80% Fortschritt - das ist großartig!")
                        elif fortschritt >= 50:
                            st.info("💪 Gut gemacht! Du bist auf dem richtigen Weg.")
                        else:
                            st.info("🌱 Jeder kleine Schritt zählt. Bleib dran!")
            else:
                st.info("Bitte schließe erst Phase 3 ab.")
        else:
            st.info("Bitte beginne mit Phase 1.")
    
    # ÜBERSICHT
    with tab5:
        st.markdown("### 📊 Übersicht deiner Analysen")
        
        if st.session_state.analyses:
            # Statistiken
            col1, col2, col3, col4 = st.columns(4)
            
            total = len(st.session_state.analyses)
            phase2_count = len([a for a in st.session_state.analyses if a['phase2']])
            phase3_count = len([a for a in st.session_state.analyses if a['phase3']])
            phase4_count = len([a for a in st.session_state.analyses if a.get('phase4')])
            
            col1.metric("Analysen gesamt", total)
            col2.metric("Analysiert", phase2_count)
            col3.metric("Geplant", phase3_count)
            col4.metric("Im Training", phase4_count)
            
            # Analysen-Liste
            for analyse in reversed(st.session_state.analyses):
                phase_status = "🔴"
                if analyse.get('phase4'):
                    phase_status = "🟢"
                elif analyse['phase3']:
                    phase_status = "🟡"
                elif analyse['phase2']:
                    phase_status = "🟠"
                
                with st.expander(f"{phase_status} Analyse #{analyse['id']} - {analyse['datum'].strftime('%d.%m.%Y %H:%M')}"):
                    # Phase 1 Details
                    st.markdown("**Phase 1: Wahrnehmen**")
                    p1 = analyse['phase1']
                    st.write(f"Situation: {p1['situation'][:100]}...")
                    st.write(f"Gefühle: {', '.join(p1['reaktion']['gefuehle'])}")
                    st.write(f"Stimmung: {p1['organismus']['stimmung']}/10")
                    
                    # Phase 2 Details
                    if analyse['phase2']:
                        st.markdown("**Phase 2: Analysieren**")
                        st.write(f"Ausstiegspunkt: {analyse['phase2']['ausstieg']}")
                    
                    # Phase 3 Details
                    if analyse['phase3']:
                        st.markdown("**Phase 3: Planen**")
                        st.write("✅ Alternative geplant")
                    
                    # Phase 4 Details
                    if analyse.get('phase4'):
                        st.markdown("**Phase 4: Trainieren**")
                        trainings = analyse['phase4']
                        avg_progress = sum(t['fortschritt'] for t in trainings) / len(trainings)
                        st.write(f"Trainingseinheiten: {len(trainings)}")
                        st.write(f"Durchschnittlicher Fortschritt: {avg_progress:.0f}%")
                    
                    # Export-Button für einzelne Analyse
                    if st.button(f"📥 Analyse #{analyse['id']} exportieren", key=f"export_{analyse['id']}"):
                        json_str = json.dumps(analyse, default=str, indent=2, ensure_ascii=False)
                        st.download_button(
                            "💾 Als JSON herunterladen",
                            json_str,
                            f"verhaltensanalyse_{analyse['id']}_{analyse['datum'].strftime('%Y%m%d')}.json",
                            "application/json",
                            key=f"download_{analyse['id']}"
                        )
            
            # Gesamt-Export
            st.markdown("---")
            if st.button("📥 Alle Analysen exportieren"):
                export_data = {
                    "analysen": st.session_state.analyses,
                    "export_datum": datetime.now().isoformat()
                }
                json_str = json.dumps(export_data, default=str, indent=2, ensure_ascii=False)
                st.download_button(
                    "💾 Alle als JSON herunterladen",
                    json_str,
                    f"alle_verhaltensanalysen_{datetime.now().strftime('%Y%m%d')}.json",
                    "application/json"
                )
        else:
            st.info("Noch keine Analysen vorhanden. Starte mit Phase 1!")

# Daten-Persistenz (Optional - für lokale Speicherung)
def save_to_local():
    """Speichert die Daten lokal (wenn möglich)"""
    try:
        data = {
            "analyses": st.session_state.analyses,
            "last_saved": datetime.now().isoformat()
        }
        # Dies funktioniert nur in lokalen Streamlit-Apps
        with open("verhaltensanalysen_backup.json", "w", encoding="utf-8") as f:
            json.dump(data, f, default=str, ensure_ascii=False)
        return True
    except:
        return False

def load_from_local():
    """Lädt Daten aus lokaler Datei (wenn vorhanden)"""
    try:
        with open("verhaltensanalysen_backup.json", "r", encoding="utf-8") as f:
            data = json.load(f)
            # Datetime-Strings zurück konvertieren
            for analyse in data.get("analyses", []):
                analyse["datum"] = datetime.fromisoformat(analyse["datum"])
            return data.get("analyses", [])
    except:
        return []
        
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
