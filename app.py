import streamlit as st
from datetime import datetime

# Seiten-Konfiguration
st.set_page_config(
    page_title="Taschen-Therapeut", 
    page_icon="🧠", 
    layout="wide",
    initial_sidebar_state="collapsed"  # Für mobile Nutzung
)

# Session State initialisieren
if "page" not in st.session_state:
    st.session_state.page = "home"
if "analyses" not in st.session_state:
    st.session_state.analyses = []

# Einfaches CSS für mobile Optimierung
st.markdown("""
<style>
    /* Mobile Optimierung */
    @media (max-width: 768px) {
        .block-container {
            padding: 1rem;
        }
    }
    
    /* Basis Styling */
    .stButton > button {
        width: 100%;
        margin: 0.25rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Header
def show_header():
    st.title("🧠 Taschen-Therapeut")
    st.caption("Verhaltensanalyse nach SORKC")

# Navigation
def show_navigation():
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🏠 Start"):
            st.session_state.page = "home"
            st.rerun()
    
    with col2:
        if st.button("➕ Neue Analyse"):
            st.session_state.page = "new"
            st.rerun()
    
    with col3:
        if st.button("📋 Meine Analysen"):
            st.session_state.page = "list"
            st.rerun()

# Startseite
def show_home():
    st.markdown("### Willkommen!")
    st.write("Diese App hilft dir, deine Verhaltensmuster zu verstehen.")
    
    st.info("""
    **SORKC steht für:**
    - S = Situation
    - O = Organismus (deine Verfassung)
    - R = Reaktion
    - K = Konsequenzen
    - C = Kontingenzen (Häufigkeit)
    """)
    
    if st.button("🚀 Erste Analyse starten", type="primary"):
        st.session_state.page = "new"
        st.rerun()

# Neue Analyse
def show_new_analysis():
    st.markdown("### Neue Verhaltensanalyse")
    
    with st.form("new_analysis"):
        # SITUATION
        st.markdown("#### 1. Situation")
        situation = st.text_area(
            "Was ist passiert?",
            placeholder="Beschreibe die Situation...",
            height=100
        )
        
        # ORGANISMUS
        st.markdown("#### 2. Deine Verfassung")
        col1, col2 = st.columns(2)
        with col1:
            stimmung = st.slider("Stimmung", 1, 10, 5)
        with col2:
            stress = st.slider("Stress", 1, 10, 5)
        
        # REAKTION
        st.markdown("#### 3. Deine Reaktion")
        gedanken = st.text_area("Gedanken", height=80)
        gefuehle = st.text_input("Gefühle")
        verhalten = st.text_area("Verhalten", height=80)
        
        # KONSEQUENZEN
        st.markdown("#### 4. Konsequenzen")
        konsequenzen = st.text_area("Was passierte danach?", height=80)
        
        # Speichern
        if st.form_submit_button("💾 Speichern", type="primary"):
            if situation and verhalten:
                analyse = {
                    "id": len(st.session_state.analyses) + 1,
                    "datum": datetime.now(),
                    "situation": situation,
                    "stimmung": stimmung,
                    "stress": stress,
                    "gedanken": gedanken,
                    "gefuehle": gefuehle,
                    "verhalten": verhalten,
                    "konsequenzen": konsequenzen
                }
                st.session_state.analyses.append(analyse)
                st.success("✅ Gespeichert!")
                st.balloons()
            else:
                st.error("Bitte fülle mindestens Situation und Verhalten aus.")

# Analysen anzeigen
def show_analyses_list():
    st.markdown("### Meine Analysen")
    
    if not st.session_state.analyses:
        st.info("Noch keine Analysen vorhanden.")
    else:
        for analyse in reversed(st.session_state.analyses):
            with st.expander(f"Analyse #{analyse['id']} - {analyse['datum'].strftime('%d.%m.%Y %H:%M')}"):
                st.write(f"**Situation:** {analyse['situation']}")
                st.write(f"**Stimmung:** {analyse['stimmung']}/10 | **Stress:** {analyse['stress']}/10")
                st.write(f"**Verhalten:** {analyse['verhalten']}")
                
                # Export Button
                text = f"""VERHALTENSANALYSE #{analyse['id']}
Datum: {analyse['datum'].strftime('%d.%m.%Y %H:%M')}

SITUATION: {analyse['situation']}
STIMMUNG: {analyse['stimmung']}/10
STRESS: {analyse['stress']}/10
GEDANKEN: {analyse['gedanken']}
GEFÜHLE: {analyse['gefuehle']}
VERHALTEN: {analyse['verhalten']}
KONSEQUENZEN: {analyse['konsequenzen']}
"""
                
                st.download_button(
                    "📥 Als Text",
                    text,
                    f"analyse_{analyse['id']}.txt",
                    key=f"download_{analyse['id']}"
                )

# Hauptfunktion
def main():
    show_header()
    show_navigation()
    
    st.markdown("---")
    
    # Routing
    if st.session_state.page == "home":
        show_home()
    elif st.session_state.page == "new":
        show_new_analysis()
    elif st.session_state.page == "list":
        show_analyses_list()
    
    # Footer
    st.markdown("---")
    st.caption("⚠️ Diese App ersetzt keine professionelle Therapie!")

if __name__ == "__main__":
    main()
