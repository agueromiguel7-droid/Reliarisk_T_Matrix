import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import pydeck as pdk

from src.i18n import get_text

def render_dashboard(df):
    st.markdown(f"<div class='headline-md'>{get_text('dash_overview')}</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='body-sm mb-8'>{get_text('dash_sub')}</div>", unsafe_allow_html=True)

    # Ensure numerical columns are ready
    df['IMP_Numeric'] = pd.to_numeric(df.get('IMP_Score', 0), errors='coerce').fillna(0)
    if 'Gravedad_API' in df.columns:
        df['Gravedad_API'] = pd.to_numeric(df['Gravedad_API'], errors='coerce')

    # --- 1. Top Section: Map and Filters ---
    map_container_col, filter_container_col = st.columns([3, 1])
    
    # Filter Logic
    with filter_container_col:
        st.markdown("<div class='card-lowest' style='height: 100%; border-radius: 12px; padding: 20px;'>", unsafe_allow_html=True)
        st.markdown(f"<div class='label-sm' style='font-size: 0.9rem; font-weight: 700; margin-bottom: 15px; color: var(--primary);'>{get_text('dash_filters')}</div>", unsafe_allow_html=True)
        
        if 'Area' in df.columns:
            area_list = [get_text("scr_all")] + sorted(df['Area'].dropna().unique().tolist())
            st.markdown(f"<div class='label-sm' style='font-size: 0.75rem; margin-bottom: 5px;'>{get_text('dash_area')}</div>", unsafe_allow_html=True)
            sel_area = st.selectbox(get_text("dash_area"), area_list, key="dash_area_filter", label_visibility="collapsed")
            if sel_area != get_text("scr_all"):
                df = df[df['Area'] == sel_area]
        
        st.markdown("<div style='margin-top: 15px;'></div>", unsafe_allow_html=True)
        tab_tech, tab_hier = st.tabs([get_text("dash_tech_tab"), get_text("dash_hier_tab")])
        
        with tab_tech:
            if 'Gravedad_API' in df.columns:
                api_data = df['Gravedad_API'].dropna()
                if not api_data.empty:
                    api_min, api_max = float(api_data.min()), float(api_data.max())
                    if api_min < api_max:
                        st.markdown(f"<div class='label-sm' style='font-size: 0.75rem; margin-top: 10px;'>{get_text('dash_api')}</div>", unsafe_allow_html=True)
                        sel_api = st.slider(get_text("dash_api"), api_min, api_max, (api_min, api_max), key="dash_api_slider", label_visibility="collapsed")
                        df = df[(df['Gravedad_API'] >= sel_api[0]) & (df['Gravedad_API'] <= sel_api[1])]
            
            if 'Sector' in df.columns:
                sector_list = [get_text("scr_all")] + sorted(df['Sector'].dropna().unique().tolist())
                st.markdown(f"<div class='label-sm' style='font-size: 0.75rem; margin-top: 10px;'>{get_text('dash_sector')}</div>", unsafe_allow_html=True)
                sel_sector = st.selectbox(get_text("dash_sector"), sector_list, key="dash_sector", label_visibility="collapsed")
                if sel_sector != get_text("scr_all"):
                    df = df[df['Sector'] == sel_sector]
                    
        with tab_hier:
            # SHALE-Mx Filter
            if 'SHALE_Mx' in df.columns:
                shale_data = df['SHALE_Mx'].dropna()
                if not shale_data.empty:
                    s_min, s_max = float(shale_data.min()), float(shale_data.max())
                    if s_min < s_max:
                        st.markdown(f"<div class='label-sm' style='font-size: 0.75rem; margin-top: 10px;'>{get_text('dash_shale_idx')}</div>", unsafe_allow_html=True)
                        sel_shale = st.slider(get_text("dash_shale_idx"), s_min, s_max, (s_min, s_max), key="dash_shale_slider", label_visibility="collapsed")
                        df = df[(df['SHALE_Mx'] >= sel_shale[0]) & (df['SHALE_Mx'] <= sel_shale[1])]

            # MEXICAN Filter
            if 'IMP_Numeric' in df.columns:
                imp_data = df['IMP_Numeric'].dropna()
                if not imp_data.empty:
                    imp_min, imp_max = float(imp_data.min()), float(imp_data.max())
                    if imp_min < imp_max:
                        st.markdown(f"<div class='label-sm' style='font-size: 0.75rem; margin-top: 10px;'>{get_text('dash_mex_idx')}</div>", unsafe_allow_html=True)
                        sel_imp = st.slider(get_text("dash_mex_idx"), imp_min, imp_max, (imp_min, imp_max), key="dash_imp_slider", label_visibility="collapsed")
                        df = df[(df['IMP_Numeric'] >= sel_imp[0]) & (df['IMP_Numeric'] <= sel_imp[1])]
        
        st.markdown("<br/>", unsafe_allow_html=True)
        if st.button(get_text("export_btn"), use_container_width=True):
            st.toast(get_text("export_toast"), icon="📄")
        st.markdown("</div>", unsafe_allow_html=True)

    with map_container_col:
        map_placeholder = st.empty()
        
        st.markdown(f"<div style='margin-top: 10px; margin-bottom: 5px; font-size: 0.8rem; color: var(--text-secondary); font-weight: 600;'>{get_text('map_metric')}</div>", unsafe_allow_html=True)
        metric_choice = st.radio("Métrica a visualizar:", [get_text("map_res_equiv"), get_text("map_shale")], horizontal=True, label_visibility="collapsed")
        
        if 'Latitud' in df.columns and 'Longitud' in df.columns and not df.empty:
            map_df = df.copy()
            map_df = map_df.rename(columns={'Latitud': 'lat', 'Longitud': 'lon'})
            map_df['lat'] = pd.to_numeric(map_df['lat'], errors='coerce')
            map_df['lon'] = pd.to_numeric(map_df['lon'], errors='coerce')
            map_df = map_df.dropna(subset=['lat', 'lon'])
            
            if not map_df.empty:
                if metric_choice == get_text("map_res_equiv"):
                    map_df['map_metric'] = map_df['Reserva_Equiv_MMBN'].fillna(0)
                    map_df['tooltip_text'] = map_df.apply(
                        lambda r: f"{r['Oportunidad']}\n{get_text('rank_contractual_area')} {r.get('Area', 'N/A')}\n{get_text('map_res_mmbls')}: {r['map_metric']:.2f} MMbls", axis=1
                    )
                else:
                    map_df['map_metric'] = map_df['SHALE_Mx'].fillna(0)
                    map_df['tooltip_text'] = map_df.apply(
                        lambda r: f"{r['Oportunidad']}\n{get_text('rank_contractual_area')} {r.get('Area', 'N/A')}\nS.H.A.L.E.-Mx: {r['map_metric']:.3f}", axis=1
                    )
                
                # Dynamic Radius Scaling [2000, 12000]
                min_val, max_val = map_df['map_metric'].min(), map_df['map_metric'].max()
                if max_val > min_val:
                    map_df['radius'] = 2000 + ((map_df['map_metric'] - min_val) / (max_val - min_val)) * 10000
                else:
                    map_df['radius'] = 3000

                layer = pdk.Layer(
                    "ScatterplotLayer", map_df,
                    get_position='[lon, lat]',
                    get_color='[0, 229, 255, 180]',
                    get_radius='radius', pickable=True, auto_highlight=True
                )
                view_state = pdk.ViewState(
                    latitude=map_df['lat'].mean(), longitude=map_df['lon'].mean(),
                    zoom=6.8, pitch=0,
                )
                
                with map_placeholder.container():
                    st.markdown("<div class='card-lowest' style='padding: 0; overflow: hidden;'>", unsafe_allow_html=True)
                    st.pydeck_chart(pdk.Deck(
                        map_style='dark', initial_view_state=view_state,
                        layers=[layer], tooltip={"text": "{tooltip_text}"}
                    ))
                    st.markdown("</div>", unsafe_allow_html=True)

    # --- 2. Metrics Section (KPIs) ---
    st.markdown("<br/>", unsafe_allow_html=True)
    valid_imp = df['IMP_Numeric'].dropna() if 'IMP_Numeric' in df.columns else pd.Series([])
    avg_imp = valid_imp.mean() if not valid_imp.empty else 0
    top_opportunities_count = valid_imp[valid_imp >= 7.3].count()
    total_opportunities = len(df)
    
    st.markdown("<div class='card-low'>", unsafe_allow_html=True)
    mcol1, mcol2, mcol3, mcol4 = st.columns(4)
    with mcol1:
        st.markdown(f"<div class='bento-cell'><div class='label-sm'>{get_text('kpi_total')}</div><div class='metric-value'>{{}}</div></div>".format(total_opportunities), unsafe_allow_html=True)
    with mcol2:
        st.markdown(f"<div class='bento-cell'><div class='label-sm'>{get_text('kpi_avg_imp')}</div><div class='metric-value highlight-cyan'>{{:.2f}}</div></div>".format(avg_imp), unsafe_allow_html=True)
    with mcol3:
        st.markdown(f"<div class='bento-cell'><div class='label-sm'>{get_text('kpi_top')}</div><div class='metric-value'>{{}}</div></div>".format(top_opportunities_count), unsafe_allow_html=True)
    with mcol4:
        avg_api = df['Gravedad_API'].mean() if 'Gravedad_API' in df.columns else 0
        st.markdown(f"<div class='bento-cell'><div class='label-sm'>{get_text('kpi_avg_api')}</div><div class='metric-value'>{{:.1f}}°</div></div>".format(avg_api), unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # --- 3. Bottom Section: Jerarquización (Ranking) ---
    st.markdown(f"<div class='headline-md' style='font-size: 1.5rem; margin-top: 1rem;'>{get_text('dash_ranking_title')}</div>", unsafe_allow_html=True)
    
    # Final data preparation
    df['IMP_Numeric'] = pd.to_numeric(df.get('IMP_Score', 0), errors='coerce').fillna(0)
    df['SHALE_Mx'] = pd.to_numeric(df.get('SHALE_Mx', 0), errors='coerce').fillna(0)

    def render_ranking_view(ranking_df, score_col, score_label):
        if ranking_df.empty:
            st.info(get_text("rank_empty"))
            return

        # Layout: Cards on the left, Chart on the right
        layout_col_cards, layout_col_chart = st.columns([1, 1])

        with layout_col_cards:
            # Render cards vertically in a single column
            for idx, row_data in ranking_df.iterrows():
                rank = ranking_df.index.get_loc(idx) + 1
                border_color = "#FFD700" if rank == 1 else "#C0C0C0" if rank == 2 else "#CD7F32" if rank == 3 else "var(--outline-variant)"
                bg_color = "rgba(255, 215, 0, 0.05)" if rank == 1 else "var(--surface-container-low)"
                
                name = str(row_data.get('Oportunidad', 'N/A'))
                score_val = float(row_data.get(score_col, 0))
                
                # Robust Area/Sector handling
                area_val = row_data.get('Area')
                if pd.isna(area_val) or str(area_val).lower() == 'nan' or str(area_val) == '':
                    area_val = "N/A"
                area_val = str(area_val)
                
                sector_val = str(row_data.get('Sector', 'N/A'))
                
                # Get alternative score
                if score_col == 'SHALE_Mx':
                    alt_label = "MEXICAN"
                    alt_val = float(row_data.get('IMP_Numeric', 0))
                else:
                    alt_label = "S.H.A.L.E.-Mx"
                    alt_val = float(row_data.get('SHALE_Mx', 0))

                ventaja = row_data.get('Ventaja_Estrategica')
                if pd.isna(ventaja) or str(ventaja).lower() in ['nan', 'none', '']:
                    # Try the new source name directly if internal key failed
                    ventaja = row_data.get('Strategic Investor Advantage', get_text('rank_pending'))
                
                st.markdown(f"""
                    <div style="padding: 15px; border-radius: 8px; margin-bottom: 12px; background: {bg_color}; border-left: 5px solid {border_color};">
                        <div style="display: flex; justify-content: space-between; align-items: baseline;">
                            <span style="font-weight: 700; color: var(--text-primary);">#{rank} {name}</span>
                            <span style="font-family: Space Grotesk; font-weight: 800; color: var(--tertiary-fixed-dim); font-size: 1.1rem;">{score_val:.2f}</span>
                        </div>
                        <div style='font-size: 0.75rem; margin-top: 5px; color: var(--text-secondary);'>
                            <b>{get_text('rank_contractual_area')}</b> {area_val} | <b>{get_text('rank_sector')}</b> {sector_val} | <b>{alt_label}:</b> {alt_val:.2f}
                        </div>
                        <div style='margin-top: 8px; font-size: 0.75rem; color: var(--outline); line-height: 1.4;'>💡 {str(ventaja)}</div>
                    </div>
                """, unsafe_allow_html=True)
        
        with layout_col_chart:
            # Ranking Chart side-by-side
            st.markdown("<div class='card-lowest' style='padding: 15px; height: 100%;'>", unsafe_allow_html=True)
            try:
                chart_data = ranking_df.sort_values(score_col, ascending=True).copy()
                fig = px.bar(
                    chart_data, x=score_col, y='Oportunidad', orientation='h',
                    color=score_col, color_continuous_scale='Teal',
                    labels={score_col: score_label, 'Oportunidad': ''}
                )
                fig.update_layout(
                    plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
                    margin=dict(l=0, r=10, t=10, b=10),
                    font=dict(family="Inter", size=10, color="#5e6368"),
                    height=max(500, len(ranking_df) * 35), # Dynamic height
                    showlegend=False, coloraxis_showscale=False
                )
                fig.update_xaxes(showgrid=True, gridcolor='rgba(128,128,128,0.1)')
                st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
            except Exception as e:
                st.error(f"Error visualizando ranking: {e}")
            st.markdown("</div>", unsafe_allow_html=True)

    tab_shale, tab_mexican = st.tabs([get_text("rank_shale_integral"), get_text("rank_mexican_log")])

    with tab_shale:
        st.markdown(f"<div class='body-sm' style='margin-bottom: 2rem;'>{get_text('rank_shale_top')}</div>", unsafe_allow_html=True)
        ranking_df_shale = df.sort_values('SHALE_Mx', ascending=False).head(20).copy()
        render_ranking_view(ranking_df_shale, 'SHALE_Mx', get_text("dash_shale_idx"))

    with tab_mexican:
        st.markdown(f"<div class='body-sm' style='margin-bottom: 2rem;'>{get_text('rank_mex_top')}</div>", unsafe_allow_html=True)
        ranking_df_mex = df.sort_values('IMP_Numeric', ascending=False).head(20).copy()
        render_ranking_view(ranking_df_mex, 'IMP_Numeric', get_text("dash_mex_idx"))
