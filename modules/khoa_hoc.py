import streamlit as st
import pandas as pd
from typing import Optional

from modules.data_loader import load_courses
from modules.theme_system import get_theme_colors


def navigate_to_dashboard(course_id: str) -> None:
    """Sets session state to navigate to the specific course dashboard."""
    st.session_state.selected_course_id = course_id
    st.session_state.current_view = "dashboard"
    st.session_state.current_user_id = None


def show(df: Optional[pd.DataFrame] = None, theme: str = "Dark") -> None:
    colors = get_theme_colors(theme)

    # ===== Theme tokens for button + tooltip + card =====
    if theme == "Light":
        btn_bg = "#ffffff"
        btn_color = "#000000"
        btn_border = "#e2e8f0"
        btn_hover_bg = "#edf2f7"
        btn_hover_color = "#000000"
        btn_shadow = "0 6px 16px rgba(0,0,0,0.10)"

        tip_bg = "#ffffff"
        tip_color = "#000000"
        tip_border = "#e2e8f0"
        tip_shadow = "0 10px 24px rgba(0,0,0,0.12)"

        card_border = "rgba(0,0,0,0.35)"
        card_bg = "rgba(255,255,255,0.98)"
        card_shadow = "0 10px 24px rgba(0,0,0,0.10)"
    else:
        btn_bg = "rgba(66, 153, 225, 0.10)"
        btn_color = colors["accent_blue"]  # #4299e1
        btn_border = "rgba(66, 153, 225, 0.45)"
        btn_hover_bg = colors["accent_blue"]
        btn_hover_color = "#ffffff"
        btn_shadow = "0 8px 20px rgba(0,0,0,0.28)"

        tip_bg = "#111827"
        tip_color = "#ffffff"
        tip_border = "rgba(255,255,255,0.14)"
        tip_shadow = "0 14px 30px rgba(0,0,0,0.38)"

        card_border = "rgba(255,255,255,0.12)"
        card_bg = "linear-gradient(180deg, #0b1220 0%, #0a0f1a 100%)"
        card_shadow = "0 10px 28px rgba(0,0,0,0.45)"

    st.markdown(
        f"""
        <style>
        :root {{
            --cd-btn-bg: {btn_bg};
            --cd-btn-color: {btn_color};
            --cd-btn-border: {btn_border};
            --cd-btn-hover-bg: {btn_hover_bg};
            --cd-btn-hover-color: {btn_hover_color};
            --cd-btn-shadow: {btn_shadow};

            --cd-tip-bg: {tip_bg};
            --cd-tip-color: {tip_color};
            --cd-tip-border: {tip_border};
            --cd-tip-shadow: {tip_shadow};

            --cd-card-border: {card_border};
            --cd-card-bg: {card_bg};
            --cd-card-shadow: {card_shadow};
        }}

        /* ====== Course cards (ONLY those tagged by JS with .course-card) ====== */
        div[data-testid="stContainer"].course-card {{
            border-radius: 12px !important;
        }}
        div[data-testid="stContainer"].course-card > div {{
            border: 2px solid var(--cd-card-border) !important;
            background: var(--cd-card-bg) !important;
            box-shadow: var(--cd-card-shadow) !important;
            border-radius: 12px !important;
        }}

        /* ====== Style ONLY buttons tagged by JS: .course-detail-btn ====== */
        button.course-detail-btn {{
            background: var(--cd-btn-bg) !important;
            background-color: var(--cd-btn-bg) !important;
            border: 1px solid var(--cd-btn-border) !important;
            border-radius: 999px !important;
            width: 34px !important;
            height: 34px !important;
            min-height: 34px !important;
            padding: 0 !important;

            box-shadow: var(--cd-btn-shadow) !important;
            transition: transform .15s ease, box-shadow .15s ease, background-color .15s ease !important;

            position: relative !important;
            display: inline-flex !important;
            align-items: center !important;
            justify-content: center !important;
            line-height: 1 !important;
        }}

        button.course-detail-btn,
        button.course-detail-btn * {{
            color: var(--cd-btn-color) !important;
            fill: var(--cd-btn-color) !important;
            stroke: var(--cd-btn-color) !important;
        }}

        button.course-detail-btn:hover {{
            background: var(--cd-btn-hover-bg) !important;
            background-color: var(--cd-btn-hover-bg) !important;
            transform: translateY(-1px) scale(1.03) !important;
        }}

        button.course-detail-btn:hover,
        button.course-detail-btn:hover * {{
            color: var(--cd-btn-hover-color) !important;
            fill: var(--cd-btn-hover-color) !important;
            stroke: var(--cd-btn-hover-color) !important;
        }}

        /* ====== Custom tooltip from data-tooltip ====== */
        button.course-detail-btn::after {{
            content: attr(data-tooltip);
            position: absolute;
            top: -44px;
            left: 50%;
            transform: translateX(-50%);
            background: var(--cd-tip-bg);
            color: var(--cd-tip-color);
            border: 1px solid var(--cd-tip-border);
            box-shadow: var(--cd-tip-shadow);
            padding: 7px 10px;
            border-radius: 10px;
            font-size: 12px;
            font-weight: 600;
            white-space: nowrap;
            opacity: 0;
            pointer-events: none;
            transition: opacity .12s ease, transform .12s ease;
            z-index: 999999;
        }}

        button.course-detail-btn::before {{
            content: "";
            position: absolute;
            top: -12px;
            left: 50%;
            transform: translateX(-50%);
            border-width: 7px;
            border-style: solid;
            border-color: var(--cd-tip-bg) transparent transparent transparent;
            opacity: 0;
            pointer-events: none;
            transition: opacity .12s ease;
            z-index: 999999;
        }}

        button.course-detail-btn:hover::after {{
            opacity: 1;
            transform: translateX(-50%) translateY(-2px);
        }}
        button.course-detail-btn:hover::before {{
            opacity: 1;
        }}

        /* ====== Course title + id label ====== */
        .course-title {{
            font-size: 24px !important;
            font-weight: 700 !important;
            margin-bottom: 0px;
            line-height: 1.2;
            background: linear-gradient(135deg, #4299e1 0%, #48bb78 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }}

        .course-id-label {{
            color: #ed8936;
            font-size: 14px;
            font-weight: 600;
            margin-bottom: 5px;
            display: block;
        }}

        /* ====== Pagination: center 2 buttons + center text ====== */
        div[data-testid="stColumn"]:has(.page-prev-marker) div[data-testid="stButton"] {{
            display: flex !important;
            justify-content: center !important;
        }}
        div[data-testid="stColumn"]:has(.page-next-marker) div[data-testid="stButton"] {{
            display: flex !important;
            justify-content: center !important;
        }}
        div[data-testid="stColumn"]:has(.page-text-marker) {{
            display: flex !important;
            justify-content: center !important;
        }}
        </style>

        <script>
        (function() {{
            function tagCourseDetailButtonsAndCards() {{
                const root = window.parent.document;
                const btns = root.querySelectorAll('button');

                btns.forEach(b => {{
                    const t = (b.innerText || '').trim();
                    if (t === '↗') {{
                        // Tag button
                        b.classList.add('course-detail-btn');
                        b.setAttribute('data-tooltip', 'Xem Dashboard Chi tiết');
                        b.removeAttribute('title');
                        b.removeAttribute('aria-describedby');

                        // Tag ONLY the nearest course card container (avoid outer border)
                        const card = b.closest('div[data-testid="stContainer"]');
                        if (card) card.classList.add('course-card');
                    }}
                }});
            }}

            setTimeout(tagCourseDetailButtonsAndCards, 50);
            setTimeout(tagCourseDetailButtonsAndCards, 250);
            setTimeout(tagCourseDetailButtonsAndCards, 700);

            const obs = new MutationObserver(() => tagCourseDetailButtonsAndCards());
            obs.observe(window.parent.document.body, {{ childList: true, subtree: true }});
        }})();
        </script>
        """,
        unsafe_allow_html=True,
    )

    # ===== Session state =====
    if "khoa_current_page" not in st.session_state:
        st.session_state.khoa_current_page = 1
    if "selected_course_id" not in st.session_state:
        st.session_state.selected_course_id = None

    # ===== Load data =====
    try:
        if df is None:
            df = load_courses()
    except FileNotFoundError:
        st.error("Lỗi: Không tìm thấy file 'course_info_final.csv'.")
        st.stop()
    except Exception as e:
        st.error(f"Lỗi khi đọc file CSV: {e}")
        st.stop()

    # ===== UI =====
    st.title("Danh Sách Khóa Học")
    search_query = st.text_input(
        "🔍 Tìm kiếm khóa học bằng tên hoặc ID...",
        placeholder="Nhập ID hoặc tên khóa học...",
    )

    if search_query:
        st.session_state.khoa_current_page = 1
        df_filtered = df[
            df["course_id"].astype(str).str.contains(search_query, case=False, na=False)
            | df["course_name"].str.contains(search_query, case=False, na=False)
        ]
    else:
        df_filtered = df.copy()

    PAGE_SIZE = 12
    total_courses = len(df_filtered)
    total_pages = (total_courses + PAGE_SIZE - 1) // PAGE_SIZE
    if total_pages == 0:
        total_pages = 1

    if st.session_state.khoa_current_page > total_pages:
        st.session_state.khoa_current_page = total_pages
    if st.session_state.khoa_current_page < 1:
        st.session_state.khoa_current_page = 1

    start_index = (st.session_state.khoa_current_page - 1) * PAGE_SIZE
    end_index = start_index + PAGE_SIZE
    courses_on_page = df_filtered.iloc[start_index:end_index].to_dict("records")

    st.markdown("---")

    # Grid display
    N_COLS = 3
    rows = [courses_on_page[i : i + N_COLS] for i in range(0, len(courses_on_page), N_COLS)]

    for row_idx, row in enumerate(rows):
        cols = st.columns(N_COLS)
        for i, course in enumerate(row):
            with cols[i]:
                with st.container(border=True):
                    col_id, col_btn = st.columns([4, 1])

                    with col_id:
                        st.markdown(
                            f'<span class="course-id-label">{course["course_id"]}</span>',
                            unsafe_allow_html=True,
                        )

                    with col_btn:
                        global_idx = start_index + row_idx * N_COLS + i
                        btn_key = f"khoa_open_{course['course_id']}_{global_idx}"
                        st.button(
                            "↗",
                            key=btn_key,
                            on_click=lambda cid=course["course_id"]: navigate_to_dashboard(cid),
                        )

                    st.markdown(f'<p class="course-title">{course["course_name"]}</p>', unsafe_allow_html=True)
                    st.markdown(f"*{course.get('school_name','') or 'N/A'}*", unsafe_allow_html=True)

                    st.markdown(
                        '<div style="margin-top: 10px; margin-bottom: 5px; border-top: 1px solid rgba(255, 255, 255, 0.05);"></div>',
                        unsafe_allow_html=True,
                    )

                    col_date, col_users = st.columns([2, 1])

                    with col_date:
                        start = course.get("class_start", "")
                        end = course.get("class_end", "")
                        st.markdown(f"🗓️ **Thời gian:** {start} – {end}")

                    with col_users:
                        try:
                            user_count_formatted = f"{int(course.get('user_count', 0)):,.0f}".replace(",", ".")
                        except Exception:
                            user_count_formatted = course.get("user_count", 0)

                        st.markdown(
                            f"<div style='text-align: right; font-weight: 700; color: #48bb78; font-size: 1.1em;'>👥 {user_count_formatted}</div>",
                            unsafe_allow_html=True,
                        )

    def go_to_page(page_num: int) -> None:
        st.session_state.khoa_current_page = page_num

    # 5 cột: spacer | prev | text | next | spacer  (text rộng hơn => cân đối)
    col_sp_l, col_prev, col_text, col_next, col_sp_r = st.columns([1, 1, 1, 0.5, 1])

    with col_prev:
        st.markdown("<span class='page-prev-marker'></span>", unsafe_allow_html=True)
        st.button(
            "⟨⟨",
            disabled=(st.session_state.khoa_current_page == 1),
            on_click=lambda: go_to_page(st.session_state.khoa_current_page - 1),
            key="page_prev",
        )

    with col_text:
        st.markdown("<span class='page-text-marker'></span>", unsafe_allow_html=True)
        st.markdown(
            f"<div style='padding-top: 12px; font-weight: 600;'>Trang {st.session_state.khoa_current_page} / {total_pages}</div>",
            unsafe_allow_html=True,
        )

    with col_next:
        st.markdown("<span class='page-next-marker'></span>", unsafe_allow_html=True)
        st.button(
            "⟩⟩",
            disabled=(st.session_state.khoa_current_page == total_pages or total_pages == 0),
            on_click=lambda: go_to_page(st.session_state.khoa_current_page + 1),
            key="page_next",
        )
