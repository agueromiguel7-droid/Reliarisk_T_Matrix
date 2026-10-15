import streamlit as st
import pandas as pd
from src.auth import list_users, create_user, delete_user, update_password
from src.i18n import get_text

def render_user_management():
    current_user = st.session_state.get("user", {})
    is_admin = current_user.get("role") == "admin"
    current_username = current_user.get("username", "")

    st.markdown("""
        <div style="margin-bottom: 1.5rem;">
            <h2 style="font-family: 'Space Grotesk', sans-serif; color: var(--primary); margin-bottom: 0.2rem;">
                ⚙️ Control de Accesos y Gestión de Usuarios
            </h2>
            <p style="color: var(--text-secondary); font-size: 0.95rem;">
                Administre las cuentas con acceso a la plataforma Reliarisk T-Matrix.
            </p>
        </div>
    """, unsafe_allow_html=True)

    if not is_admin:
        # Standard user view: change own password
        st.info("Su cuenta tiene permisos estándar. Puede actualizar su contraseña a continuación.")
        _render_my_account(current_username)
        return

    # Admin view with tabs
    tabs = st.tabs(["👥 Usuarios Registrados", "➕ Registrar Nuevo Usuario", "🔑 Mi Cuenta"])

    with tabs[0]:
        _render_user_list(current_username)

    with tabs[1]:
        _render_create_user_form()

    with tabs[2]:
        _render_my_account(current_username)


def _render_user_list(current_username: str):
    users = list_users()
    
    # Summary KPIs
    total_users = len(users)
    admin_count = sum(1 for u in users if u["role"] == "admin")
    regular_count = total_users - admin_count

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f"""
            <div class="card-lowest" style="padding: 16px; text-align: center;">
                <div style="font-size: 0.8rem; color: var(--text-secondary); font-weight: 600; text-transform: uppercase;">Total Cuentas</div>
                <div style="font-size: 2rem; font-weight: 700; color: var(--primary);">{total_users}</div>
            </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
            <div class="card-lowest" style="padding: 16px; text-align: center;">
                <div style="font-size: 0.8rem; color: var(--text-secondary); font-weight: 600; text-transform: uppercase;">Administradores</div>
                <div style="font-size: 2rem; font-weight: 700; color: #0284c7;">{admin_count}</div>
            </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown(f"""
            <div class="card-lowest" style="padding: 16px; text-align: center;">
                <div style="font-size: 0.8rem; color: var(--text-secondary); font-weight: 600; text-transform: uppercase;">Usuarios Regulares</div>
                <div style="font-size: 2rem; font-weight: 700; color: #10b981;">{regular_count}</div>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("<br/>", unsafe_allow_html=True)

    # User table
    df_users = pd.DataFrame(users)
    if not df_users.empty:
        display_df = df_users[["username", "name", "role", "created_at", "is_active"]].copy()
        display_df.columns = ["Usuario", "Nombre Completo", "Rol", "Fecha de Alta", "Activo"]
        display_df["Rol"] = display_df["Rol"].map({"admin": "🛡️ Administrador", "user": "👤 Usuario"})
        display_df["Activo"] = display_df["Activo"].map({True: "✅ Sí", False: "❌ No"})

        st.dataframe(
            display_df,
            use_container_width=True,
            hide_index=True
        )

    st.markdown("<br/>", unsafe_allow_html=True)
    st.markdown("#### 🛠️ Acciones sobre Usuarios")

    col_del, col_pwd = st.columns(2)

    with col_del:
        st.markdown("**Eliminar Usuario**")
        non_admin_users = [u["username"] for u in users if u["username"] != "admin"]
        if non_admin_users:
            user_to_delete = st.selectbox("Seleccione usuario a eliminar:", non_admin_users, key="del_select")
            if st.button("🗑️ Eliminar Usuario", type="secondary", key="btn_del_user"):
                ok, msg = delete_user(user_to_delete)
                if ok:
                    st.success(msg)
                    st.rerun()
                else:
                    st.error(msg)
        else:
            st.caption("No hay usuarios adicionales para eliminar.")

    with col_pwd:
        st.markdown("**Restablecer Contraseña**")
        all_usernames = [u["username"] for u in users]
        user_to_reset = st.selectbox("Seleccione usuario:", all_usernames, key="reset_select")
        new_pwd = st.text_input("Nueva Contraseña", type="password", key="reset_pwd")
        if st.button("🔄 Actualizar Contraseña", key="btn_reset_pwd"):
            if len(new_pwd) < 6:
                st.error("La contraseña debe tener al menos 6 caracteres.")
            else:
                ok, msg = update_password(user_to_reset, new_pwd)
                if ok:
                    st.success(f"Contraseña actualizada para '{user_to_reset}'.")
                else:
                    st.error(msg)


def _render_create_user_form():
    st.markdown("#### ➕ Registrar Nueva Cuenta de Acceso")
    st.caption("Complete el formulario para autorizar el ingreso de un nuevo analista o administrador.")

    with st.form("create_user_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input("Nombre y Apellido *", placeholder="Ej. Juan Pérez")
            username = st.text_input("Usuario (Login) *", placeholder="Ej. jperez").strip().lower()
            role = st.selectbox("Rol del Usuario", ["user", "admin"], format_func=lambda x: "👤 Usuario Estándar" if x == "user" else "🛡️ Administrador")

        with col2:
            password = st.text_input("Contraseña *", type="password", help="Mínimo 6 caracteres")
            password_confirm = st.text_input("Confirmar Contraseña *", type="password")

        submitted = st.form_submit_button("Crear Usuario", type="primary")

        if submitted:
            if not name or not username or not password:
                st.error("Todos los campos marcados con asterisco (*) son obligatorios.")
            elif password != password_confirm:
                st.error("Las contraseñas no coinciden. Por favor verifíquelas.")
            elif len(password) < 6:
                st.error("La contraseña debe tener al menos 6 caracteres.")
            else:
                ok, msg = create_user(username=username, password=password, name=name, role=role)
                if ok:
                    st.success(f"✅ {msg}")
                    st.rerun()
                else:
                    st.error(f"❌ {msg}")


def _render_my_account(username: str):
    st.markdown(f"#### 👤 Perfil de Cuenta: `{username}`")
    with st.form("change_my_pwd_form", clear_on_submit=True):
        new_pass = st.text_input("Nueva Contraseña", type="password")
        new_pass_confirm = st.text_input("Confirmar Nueva Contraseña", type="password")
        submit_btn = st.form_submit_button("Guardar Nueva Contraseña")

        if submit_btn:
            if not new_pass or len(new_pass) < 6:
                st.error("La contraseña debe tener al menos 6 caracteres.")
            elif new_pass != new_pass_confirm:
                st.error("Las contraseñas no coinciden.")
            else:
                ok, msg = update_password(username, new_pass)
                if ok:
                    st.success("✅ Contraseña actualizada correctamente.")
                else:
                    st.error(f"❌ {msg}")
