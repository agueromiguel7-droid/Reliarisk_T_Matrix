import pandas as pd
import streamlit as st
import os

# Resolve relative to the project root (works locally and on Streamlit Cloud / Linux)
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MAPPING_PATH = os.path.join(PROJECT_ROOT, "Encabezado Español-Ingles.xlsx")

@st.cache_data
def load_schema():
    if not os.path.exists(MAPPING_PATH):
        return None
    
    try:
        # Load the mapping, row 1 is headers (N, Opportunity_0, etc.)
        # Skip the very first empty-ish row
        df = pd.read_excel(MAPPING_PATH, skiprows=1)
        df = df.dropna(axis=1, how='all')
        
        # We expect columns to be: [Español, Ingles, Agrupador Español, Agrupador Ingles]
        # But let's be safe and name them
        df.columns = ['es_header', 'en_header', 'es_group', 'en_group']
        
        # Clean up
        df['es_header'] = df['es_header'].astype(str).str.strip()
        df['en_header'] = df['en_header'].astype(str).str.strip()
        df['es_group'] = df['es_group'].astype(str).str.strip()
        df['en_group'] = df['en_group'].astype(str).str.strip()
        
        # Filter out the literal header row if it was included in data
        df = df[df['es_header'].str.lower() != 'español']
        df = df[df['en_header'].str.lower() != 'ingles']
        df = df[df['en_header'].str.lower() != 'english']
        return df
    except Exception as e:
        st.error(f"Error loading schema mapping: {e}")
        return None

def get_screener_schema():
    df = load_schema()
    if df is None:
        return []
    
    lang = st.session_state.get('language', 'Español')
    group_col = 'es_group' if lang == 'Español' else 'en_group'
    header_col = 'es_header' if lang == 'Español' else 'en_header'
    
    # Filter rows with groupings (avoiding 'nan' string from strip/astype)
    grouped_df = df[df[group_col].notna() & (df[group_col].astype(str).str.lower() != 'nan')].copy()
    
    # Unique groups in order of appearance
    groups = []
    seen = set()
    for g in grouped_df[group_col]:
        if g not in seen:
            groups.append(g)
            seen.add(g)
            
    schema = []
    for g in groups:
        cols = grouped_df[grouped_df[group_col] == g]
        # List of (Source Column Name, Display Header)
        # Source Column Name is 'en_header' because that's what's in the DB
        col_mappings = []
        for _, row in cols.iterrows():
            col_mappings.append({
                'source': row['en_header'],
                'display': row[header_col]
            })
        schema.append({
            'group_name': g,
            'columns': col_mappings
        })
        
    return schema

def get_column_translations():
    df = load_schema()
    if df is None:
        return {}, {}
        
    # Mapping from English (Source) to display based on language
    es_map = dict(zip(df['en_header'], df['es_header']))
    en_map = dict(zip(df['en_header'], df['en_header'])) # For English, use source name or English header
    
    # Actually, for English mode, use the 'en_header' column
    en_map = dict(zip(df['en_header'], df['en_header']))
    
    return es_map, en_map

def get_opportunity_key():
    df = load_schema()
    if df is None:
        return 'Opportunity'
    
    # Look for 'Opportunity' in 'en_header' that corresponds to 'Oportunidad' in 'es_header'
    # The user mentioned Oportunidad_1 -> Opportunity
    row = df[df['en_header'] == 'Opportunity']
    if not row.empty:
        return 'Opportunity'
    
    # Fallback: look for 'Oportunidad' in 'es_header'
    row = df[df['es_header'].str.contains('Oportunidad', case=False, na=False)]
    if not row.empty:
        return row.iloc[0]['en_header']
        
    return 'Opportunity'
