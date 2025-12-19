"""
CSS styles for the MOOCCubeX Dashboard
"""

from modules.theme_system import get_theme_colors

def get_main_css(theme='Light'):
    """Return main CSS for the dashboard"""
    colors = get_theme_colors(theme)
    
    return f"""
    <style>
        /* Global Styles */
        .stApp {{
            background: linear-gradient(135deg, {colors['bg_primary']} 0%, {colors['bg_secondary']} 100%);
            animation: gradientShift 15s ease infinite;
        }}
        
        @keyframes gradientShift {{
            0%, 100% {{ background-position: 0% 50%; }}
            50% {{ background-position: 100% 50%; }}
        }}
        
        /* Metric Cards with Premium Design */
        .metric-card {{
            background: {colors['bg_card']};
            padding: 24px;
            border-radius: 16px;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.4), 
                        0 0 0 1px {colors['border_color']};
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            position: relative;
            overflow: hidden;
        }}
        
        .metric-card::before {{
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 3px;
            background: linear-gradient(90deg, {colors['accent_blue']}, {colors['accent_green']}, {colors['accent_orange']});
            opacity: 0;
            transition: opacity 0.3s ease;
        }}
        
        .metric-card:hover {{
            transform: translateY(-4px);
            box-shadow: 0 12px 48px rgba(0, 0, 0, 0.5),
                        0 0 0 1px {colors['border_color']};
        }}
        
        .metric-card:hover::before {{
            opacity: 1;
        }}
        
        .metric-value {{
            font-size: 42px;
            font-weight: 700;
            color: {colors['text_primary']};
            text-shadow: 0 2px 8px rgba(0, 0, 0, 0.3);
            animation: fadeInUp 0.6s ease;
        }}
        
        .metric-label {{
            font-size: 16px;
            color: {colors['text_secondary']};
            margin-bottom: 8px;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            font-weight: 500;
        }}
        
        .metric-change {{
            font-size: 14px;
            margin-top: 8px;
            font-weight: 600;
            display: inline-flex;
            align-items: center;
            gap: 4px;
        }}
        
        .positive {{
            color: {colors['accent_green']};
            text-shadow: 0 0 10px rgba(72, 187, 120, 0.3);
        }}
        
        .negative {{
            color: {colors['accent_red']};
            text-shadow: 0 0 10px rgba(245, 101, 101, 0.3);
        }}
        
        /* Headers with Gradient */
        h1, h2, h3 {{
            color: {colors['text_primary']};
            font-weight: 700;
            background: linear-gradient(135deg, {colors['text_primary']} 0%, {colors['text_secondary']} 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }}
        
        /* DataFrames */
        .stDataFrame {{
            background-color: {colors['bg_secondary']};
            border-radius: 12px;
            overflow: hidden;
            box-shadow: 0 4px 16px rgba(0, 0, 0, 0.3);
        }}
        
        /* Plotly Charts Enhancement */
        .js-plotly-plot {{
            border-radius: 12px;
            overflow: hidden;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
            transition: transform 0.3s ease;
        }}
        
        .js-plotly-plot:hover {{
            transform: scale(1.01);
        }}
        
        /* Selectbox Styling */
        .stSelectbox > div > div {{
            background: {colors['bg_tertiary']};
            color: {colors['text_primary']};
            border: 1px solid {colors['border_hover']};
            border-radius: 10px;
            transition: all 0.3s ease;
        }}
        
        .stSelectbox > div > div:hover {{
            border-color: {colors['accent_blue']};
            box-shadow: 0 0 20px {colors['border_hover']};
        }}
        
        /* Dropdown Menu (Popover) Styling */
        /* Dropdown Menu (Popover) Styling */
        div[data-baseweb="popover"], div[data-baseweb="menu"] {{
            background-color: {colors['bg_secondary']} !important;
            border: 1px solid {colors['border_color']} !important;
        }}
        
        div[data-baseweb="menu"] ul {{
            background-color: {colors['bg_secondary']} !important;
        }}
        
        /* Target the list items and their internal div/content */
        li[role="option"] {{
            background-color: {colors['bg_secondary']} !important;
            color: {colors['text_primary']} !important;
        }}
        
        li[role="option"] div {{
            color: {colors['text_primary']} !important;
        }}
        
        /* Hover and Selected states */
        li[role="option"]:hover, li[role="option"][aria-selected="true"] {{
            background-color: {colors['bg_tertiary']} !important;
            color: {colors['accent_blue']} !important;
        }}
        
        li[role="option"]:hover div, li[role="option"][aria-selected="true"] div {{
            color: {colors['accent_blue']} !important;
        }}
        
        /* Animations */
        /* Animations */
        @keyframes fadeInUp {{
            from {{
                opacity: 0;
                transform: translateY(20px);
            }}
            to {{
                opacity: 1;
                transform: translateY(0);
            }}
        }}
        
        /* Scrollbar Styling */
        ::-webkit-scrollbar {{
            width: 8px;
            height: 8px;
        }}
        
        ::-webkit-scrollbar-track {{
            background: #1a202c;
        }}
        
        ::-webkit-scrollbar-thumb {{
            background: linear-gradient(180deg, #4299e1 0%, #2d3748 100%);
            border-radius: 4px;
        }}
        
        ::-webkit-scrollbar-thumb:hover {{
            background: linear-gradient(180deg, #5ab3f5 0%, #3d4758 100%);
        }}
        
        /* Loading Animation */
        .stSpinner > div {{
            border-color: #4299e1 transparent transparent transparent !important;
        }}
    </style>
    """

def get_header_css():
    """Return CSS for header section"""
    return """
    <style>
        .header-container {
            background: linear-gradient(135deg, rgba(30, 37, 48, 0.8) 0%, rgba(45, 55, 72, 0.6) 100%);
            padding: 20px 30px;
            border-radius: 16px;
            margin-bottom: 30px;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.05);
        }
        .header-title {
            font-size: 32px;
            font-weight: 700;
            background: linear-gradient(135deg, #4299e1 0%, #48bb78 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            display: inline-block;
        }
        .header-links {
            text-align: center;
        }
        .header-links a {
            color: #a0aec0;
            text-decoration: none;
            margin: 0 15px;
            font-size: 20px;
            transition: all 0.3s ease;
            position: relative;
        }
        .header-links a:hover {
            color: #4299e1;
        }
        .header-links a::after {
            content: '';
            position: absolute;
            bottom: -4px;
            left: 0;
            width: 0;
            height: 2px;
            background: linear-gradient(90deg, #4299e1, #48bb78);
            transition: width 0.3s ease;
        }
        .header-links a:hover::after {
            width: 100%;
        }
    </style>
    """
