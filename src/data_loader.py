import pandas as pd
import streamlit as st
import os

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

@st.cache_data
def load_data(file_path=os.path.join(PROJECT_ROOT, 'Oportunidades Exploratoria YBP.xlsx')):
    if not os.path.exists(file_path):
        st.error(f"File {file_path} not found.")
        return None
        
    try:
        # Load the data. 
        try:
            df = pd.read_excel(file_path, header=1)
            if 'Oportunidad' not in df.columns and 'Opportunity' not in df.columns:
                df = pd.read_excel(file_path, header=0)
        except:
            df = pd.read_excel(file_path, header=0)
        
        # Load mapping for normalization
        from src.schema_manager import load_schema
        schema_df = load_schema()
        if schema_df is not None:
            norm_map = {}
            for _, row in schema_df.iterrows():
                en_name = str(row['en_header']).strip()
                es_name = str(row['es_header']).strip()
                
                # If DB doesn't have the English name but has the Spanish name, map it
                if en_name not in df.columns and es_name in df.columns:
                    norm_map[es_name] = en_name
            
            if norm_map:
                df = df.rename(columns=norm_map)

        # Clean column names (strip whitespace)
        df.columns = [str(c).strip() for c in df.columns]

        # Helper to find columns
        def find_col(keywords):
            if isinstance(keywords, str): keywords = [keywords]
            for k in keywords:
                match = next((c for c in df.columns if str(k).lower() == str(c).lower().strip()), None)
                if match: return match
            return None

        # Identification for calculations
        k_mex = find_col(['M.E.X.I.C.A.N.', 'IMP'])
        k_api = find_col(['API Gravity', '°API', 'API'])
        if not k_api:
            # Fallback for substrings
            api_cols = [c for c in df.columns if 'api' in str(c).lower()]
            if api_cols: k_api = api_cols[0]
        k_eur = find_col(['EUR equivalent (MMBN)'])
        k_rgo = find_col(['RGO (pc/Bn)', 'RGA'])
        k_area = find_col(['Contract Areas'])
        k_sector = find_col(['Sector'])
        k_lat = find_col(['Latitude (N)'])
        k_lon = find_col(['Length (W)'])
        k_ventaja = find_col(['Strategic Investor Advantage'])
        
        k_np = find_col(['NP (MMBN)', 'NP'])
        k_gp = find_col(['GP (MMMPC)', 'GP'])
        
        # Factors
        k_vias = find_col(['ID Onramp Vulnerability'])
        k_inf = find_col(['ID Proximity to Facilities'])
        k_sec = find_col(['ID Security'])
        k_lu = find_col(['ID Land Use Restrictions'])
        k_wat = find_col(['ID Water Availability'])
        k_arn = find_col(['ID Arena Availability'])
        k_pop = find_col(['ID Nearby Population Density'])

        k_total_cost = find_col(['CAPEX + OPEX + ABEX', 'Total_Cost_MMUSD'])
        
        # Create internal calculation columns (aliases)
        if k_mex: df['IMP_Score'] = pd.to_numeric(df[k_mex], errors='coerce').fillna(0)
        if k_api: df['Gravedad_API'] = pd.to_numeric(df[k_api], errors='coerce').fillna(0)
        if k_eur: df['Reserva_Equiv_MMBN'] = pd.to_numeric(df[k_eur], errors='coerce').fillna(0)
        if k_np: df['NP_MMBN'] = pd.to_numeric(df[k_np], errors='coerce').fillna(0)
        if k_gp: df['GP_MMMPC'] = pd.to_numeric(df[k_gp], errors='coerce').fillna(0)
        if k_rgo: df['RGP_pc_bn'] = pd.to_numeric(df[k_rgo], errors='coerce').fillna(0)
        if k_total_cost: df['Total_Cost'] = pd.to_numeric(df[k_total_cost], errors='coerce').fillna(0)
        
        # Keep calculation-friendly names for internal use in other modules
        if k_area: df['Area'] = df[k_area]
        if k_sector: df['Sector'] = df[k_sector]
        if k_lat: df['Latitud'] = df[k_lat]
        if k_lon: df['Longitud'] = df[k_lon]
        if k_ventaja: df['Ventaja_Estrategica'] = df[k_ventaja]
        
        if k_vias: df['Factor_Vias_Acceso'] = df[k_vias]
        if k_inf: df['Factor_Infraestructura'] = df[k_inf]
        if k_sec: df['Factor_Seguridad'] = df[k_sec]
        if k_lu: df['Factor_Uso_Suelo'] = df[k_lu]
        if k_wat: df['Factor_Agua'] = df[k_wat]
        if k_arn: df['Factor_Arena'] = df[k_arn]
        if k_pop: df['Factor_Poblacion'] = df[k_pop]
        
        # Opportunity key
        op_col = find_col(['Opportunity', 'Oportunidad'])
        if op_col:
            df['Oportunidad'] = df[op_col].astype(str).str.strip()
        else:
            df['Oportunidad'] = df.iloc[:, 1].astype(str).str.strip()

        # --- Calculate S.H.A.L.E.-Mx Index ---
        for c in ['Reserva_Equiv_MMBN', 'IMP_Score', 'Gravedad_API', 'RGP_pc_bn', 'Total_Cost']:
            if c in df.columns:
                df[c] = pd.to_numeric(df[c], errors='coerce').fillna(0)
            else:
                df[c] = 0.0

        max_res = df['Reserva_Equiv_MMBN'].max()
        max_imp = df['IMP_Score'].max()
        max_api = df['Gravedad_API'].max()
        max_rgp = df['RGP_pc_bn'].max()

        P_res, P_imp, P_api, P_rgp = 0.35, 0.30, 0.20, 0.15

        df['PTO_res'] = df['Reserva_Equiv_MMBN'] / max_res if max_res > 0 else 0
        df['PTO_imp'] = df['IMP_Score'] / max_imp if max_imp > 0 else 0
        df['PTO_api'] = df['Gravedad_API'] / max_api if max_api > 0 else 0
        df['PTO_rgp'] = df['RGP_pc_bn'] / max_rgp if max_rgp > 0 else 0

        num = (P_res * df['PTO_res']) + (P_api * df['PTO_api']) + 1
        den = (P_rgp * df['PTO_rgp']) + (P_imp * df['PTO_imp']) + 1
        df['SHALE_Mx'] = num / den
            
        return df
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return None

def get_mexican_factors(df, oportunidad_name):
    if df is None: return None
    row = df[df['Oportunidad'] == oportunidad_name]
    if row.empty: return None
    row = row.iloc[0]
    factors = {
        'infra': row.get('Factor_Infraestructura', 0),
        'security': row.get('Factor_Seguridad', 0),
        'land_use': row.get('Factor_Uso_Suelo', 0),
        'water': row.get('Factor_Agua', 0),
        'sand': row.get('Factor_Arena', 0),
        'roads': row.get('Factor_Vias_Acceso', 0),
        'pop': row.get('Factor_Poblacion', 0)
    }
    for k, v in factors.items():
        try: factors[k] = float(v)
        except: factors[k] = 0.0
    return factors
