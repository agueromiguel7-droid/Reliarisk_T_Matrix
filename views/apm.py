import streamlit as st
import plotly.express as px
import pandas as pd
from src.i18n import get_text

def render_apm(df):
    st.markdown(f"<div class='headline-md'>{get_text('apm_title')}</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='body-sm mb-8'>{get_text('apm_desc')}</div>", unsafe_allow_html=True)
    
    if df.empty:
        st.warning(get_text('rad_err'))
        return

    # Ensure numerical columns are ready (now directly from data_loader mapping)
    df['IMP_Numeric'] = pd.to_numeric(df.get('IMP_Score', 0), errors='coerce').fillna(0)
    df['SHALE_Mx'] = pd.to_numeric(df.get('SHALE_Mx', 0), errors='coerce').fillna(0)
    
    # These are already handled in data_loader rename_dict or calculated there
    # But we ensure they are numeric for plotting
    for c in ['Gravedad_API', 'Reserva_Equiv_MMBN', 'NP_MMBN', 'GP_MMMPC', 'RGP_pc_bn']:
        if c in df.columns:
            df[c] = pd.to_numeric(df[c], errors='coerce').fillna(0)

    col1, col2 = st.columns(2)
    
    x_options = {
        get_text("dash_api"): "Gravedad_API",
        get_text("dash_mex_idx"): "IMP_Numeric",
        get_text("apm_total_cost"): "Total_Cost"
    }
    
    y_options = {
        get_text("map_res_equiv"): "Reserva_Equiv_MMBN",
        get_text("apm_res_oil"): "NP_MMBN",
        get_text("apm_res_gas"): "GP_MMMPC",
        get_text("rad_kpi_gor"): "RGP_pc_bn"
    }
    
    x_label = col1.selectbox(get_text('apm_x'), list(x_options.keys()), index=0)
    y_label = col2.selectbox(get_text('apm_y'), list(y_options.keys()), index=0)
    
    st.markdown("<hr style='border-color: var(--outline-variant); margin-top: 1rem; margin-bottom: 2rem;'/>", unsafe_allow_html=True)
    
    x_col = x_options[x_label]
    y_col = y_options[y_label]
    
    plot_df = df.dropna(subset=[x_col, y_col]).copy()
    
    if plot_df.empty:
        st.warning("No hay suficientes datos válidos para generar el gráfico.")
        return

    # Bubble Size handling based on SHALE_Mx - Normalize for better visualization
    if not plot_df['SHALE_Mx'].empty:
        s_min, s_max = plot_df['SHALE_Mx'].min(), plot_df['SHALE_Mx'].max()
        if s_max > s_min:
            plot_df['bubble_size'] = 10 + ((plot_df['SHALE_Mx'] - s_min) / (s_max - s_min)) * 40
        else:
            plot_df['bubble_size'] = 25
    else:
        plot_df['bubble_size'] = 10
        
    st.markdown("<div class='card-lowest' style='margin-top: 20px; padding: 15px;'>", unsafe_allow_html=True)
    
    try:
        # Define hover data with specific formatting
        hover_data_config = {
            x_col: ":.4f",
            y_col: ":.4f",
            'SHALE_Mx': ":.4f",
            'bubble_size': False # Hide internal scaling factor
        }
        
        fig = px.scatter(
            plot_df, x=x_col, y=y_col, hover_name='Oportunidad', 
            color='SHALE_Mx', color_continuous_scale='Blues',
            size='bubble_size', size_max=40,
            opacity=0.8,
            hover_data=hover_data_config,
            labels={x_col: x_label, y_col: y_label, 'SHALE_Mx': get_text("dash_shale_idx")},
            template='plotly_dark'
        )
        
        fig.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font_color='#e2e2e5',
            xaxis=dict(gridcolor='rgba(128,128,128,0.1)'),
            yaxis=dict(gridcolor='rgba(128,128,128,0.1)'),
            margin=dict(l=20, r=20, t=30, b=20)
        )
        st.plotly_chart(fig, use_container_width=True)
    except Exception as e:
        st.error(f"Error generando gráfico APM: {e}")
        
    st.markdown("</div>", unsafe_allow_html=True)
