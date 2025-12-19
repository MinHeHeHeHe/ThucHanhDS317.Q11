# app.py
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# Import page modules
from modules import tong_quan, chat_luong_du_lieu, khoa_hoc, gioi_thieu, ket_qua_phan_tich_du_doan
from modules.styles import get_main_css, get_header_css
from modules.theme_system import get_dynamic_css, get_theme_colors

# Load data via centralized module
from modules.data_loader import load_train_data, load_courses, load_clean_data

# Import course_dashboard
import course_dashboard as course_dashboard


# Page configuration
st.set_page_config(
    page_title="BI MOOCCubeX",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -----------------------------
# Global Styles & Fonts
# -----------------------------
st.markdown(
    """
    <link href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@24,400,0,0" rel="stylesheet">
    <style>
    .material-symbols-outlined {
        font-variation-settings: 'FILL' 1, 'wght' 400, 'GRAD' 0, 'opsz' 24;
        vertical-align: middle;
        display: inline-block;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# -----------------------------
# Read query params early
# -----------------------------
query_params = st.query_params
current_page_param = query_params.get("page", "dashboard")

# -----------------------------
# Init session state
# -----------------------------
st.session_state.setdefault("selected_course_id", None)
st.session_state.setdefault("current_user_id", None)

# current_view dùng trong course_dashboard: dashboard | user_list | user_detail
st.session_state.setdefault("current_view", "dashboard")

# -----------------------------
# Deep-link:
# - ?page=dashboard&course_id=C_xxx
# - ?page=dashboard&course_id=C_xxx&user_id=U_xxx
# -----------------------------
course_id_param = query_params.get("course_id", None)
user_id_param = query_params.get("user_id", None)

if course_id_param and current_page_param not in ["intro", "prediction_results"]:
    # Sync selected_course_id from URL
    if st.session_state.selected_course_id != course_id_param:
        st.session_state.selected_course_id = str(course_id_param)
        # ✅ RESET: Chỉ reset về dashboard khi thực sự đổi sang khóa học khác
        st.session_state.current_user_id = None
        st.session_state.current_view = "dashboard"
        st.session_state.course_detail_tabs = "📊 Course Dashboard"

    # Nếu có user_id trong URL -> đồng bộ vào state (Deep-link)
    if user_id_param:
        if st.session_state.current_user_id != user_id_param:
            st.session_state.current_user_id = str(user_id_param)
            st.session_state.current_view = "user_detail"
            st.session_state.course_detail_tabs = f"👤 User: {st.session_state.current_user_id}"
    else:
        # Nếu URL không có user_id nhưng state đang ở user_detail -> sync ngược lại (thoát user detail)
        if st.session_state.current_view == "user_detail":
            st.session_state.current_user_id = None
            st.session_state.current_view = "dashboard"
            st.session_state.course_detail_tabs = "📊 Course Dashboard"


# Sidebar navigation with enhanced styling
with st.sidebar:
    st.markdown("""
    <style>
        [data-testid="stSidebar"] {
            background: linear-gradient(180deg, #1a202c 0%, #0f1419 100%);
            box-shadow: 2px 0 20px rgba(0, 0, 0, 0.4);
        }

        .stRadio { margin-top: 20px; }
        .stRadio > div { gap: 8px; }

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

        .stRadio > div > label[data-baseweb="radio"] > div:first-child {
            display: none;
        }

        .stRadio > div > label > div:first-child {
            background: rgba(66, 153, 225, 0.1);
            border-radius: 8px;
            padding: 8px;
        }

        .stRadio label p {
            color: #e2e8f0;
            font-size: 22px;
            font-weight: 700;
            margin: 0;
        }

        .stRadio > div[role="radiogroup"] > label:has(input:checked) {
            background: linear-gradient(135deg, rgba(66, 153, 225, 0.15) 0%, rgba(72, 187, 120, 0.1) 100%);
            border-color: rgba(66, 153, 225, 0.4);
            box-shadow: 0 4px 12px rgba(66, 153, 225, 0.2);
        }
    </style>
    """, unsafe_allow_html=True)

    # If page=intro or prediction_results -> sidebar state none
    if current_page_param in ["intro", "prediction_results"]:
        st.session_state.main_selected_tab = None

    def on_sidebar_change():
        # Khi đổi tab sidebar -> quay lại dashboard
        st.query_params["page"] = "dashboard"

        # ✅ Nếu đang ở course dashboard -> thoát ra
        if st.session_state.get("selected_course_id") is not None:
            st.session_state.selected_course_id = None
            st.session_state.current_view = "dashboard"
            st.session_state.current_user_id = None
            st.session_state.course_detail_tabs = "📊 Course Dashboard"

            # Clear course_id/user_id in URL
            for k in ["course_id", "user_id"]:
                try:
                    if k in st.query_params:
                        del st.query_params[k]
                except Exception:
                    pass

    selected_tab = st.radio(
        "Navigation",
        ["📊 Tổng quan", "📈 Chất lượng dữ liệu", "📚 Khóa học"],
        label_visibility="collapsed",
        key="main_selected_tab",
        on_change=on_sidebar_change
    )


# -----------------------------
# Initialize theme in session state
# -----------------------------
if "theme" not in st.session_state:
    st.session_state.theme = st.query_params.get("theme", "Light")
else:
    if "theme" not in st.query_params or st.query_params["theme"] != st.session_state.theme:
        st.query_params["theme"] = st.session_state.theme

# Apply dynamic theme CSS
st.markdown(get_dynamic_css(st.session_state.theme), unsafe_allow_html=True)
st.markdown(get_main_css(st.session_state.theme), unsafe_allow_html=True)

# Load data
df_courses = load_courses()
df = load_train_data()

# Enhanced header with sticky positioning
header_bg = "#1a202c" if st.session_state.theme == "Dark" else "#ffffff"
header_border = "rgba(255, 255, 255, 0.1)" if st.session_state.theme == "Dark" else "rgba(0, 0, 0, 0.1)"
header_text_color = "#3182ce" if st.session_state.theme == "Dark" else "#000000"

st.markdown(f"""
<style>
    header[data-testid="stHeader"] {{ display: none; }}
    .sticky-header {{
        position: fixed; top: 0; left: 0; right: 0;
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
    #mainHeader h3 {{ color: {header_text_color} !important; }}
    #mainHeader a {{ color: {header_text_color} !important; }}
    #mainHeader a:hover {{ color: #3182ce !important; }}
    #mainHeader a::after {{ background-color: {header_text_color}; }}
</style>
""", unsafe_allow_html=True)

st.markdown(f"""
<style>
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
    .header-left {{
        position: absolute !important;
        left: 1rem !important;
        top: 50% !important;
        transform: translateY(-50%) !important;
        display: flex;
        align-items: center;
        z-index: 2;
    }}
    .header-title {{
        margin: 0 !important;
        font-size: 25px !important;
        font-weight: 700 !important;
        white-space: nowrap;
        line-height: 1.2 !important;
    }}
    .header-center {{
        z-index: 1;
        display: flex;
        gap: 20px;
        align-items: center;
    }}
    .sticky-header.scrolled .header-title {{
        font-size: 18px !important;
    }}
    .sticky-header a {{
        text-decoration: none !important;
        font-size: 22px !important;
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
    .sticky-header a:hover::after {{ width: 100%; }}
    .header-center a.active {{
        color: #3182ce !important;
        font-weight: 700 !important;
    }}
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
    #theme-btn-placeholder .stButton {{
        margin: 0 !important;
        padding: 0 !important;
        width: auto !important;
        border: none !important;
        position: static !important;
    }}
    .main .block-container {{ padding-top: 80px !important; }}
</style>

<div class="sticky-header" id="mainHeader">
    <div class="header-content">
        <div class="header-left">
            <a href="?page=dashboard&theme={st.session_state.theme}" target="_self">
                <div class="header-title" style="color: {header_text_color} !important;">📊 BI MOOCCubeX</div>
            </a>
        </div>
        <div class="header-center">
            <a href="?page=intro&theme={st.session_state.theme}" target="_self"
               class="{ 'active' if current_page_param == 'intro' else '' }"
               style="color: {header_text_color} !important;">Giới thiệu</a>
            <span style="color: {header_text_color}; opacity: 0.5;">|</span>
            <a href="?page=prediction_results&theme={st.session_state.theme}" target="_self"
               class="{ 'active' if current_page_param == 'prediction_results' else '' }"
               style="color: {header_text_color} !important;">Kết quả phân tích dự đoán</a>
        </div>
        <div id="theme-btn-placeholder"></div>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<script>
    (function() {
        const header = document.getElementById('mainHeader');
        function handleScroll() {
            const scrollTop = window.pageYOffset || document.documentElement.scrollTop;
            if (scrollTop > 50) header.classList.add('scrolled');
            else header.classList.remove('scrolled');
        }
        let scrollTimeout;
        window.addEventListener('scroll', function() {
            if (scrollTimeout) window.cancelAnimationFrame(scrollTimeout);
            scrollTimeout = window.requestAnimationFrame(handleScroll);
        }, { passive: true });
        handleScroll();
        setTimeout(handleScroll, 100);
        setTimeout(handleScroll, 500);
    })();

    function moveThemeToggle() {
        const headerPlaceholder = document.getElementById('theme-btn-placeholder');
        const buttons = window.parent.document.querySelectorAll('button');
        for (const btn of buttons) {
            if (btn.innerText.includes('☀️') || btn.innerText.includes('🌙')) {
                const container = btn.closest('.stButton');
                if (container && headerPlaceholder && !headerPlaceholder.contains(container)) {
                    headerPlaceholder.appendChild(container);
                }
                break;
            }
        }
    }
    setTimeout(moveThemeToggle, 100);
    setTimeout(moveThemeToggle, 500);
    setTimeout(moveThemeToggle, 1000);
    const observer = new MutationObserver(() => { moveThemeToggle(); });
    observer.observe(window.parent.document.body, { childList: true, subtree: true });
</script>
""", unsafe_allow_html=True)

# Theme toggle button logic
col_dummy, col_btn = st.columns([10, 1])
with col_btn:
    theme_icon = "☀️" if st.session_state.theme == "Dark" else "🌙"
    if st.button(theme_icon, key="theme_toggle_btn"):
        st.session_state.theme = "Light" if st.session_state.theme == "Dark" else "Dark"
        st.query_params["theme"] = st.session_state.theme
        st.rerun()

st.markdown("""
<style>
    div[data-testid="column"]:has(button[key="theme_toggle_btn"]) { display: none; }
</style>
""", unsafe_allow_html=True)

st.markdown("---")

theme = st.session_state.theme

# Main App Logic based on Page Param
if current_page_param == "intro":
    gioi_thieu.show(st.session_state.theme)

elif current_page_param == "prediction_results":
    ket_qua_phan_tich_du_doan.show(st.session_state.theme)

else:
    current_tab = st.session_state.main_selected_tab if st.session_state.main_selected_tab else "📊 Tổng quan"

    # ✅ Nếu selected_course_id tồn tại -> luôn show course_dashboard
    if st.session_state.selected_course_id is not None:
        course_dashboard.show()

    elif current_tab == "📊 Tổng quan":
        tong_quan.show(df, st.session_state.theme)

    elif current_tab == "📈 Chất lượng dữ liệu":
        chat_luong_du_lieu.show(load_clean_data(), st.session_state.theme)

    elif current_tab == "📚 Khóa học":
        khoa_hoc.show(df_courses, st.session_state.theme)
