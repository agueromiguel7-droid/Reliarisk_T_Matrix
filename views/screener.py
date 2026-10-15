import streamlit as st
import pandas as pd
from src.i18n import get_text
from src.schema_manager import get_screener_schema, get_opportunity_key, get_column_translations

def render_screener(df):
    st.markdown(f"<div class='headline-md'>{get_text('scr_title')}</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='body-sm mb-8'>{get_text('scr_desc')}</div>", unsafe_allow_html=True)

    if df.empty:
        st.warning("No hay datos disponibles.")
        return

    # Sidebar Filters
    with st.sidebar:
        st.markdown(f"### {get_text('dash_filters')}")
        
        # Contractual Area - Use 'Area' internal key
        areas = ["All"] + sorted(df['Area'].unique().tolist()) if 'Area' in df.columns else ["All"]
        selected_area = st.selectbox(get_text('dash_area'), areas)
        
        # Sector - Use 'Sector' internal key
        sectors = ["All"] + sorted(df['Sector'].unique().tolist()) if 'Sector' in df.columns else ["All"]
        selected_sector = st.selectbox(get_text('dash_sector'), sectors)

    # Filter data
    mask = pd.Series([True] * len(df))
    if selected_area != "All":
        mask &= (df['Area'] == selected_area)
    if selected_sector != "All":
        mask &= (df['Sector'] == selected_sector)
        
    filtered_df = df[mask].copy()

    # Get dynamic schema
    schema = get_screener_schema()
    op_key = get_opportunity_key()
    
    if not schema:
        st.error("No se pudo cargar el esquema de agrupadores desde 'Encabezado Español-Ingles.xlsx'.")
        return

    # Info summary
    st.markdown(f"<div class='body-xs opacity-60 mb-4'>SHOWING {len(filtered_df)} RESULTS</div>", unsafe_allow_html=True)

    # Dynamic Tabs
    tab_titles = [s['group_name'] for s in schema]
    tabs = st.tabs(tab_titles)

    lang = st.session_state.get('language', 'Español')

    for i, group in enumerate(schema):
        with tabs[i]:
            # Always start with Opportunity
            cols_to_show = []
            rename_dict = {}
            
            # Find the actual column in filtered_df that represents Oportunidad
            # We look for the translated name or the source name
            op_display = "Oportunidad" if lang == 'Español' else "Opportunity"
            actual_op_col = next((c for c in filtered_df.columns if str(c).lower() == op_display.lower() or str(c).lower() == op_key.lower()), None)
            
            if actual_op_col:
                cols_to_show.append(actual_op_col)
                # No need to rename if already translated, but let's be safe
                rename_dict[actual_op_col] = op_display
            
            # Get column mappings for this group
            es_map, en_map = get_column_translations()
            mapping = es_map if lang == "Español" else en_map

            # Add the rest of the columns in the group
            for col_info in group['columns']:
                source_name = col_info['source']
                display_name = col_info['display'] # This is already in the target language from get_screener_schema
                
                # Skip if it's the opportunity key (already added)
                if source_name.lower() == op_key.lower():
                    continue
                
                # The column in filtered_df might be the source name OR the translated name
                # Let's check both
                translated_name = mapping.get(source_name, source_name)
                
                match = next((c for c in filtered_df.columns if str(c).strip() == translated_name.strip() or str(c).strip() == source_name.strip()), None)
                
                if match:
                    if match not in cols_to_show:
                        cols_to_show.append(match)
                        rename_dict[match] = display_name
            
            if cols_to_show:
                # Create a temporary DF with renamed columns for display
                display_df = filtered_df[cols_to_show].rename(columns=rename_dict)
                
                # Configure columns for better readability
                col_config = {}
                for col in display_df.columns:
                    if "advantage" in col.lower() or "ventaja" in col.lower() or "strategic" in col.lower():
                        col_config[col] = st.column_config.TextColumn(
                            col,
                            width=800, # Very wide
                            help=col
                        )
                    elif "opportunity" in col.lower() or "oportunidad" in col.lower():
                        col_config[col] = st.column_config.TextColumn(
                            col,
                            pinned=True,
                            width="medium"
                        )
                
                st.dataframe(
                    display_df, 
                    hide_index=True, 
                    use_container_width=True,
                    column_config=col_config
                )
            else:
                st.info("No hay columnas asignadas a este grupo en la base de datos.")
