import streamlit as st

def apply_custom_styles():
    st.markdown("""
        <style>
        /* Import Fonts */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=Space+Grotesk:wght@400;500;700&display=swap');

        /* Global Variables based on DESIGN.md */
        :root {
            --primary: #012743;
            --primary-container: #1d3d5a;
            --surface-container-lowest: #ffffff;
            --surface-container-low: #f2f4f6;
            --surface: #f7f9fb;
            --surface-container-highest: #e0e3e5;
            --tertiary-fixed-dim: #00E5FF; /* Electric Cyan */
            --outline-variant: rgba(195, 199, 206, 0.15); /* 15% opacity */
            --text-primary: #1a1c1e;
            --text-secondary: #5e6368;
        }

        /* Base Typography */
        html, body, [class*="css"]  {
            font-family: 'Inter', sans-serif;
            color: var(--text-primary);
        }
        
        h1, h2, h3, h4, h5, h6, .display-font {
            font-family: 'Space Grotesk', sans-serif !important;
            color: var(--primary);
        }

        /* Streamlit Overrides */
        .stApp {
            background-color: var(--surface);
        }

        /* Sidebar Glassmorphism */
        [data-testid="stSidebar"] {
            background-color: rgba(242, 244, 246, 0.85) !important; /* surface-container-low */
            backdrop-filter: blur(10px);
            -webkit-backdrop-filter: blur(10px);
            border-right: none !important;
        }

        /* Cards and Containers - "No-Line" Rule */
        .card-lowest {
            background-color: var(--surface-container-lowest);
            border-radius: 12px;
            padding: 24px;
            margin-bottom: 24px;
            /* No solid border, just a subtle ambient shadow or ghost border */
            box-shadow: 0 4px 20px rgba(25, 28, 30, 0.03);
            border: 1px solid var(--outline-variant);
        }

        .card-low {
            background-color: var(--surface-container-low);
            border-radius: 12px;
            padding: 24px;
            margin-bottom: 24px;
            border: none;
        }
        
        .bento-cell {
            background-color: var(--surface-container-lowest);
            border-radius: 8px;
            padding: 16px;
            height: 100%;
            border: 1px solid var(--outline-variant);
            display: flex;
            flex-direction: column;
            justify-content: center;
        }

        /* Floating elements (ambient shadows) */
        .floating-element {
            box-shadow: 0 12px 40px rgba(25, 28, 30, 0.06);
            border: 1px solid var(--outline-variant);
        }

        /* Typography Hierarchy */
        .headline-lg {
            font-size: 3.5rem;
            font-family: 'Space Grotesk', sans-serif;
            font-weight: 700;
            line-height: 1.1;
            margin-bottom: 0.5rem;
        }
        
        .headline-md {
            font-size: 2rem;
            font-family: 'Space Grotesk', sans-serif;
            font-weight: 700;
        }

        .label-sm {
            font-size: 0.75rem;
            font-family: 'Inter', sans-serif;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            color: var(--text-secondary);
        }
        
        .body-sm {
            font-size: 0.875rem;
            font-family: 'Inter', sans-serif;
            color: var(--text-secondary);
        }

        /* Highlight/Focus */
        .highlight-cyan {
            color: var(--tertiary-fixed-dim);
            font-weight: 600;
        }
        
        /* Metric values */
        .metric-value {
            font-size: 2.5rem;
            font-weight: 700;
            font-family: 'Space Grotesk', sans-serif;
            color: var(--primary);
        }

        /* Input fields - Modern Wells */
        .stTextInput>div>div>input,
        .stSelectbox>div>div>div {
            background-color: var(--surface-container-highest) !important;
            border-radius: 0.25rem !important;
            border: none !important;
            border-bottom: 2px solid transparent !important;
            transition: all 0.2s ease;
        }
        
        .stTextInput>div>div>input:focus,
        .stSelectbox>div>div>div:focus-within {
            border-bottom: 2px solid var(--tertiary-fixed-dim) !important;
            box-shadow: none !important;
        }

        /* Buttons */
        .stButton>button {
            background: linear-gradient(135deg, var(--primary) 0%, var(--primary-container) 100%);
            color: white;
            border: none;
            border-radius: 0.5rem;
            font-family: 'Inter', sans-serif;
            font-weight: 500;
            padding: 0.5rem 1rem;
            transition: opacity 0.2s;
        }
        
        .stButton>button:hover {
            opacity: 0.9;
            color: white;
            border: none;
        }
        
        /* Stochastic Status Chips */
        .status-chip-pass {
            background-color: #dcedc8; /* tertiary_container approx */
            color: #33691e;
            padding: 4px 12px;
            border-radius: 16px;
            font-size: 0.875rem;
            font-weight: 600;
            display: inline-block;
        }
        
        .status-chip-fail {
            background-color: #ffcdd2; /* error_container approx */
            color: #b71c1c;
            padding: 4px 12px;
            border-radius: 16px;
            font-size: 0.875rem;
            font-weight: 600;
            display: inline-block;
        }
        
        /* Spacing utilities */
        .mt-4 { margin-top: 1rem; }
        .mb-4 { margin-bottom: 1rem; }
        .mt-8 { margin-top: 2rem; }
        .mb-8 { margin-bottom: 2rem; }
        
        /* Hide default Streamlit elements */
        header { visibility: hidden; }
        footer { visibility: hidden; }
        
        /* Dataframes */
        [data-testid="stDataFrame"] {
            border: none !important;
        }
        
        [data-testid="stDataFrame"] > div {
            border: none !important;
        }
        
        </style>
    """, unsafe_allow_html=True)
