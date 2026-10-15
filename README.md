# Reliarisk T-Matrix 🛢️

**Reliarisk T-Matrix** es una plataforma analítica y de soporte para la toma de decisiones estratégicas en la evaluación y jerarquización de oportunidades en **Yacimientos de Baja Permeabilidad (YBP)**.

La herramienta integra indicadores geológicos, de producción, calidad de hidrocarburo y viabilidad logística superficial mediante los modelos cuantitativos **S.H.A.L.E.-Mx** y **M.E.X.I.C.A.N.**.

---

## 🚀 Características Principales

1. **🔐 Control de Accesos y Gestión de Usuarios:**
   - Autenticación segura de usuarios mediante almacenamiento cifrado (PBKDF2 HMAC SHA-256).
   - Roles diferenciados: **Administrador** y **Usuario**.
   - Módulo administrativo para crear nuevos usuarios, restablecer contraseñas y dar de baja cuentas.
   - Perfil de usuario para actualización personal de credenciales.
   
2. **📊 Executive Portfolio (YBP):**
   - Resumen ejecutivo de portafolio con KPIs clave, mapa geoespacial interactivo (PyDeck) y ranking ponderado multivariante.

3. **🔍 Opportunity Screener:**
   - Tabla dinámica e interactiva de filtrado, ordenamiento y exportación de prospectos a CSV.

4. **📈 Asset Performance Matrix (APM):**
   - Matriz de dispersión multivariable configurable para comparar costos vs. reservas vs. índices de viabilidad.

5. **🎯 Radar M.E.X.I.C.A.N.:**
   - Visualización gráfica de araña/radar sobre 7 dimensiones críticas: Infraestructura, Seguridad, Uso de Suelo, Agua, Arena, Vías de Acceso y Población.

6. **🌐 Soporte Bilingüe:**
   - Conmutación en tiempo real entre **Español** e **Inglés**.

---

## 🔑 Credenciales Iniciales de Administrador

Al iniciar la plataforma por primera vez, el sistema autoconfigura el usuario administrador predeterminado:

- **Usuario:** `admin`
- **Contraseña:** `Coromoto_22`
- **Rol:** `Administrador`

> 💡 *Una vez dentro, el administrador puede crear nuevas cuentas de acceso desde el menú lateral en **Control de Accesos / Usuarios**.*

---

## 🛠️ Ejecución Local

1. **Clonar o descargar el repositorio:**
   ```bash
   git clone <URL_DEL_REPOSITORIO>
   cd "Reliarisk T-Matrix"
   ```

2. **Crear y activar un entorno virtual (recomendado):**
   ```bash
   python -m venv venv
   # En Windows:
   venv\Scripts\activate
   # En Linux / macOS:
   source venv/bin/activate
   ```

3. **Instalar dependencias:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Ejecutar la aplicación:**
   ```bash
   streamlit run app.py
   ```

---

## ☁️ Publicación en Streamlit Community Cloud

Para desplegar la aplicación en la nube de Streamlit de forma gratuita y accesible vía navegador:

1. **Subir este código a un repositorio en GitHub:**
   - Crear un nuevo repositorio en [GitHub](https://github.com/new) (puede ser Público o Privado).
   - Enlazar y subir los cambios:
     ```bash
     git init
     git add .
     git commit -m "feat: initial commit with access control and analytics"
     git branch -M main
     git remote add origin https://github.com/<TU_USUARIO>/<TU_REPOSITORIO>.git
     git push -u origin main
     ```

2. **Ingresar a Streamlit Community Cloud:**
   - Ir a [share.streamlit.io](https://share.streamlit.io/) e iniciar sesión con tu cuenta de GitHub.

3. **Crear una nueva App:**
   - Pulsar el botón **"Create app"** o **"New app"**.
   - Seleccionar el repositorio de GitHub recién creado.
   - En **Main file path**, colocar: `app.py`.
   - Pulsar **"Deploy!"**.

4. **Listo:**
   - Streamlit instalará automáticamente las dependencias listadas en `requirements.txt`.
   - Podrás ingresar con el usuario `admin` y clave `Coromoto_22` y crear los accesos para tu equipo.

---

## 📁 Estructura del Proyecto

```text
├── app.py                      # Punto de entrada principal y ruteador
├── requirements.txt            # Dependencias de Python para Streamlit Cloud
├── .gitignore                  # Exclusiones de Git
├── README.md                   # Documentación general y guía de despliegue
├── mi_logo.png                 # Logotipo corporativo Reliarisk
├── logo_app.png                # Logotipo aplicativo T-Matrix
├── Oportunidades Exploratoria YBP.xlsx   # Base de datos de yacimientos
├── Encabezado Español-Ingles.xlsx        # Mapeo de columnas bilingüe
├── .streamlit/
│   └── config.toml             # Tema visual y configuración del servidor
├── src/
│   ├── auth.py                 # Lógica de autenticación, hash seguro y base de datos
│   ├── data_loader.py          # Procesamiento y cálculo de índices S.H.A.L.E.-Mx y MEXICAN
│   ├── i18n.py                 # Diccionario y utilidades de internacionalización
│   ├── schema_manager.py       # Mapeo y validación de esquemas de datos
│   └── styles.py               # Estilos CSS modernos y tema visual
└── views/
    ├── login.py                # Pantalla de inicio de sesión
    ├── user_management.py      # Interfaz de creación y gestión de usuarios
    ├── dashboard.py            # Vista Executive Portfolio
    ├── screener.py             # Vista Opportunity Screener
    ├── apm.py                  # Vista Asset Performance Matrix
    └── mexican_radar.py        # Vista Radar M.E.X.I.C.A.N.
```
