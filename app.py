with st.form("behavior_analysis_form"):
            st.markdown("**📍 SITUATION (Auslöser)**")
            col1, col2 = st.columns(2)
            
            with col1:
                situation_when = st.text_input("Wann?", placeholder="z.B. Heute Morgen, 14:30 Uhr")
                situation_where = st.text_input("Wo?", placeholder="z.B. Im Büro, zu Hause")
            
            with col2:
                situation_who = st.text_input("Wer war dabei?", placeholder="z.B. Kollegen, Familie, allein")
                situation_what = st.text_area("Was ist passiert?", placeholder="Beschreibe die konkrete Situation...", height=80)
            
            st.markdown("---")
            st.markdown("**🧠 ORGANISMUS-VARIABLEN (Deine Verfassung)**")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**Aktuelle Tagesform:**")
                mood_scale = st.slider("Stimmung (0-10)", 0, 10, 5, help="0 = sehr schlecht, 10 = sehr gut")
                energy_level = st.selectbox("Energielevel", ["Sehr müde", "Etwas müde", "Normal", "Energetisch", "Sehr energetisch"])
                stress_level = st.selectbox("Stress-Level", ["Entspannt", "Leicht angespannt", "Gestresst", "Sehr gestresst", "Überwältigt"])
            
            with col2:
                st.markdown("**Grundannahmen/Denkmuster:**")
                belief_patterns = st.multiselect(
                    "Welche Denkmuster waren aktiv?",
                    ["Perfektionismus", "Katastrophisieren", "Schwarz-Weiß-Denken", 
                     "Selbstkritik", "Sorgen um andere", "Kontrollbedürfnis",
                     "Versagensangst", "Nicht-gut-genug-sein", "Andere"]
                )
                other_beliefs = st.text_input("Andere Denkmuster:", placeholder="z.B. spezifische Glaubenssätze")
            
            st.markdown("---")
            st.markdown("**🧩 REAKTIONEN**")
            
            # Gedanken
            st.markdown("**💭 Gedanken**")
            thoughts = st.text_area(
                "Welche Gedanken gingen dir durch den Kopf?",
                placeholder="z.B. 'Das schaffe ich nie', 'Was denken die anderen über mich?'",
                height=100
            )
            
            # Gefühle
            st.markdown("**💙 Gefühle**")
            col1, col2 = st.columns(2)
            
            with col1:
                primary_emotions = st.multiselect(
                    "Hauptgefühle:",
                    ["Angst", "Traurigkeit", "Wut", "Freude", "Scham", "Schuld", 
                     "Enttäuschung", "Frustration", "Hilflosigkeit", "Überforderung"]
                )
            
            with col2:
                emotion_intensity = st.slider("Intensität der Gefühle (0-100)", 0, 100, 50)
            
            # Körperempfindungen
            st.markdown("**🫀 Körperempfindungen**")
            col1, col2 = st.columns(2)
            
            with col1:
                body_sensations = st.multiselect(
                    "Körperliche Reaktionen:",
                    ["Herzklopfen", "Schwitzen", "Zittern", "Bauchschmerzen", "Kopfschmerzen",
                     "Muskelverspannungen", "Atemnot", "Schwindel", "Übelkeit", "Hitze/Kälte"]
                )
            
            with col2:
                tension_level = st.slider("Körperliche Anspannung (0-100)", 0, 100, 50)
            
            # Verhalten
            st.markdown("**🎭 Beobachtbares Verhalten**")
            behavior_description = st.text_area(
                "Was hast du konkret getan? (So dass es jemand filmen könnte)",
                placeholder="z.B. 'Bin aufgestanden und weggegangen', 'Habe laut geschrien', 'Bin stumm geworden'",
                height=100
            )
            
            st.markdown("---")
            st.markdown("**⚡ KONSEQUENZEN**")
            
            # Kurzfristige Konsequenzen
            st.markdown("**🔄 Kurzfristige Konsequenzen (sofort danach)**")
            short_term_consequences = st.text_area(
                "Was passierte unmittelbar nach deinem Verhalten?",
                placeholder="z.B. 'Anspannung ließ nach', 'Andere schauten mich an', 'Fühlte mich erleichtert'",
                height=80
            )
            
            # Langfristige Folgen
            st.markdown("**📈 Langfristige Folgen (Stunden/Tage später)**")
            long_term_consequences = st.text_area(
                "Welche Auswirkungen hatte dein Verhalten langfristig?",
                placeholder="z.B. 'Schuldgefühle', 'Konflikt verschärft', 'Problem ungelöst', 'Selbstvertrauen gesunken'",
                height=80
            )
            
            # Zusätzliche Informationen
            st.markdown("---")
            st.markdown("**📝 Zusätzliche Beobachtungen**")
            additional_notes = st.text_area(
                "Weitere wichtige Beobachtungen:",
                placeholder="Alles was dir noch wichtig erscheint...",
                height=60
            )
            
            # Submit Button
            submitted = st.form_submit_button("💾 Verhaltensanalyse speichern", type="primary")
            
            if submitted:
                if situation_what and thoughts and behavior_description:
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
                        "additional_notes": additional_notes,
                        "analysis_phase": "documented",  # documented -> analyzed -> planned -> trained
                        "helpful_aspects": {},
                        "exit_points": [],
                        "prevention_strategies": "",
                        "repair_strategies": ""
                    }
                    
                    st.session_state.behavior_analyses.append(new_analysis)
                    st.success("🎉 Verhaltensanalyse erfolgreich gespeichert!")
                    st.balloons()
                    
                    # Sofortiges Feedback
                    st.markdown("""
                    <div class="quote-box">
                        <h4>✨ Gut gemacht!</h4>
                        <p>Du hast den ersten wichtigen Schritt gemacht: <strong>Bewusstsein schaffen</strong>.</p>
                        <p>Diese Analyse ist jetzt in deinem persönlichen Archiv gespeichert. 
                        Im nächsten Schritt können wir sie gemeinsam analysieren und Veränderungsstrategien entwickeln.</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                else:
                    st.error("⚠️ Bitte fülle mindestens die Felder 'Situation', 'Gedanken' und 'Verhalten' aus.")
    
    with tab2:
        st.markdown("### 📊 Meine Verhaltensanalysen")
        st.markdown("*Übersicht über deine dokumentierten Verhaltensmuster*")
        
        if st.session_state.behavior_analyses:
            # Statistiken
            total_analyses = len(st.session_state.behavior_analyses)
            analyzed_count = len([a for a in st.session_state.behavior_analyses if a.get('analysis_phase') in ['analyzed', 'planned', 'trained']])
            planned_count = len([a for a in st.session_state.behavior_analyses if a.get('analysis_phase') in ['planned', 'trained']])
            trained_count = len([a for a in st.session_state.behavior_analyses if a.get('analysis_phase') == 'trained'])
            
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("📝 Gesamt", total_analyses)
            col2.metric("🔍 Analysiert", analyzed_count)
            col3.metric("📋 Geplant", planned_count)
            col4.metric("🎯 Trainiert", trained_count)
            
            # Fortschrittsbalken
            if total_analyses > 0:
                progress_percentage = (trained_count / total_analyses) * 100
                st.markdown(f"""
                <div class="progress-container">
                    <div class="progress-bar" style="width: {progress_percentage}%"></div>
                </div>
                <p style="text-align: center;">Bearbeitungsfortschritt: {progress_percentage:.1f}%</p>
                """, unsafe_allow_html=True)
            
            st.markdown("---")
            
            # Filter und Sortierung
            col1, col2 = st.columns(2)
            
            with col1:
                filter_phase = st.selectbox(
                    "Nach Phase filtern:",
                    ["Alle", "Dokumentiert", "Analysiert", "Geplant", "Trainiert"]
                )
            
            with col2:
                sort_order = st.selectbox("Sortierung:", ["Neueste zuerst", "Älteste zuerst"])
            
            # Gefilterte Analysen
            filtered_analyses = st.session_state.behavior_analyses.copy()
            
            if filter_phase != "Alle":
                phase_map = {
                    "Dokumentiert": "documented",
                    "Analysiert": "analyzed", 
                    "Geplant": "planned",
                    "Trainiert": "trained"
                }
                filtered_analyses = [a for a in filtered_analyses if a.get('analysis_phase') == phase_map[filter_phase]]
            
            if sort_order == "Neueste zuerst":
                filtered_analyses = sorted(filtered_analyses, key=lambda x: x['timestamp'], reverse=True)
            else:
                filtered_analyses = sorted(filtered_analyses, key=lambda x: x['timestamp'])
            
            # Analysen anzeigen
            st.markdown(f"**📋 {len(filtered_analyses)} Analyse(n) gefunden**")
            
            for i, analysis in enumerate(filtered_analyses):
                timestamp = datetime.datetime.fromisoformat(analysis['timestamp'])
                date_str = timestamp.strftime("%d.%m.%Y %H:%M")
                
                # Status Badge
                phase = analysis.get('analysis_phase', 'documented')
                phase_colors = {
                    'documented': '#74b9ff',
                    'analyzed': '#fdcb6e', 
                    'planned': '#e17055',
                    'trained': '#00b894'
                }
                phase_names = {
                    'documented': '📝 Dokumentiert',
                    'analyzed': '🔍 Analysiert',
                    'planned': '📋 Geplant', 
                    'trained': '🎯 Trainiert'
                }
                
                phase_color = phase_colors.get(phase, '#ddd')
                phase_name = phase_names.get(phase, 'Unbekannt')
                
                with st.expander(f"#{analysis['id']} | {date_str} | {analysis['situation']['what'][:50]}..."):
                    # Status und Aktionen
                    col1, col2 = st.columns([2, 1])
                    
                    with col1:
                        st.markdown(f"""
                        <div style="background: {phase_color}; color: white; padding: 0.5em 1em; border-radius: 20px; display: inline-block; margin-bottom: 1em;">
                            {phase_name}
                        </div>
                        """, unsafe_allow_html=True)
                    
                    with col2:
                        if st.button(f"🔍 Bearbeiten", key=f"edit_{analysis['id']}"):
                            st.session_state.selected_analysis_for_editing = analysis['id']
                            st.info("Wechsle zum 'Analysieren'-Tab um fortzufahren!")
                    
                    # Analyse-Zusammenfassung
                    st.markdown("**📍 Situation:**")
                    st.write(f"• **Wann:** {analysis['situation']['when']}")
                    st.write(f"• **Wo:** {analysis['situation']['where']}")
                    st.write(f"• **Wer:** {analysis['situation']['who']}")
                    st.write(f"• **Was:** {analysis['situation']['what']}")
                    
                    st.markdown("**🧠 Reaktionen:**")
                    st.write(f"• **Gedanken:** {analysis['reactions']['thoughts'][:100]}...")
                    st.write(f"• **Gefühle:** {', '.join(analysis['reactions']['emotions'])} (Intensität: {analysis['reactions']['emotion_intensity']}/100)")
                    st.write(f"• **Verhalten:** {analysis['reactions']['behavior'][:100]}...")
                    
                    # Weitere Details ausklappbar
                    with st.expander("📊 Vollständige Details"):
                        st.json(analysis)
        
        else:
            st.info("📝 Noch keine Verhaltensanalysen erstellt. Starte mit dem ersten Tab!")
    
    with tab3:
        st.markdown("### 🔍 Analyse bewerten und Ausstiegspunkte finden")
        st.markdown("*Bewerte deine Reaktionen und finde Ansatzpunkte für Veränderungen*")
        
        # Analyse zum Bearbeiten auswählen
        if st.session_state.behavior_analyses:
            # Auswahl der zu analysierenden Verhaltensanalyse
            analysis_options = []
            for analysis in st.session_state.behavior_analyses:
                timestamp = datetime.datetime.fromisoformat(analysis['timestamp'])
                date_str = timestamp.strftime("%d.%m.%Y")
                situation_preview = analysis['situation']['what'][:30] + "..."
                analysis_options.append(f"#{analysis['id']} - {date_str} - {situation_preview}")
            
            selected_analysis_index = st.selectbox(
                "Welche Analyse möchtest du bearbeiten?",
                range(len(analysis_options)),
                format_func=lambda x: analysis_options[x],
                index=0
            )
            
            selected_analysis = st.session_state.behavior_analyses[selected_analysis_index]
            
            st.markdown("---")
            
            # Analyse-Bewertung
            st.markdown(f"**🔍 Analysiere: {selected_analysis['situation']['what'][:50]}...**")
            
            # Hilfreich/Weniger hilfreich Bewertung
            st.markdown("**✅❌ Bewerte deine Reaktionen als hilfreich oder weniger hilfreich:**")
            
            rating_categories = {
                "Situation": {
                    "description": "War die Situation vermeidbar oder besser handhabbar?",
                    "content": selected_analysis['situation']['what']
                },
                "Gedanken": {
                    "description": "Waren deine Gedanken hilfreich und realistisch?", 
                    "content": selected_analysis['reactions']['thoughts']
                },
                "Gefühle": {
                    "description": "Waren die Gefühle angemessen für die Situation?",
                    "content": f"{', '.join(selected_analysis['reactions']['emotions'])} (Intensität: {selected_analysis['reactions']['emotion_intensity']}/100)"
                },
                "Verhalten": {
                    "description": "War dein Verhalten zielführend?",
                    "content": selected_analysis['reactions']['behavior']
                },
                "Kurzfristige Folgen": {
                    "description": "Waren die sofortigen Konsequenzen positiv?",
                    "content": selected_analysis['consequences']['short_term']
                },
                "Langfristige Folgen": {
                    "description": "Unterstützen die langfristigen Folgen deine Ziele?",
                    "content": selected_analysis['consequences']['long_term']
                }
            }
            
            helpful_ratings = {}
            
            for category, info in rating_categories.items():
                st.markdown(f"**{category}:** {info['content'][:100]}...")
                
                col1, col2, col3 = st.columns([2, 1, 1])
                
                with col1:
                    st.caption(info['description'])
                
                with col2:
                    if st.button(f"✅ Hilfreich", key=f"helpful_{category}"):
                        helpful_ratings[category] = "helpful"
                        st.success(f"{category} als hilfreich markiert!")
                
                with col3:
                    if st.button(f"❌ Weniger hilfreich", key=f"unhelpful_{category}"):
                        helpful_ratings[category] = "unhelpful"
                        st.warning(f"{category} als weniger hilfreich markiert!")
            
            # Ausstiegspunkte identifizieren
            st.markdown("---")
            st.markdown("**🚪 Ausstiegspunkte identifizieren:**")
            st.markdown("*An welchem Punkt hättest du die Reaktionskette unterbrechen können?*")
            
            exit_points = []
            
            exit_options = {
                "🔔 Frühwarnung": "Situation früher erkennen und vermeiden",
                "🧠 Gedanken stoppen": "Automatische Gedanken unterbrechen",
                "💙 Gefühle regulieren": "Emotionsregulationstechniken anwenden", 
                "🫀 Körper beruhigen": "Körperliche Anspannung reduzieren",
                "🎭 Verhalten ändern": "Alternative Verhaltensweise wählen",
                "⏸️ Pause einlegen": "Kurz innehalten vor der Reaktion"
            }
            
            st.markdown("**Mögliche Ausstiegspunkte:**")
            
            for exit_key, exit_description in exit_options.items():
                if st.checkbox(f"{exit_key} {exit_description}", key=f"exit_{exit_key}"):
                    exit_points.append(exit_key)
                    
                    # Konkrete Strategie erfragen
                    strategy = st.text_input(
                        f"Was würdest du konkret anders machen? ({exit_key})",
                        key=f"strategy_{exit_key}",
                        placeholder="Beschreibe deine alternative Reaktion..."
                    )
                    
                    if strategy:
                        helpful_ratings[f"strategy_{exit_key}"] = strategy
            
            # Prävention und Wiedergutmachung
            st.markdown("---")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**🛡️ Prävention:**")
                prevention_strategies = st.text_area(
                    "Wie könntest du dich auf ähnliche Situationen vorbereiten?",
                    placeholder="z.B. Entspannungsübungen lernen, Situation vorab besprechen...",
                    height=100
                )
            
            with col2:
                st.markdown("**🔧 Wiedergutmachung:**")
                repair_strategies = st.text_area(
                    "Was könntest du tun, um die aktuelle Situation zu verbessern?",
                    placeholder="z.B. Entschuldigung, Gespräch führen, sich selbst etwas Gutes tun...",
                    height=100
                )
            
            # Analyse speichern
            if st.button("💾 Analyse-Ergebnisse speichern", type="primary"):
                # Update der ausgewählten Analyse
                selected_analysis['helpful_aspects'] = helpful_ratings
                selected_analysis['exit_points'] = exit_points
                selected_analysis['prevention_strategies'] = prevention_strategies
                selected_analysis['repair_strategies'] = repair_strategies
                selected_analysis['analysis_phase'] = 'analyzed'
                
                # Speichern in Session State
                st.session_state.behavior_analyses[selected_analysis_index] = selected_analysis
                
                st.success("🎉 Analyse-Bewertung gespeichert!")
                st.balloons()
                
                # Feedback geben
                unhelpful_count = len([v for v in helpful_ratings.values() if v == "unhelpful"])
                exit_count = len(exit_points)
                
                st.markdown(f"""
                <div class="quote-box">
                    <h4>📊 Deine Analyse-Zusammenfassung:</h4>
                    <p>• <strong>{unhelpful_count}</strong> Aspekte als "weniger hilfreich" identifiziert</p>
                    <p>• <strong>{exit_count}</strong> mögliche Ausstiegspunkte gefunden</p>
                    <p>• Präventionsstrategien entwickelt: {"✅" if prevention_strategies else "❌"}</p>
                    <p>• Wiedergutmachung geplant: {"✅" if repair_strategies else "❌"}</p>
                    <br>
                    <p><strong>Nächster Schritt:</strong> Gehe zum "Planen"-Tab um alternative Reaktionen zu entwickeln!</p>
                </div>
                """, unsafe_allow_html=True)
        
        else:
            st.info("📝 Erstelle erst eine Verhaltensanalyse im ersten Tab!")
    
    with tab4:
        st.markdown("### 📋 Alternative Reaktionen planen")
        st.markdown("*Entwickle neue, hilfreichere Verhaltensweisen*")
        
        # Analysierte Analysen zur Auswahl
        analyzed_analyses = [a for a in st.session_state.behavior_analyses if a.get('analysis_phase') in ['analyzed', 'planned', 'trained']]
        
        if analyzed_analyses:
            # Auswahl der zu planenden Analyse
            planning_options = []
            for analysis in analyzed_analyses:
                timestamp = datetime.datetime.fromisoformat(analysis['timestamp'])
                date_str = timestamp.strftime("%d.%m.%Y")
                situation_preview = analysis['situation']['what'][:30] + "..."
                planning_options.append(f"#{analysis['id']} - {date_str} - {situation_preview}")
            
            selected_planning_index = st.selectbox(
                "Für welche Analyse möchtest du Alternativen planen?",
                range(len(planning_options)),
                format_func=lambda x: planning_options[x]
            )
            
            selected_analysis = analyzed_analyses[selected_planning_index]
            
            st.markdown("---")
            
            # Planning Interface
            st.markdown(f"**📋 Plane Alternativen für: {selected_analysis['situation']['what'][:50]}...**")
            
            # Zeige identifizierte Ausstiegspunkte
            if selected_analysis.get('exit_points'):
                st.markdown("**🚪 Deine identifizierten Ausstiegspunkte:**")
                for exit_point in selected_analysis['exit_points']:
                    st.markdown(f"• {exit_point}")
            
            st.markdown("---")
            st.markdown("**🔄 Entwirf eine alternative Reaktionskette:**")
            st.markdown("*Beginne an deinem gewählten Ausstiegspunkt und beschreibe, was du anders machen würdest*")
            
            # Alternative Reaktionskette planen
            with st.form("alternative_planning_form"):
                st.markdown("**📍 Situationsveränderung (falls möglich):**")
                alt_situation = st.text_area(
                    "Könntest du die auslösende Situation verändern oder früher erkennen?",
                    value=selected_analysis['situation']['what'],
                    height=80
                )
                
                st.markdown("**🧠 Alternative Gedanken:**")
                alt_thoughts = st.text_area(
                    "Welche hilfreichen Gedanken könntest du stattdessen denken?",
                    placeholder="z.B. 'Ich kann das Schritt für Schritt angehen', 'Das ist eine Herausforderung, aber machbar'",
                    height=100
                )
                
                st.markdown("**💙 Erwartete Gefühle:**")
                col1, col2 = st.columns(2)
                
                with col1:
                    alt_emotions = st.multiselect(
                        "Welche Gefühle würden die neuen Gedanken auslösen?",
                        ["Ruhe", "Zuversicht", "Konzentration", "Entschlossenheit", 
                         "Gelassenheit", "Motivation", "Klarheit", "Selbstvertrauen"]
                    )
                
                with col2:
                    alt_emotion_intensity = st.slider(
                        "Erwartete Intensität (0-100):",
                        0, 100, 30,
                        help="Oft sind alternative Emotionen weniger intensiv"
                    )
                
                st.markdown("**🫀 Körperliche Veränderungen:**")
                alt_body_sensations = st.multiselect(
                    "Welche körperlichen Veränderungen erwartest du?",
                    ["Entspannte Muskeln", "Ruhiger Atem", "Normaler Herzschlag", 
                     "Weniger Anspannung", "Ausgeglichenheit", "Mehr Energie"]
                )
                
                alt_tension_level = st.slider("Erwartete Anspannung (0-100):", 0, 100, 20)
                
                st.markdown("**🎭 Alternatives Verhalten:**")
                alt_behavior = st.text_area(
                    "Was würdest du konkret anders machen?",
                    placeholder="Beschreibe dein neues Verhalten so konkret wie möglich...",
                    height=120
                )
                
                st.markdown("**⚡ Erwartete Konsequenzen:**")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    alt_short_consequences = st.text_area(
                        "Kurzfristige Folgen des neuen Verhaltens:",
                        placeholder="Was würde sofort passieren?",
                        height=80
                    )
                
                with col2:
                    alt_long_consequences = st.text_area(
                        "Langfristige Folgen des neuen Verhaltens:",
                        placeholder="Wie würde sich das langfristig auswirken?",
                        height=80
                    )
                
                st.markdown("**🎯 Umsetzungsplanung:**")
                
                implementation_plan = st.text_area(
                    "Wie willst du diese Alternativen konkret üben/umsetzen?",
                    placeholder="z.B. 'Ich werde täglich 5 Min die neuen Gedanken üben', 'Beim nächsten Mal atme ich erst tief durch'",
                    height=80
                )
                
                success_criteria = st.text_input(
                    "Woran erkennst du, dass es funktioniert hat?",
                    placeholder="z.B. 'Ich bleibe ruhiger', 'Das Gespräch verläuft besser'"
                )
                
                # Submit Planning
                planning_submitted = st.form_submit_button("💾 Alternative Reaktionskette speichern", type="primary")
                
                if planning_submitted and alt_thoughts and alt_behavior:
                    # Finde die ursprüngliche Analyse und aktualisiere sie
                    original_index = next(i for i, a in enumerate(st.session_state.behavior_analyses) if a['id'] == selected_analysis['id'])
                    
                    # Speichere die geplanten Alternativen
                    st.session_state.behavior_analyses[original_index]['planned_alternatives'] = {
                        "situation": alt_situation,
                        "thoughts": alt_thoughts,
                        "emotions": alt_emotions,
                        "emotion_intensity": alt_emotion_intensity,
                        "body_sensations": alt_body_sensations,
                        "tension_level": alt_tension_level,
                        "behavior": alt_behavior,
                        "short_consequences": alt_short_consequences,
                        "long_consequences": alt_long_consequences,
                        "implementation_plan": implementation_plan,
                        "success_criteria": success_criteria
                    }
                    
                    st.session_state.behavior_analyses[original_index]['analysis_phase'] = 'planned'
                    
                    st.success("🎉 Alternative Reaktionskette geplant!")
                    st.balloons()
                    
                    st.markdown(f"""
                    <div class="quote-box">
                        <h4>🎯 Dein Veränderungsplan ist bereit!</h4>
                        <p><strong>Neue Gedanken:</strong> {alt_thoughts[:100]}...</p>
                        <p><strong>Neues Verhalten:</strong> {alt_behavior[:100]}...</p>        else:
            # Denkfallen-Übersicht ohne konkreten Gedanken
            st.markdown("**🎓 Lerne die häufigsten Denkfallen kennen:**")
            
            for distortion_name, distortion_info in cognitive_distortions.items():
                with st.expander(f"{distortion_name} - {distortion_info['description']}"):
                    st.markdown(f"**Beispiel:** {distortion_info['example']}")
                    st.markdown(f"**Gegenmittel:** {distortion_info['counter']}")
                    st.markdown("**Hilfreiche Fragen:**")
                    for question in distortion_info['questions']:
                        st.markdown(f"• {question}")
    
    with tab3:
        st.markdown("### 💭 Gedanken-Protokoll")
        st.markdown("*Dokumentiere deine automatischen Gedanken über den Tag*")
        
        if "thought_log" not in st.session_state:
            st.session_state.thought_log = []
        
        # Neuen Gedanken hinzufügen
        st.markdown("**📝 Gedanken-Eintrag erstellen:**")
        
        col1, col2 = st.columns(2)
        
        with col1:
            thought_situation = st.text_input("In welcher Situation?", placeholder="z.B. 'Meeting mit Chef'")
            automatic_thought = st.text_area("Automatischer Gedanke:", placeholder="z.B. 'Das wird bestimmt schlecht laufen'")
            thought_emotion = st.selectbox("Resultierende Emotion:", 
                                         ["😰 Angst", "😢 Traurigkeit", "😡 Wut", "😖 Frustration", "😔 Hoffnungslosigkeit"])
        
        with col2:
            emotion_intensity = st.slider("Emotionsintensität (1-10):", 1, 10, 5)
            belief_in_thought = st.slider("Wie sehr glaubst du dem Gedanken? (0-100%):", 0, 100, 70)
            
            # Denkfallen-Check für diesen Gedanken
            potential_distortions = st.multiselect(
                "Welche Denkfallen erkennst du?",
                list(cognitive_distortions.keys())
            )
        
        # Alternative Gedanken entwickeln
        st.markdown("**🔄 Alternative Sichtweisen:**")
        alternative_thought = st.text_area("Ausgewogenerer Gedanke:", placeholder="z.B. 'Ich habe mich gut vorbereitet und gebe mein Bestes'")
        
        if st.button("💾 Gedanken-Protokoll speichern") and automatic_thought:
            thought_entry = {
                "timestamp": datetime.datetime.now().isoformat(),
                "situation": thought_situation,
                "automatic_thought": automatic_thought,
                "emotion": thought_emotion,
                "emotion_intensity": emotion_intensity,
                "belief_percentage": belief_in_thought,
                "distortions": potential_distortions,
                "alternative_thought": alternative_thought,
                "id": len(st.session_state.thought_log) + 1
            }
            st.session_state.thought_log.append(thought_entry)
            st.success("🧠 Gedanken-Protokoll gespeichert! Bewusstsein ist der erste Schritt zur Veränderung.")
        
        # Gedanken-Log anzeigen
        if st.session_state.thought_log:
            st.markdown("---")
            st.markdown("**📚 Deine letzten Gedanken-Protokolle:**")
            
            for entry in reversed(st.session_state.thought_log[-5:]):
                timestamp = datetime.datetime.fromisoformat(entry["timestamp"])
                time_str = timestamp.strftime("%d.%m.%Y %H:%M")
                
                st.markdown(f"""
                <div class="diary-entry">
                    <strong>{time_str}</strong> | {entry['emotion']} ({entry['emotion_intensity']}/10)<br>
                    <strong>Situation:</strong> {entry['situation']}<br>
                    <strong>Automatischer Gedanke:</strong> "{entry['automatic_thought']}" (Glaube: {entry['belief_percentage']}%)<br>
                    {f"<strong>Erkannte Denkfallen:</strong> {', '.join(entry['distortions'])}<br>" if entry['distortions'] else ""}
                    {f"<strong>Alternative:</strong> \"{entry['alternative_thought']}\"" if entry['alternative_thought'] else ""}
                </div>
                """, unsafe_allow_html=True)
    
    with tab4:
        st.markdown("### 🎯 Realitäts-Check Station")
        st.markdown("*Überprüfe deine Gedanken auf Wahrheitsgehalt*")
        
        if current_thought:
            st.markdown(f"**🔍 Realitäts-Check für:** '{current_thought}'")
            
            # Strukturierter Realitäts-Check
            reality_checks = {
                "Fakten vs. Meinungen": {
                    "question": "Was davon sind Fakten, was sind Interpretationen?",
                    "prompt": "Trenne objektive Beobachtungen von subjektiven Bewertungen"
                },
                "Worst-Case-Analyse": {
                    "question": "Was ist das Schlimmste, was realistisch passieren könnte?",
                    "prompt": "Ist es wirklich so katastrophal? Würdest du überleben?"
                },
                "Wahrscheinlichkeits-Check": {
                    "question": "Wie wahrscheinlich ist es wirklich (0-100%)?",
                    "prompt": "Basierend auf Erfahrung und Logik, nicht auf Gefühlen"
                },
                "Beweise sammeln": {
                    "question": "Welche Beweise sprechen DAFÜR und DAGEGEN?",
                    "prompt": "Sammle objektive Belege für beide Seiten"
                },
                "Freund-Perspektive": {
                    "question": "Was würdest du einem guten Freund in derselben Lage sagen?",
                    "prompt": "Oft sind wir zu anderen mitfühlender als zu uns selbst"
                },
                "10-Jahre-Test": {
                    "question": "Wird das in 10 Jahren noch wichtig sein?",
                    "prompt": "Langfristige Perspektive hilft bei der Einordnung"
                }
            }
            
            for check_name, check_info in reality_checks.items():
                with st.expander(f"🔍 {check_name}"):
                    st.markdown(f"**{check_info['question']}**")
                    st.caption(check_info['prompt'])
                    
                    response = st.text_area(f"Deine Antwort:", key=f"reality_{check_name}", height=80)
                    
                    if response:
                        if check_name == "Wahrscheinlichkeits-Check":
                            try:
                                percentage = int(''.join(filter(str.isdigit, response)))
                                if percentage < 30:
                                    st.success("💡 Das ist ziemlich unwahrscheinlich! Vielleicht machst du dir unnötig Sorgen?")
                                elif percentage > 70:
                                    st.info("🎯 Das scheint wahrscheinlich. Lass uns Bewältigungsstrategien entwickeln!")
                                else:
                                    st.info("⚖️ Moderates Risiko. Bereite dich vor, aber panik nicht!")
                            except:
                                st.info("💭 Interessante Einschätzung!")
                        else:
                            st.info(f"✅ Notiert: {response[:100]}{'...' if len(response) > 100 else ''}")
            
            # Zusammenfassung nach Realitäts-Check
            if st.button("📊 Realitäts-Check Zusammenfassung"):
                st.markdown(f"""
                <div class="quote-box">
                    <h4>🎯 Dein Realitäts-Check Ergebnis</h4>
                    <p><strong>Ursprünglicher Gedanke:</strong> "{current_thought}"</p>
                    <p><strong>Nach dem Check:</strong> Du hast verschiedene Perspektiven betrachtet und Beweise gesammelt.</p>
                    <p><strong>Neuer Blickwinkel:</strong> Gedanken sind nicht automatisch Wahrheiten. Du kannst sie hinterfragen!</p>
                    <p><strong>Nächster Schritt:</strong> Entwickle einen ausgewogeneren Alternativ-Gedanken.</p>
                </div>
                """, unsafe_allow_html=True)
        
        else:
            st.info("💭 Gib oben im ersten Tab einen Gedanken ein, um den Realitäts-Check zu nutzen!")

def handle_parts_module():
    """Erweiterte innere Anteile Arbeit"""
    
    tab1, tab2, tab3, tab4 = st.tabs(["🎭 Anteil kennenlernen", "💬 Innerer Dialog", "🗺️ Anteile-Mapping", "🤝 Integration"])
    
    with tab1:
        st.markdown("### 🎭 Wer meldet sich heute zu Wort?")
        st.markdown("*Lerne deine inneren Stimmen kennen*")
        
        # Erweiterte Anteile-Galerie
        parts_gallery = {
            "👨‍💼 Der Perfektionist": {
                "description": "Will alles perfect machen",
                "typical_thoughts": ["Das ist nicht gut genug!", "Was werden die anderen denken?", "Ich muss es besser machen!"],
                "positive_function": "Sorgt für Qualität und hohe Standards",
                "shadow_side": "Kann zu Selbstkritik und Prokrastination führen",
                "color": "#e74c3c"
            },
            "😰 Der Ängstliche": {
                "description": "Warnt vor Gefahren",
                "typical_thoughts": ["Was wenn etwas schief geht?", "Das ist zu riskant!", "Ich bin nicht sicher..."],
                "positive_function": "Beschützt vor echten Gefahren",
                "shadow_side": "Kann übervorsichtig machen und Wachstum verhindern",
                "color": "#f39c12"
            },
            "🎨 Der Kreative": {
                "description": "Sucht nach Inspiration und Schönheit",
                "typical_thoughts": ["Das könnte interessant sein!", "Lass uns was Neues ausprobieren!", "Wie wäre es wenn..."],
                "positive_function": "Bringt Freude und Innovation ins Leben",
                "shadow_side": "Kann impulsiv sein und praktische Dinge vernachlässigen",
                "color": "#9b59b6"
            },
            "😡 Der Wütende": {
                "description": "Kämpft für Gerechtigkeit und Grenzen",
                "typical_thoughts": ["Das ist unfair!", "So lasse ich nicht mit mir umgehen!", "Das reicht!"],
                "positive_function": "Setzt Grenzen und kämpft für Werte",
                "shadow_side": "Kann verletzend sein und Beziehungen schädigen",
                "color": "#c0392b"
            },
            "🛡️ Der Beschützer": {
                "description": "Sorgt für Sicherheit und Überleben",
                "typical_thoughts": ["Ich muss aufpassen", "Vertraue niemandem", "Ich schaffe das allein"],
                "positive_function": "Hält uns sicher und unabhängig",
                "shadow_side": "Kann zu Isolation und Misstrauen führen",
                "color": "#34495e"
            },
            "👶 Das innere Kind": {
                "description": "Will Spaß, Liebe und Anerkennung",
                "typical_thoughts": ["Das macht Spaß!", "Lieb mich!", "Ich will das JETZT!"],
                "positive_function": "Bringt Spontaneität und Lebensfreude",
                "shadow_side": "Kann unreife Entscheidungen treffen",
                "color": "#f1c40f"
            },
            "🧙‍♀️ Der Weise": {
                "description": "Sieht das größere Bild",
                "typical_thoughts": ["Das wird auch vorübergehen", "Was kann ich daraus lernen?", "Alles hat seinen Grund"],
                "positive_function": "Gibt Perspektive und tiefere Einsichten",
                "shadow_side": "Kann zu passiv oder abgehoben wirken",
                "color": "#2ecc71"
            },
            "💪 Der Macher": {
                "description": "Will Dinge erledigen und Ziele erreichen",
                "typical_thoughts": ["Lass uns anfangen!", "Das schaffen wir!", "Weitermachen!"],
                "positive_function": "Sorgt für Produktivität und Zielerreichung",
                "shadow_side": "Kann überarbeitung und Burnout verursachen",
                "color": "#3498db"
            }
        }
        
        col1, col2 = st.columns([1, 2])
        
        with col1:
            st.markdown("**👥 Wähle einen Anteil:**")
            selected_part = None
            
            for part_name in parts_gallery.keys():
                if st.button(part_name, key=f"part_select_{part_name}"):
                    selected_part = part_name
                    st.session_state.selected_part = part_name
                    st.session_state.selected_part_data = parts_gallery[part_name]
        
        with col2:
            if hasattr(st.session_state, 'selected_part_data'):
                part_data = st.session_state.selected_part_data
                part_name = st.session_state.selected_part
                
                st.markdown(f"""
                <div style="background: {part_data['color']}; color: white; padding: 2em; border-radius: 20px; margin: 1em 0;">
                    <h3>{part_name}</h3>
                    <p><strong>Rolle:</strong> {part_data['description']}</p>
                    <p><strong>Positive Funktion:</strong> {part_data['positive_function']}</p>
                    <p><strong>Schattenseite:</strong> {part_data['shadow_side']}</p>
                </div>
                """, unsafe_allow_html=True)
                
                st.markdown("**💭 Typische Gedanken dieses Anteils:**")
                for thought in part_data['typical_thoughts']:
                    st.markdown(f"• *\"{thought}\"*")
                
                # Anteil-spezifische Fragen
                st.markdown("---")
                st.markdown(f"**🤔 Fragen an {part_name}:**")
                
                anteil_questions = {
                    "Wann meldest du dich": "In welchen Situationen wirst du besonders aktiv?",
                    "Was brauchst du": "Was brauchst du von mir, um dich sicher zu fühlen?",
                    "Was ist deine Angst": "Wovor hast du am meisten Angst?",
                    "Wie kann ich dir helfen": "Wie kann ich besser mit dir zusammenarbeiten?"
                }
                
                for q_key, question in anteil_questions.items():
                    response = st.text_area(question, key=f"part_q_{q_key}", height=60)
                    if response:
                        st.info(f"💭 Antwort notiert: {response[:80]}{'...' if len(response) > 80 else ''}")
    
    with tab2:
        st.markdown("### 💬 Innerer Dialog führen")
        st.markdown("*Moderiere ein Gespräch zwischen deinen Anteilen*")
        
        if "inner_dialogues" not in st.session_state:
            st.session_state.inner_dialogues = []
        
        # Dialog-Setup
        st.markdown("**🎬 Dialog-Setup:**")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            part_a = st.selectbox("Erster Gesprächspartner:", list(parts_gallery.keys()), key="dialog_part_a")
        
        with col2:
            part_b = st.selectbox("Zweiter Gesprächspartner:", list(parts_gallery.keys()), key="dialog_part_b")
        
        with col3:
            dialog_topic = st.text_input("Gesprächsthema:", placeholder="z.B. 'Jobwechsel', 'Beziehung'")
        
        if part_a != part_b and dialog_topic:
            st.markdown(f"**🎭 Dialog zwischen {part_a} und {part_b} über: '{dialog_topic}'**")
            
            # Dialog-Interface
            current_speaker = st.radio("Wer spricht gerade?", [part_a, part_b])
            
            message = st.text_area(f"Was sagt {current_speaker}?", height=80, placeholder=f"Schreib aus der Perspektive von {current_speaker}...")
            
            if st.button("💬 Nachricht senden") and message:
                dialog_entry = {
                    "timestamp": datetime.datetime.now().isoformat(),
                    "topic": dialog_topic,
                    "speaker": current_speaker,
                    "message": message,
                    "participants": [part_a, part_b]
                }
                st.session_state.inner_dialogues.append(dialog_entry)
                st.success(f"💭 {current_speaker} hat gesprochen!")
            
            # Dialog-Verlauf anzeigen
            if st.session_state.inner_dialogues:
                current_topic_dialogues = [d for d in st.session_state.inner_dialogues if d['topic'] == dialog_topic]
                
                if current_topic_dialogues:
                    st.markdown("---")
                    st.markdown("**💬 Dialog-Verlauf:**")
                    
                    for entry in current_topic_dialogues[-10:]:  # Letzte 10 Nachrichten
                        speaker_color = parts_gallery[entry['speaker']]['color']
                        timestamp = datetime.datetime.fromisoformat(entry['timestamp'])
                        time_str = timestamp.strftime("%H:%M")
                        
                        st.markdown(f"""
                        <div style="background: {speaker_color}; color: white; padding: 1em; border-radius: 15px; margin: 0.5em 0;">
                            <strong>{entry['speaker']} ({time_str}):</strong><br>
                            "{entry['message']}"
                        </div>
                        """, unsafe_allow_html=True)
            
            # Dialog-Moderation
            st.markdown("---")
            st.markdown("**🧘‍♀️ Dialog-Moderation:**")
            
            moderation_tools = {
                "Zusammenfassung": "Was haben beide Anteile gesagt? Wo sind sie sich einig?",
                "Kompromiss finden": "Wie können beide Anteile ihre Bedürfnisse erfüllen?",
                "Gemeinsames Ziel": "Wofür arbeiten beide Anteile letztendlich?",
                "Wertschätzung": "Was kann jeder Anteil vom anderen lernen?"
            }
            
            for tool_name, tool_question in moderation_tools.items():
                if st.button(f"🤝 {tool_name}"):
                    st.info(f"**Moderations-Frage:** {tool_question}")
    
    with tab3:
        st.markdown("### 🗺️ Deine innere Landkarte")
        st.markdown("*Visualisiere dein inneres Team*")
        
        # Anteile-Stärke Assessment
        st.markdown("**📊 Wie stark sind deine Anteile gerade?**")
        
        if "parts_strength" not in st.session_state:
            st.session_state.parts_strength = {}
        
        parts_strength_data = {}
        
        for part_name, part_data in parts_gallery.items():
            strength = st.slider(
                f"{part_name}",
                0, 10, 
                st.session_state.parts_strength.get(part_name, 5),
                help=f"{part_data['description']}"
            )
            parts_strength_data[part_name] = strength
            st.session_state.parts_strength[part_name] = strength
        
        # Visualisierung der Anteile-Stärken
        st.markdown("---")
        st.markdown("**🎨 Deine aktuelle Anteile-Konstellation:**")
        
        # Erstelle eine visuelle Darstellung
        for part_name, strength in parts_strength_data.items():
            part_data = parts_gallery[part_name]
            width_percent = (strength / 10) * 100
            
            st.markdown(f"""
            <div style="margin: 0.5em 0;">
                <div style="display: flex; align-items: center; margin-bottom: 0.2em;">
                    <span style="width: 200px;">{part_name}</span>
                    <span style="margin-left: 1em; font-weight: bold;">{strength}/10</span>
                </div>
                <div style="background: #e0e0e0; height: 20px; border-radius: 10px; overflow: hidden;">
                    <div style="background: {part_data['color']}; height: 100%; width: {width_percent}%; border-radius: 10px; transition: width 0.3s ease;"></div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        # Anteile-Balance Analyse
        st.markdown("---")
        st.markdown("**⚖️ Balance-Analyse:**")
        
        strongest_parts = sorted(parts_strength_data.items(), key=lambda x: x[1], reverse=True)[:3]
        weakest_parts = sorted(parts_strength_data.items(), key=lambda x: x[1])[:3]
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**🔥 Stärkste Anteile:**")
            for part, strength in strongest_parts:
                st.markdown(f"• {part}: {strength}/10")
        
        with col2:
            st.markdown("**💤 Leiseste Anteile:**")
            for part, strength in weakest_parts:
                st.markdown(f"• {part}: {strength}/10")
        
        # Balance-Tipps
        if strongest_parts[0][1] >= 8:
            strong_part = strongest_parts[0][0]
            st.warning(f"⚠️ {strong_part} ist sehr dominant. Achte darauf, dass andere Anteile auch Raum bekommen!")
        
        if weakest_parts[0][1] <= 2:
            weak_part = weakest_parts[0][0]
            st.info(f"💡 {weak_part} ist sehr leise. Vielleicht braucht dieser Anteil mehr Aufmerksamkeit?")
    
    with tab4:
        st.markdown("### 🤝 Anteile-Integration")
        st.markdown("*Arbeite mit deinen Anteilen als Team*")
        
        # Integration-Übungen
        st.markdown("**🎯 Integration-Übungen:**")
        
        integration_exercises = {
            "Anteile-Meeting": {
                "description": "Führe ein imaginäres Team-Meeting mit deinen Anteilen",
                "steps": [
                    "1. Stelle dir vor, alle Anteile sitzen an einem Tisch",
                    "2. Lass jeden Anteil zu Wort kommen",
                    "3. Höre ihre Sorgen und Wünsche",
                    "4. Finde gemeinsame Ziele",
                    "5. Vereinbare, wie ihr zusammenarbeiten wollt"
                ]
            },
            "Anteile-Dankbarkeit": {
                "description": "Würdige die positive Funktion jedes Anteils",
                "steps": [
                    "1. Wähle einen Anteil aus",
                    "2. Erkenne seine positive Absicht",
                    "3. Danke ihm für seinen Schutz/seine Hilfe",
                    "4. Erkläre, wie er dir geholfen hat",
                    "5. Bitte ihn, weiter für dich da zu sein"
                ]
            },
            "Anteile-Verhandlung": {
                "description": "Vermittle zwischen konfligierenden Anteilen",
                "steps": [
                    "1. Identifiziere zwei konflikthafte Anteile",
                    "2. Verstehe die Bedürfnisse beider",
                    "3. Suche nach Gemeinsamkeiten",
                    "4. Entwickle einen Kompromiss",
                    "5. Teste die Lösung in deiner Vorstellung"
                ]
            }
        }
        
        selected_exercise = st.selectbox("Wähle eine Übung:", list(integration_exercises.keys()))
        
        if selected_exercise:
            exercise_info = integration_exercises[selected_exercise]
            
            st.markdown(f"**🎯 {selected_exercise}**")
            st.markdown(f"*{exercise_info['description']}*")
            
            st.markdown("**📋 Schritte:**")
            for step in exercise_info['steps']:
                st.markdown(step)
            
            # Reflexions-Bereich für die Übung
            st.markdown("---")
            st.markdown("**📝 Deine Erfahrung mit der Übung:**")
            
            exercise_reflection = st.text_area(
                "Was hast du bei der Übung erlebt?",
                height=120,
                placeholder="Beschreibe deine Erfahrung, Erkenntnisse oder Schwierigkeiten..."
            )
            
            if exercise_reflection and st.button("💾 Erfahrung speichern"):
                if "integration_experiences" not in st.session_state:
                    st.session_state.integration_experiences = []
                
                experience_entry = {
                    "timestamp": datetime.datetime.now().isoformat(),
                    "exercise": selected_exercise,
                    "reflection": exercise_reflection
                }
                st.session_state.integration_experiences.append(experience_entry)
                st.success("🌟 Integration-Erfahrung gespeichert!")
        
        # Anteile-Weisheiten
        st.markdown("---")
        st.markdown("**💎 Anteile-Weisheiten:**")
        
        wisdom_quotes = [
            "Jeder Anteil in dir hat eine positive Absicht, auch wenn sie manchmal verborgen ist.",
            "Integration bedeutet nicht, Anteile zu eliminieren, sondern sie zu verstehen und zu würdigen.",
            "Deine vermeintlichen 'Schwächen' sind oft Anteile, die Schutz und Anerkennung brauchen.",
            "Ein inneres Team funktioniert wie ein äußeres: Kommunikation ist der Schlüssel.",
            "Selbstmitgefühl bedeutet, mit allen deinen Anteilen freundlich zu sein."
        ]
        
        if st.button("🎲 Zufällige Anteile-Weisheit"):
            wisdom = random.choice(wisdom_quotes)
            st.markdown(f"""
            <div class="quote-box">
                <h4>💎 Weisheit für heute:</h4>
                <p>"{wisdom}"</p>
            </div>
            """, unsafe_allow_html=True)

# Verhaltensanalyse-Modul (NEU!)
def handle_behavior_analysis_module():
    """Professionelle Verhaltensanalyse basierend auf SORKC-Modell"""
    
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["📝 Neue Analyse", "📊 Meine Analysen", "🔍 Analysieren", "📋 Planen", "🎯 Trainieren"])
    
    with tab1:
        st.markdown("### 📝 Verhaltensanalyse erstellen")
        st.markdown("*Verstehe deine Reaktionsmuster mit der professionellen SORKC-Methode*")
        
        # Einleitung zur Verhaltensanalyse
        st.markdown("""
        <div class="info-box">
            <h4>🧠 Was ist eine Verhaltensanalyse?</h4>
            <p>Die Verhaltensanalyse hilft dir dabei, deine automatischen Reaktionen zu verstehen. 
            Sie zeigt den Zusammenhang zwischen Situationen, Gedanken, Gefühlen und Verhalten auf.</p>
            <p><strong>SORKC-Modell:</strong></p>
            <ul>
                <li><strong>S</strong>ituation: Was war der Auslöser?</li>
                <li><strong>O</strong>rganismus: Deine Tagesform und Grundeinstellungen</li>
                <li><strong>R</strong>eaktion: Gedanken, Gefühle, Körper, Verhalten</li>
                <li><strong>K</strong>onsequenzen: Kurzfristige Folgen</li>
                <li><strong>C</strong>onsequences: Langfristige Folgen</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Verhaltensanalyse-Formular
        if "behavior_analyses" not in st.session_state:
            st.session_state.behavior_analyses = []
        
        with st.form("behavior_analysis_form"):                # Visualisierung der Emotion
                st.markdown(f"""
                <div style="background: {data['color']}; color: white; padding: 2em; border-radius: 15px; text-align: center; margin: 1em 0;">
                    <h3>{main_emotion}</h3>
                    <h4>{selected_subcategory}</h4>
                    <p>Intensität: {intensity}/10</p>
                    <div style="background: rgba(255,255,255,0.3); height: 15px; border-radius: 10px; margin: 1em 0;">
                        <div style="background: white; height: 100%; width: {intensity*10}%; border-radius: 10px; transition: width 0.3s ease;"></div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                # Körperliche Sensationen
                st.markdown("**🫀 Wo spürst du das im Körper?**")
                body_sensations = st.multiselect(
                    "Wähle alles was zutrifft:",
                    ["💓 Herz rast", "🫁 Atemprobleme", "😵 Kopfschmerzen", "💪 Muskelverspannungen", 
                     "🤢 Übelkeit", "🥵 Hitzewallungen", "🥶 Kälteschauer", "😵‍💫 Schwindel", 
                     "🤲 Zittern", "💤 Müdigkeit", "🔋 Energielosigkeit", "⚡ Unruhe"]
                )
                
                if st.button("💾 Gefühlszustand speichern", type="primary"):
                    emotion_entry = {
                        "timestamp": datetime.datetime.now().isoformat(),
                        "main_emotion": main_emotion,
                        "subcategory": selected_subcategory,
                        "intensity": intensity,
                        "body_sensations": body_sensations,
                        "id": len(st.session_state.user_mood_history) + 1
                    }
                    st.session_state.user_mood_history.append(emotion_entry)
                    st.success("🎯 Emotion erfasst! Du entwickelst Achtsamkeit für deine Gefühle.")
                    
                    # Sofortige Hilfe anbieten
                    if intensity >= 7:
                        st.warning("⚠️ Das ist ziemlich intensiv! Soll ich dir Regulation-Tools zeigen?")
                        if st.button("🧘 Ja, hilf mir!"):
                            st.session_state.show_regulation_tools = True
    
    with tab2:
        st.markdown("### 🎨 Deine emotionale Landkarte")
        st.markdown("*Visualisiere deine Gefühlswelt*")
        
        # Emotionsmapping-Tool
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown("**🗺️ Wo stehst du emotional gerade?**")
            
            # Interaktive Emotionslandkarte
            emotions_grid = {
                "Hoch aktiviert": {
                    "Positiv": ["🎉 Euphorie", "⚡ Aufregung", "💪 Energie", "🔥 Leidenschaft"],
                    "Negativ": ["😡 Wut", "😰 Panik", "😖 Stress", "🌪️ Chaos"]
                },
                "Niedrig aktiviert": {
                    "Positiv": ["😌 Ruhe", "🕯️ Frieden", "💙 Zufriedenheit", "🌅 Gelassenheit"],
                    "Negativ": ["😔 Trauer", "😑 Leere", "😴 Erschöpfung", "🌧️ Melancholie"]
                }
            }
            
            selected_quadrant = st.selectbox(
                "Wähle deinen emotionalen Bereich:",
                ["Hoch aktiviert + Positiv", "Hoch aktiviert + Negativ", 
                 "Niedrig aktiviert + Positiv", "Niedrig aktiviert + Negativ"]
            )
            
            # Parse selection
            activation_level = "Hoch aktiviert" if "Hoch" in selected_quadrant else "Niedrig aktiviert"
            valence = "Positiv" if "Positiv" in selected_quadrant else "Negativ"
            
            emotions_in_quadrant = emotions_grid[activation_level][valence]
            
            selected_emotion_detailed = st.radio(
                f"Genauer gesagt - {activation_level} & {valence}:",
                emotions_in_quadrant
            )
            
            # Zusätzliche Dimensionen
            st.markdown("**📊 Weitere Dimensionen:**")
            col_a, col_b = st.columns(2)
            
            with col_a:
                clarity = st.slider("🔍 Wie klar ist das Gefühl?", 1, 10, 5)
                duration = st.selectbox("⏱️ Wie lange schon?", 
                                       ["Gerade erst", "Seit heute", "Seit gestern", 
                                        "Diese Woche", "Länger"])
            
            with col_b:
                controllability = st.slider("🎛️ Wie kontrollierbar?", 1, 10, 5)
                social_context = st.selectbox("👥 Sozialer Kontext:", 
                                             ["Allein", "Mit Familie", "Mit Freunden", 
                                              "Bei der Arbeit", "In der Öffentlichkeit"])
        
        with col2:
            # Emotional Weather Report
            st.markdown("**🌤️ Dein emotionales Wetter:**")
            
            weather_mapping = {
                ("Hoch aktiviert", "Positiv"): "☀️ Sonnenschein",
                ("Hoch aktiviert", "Negativ"): "⛈️ Gewitter",
                ("Niedrig aktiviert", "Positiv"): "🌅 Klarer Himmel",
                ("Niedrig aktiviert", "Negativ"): "🌧️ Regenwetter"
            }
            
            current_weather = weather_mapping.get((activation_level, valence), "🌫️ Nebelig")
            
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, #74b9ff, #0984e3); color: white; padding: 2em; border-radius: 20px; text-align: center;">
                <h3>Aktuelles Gefühls-Wetter</h3>
                <div style="font-size: 3em; margin: 0.5em 0;">{current_weather.split()[0]}</div>
                <h4>{current_weather.split(' ', 1)[1]}</h4>
                <p><strong>Emotion:</strong> {selected_emotion_detailed}</p>
                <p><strong>Klarheit:</strong> {clarity}/10</p>
                <p><strong>Kontrolle:</strong> {controllability}/10</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Wettervorhersage (spielerisch)
            if st.button("🔮 Emotionale Wettervorhersage"):
                forecasts = [
                    "Morgen: Leicht bewölkt mit Chancen auf Motivation",
                    "Diese Woche: Wechselhaft, aber mit sonnigen Momenten",
                    "Wochenende: Entspannung mit gelegentlichen Hoffnungsschauern",
                    "Nächste Woche: Stabil mit leichter Besserungstendenz"
                ]
                st.info(random.choice(forecasts))
    
    with tab3:
        st.markdown("### 🧘 Emotions-Regulation Toolbox")
        st.markdown("*Werkzeuge für den Umgang mit schwierigen Gefühlen*")
        
        # Regulation Techniques basierend auf aktueller Emotion
        current_intensity = getattr(st.session_state, 'current_emotion_intensity', 5)
        
        if current_intensity >= 7:
            st.warning("🚨 Hohe Intensität erkannt - Hier sind Sofort-Hilfe Tools:")
            
            tab_crisis, tab_breathing, tab_grounding = st.tabs(["🆘 Krisen-Tools", "🫁 Atemtechniken", "🌍 Grounding"])
            
            with tab_crisis:
                st.markdown("**🆘 Wenn alles zu viel wird:**")
                
                if st.button("❄️ Eiswürfel-Trick"):
                    st.info("""
                    🧊 **Eiswürfel-Methode:**
                    1. Nimm einen Eiswürfel in die Hand
                    2. Spüre die Kälte bewusst
                    3. Konzentriere dich nur auf diese Sensation
                    4. Lass den Eiswürfel schmelzen
                    
                    Das holt dich zurück ins Hier und Jetzt!
                    """)
                
                if st.button("🚿 Kalt-Warm-Technik"):
                    st.info("""
                    🌡️ **Temperatur-Regulation:**
                    1. Kaltes Wasser über die Handgelenke
                    2. Oder ein warmes Bad für die Füße
                    3. Bewusst den Temperaturwechsel spüren
                    
                    Hilft beim Reset des Nervensystems!
                    """)
                
                if st.button("📱 Notfall-Kontakte"):
                    st.error("""
                    ☎️ **Wenn es wirklich schlimm wird:**
                    
                    • **Telefonseelsorge:** 0800 111 0 111 oder 0800 111 0 222
                    • **Nummer gegen Kummer:** 116 123
                    • **Bei akuter Gefahr:** 112
                    
                    Du bist nicht allein! ❤️
                    """)
            
            with tab_breathing:
                st.markdown("**🫁 Atem-Techniken:**")
                
                breathing_technique = st.selectbox(
                    "Wähle eine Technik:",
                    ["4-7-8 Atmung", "Box-Breathing", "478 Beruhigung", "Bauchatmung"]
                )
                
                if breathing_technique == "4-7-8 Atmung":
                    if st.button("▶️ Starten"):
                        st.markdown("""
                        **🌬️ 4-7-8 Atemtechnik:**
                        
                        1. 4 Sekunden **einatmen** 📥
                        2. 7 Sekunden **anhalten** ⏸️
                        3. 8 Sekunden **ausatmen** 📤
                        
                        Wiederhole 4x. Entspannung kommt automatisch!
                        """)
                        
                        # Simulation with progress bars
                        for cycle in range(4):
                            st.write(f"**Zyklus {cycle + 1}/4**")
                            
                            st.write("Einatmen...")
                            progress = st.progress(0)
                            for i in range(40):
                                progress.progress((i + 1) / 40)
                                time.sleep(0.1)
                            
                            st.write("Anhalten...")
                            progress = st.progress(0)
                            for i in range(70):
                                progress.progress((i + 1) / 70)
                                time.sleep(0.1)
                            
                            st.write("Ausatmen...")
                            progress = st.progress(0)
                            for i in range(80):
                                progress.progress((i + 1) / 80)
                                time.sleep(0.1)
                        
                        st.success("🌟 Gut gemacht! Wie fühlst du dich jetzt?")
                
                elif breathing_technique == "Box-Breathing":
                    st.info("""
                    **📦 Box-Breathing (4-4-4-4):**
                    
                    1. 4 Sek einatmen
                    2. 4 Sek halten
                    3. 4 Sek ausatmen  
                    4. 4 Sek halten
                    
                    Stelle dir ein Quadrat vor und folge den Seiten!
                    """)
            
            with tab_grounding:
                st.markdown("**🌍 Grounding-Techniken:**")
                
                if st.button("5-4-3-2-1 Technik"):
                    st.markdown("""
                    **👀 5-4-3-2-1 Sinnes-Grounding:**
                    
                    Benenne laut oder in Gedanken:
                    
                    • **5 Dinge** die du SIEHST 👁️
                    • **4 Dinge** die du FÜHLST (Textur, Temperatur) ✋
                    • **3 Dinge** die du HÖRST 👂  
                    • **2 Dinge** die du RIECHST 👃
                    • **1 Ding** das du SCHMECKST 👅
                    
                    Das holt dich zurück in die Realität!
                    """)
                
                if st.button("🦶 Füße am Boden"):
                    st.info("""
                    **🌍 Erdungs-Übung:**
                    
                    1. Spüre deine Füße am Boden
                    2. Drücke sie bewusst fest auf
                    3. Spüre die Verbindung zur Erde
                    4. Du bist hier, du bist sicher
                    5. Atme in dieses Gefühl hinein
                    """)
        
        else:
            # Reguläre Regulation Tools für moderate Intensität
            st.info("💙 Du scheinst in einem moderaten emotionalen Bereich zu sein. Hier sind Tools zur Regulation:")
            
            tab_mindful, tab_reframe, tab_physical = st.tabs(["🧘 Achtsamkeit", "🔄 Reframing", "💪 Körperlich"])
            
            with tab_mindful:
                st.markdown("**🧘 Achtsamkeits-Übungen:**")
                
                mindful_exercises = {
                    "Body Scan": "Scanne deinen Körper von Kopf bis Fuß. Wo sitzt die Emotion?",
                    "Emotions-Beobachter": "Beobachte deine Emotion wie einen Wettervorgang. Ohne zu urteilen.",
                    "Atem-Anker": "Nutze deinen Atem als Anker. Kehre immer zu ihm zurück.",
                    "Selbst-Mitgefühl": "Sprich mit dir wie mit einem guten Freund in derselben Lage."
                }
                
                for exercise, description in mindful_exercises.items():
                    if st.button(f"🌸 {exercise}"):
                        st.success(f"**{exercise}:** {description}")
            
            with tab_reframe:
                st.markdown("**🔄 Perspective Shifts:**")
                
                current_thought = st.text_input("Was denkst du gerade?", placeholder="z.B. 'Das schaffe ich nie'")
                
                if current_thought:
                    reframes = [
                        f"Alternativer Gedanke: 'Das ist schwer, aber ich kann kleine Schritte gehen.'",
                        f"Freund-Perspektive: 'Was würdest du einem Freund in dieser Lage sagen?'",
                        f"Zukunfts-Ich: 'Was wird dein zukünftiges Ich über diese Situation denken?'",
                        f"Neugierig werden: 'Was kann ich aus dieser Situation lernen?'"
                    ]
                    
                    for reframe in reframes:
                        st.info(reframe)
            
            with tab_physical:
                st.markdown("**💪 Körperliche Regulation:**")
                
                physical_tools = {
                    "Progressive Muskelentspannung": "Spanne 5 Sek an, dann 10 Sek entspannen. Von Kopf bis Fuß.",
                    "Klopftechnik": "Klopfe sanft auf Brust, Arme, Beine. Das beruhigt das Nervensystem.",
                    "Schütteln": "Schüttle 30 Sek den ganzen Körper. Lass Spannungen raus!",
                    "Selbst-Umarmung": "Umarme dich selbst. Du verdienst Mitgefühl."
                }
                
                for tool, instruction in physical_tools.items():
                    if st.button(f"🤲 {tool}"):
                        st.success(f"**{tool}:** {instruction}")
    
    with tab4:
        st.markdown("### 📊 Deine emotionale Reise")
        st.markdown("*Erkenne Muster und Fortschritte*")
        
        if st.session_state.user_mood_history:
            # Emotionstrends
            st.markdown("**📈 Deine letzten Emotionen:**")
            
            recent_moods = st.session_state.user_mood_history[-10:]  # Letzte 10
            
            for mood in reversed(recent_moods):
                timestamp = datetime.datetime.fromisoformat(mood["timestamp"])
                time_str = timestamp.strftime("%d.%m %H:%M")
                
                st.markdown(f"""
                <div class="diary-entry">
                    <strong>{time_str}</strong><br>
                    {mood.get('main_emotion', 'Unbekannt')} → {mood.get('subcategory', 'Unbekannt')}<br>
                    Intensität: {mood.get('intensity', 0)}/10
                    {f"<br>Körperlich: {', '.join(mood.get('body_sensations', []))}" if mood.get('body_sensations') else ""}
                </div>
                """, unsafe_allow_html=True)
            
            # Statistiken
            st.markdown("---")
            st.markdown("**🎯 Emotionale Statistiken:**")
            
            col1, col2, col3 = st.columns(3)
            
            # Häufigste Emotion
            main_emotions = [mood.get('main_emotion', '') for mood in st.session_state.user_mood_history]
            if main_emotions:
                most_common = max(set(main_emotions), key=main_emotions.count)
                col1.metric("Häufigste Emotion", most_common)
            
            # Durchschnittliche Intensität
            intensities = [mood.get('intensity', 0) for mood in st.session_state.user_mood_history]
            if intensities:
                avg_intensity = sum(intensities) / len(intensities)
                col2.metric("⌀ Intensität", f"{avg_intensity:.1f}/10")
            
            # Tracking-Streak
            col3.metric("Einträge gesamt", len(st.session_state.user_mood_history))
            
            # Insights
            st.markdown("---")
            st.markdown("**💡 Deine emotionalen Insights:**")
            
            if avg_intensity > 7:
                st.warning("🔥 Du erlebst oft intensive Emotionen. Das ist normal, aber achte auf Selbstfürsorge!")
            elif avg_intensity < 3:
                st.info("😌 Du bist emotional ziemlich ausgeglichen. Das ist eine Stärke!")
            else:
                st.success("⚖️ Du hast eine gesunde emotionale Balance!")
            
            # Wochentag-Pattern (wenn genug Daten)
            if len(st.session_state.user_mood_history) >= 7:
                st.markdown("**📅 Wann fühlst du dich wie?**")
                weekday_moods = {}
                for mood in st.session_state.user_mood_history:
                    timestamp = datetime.datetime.fromisoformat(mood["timestamp"])
                    weekday = timestamp.strftime("%A")
                    weekday_moods[weekday] = weekday_moods.get(weekday, []) + [mood.get('intensity', 0)]
                
                for weekday, intensities in weekday_moods.items():
                    avg = sum(intensities) / len(intensities)
                    st.write(f"**{weekday}:** ⌀{avg:.1f}/10 ({len(intensities)} Einträge)")
        
        else:
            st.info("📊 Noch keine Emotions-Daten. Beginne mit dem Gefühls-Check, um deine emotionale Reise zu verfolgen!")

def handle_cognitive_module():
    """Erweitertes kognitives Modul mit CBT-Techniken"""
    
    tab1, tab2, tab3, tab4 = st.tabs(["🧠 Gedanken-Detektiv", "🔍 Denkfallen", "💭 Gedanken-Protokoll", "🎯 Realitäts-Check"])
    
    with tab1:
        st.markdown("### 🧠 Was geht dir durch den Kopf?")
        st.markdown("*Werde zum Detektiv deiner eigenen Gedanken*")
        
        # Aktueller Gedanke
        current_thought = st.text_area(
            "Welcher Gedanke beschäftigt dich gerade?",
            placeholder="z.B. 'Ich schaffe das nie', 'Alle denken schlecht über mich', 'Das wird ein Desaster'",
            height=100
        )
        
        if current_thought:
            st.markdown("---")
            
            # Gedanken-Analyse
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**🔬 Automatische Gedanken-Analyse:**")
                
                # Emotion zum Gedanken
                thought_emotion = st.selectbox(
                    "Welche Emotion löst dieser Gedanke aus?",
                    ["😰 Angst", "😢 Traurigkeit", "😡 Wut", "😖 Frustration", 
                     "😔 Hoffnungslosigkeit", "😤 Ärger", "🤔 Verwirrung"]
                )
                
                emotion_intensity = st.slider("Wie stark? (1-10)", 1, 10, 5)
                
                # Kontext
                thought_context = st.text_input(
                    "In welcher Situation kam der Gedanke auf?",
                    placeholder="z.B. 'Bei der Arbeit', 'Zu Hause', 'Mit Freunden'"
                )
            
            with col2:
                st.markdown(f"""
                <div style="background: linear-gradient(135deg, #ff6b6b, #feca57); color: white; padding: 1.5em; border-radius: 15px;">
                    <h4>🎯 Gedanken-Profil</h4>
                    <p><strong>Emotion:</strong> {thought_emotion}</p>
                    <p><strong>Intensität:</strong> {emotion_intensity}/10</p>
                    <p><strong>Kontext:</strong> {thought_context or 'Nicht angegeben'}</p>
                    <div style="background: rgba(255,255,255,0.2); height: 10px; border-radius: 5px; margin: 1em 0;">
                        <div style="background: white; height: 100%; width: {emotion_intensity*10}%; border-radius: 5px;"></div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            
            # Sofortiger Gedanken-Check
            st.markdown("---")
            st.markdown("**🔍 Schnell-Analyse deines Gedankens:**")
            
            quick_checks = {
                "Wahrscheinlichkeit": "Wie wahrscheinlich ist es, dass das wirklich passiert? (1-100%)",
                "Beweise dafür": "Welche Beweise SPRECHEN für diesen Gedanken?",
                "Beweise dagegen": "Welche Beweise SPRECHEN GEGEN diesen Gedanken?",
                "Worst Case": "Was wäre das Schlimmste, was passieren könnte?",
                "Best Case": "Was wäre das Beste, was passieren könnte?",
                "Most Likely": "Was wird realistisch betrachtet wahrscheinlich passieren?"
            }
            
            for check_name, question in quick_checks.items():
                with st.expander(f"🤔 {check_name}"):
                    if check_name == "Wahrscheinlichkeit":
                        probability = st.slider(question, 0, 100, 50)
                        if probability < 30:
                            st.success("💡 Das ist ziemlich unwahrscheinlich! Vielleicht übertreibt dein Gehirn?")
                        elif probability > 70:
                            st.info("🎯 Das scheint wahrscheinlich. Lass uns Lösungen finden!")
                    else:
                        response = st.text_area(question, key=f"check_{check_name}")
                        if response:
                            st.info(f"Notiert: {response}")
    
    with tab2:
        st.markdown("### 🔍 Denkfallen-Detektor")
        st.markdown("*Erkenne die Tricks deines Gehirns*")
        
        # Denkfallen-Katalog
        cognitive_distortions = {
            "🔮 Gedankenlesen": {
                "description": "Du denkst, du weißt was andere denken",
                "example": "'Er findet mich bestimmt langweilig'",
                "counter": "Frag nach oder beobachte objektiv das Verhalten",
                "questions": ["Woher weißt du das?", "Hast du gefragt?", "Gibt es andere Erklärungen?"]
            },
            "🌍 Katastrophisieren": {
                "description": "Du stellst dir das Schlimmste vor",
                "example": "'Wenn ich das vermassel, ist mein Leben ruiniert'",
                "counter": "Was ist realistisch betrachtet wahrscheinlich?",
                "questions": ["Ist das wirklich das Ende der Welt?", "Was würde einem Freund sagen?"]
            },
            "⚫ Schwarz-Weiß-Denken": {
                "description": "Alles ist entweder perfekt oder katastrophal",
                "example": "'Wenn es nicht perfekt ist, ist es wertlos'",
                "counter": "Suche nach Grautönen und Zwischenlösungen",
                "questions": ["Gibt es etwas dazwischen?", "Wo ist die Mitte?"]
            },
            "🔍 Übergeneralisierung": {
                "description": "Ein Ereignis wird zu einem Muster gemacht",
                "example": "'Das passiert mir immer'",
                "counter": "Sammle konkrete Gegenbeispiele",
                "questions": ["Stimmt 'immer' wirklich?", "Wann war es anders?"]
            },
            "🎯 Personalisierung": {
                "description": "Du machst dich für alles verantwortlich",
                "example": "'Es ist meine Schuld, dass er schlechte Laune hat'",
                "counter": "Andere Menschen haben eigene Gründe für ihre Gefühle",
                "questions": ["Welche anderen Faktoren könnten eine Rolle spielen?"]
            },
            "🔮 Wahrsagerei": {
                "description": "Du prophezeist negative Zukunft",
                "example": "'Das wird sicher schief gehen'",
                "counter": "Die Zukunft ist ungewiss und kann positiv überraschen",
                "questions": ["Wie oft lagen deine Vorhersagen falsch?"]
            },
            "📊 Emotional Reasoning": {
                "description": "Gefühle werden als Fakten behandelt",
                "example": "'Ich fühle mich dumm, also bin ich dumm'",
                "counter": "Gefühle sind Signale, keine Wahrheiten",
                "questions": ["Ist das ein Gefühl oder ein Fakt?"]
            },
            "🏷️ Labeling": {
                "description": "Du stempelst dich oder andere ab",
                "example": "'Ich bin ein Versager'",
                "counter": "Menschen sind komplex, nicht nur ein Label",
                "questions": ["Beschreibt das wirklich den ganzen Menschen?"]
            }
        }
        
        # Denkfallen-Test
        if current_thought:
            st.markdown(f"**🔍 Denkfallen-Check für:** '{current_thought}'")
            
            detected_distortions = []
            
            for distortion_name, distortion_info in cognitive_distortions.items():
                if st.button(f"Könnte das {distortion_name} sein?", key=f"distortion_{distortion_name}"):
                    detected_distortions.append(distortion_name)
                    
                    st.markdown(f"""
                    <div style="background: linear-gradient(135deg, #fd79a8, #fdcb6e); color: white; padding: 1.5em; border-radius: 15px; margin: 1em 0;">
                        <h4>🎯 {distortion_name} erkannt!</h4>
                        <p><strong>Was das ist:</strong> {distortion_info['description']}</p>
                        <p><strong>Beispiel:</strong> {distortion_info['example']}</p>
                        <p><strong>Gegenmittel:</strong> {distortion_info['counter']}</p>
                        <p><strong>Hilfreiche Fragen:</strong></p>
                        <ul>{''.join([f'<li>{q}</li>' for q in distortion_info['questions']])}</ul>
                    </div>
                    """, unsafe_allow_html=True)
        
        elseimport streamlit as st
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
if "current_theme" not in st.session_state:
    st.session_state.current_theme = "cozy"

# Erweiterte CSS-Styling mit Animationen und modernem Design
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

/* Floating background elements */
.background-decoration {
    position: fixed;
    pointer-events: none;
    z-index: -1;
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
    position: relative;
    overflow: hidden;
    width: 100%;
}

.stButton > button:hover {
    transform: translateY(-3px);
    box-shadow: var(--shadow-hover);
    background: linear-gradient(45deg, var(--secondary-color), var(--accent-color));
}

.stButton > button:active {
    transform: translateY(-1px);
}

/* Card Styles */
.therapy-card {
    background: var(--bg-card);
    border-radius: 20px;
    padding: 2em;
    margin: 1em 0;
    box-shadow: var(--shadow);
    border: 1px solid rgba(255,255,255,0.5);
    transition: all 0.3s ease;
    position: relative;
    overflow: hidden;
}

.therapy-card:hover {
    transform: translateY(-5px);
    box-shadow: var(--shadow-hover);
}

.therapy-card::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 4px;
    background: var(--bg-primary);
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

.info-box::before {
    content: '';
    position: absolute;
    top: -50%;
    left: -50%;
    width: 200%;
    height: 200%;
    background: linear-gradient(45deg, transparent, rgba(255,255,255,0.1), transparent);
    transform: rotate(45deg);
    animation: shine 3s infinite;
}

@keyframes shine {
    0% { transform: translateX(-100%) translateY(-100%) rotate(45deg); }
    100% { transform: translateX(100%) translateY(100%) rotate(45deg); }
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
    position: relative;
    overflow: hidden;
}

.quote-box::before {
    content: '"';
    font-size: 4em;
    position: absolute;
    top: -10px;
    left: 20px;
    opacity: 0.3;
    font-family: serif;
}

.diary-entry {
    background: linear-gradient(135deg, #f8f9ff, #e8f0ff);
    border-left: 5px solid var(--primary-color);
    padding: 1.5em;
    margin: 1em 0;
    border-radius: 0 15px 15px 0;
    box-shadow: 0 5px 15px rgba(0,0,0,0.1);
    transition: transform 0.2s ease;
}

.diary-entry:hover {
    transform: translateX(5px);
}

.module-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 1.5em;
    margin: 2em 0;
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
    position: relative;
    overflow: hidden;
}

.progress-bar::after {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: linear-gradient(90deg, transparent, rgba(255,255,255,0.4), transparent);
    animation: progress-shine 2s infinite;
}

@keyframes progress-shine {
    0% { transform: translateX(-100%); }
    100% { transform: translateX(100%); }
}

.mood-selector {
    display: flex;
    justify-content: space-around;
    flex-wrap: wrap;
    gap: 1em;
    margin: 1.5em 0;
}

.mood-item {
    background: var(--bg-card);
    border-radius: 15px;
    padding: 1em;
    text-align: center;
    cursor: pointer;
    transition: all 0.3s ease;
    border: 2px solid transparent;
    min-width: 100px;
}

.mood-item:hover {
    transform: scale(1.1);
    border-color: var(--primary-color);
    box-shadow: 0 5px 20px rgba(102, 126, 234, 0.3);
}

.mood-item.selected {
    border-color: var(--primary-color);
    background: linear-gradient(135deg, rgba(102, 126, 234, 0.1), rgba(118, 75, 162, 0.1));
}

.floating-hearts {
    position: fixed;
    pointer-events: none;
    z-index: 1000;
}

.heart {
    position: absolute;
    color: var(--accent-color);
    font-size: 1.5em;
    animation: float-heart 3s ease-out forwards;
}

@keyframes float-heart {
    0% {
        opacity: 1;
        transform: translateY(0) scale(1);
    }
    100% {
        opacity: 0;
        transform: translateY(-100px) scale(0.5);
    }
}

/* Responsive Design */
@media (max-width: 768px) {
    .main-title {
        font-size: 2.5em;
    }
    
    .main-container {
        margin: 0.5em;
        padding: 1.5em;
    }
    
    .module-grid {
        grid-template-columns: 1fr;
    }
}

/* Custom Scrollbar */
::-webkit-scrollbar {
    width: 8px;
}

::-webkit-scrollbar-track {
    background: rgba(255, 255, 255, 0.1);
    border-radius: 10px;
}

::-webkit-scrollbar-thumb {
    background: var(--bg-primary);
    border-radius: 10px;
}

::-webkit-scrollbar-thumb:hover {
    background: var(--secondary-color);
}

/* Loading Animation */
.loading-spinner {
    display: inline-block;
    width: 40px;
    height: 40px;
    border: 4px solid rgba(255, 255, 255, 0.3);
    border-radius: 50%;
    border-top-color: white;
    animation: spin 1s ease-in-out infinite;
}

@keyframes spin {
    to { transform: rotate(360deg); }
}

/* Glassmorphism effects */
.glass-card {
    background: rgba(255, 255, 255, 0.1);
    backdrop-filter: blur(20px);
    border: 1px solid rgba(255, 255, 255, 0.2);
    border-radius: 20px;
    padding: 2em;
    margin: 1em 0;
}

/* Theme colors for different moods */
.theme-cozy { --accent: #ffeaa7; }
.theme-energetic { --accent: #74b9ff; }
.theme-calm { --accent: #81ecec; }
.theme-creative { --accent: #fd79a8; }

</style>
""", unsafe_allow_html=True)

# Background Decorations
st.markdown("""
<div class="background-decoration">
    <div class="floating-shape" style="width: 100px; height: 100px; top: 10%; left: 5%; animation-delay: 0s;"></div>
    <div class="floating-shape" style="width: 60px; height: 60px; top: 20%; right: 10%; animation-delay: 1s;"></div>
    <div class="floating-shape" style="width: 80px; height: 80px; bottom: 30%; left: 10%; animation-delay: 2s;"></div>
    <div class="floating-shape" style="width: 120px; height: 120px; bottom: 10%; right: 5%; animation-delay: 3s;"></div>
</div>
""", unsafe_allow_html=True)

# Titel & Untertitel mit verbessertem Design
st.markdown('<div class="main-title gradient-text">🎧 Traumatisierender Taschen-Therapeut</div>', unsafe_allow_html=True)

# Hauptcontainer
st.markdown('<div class="main-container">', unsafe_allow_html=True)

# Hauptlogik
if st.session_state.insurance is None:
    # Verbesserte Versicherungsauswahl
    st.markdown('<div class="subtitle">🏥 Bitte wähle deine Krankenversicherung</div>', unsafe_allow_html=True)
    st.markdown("*Diese lebenswichtige Entscheidung bestimmt die Qualität deiner digitalen Seelenhygiene*")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        # GKV Option
        st.markdown("""
        <div class="therapy-card" style="text-align: center; margin-bottom: 1em;">
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
        
        # PKV Option
        st.markdown("""
        <div class="therapy-card" style="text-align: center;">
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

elif not st.session_state.loading_done:
    # Erweiterte Ladeanimation
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
        <div class="loading-spinner"></div>
        <p style="margin-top: 1em; font-style: italic;">
            "Der beste Zeitpunkt, einen Therapeuten zu pflanzen, war vor 20 Jahren.<br>
            Der zweitbeste Zeitpunkt ist jetzt." - Konfuzius (wahrscheinlich)
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("🎟️ 🚪 Wartezimmer B2.01 betreten", key="enter_therapy"):
        st.session_state.loading_done = True
        rerun_app()

else:
    # Hauptbereich mit erweitertem Design
    status = st.session_state.insurance
    ticket = f"{status}-{random.randint(100000, 999999)}"
    
    # Personalisierte Begrüßung
    current_hour = datetime.datetime.now().hour
    if current_hour < 12:
        greeting = "Guten Morgen"
        mood_comment = "Schön, dass du heute schon hier bist. Das Leben wartet nicht!"
    elif current_hour < 18:
        greeting = "Guten Tag"
        mood_comment = "Mittags-Depression oder Nachmittags-Krise?"
    else:
        greeting = "Guten Abend"
        mood_comment = "Spätschicht der Selbstreflexion, wie ich sehe."
    
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
            
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 1em; margin: 1.5em 0;">
                <div style="text-align: center; padding: 1em; background: rgba(255,255,255,0.5); border-radius: 10px;">
                    <div style="font-size: 2em;">⏰</div>
                    <strong>Wartezeit</strong><br>
                    6-18 Monate<br>
                    <small>(perfekt für Gedulds-Training)</small>
                </div>
                <div style="text-align: center; padding: 1em; background: rgba(255,255,255,0.5); border-radius: 10px;">
                    <div style="font-size: 2em;">🎭</div>
                    <strong>Leistungen</strong><br>
                    Basis-Verzweiflung<br>
                    <small>(aber dafür authentisch)</small>
                </div>
                <div style="text-align: center; padding: 1em; background: rgba(255,255,255,0.5); border-radius: 10px;">
                    <div style="font-size: 2em;">🎁</div>
                    <strong>Bonus</strong><br>
                    Wartezimmer-Zen<br>
                    <small>(Achtsamkeit durch Langeweile)</small>
                </div>
            </div>
            
            <p style="margin-top: 1.5em; font-style: italic; text-align: center;">
                💡 <strong>Geheimtipp:</strong> {mood_comment}<br>
                Wenn du beim Kartenscannen weinst, zählt das als therapeutisches Vorgespräch!
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
            
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 1em; margin: 1.5em 0;">
                <div style="text-align: center; padding: 1em; background: linear-gradient(135deg, #ffd700, #ffed4e); border-radius: 10px; color: #333;">
                    <div style="font-size: 2em;">⚡</div>
                    <strong>Express-Service</strong><br>
                    24-48h Wartezeit<br>
                    <small>(Krise wartet nicht)</small>
                </div>
                <div style="text-align: center; padding: 1em; background: linear-gradient(135deg, #ff9a9e, #fecfef); border-radius: 10px;">
                    <div style="font-size: 2em;">🛋️</div>
                    <strong>Luxus-Equipment</strong><br>
                    Designer-Sitzsäcke<br>
                    <small>(weinen in Stil)</small>
                </div>
                <div style="text-align: center; padding: 1em; background: linear-gradient(135deg, #a8edea, #fed6e3); border-radius: 10px;">
                    <div style="font-size: 2em;">📞</div>
                    <strong>24/7 Hotline</strong><br>
                    Notfall-Support<br>
                    <small>(auch für kleine Krisen)</small>
                </div>
                <div style="text-align: center; padding: 1em; background: linear-gradient(135deg, #ffecd2, #fcb69f); border-radius: 10px;">
                    <div style="font-size: 2em;">🥇</div>
                    <strong>Premium-Extras</strong><br>
                    Vergoldete Klangschale<br>
                    <small>(Ego-Streicheln inklusive)</small>
                </div>
            </div>
            
            <p style="margin-top: 1.5em; font-style: italic; text-align: center;">
                💡 <strong>VIP-Info:</strong> {mood_comment}<br>
                Dein Therapeut hat bereits dein LinkedIn-Profil studiert und einen personalisierten Behandlungsplan erstellt!
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    # Erweiterte Therapie-Fortschritts-Anzeige
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
    
    # Erweiterte Module-Auswahl mit Grid-Layout
    st.markdown("### 🎯 Deine heutige Therapie-Session")
    st.markdown("*Wähle dein therapeutisches Abenteuer – jedes Modul wurde von Experten entwickelt (oder zumindest von jemandem, der mal Psychologie-YouTube geschaut hat)*")
    
    # Module-Grid mit verbessertem Design
    modules_data = {
        "📔 Tagebuch öffnen": {
            "description": "Digitales Seelen-Archiv",
            "subtitle": "Verwandle deine Gedanken in lesbare Verzweiflung",
            "color": "linear-gradient(135deg, #667eea, #764ba2)",
            "benefits": ["Strukturiertes Jammern", "Mood-Tracking", "Erinnerungs-Archiv"]
        },
        "😅 Galgenhumor-Modus": {
            "description": "Therapie durch Sarkasmus",
            "subtitle": "Lachen über das Unlachbare",
            "color": "linear-gradient(135deg, #f093fb, #f5576c)",
            "benefits": ["Sarkasmus-Generator", "Ironie-Therapie", "Realitäts-Humor"]
        },
        "🎮 Therapie-Minispiel": {
            "description": "Gamification der Existenzkrise",
            "subtitle": "Level up deine mentale Gesundheit",
            "color": "linear-gradient(135deg, #4facfe, #00f2fe)",
            "benefits": ["Belohnungssystem", "Achievement-Unlock", "Progress-Tracking"]
        },
        "💙 Etwas fühlen": {
            "description": "Emotionsregulation ohne Regulation",
            "subtitle": "Gefühls-Chaos professionell sortieren",
            "color": "linear-gradient(135deg, #a8edea, #fed6e3)",
            "benefits": ["Gefühls-Scanner", "Intensitäts-Messung", "Emotions-Mapping"]
        },
        "🧠 Etwas verstehen": {
            "description": "Kognitive Verhaltenstherapie für Dummies",
            "subtitle": "Gedanken-Detektiv werden",
            "color": "linear-gradient(135deg, #ffecd2, #fcb69f)",
            "benefits": ["Denkfallen-Finder", "Realitäts-Check", "Gedanken-Korrektur"]
        },
        "🎭 Innere Anteile besuchen": {
            "description": "Systemische Familientherapie im Kopf",
            "subtitle": "Meet & Greet mit deiner inneren WG",
            "color": "linear-gradient(135deg, #fa709a, #fee140)",
            "benefits": ["Persönlichkeits-Chat", "Innerer Dialog", "Anteil-Mediation"]
        }
    }
    
    # Erstelle 2x3 Grid für Module
    row1_cols = st.columns(3)
    row2_cols = st.columns(3)
    all_cols = row1_cols + row2_cols
    
    module_names = list(modules_data.keys())
    
    for i, (col, module_name) in enumerate(zip(all_cols, module_names)):
        module_info = modules_data[module_name]
        
        with col:
            # Module Card mit hover-Effekt
            card_html = f"""
            <div class="module-card" style="background: {module_info['color']}; color: white; min-height: 280px;">
                <div class="module-icon">{module_name.split()[0]}</div>
                <h4 style="margin: 0.5em 0; font-size: 1.2em;">{module_name.split(' ', 1)[1]}</h4>
                <p style="font-size: 0.9em; opacity: 0.9; margin: 0.5em 0;">{module_info['subtitle']}</p>
                <div style="margin: 1em 0; font-size: 0.8em;">
                    {'<br>'.join([f"• {benefit}" for benefit in module_info['benefits']])}
                </div>
            </div>
            """
            st.markdown(card_html, unsafe_allow_html=True)
            
            if st.button(f"Starten", key=f"start_{i}", help=f"{module_info['description']}"):
                handle_module_selection(module_name, module_info)

def handle_module_selection(module_name: str, module_info: dict):
    """Behandelt die Auswahl eines Moduls mit verbessertem Design"""
    
    # Module Header
    st.markdown(f"""
    <div class="therapy-card" style="background: {module_info['color']}; color: white; text-align: center; margin: 2em 0;">
        <div style="font-size: 4em; margin-bottom: 0.5em;">{module_name.split()[0]}</div>
        <h2 style="margin: 0;">{module_name.split(' ', 1)[1]}</h2>
        <p style="opacity: 0.9; font-size: 1.1em;">{module_info['subtitle']}</p>
    </div>
    """, unsafe_allow_html=True)
    
    if "Tagebuch" in module_name:
        handle_diary_module()
    elif "Galgenhumor" in module_name:
        handle_humor_module()
    elif "Minispiel" in module_name:
        handle_game_module()
    elif "fühlen" in module_name:
        handle_emotions_module()
    elif "verstehen" in module_name:
        handle_cognitive_module()
    elif "Anteile" in module_name:
        handle_parts_module()

def handle_diary_module():
    """Erweiteres Tagebuch-Modul"""
    
    tab1, tab2, tab3, tab4 = st.tabs(["✍️ Neuer Eintrag", "📚 Mein Archiv", "📊 Stimmungs-Analytics", "🎯 Insights"])
    
    with tab1:
        st.markdown("### 📝 Was bewegt dich heute?")
        
        # Erweiterte Stimmungsauswahl mit Visualisierung
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
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("💾 Eintrag speichern", type="primary"):
                if entry_text:
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
                    
                    # Success Animation
                    st.success("🎉 Eintrag gespeichert! Deine Gedanken sind jetzt digital unsterblich.")
                    st.balloons()
                    
                    # Statistik Update
                    total_words = sum(entry.get('word_count', 0) for entry in st.session_state.diary_entries)
                    st.info(f"📊 Das waren {len(entry_text.split())} Wörter. Insgesamt hast du schon {total_words} Wörter deiner Seele anvertraut!")
                    
        with col2:
            if st.button("🎲 Zufälliger Prompt"):
                random_prompts = [
                    "Was würdest du deinem 5-Jahre-jüngeren Ich sagen?",
                    "Beschreibe deinen Tag in drei Worten.",
                    "Was ist das Absurdeste, was dir heute passiert ist?",
                    "Wofür bist du heute dankbar (auch wenns schwerfällt)?",
                    "Was brauchst du gerade am meisten?",
                    "Wenn deine Stimmung ein Wetter wäre, welches wäre es?",
                    "Was hast du heute gelernt über dich oder das Leben?"
                ]
                prompt = random.choice(random_prompts)
                st.info(f"💭 **Schreib-Impuls:** {prompt}")
        
        with col3:
            if st.button("🧘 Achtsamkeits-Moment"):
                st.markdown("""
                <div class="quote-box">
                    <h4>🌸 Kurzer Achtsamkeits-Check:</h4>
                    <p>• Wie fühlt sich dein Körper gerade an?<br>
                    • Was nimmst du um dich herum wahr?<br>
                    • Wie ist dein Atem?<br>
                    • Was ist in diesem Moment okay?</p>
                </div>
                """, unsafe_allow_html=True)
    
    with tab2:
        st.markdown("### 📚 Dein persönliches Seelen-Archiv")
        
        if st.session_state.diary_entries:
            # Filter Optionen
            col1, col2, col3 = st.columns(3)
            
            with col1:
                # Filter nach Kategorie
                all_categories = list(set([entry.get('category', 'Unbekannt') for entry in st.session_state.diary_entries]))
                selected_categories = st.multiselect("Nach Kategorie filtern:", all_categories, default=all_categories)
            
            with col2:
                # Filter nach Tags
                all_tags = list(set([tag for entry in st.session_state.diary_entries for tag in entry.get('tags', [])]))
                if all_tags:
                    selected_tags = st.multiselect("Nach Tags filtern:", all_tags)
                else:
                    selected_tags = []
            
            with col3:
                # Sortierung
                sort_option = st.selectbox("Sortieren nach:", ["Neueste zuerst", "Älteste zuerst", "Nach Stimmung"])
            
            # Gefilterte Einträge
            filtered_entries = [
                entry for entry in st.session_state.diary_entries
                if entry.get('category', 'Unbekannt') in selected_categories
                and (not selected_tags or any(tag in entry.get('tags', []) for tag in selected_tags))
            ]
            
            # Sortierung anwenden
            if sort_option == "Neueste zuerst":
                filtered_entries = sorted(filtered_entries, key=lambda x: x['date'], reverse=True)
            elif sort_option == "Älteste zuerst":
                filtered_entries = sorted(filtered_entries, key=lambda x: x['date'])
            
            st.markdown(f"**{len(filtered_entries)} Einträge gefunden**")
            
            # Einträge anzeigen
            for i, entry in enumerate(filtered_entries[:10]):  # Nur die ersten 10 anzeigen
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
    
    with tab4:
        st.markdown("### 🔍 Persönliche Insights")
        
        if len(st.session_state.diary_entries) >= 3:
            # Generiere Insights basierend auf Einträgen
            recent_entries = st.session_state.diary_entries[-5:]
            
            st.markdown("**🎯 Deine letzten Patterns:**")
            
            # Häufigste Kategorien
            recent_categories = [entry.get('category', 'Unbekannt') for entry in recent_entries]
            most_common_category = max(set(recent_categories), key=recent_categories.count) if recent_categories else None
            
            if most_common_category:
                st.info(f"🔍 **Aktueller Fokus:** Du beschäftigst dich oft mit '{most_common_category}'. Das zeigt, was gerade wichtig für dich ist.")
            
            # Schreibhäufigkeit
            if len(st.session_state.diary_entries) >= 7:
                st.success("🔥 **Schreib-Streak:** Du bist dabei, eine richtige Routine zu entwickeln! Das ist großartig für deine Selbstreflexion.")
            
            # Wort-Trends
            recent_word_counts = [entry.get('word_count', 0) for entry in recent_entries]
            if recent_word_counts:
                avg_recent = sum(recent_word_counts) / len(recent_word_counts)
                if avg_recent > 50:
                    st.info("✍️ **Detailfreude:** Du schreibst ausführlich - das zeigt tiefe Reflexion!")
                else:
                    st.info("📝 **Prägnant:** Kurz und knackig - manchmal sagt weniger mehr!")
            
            # Motivierende Nachricht
            encouragements = [
                "Du machst das großartig! Jeder Eintrag ist ein Schritt zur Selbsterkenntnis.",
                "Deine Ehrlichkeit dir selbst gegenüber ist beeindruckend.",
                "Das regelmäßige Schreiben zeigt, dass du dir selbst wichtig bist.",
                "Deine Reflexionsfähigkeit entwickelt sich mit jedem Eintrag weiter.",
                "Du baust dir hier ein wertvolles Archiv deiner persönlichen Entwicklung auf."
            ]
            
            st.markdown(f"""
            <div class="quote-box">
                <h4>💫 Message für dich:</h4>
                <p>{random.choice(encouragements)}</p>
            </div>
            """, unsafe_allow_html=True)
        
        else:
            st.markdown("""
            <div style="text-align: center; padding: 2em;">
                <h3>🌱 Deine Insight-Reise beginnt hier</h3>
                <p>Schreib mindestens 3 Einträge, um personalisierte Einblicke zu erhalten!</p>
                <p>Jeder Eintrag hilft der App, deine Muster und Entwicklung besser zu verstehen.</p>
            </div>
            """, unsafe_allow_html=True)

def handle_humor_module():
    """Erweiterter Galgenhumor-Modus mit mehr Interaktivität"""
    
    tab1, tab2, tab3 = st.tabs(["🎲 Zufallsweisheiten", "🎭 Interaktiver Humor", "📝 Humor-Tagebuch"])
    
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
            "🤔 Philosophisch absurd": [
                "Wenn ein Therapeut in der Therapie weint und niemand da ist, ist es dann trotzdem therapeutisch?",
                "Die Definition von Wahnsinn ist, immer wieder dasselbe zu tun und andere Ergebnisse zu erwarten. Also ist normalität auch nicht besser.",
                "Existenzangst ist nur ein Zeichen dafür, dass du existierst. Herzlichen Glückwunsch!",
                "In einer verrückten Welt ist Anpassung das eigentliche Problem.",
                "Deine Neurosen sind Features, keine Bugs. Du bist eine sehr interessante Beta-Version.",
                "Das Leben ist absurd. Aber hey, wenigstens ist es konsistent absurd."
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
                <div class="quote-box" style="background: linear-gradient(135deg, #667eea, #764ba2);">
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
            
            # Tägliches Spezial
            today = datetime.datetime.now().strftime("%Y-%m-%d")
            if st.button("📅 Weisheit des Tages"):
                daily_specials = [
                    "Montag: 'Wer hat entschieden, dass Montage existieren müssen?'",
                    "Dienstag: 'Dienstag ist der Beweis, dass auch die Woche ein Trauma hat.'",
                    "Mittwoch: 'Bergfest! Du hast die Hälfte der Woche überlebt!'",
                    "Donnerstag: 'Donnerstag - fast Freitag, aber noch nicht Freitag. Ein metaphysisches Dilemma.'",
                    "Freitag: 'TGIF - Thank God It's Finally... oh wait, morgen ist Samstag. Arbeitsfreie Zeit ist auch stressig.'",
                    "Samstag: 'Samstag: Der Tag, an dem du merkst, dass Freizeit auch Verantwortung ist.'",
                    "Sonntag: 'Sunday Scaries sind real. Morgen ist wieder Montag. Der Kreislauf beginnt von vorn.'"
                ]
                
                weekday = datetime.datetime.now().weekday()
                daily_quote = daily_specials[weekday]
                
                st.success(f"🌅 **{daily_quote}**")
    
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
                    f"Pro-Tipp: Stell dir vor, dein Chef ist ein NPCs in deinem Lebensspiel. Macht ihn weniger real, aber nicht weniger nervig."
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
                ],
                "default": [
                    f"'{situation}' - Klingt herausfordernd! Aber hey, du bist hier und beschreibst es. Das ist schon was.",
                    f"'{situation}' - Manchmal ist das Leben wie ein schlechter Film, nur dass du nicht gehen kannst.",
                    f"'{situation}' - Das klingt nach einem typischen Menschlichkeits-Problem. Du bist sehr menschlich!"
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
                category_responses = responses["default"]
            
            response = random.choice(category_responses)
            
            st.markdown(f"""
            <div class="quote-box">
                <h4>🎯 Maßgeschneiderter Kommentar:</h4>
                <p style="font-size: 1.1em;">"{response}"</p>
                <small>— Dein persönlicher Sarkasmus-Assistent</small>
            </div>
            """, unsafe_allow_html=True)
        
        # Humor-Tools
        st.markdown("---")
        st.markdown("### 🛠️ Humor-Werkzeugkasten")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("🔄 Perspektiv-Wechsel"):
                perspectives = [
                    "Stell dir vor, ein Alien würde deine Situation beobachten. Was würde es denken?",
                    "In 10 Jahren ist das hier eine lustige Anekdote. Wahrscheinlich.",
                    "Irgendwo auf der Welt hat jemand das gleiche Problem. Ihr seid Problem-Twins!",
                    "Das ist Material für deine zukünftige Stand-up-Comedy-Karriere.",
                    "Mindestens bist du nicht in einem Reality-TV-Format gefangen."
                ]
                st.info(random.choice(perspectives))
        
        with col2:
            if st.button("🎪 Absurditäts-Check"):
                absurd_facts = [
                    "Fakt: Wombats haben würfelförmigen Kot. Dein Problem ist also nicht das Absurdeste heute.",
                    "Irgendwo macht jemand gerade Musik mit Gemüse. Deine Sorgen sind relativ normal.",
                    "Es gibt Menschen, die professionell Pandas zum Schlafen bringen. Dein Job ist ok.",
                    "Jemand hat mal versucht, Ketchup als Medizin zu verkaufen. Deine Ideen sind nicht die schlechtesten.",
                    "Es gibt ein Wort für die Angst vor Clowns, aber keins für Montagsmorgen. Prioritäten..."
                ]
                st.success(random.choice(absurd_facts))
        
        with col3:
            if st.button("💫 Instant-Aufmunterung"):
                uplifting = [
                    "Du atmest noch. Das ist statistisch gesehen ein sehr gutes Zeichen!",
                    "Du hast heute schon mehr geschafft als ein Koala. Die schlafen 22h am Tag.",
                    "Deine Probleme zeigen, dass du ein Leben hast. Glückwunsch zur Existenz!",
                    "Du bist der Hauptcharakter in deiner Geschichte. Auch wenn's gerade ein Drama ist.",
                    "Du hast bis jetzt 100% deiner schlechten Tage überlebt. Beeindruckende Bilanz!"
                ]
                st.balloons()
                st.success(random.choice(uplifting))
    
    with tab3:
        st.markdown("### 📝 Dein persönliches Humor-Archiv")
        
        if "humor_entries" not in st.session_state:
            st.session_state.humor_entries = []
        
        # Neuen Humor-Moment hinzufügen
        st.markdown("**Was war heute absurd, ironisch oder einfach zum Lachen?**")
        
        humor_text = st.text_area(
            "Beschreib die Situation:",
            placeholder="z.B. 'Bin ausgerutscht, aber elegant gelandet' oder 'Chef hat sich selbst widersprochen - in einem Satz'"
        )
        
        humor_rating = st.slider("Wie lustig war es? (1-10)", 1, 10, 5)
        
        if st.button("😄 Humor-Moment speichern") and humor_text:
            humor_entry = {
                "date": datetime.datetime.now().isoformat(),
                "text": humor_text,
                "rating": humor_rating,
                "id": len(st.session_state.humor_entries) + 1
            }
            st.session_state.humor_entries.append(humor_entry)
            st.success("😂 Humor-Moment gespeichert! Lachen ist die beste Medizin (angeblich).")
        
        # Humor-Archiv anzeigen
        if st.session_state.humor_entries:
            st.markdown("---")
            st.markdown("**🎭 Deine gesammelten Lacher:**")
            
            for entry in reversed(st.session_state.humor_entries[-5:]):
                date_str = datetime.datetime.fromisoformat(entry["date"]).strftime("%d.%m.%Y")
                stars = "⭐" * entry["rating"]
                
                st.markdown(f"""
                <div class="diary-entry">
                    <strong>{date_str}</strong> | {stars}<br>
                    <em>"{entry['text']}"</em>
                </div>
                """, unsafe_allow_html=True)

def handle_game_module():
    """Erweiterte Gamification mit mehr Spielelementen"""
    
    tab1, tab2, tab3, tab4 = st.tabs(["🎮 Daily Challenges", "🏆 Achievements", "📊 Stats & Level", "🎯 Custom Goals"])
    
    with tab1:
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
        
        # Tägliche Challenges (verschiedene Schwierigkeitsgrade)
        st.markdown("### 🌟 Heute verfügbare Missionen")
        
        challenges = {
            "Anfänger": [
                {"text": "Steh auf, ohne den Wecker zu verfluchen", "points": 10, "icon": "🌅"},
                {"text": "Trink ein Glas Wasser (nicht nur Kaffee)", "points": 10, "icon": "💧"},
                {"text": "Mach das Bett (oder tu wenigstens so)", "points": 15, "icon": "🛏️"},
                {"text": "Sag 'Danke' zu jemandem", "points": 15, "icon": "🙏"}
            ],
            "Fortgeschritten": [
                {"text": "Geh 15 Minuten spazieren (auch im Haus zählt)", "points": 25, "icon": "🚶"},
                {"text": "Ruf einen Freund an (nicht für eine Krise)", "points": 30, "icon": "📞"},
                {"text": "Mach etwas, was du aufgeschoben hast", "points": 35, "icon": "✅"},
                {"text": "Meditiere 5 Minuten (oder starr 5 Min an die Wand)", "points": 25, "icon": "🧘"}
            ],
            "Experte": [
                {"text": "Geh vor 23 Uhr ins Bett", "points": 40, "icon": "🌙"},
                {"text": "Koche etwas Gesundes (Instant-Nudeln zählen nicht)", "points": 45, "icon": "👨‍🍳"},
                {"text": "Mach Sport (auch 5 Liegestütze zählen)", "points": 50, "icon": "💪"},
                {"text": "Schreib jemandem eine nette Nachricht", "points": 35, "icon": "💌"}
            ],
            "Legendary": [
                {"text": "Einen ganzen Tag ohne Social Media", "points": 100, "icon": "📱❌"},
                {"text": "Löse ein Problem, das du Wochen aufgeschoben hast", "points": 80, "icon": "🎯"},
                {"text": "Plane aktiv etwas Schönes für nächste Woche", "points": 60, "icon": "📅"},
                {"text": "Hilf jemandem ohne dass er danach fragt", "points": 70, "icon": "🤝"}
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
                        
                        # Achievement Check
                        if st.session_state.game_score >= 500 and "high_scorer" not in st.session_state:
                            st.session_state.high_scorer = True
                            st.success("🏆 ACHIEVEMENT UNLOCKED: High Scorer!")
                    
                    if st.button("❌ Nicht heute", key=f"{difficulty}_fail"):
                        encouraging_messages = [
                            "Auch okay! Morgen ist ein neuer Tag zum Versagen... äh, Versuchen!",
                            "Kein Problem! Selbsterkenntnis ist auch eine Art von Fortschritt.",
                            "Ehrlichkeit ist die beste Politik. Auch gegenüber dir selbst!",
                            "Das Leben ist kein Sprint. Manchmal ist es ein sehr langsamer Spaziergang.",
                            "Du hast immerhin die Ehrlichkeit aufgebracht, 'Nein' zu sagen!"
                        ]
                        st.info(random.choice(encouraging_messages))
    
    with tab2:
        st.markdown("### 🏆 Achievement-System")
        st.markdown("*Sammle Abzeichen für deine Lebens-Skills!*")
        
        # Initialize achievements if not present
        if "achievements" not in st.session_state:
            st.session_state.achievements = set()
        
        achievements_list = {
            "first_points": {"name": "First Steps", "desc": "Erste Punkte gesammelt", "icon": "🌱", "requirement": "score >= 10"},
            "consistent": {"name": "Routine Builder", "desc": "5 Challenges geschafft", "icon": "🔄", "requirement": "score >= 50"},
            "high_scorer": {"name": "High Achiever", "desc": "500 Punkte erreicht", "icon": "⭐", "requirement": "score >= 500"},
            "level_5": {"name": "Veteran", "desc": "Level 5 erreicht", "icon": "🎖️", "requirement": "score >= 400"},
            "diary_writer": {"name": "Soul Writer", "desc": "10 Tagebuch-Einträge", "icon": "📚", "requirement": "diary >= 10"},
            "mood_tracker": {"name": "Emotion Explorer", "desc": "Verschiedene Stimmungen erfasst", "icon": "🎭", "requirement": "moods >= 5"}
        }
        
        # Check and award achievements
        current_score = st.session_state.game_score
        diary_count = len(st.session_state.diary_entries)
        
        earned_count = 0
        total_count = len(achievements_list)
        
        col1, col2 = st.columns(2)
        
        for achievement_id, achievement in achievements_list.items():
            earned = False
            
            # Check requirements
            if "score >= 10" in achievement["requirement"] and current_score >= 10:
                earned = True
            elif "score >= 50" in achievement["requirement"] and current_score >= 50:
                earned = True
            elif "score >= 500" in achievement["requirement"] and current_score >= 500:
                earned = True
            elif "score >= 400" in achievement["requirement"] and current_score >= 400:
                earned = True
            elif "diary >= 10" in achievement["requirement"] and diary_count >= 10:
                earned = True
            elif "moods >= 5" in achievement["requirement"] and len(set([entry.get('mood', '') for entry in st.session_state.diary_entries])) >= 5:
                earned = True
            
            if earned:
                st.session_state.achievements.add(achievement_id)
                earned_count += 1
            
            # Display achievement
            with col1 if len(achievements_list) % 2 == 0 or achievement_id in list(achievements_list.keys())[::2] else col2:
                if earned:
                    st.markdown(f"""
                    <div style="background: linear-gradient(135deg, #4ecdc4, #44a08d); color: white; padding: 1em; border-radius: 10px; margin: 0.5em 0;">
                        <h4>{achievement['icon']} {achievement['name']} ✅</h4>
                        <p>{achievement['desc']}</p>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div style="background: rgba(0,0,0,0.1); padding: 1em; border-radius: 10px; margin: 0.5em 0; opacity: 0.6;">
                        <h4>🔒 {achievement['name']}</h4>
                        <p>{achievement['desc']}</p>
                    </div>
                    """, unsafe_allow_html=True)
        
        # Achievement Summary
        st.markdown(f"""
        <div style="text-align: center; margin: 2em 0; padding: 1em; background: rgba(255,255,255,0.1); border-radius: 15px;">
            <h3>🎯 Achievement Progress</h3>
            <p><strong>{earned_count}/{total_count}</strong> Achievements unlocked</p>
            <div class="progress-container">
                <div class="progress-bar" style="width: {(earned_count/total_count)*100}%"></div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with tab3:
        st.markdown("### 📊 Deine Gaming-Statistiken")
        
        # Hauptstatistiken
        col1, col2, col3, col4 = st.columns(4)
        
        col1.metric("🎯 Gesamtpunkte", st.session_state.game_score)
        col2.metric("⭐ Aktuelles Level", st.session_state.game_score // 100 + 1)
        col3.metric("🏆 Achievements", len(st.session_state.achievements))
        col4.metric("📝 Diary Entries", len(st.session_state.diary_entries))
        
        # Fortschritts-Visualisierung
        st.markdown("---")
        st.markdown("### 📈 Fortschritts-Übersicht")
        
        # Simulierte Fortschrittsdaten (in echter App würde man das tracken)
        if st.session_state.game_score > 0:
            weeks = ["KW 1", "KW 2", "KW 3", "KW 4"]
            points_per_week = [
                min(st.session_state.game_score * 0.2, 50),
                min(st.session_state.game_score * 0.3, 80),
                min(st.session_state.game_score * 0.3, 100),
                min(st.session_state.game_score * 0.2, 120)
            ]
            
            st.markdown("**📊 Punkteentwicklung (simuliert):**")
            for week, points in zip(weeks, points_per_week):
                st.markdown(f"**{week}:** {points:.0f} Punkte")
                st.progress(points / 150)
        
        # Persönliche Bestleistungen
        st.markdown("---")
        st.markdown("### 🌟 Deine Bestleistungen")
        
        personal_bests = {
            "Längste Schreibsession": f"{max([len(entry.get('text', '').split()) for entry in st.session_state.diary_entries], default=0)} Wörter",
            "Höchste Tagespunkte": "50 Punkte",  # Würde man tracken
            "Längste Streak": "3 Tage in Folge",  # Würde man tracken
            "Lieblings-Kategorie": max([entry.get('category', 'Unbekannt') for entry in st.session_state.diary_entries], key=[entry.get('category', 'Unbekannt') for entry in st.session_state.diary_entries].count, default="Noch keine Daten")
        }
        
        for title, value in personal_bests.items():
            st.markdown(f"**{title}:** {value}")
    
    with tab4:
        st.markdown("### 🎯 Personalisierte Ziele")
        st.markdown("*Erstelle deine eigenen Challenges!*")
        
        # Goal Creation
        if "custom_goals" not in st.session_state:
            st.session_state.custom_goals = []
        
        st.markdown("**🎨 Neues Ziel erstellen:**")
        
        col1, col2 = st.columns(2)
        
        with col1:
            goal_text = st.text_input("Beschreibe dein Ziel:", placeholder="z.B. 'Jeden Tag 10 Min lesen'")
            goal_points = st.slider("Punkte-Belohnung:", 10, 100, 25)
            goal_difficulty = st.selectbox("Schwierigkeit:", ["Leicht", "Mittel", "Schwer", "Extrem"])
        
        with col2:
            goal_deadline = st.date_input("Bis wann?", value=datetime.datetime.now() + datetime.timedelta(days=7))
            goal_category = st.selectbox("Kategorie:", ["💪 Gesundheit", "🧠 Lernen", "❤️ Beziehungen", "🎨 Kreativität", "🏠 Haushalt", "💼 Arbeit"])
            reminder_frequency = st.selectbox("Erinnerung:", ["Täglich", "Wöchentlich", "Einmalig"])
        
        if st.button("🎯 Ziel erstellen") and goal_text:
            new_goal = {
                "id": len(st.session_state.custom_goals) + 1,
                "text": goal_text,
                "points": goal_points,
                "difficulty": goal_difficulty,
                "deadline": goal_deadline.isoformat(),
                "category": goal_category,
                "reminder": reminder_frequency,
                "completed": False,
                "created": datetime.datetime.now().isoformat()
            }
            st.session_state.custom_goals.append(new_goal)
            st.success(f"🎯 Ziel '{goal_text}' erstellt! Viel Erfolg!")
        
        # Display active goals
        if st.session_state.custom_goals:
            st.markdown("---")
            st.markdown("### 📋 Deine aktiven Ziele")
            
            active_goals = [goal for goal in st.session_state.custom_goals if not goal["completed"]]
            completed_goals = [goal for goal in st.session_state.custom_goals if goal["completed"]]
            
            for goal in active_goals:
                deadline = datetime.datetime.fromisoformat(goal["deadline"])
                days_left = (deadline - datetime.datetime.now()).days
                
                urgency_color = "#ff6b6b" if days_left <= 1 else "#feca57" if days_left <= 3 else "#48cae4"
                
                st.markdown(f"""
                <div style="background: {urgency_color}; color: white; padding: 1em; border-radius: 10px; margin: 0.5em 0;">
                    <h4>{goal['category']} {goal['text']}</h4>
                    <p>Belohnung: {goal['points']} Punkte | Schwierigkeit: {goal['difficulty']}</p>
                    <p>⏰ Noch {days_left} Tag(e) | Reminder: {goal['reminder']}</p>
                </div>
                """, unsafe_allow_html=True)
                
                col1, col2 = st.columns(2)
                with col1:
                    if st.button(f"✅ Ziel erreicht!", key=f"complete_{goal['id']}"):
                        goal["completed"] = True
                        st.session_state.game_score += goal["points"]
                        st.balloons()
                        st.success(f"🎉 Glückwunsch! +{goal['points']} Punkte für '{goal['text']}'!")
                        st.rerun()
                
                with col2:
                    if st.button(f"🗑️ Ziel löschen", key=f"delete_{goal['id']}"):
                        st.session_state.custom_goals = [g for g in st.session_state.custom_goals if g["id"] != goal["id"]]
                        st.info("Ziel gelöscht. Manchmal ändern sich Prioritäten!")
                        st.rerun()
            
            # Completed goals
            if completed_goals:
                st.markdown("### ✅ Erreichte Ziele")
                for goal in completed_goals[-5:]:  # Zeige die letzten 5
                    st.markdown(f"✅ {goal['category']} {goal['text']} (+{goal['points']} Punkte)")

def handle_emotions_module():
    """Erweiterte Emotions-Regulation"""
    
    tab1, tab2, tab3, tab4 = st.tabs(["🌡️ Gefühls-Check", "🎨 Emotion-Mapping", "🧘 Regulation-Tools", "📊 Emotion-History"])
    
    with tab1:
        st.markdown("### 💙 Wie geht es dir gerade wirklich?")
        st.markdown("*Sei ehrlich - hier wird nicht geurteilt!*")
        
        # Erweiterte Emotionsauswahl
        emotion_categories = {
            "😢 Traurig": {
                "subcategories": ["Melancholisch", "Traurig", "Deprimiert", "Hoffnungslos", "Leer"],
                "color": "#74b9ff"
            },
            "😰 Ängstlich": {
                "subcategories": ["Nervös", "Besorgt", "Panisch", "Unsicher", "Überwältigt"],
                "color": "#fd79a8"
            },
            "😡 Wütend": {
                "subcategories": ["Genervt", "Frustriert", "Zornig", "Verbittert", "Empört"],
                "color": "#e17055"
            },
            "😴 Müde": {
                "subcategories": ["Erschöpft", "Ausgelaugt", "Energielos", "Burnt-out", "Müde"],
                "color": "#a29bfe"
            },
            "🤗 Einsam": {
                "subcategories": ["Isoliert", "Unverstanden", "Verlassen", "Sehnsüchtig", "Distanziert"],
                "color": "#00cec9"
            },
            "😖 Überfordert": {
                "subcategories": ["Gestresst", "Unter Druck", "Chaotisch", "Verloren", "Hilflos"],
                "color": "#fdcb6e"
            },
            "😌 Ruhig": {
                "subcategories": ["Entspannt", "Friedlich", "Gelassen", "Ausgeglichen", "Zentiert"],
                "color": "#00b894"
            },
            "✨ Positiv": {
                "subcategories": ["Hoffnungsvoll", "Dankbar", "Motiviert", "Glücklich", "Euphorisch"],
                "color": "#ffeaa7"
            }
        }
        
        col1, col2 = st.columns([1, 2])
        
        with col1:
            st.markdown("**🎯 Hauptemotion wählen:**")
            selected_main_emotion = None
            
            for emotion, data in emotion_categories.items():
                if st.button(emotion, key=f"main_{emotion}"):
                    selected_main_emotion = emotion
                    st.session_state.selected_emotion_data = data
                    st.session_state.selected_main_emotion = emotion
        
        with col2:
            if hasattr(st.session_state, 'selected_emotion_data'):
                data = st.session_state.selected_emotion_data
                main_emotion = st.session_state.selected_main_emotion
                
                st.markdown(f"**🎨 Nuancen von {main_emotion}:**")
                selected_subcategory = st.selectbox(
                    "Genauer gesagt fühlst du dich:",
                    data["subcategories"],
                    key="emotion_subcategory"
                )
                
                intensity = st.slider(
                    "Wie stark? (1-10)",
                    1, 10, 5,
                    help="1 = kaum spürbar, 10 = überwältigend"
                )
                
                # Visualisierung der Emotion
                st.markdown(f"""
                <div style="background: {data['color']}; color: white; padding: 2em; border-radius: 15px; text-align: center; margin: 1em 0;">
                    <h3>{main_emotion}</h3>
                    <h4>{selected_subcategory}</h4
