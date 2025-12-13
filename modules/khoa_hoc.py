import streamlit as st
import pandas as pd
import os
from typing import Optional

from modules.data_loader import load_courses


def navigate_to_dashboard(course_id: str) -> None:
    """Sets session state to navigate to the specific course dashboard."""
    st.session_state.selected_course_id = course_id
    st.session_state.current_view = 'dashboard'
    st.session_state.current_user_id = None


def show(df: Optional[pd.DataFrame] = None) -> None:
    st.markdown("""
    <style>
        /* Tùy chỉnh nút xem chi tiết */
        .course-card-btn button {
            background: rgba(66, 153, 225, 0.1);
            color: #4299e1 !important;
            border: 1px solid #4299e1;
            border-radius: 50%;
            width: 40px;
            height: 40px;
            min-height: 40px;
            padding: 0;
            font-size: 1.2em;
            transition: all 0.3s ease;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
        }
        .course-card-btn button:hover {
            background: #4299e1;
            color: white !important;
            box-shadow: 0 6px 15px rgba(66, 153, 225, 0.5);
            transform: scale(1.05);
        }
        
        /* Đảm bảo tiêu đề khóa học nổi bật */
        .course-title {
            font-size: 24px !important;
            font-weight: 700 !important;
            margin-bottom: 0px;
            line-height: 1.2;
            /* Áp dụng gradient text từ styles.py */
            background: linear-gradient(135deg, #4299e1 0%, #48bb78 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }
        
        /* Hiển thị Course ID nổi bật */
        .course-id-label {
            color: #ed8936; /* Màu cam/vàng nhấn mạnh */
            font-size: 14px;
            font-weight: 600;
            margin-bottom: 5px;
            display: block;
        }
    </style>
    """, unsafe_allow_html=True)

    if 'khoa_current_page' not in st.session_state:
        st.session_state.khoa_current_page = 1
    if 'selected_course_id' not in st.session_state:
        st.session_state.selected_course_id = None

    try:
        if df is None:
            df = load_courses()
    except FileNotFoundError:
        st.error("Lỗi: Không tìm thấy file 'course_info_final.csv'.")
        st.stop()
    except Exception as e:
        st.error(f"Lỗi khi đọc file CSV: {e}")
        st.stop()

    st.title("Danh Sách Khóa Học")
    search_query = st.text_input(
        "🔍 Tìm kiếm khóa học bằng tên hoặc ID...",
        placeholder="Nhập ID hoặc tên khóa học..."
    )

    if search_query:
        # Reset về trang 1 khi bắt đầu search
        st.session_state.khoa_current_page = 1

        df_filtered = df[
            df['course_id'].astype(str).str.contains(search_query, case=False, na=False) |
            df['course_name'].str.contains(search_query, case=False, na=False)
        ]
    else:
        df_filtered = df.copy()

    PAGE_SIZE = 12
    total_courses = len(df_filtered)
    total_pages = (total_courses + PAGE_SIZE - 1) // PAGE_SIZE
    if total_pages == 0:
        total_pages = 1

    # clamp current page
    if st.session_state.khoa_current_page > total_pages:
        st.session_state.khoa_current_page = total_pages
    if st.session_state.khoa_current_page < 1:
        st.session_state.khoa_current_page = 1

    start_index = (st.session_state.khoa_current_page - 1) * PAGE_SIZE
    end_index = start_index + PAGE_SIZE
    courses_on_page = df_filtered.iloc[start_index:end_index].to_dict('records')

    st.markdown("---")

 # Grid display
    N_COLS = 3
    rows = [courses_on_page[i:i + N_COLS] for i in range(0, len(courses_on_page), N_COLS)]

    for row_idx, row in enumerate(rows):
        cols = st.columns(N_COLS)
        for i, course in enumerate(row):
            with cols[i]:
                with st.container(border=True):
                    col_id, col_btn = st.columns([4, 1])
                    with col_id:
                        st.markdown(f'<span class="course-id-label">{course["course_id"]}</span>', unsafe_allow_html=True)
                    with col_btn:
                        global_idx = start_index + row_idx * N_COLS + i
                        btn_key = f"khoa_open_{course['course_id']}_{global_idx}"
                        st.markdown('<div class="course-card-btn">', unsafe_allow_html=True)
                        st.button("↗", key=btn_key, help="Xem Dashboard Chi tiết",
                                  on_click=lambda cid=course['course_id']: navigate_to_dashboard(cid))
                        st.markdown('</div>', unsafe_allow_html=True)

                    # Tên Khóa học
                    st.markdown(f'<p class="course-title">{course["course_name"]}</p>', unsafe_allow_html=True)
                    
                    # Tên Trường học (Text Secondary Style)
                    st.markdown(f"*{course.get('school_name','') or 'N/A'}*", unsafe_allow_html=True)

                    st.markdown('<div style="margin-top: 10px; margin-bottom: 5px; border-top: 1px solid rgba(255, 255, 255, 0.05);"></div>', unsafe_allow_html=True)

                    # Hàng cuối: Thời gian và Số lượng Users
                    col_date, col_users = st.columns([2, 1])
                    with col_date:
                        # Thời gian
                        start = course.get('class_start','')
                        end = course.get('class_end','')
                        st.markdown(f"🗓️ **Thời gian:** {start} – {end}")

                    with col_users:
                        # Số lượng Users
                        try:
                            user_count_formatted = f"{int(course.get('user_count',0)):,.0f}".replace(",", ".")
                        except Exception:
                            user_count_formatted = course.get('user_count', 0)

                        st.markdown(
                            f"<div style='text-align: right; font-weight: 700; color: #48bb78; font-size: 1.1em;'>👥 {user_count_formatted}</div>",
                            unsafe_allow_html=True
                        )

        # --- Phần Phân trang ---
    def go_to_page(page_num):
        st.session_state.khoa_current_page = page_num

    # Tạo bố cục cho phần phân trang
    col_prev, col_pages, col_next = st.columns([1, 4, 1])

    with col_prev:
        # Nút "Prev"
        st.markdown('<div class="nav-btn-std">', unsafe_allow_html=True)
        st.button("⟨⟨", disabled=(st.session_state.khoa_current_page == 1),
                 on_click=lambda: go_to_page(st.session_state.khoa_current_page - 1))
        st.markdown('</div>', unsafe_allow_html=True)

    with col_next:
        # Nút "Next"
        st.button("⟩⟩", disabled=(st.session_state.khoa_current_page == total_pages or total_pages == 0),
                 on_click=lambda: go_to_page(st.session_state.khoa_current_page + 1))

    with col_pages:
        st.markdown(f"<div style='text-align: center; padding-top: 10px;'>Trang {st.session_state.khoa_current_page} / {total_pages}</div>", unsafe_allow_html=True)