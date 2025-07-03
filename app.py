import streamlit as st
import datetime
from datetime import datetime
import json
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
        st.session_state.page = "home"
        st.session_state.insurance = None
        st.session_state.entries = []
        st.session_state.analyses = []

# CSS für professionelles Styling
def load_css():
    """Lädt das CSS für die App"""
    st.markdown("""
    <style>
    /* Hauptfarben */
    :root {
        --primary-color: #3498db;
        --secondary-color: #2c3e50;
        --success-color: #27ae60;
        --warning-color: #f39c12;
        --danger-color: #e74c3c;
        --light-bg: #f8f9fa;
        --card-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }
    
    /* Header Styling */
    .main-header {
        background: linear-gradient(135deg, var(--secondary-color), var(--primary-color));
        color: white;
        padding: 2.5rem;
        border-radius: 15px;
        margin-bottom: 2rem;
        text-align: center;
        box-shadow: var(--card-shadow);
    }
    
    .main-title {
        font-size: 2.8rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
    }
    
    .subtitle {
        font-size: 1.2rem;
        opacity: 0.95;
        font-weight: 300;
    }
    
    /* Karten Design */
    .info-card {
        background: white;
        border: 1px solid #e1e8ed;
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: var(--card-shadow);
        transition: all 0.3s ease;
    }
    
    .info-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    }
    
    .premium-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
    }
    
    .standard-card {
        background: linear-gradient(135deg, #84fab0 0%, #8fd3f4 100%);
    }
    
    /* Phase Cards */
    .phase-card {
        background: white;
        border-left: 4px solid var(--primary-color);
        padding: 1rem;
        margin: 0.5rem 0;
        border-radius: 0 8px 8px 0;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    }
    
    .phase-complete {
        border-left-color: var(--success-color);
        background: #f0f9ff;
    }
    
    /* Progress Bar */
    .progress-container {
        background: #e1e8ed;
        border-radius: 10px;
        height: 24px;
        margin: 1rem 0;
        overflow: hidden;
    }
    
    .progress-bar {
        background: linear-gradient(90deg, var(--success-color), #2ecc71);
        height: 100%;
        border-radius: 10px;
        transition: width 0.5s ease;
        display: flex;
        align-items: center;
        justify-content: center;
        color: white;
        font-weight: 600;
    }
    
    /* Status Badges */
    .status-badge {
        display: inline-block;
        padding: 0.25rem 0.75rem;
        border-radius: 20px;
        font-size: 0.875rem;
        font-weight: 500;
        margin: 0.25rem;
    }
    
    .badge-success {
        background: var(--success-color);
        color: white;
    }
    
    .badge-warning {
        background: var(--warning-color);
        color: white;
    }
    
    .badge-info {
        background: var(--primary-color);
        color: white;
    }
    
    /* Buttons */
    .stButton > button {
        border-radius: 8px;
        padding: 0.5rem 1rem;
        font-weight: 500;
        transition: all 0.3s ease;
        border: none;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    }
    
    /* Form Styling */
    .stForm {
        background: var(--light-bg);
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: var(--card-shadow);
    }
    
    /* Metrics */
    [data-testid="metric-container"] {
        background: white;
        padding: 1rem;
        border-radius: 8px;
        box-shadow: var(--card-shadow);
    }
    
    /* Expander */
    .streamlit-expanderHeader {
        background: var(--light-bg);
        border-radius: 8px;
        font-weight: 500;
    }
    
    /* Mobile Responsive */
    @media (max-width: 768px) {
        .main-title {
            font-size: 2rem;
        }
        
        .info-card {
            padding: 1rem;
        }
    }
    </style>
    """, unsafe_allow_html=True)

# Header-Komponente
def show_header():
    """Zeigt den App-Header"""
    st.markdown("""
    <div class="main-header">
        <div class="main-title">🧠 Taschen-Therapeut Pro</div>
        <div class="subtitle">Professionelle Selbsthilfe mit wissenschaftlichem Hintergrund</div>
    </div>
    """, unsafe_allow_html=True)

# Versicherungsauswahl
def show_insurance_selection():
    """Zeigt die Versicherungsauswahl"""
    st.markdown("### 🏥 Willkommen! Bitte wähle deinen Status:")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="info-card standard-card">
            <h3>🪪 Gesetzlich versichert</h3>
            <p><strong>Standard-Paket</strong></p>
            <ul>
                <li>Alle Basis-Module</li>
                <li>Verhaltensanalyse</li>
                <li>Tagebuch-Funktion</li>
                <li>Export-Funktionen</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("GKV wählen", key="gkv", use_container_width=True):
            st.session_state.insurance = "GKV"
            st.session_state.page = "dashboard"
            st.rerun()
    
    with col2:
        st.markdown("""
        <div class="info-card premium-card">
            <h3>💳 Privat versichert</h3>
            <p><strong>Premium-Paket</strong></p>
            <ul>
                <li>Alle Standard-Features</li>
                <li>Erweiterte Analysen</li>
                <li>Premium-Statistiken</li>
                <li>Priority Support*</li>
            </ul>
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
        st.markdown("""
        <div class="info-card">
            <span class="status-badge badge-info">🪪 Gesetzlich versichert</span>
            <span style="margin-left: 1rem;">Alle Basis-Features verfügbar</span>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="info-card">
            <span class="status-badge badge-success">💳 Premium-Status</span>
            <span style="margin-left: 1rem;">Alle Features freigeschaltet</span>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("### 🎯 Verfügbare Module")
    
    # Module in 3 Spalten
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown('<div class="info-card">', unsafe_allow_html=True)
        if st.button("🔬 Verhaltensanalyse", use_container_width=True):
            st.session_state.page = "analysis"
            st.rerun()
        st.caption("SORKC-Modell zur Verhaltensanalyse")
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="info-card">', unsafe_allow_html=True)
        if st.button("📔 Digitales Tagebuch", use_container_width=True):
            st.session_state.page = "diary"
            st.rerun()
        st.caption("Strukturierte Selbstreflexion")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="info-card">', unsafe_allow_html=True)
        if st.button("🧠 Gedanken-Check", use_container_width=True):
            st.session_state.page = "thoughts"
            st.rerun()
        st.caption("Kognitive Verzerrungen erkennen")
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="info-card">', unsafe_allow_html=True)
        if st.button("😄 Humor-Therapie", use_container_width=True):
            st.session_state.page = "humor"
            st.rerun()
        st.caption("Heilung durch Humor")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col3:
        st.markdown('<div class="info-card">', unsafe_allow_html=True)
        if st.button("📊 Statistiken", use_container_width=True):
            st.session_state.page = "stats"
            st.rerun()
        st.caption("Deine Fortschritte im Überblick")
        st.markdown('</div>', unsafe_allow_html=True)
        
        if st.session_state.insurance == "PKV":
            st.markdown('<div class="info-card premium-card">', unsafe_allow_html=True)
            if st.button("⭐ Premium-Features", use_container_width=True):
                st.session_state.page = "premium"
                st.rerun()
            st.caption("Exklusive Zusatzfunktionen")
            st.markdown('</div>', unsafe_allow_html=True)

# Verhaltensanalyse-Modul (vollständig überarbeitet)
def show_behavior_analysis():
    """Zeigt das erweiterte Verhaltensanalyse-Modul"""
    # Sicherheitscheck
    if "analyses" not in st.session_state:
        st.session_state.analyses = []
    
    st.markdown("## 🔬 Verhaltensanalyse (SORKC-Modell)")
    
    # Info aus dem PDF
    with st.expander("ℹ️ Was ist eine Verhaltensanalyse?", expanded=False):
        st.markdown("""
        Die Verhaltensanalyse hilft dir, deine Reaktionsmuster zu verstehen und zu verändern.
        
        **Die 4 Phasen:**
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
    
    # Tabs für die 4 Phasen + Übersicht
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
        st.info("💡 Beschreibe rückblickend dein Reaktionsverhalten, die auslösende Situation und die Folgen.")
        
        with st.form("phase1_wahrnehmen", clear_on_submit=True):
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.markdown("#### 📍 Situation")
                st.caption("Wann, was, wer & wo? Was führte zu deiner Reaktion?")
                situation = st.text_area(
                    "Beschreibe die Situation:",
                    placeholder="z.B. Streit mit Partner am Abend in der Küche...",
                    height=120
                )
            
            with col2:
                st.markdown("#### 📅 Zeitpunkt")
                datum = st.date_input("Datum:", datetime.now())
                uhrzeit = st.time_input("Uhrzeit:", datetime.now().time())
            
            # ORGANISMUS
            st.markdown("#### 🧍 Ich (O-Variable)")
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**Aktuelle Tagesform**")
                stimmung = st.slider("Stimmung", 0, 10, 5, help="0 = sehr schlecht, 10 = sehr gut")
                energie = st.select_slider(
                    "Energie-Level", 
                    options=["Sehr niedrig", "Niedrig", "Mittel", "Hoch", "Sehr hoch"],
                    value="Mittel"
                )
                schlaf = st.selectbox(
                    "Schlafqualität letzte Nacht",
                    ["Sehr schlecht", "Schlecht", "OK", "Gut", "Sehr gut"],
                    index=2
                )
            
            with col2:
                st.markdown("**Glaubenssätze/Denkmuster**")
                denkmuster = st.text_area(
                    "Welche Grundannahmen spielten eine Rolle?",
                    placeholder="z.B. 'Ich muss perfekt sein', 'Andere mögen mich nicht'...",
                    height=100
                )
            
            # REAKTION
            st.markdown("#### 💭 Reaktion")
            
            # Gedanken
            gedanken = st.text_area(
                "**Gedanken** (Was ging dir durch den Kopf?):",
                placeholder="z.B. 'Das schaffe ich nie', 'Alle sind gegen mich'...",
                height=100
            )
            
            # Gefühle mit visueller Darstellung
            col1, col2 = st.columns([3, 1])
            with col1:
                gefuehle = st.multiselect(
                    "**Gefühle** (mehrere möglich):",
                    ["😨 Angst", "😡 Wut", "😢 Trauer", "😊 Freude", "😳 Scham", 
                     "😔 Schuld", "🤢 Ekel", "😲 Überraschung", "😞 Enttäuschung", 
                     "😤 Frustration", "😰 Nervosität", "😌 Erleichterung"]
                )
            with col2:
                gefuehl_intensitaet = st.number_input(
                    "Intensität (0-100)",
                    0, 100, 50,
                    step=10
                )
            
            # Körperempfindungen
            col1, col2 = st.columns([3, 1])
            with col1:
                koerper_optionen = st.multiselect(
                    "**Körperempfindungen**:",
                    ["Herzrasen", "Schwitzen", "Zittern", "Übelkeit", "Kopfschmerzen",
                     "Verspannungen", "Schwindel", "Atemnot", "Magenschmerzen"]
                )
                koerper_andere = st.text_input("Andere Körperempfindungen:")
            with col2:
                anspannung = st.number_input(
                    "Anspannung (0-100)",
                    0, 100, 50,
                    step=10
                )
            
            # Verhalten
            verhalten = st.text_area(
                "**Beobachtbares Verhalten** (Was hast du getan?):",
                placeholder="z.B. 'Bin aus dem Raum gegangen', 'Habe laut gesprochen'...",
                height=100
            )
            
            # KONSEQUENZEN
            st.markdown("#### ⚡ Konsequenzen")
            
            col1, col2 = st.columns(2)
            with col1:
                konseq_kurz = st.text_area(
                    "**Kurzfristige Konsequenzen** (sofort bis wenige Minuten):",
                    placeholder="z.B. 'Fühlte mich erleichtert', 'Spannung ließ nach'...",
                    height=100
                )
            
            with col2:
                konseq_lang = st.text_area(
                    "**Langfristige Folgen** (Stunden bis Jahre):",
                    placeholder="z.B. 'Beziehung belastet', 'Selbstvertrauen gesunken'...",
                    height=100
                )
            
            # Häufigkeit
            haeufigkeit = st.selectbox(
                "**Wie oft kommt diese Situation vor?**",
                ["Einmalig", "Selten (1x pro Monat)", "Gelegentlich (1x pro Woche)", 
                 "Häufig (mehrmals pro Woche)", "Täglich", "Mehrmals täglich"]
            )
            
            # Speichern
            submitted = st.form_submit_button("💾 Phase 1 speichern", type="primary", use_container_width=True)
            
            if submitted:
                if situation and verhalten:
                    analyse_id = len(st.session_state.analyses) + 1
                    
                    # Körperempfindungen zusammenführen
                    alle_koerper = koerper_optionen
                    if koerper_andere:
                        alle_koerper.append(koerper_andere)
                    
                    # Neue Analyse erstellen
                    neue_analyse = {
                        "id": analyse_id,
                        "datum": datetime.combine(datum, uhrzeit),
                        "phase1": {
                            "situation": situation,
                            "organismus": {
                                "stimmung": stimmung,
                                "energie": energie,
                                "schlaf": schlaf,
                                "denkmuster": denkmuster
                            },
                            "reaktion": {
                                "gedanken": gedanken,
                                "gefuehle": gefuehle,
                                "gefuehl_intensitaet": gefuehl_intensitaet,
                                "koerper": alle_koerper,
                                "anspannung": anspannung,
                                "verhalten": verhalten
                            },
                            "konsequenzen": {
                                "kurz": konseq_kurz,
                                "lang": konseq_lang
                            },
                            "haeufigkeit": haeufigkeit
                        },
                        "phase2": None,
                        "phase3": None,
                        "phase4": []
                    }
                    
                    st.session_state.analyses.append(neue_analyse)
                    st.success("✅ Phase 1 erfolgreich gespeichert!")
                    st.balloons()
                    st.info("👉 Wechsle zu Phase 2, um deine Analyse fortzusetzen.")
                else:
                    st.error("⚠️ Bitte fülle mindestens Situation und Verhalten aus.")
    
    # Phase 2: ANALYSIEREN
    with tab2:
        st.markdown("### Phase 2: Analysieren")
        st.info("💡 Bewerte deine Reaktionen und finde Ausstiegspunkte für Veränderungen.")
        
        # Analyse auswählen
        if st.session_state.analyses:
            analyse_ids = [f"Analyse #{a['id']} vom {a['datum'].strftime('%d.%m.%Y %H:%M')}" 
                          for a in st.session_state.analyses if a['phase1']]
            
            if analyse_ids:
                selected = st.selectbox("Wähle eine Analyse:", analyse_ids)
                analyse_idx = int(selected.split('#')[1].split(' ')[0]) - 1
                current_analyse = st.session_state.analyses[analyse_idx]
                
                if current_analyse['phase1']:
                    # Zusammenfassung anzeigen
                    with st.expander("📋 Zusammenfassung Phase 1", expanded=True):
                        p1 = current_analyse['phase1']
                        col1, col2 = st.columns(2)
                        with col1:
                            st.write(f"**Situation:** {p1['situation'][:200]}...")
                            st.write(f"**Verhalten:** {p1['reaktion']['verhalten']}")
                        with col2:
                            st.write(f"**Gefühle:** {', '.join([g.split()[1] for g in p1['reaktion']['gefuehle']])}")
                            st.write(f"**Intensität:** {p1['reaktion']['gefuehl_intensitaet']}/100")
                    
                    with st.form("phase2_analysieren"):
                        st.markdown("#### 🎯 Bewertung (Grün = hilfreich, Rot = nicht hilfreich)")
                        
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            st.markdown("**Bewerte die Elemente:**")
                            hilfreich_situation = st.checkbox("✅ Situation war unvermeidbar/neutral")
                            hilfreich_gedanken = st.checkbox("✅ Gedanken waren hilfreich/realistisch")
                            hilfreich_verhalten = st.checkbox("✅ Verhalten war angemessen")
                        
                        with col2:
                            st.markdown("**Bewerte die Folgen:**")
                            hilfreich_kurz = st.checkbox("✅ Kurzfristige Folgen waren positiv")
                            hilfreich_lang = st.checkbox("✅ Langfristige Folgen sind positiv")
                        
                        st.markdown("#### 🚪 Ausstiegspunkt")
                        ausstieg = st.radio(
                            "Wo könntest du die Reaktionskette am besten unterbrechen?",
                            ["🌍 Situation verändern/vermeiden", 
                             "💭 Gedanken hinterfragen", 
                             "🎭 Verhalten ändern", 
                             "🧘 Tagesform verbessern",
                             "😌 Gefühle regulieren"],
                            index=1
                        )
                        
                        ausstieg_wie = st.text_area(
                            "Was würdest du konkret verändern?",
                            placeholder="Beschreibe möglichst genau, was du anders machen würdest...",
                            height=100
                        )
                        
                        st.markdown("#### 🛡️ Strategien")
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            praevention = st.text_area(
                                "**Prävention:** Wie kannst du dich vorbereiten?",
                                placeholder="z.B. Frühwarnzeichen erkennen, Skills vorbereiten...",
                                height=100
                            )
                        
                        with col2:
                            wiedergutmachung = st.text_area(
                                "**Wiedergutmachung:** Was kannst du jetzt tun?",
                                placeholder="z.B. Entschuldigung, Selbstfürsorge...",
                                height=100
                            )
                        
                        submitted = st.form_submit_button("💾 Phase 2 speichern", type="primary", use_container_width=True)
                        
                        if submitted:
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
                            st.success("✅ Phase 2 erfolgreich gespeichert!")
                            st.info("👉 Wechsle zu Phase 3, um alternative Reaktionen zu planen.")
        else:
            st.info("📝 Bitte erstelle zuerst eine Analyse in Phase 1.")
    
    # Phase 3: PLANEN
    with tab3:
        st.markdown("### Phase 3: Planen")
        st.info("💡 Entwirf eine alternative Reaktionskette ab deinem gewählten Ausstiegspunkt.")
        
        if st.session_state.analyses:
            phase2_analyses = [a for a in st.session_state.analyses if a.get('phase2')]
            
            if phase2_analyses:
                analyse_ids = [f"Analyse #{a['id']} vom {a['datum'].strftime('%d.%m.%Y')}" 
                              for a in phase2_analyses]
                
                selected = st.selectbox("Wähle eine Analyse:", analyse_ids, key="phase3_select")
                analyse_idx = int(selected.split('#')[1].split(' ')[0]) - 1
                current_analyse = next(a for a in st.session_state.analyses if a['id'] == analyse_idx + 1)
                
                # Info anzeigen
                with st.expander("📋 Dein gewählter Ausstiegspunkt", expanded=True):
                    st.write(f"**Ausstiegspunkt:** {current_analyse['phase2']['ausstieg']}")
                    st.write(f"**Geplante Veränderung:** {current_analyse['phase2']['ausstieg_wie']}")
                
                with st.form("phase3_planen"):
                    st.markdown("#### 🔄 Alternative Reaktionskette")
                    st.caption("Beschreibe, wie die Situation mit deiner Veränderung ablaufen könnte:")
                    
                    # Je nach Ausstiegspunkt unterschiedliche Schwerpunkte
                    if "Situation" in current_analyse['phase2']['ausstieg']:
                        alt_situation = st.text_area(
                            "**Alternative Situation:**",
                            placeholder="Wie könntest du die Situation anders gestalten oder vermeiden?",
                            height=100
                        )
                    else:
                        alt_situation = current_analyse['phase1']['situation']
                    
                    alt_gedanken = st.text_area(
                        "**Alternative/hilfreiche Gedanken:**",
                        placeholder="z.B. 'Ich gebe mein Bestes', 'Fehler sind menschlich'...",
                        height=100
                    )
                    
                    alt_gefuehle = st.text_area(
                        "**Erwartete Gefühle:**",
                        placeholder="Welche Gefühle würden wahrscheinlich auftreten?",
                        height=80
                    )
                    
                    alt_koerper = st.text_area(
                        "**Erwartete Körperempfindungen:**",
                        placeholder="z.B. 'Entspannter', 'Ruhigere Atmung'...",
                        height=80
                    )
                    
                    alt_verhalten = st.text_area(
                        "**Alternatives Verhalten:**",
                        placeholder="Was würdest du stattdessen tun?",
                        height=100
                    )
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        alt_konseq_kurz = st.text_area(
                            "**Erwartete kurzfristige Konsequenzen:**",
                            placeholder="Was würde direkt danach passieren?",
                            height=100
                        )
                    
                    with col2:
                        alt_konseq_lang = st.text_area(
                            "**Erwartete langfristige Folgen:**",
                            placeholder="Positive Auswirkungen auf dein Leben?",
                            height=100
                        )
                    
                    submitted = st.form_submit_button("💾 Phase 3 speichern", type="primary", use_container_width=True)
                    
                    if submitted:
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
                        st.success("✅ Phase 3 erfolgreich gespeichert!")
                        st.info("👉 Jetzt kannst du mit dem Training beginnen!")
            else:
                st.info("📝 Bitte schließe erst Phase 2 ab.")
        else:
            st.info("📝 Bitte beginne mit Phase 1.")
    
    # Phase 4: TRAINIEREN
    with tab4:
        st.markdown("### Phase 4: Trainieren")
        st.info("💡 Dokumentiere deine Übungsversuche und feiere kleine Erfolge!")
        
        if st.session_state.analyses:
            phase3_analyses = [a for a in st.session_state.analyses if a.get('phase3')]
            
            if phase3_analyses:
                analyse_ids = [f"Analyse #{a['id']} vom {a['datum'].strftime('%d.%m.%Y')}" 
                              for a in phase3_analyses]
                
                selected = st.selectbox("Wähle eine Analyse:", analyse_ids, key="phase4_select")
                analyse_idx = int(selected.split('#')[1].split(' ')[0]) - 1
                current_analyse = next(a for a in st.session_state.analyses if a['id'] == analyse_idx + 1)
                
                # Bisherige Trainings anzeigen
                if current_analyse.get('phase4'):
                    st.markdown("#### 📈 Bisherige Trainingseinheiten")
                    fortschritte = [t['fortschritt'] for t in current_analyse['phase4']]
                    durchschnitt = sum(fortschritte) / len(fortschritte)
                    
                    col1, col2, col3 = st.columns(3)
                    col1.metric("Trainings", len(current_analyse['phase4']))
                    col2.metric("Ø Fortschritt", f"{durchschnitt:.0f}%")
                    col3.metric("Bester Versuch", f"{max(fortschritte)}%")
                    
                    # Fortschritts-Visualisierung
                    st.markdown(f"""
                    <div class="progress-container">
                        <div class="progress-bar" style="width: {durchschnitt}%">
                            {durchschnitt:.0f}%
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                
                # Geplante Alternative anzeigen
                with st.expander("📋 Dein Plan", expanded=False):
                    alt = current_analyse['phase3']['alternative']
                    st.write(f"**Geplantes Verhalten:** {alt['verhalten']}")
                    st.write(f"**Hilfreiche Gedanken:** {alt['gedanken']}")
                
                with st.form("phase4_trainieren"):
                    st.markdown("#### 📝 Neuer Trainingsversuch")
                    
                    col1, col2 = st.columns([3, 1])
                    with col1:
                        training_situation = st.text_area(
                            "**Situation** (Wann und wo hast du geübt?):",
                            placeholder="Beschreibe die Übungssituation...",
                            height=100
                        )
                    with col2:
                        training_datum = st.date_input("Datum:", datetime.now())
                        training_zeit = st.time_input("Uhrzeit:", datetime.now().time())
                    
                    # Fortschritt mit visueller Skala
                    st.markdown("#### 🎯 Umsetzung")
                    fortschritt = st.slider(
                        "Wie gut konntest du deinen Plan umsetzen?",
                        0, 100, 50,
                        help="0% = gar nicht, 100% = vollständig wie geplant"
                    )
                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        geklappt = st.text_area(
                            "**Was hat gut geklappt?** ⭐",
                            placeholder="Feiere deine Erfolge, auch kleine!",
                            height=100
                        )
                    
                    with col2:
                        schwierig = st.text_area(
                            "**Was war schwierig?**",
                            placeholder="Herausforderungen sind normal...",
                            height=100
                        )
                    
                    # Tatsächliche Reaktionen
                    st.markdown("#### 💭 Tatsächliche Reaktionen")
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        tats_gedanken = st.text_area(
                            "Gedanken:",
                            placeholder="Welche Gedanken hattest du wirklich?",
                            height=80
                        )
                        
                        tats_verhalten = st.text_area(
                            "Verhalten:",
                            placeholder="Was hast du tatsächlich getan?",
                            height=80
                        )
                    
                    with col2:
                        tats_gefuehle = st.text_area(
                            "Gefühle:",
                            placeholder="Welche Gefühle sind aufgetreten?",
                            height=80
                        )
                        
                        tats_intensitaet = st.slider(
                            "Gefühls-Intensität:",
                            0, 100, 50
                        )
                    
                    # Erkenntnisse
                    erkenntnisse = st.text_area(
                        "**Neue Erkenntnisse & Learnings:**",
                        placeholder="Was hast du über dich gelernt?",
                        height=100
                    )
                    
                    submitted = st.form_submit_button("💾 Training speichern", type="primary", use_container_width=True)
                    
                    if submitted:
                        if training_situation:
                            if not current_analyse.get('phase4'):
                                current_analyse['phase4'] = []
                            
                            current_analyse['phase4'].append({
                                "datum": datetime.combine(training_datum, training_zeit),
                                "situation": training_situation,
                                "fortschritt": fortschritt,
                                "geklappt": geklappt,
                                "schwierig": schwierig,
                                "reaktionen": {
                                    "gedanken": tats_gedanken,
                                    "gefuehle": tats_gefuehle,
                                    "intensitaet": tats_intensitaet,
                                    "verhalten": tats_verhalten
                                },
                                "erkenntnisse": erkenntnisse
                            })
                            
                            st.success("✅ Training dokumentiert!")
                            
                            # Motivations-Feedback basierend auf Fortschritt
                            if fortschritt >= 80:
                                st.balloons()
                                st.success("🎉 Wow! Über 80% - das ist fantastisch! Du machst große Fortschritte!")
                            elif fortschritt >= 60:
                                st.info("💪 Sehr gut! Du bist auf einem tollen Weg. Weiter so!")
                            elif fortschritt >= 40:
                                st.info("🌱 Gut gemacht! Jeder Schritt zählt. Übung macht den Meister!")
                            else:
                                st.info("🤗 Danke fürs Dokumentieren! Auch schwierige Versuche sind wertvoll. Du lernst mit jedem Mal!")
                        else:
                            st.error("⚠️ Bitte beschreibe die Trainingssituation.")
            else:
                st.info("📝 Bitte schließe erst Phase 3 ab.")
        else:
            st.info("📝 Bitte beginne mit Phase 1.")
    
    # ÜBERSICHT
    with tab5:
        st.markdown("### 📊 Übersicht deiner Verhaltensanalysen")
        
        if st.session_state.analyses:
            # Statistiken
            col1, col2, col3, col4 = st.columns(4)
            
            total = len(st.session_state.analyses)
            phase2_count = len([a for a in st.session_state.analyses if a.get('phase2')])
            phase3_count = len([a for a in st.session_state.analyses if a.get('phase3')])
            phase4_count = len([a for a in st.session_state.analyses if a.get('phase4')])
            
            col1.metric("📋 Analysen gesamt", total)
            col2.metric("🔍 Analysiert", phase2_count)
            col3.metric("📝 Geplant", phase3_count)
            col4.metric("💪 Im Training", phase4_count)
            
            # Filter
            st.markdown("#### 🔍 Filter")
            col1, col2 = st.columns(2)
            with col1:
                filter_phase = st.selectbox(
                    "Phase:",
                    ["Alle", "Nur Phase 1", "Mit Analyse", "Mit Plan", "In Training"]
                )
            with col2:
                filter_zeitraum = st.selectbox(
                    "Zeitraum:",
                    ["Alle", "Letzte Woche", "Letzter Monat", "Letzte 3 Monate"]
                )
            
            # Analysen-Liste
            st.markdown("#### 📚 Deine Analysen")
            
            for analyse in reversed(st.session_state.analyses):
                # Filter anwenden
                if filter_phase == "Nur Phase 1" and analyse.get('phase2'):
                    continue
                elif filter_phase == "Mit Analyse" and not analyse.get('phase2'):
                    continue
                elif filter_phase == "Mit Plan" and not analyse.get('phase3'):
                    continue
                elif filter_phase == "In Training" and not analyse.get('phase4'):
                    continue
                
                # Status-Indikator
                phase_status = "🔴 Phase 1"
                if analyse.get('phase4'):
                    phase_status = "🟢 Training läuft"
                elif analyse.get('phase3'):
                    phase_status = "🟡 Plan erstellt"
                elif analyse.get('phase2'):
                    phase_status = "🟠 Analysiert"
                
                with st.expander(f"{phase_status} | Analyse #{analyse['id']} - {analyse['datum'].strftime('%d.%m.%Y %H:%M')}"):
                    # Übersicht
                    col1, col2 = st.columns([3, 1])
                    
                    with col1:
                        # Phase 1 Details
                        st.markdown("**📍 Situation:**")
                        st.write(analyse['phase1']['situation'][:200] + "..." if len(analyse['phase1']['situation']) > 200 else analyse['phase1']['situation'])
                        
                        if analyse['phase1']['reaktion']['gefuehle']:
                            gefuehle_text = ", ".join([g.split()[1] for g in analyse['phase1']['reaktion']['gefuehle']])
                            st.write(f"**Gefühle:** {gefuehle_text} (Intensität: {analyse['phase1']['reaktion']['gefuehl_intensitaet']}/100)")
                        
                        # Phase 2 Details
                        if analyse.get('phase2'):
                            st.markdown("**🔍 Analyse:**")
                            st.write(f"Ausstiegspunkt: {analyse['phase2']['ausstieg']}")
                            if analyse['phase2']['ausstieg_wie']:
                                st.write(f"Plan: {analyse['phase2']['ausstieg_wie'][:100]}...")
                        
                        # Phase 4 Details
                        if analyse.get('phase4'):
                            st.markdown("**💪 Training:**")
                            trainings = analyse['phase4']
                            letztes = trainings[-1]
                            st.write(f"Letzte Übung: {letztes['datum'].strftime('%d.%m. %H:%M')} - {letztes['fortschritt']}% Erfolg")
                    
                    with col2:
                        st.markdown("**📊 Status:**")
                        st.write(f"Stimmung: {analyse['phase1']['organismus']['stimmung']}/10")
                        st.write(f"Häufigkeit: {analyse['phase1']['haeufigkeit']}")
                        
                        if analyse.get('phase4'):
                            fortschritte = [t['fortschritt'] for t in analyse['phase4']]
                            st.write(f"Ø Training: {sum(fortschritte)/len(fortschritte):.0f}%")
                    
                    # Export-Buttons
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        if st.button(f"📄 Als Text", key=f"txt_{analyse['id']}"):
                            text = export_analysis_as_text(analyse)
                            st.download_button(
                                "💾 Herunterladen",
                                text,
                                f"analyse_{analyse['id']}_{analyse['datum'].strftime('%Y%m%d')}.txt",
                                "text/plain",
                                key=f"download_txt_{analyse['id']}"
                            )
                    
                    with col2:
                        if st.button(f"📊 Als JSON", key=f"json_{analyse['id']}"):
                            json_str = json.dumps(analyse, default=str, indent=2, ensure_ascii=False)
                            st.download_button(
                                "💾 Herunterladen",
                                json_str,
                                f"analyse_{analyse['id']}_{analyse['datum'].strftime('%Y%m%d')}.json",
                                "application/json",
                                key=f"download_json_{analyse['id']}"
                            )
                    
                    with col3:
                        if st.button(f"🗑️ Löschen", key=f"del_{analyse['id']}"):
                            if st.checkbox(f"Wirklich löschen?", key=f"confirm_del_{analyse['id']}"):
                                st.session_state.analyses.remove(analyse)
                                st.rerun()
            
            # Gesamt-Export
            st.markdown("---")
            st.markdown("#### 💾 Alle Analysen exportieren")
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("📄 Alle als Text", use_container_width=True):
                    all_text = "VERHALTENSANALYSEN - GESAMTÜBERSICHT\n" + "="*50 + "\n\n"
                    all_text += f"Exportiert am: {datetime.now().strftime('%d.%m.%Y %H:%M')}\n"
                    all_text += f"Anzahl Analysen: {len(st.session_state.analyses)}\n\n"
                    
                    for analyse in st.session_state.analyses:
                        all_text += export_analysis_as_text(analyse)
                        all_text += "\n" + "="*50 + "\n\n"
                    
                    st.download_button(
                        "💾 Text-Datei herunterladen",
                        all_text,
                        f"alle_analysen_{datetime.now().strftime('%Y%m%d_%H%M')}.txt",
                        "text/plain"
                    )
            
            with col2:
                if st.button("📊 Alle als JSON", use_container_width=True):
                    export_data = {
                        "analysen": st.session_state.analyses,
                        "export_datum": datetime.now().isoformat(),
                        "anzahl": len(st.session_state.analyses)
                    }
                    json_str = json.dumps(export_data, default=str, indent=2, ensure_ascii=False)
                    st.download_button(
                        "💾 JSON-Datei herunterladen",
                        json_str,
                        f"alle_analysen_{datetime.now().strftime('%Y%m%d_%H%M')}.json",
                        "application/json"
                    )
            
            # Insights bei genug Daten
            if len(st.session_state.analyses) >= 3:
                st.markdown("---")
                st.markdown("#### 💡 Deine Muster & Insights")
                
                # Häufigste Gefühle
                alle_gefuehle = []
                for a in st.session_state.analyses:
                    if a['phase1']['reaktion']['gefuehle']:
                        alle_gefuehle.extend([g.split()[1] for g in a['phase1']['reaktion']['gefuehle']])
                
                if alle_gefuehle:
                    gefuehl_counts = Counter(alle_gefuehle)
                    top_gefuehle = gefuehl_counts.most_common(5)
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        st.markdown("**Häufigste Gefühle:**")
                        for gefuehl, count in top_gefuehle:
                            pass
                            
    
    st.markdown("""
    <div class="info-card premium-card">
        <h3>🎯 Erweiterte Analysen</h3>
        <p>Detaillierte Auswertungen deiner Verhaltensmuster mit KI-Unterstützung*</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="info-card premium-card">
        <h3>📱 App-Synchronisation</h3>
        <p>Synchronisiere deine Daten mit der mobilen App*</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="info-card premium-card">
        <h3>🎧 Audio-Übungen</h3>
        <p>Geführte Meditationen und Entspannungsübungen*</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.caption("*Diese Features sind aktuell in Entwicklung")

# Sidebar mit Navigation
def show_sidebar():
    """Zeigt die Sidebar mit Navigation und Statistiken"""
    with st.sidebar:
        st.markdown("### 🧭 Navigation")
        
        if st.button("🏠 Hauptmenü", use_container_width=True):
            st.session_state.page = "dashboard"
            st.rerun()
        
        if st.session_state.insurance:
            st.markdown("---")
            
            # Quick Stats
            st.markdown("### 📊 Quick Stats")
            st.metric("Analysen", len(st.session_state.analyses))
            st.metric("Tagebuch", len(st.session_state.entries))
            
            # Status
            st.markdown("---")
            if st.session_state.insurance == "GKV":
                st.info("🪪 Gesetzlich versichert")
            else:
                st.success("💳 Premium-Status")
            
            # Tools
            st.markdown("---")
            st.markdown("### 🛠️ Tools")
            
            # Backup
            if st.button("💾 Backup erstellen", use_container_width=True):
                backup_data = {
                    "version": "1.0",
                    "created": datetime.now().isoformat(),
                    "insurance": st.session_state.insurance,
                    "analyses": st.session_state.analyses,
                    "entries": st.session_state.entries
                }
                json_string = json.dumps(backup_data, default=str, indent=2, ensure_ascii=False)
                
                st.download_button(
                    "📥 Backup herunterladen",
                    json_string,
                    f"therapie_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                    "application/json"
                )
            
            # Import (nur Platzhalter)
            st.file_uploader("📤 Backup laden", type=['json'], disabled=True, help="Funktion kommt bald!")
            
            # Reset
            st.markdown("---")
            if st.button("🔄 Neu starten", use_container_width=True):
                if st.checkbox("Wirklich alles löschen?"):
                    for key in list(st.session_state.keys()):
                        del st.session_state[key]
                    st.rerun()

# Footer
def show_footer():
    """Zeigt den Footer mit wichtigen Hinweisen"""
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #666; padding: 2rem 0;">
        <p><strong>⚠️ Wichtiger Hinweis</strong></p>
        <p>Diese App ersetzt keine professionelle psychotherapeutische Behandlung!</p>
        <p>Bei akuten Krisen wende dich bitte an:</p>
        <p>📞 <strong>Telefonseelsorge:</strong> 0800 111 0 111 oder 0800 111 0 222 (24/7 kostenlos)</p>
        <p>🚨 <strong>Notfall:</strong> 112</p>
        <p style="margin-top: 2rem; font-size: 0.9rem;">
            Made with ❤️ using Streamlit | Version 1.0
        </p>
    </div>
    """, unsafe_allow_html=True)

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
    elif st.session_state.page == "analysis":
        show_behavior_analysis()
    elif st.session_state.page == "diary":
        show_diary()
    elif st.session_state.page == "thoughts":
        show_thoughts()
    elif st.session_state.page == "humor":
        show_humor()
    elif st.session_state.page == "stats":
        show_stats()
    elif st.session_state.page == "premium":
        show_premium()
    
    # Footer immer anzeigen
    show_footer()

    if __name__ == "__main__":
        main()
        
        else:
            st.info("🌟 Noch keine Analysen vorhanden. Starte mit deiner ersten Verhaltensanalyse in Phase 1!")

# Export-Funktion für Text
def export_analysis_as_text(analyse):
    """Erstellt einen formatierten Text für Export"""
    p1 = analyse['phase1']
    
    # Gefühle als Text
    gefuehle_text = ", ".join([g.split()[1] for g in p1['reaktion']['gefuehle']]) if p1['reaktion']['gefuehle'] else "Keine angegeben"
    koerper_text = ", ".join(p1['reaktion']['koerper']) if p1['reaktion']['koerper'] else "Keine angegeben"
    
    text = f"""
VERHALTENSANALYSE #{analyse['id']} (SORKC-Modell)
{'='*50}
Datum: {analyse['datum'].strftime('%d.%m.%Y %H:%M')}

PHASE 1: WAHRNEHMEN
{'='*20}

SITUATION (S)
{'-'*13}
{p1['situation']}

ORGANISMUS (O)
{'-'*14}
Stimmung: {p1['organismus']['stimmung']}/10
Energie: {p1['organismus']['energie']}
Schlafqualität: {p1['organismus']['schlaf']}
Denkmuster: {p1['organismus']['denkmuster'] or 'Keine angegeben'}

REAKTION (R)
{'-'*12}
Gedanken: {p1['reaktion']['gedanken'] or 'Keine angegeben'}
Gefühle: {gefuehle_text} (Intensität: {p1['reaktion']['gefuehl_intensitaet']}/100)
Körperempfindungen: {koerper_text} (Anspannung: {p1['reaktion']['anspannung']}/100)
Verhalten: {p1['reaktion']['verhalten']}

KONSEQUENZEN (K)
{'-'*16}
Kurzfristig: {p1['konsequenzen']['kurz'] or 'Keine angegeben'}
Langfristig: {p1['konsequenzen']['lang'] or 'Keine angegeben'}

HÄUFIGKEIT: {p1['haeufigkeit']}
"""
    
    # Phase 2
    if analyse.get('phase2'):
        p2 = analyse['phase2']
        bewertung = p2['bewertung']
        hilfreich = sum([bewertung['situation'], bewertung['gedanken'], 
                        bewertung['verhalten'], bewertung['kurz'], bewertung['lang']])
        
        text += f"""

PHASE 2: ANALYSIEREN
{'='*20}
Hilfreiche Elemente: {hilfreich}/5
Ausstiegspunkt: {p2['ausstieg']}
Veränderungsplan: {p2['ausstieg_wie']}
Prävention: {p2['praevention'] or 'Keine angegeben'}
Wiedergutmachung: {p2['wiedergutmachung'] or 'Keine angegeben'}
"""
    
    # Phase 3
    if analyse.get('phase3'):
        p3 = analyse['phase3']['alternative']
        text += f"""

PHASE 3: PLANEN
{'='*16}
Alternative Gedanken: {p3['gedanken']}
Alternatives Verhalten: {p3['verhalten']}
Erwartete kurzfristige Folgen: {p3['konseq_kurz']}
Erwartete langfristige Folgen: {p3['konseq_lang']}
"""
    
    # Phase 4
    if analyse.get('phase4'):
        text += f"""

PHASE 4: TRAINIEREN
{'='*19}
Anzahl Trainingseinheiten: {len(analyse['phase4'])}
"""
        for i, training in enumerate(analyse['phase4'], 1):
            text += f"""
Training #{i} - {training['datum'].strftime('%d.%m.%Y %H:%M')}
Fortschritt: {training['fortschritt']}%
Situation: {training['situation']}
Geklappt: {training['geklappt'] or 'Nicht angegeben'}
Schwierig: {training['schwierig'] or 'Nicht angegeben'}
Erkenntnisse: {training['erkenntnisse'] or 'Keine'}
"""
    
    return text

# Weitere Module (Platzhalter)
def show_diary():
    """Zeigt das Tagebuch-Modul"""
    st.markdown("## 📔 Digitales Tagebuch")
    
    with st.form("diary_entry"):
        mood = st.selectbox(
            "Wie fühlst du dich heute?",
            ["😊 Gut", "😐 Neutral", "😔 Schlecht", "😤 Gestresst", "😌 Entspannt"]
        )
        
        entry = st.text_area("Was beschäftigt dich heute?", height=150)
        
        if st.form_submit_button("Speichern", type="primary"):
            if entry:
                new_entry = {
                    "date": datetime.now(),
                    "mood": mood,
                    "text": entry
                }
                st.session_state.entries.append(new_entry)
                st.success("✅ Eintrag gespeichert!")
                st.balloons()

    if st.session_state.entries:
        st.markdown("### 📚 Letzte Einträge")
        for entry in reversed(st.session_state.entries[-5:]):
            with st.expander(f"{entry['mood']} - {entry['date'].strftime('%d.%m.%Y %H:%M')}"):
                st.write(entry['text'])

def show_thoughts():
    st.markdown("## 🧠 Gedanken-Check")
    st.info("Dieses Modul hilft dir, kognitive Verzerrungen zu erkennen und zu hinterfragen.")
    
    thought = st.text_input("Welcher Gedanke beschäftigt dich?")
    
    if thought:
        st.markdown("### 🔍 Mögliche Denkfallen:")
        
        denkfallen = {
            "Katastrophisieren": "Du malst dir das Schlimmste aus",
            "Schwarz-Weiß-Denken": "Es gibt nur gut oder schlecht, nichts dazwischen",
            "Gedankenlesen": "Du glaubst zu wissen, was andere denken",
            "Übergeneralisierung": "Aus einem Ereignis wird 'immer' oder 'nie'"
        }
        
        for name, beschreibung in denkfallen.items():
            if st.checkbox(name):
                st.caption(f"→ {beschreibung}")
        
        if st.button("💡 Hilfreiche Alternative vorschlagen"):
            st.success(f"Alternative: 'Ich kann mit dieser Herausforderung umgehen und Unterstützung suchen, wenn nötig.'")

def show_humor():
    st.markdown("## 😄 Humor-Therapie")
    
    import random
    
    kategorien = {
        "Therapeuten-Witze": [
            "Patient: 'Ich spreche im Schlaf.' Therapeut: 'Das ist nicht ungewöhnlich.' Patient: 'Aber der ganze Hörsaal lacht!'",
            "Warum gehen Therapeuten nie in den Ruhestand? Sie arbeiten ihre eigenen Probleme auf!",
            "Patient: 'Niemand hört mir zu!' Therapeut: 'Hmm, interessant, erzählen Sie mehr...'"
        ],
        "Motivationssprüche mal anders": [
            "Du bist nicht perfekt - zum Glück, sonst wärst du langweilig!",
            "Fehler sind der Beweis, dass du es versuchst. Manche versuchen es öfter als andere...",
            "Der frühe Vogel fängt den Wurm, aber die zweite Maus bekommt den Käse!"
        ]
    }
    
    kategorie = st.selectbox("Wähle eine Kategorie:", list(kategorien.keys()))
    
    if st.button("😂 Zeig mir was!", type="primary"):
        witz = random.choice(kategorien[kategorie])
        st.markdown(f"""
        <div class="info-card" style="background: #fff3cd; border-color: #ffeeba;">
            <h4>😄 {witz}</h4>
        </div>
        """, unsafe_allow_html=True)
        
        st.caption("Humor ist die beste Medizin - aber bitte nicht überdosieren! 😉")

def show_stats():
    st.markdown("## 📊 Deine Statistiken")
    
    col1, col2, col3 = st.columns(3)
    
    col1.metric("📔 Tagebuch-Einträge", len(st.session_state.entries))
    col2.metric("🔬 Verhaltensanalysen", len(st.session_state.analyses))
    
    # Berechne abgeschlossene Analysen
    completed = len([a for a in st.session_state.analyses if a.get('phase4')])
    col3.metric("✅ Abgeschlossene Analysen", completed)
    
    if st.session_state.analyses:
        st.markdown("### 📈 Fortschritt über Zeit")
        st.info("Hier könnte eine schöne Grafik deiner Fortschritte stehen!")
        
        # Emotionen-Statistik
        if len(st.session_state.analyses) >= 2:
            st.markdown("### 😊 Gefühls-Statistik")
            alle_gefuehle = []
            for a in st.session_state.analyses:
                if a['phase1']['reaktion']['gefuehle']:
                    alle_gefuehle.extend([g.split()[1] for g in a['phase1']['reaktion']['gefuehle']])
            
            if alle_gefuehle:
                gefuehl_counts = Counter(alle_gefuehle)
                st.write("Deine häufigsten Gefühle:")
                for gefuehl, count in gefuehl_counts.most_common(5):
                    st.write(f"•
