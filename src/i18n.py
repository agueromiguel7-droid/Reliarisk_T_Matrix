import streamlit as st

translations = {
    "English": {
        "nav_title": "Navigation",
        "nav_dashboard": "Executive Portfolio (YBP)",
        "nav_screener": "Opportunity Screener",
        "nav_apm": "Asset Performance Matrix",
        "nav_radar": "MEXICAN Radar",
        "nav_users": "Access Control / Users",
        
        "dash_overview": "Portfolio Overview",
        "dash_sub": "Strategic Analysis of Low Permeability Reservoirs (YBP)",
        "dash_filters": "PORTFOLIO FILTERS",
        "dash_area": "CONTRACTUAL AREA",
        "dash_sector": "SECTOR",
        "dash_tech_tab": "📊 TECHNICAL VARIABLES",
        "dash_hier_tab": "🏆 HIERARCHY",
        "dash_api": "API GRAVITY",
        "dash_shale_idx": "S.H.A.L.E.-Mx Index",
        "dash_mex_idx": "MEXICAN Index",
        "dash_ranking_title": "🏆 Opportunity Ranking",
        
        "map_metric": "MAP VISUALIZATION METRIC:",
        "map_res_equiv": "Equivalent Reserves",
        "map_shale": "S.H.A.L.E.-Mx",
        "map_res_mmbls": "Reserves (MMbls)",
        
        "kpi_avg_imp": "AVG MEXICAN SCORE",
        "kpi_top": "TOP TIER (IMP > 7.3)",
        "kpi_total": "TOTAL OPPORTUNITIES",
        "kpi_avg_api": "AVERAGE API GRAVITY",
        
        "rank_empty": "No opportunities available to rank.",
        "rank_contractual_area": "Contractual Area:",
        "rank_sector": "Sector:",
        "rank_pending": "Pending technical analysis",
        "rank_shale_integral": "🎯 S.H.A.L.E.-Mx Index (Integral)",
        "rank_mexican_log": "📊 MEXICAN Index (Logistics)",
        "rank_shale_top": "Top ranked opportunities by integral evaluation (Reserves, API, GOR and IMP)",
        "rank_mex_top": "Top ranked opportunities by logistic feasibility (Infrastructure, Security, Resources)",
        
        "scr_title": "Opportunity Screener",
        "scr_desc": "Dynamic table of opportunities. Use the dropdown to sort the fields according to your investment strategy.",
        "scr_dl": "Download CSV",
        "scr_sort_by": "Sort by:",
        "scr_all": "All",
        
        "rad_title": "Integrated MEXICAN Analysis",
        "rad_select": "Select an Opportunity to analyze:",
        "rad_err": "Opportunity not found.",
        "rad_multivariate": "Multivariate Radar",
        "rad_specs": "Geological & Technical Specifications",
        "rad_kpi_res": "EQUIV. EUR (MMbls)",
        "rad_kpi_gor": "GOR (cf/bbl)",
        "rad_kpi_api": "API GRAVITY",
        "rad_kpi_depth": "DEPTH (TVD)",
        "rad_kpi_capex": "WELL CAPEX (MMUSD)",
        "rad_kpi_shale": "S.H.A.L.E.-Mx SCORE",
        "rad_fac_inf": "Infrastructure",
        "rad_fac_sec": "Security",
        "rad_fac_lu": "Land Use",
        "rad_fac_water": "Water Avail.",
        "rad_fac_sand": "Sand Avail.",
        "rad_fac_pop": "Population Den.",
        "rad_fac_roads": "Access Roads",
        "rad_method_title": "Methodological Context",
        "rad_method_body": "The **M.E.X.I.C.A.N.** index evaluates the surface and logistical feasibility for the development of Low Permeability Reservoirs. Critical factors such as the vulnerability of access roads to climate events, water resource availability for hydraulic fracturing, and proximity to silica sand (proppant) sources are considered. Areas with an **IMP score above 7.30** present optimal conditions for immediate investment due to their proximity to consolidated infrastructure and lower environmental or social restrictions.",
        
        "Well Capex - Concept": "Well Capex - Concept (MMUSD)",
        "Well Capex - Pilot": "Well Capex - Pilot (MMUSD)",
        "Well Capex - Development": "Well Capex - Development (MMUSD)",
        "Well Capex - Total": "Well Capex - Total (MMUSD)",
        
        "apm_title": "Asset Performance Matrix (APM)",
        "apm_desc": "Analyze the relationship between key field variables. The size of the bubbles corresponds to the **S.H.A.L.E.-Mx Index**.",
        "apm_x": "Select X Axis",
        "apm_y": "Select Y Axis",
        "apm_total_cost": "CAPEX + OPEX + ABEX",
        "apm_res_oil": "Oil Reserves",
        "apm_res_gas": "Gas Reserves",
        
        "export_btn": "Export Report",
        "export_toast": "Generating detailed report...",
        
        "sidebar_mexican_title": "ℹ️ About the M.E.X.I.C.A.N. Index",
        "sidebar_mexican_content": "**M.E.X.I.C.A.N.** (Multicriteria Evaluation for X-fields Investment, Connectivity, & Assets Network) is a multivariate evaluation matrix used to analyze the logistical and surface viability of hydrocarbon assets.",
        "sidebar_shale_title": "ℹ️ About the S.H.A.L.E.-Mx Index",
        "sidebar_shale_content": "**S.H.A.L.E.-Mx** (Strategic Hydrocarbon Assessment & Logistical Evaluation - Mexico) evaluates the operational and logistical viability along with the subsoil potential.",
    },
    "Español": {
        "nav_title": "Navegación",
        "nav_dashboard": "Portafolio Ejecutivo (YBP)",
        "nav_screener": "Screener de Oportunidades",
        "nav_apm": "Asset Performance Matrix (APM)",
        "nav_radar": "Radar MEXICAN",
        "nav_users": "Control de Accesos / Usuarios",
        
        "dash_overview": "Resumen del Portafolio",
        "dash_sub": "Análisis Estratégico de Yacimientos de Baja Permeabilidad (YBP)",
        "dash_filters": "FILTROS DEL PORTAFOLIO",
        "dash_area": "ÁREA CONTRACTUAL",
        "dash_sector": "SECTOR",
        "dash_tech_tab": "📊 VARIABLES TÉCNICAS",
        "dash_hier_tab": "🏆 JERARQUÍA",
        "dash_api": "GRAVEDAD API",
        "dash_shale_idx": "S.H.A.L.E.-Mx",
        "dash_mex_idx": "Índice MEXICAN",
        "dash_ranking_title": "🏆 Jerarquización de Oportunidades",
        
        "map_metric": "MÉTRICA DE VISUALIZACIÓN EN MAPA:",
        "map_res_equiv": "Reservas Equivalentes",
        "map_shale": "S.H.A.L.E.-Mx",
        "map_res_mmbls": "Reservas",
        
        "kpi_avg_imp": "PUNTUACIÓN IMP PROMEDIO",
        "kpi_top": "TOP TIER (IMP > 7.3)",
        "kpi_total": "TOTAL DE OPORTUNIDADES",
        "kpi_avg_api": "GRAVEDAD API PROMEDIO",
        
        "rank_empty": "No hay oportunidades disponibles para clasificar.",
        "rank_contractual_area": "Área Contractual:",
        "rank_sector": "Sector:",
        "rank_pending": "Análisis técnico pendiente",
        "rank_shale_integral": "🎯 Índice S.H.A.L.E.-Mx (Integral)",
        "rank_mexican_log": "📊 Índice MEXICAN (Logística)",
        "rank_shale_top": "Top oportunidades jerarquizadas por evaluación integral (Reservas, API, RGP e IMP)",
        "rank_mex_top": "Top oportunidades jerarquizadas por factibilidad logística (Infraestructura, Seguridad, Recursos)",
        
        "scr_title": "Screener de Oportunidades",
        "scr_desc": "Tabla dinámica de oportunidades. Use el selector para ordenar los campos de acuerdo a su estrategia de inversión.",
        "scr_dl": "Descargar CSV",
        "scr_sort_by": "Ordenar por:",
        "scr_all": "Todos",
        
        "rad_title": "Análisis Integrado MEXICAN",
        "rad_select": "Seleccione una Oportunidad a analizar:",
        "rad_err": "Oportunidad no encontrada.",
        "rad_multivariate": "Radar Multivariante",
        "rad_specs": "Especificaciones Geológicas y Técnicas",
        "rad_kpi_res": "EUR EQUIV. (MMBN)",
        "rad_kpi_gor": "RGP (pc/bn)",
        "rad_kpi_api": "GRAVEDAD API",
        "rad_kpi_depth": "PROF. (TVD)",
        "rad_kpi_capex": "CAPEX POZOS (MMUSD)",
        "rad_kpi_shale": "SCORE S.H.A.L.E.-Mx",
        "rad_fac_inf": "Infraestructura",
        "rad_fac_sec": "Seguridad",
        "rad_fac_lu": "Uso Suelo",
        "rad_fac_water": "Agua",
        "rad_fac_sand": "Arena",
        "rad_fac_pop": "Población",
        "rad_fac_roads": "Vías Acceso",
        "rad_method_title": "Contexto Metodológico",
        "rad_method_body": "El índice **M.E.X.I.C.A.N.** evalúa la viabilidad superficial y logística para el desarrollo de Yacimientos de Baja Permeabilidad. Se consideran factores críticos como la vulnerabilidad de las vías de acceso ante eventos climáticos, la disponibilidad de recursos hídricos para el fracturamiento hidráulico, y la cercanía a bancos de arena sílica (proppant). Las áreas con un **IMP superior a 7.30** presentan condiciones óptimas para la inversión inmediata debido a su proximidad a infraestructura consolidada y menores restricciones ambientales o sociales.",
        
        "Well Capex - Concept": "Capex Pozos Concepto MMUSD",
        "Well Capex - Pilot": "Capex Pozos Piloto MMUSD",
        "Well Capex - Development": "Capex Pozos Desarrollo MMUSD",
        "Well Capex - Total": "Capex Pozos Total MMUSD",
        
        "apm_title": "Asset Performance Matrix (APM)",
        "apm_desc": "Analice la relación entre las variables clave. El tamaño de cada burbuja es proporcional a su valor **S.H.A.L.E.-Mx**.",
        "apm_x": "Seleccione Eje X",
        "apm_y": "Seleccione Eje Y",
        "apm_total_cost": "CAPEX + OPEX + ABEX",
        "apm_res_oil": "Reserva de Petróleo",
        "apm_res_gas": "Reservas de Gas",
        
        "export_btn": "Exportar Reporte",
        "export_toast": "Generando reporte detallado...",
        
        "sidebar_mexican_title": "ℹ️ Sobre el Índice M.E.X.I.C.A.N.",
        "sidebar_mexican_content": "**M.E.X.I.C.A.N.** (Multicriteria Evaluation for X-fields Investment, Connectivity, & Assets Network) es una matriz de evaluación multivariante que analiza la viabilidad logística y superficial de los activos.",
        "sidebar_shale_title": "ℹ️ Sobre el Índice S.H.A.L.E.-Mx",
        "sidebar_shale_content": "**S.H.A.L.E.-Mx** (Strategic Hydrocarbon Assessment & Logistical Evaluation - México) evalúa la viabilidad operativa y logística junto con el potencial del subsuelo.",
    }
}

def get_text(key, default=None):
    lang = st.session_state.get('language', 'Español')
    res = translations.get(lang, translations['Español']).get(key, default if default else key)
    return res

def translate_columns(df):
    """Dynamically rename dataframe columns based on selected language and schema mapping."""
    from src.schema_manager import get_column_translations
    
    lang = st.session_state.get('language', 'Español')
    es_map, en_map = get_column_translations()
    
    if not es_map:
        return df # Fallback if schema not loaded
        
    mapping = es_map if lang == "Español" else en_map
    
    new_cols = []
    for c in df.columns:
        c_str = str(c).strip()
        # Direct match
        if c_str in mapping:
            new_cols.append(mapping[c_str])
        else:
            # Fuzzy match (database might have extra spaces or .1 from pandas)
            match = None
            c_clean = c_str.lower()
            for k, v in mapping.items():
                if len(str(k)) > 3 and str(k).lower() in c_clean:
                    match = v
                    break
            new_cols.append(match if match else c_str)
            
    # Deduplicate
    counts = {}
    unique_cols = []
    for col in new_cols:
        if col in counts:
            counts[col] += 1
            unique_cols.append(f"{col} ({counts[col]})")
        else:
            counts[col] = 0
            unique_cols.append(col)
            
    df.columns = unique_cols
    return df
