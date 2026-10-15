import streamlit as st
import base64
import os
from src.auth import authenticate

def _get_img_as_base64(file_path):
    if not os.path.exists(file_path):
        return None
    try:
        with open(file_path, "rb") as f:
            data = f.read()
        return base64.b64encode(data).decode()
    except Exception:
        return None

def render_login_page():
    # Spacing and layout alignment
    st.markdown("<br/>", unsafe_allow_html=True)
    _, center_col, _ = st.columns([1, 1.8, 1])

    with center_col:
        # Generate logos HTML without any leading indentation (preventing markdown code block interpretation)
        mi_logo_b64 = _get_img_as_base64("mi_logo.png")
        logo_app_b64 = _get_img_as_base64("logo_app.png")

        logo_imgs = ""
        if mi_logo_b64:
            logo_imgs += f'<img src="data:image/png;base64,{mi_logo_b64}" style="height: 65px; width: auto; object-fit: contain;" alt="Logo Reliarisk" />'
        if logo_app_b64:
            logo_imgs += f'<img src="data:image/png;base64,{logo_app_b64}" style="height: 65px; width: auto; object-fit: contain;" alt="Logo T-Matrix" />'

        header_card_html = (
            '<div style="text-align: center; margin-bottom: 1.5rem; padding: 2rem 1.5rem 1.5rem 1.5rem; '
            'background: #ffffff; border-radius: 14px; border: 1px solid rgba(195, 199, 206, 0.25); '
            'box-shadow: 0 4px 20px rgba(0, 0, 0, 0.04);">'
            f'<div style="display: flex; justify-content: center; align-items: center; gap: 20px; margin-bottom: 16px;">{logo_imgs}</div>'
            '<h2 style="font-family: \'Space Grotesk\', sans-serif; font-size: 2.1rem; font-weight: 700; color: #012743; margin: 0 0 6px 0;">Reliarisk T-Matrix</h2>'
            '<p style="color: #5e6368; font-size: 0.95rem; margin: 0;">Control de Accesos • Evaluación de Yacimientos de Baja Permeabilidad (YBP)</p>'
            '</div>'
        )
        st.markdown(header_card_html, unsafe_allow_html=True)

        # Login Card Container
        with st.form("login_form", clear_on_submit=False):
            st.markdown(
                '<div style="font-weight: 600; color: #012743; font-size: 1.15rem; margin-bottom: 12px;">'
                '🔐 Iniciar Sesión'
                '</div>',
                unsafe_allow_html=True
            )

            username = st.text_input("Usuario", placeholder="admin", key="login_username").strip()
            password = st.text_input("Contraseña", type="password", placeholder="••••••••", key="login_password")

            st.markdown("<div style='height: 8px;'></div>", unsafe_allow_html=True)
            submit_login = st.form_submit_button("Ingresar a la Plataforma", type="primary", use_container_width=True)

            if submit_login:
                if not username or not password:
                    st.error("Por favor ingrese su usuario y contraseña.")
                else:
                    user_data = authenticate(username, password)
                    if user_data:
                        st.session_state.authenticated = True
                        st.session_state.user = user_data
                        st.success(f"¡Bienvenido, {user_data.get('name', username)}!")
                        st.rerun()
                    else:
                        st.error("❌ Credenciales inválidas. Verifique su usuario y contraseña.")

        # Helper note at bottom
        st.markdown(
            '<div style="text-align: center; margin-top: 1.5rem; font-size: 0.85rem; color: #5e6368;">'
            '🔒 Sistema protegido por autenticación segura.<br/>'
            'Para credenciales de acceso inicial, contacte al administrador.'
            '</div>',
            unsafe_allow_html=True
        )
