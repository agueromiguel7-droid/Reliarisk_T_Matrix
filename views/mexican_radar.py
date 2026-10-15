import streamlit as st
import plotly.graph_objects as go
from src.data_loader import get_mexican_factors
from src.i18n import get_text

def render_radar(df):
    st.markdown(f"<div class='headline-md'>{get_text('rad_title')}</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='body-sm mb-8'>{get_text('rad_multivariate')}</div>", unsafe_allow_html=True)

    if df.empty or 'Oportunidad' not in df.columns:
        st.warning(get_text("rad_err"))
        return

    # Selectores
    col_area, col_sector, col_op = st.columns(3)
    
    # Internal keys are now guaranteed by data_loader
    col_area_name = 'Area'
    col_sector_name = 'Sector'
    
    filtered_df = df.copy()

    with col_area:
        if col_area_name in filtered_df.columns:
            areas = [get_text("scr_all")] + sorted(filtered_df[col_area_name].dropna().unique().tolist())
            selected_area = st.selectbox(get_text("dash_area"), areas)
            if selected_area != get_text("scr_all"):
                filtered_df = filtered_df[filtered_df[col_area_name] == selected_area]

    with col_sector:
        if col_sector_name in filtered_df.columns:
            sectors = [get_text("scr_all")] + sorted(filtered_df[col_sector_name].dropna().unique().tolist())
            selected_sector = st.selectbox(get_text("dash_sector"), sectors)
            if selected_sector != get_text("scr_all"):
                filtered_df = filtered_df[filtered_df[col_sector_name] == selected_sector]

    with col_op:
        oportunidades = sorted(filtered_df['Oportunidad'].dropna().unique().tolist())
        selected_op = st.selectbox(get_text("rad_select"), oportunidades) if oportunidades else None

    st.markdown("<hr style='border-color: var(--outline-variant); margin-top: 1rem; margin-bottom: 2rem;'/>", unsafe_allow_html=True)

    if selected_op:
        factors = get_mexican_factors(df, selected_op)
        row = df[df['Oportunidad'] == selected_op].iloc[0]
        imp_score = row.get('IMP_Score', 0)
        
        if not factors:
            st.error("No se pudieron extraer los factores para esta oportunidad.")
            return

        col_left, col_right = st.columns([1, 1])

        with col_left:
            st.markdown("<div class='card-lowest'>", unsafe_allow_html=True)
            st.markdown(f"<div style='font-family: Space Grotesk; font-size: 1.5rem; font-weight: 700; color: var(--primary);'>{selected_op}</div>", unsafe_allow_html=True)
            st.markdown(f"<div class='label-sm' style='margin-bottom: 20px;'>{row.get('Area', 'Área no definida')}</div>", unsafe_allow_html=True)
            
            # Show IMP Score prominently
            st.markdown("<div class='bento-cell' style='background: linear-gradient(135deg, var(--primary) 0%, var(--primary-container) 100%); color: white; border: none;'>", unsafe_allow_html=True)
            st.markdown("<div class='label-sm' style='color: #b2b9c1;'>Índice M.E.X.I.C.A.N.</div>", unsafe_allow_html=True)
            st.markdown(f"<div style='font-family: Space Grotesk; font-size: 3rem; font-weight: 700; color: var(--tertiary-fixed-dim);'>{float(imp_score):.2f}</div>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)
            
            st.markdown("<div class='mt-4'>", unsafe_allow_html=True)
            
            label_map = {
                'infra': get_text('rad_fac_inf'),
                'security': get_text('rad_fac_sec'),
                'land_use': get_text('rad_fac_lu'),
                'water': get_text('rad_fac_water'),
                'sand': get_text('rad_fac_sand'),
                'roads': get_text('rad_fac_roads'),
                'pop': get_text('rad_fac_pop')
            }
            
            # Display factor bars
            for label, value in factors.items():
                val_float = float(value)
                pct = (val_float / 10.0) * 100 if val_float <= 10 else 100 # Assuming max is 10
                t_label = label_map.get(label, label)
                st.markdown(f"""
                <div style='margin-bottom: 10px;'>
                    <div style='display: flex; justify-content: space-between; margin-bottom: 4px;'>
                        <span class='label-sm'>{t_label}</span>
                        <span class='body-sm' style='font-weight: 600;'>{val_float}</span>
                    </div>
                    <div style='width: 100%; background-color: var(--surface-container-highest); border-radius: 4px; height: 6px;'>
                        <div style='width: {pct}%; background-color: var(--tertiary-fixed-dim); height: 100%; border-radius: 4px;'></div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

        with col_right:
            st.markdown("<div class='card-lowest' style='height: 100%; display: flex; align-items: center; justify-content: center;'>", unsafe_allow_html=True)
            
            # Prepare data for Radar Chart
            categories = [label_map.get(k, k) for k in factors.keys()]
            values = list(factors.values())
            
            # Close the loop for the radar chart
            categories.append(categories[0])
            values.append(values[0])
            
            # Wrap labels to prevent cutoff
            wrapped_categories = [c.replace(' ', '<br>') for c in categories]

            fig = go.Figure()
            fig.add_trace(go.Scatterpolar(
                r=values,
                theta=wrapped_categories,
                fill='toself',
                fillcolor='rgba(0, 229, 255, 0.2)', # tertiary-fixed-dim with opacity
                line=dict(color='#00E5FF', width=2),
                name=get_text('rad_title')
            ))

            fig.update_layout(
                polar=dict(
                    radialaxis=dict(
                        visible=True,
                        range=[0, 10], # Assuming max score is 10
                        gridcolor='rgba(195, 199, 206, 0.3)',
                        tickfont=dict(color='#5e6368')
                    ),
                    angularaxis=dict(
                        tickfont=dict(size=11, color='#1a1c1e', family='Inter'),
                        gridcolor='rgba(195, 199, 206, 0.3)'
                    ),
                    bgcolor='rgba(0,0,0,0)'
                ),
                showlegend=False,
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                margin=dict(l=40, r=40, t=40, b=40)
            )
            
            st.plotly_chart(fig, use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)
            
    # Context section
    st.markdown("<div class='card-low mt-8'>", unsafe_allow_html=True)
    st.markdown(f"<div style='font-family: Space Grotesk; font-size: 1.25rem; font-weight: 600; color: var(--primary); margin-bottom: 10px;'>{get_text('rad_method_title')}</div>", unsafe_allow_html=True)
    st.markdown(f"""
    <div class='body-sm'>
    {get_text('rad_method_body')}
    </div>
    """, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)
