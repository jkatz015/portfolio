"""
Custom CSS styles for D.A.T.A.
Dashboard & Analytics Tool for Accounting
Professional design system - V0 inspired light theme
"""

CUSTOM_CSS = """
<style>
    /* Google Fonts are loaded via <link> tag in streamlit_app.py for Railway compatibility */

    /* Root Variables - Light theme with teal accent */
    :root {
        --background: #f5f5f4;
        --background-card: #ffffff;
        --background-muted: #fafaf9;
        --foreground: #1c1917;
        --foreground-muted: #78716c;
        --foreground-subtle: #a8a29e;
        --primary: #0d9488;
        --primary-hover: #0f766e;
        --primary-light: #ccfbf1;
        --primary-bg: rgba(13, 148, 136, 0.1);
        --accent: #2dd4bf;
        --border: #e7e5e4;
        --border-hover: #d6d3d1;
        --success: #10b981;
        --danger: #e11d48;
        --shadow-sm: 0 1px 2px 0 rgb(0 0 0 / 0.05);
        --shadow: 0 1px 3px 0 rgb(0 0 0 / 0.1), 0 1px 2px -1px rgb(0 0 0 / 0.1);
        --shadow-lg: 0 10px 15px -3px rgb(0 0 0 / 0.1), 0 4px 6px -4px rgb(0 0 0 / 0.1);
        --radius: 0.5rem;
    }

    /* Global Styles */
    .stApp {
        background-color: var(--background) !important;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    }

    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stDeployButton {display: none;}

    /* Main container */
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 1200px;
    }

    /* Headers */
    h1 {
        font-family: 'Inter', sans-serif !important;
        font-weight: 700 !important;
        color: var(--foreground) !important;
        font-size: 2rem !important;
        letter-spacing: -0.025em !important;
        margin-bottom: 0 !important;
    }

    h2 {
        font-family: 'Inter', sans-serif !important;
        font-weight: 600 !important;
        color: var(--primary) !important;
        font-size: 1.125rem !important;
        margin-top: 1.5rem !important;
        margin-bottom: 1rem !important;
    }

    h3 {
        font-family: 'Inter', sans-serif !important;
        font-weight: 600 !important;
        color: var(--foreground) !important;
        font-size: 1rem !important;
    }

    /* Tagline/subtitle */
    .tagline {
        font-size: 0.875rem;
        color: var(--foreground-muted);
        margin-top: 0.25rem;
    }

    /* Logo container */
    .logo-container {
        display: flex;
        align-items: center;
        gap: 0.75rem;
        margin-bottom: 1.5rem;
    }

    .logo-icon {
        width: 2.5rem;
        height: 2.5rem;
        border-radius: 0.5rem;
        background-color: var(--primary-bg);
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.25rem;
    }

    /* Status badge */
    .status-badge {
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
        padding: 0.375rem 0.75rem;
        background-color: var(--primary-light);
        border: 1px solid var(--accent);
        border-radius: 9999px;
        font-size: 0.75rem;
        color: var(--primary);
        font-weight: 500;
    }

    .status-dot {
        width: 0.5rem;
        height: 0.5rem;
        border-radius: 50%;
        background-color: var(--primary);
        animation: pulse 2s infinite;
    }

    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.5; }
    }

    /* Cards */
    .card {
        background: var(--background-card);
        border-radius: var(--radius);
        padding: 1.5rem;
        box-shadow: var(--shadow-sm);
        border: 1px solid var(--border);
        margin-bottom: 1rem;
    }

    .card-muted {
        background: linear-gradient(to bottom right, var(--background-card), #f1f5f9);
    }

    .card-teal {
        background: rgba(204, 251, 241, 0.3);
    }

    .card-amber {
        background: rgba(254, 243, 199, 0.3);
    }

    .card-cyan {
        background: rgba(207, 250, 254, 0.4);
    }

    /* KPI Cards */
    .kpi-card {
        background: linear-gradient(to bottom right, var(--background-card), #f1f5f9);
        border-radius: var(--radius);
        padding: 1.25rem;
        box-shadow: var(--shadow-sm);
        border: 1px solid var(--border);
    }

    .kpi-label {
        font-size: 0.875rem;
        color: var(--foreground-muted);
        margin-bottom: 0.25rem;
    }

    .kpi-value {
        font-family: 'Inter', sans-serif;
        font-size: 1.5rem;
        font-weight: 700;
        color: var(--foreground);
    }

    .kpi-value-mono {
        font-family: 'JetBrains Mono', monospace;
    }

    .kpi-change {
        display: flex;
        align-items: center;
        gap: 0.25rem;
        margin-top: 0.5rem;
        font-size: 0.875rem;
    }

    .kpi-change-positive {
        color: var(--success);
    }

    .kpi-change-negative {
        color: var(--danger);
    }

    /* Streamlit metric overrides */
    [data-testid="stMetricValue"] {
        font-family: 'Inter', sans-serif !important;
        font-size: 1.5rem !important;
        font-weight: 700 !important;
        color: var(--foreground) !important;
    }

    [data-testid="stMetricLabel"] {
        font-size: 0.875rem !important;
        color: var(--foreground-muted) !important;
    }

    [data-testid="stMetricDelta"] svg {
        display: none;
    }

    /* File uploader */
    [data-testid="stFileUploader"] {
        background: var(--background-muted);
        border: 2px dashed var(--border);
        border-radius: var(--radius);
        padding: 2rem;
        transition: all 0.2s;
    }

    [data-testid="stFileUploader"]:hover {
        border-color: var(--primary);
        background: var(--primary-light);
    }

    [data-testid="stFileUploader"] section {
        padding: 0 !important;
    }

    /* Buttons */
    .stButton > button {
        background-color: var(--primary) !important;
        color: white !important;
        font-family: 'Inter', sans-serif !important;
        font-weight: 600 !important;
        padding: 0.625rem 1.25rem !important;
        border-radius: var(--radius) !important;
        border: none !important;
        transition: background-color 0.2s !important;
        box-shadow: var(--shadow-sm) !important;
    }

    .stButton > button:hover {
        background-color: var(--primary-hover) !important;
    }

    .stDownloadButton > button {
        background-color: transparent !important;
        color: var(--foreground) !important;
        font-family: 'Inter', sans-serif !important;
        font-weight: 500 !important;
        padding: 0.625rem 1.25rem !important;
        border-radius: var(--radius) !important;
        border: 1px solid var(--border) !important;
        transition: all 0.2s !important;
    }

    .stDownloadButton > button:hover {
        background-color: var(--background-muted) !important;
        border-color: var(--border-hover) !important;
    }

    /* Select boxes */
    .stSelectbox > div > div {
        background-color: var(--background-muted) !important;
        border: 1px solid var(--border) !important;
        border-radius: var(--radius) !important;
    }

    .stSelectbox > div > div:focus-within {
        border-color: var(--primary) !important;
        box-shadow: 0 0 0 1px var(--primary) !important;
    }

    .stSelectbox label {
        font-size: 0.875rem !important;
        color: var(--foreground) !important;
        font-weight: 500 !important;
    }

    /* Text input */
    .stTextInput > div > div > input {
        font-family: 'Inter', sans-serif !important;
        background-color: var(--background-muted) !important;
        border: 1px solid var(--border) !important;
        border-radius: var(--radius) !important;
        padding: 0.625rem 0.875rem !important;
        color: var(--foreground) !important;
    }

    .stTextInput > div > div > input:focus {
        border-color: var(--primary) !important;
        box-shadow: 0 0 0 1px var(--primary) !important;
    }

    .stTextInput > div > div > input::placeholder {
        color: var(--foreground-subtle) !important;
    }

    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 0 !important;
        border-bottom: 1px solid var(--border);
        background-color: transparent !important;
    }

    .stTabs [data-baseweb="tab"] {
        font-family: 'Inter', sans-serif !important;
        font-weight: 500 !important;
        font-size: 0.875rem !important;
        color: var(--foreground-muted) !important;
        padding: 0.75rem 1rem !important;
        border-bottom: 2px solid transparent !important;
        background-color: transparent !important;
        transition: all 0.2s !important;
    }

    .stTabs [data-baseweb="tab"]:hover {
        color: var(--foreground) !important;
    }

    .stTabs [aria-selected="true"] {
        color: var(--primary) !important;
        border-bottom-color: var(--primary) !important;
        background-color: transparent !important;
    }

    /* Expander */
    .streamlit-expanderHeader {
        font-family: 'Inter', sans-serif !important;
        font-weight: 500 !important;
        color: var(--foreground) !important;
        background-color: var(--background-card) !important;
        border-radius: var(--radius) !important;
    }

    /* Data preview table */
    .stDataFrame {
        border-radius: var(--radius) !important;
        overflow: hidden !important;
    }

    /* Success/Error messages */
    .stSuccess {
        background-color: rgba(16, 185, 129, 0.1) !important;
        border-left: 4px solid var(--success) !important;
        border-radius: 0 var(--radius) var(--radius) 0 !important;
        color: var(--foreground) !important;
    }

    .stError {
        background-color: rgba(225, 29, 72, 0.1) !important;
        border-left: 4px solid var(--danger) !important;
        border-radius: 0 var(--radius) var(--radius) 0 !important;
    }

    .stInfo {
        background-color: rgba(13, 148, 136, 0.1) !important;
        border-left: 4px solid var(--primary) !important;
        border-radius: 0 var(--radius) var(--radius) 0 !important;
    }

    /* Spinner */
    .stSpinner > div {
        border-top-color: var(--primary) !important;
    }

    /* Divider */
    hr {
        border-color: var(--border) !important;
        margin: 1.5rem 0 !important;
    }

    /* Footer */
    .footer {
        text-align: center;
        padding: 1.5rem 0;
        color: var(--foreground-muted);
        font-size: 0.875rem;
        border-top: 1px solid var(--border);
        margin-top: 2rem;
    }

    .footer a {
        color: var(--primary);
        text-decoration: none;
        font-weight: 500;
    }

    .footer a:hover {
        text-decoration: underline;
    }

    /* Login card */
    .login-card {
        max-width: 28rem;
        margin: 0 auto;
        background: rgba(204, 251, 241, 0.5);
        border: 1px solid var(--border);
        border-radius: var(--radius);
        padding: 2rem;
        box-shadow: var(--shadow-lg);
    }

    /* Slider */
    .stSlider > div > div > div {
        background-color: var(--primary) !important;
    }

    /* Radio buttons */
    .stRadio > div {
        gap: 0.5rem !important;
    }

    .stRadio label {
        font-size: 0.875rem !important;
        color: var(--foreground) !important;
    }

    /* Column gaps */
    [data-testid="column"] {
        padding: 0 0.5rem;
    }
</style>
"""

# Color constants for Plotly charts - matching V0 theme
CHART_COLORS = {
    'primary': '#0d9488',
    'primary_light': '#14b8a6',
    'accent': '#2dd4bf',
    'success': '#10b981',
    'danger': '#e11d48',
    'purple': '#a78bfa',
    'pink': '#f472b6',
    'amber': '#fbbf24',
    'cyan': '#22d3ee',
    'gray_100': '#f5f5f4',
    'gray_200': '#e7e5e4',
    'gray_300': '#d6d3d1',
    'gray_400': '#a8a29e',
    'gray_500': '#78716c',
    'gray_900': '#1c1917',
}

# Sequential color palette for charts
CHART_PALETTE = [
    '#0d9488',  # Teal (primary)
    '#22d3ee',  # Cyan
    '#a78bfa',  # Purple
    '#f472b6',  # Pink
    '#fbbf24',  # Amber
    '#10b981',  # Emerald
    '#6366f1',  # Indigo
    '#ef4444',  # Red
]

# Plotly layout template - light theme
PLOTLY_LAYOUT = {
    'font': {
        'family': 'Inter, -apple-system, BlinkMacSystemFont, sans-serif',
        'color': '#1c1917',
        'size': 12,
    },
    'paper_bgcolor': 'rgba(0,0,0,0)',
    'plot_bgcolor': 'rgba(0,0,0,0)',
    'margin': {'t': 40, 'b': 40, 'l': 40, 'r': 30},
    'title': {
        'font': {'size': 14, 'color': '#1c1917', 'weight': 600},
        'x': 0,
        'xanchor': 'left',
    },
    'xaxis': {
        'gridcolor': '#e7e5e4',
        'linecolor': '#e7e5e4',
        'tickfont': {'size': 11, 'color': '#78716c'},
        'showgrid': True,
        'gridwidth': 1,
    },
    'yaxis': {
        'gridcolor': '#e7e5e4',
        'linecolor': '#e7e5e4',
        'tickfont': {'size': 11, 'color': '#78716c'},
        'showgrid': True,
        'gridwidth': 1,
    },
    'legend': {
        'bgcolor': 'rgba(255,255,255,0.8)',
        'bordercolor': '#e7e5e4',
        'borderwidth': 1,
        'font': {'size': 11},
    },
    'hoverlabel': {
        'bgcolor': '#ffffff',
        'bordercolor': '#e7e5e4',
        'font': {'family': 'Inter', 'size': 12, 'color': '#1c1917'},
    },
}
