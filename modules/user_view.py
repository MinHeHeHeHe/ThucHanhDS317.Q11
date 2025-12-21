import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from urllib.parse import quote  # ✅ thêm để encode user_id/course_id an toàn
from modules.data_loader import load_users, load_courses


def _theme_tokens():
    theme = st.session_state.get("theme", "Light")
    if str(theme).lower() == "dark":
        return {
            "bg": "#1a202c",
            "text": "#ffffff",
            "card": "#2d3748",
            "grid": "#4a5568",
        }
    return {
        "bg": "#ffffff",
        "text": "#000000",
        "card": "#f7fafc",
        "grid": "#e2e8f0",
    }


def display_user_dashboard(USER_ID: str):
    """Hiển thị giao diện chi tiết của học viên."""
    tok = _theme_tokens()
    bg_color, text_color, grid_color = tok["bg"], tok["text"], tok["grid"]

    st.markdown(f"<h1 style='font-size: 42px; font-weight: 800; margin-bottom: 5px;'>Chi tiết học viên: {USER_ID}</h1>", unsafe_allow_html=True)

    st.markdown(
        f"""
    <style>
        .metric-card {{
            color: {text_color} !important;
        }}
        .metric-label {{
            color: {text_color} !important;
            font-size: 18px !important;
            font-weight: 600 !important;
        }}
        .metric-value {{
            color: {text_color} !important;
            font-size: 32px !important; 
        }}
        h1, h2, h3, p, li, span, div {{
            font-size: 16px;
        }}
    </style>
    """,
        unsafe_allow_html=True,
    )

    st.markdown("---")

    try:
        df_users = load_users()
        df_courses = load_courses()

        COURSE_ID = st.session_state.selected_course_id
        if COURSE_ID is None:
            st.error("Không có COURSE_ID trong session. Vui lòng chọn khóa học lại.")
            return

        user_data = df_users[(df_users["user_id"] == USER_ID) & (df_users["course_id"] == COURSE_ID)]
        course_data = df_courses[df_courses["course_id"] == COURSE_ID].iloc[0]

        if user_data.empty:
            st.error(f"Không tìm thấy dữ liệu cho User ID: {USER_ID}")
            return

        user = user_data.iloc[0]
        enroll_time_formatted = pd.to_datetime(user.get("enroll_time", None), errors="coerce")
        enroll_time_formatted = enroll_time_formatted.strftime("%d/%m/%Y") if not pd.isna(enroll_time_formatted) else "-"

    except Exception as e:
        st.error(f"Lỗi khi đọc dữ liệu: {e}")
        return

    col1, col2, col3, col4, col5 = st.columns([1.5, 1, 1, 1, 1])

    with col1:
        st.markdown(
            f"""
        <div class='metric-card'>
            <div class='metric-label'>Thông tin cơ bản</div>
            <div style='font-size: 18px; line-height: 1.8; color: {text_color};'>
                <b>User ID:</b> {user.get('user_id', '-') }<br>
                <b>Course ID:</b> {user.get('course_id', '-') }<br>
                <b>Ngày đăng kí:</b> {enroll_time_formatted}<br>
                <b>Số khóa học:</b> {int(user.get('user_num_prev_courses', 0) or 0) + 1}<br>
                <b>Thời gian còn lại:</b> {float(user.get('remaining_time', 0) or 0):.0f} ngày
            </div>
        </div>
        """,
            unsafe_allow_html=True,
        )

    with col2:
        num_videos = int(user.get("num_videos_P5", 0) or 0)
        st.markdown(
            f"""
        <div class='metric-card'>
            <div class='metric-label'>Video</div>
            <div class='metric-value'>{num_videos}</div>
            <div style='font-size: 18px; color: {text_color}; opacity: 0.8; margin-top: 8px;'>Đã xem</div>
        </div>
        """,
            unsafe_allow_html=True,
        )

    with col3:
        n_comments = int(user.get("n_comments_P5", 0) or 0)
        st.markdown(
            f"""
        <div class='metric-card'>
            <div class='metric-label'>Comment</div>
            <div class='metric-value'>{n_comments}</div>
            <div style='font-size: 18px; color: {text_color}; opacity: 0.8; margin-top: 8px;'>Số bình luận</div>
        </div>
        """,
            unsafe_allow_html=True,
        )

    with col4:
        n_attempts = int(user.get("n_attempts_P5", 0) or 0)
        st.markdown(
            f"""
        <div class='metric-card'>
            <div class='metric-label'>Problem</div>
            <div class='metric-value'>{n_attempts}</div>
            <div style='font-size: 18px; color: {text_color}; opacity: 0.8; margin-top: 8px;'>Đã làm</div>
        </div>
        """,
            unsafe_allow_html=True,
        )

    with col5:
        duration_days = float(user.get("class_duration_days", 0) or 0)
        remaining_time = float(user.get("remaining_time", 0) or 0)

        time_elapsed = max(duration_days - remaining_time, 0)
        time_progress_percent = (time_elapsed / duration_days) * 100 if duration_days > 0 else 0

        fig_time_gauge = go.Figure(
            go.Indicator(
                mode="gauge+number",
                value=time_progress_percent,
                title={"text": "<b>Tiến trình Thời gian (%)</b>", "font": {"size": 22}},
                number={"font": {"size": 42}},
                gauge={
                    "axis": {"range": [None, 100], "tickwidth": 1},
                    "bar": {"color": "darkblue"},
                    "steps": [{"range": [0, 50], "color": "lightgray"}, {"range": [50, 100], "color": "gray"}],
                    "threshold": {"line": {"color": "red", "width": 4}, "thickness": 0.75, "value": 90},
                },
            )
        )
        fig_time_gauge.update_layout(
            height=250,
            margin=dict(l=20, r=20, t=80, b=20),
            paper_bgcolor=bg_color,
            font=dict(color=text_color, size=20),
        )
        st.plotly_chart(fig_time_gauge, use_container_width=True, theme=None)

    st.markdown("---")

    col_chart_left, col_chart_right = st.columns(2)

    with col_chart_left:
        with st.container(border=True):
            st.markdown("<h2 style='font-size: 32px; font-weight: 700; margin-bottom: 20px;'>Phân phối điểm số</h2>", unsafe_allow_html=True)

            num_videos_watched = float(user.get("num_videos_P5", 0) or 0)
            total_videos = float(course_data.get("video_count", 0) or 0)
            accuracy_rate = float(user.get("accuracy_rate_P5", 0) or 0)

            video_percentage = (num_videos_watched / total_videos) * 100 if total_videos > 0 else 0
            exercise_percentage = accuracy_rate * 100

            df_scores = pd.DataFrame(
                {
                    "Hoạt động": ["Video", "Exercise"],
                    "Điểm (%)": [video_percentage, exercise_percentage],
                    "Nhãn": [f"{video_percentage:.1f}%", f"{exercise_percentage:.1f}%"],
                }
            )

            color_map = {"Video": "#3182ce", "Exercise": "#38a169"}
            fig = px.bar(
                df_scores,
                x="Hoạt động",
                y="Điểm (%)",
                text="Nhãn",
                color="Hoạt động",
                color_discrete_map=color_map,
                height=450,
            )

            fig.update_traces(
                textposition="outside", 
                textfont=dict(size=18, weight='bold'), 
                marker_line_width=0,
                hovertemplate="<b>%{x}</b><br>Điểm: %{y:.1f}%<extra></extra>"
            )
            fig.update_layout(
                title=dict(text="<b>Phân phối điểm số</b>", x=0.5, font=dict(size=32, color=text_color)),
                yaxis=dict(
                    title="<b>Phần trăm (%)</b>",
                    range=[0, 115], # Extra room for labels
                    tickvals=[0, 25, 50, 75, 100],
                    showgrid=True,
                    gridcolor=grid_color,
                    tickfont=dict(color=text_color, size=16),
                    titlefont=dict(color=text_color, size=20),
                ),
                xaxis=dict(
                    title=None, 
                    tickfont=dict(color=text_color, size=16)
                ),
                showlegend=False,
                plot_bgcolor=bg_color,
                paper_bgcolor=bg_color,
                font=dict(color=text_color, size=16),
                margin=dict(l=60, r=20, t=100, b=60), # Added more padding
            )
            st.plotly_chart(fig, use_container_width=True, theme=None)

    with col_chart_right:
        with st.container(border=True):
            st.markdown("<h2 style='font-size: 32px; font-weight: 700; margin-bottom: 20px;'>Lượt xem video và làm bài tập theo giai đoạn</h2>", unsafe_allow_html=True)

            periods_percent = [0.20, 0.40, 0.60, 0.80, 0.90]
            video_cols = [f"num_events_P{i}" for i in range(1, 6)]
            attempt_cols = [f"n_attempts_P{i}" for i in range(1, 6)]

            duration_days = float(user.get("class_duration_days", 0) or 0)
            time_labels = []

            enroll_ts = pd.to_datetime(user.get("enroll_time", None), errors="coerce")

            if duration_days > 0 and not pd.isna(enroll_ts):
                for percent in periods_percent:
                    days_added = int(duration_days * percent)
                    new_date = enroll_ts + pd.Timedelta(days=days_added)
                    time_labels.append(new_date.strftime("%b %Y"))
            else:
                time_labels = [f"P{i} ({int(p*100)}%)" for i, p in enumerate(periods_percent, 1)]

            video_views = [float(user.get(col, 0) or 0) for col in video_cols]
            attempt_attempts = [float(user.get(col, 0) or 0) for col in attempt_cols]

            df_chart = pd.DataFrame({"Giai đoạn": time_labels, "Lượt xem video": video_views, "Lượt làm bài tập": attempt_attempts})
            # Aggregate by Giai đoạn to handle duplicate months
            df_chart = df_chart.groupby("Giai đoạn", sort=False).sum().reset_index()

            if not df_chart.empty:
                fig_monthly = px.line(
                    df_chart, 
                    x="Giai đoạn", 
                    y=["Lượt xem video", "Lượt làm bài tập"], 
                    markers=True, 
                    height=400,
                    line_shape='spline' # Smooth curves
                )
                fig_monthly.update_traces(marker=dict(size=10, line=dict(width=2)))
                fig_monthly.update_layout(
                    title=dict(text="<b>Lượt xem video và làm bài tập theo giai đoạn</b>", x=0.5, font=dict(size=32)),
                    xaxis_title=None,
                    yaxis_title="<b>Số lượt</b>",
                    hovermode="x unified",
                    legend=dict(
                        title=None, # Remove "variable"
                        orientation="h",
                        yanchor="bottom",
                        y=1.02,
                        xanchor="right",
                        x=1,
                        font=dict(color=text_color, size=18), 
                        bgcolor="rgba(0,0,0,0)"
                    ),
                    plot_bgcolor=bg_color,
                    paper_bgcolor=bg_color,
                    font=dict(color=text_color, size=18),
                    xaxis=dict(
                        gridcolor=grid_color, 
                        tickfont=dict(color=text_color, size=18),
                        tickangle=0
                    ),
                    yaxis=dict(
                        gridcolor=grid_color, 
                        tickfont=dict(color=text_color, size=18), 
                        titlefont=dict(color=text_color, size=20)
                    ),
                    margin=dict(l=50, r=20, t=80, b=40),
                )
                st.plotly_chart(fig_monthly, use_container_width=True, theme=None)
            else:
                st.info("⚠️ Không có dữ liệu sự kiện theo giai đoạn.")

    st.markdown("<h2 style='font-size: 32px; font-weight: 700; margin-bottom: 20px; margin-top: 30px;'>Số ngày hoạt động (Nộp bài vs. Xem Video)</h2>", unsafe_allow_html=True)

    active_days_video_cols = [f"num_active_days_P{i}" for i in range(1, 6)]
    active_days_submit_cols = [f"active_days_P{i}" for i in range(1, 6)]

    df_active = pd.DataFrame(
        {
            "Giai đoạn": time_labels,
            "Số ngày hoạt động theo video": [float(user.get(col, 0) or 0) for col in active_days_video_cols],
            "Số ngày hoạt động theo bài tập": [float(user.get(col, 0) or 0) for col in active_days_submit_cols],
        }
    )
    # Aggregate by Giai đoạn to handle duplicate months
    df_active = df_active.groupby("Giai đoạn", sort=False).sum().reset_index()

    df_melted_active = df_active.melt(
        id_vars="Giai đoạn",
        value_vars=["Số ngày hoạt động theo video", "Số ngày hoạt động theo bài tập"],
        var_name="Hoạt động",
        value_name="Số ngày",
    )

    fig_active = px.bar(
        df_melted_active,
        x="Giai đoạn",
        y="Số ngày",
        color="Hoạt động",
        barmode="group",
        height=400,
        text="Số ngày",
        color_discrete_sequence=["#4299e1", "#ed8936"] # Blue and Orange
    )
    max_active = df_melted_active["Số ngày"].max() if not df_melted_active.empty else 0
    y_range_active = [0, max_active * 1.3] if max_active > 0 else [0, 5]

    fig_active.update_traces(
        textposition="outside", 
        textfont=dict(size=18, weight='bold'),
        marker_line_width=0,
        cliponaxis=False
    )
    fig_active.update_layout(
        title=dict(text="<b>Số ngày Hoạt động theo Giai đoạn</b>", x=0.5, font=dict(size=32)),
        xaxis_tickangle=0, # Prefer horizontal if labels are short
        plot_bgcolor=bg_color,
        paper_bgcolor=bg_color,
        font=dict(color=text_color, size=18),
        xaxis=dict(
            title=None,
            gridcolor=grid_color, 
            tickfont=dict(color=text_color, size=18)
        ),
        yaxis=dict(
            title="<b>Số ngày</b>",
            gridcolor=grid_color, 
            tickfont=dict(color=text_color, size=18),
            titlefont=dict(color=text_color, size=20),
            range=y_range_active
        ),
        legend=dict(
            title=None,
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            font=dict(color=text_color, size=18), 
            bgcolor="rgba(0,0,0,0)"
        ),
        margin=dict(l=50, r=20, t=110, b=40),
    )
    st.plotly_chart(fig_active, use_container_width=True, theme=None)

    is_dropout = int(user.get("predict", 0) or 0) == 1
    if is_dropout:
        status_text = "⚠️ Cảnh báo: Học viên này có khả năng sẽ bỏ học!"
        status_color = "#e53e3e"  # Red
        status_bg = "rgba(229, 62, 62, 0.1)"
        status_border = "#feb2b2"
    else:
        status_text = "✅ Học viên này có khả năng hoàn thành khóa học."
        status_color = "#38a169"  # Green
        status_bg = "rgba(56, 161, 105, 0.1)"
        status_border = "#9ae6b4"

    st.markdown(
        f"""
        <div style='
            background-color: {status_bg};
            border: 2px solid {status_border};
            border-radius: 12px;
            padding: 25px;
            margin-top: 40px;
            margin-bottom: 20px;
            text-align: center;
        '>
            <div style='font-size: 36px; font-weight: 800; color: {status_color};'>
                {status_text}
            </div>
        </div>
    """,
        unsafe_allow_html=True,
    )


# =========================
# ✅ ROUTING FIX HERE
# =========================
def navigate_to_user_detail(user_id: str):
    """
    Click nút ... ở User List => mở tab User Detail.
    Phải set page=dashboard (khớp app.py), kèm course_id & user_id.
    """
    user_id = str(user_id)
    course_id = st.session_state.get("selected_course_id")

    st.session_state.current_user_id = user_id
    st.session_state.current_view = "user_detail"
    st.session_state.course_detail_tabs = f"👤 User: {user_id}"

    if not course_id:
        # nếu thiếu course_id thì chỉ set user_id trong state và dừng
        return

    # ✅ app.py của bạn dùng page=dashboard
    st.query_params["page"] = "dashboard"
    st.query_params["theme"] = st.session_state.get("theme", "Light")

    # encode an toàn
    st.query_params["course_id"] = quote(str(course_id))
    st.query_params["user_id"] = quote(user_id)


def go_to_user_page(page_num):
    st.session_state.user_page = page_num


def display_user_list(COURSE_ID):
    tok = _theme_tokens()
    text_color = tok["text"]

    st.markdown(
        f"""
    <style>
        h1, h2, h3, p, div, span, label, li, button, input {{
            font-size: 20px !important;
            color: {text_color} !important;
        }}
    </style>
    """,
        unsafe_allow_html=True,
    )

    if "last_course_id" not in st.session_state or st.session_state.last_course_id != COURSE_ID:
        st.session_state.user_page = 1
        st.session_state.last_course_id = COURSE_ID

    try:
        df_users = load_users()
        df_filtered_users = df_users[df_users["course_id"] == COURSE_ID].copy()
        if "enroll_time" in df_filtered_users.columns:
            df_filtered_users["enroll_time"] = pd.to_datetime(df_filtered_users["enroll_time"], errors="coerce").dt.strftime("%d/%m/%Y")
    except Exception as e:
        st.error(f"Lỗi khi đọc dữ liệu user: {e}")
        return

    st.header("Danh sách học viên")
    total_users = len(df_filtered_users)
    st.markdown(f"Quản lý và xem tất cả người dùng hệ thống ({total_users} học viên)")

    search_user = st.text_input("🔍 Tìm kiếm bằng ID ...", placeholder="Tìm kiếm bằng ID ...")

    if search_user:
        st.session_state.user_page = 1
        df_display = df_filtered_users[df_filtered_users["user_id"].astype(str).str.contains(search_user, case=False, na=False)]
    else:
        df_display = df_filtered_users.copy()

    PAGE_SIZE = 10
    total_display_users = len(df_display)
    total_pages = (total_display_users + PAGE_SIZE - 1) // PAGE_SIZE
    if total_pages == 0:
        total_pages = 1

    st.session_state.user_page = max(1, min(st.session_state.user_page, total_pages))

    start_index = (st.session_state.user_page - 1) * PAGE_SIZE
    end_index = start_index + PAGE_SIZE
    users_on_page = df_display.iloc[start_index:end_index]

    st.markdown("---")

    col_avatar, col_user_id, col_enroll, col_view = st.columns([1, 3, 2, 1])
    with col_avatar:
        st.markdown("**AVATAR**")
    with col_user_id:
        st.markdown("**USER ID**")
    with col_enroll:
        st.markdown("**ĐĂNG KÝ**")
    with col_view:
        st.markdown("**XEM**")
    st.markdown("---")

    if total_display_users > 0:
        for index, user in users_on_page.iterrows():
            col_avatar, col_user_id, col_enroll, col_view = st.columns([1, 3, 2, 1])

            with col_avatar:
                st.markdown("👤")
            with col_user_id:
                st.markdown(f"**{user['user_id']}**")
            with col_enroll:
                st.markdown(f"🗓️ {user.get('enroll_time','-')}")
            with col_view:
                st.button(
                    ":material/more_horiz:",
                    key=f"user_view_{user['user_id']}_{index}",
                    on_click=navigate_to_user_detail,
                    args=(user["user_id"],),
                )

            st.markdown("---")
    else:
        st.info("Không tìm thấy học viên nào phù hợp với tìm kiếm.")

    _, col_prev, col_pages, col_next, _ = st.columns([3, 0.5, 2, 1.5, 2])

    with col_prev:
        st.button(
            "⟨⟨",
            disabled=(st.session_state.user_page == 1),
            key="user_prev_btn_tab",
            on_click=go_to_user_page,
            args=(st.session_state.user_page - 1,),
        )

    with col_next:
        st.button(
            "⟩⟩",
            disabled=(st.session_state.user_page == total_pages or total_pages == 0),
            key="user_next_btn_tab",
            on_click=go_to_user_page,
            args=(st.session_state.user_page + 1,),
        )

    with col_pages:
        st.markdown(
            f"<div style='text-align: center; padding-top: 10px;'>Trang {st.session_state.user_page} / {total_pages}</div>",
            unsafe_allow_html=True,
        )
