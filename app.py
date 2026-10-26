import streamlit as st
import os
import sys

# Ensure we can import from src
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.styles import apply_custom_styles
from src.auth import init_auth_db
from src.data_loader import load_data
from src.i18n import get_text, translate_columns
from views.login import render_login_page
from views.dashboard import render_dashboard
from views.screener import render_screener
from views.mexican_radar import render_radar
from views.apm import render_apm
from views.user_management import render_user_management

st.set_page_config(
    page_title="Reliarisk T-Matrix",
    page_icon="🛢️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply CSS injection
apply_custom_styles()

def main():
    # Initialize authentication database
    init_auth_db()

    # Session State initialization
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
    if "user" not in st.session_state:
        st.session_state.user = None
    if "language" not in st.session_state:
        st.session_state.language = "Español"

    # --- Authentication Gate ---
    if not st.session_state.authenticated:
        render_login_page()
        return

    current_user = st.session_state.user or {}
    is_admin = current_user.get("role") == "admin"

    # --- Sidebar ---
    with st.sidebar:
        # Logos Implementation with Equal Height
        import base64
        def get_img_as_base64(file):
            if not os.path.exists(file):
                return None
            with open(file, "rb") as f:
                data = f.read()
            return base64.b64encode(data).decode()

        try:
            mi_logo_b64 = get_img_as_base64("mi_logo.png")
            logo_app_b64 = get_img_as_base64("logo_app.png")
            if mi_logo_b64 and logo_app_b64:
                st.sidebar.markdown(
                    '<div style="display: flex; justify-content: center; align-items: center; gap: 20px; margin-bottom: 10px;">'
                    f'<img src="data:image/png;base64,{mi_logo_b64}" style="height: 65px; width: auto; object-fit: contain;">'
                    f'<img src="data:image/png;base64,{logo_app_b64}" style="height: 65px; width: auto; object-fit: contain;">'
                    '</div>',
                    unsafe_allow_html=True
                )
        except Exception:
            st.sidebar.warning("Logos no encontrados")
        
        st.markdown("<h4 style='text-align: center; color: var(--tertiary-fixed-dim); margin-top: 10px; margin-bottom: 15px; font-weight: 700; font-family: space-grotesk;'>Reliarisk T-Matrix</h4>", unsafe_allow_html=True)

        # Active User Profile Card
        role_badge = "🛡️ Administrador" if is_admin else "👤 Usuario"
        st.sidebar.markdown(
            '<div style="background: rgba(1, 39, 67, 0.05); padding: 12px 14px; border-radius: 10px; margin-bottom: 15px; border: 1px solid var(--outline-variant);">'
            '<div style="font-size: 0.72rem; color: var(--text-secondary); text-transform: uppercase; font-weight: 600; letter-spacing: 0.5px;">Sesión Activa</div>'
            f'<div style="font-weight: 700; color: var(--primary); font-size: 0.95rem; margin-top: 2px;">{current_user.get("name", "Usuario")}</div>'
            f'<div style="font-size: 0.75rem; color: #0284c7; margin-top: 2px; font-weight: 600;">{role_badge} <span style="color: var(--text-secondary); font-weight: 400;">(@{current_user.get("username")})</span></div>'
            '</div>',
            unsafe_allow_html=True
        )

        # Logout button
        if st.sidebar.button("🚪 Cerrar Sesión / Logout", use_container_width=True):
            st.session_state.authenticated = False
            st.session_state.user = None
            st.rerun()

        st.markdown("<hr style='border-color: var(--outline-variant); margin: 15px 0;'/>", unsafe_allow_html=True)

        # Language Selector
        st.selectbox("Idioma / Language", ["Español", "English"], key='language')
                
        st.markdown("<br/>", unsafe_allow_html=True)
        
        st.markdown(f"<div class='label-sm' style='margin-bottom: 10px;'>{get_text('nav_title')}</div>", unsafe_allow_html=True)
        
        # Navigation
        pages = [
            get_text("nav_dashboard"),
            get_text("nav_screener"),
            get_text("nav_apm"),
            get_text("nav_radar"),
            get_text("nav_users")
        ]
        page = st.radio("Ir a / Go to", pages, label_visibility="collapsed")
        
        st.markdown("<br/>"*2, unsafe_allow_html=True)
        
        # Methodology snippets
        with st.expander(get_text("sidebar_mexican_title")):
            st.markdown(f"""
                <div class='body-sm'>
                {get_text("sidebar_mexican_content")}
                <br/><br/>
                • Infraestructura / Infrastructure<br/>
                • Seguridad / Security<br/>
                • Uso de Suelo / Land Use<br/>
                • Agua / Water<br/>
                • Arena / Sand<br/>
                • Vías de Acceso / Access Roads<br/>
                • Densidad Poblacional / Population Den.
                </div>
            """, unsafe_allow_html=True)

        with st.expander(get_text("sidebar_shale_title")):
            st.markdown(f"""
                <div class='body-sm'>
                {get_text("sidebar_shale_content")}
                <br/><br/>
                • <b>35%</b> Reservas / Reserves (Volumen)<br/>
                • <b>30%</b> Índice M.E.X.I.C.A.N. (Logística)<br/>
                • <b>20%</b> Gravedad API / API Gravity (Calidad)<br/>
                • <b>15%</b> RGP / GOR (Diseño de instalaciones)
                </div>
            """, unsafe_allow_html=True)

    # --- Top App Bar (compact, single row) ---
    st.markdown(
        '<div class="app-bar">'
        '<div class="app-bar__brand">'
        '<span class="app-bar__mark"></span>'
        '<span class="app-bar__title">Reliarisk <span class="app-bar__title-accent">T-Matrix</span></span>'
        '<span class="app-bar__sep"></span>'
        f'<span class="app-bar__subtitle">{get_text("dash_sub")}</span>'
        '</div>'
        f'<div class="app-bar__crumb"><span class="app-bar__dot"></span>{page}</div>'
        '</div>',
        unsafe_allow_html=True
    )

    # --- Routing Views ---
    if page == get_text("nav_users"):
        render_user_management()
        return

    # --- Load Data for Analytical Views ---
    df = load_data()
    
    if df is not None:
        if page == get_text("nav_dashboard"):
            render_dashboard(df)
        elif page == get_text("nav_screener"):
            df_translated = translate_columns(df.copy())
            render_screener(df_translated)
        elif page == get_text("nav_apm"):
            render_apm(df)
        elif page == get_text("nav_radar"):
            render_radar(df)
    else:
        st.error("No se pudo cargar la base de datos de oportunidades.")

if __name__ == "__main__":
    main()
