def show_loading_animation():
    st.image("glockenkurve_ladeanimation.gif", caption="Versicherungsstatus wird analysiert...", use_container_width=True)

    ladeplatz = st.empty()
    ladebotschaften = [
        "🧠 Analysiere deine Versichertenzugehörigkeit…",
        "📑 Prüfe Wartezeit im seelischen Wartezimmer…",
        "💸 Vergleichst du Leistungen oder nur Leidensdruck?",
    ]

    for botschaft in ladebotschaften:
        ladeplatz.markdown(f'<div style="text-align: center; color: #000000;">{botschaft}</div>', unsafe_allow_html=True)
        time.sleep(1.7)  # Langsamer Wechsel

    # Nach ca. 5 Sekunden Button anzeigen
    st.markdown("""
        <style>
        .weiter-button button {
            background-color: #f4c2c2;
            color: #000000;
            border: none;
            padding: 10px 20px;
            font-size: 1.1em;
            border-radius: 8px;
            margin-top: 20px;
            transition: 0.3s;
        }
        .weiter-button button:hover {
            background-color: #f2b6b6;
            transform: scale(1.02);
        }
        </style>
    """, unsafe_allow_html=True)

    # Button wird erst angezeigt, wenn Zeit abgelaufen ist
    with st.container():
        if st.markdown('<div class="weiter-button">', unsafe_allow_html=True) or True:
            if st.button("B2.01 besuchen"):
                st.session_state["scanned"] = True
