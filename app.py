import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# Import page modules
from modules import tong_quan, chat_luong_du_lieu, khoa_hoc
from modules.styles import get_main_css, get_header_css
from modules.theme_system import get_dynamic_css, get_theme_colors

# Load data via centralized module
from modules.data_loader import load_train_data, load_courses

# Import course_dashboard
import course_dashboard as course_dashboard 

# Page configuration
st.set_page_config(
    page_title="BI MOOCCubeX",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Sidebar navigation with enhanced styling
with st.sidebar:
    # Enhanced sidebar CSS
    st.markdown("""
    <style>
        [data-testid="stSidebar"] {
            background: linear-gradient(180deg, #1a202c 0%, #0f1419 100%);
            box-shadow: 2px 0 20px rgba(0, 0, 0, 0.4);
        }
        
        /* Radio button container */
        .stRadio {
            margin-top: 20px;
        }
        
        /* Individual radio items */
        .stRadio > div {
            gap: 8px;
        }
        
        .stRadio > div > label {
            background: transparent;
            padding: 16px 18px;
            border-radius: 12px;
            margin: 4px 0;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            border: 1px solid transparent;
            cursor: pointer;
            display: flex;
            align-items: center;
            gap: 12px;
        }
        
        .stRadio > div > label:hover {
            background: rgba(45, 55, 72, 0.6);
            border-color: rgba(66, 153, 225, 0.2);
            transform: translateX(4px);
        }
        
        /* Selected radio item */
        .stRadio > div > label[data-baseweb="radio"] > div:first-child {
            display: none;
        }
        
        /* Custom radio indicator */
        .stRadio > div > label > div:first-child {
            background: rgba(66, 153, 225, 0.1);
            border-radius: 8px;
            padding: 8px;
        }
        
        /* Text styling - LARGER FONT */
        .stRadio label p {
            color: #e2e8f0;
            font-size: 22px;
            font-weight: 700;
            margin: 0;
        }
        
        /* Active/Selected state */
        .stRadio > div[role="radiogroup"] > label:has(input:checked) {
            background: linear-gradient(135deg, rgba(66, 153, 225, 0.15) 0%, rgba(72, 187, 120, 0.1) 100%);
            border-color: rgba(66, 153, 225, 0.4);
            box-shadow: 0 4px 12px rgba(66, 153, 225, 0.2);
        }
    </style>
    """, unsafe_allow_html=True)
    
    # Navigation items with better icons
    selected_tab = st.radio(
        "Navigation",
        ["📊 Tổng quan", "📈 Chất lượng dữ liệu", "📚 Khóa học"],
        label_visibility="collapsed",
        key="main_selected_tab"
    )

    if ('selected_course_id' in st.session_state and st.session_state.selected_course_id is not None and 
        selected_tab != "📚 Khóa học"):
        st.session_state.selected_course_id = None
        if 'current_view' in st.session_state:
            del st.session_state.current_view
        if 'current_user_id' in st.session_state:
            st.session_state.current_user_id = None
        st.rerun()

if 'current_view' not in st.session_state:
    st.session_state.current_view = None
if 'selected_course_id' not in st.session_state:
    st.session_state.selected_course_id = None

# Initialize theme in session state
if 'theme' not in st.session_state:
    st.session_state.theme = 'Dark'

# Apply dynamic theme CSS
# Apply dynamic theme CSS
st.markdown(get_dynamic_css(st.session_state.theme), unsafe_allow_html=True)
st.markdown(get_main_css(st.session_state.theme), unsafe_allow_html=True)

# Load data
df_courses = load_courses()
df = load_train_data()

# Enhanced header with sticky positioning
header_bg = '#1a202c' if st.session_state.theme == 'Dark' else '#ffffff'
header_border = 'rgba(255, 255, 255, 0.1)' if st.session_state.theme == 'Dark' else 'rgba(0, 0, 0, 0.1)'
header_text_color = '#3182ce' if st.session_state.theme == 'Dark' else '#000000'

st.markdown(f"""
<style>
    /* Hide default Streamlit header */
    header[data-testid="stHeader"] {{
        display: none;
    }}
    
    /* Sticky header container */
    .sticky-header {{
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        z-index: 9999;
        background: {header_bg};
        padding: 1rem 2rem;
        border-bottom: 2px solid {header_border};
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
    }}
    
    .sticky-header.scrolled {{
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
        padding: 0.75rem 2rem;
    }}
    
    /* Dynamic Text Colors injected here using ID for specificity */
    #mainHeader h3 {{
        color: {header_text_color} !important;
        transition: color 0.3s ease;
    }}
    
    #mainHeader a {{
        color: {header_text_color} !important;
        transition: color 0.3s ease;
    }}
    
    #mainHeader a:hover {{
        color: #3182ce !important; /* Always blue on hover */
    }}
    
    #mainHeader a::after {{
        background-color: {header_text_color};
    }}
</style>
""", unsafe_allow_html=True)


st.markdown(f"""
<style>
    /* Header content wrapper - Relative anchor */
    .sticky-header .header-content {{
        position: relative !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        height: 100%;
        width: 100%;
        max-width: 1200px;
        margin: 0 auto;
        padding: 0 1rem;
    }}
    
    /* Left: Logo - Absolute Left */
    .header-left {{
        position: absolute !important;
        left: 1rem !important;
        top: 50% !important;
        transform: translateY(-50%) !important;
        display: flex;
        align-items: center;
        z-index: 2;
    }}
    
    /* Replaces older h3 selector */
    .header-title {{
        margin: 0 !important;
        font-size: 20px !important;
        font-weight: 700 !important;
        white-space: nowrap;
        transition: all 0.3s ease;
        line-height: 1.2 !important;
    }}
    
    /* Center: Link - Center in flow (or absolute center if desired) */
    .header-center {{
        z-index: 1;
    }}
    
    .sticky-header.scrolled .header-title {{
        font-size: 18px !important;
    }}
    
    .sticky-header a {{
        text-decoration: none !important;
        font-size: 16px !important;
        font-weight: 500 !important;
        white-space: nowrap;
        transition: all 0.3s ease;
        position: relative;
    }}
    
    .sticky-header a::after {{
        content: '';
        position: absolute;
        width: 0;
        height: 2px;
        bottom: -4px;
        left: 0;
        transition: width 0.3s ease;
    }}
    
    .sticky-header a:hover::after {{
        width: 100%;
    }}

    /* Right: Theme Button - Absolute Right */
    #theme-btn-placeholder {{
        position: absolute !important;
        right: 1rem !important;
        top: 50% !important;
        transform: translateY(-50%) !important;
        width: 45px !important;
        height: 45px !important;
        z-index: 3;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
    }}
    
    /* Styling for the moved button */
    #theme-btn-placeholder button {{
        background: transparent !important;
        border: 2px solid #3182ce !important;
        border-radius: 50% !important;
        width: 40px !important;
        height: 40px !important;
        min-height: 40px !important;
        font-size: 18px !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        padding: 0 !important;
        margin: 0 !important;
        color: inherit !important;
        box-shadow: none !important;
        line-height: 1 !important;
    }}
    
    #theme-btn-placeholder button:hover {{
        transform: rotate(180deg) !important;
        box-shadow: 0 0 15px rgba(49, 130, 206, 0.4) !important;
        background: rgba(49, 130, 206, 0.1) !important;
        border-color: #3182ce !important;
    }}

    /* Reset Streamlit container styles inside placeholder */
    #theme-btn-placeholder .stButton {{
        margin: 0 !important;
        padding: 0 !important;
        width: auto !important;
        border: none !important;
        position: static !important;
    }}
    
    /* Add padding to main content */
    .main .block-container {{
        padding-top: 80px !important;
    }}
</style>
<div class="sticky-header" id="mainHeader">
    <div class="header-content">
        <div class="header-left">
            <div class="header-title" style="color: {header_text_color} !important; transition: color 0.3s ease;">📊 BI MOOCCubeX</div>
        </div>
        <div class="header-center">
             <a href="#" style="color: {header_text_color} !important; transition: color 0.3s ease;">Kết quả phân tích dự đoán</a>
        </div>
        <div id="theme-btn-placeholder"></div>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<script>
    // Enhanced header scroll behavior
    (function() {
        const header = document.getElementById('mainHeader');
        
        function handleScroll() {
            const scrollTop = window.pageYOffset || document.documentElement.scrollTop;
            
            if (scrollTop > 50) {
                header.classList.add('scrolled');
            } else {
                header.classList.remove('scrolled');
            }
        }
        
        let scrollTimeout;
        window.addEventListener('scroll', function() {
            if (scrollTimeout) {
                window.cancelAnimationFrame(scrollTimeout);
            }
            scrollTimeout = window.requestAnimationFrame(handleScroll);
        }, { passive: true });
        
        handleScroll();
        setTimeout(handleScroll, 100);
        setTimeout(handleScroll, 500);
    })();

    // Function to move Streamlit button into header
    function moveThemeToggle() {
        const headerPlaceholder = document.getElementById('theme-btn-placeholder');
        const buttons = window.parent.document.querySelectorAll('button');
        
        for (const btn of buttons) {
            if (btn.innerText.includes('☀️') || btn.innerText.includes('🌙')) {
                const container = btn.closest('.stButton');
                if (container && headerPlaceholder && !headerPlaceholder.contains(container)) {
                    headerPlaceholder.appendChild(container);
                    console.log('Moved theme button to header');
                }
                break;
            }
        }
    }
    
    setTimeout(moveThemeToggle, 100);
    setTimeout(moveThemeToggle, 500);
    setTimeout(moveThemeToggle, 1000);
    
    const observer = new MutationObserver(() => {
        moveThemeToggle();
    });
    observer.observe(window.parent.document.body, { childList: true, subtree: true });
</script>
""", unsafe_allow_html=True)

# Theme toggle button logic
col_dummy, col_btn = st.columns([10, 1])
with col_btn:
    theme_icon = "☀️" if st.session_state.theme == "Dark" else "🌙"
    if st.button(theme_icon, key="theme_toggle_btn"):
        st.session_state.theme = "Light" if st.session_state.theme == "Dark" else "Dark"
        st.rerun()

# Hide original button location if needed (though JS moves it)
st.markdown("""
<style>
    div[data-testid="column"]:has(button[key="theme_toggle_btn"]) {
        display: none;
    }
</style>
""", unsafe_allow_html=True)

st.markdown("---")

# Get current theme
theme = st.session_state.theme

if 'selected_course_id' in st.session_state and st.session_state.selected_course_id is not None:
    course_dashboard.show()

elif st.session_state.main_selected_tab == "📊 Tổng quan":
    tong_quan.show(df, theme)
elif st.session_state.main_selected_tab == "📈 Chất lượng dữ liệu":
    chat_luong_du_lieu.show(df, theme)
elif st.session_state.main_selected_tab == "📚 Khóa học":
    khoa_hoc.show(df_courses)
