# course_dashboard.py
import streamlit as st
import pandas as pd
from modules.data_loader import load_courses

from modules.course_view import display_course_dashboard
from modules.user_view import display_user_list, display_user_dashboard


def navigate_to_main_page():
    st.session_state.selected_course_id = None
    st.session_state.current_user_id = None
    st.session_state.current_view = "dashboard"
    st.session_state.course_detail_tabs = "📊 Course Dashboard"

    # clear URL but keep theme
    st.query_params["page"] = "dashboard"
    st.query_params["theme"] = st.session_state.get("theme", "Light")
    for k in ["course_id", "user_id", "view"]:
        if k in st.query_params:
            del st.query_params[k]
    


def _sync_state_from_url():
    # Sync course_id
    course_id_param = st.query_params.get("course_id", None)
    if course_id_param:
        st.session_state.selected_course_id = str(course_id_param)

    # Sync view (dashboard or user_list)
    view_param = st.query_params.get("view", None)
    
    # Sync user_id -> user_detail view
    user_id_param = st.query_params.get("user_id", None)
    if user_id_param:
        st.session_state.current_user_id = str(user_id_param)
        st.session_state.current_view = "user_detail"
        st.session_state.course_detail_tabs = f"👤 User: {st.session_state.current_user_id}"
    elif view_param:
        if view_param == "user_list":
            st.session_state.current_view = "user_list"
            st.session_state.course_detail_tabs = "👥 User List"
        else:
            st.session_state.current_view = "dashboard"
            st.session_state.course_detail_tabs = "📊 Course Dashboard"


def show():
    # init
    st.session_state.setdefault("current_view", "dashboard")
    st.session_state.setdefault("current_user_id", None)
    st.session_state.setdefault("course_detail_tabs", "📊 Course Dashboard")
    st.session_state.setdefault("user_page", 1)

    # ✅ sync theo URL
    _sync_state_from_url()

    COURSE_ID = st.session_state.get("selected_course_id")
    if not COURSE_ID:
        st.warning("⚠️ Vui lòng chọn một khóa học từ trang Tổng quan.")
        if st.button("Quay lại Tổng quan"):
            navigate_to_main_page()
            st.rerun()
        st.stop()

    df = load_courses().copy()
    df["class_start"] = pd.to_datetime(df.get("class_start", None), errors="coerce")
    df["class_end"] = pd.to_datetime(df.get("class_end", None), errors="coerce")

    course_data = df[df["course_id"] == COURSE_ID]
    if course_data.empty:
        st.error(f"Không tìm thấy dữ liệu cho Course ID: {COURSE_ID}")
        if st.button("Quay lại Tổng quan", key="back_main_err"):
            navigate_to_main_page()
            st.rerun()
        st.stop()

    course = course_data.iloc[0]

    # header
    st.button("⟨⟨", key="nav_back_main", on_click=navigate_to_main_page)
    st.markdown(f"<h1 style='margin-bottom: 0;'>Khóa học {course.get('course_name','-')}</h1>", unsafe_allow_html=True)
    st.markdown(f"<div style='font-size: 24px; font-weight: 500; margin-bottom: 5px;'>🏫 Được cung cấp bởi <b>{course.get('school_name','-')}</b></div>", unsafe_allow_html=True)
    st.markdown(f"<div style='font-size: 20px; color: #718096; margin-bottom: 10px;'>Course ID: <b>{COURSE_ID}</b></div>", unsafe_allow_html=True)
    st.markdown("---")

    # Tabs: luôn có 2 tab + tab user nếu đã chọn user
    tab_titles = ["📊 Course Dashboard", "👥 User List"]
    if st.session_state.current_user_id:
        tab_titles.append(f"👤 User: {st.session_state.current_user_id}")

    # bảo đảm tab hiện tại hợp lệ
    if st.session_state.course_detail_tabs not in tab_titles:
        st.session_state.course_detail_tabs = "📊 Course Dashboard"

    def on_tab_change():
        new_tab = st.session_state.course_detail_tabs
        if new_tab == "📊 Course Dashboard":
            st.session_state.current_view = "dashboard"
            st.session_state.current_user_id = None
            st.query_params["view"] = "dashboard"
            if "user_id" in st.query_params:
                del st.query_params["user_id"]
        elif new_tab == "👥 User List":
            st.session_state.current_view = "user_list"
            st.session_state.current_user_id = None
            st.query_params["view"] = "user_list"
            if "user_id" in st.query_params:
                del st.query_params["user_id"]
        elif new_tab.startswith("👤 User:"):
            st.session_state.current_view = "user_detail"
            if "view" in st.query_params:
                del st.query_params["view"]
            # user_id is already in session_state.current_user_id

    # Calculate the correct index for the radio button to ensure highlighting persists
    try:
        current_tab_index = tab_titles.index(st.session_state.course_detail_tabs)
    except (ValueError, KeyError):
        current_tab_index = 0

    active_tab = st.radio(
        "Chọn tab",
        tab_titles,
        index=current_tab_index,
        horizontal=True,
        label_visibility="collapsed",
        key="course_detail_tabs",
        on_change=on_tab_change
    )

    st.markdown("---")

    # render
    if st.session_state.current_view == "dashboard":
        display_course_dashboard(course, COURSE_ID)
    elif st.session_state.current_view == "user_list":
        display_user_list(COURSE_ID)
    elif st.session_state.current_view == "user_detail":
        display_user_dashboard(st.session_state.current_user_id)
