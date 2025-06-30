import streamlit as st
import datetime

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

def show_humor():
    st.markdown("## 😄 Humor-Therapie")
    st.info("Dieses Modul wird noch entwickelt...")

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
    elif st.session_state.page == "humor":
        show_humor()
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
