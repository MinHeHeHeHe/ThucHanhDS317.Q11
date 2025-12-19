"""
Dynamic theme system for MOOCCubeX Dashboard
Provides comprehensive color schemes for light and dark themes
"""

def get_theme_colors(theme='Light'):
    """Return color scheme based on theme"""
    if theme == 'Dark':
        return {
            # Backgrounds
            'bg_primary': '#0a0e1a',
            'bg_secondary': '#1a202c',
            'bg_tertiary': '#2d3748',
            'bg_card': 'linear-gradient(135deg, #1e2530 0%, #2d3748 100%)',
            
            # Text
            'text_primary': '#ffffff',
            'text_secondary': '#a0aec0',
            'text_muted': '#718096',
            
            # Accents
            'accent_blue': '#4299e1',
            'accent_green': '#48bb78',
            'accent_orange': '#ed8936',
            'accent_red': '#f56565',
            
            # Chart colors
            'chart_bg': '#1a202c',
            'chart_grid': '#2d3748',
            'chart_text': '#ffffff',
            
            # Borders
            'border_color': 'rgba(255, 255, 255, 0.05)',
            'border_hover': 'rgba(66, 153, 225, 0.3)',
        }
    else:  # Light theme
        return {
            # Backgrounds
            'bg_primary': '#f7fafc',
            'bg_secondary': '#ffffff',
            'bg_tertiary': '#edf2f7',
            'bg_card': 'linear-gradient(135deg, #ffffff 0%, #f7fafc 100%)',
            
            # Text
            'text_primary': '#1a202c',
            'text_secondary': '#4a5568',
            'text_muted': '#718096',
            
            # Accents
            'accent_blue': '#3182ce',
            'accent_green': '#38a169',
            'accent_orange': '#dd6b20',
            'accent_red': '#e53e3e',
            
            # Chart colors
            'chart_bg': '#ffffff',
            'chart_grid': '#e2e8f0',
            'chart_text': '#1a202c',
            
            # Borders
            'border_color': 'rgba(0, 0, 0, 0.1)',
            'border_hover': 'rgba(49, 130, 206, 0.3)',
        }

def get_dynamic_css(theme='Light'):
    """Generate dynamic CSS based on theme"""
    colors = get_theme_colors(theme)
    
    return f"""
    <style>
        /* Global theme styles with smooth transitions */
        .stApp {{
            background: {colors['bg_primary']} !important;
            color: {colors['text_primary']} !important;
            transition: background 0.3s ease, color 0.3s ease;
        }}
        
        /* Sidebar theme */
        [data-testid="stSidebar"] {{
            background: {colors['bg_secondary']} !important;
            border-right: 1px solid {colors['border_color']};
        }}
        
        [data-testid="stSidebar"] .stRadio label p {{
            color: {colors['text_primary']} !important;
        }}
        
        /* Headers - Multiple selectors for maximum coverage */
        h1, h2, h3, h4, h5, h6 {{
            color: {colors['text_primary']} !important;
        }}
        
        /* Streamlit markdown headers */
        .stMarkdown h1, .stMarkdown h2, .stMarkdown h3, 
        .stMarkdown h4, .stMarkdown h5, .stMarkdown h6 {{
            color: {colors['text_primary']} !important;
        }}
        
        /* Section titles */
        div[data-testid="stMarkdownContainer"] h3 {{
            color: {colors['text_primary']} !important;
        }}
        
        /* All markdown elements */
        [data-testid="stMarkdownContainer"] * {{
            color: {colors['text_primary']} !important;
        }}
        
        /* Streamlit element container */
        .element-container h1, .element-container h2, .element-container h3,
        .element-container h4, .element-container h5, .element-container h6 {{
            color: {colors['text_primary']} !important;
        }}
        
        /* Metric cards */
        .metric-card {{
            background: {colors['bg_card']} !important;
            border: 1px solid {colors['border_color']};
            box-shadow: 0 4px 16px {'rgba(0, 0, 0, 0.3)' if theme == 'Dark' else 'rgba(0, 0, 0, 0.1)'};
        }}
        
        .metric-value {{
            color: {colors['text_primary']} !important;
        }}
        
        .metric-label {{
            color: {colors['text_secondary']} !important;
        }}
        
        /* Ranking table theme */
        .ranking-container {{
            background: {colors['bg_card']} !important;
            border: 1px solid {colors['border_color']};
        }}
        
        .ranking-table thead th {{
            color: {colors['text_secondary']} !important;
            border-bottom-color: {colors['border_hover']};
        }}
        
        .ranking-table tbody tr {{
            background: {colors['bg_tertiary']} !important;
        }}
        
        .ranking-table tbody tr:hover {{
            background: {'rgba(45, 55, 72, 0.8)' if theme == 'Dark' else 'rgba(237, 242, 247, 0.8)'} !important;
        }}
        
        .ranking-table tbody td {{
            color: {colors['text_primary']} !important;
            border-color: {colors['border_color']};
        }}
        
        .rank-number {{
            color: {colors['text_primary']} !important;
        }}
        
        .course-code {{
            color: {colors['accent_blue']} !important;
        }}
        
        /* Selectbox */
        .stSelectbox > div > div {{
            background: {colors['bg_tertiary']} !important;
            color: {colors['text_primary']} !important;
            border-color: {colors['border_color']} !important;
        }}
        
        /* Text inputs and other form elements */
        input, textarea, select {{
            background: {colors['bg_tertiary']} !important;
            color: {colors['text_primary']} !important;
            border-color: {colors['border_color']} !important;
        }}
        
        /* Plotly charts container */
        .js-plotly-plot {{
            background: {colors['chart_bg']} !important;
        }}
        
        /* Scrollbar */
        ::-webkit-scrollbar-track {{
            background: {colors['bg_secondary']};
        }}
        
        ::-webkit-scrollbar-thumb {{
            background: {colors['bg_tertiary']};
        }}
        
        /* Theme toggle button styling */
        .stButton > button {{
            background: {colors['bg_tertiary']} !important;
            color: {colors['text_primary']} !important;
            border: 2px solid {colors['border_hover']} !important;
            border-radius: 50%;
            width: 50px;
            height: 50px;
            font-size: 24px;
            transition: all 0.3s ease;
        }}
        
        .stButton > button:hover {{
            transform: rotate(180deg);
            box-shadow: 0 0 20px {colors['border_hover']};
        }}
    </style>
    """
