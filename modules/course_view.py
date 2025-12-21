import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from modules.data_loader import load_users

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

def display_course_dashboard(course, COURSE_ID):
    st.header("Tổng quan Khóa học")

    tok = _theme_tokens()
    bg_color, text_color, grid_color = tok["bg"], tok["text"], tok["grid"]

    st.markdown(
        f"""
    <style>
        .metric-card {{ color: {text_color} !important; }}
        .metric-label {{ color: {text_color} !important; font-size: 18px !important; }}
        .metric-value {{ color: {text_color} !important; font-size: 32px !important; }}
        h1, h2, h3, p, div, span {{ font-size: 16px; }}
    </style>
    """,
        unsafe_allow_html=True,
    )

    col1, col2, col3, col4 = st.columns([2, 1.5, 1.5, 1.5])

    with col1:
        start_dt = pd.to_datetime(course.get("class_start", None), errors="coerce")
        end_dt = pd.to_datetime(course.get("class_end", None), errors="coerce")
        start_date_formatted = start_dt.strftime("%d/%m/%Y") if not pd.isna(start_dt) else "-"
        end_date_formatted = end_dt.strftime("%d/%m/%Y") if not pd.isna(end_dt) else "-"

        st.markdown(
            f"""
            <div class='metric-card' style='padding: 18px 24px;'>
                <div class='metric-label'>Thời gian diễn ra</div>
                <div class='metric-value' style='font-size: 24px; font-weight: 500; color: {text_color};'>
                    🗓️ {start_date_formatted} <br> 
                    🗓️ {end_date_formatted}
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col2:
        st.markdown(
            f"""
        <div class='metric-card'>
            <div class='metric-label'>Số Video</div>
            <div class='metric-value'>{int(course.get('video_count',0) or 0):,}</div>
        </div>
        """,
            unsafe_allow_html=True,
        )

    with col3:
        st.markdown(
            f"""
        <div class='metric-card'>
            <div class='metric-label'>Số Bài tập</div>
            <div class='metric-value'>{int(course.get('exercise_count',0) or 0):,}</div>
        </div>
        """,
            unsafe_allow_html=True,
        )

    with col4:
        cert = int(course.get("certificate", 0) or 0)
        if cert == 1:
            icon_html = '<span class="material-symbols-outlined" style="font-size:36px; color:#F19E39; line-height: 1;">workspace_premium</span>'
            status_text = "Certificate"
        else:
            icon_html = '<span class="material-symbols-outlined" style="font-size:36px; color:#999; line-height: 1;">unlicense</span>'
            status_text = "No Certificate"

        st.markdown(
            f"""
        <div class='metric-card' style='text-align: center;'>
            <div class='metric-label' style='margin-bottom: 5px;'>Chứng chỉ</div>
            <div class='metric-value' style='display: flex; flex-direction: column; justify-content: center; align-items: center;'>
                {icon_html}
                <div style='font-size: 18px; font-weight: 600; color: {text_color}; margin-top: 5px;'>{status_text}</div>
            </div>
        </div>
        """,
            unsafe_allow_html=True,
        )

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("---")

    col_left, col_right = st.columns(2)

    with col_left:
        st.header("Phân phối điểm trong khóa học")
        score_columns = ["assignment", "video", "exam", "discussion", "article"]
        score_data = course[score_columns].fillna(0) if all(c in course.index for c in score_columns) else pd.Series([0, 0, 0, 0, 0], index=score_columns)

        df_scores = pd.DataFrame({"Phần": score_data.index, "Tỷ lệ": score_data.values}).query("`Tỷ lệ` > 0")

        if not df_scores.empty:
            fig = px.pie(df_scores, values="Tỷ lệ", names="Phần", title="Tỷ lệ đóng góp của từng phần (Assignment, Exam, etc.)", hole=0.3)
            fig.update_traces(textposition="inside", textinfo="percent+label", textfont=dict(size=20, weight="bold"))
            fig.update_layout(
                title=dict(text="<b>Tỷ lệ đóng góp của từng phần (Assignment, Exam, etc.)</b>", font=dict(size=28, color=text_color)),
                paper_bgcolor=bg_color,
                font=dict(color=text_color, size=18),
                legend=dict(font=dict(color=text_color, size=20)),
            )
            st.plotly_chart(fig, use_container_width=True, theme=None)
        else:
            st.info("Không có dữ liệu phân phối điểm cho khóa học này.")

    # Load user data once for all charts
    try:
        df_users = load_users()
        course_users = df_users[df_users["course_id"] == COURSE_ID]
    except Exception as e:
        st.error(f"Lỗi khi load dữ liệu người dùng: {e}")
        course_users = pd.DataFrame()

    with col_right:
        st.header("Dự đoán tỉ lệ bỏ học trong toàn khóa")

        if not course_users.empty and "predict" in course_users.columns:
            dropout_counts = course_users["predict"].value_counts().reset_index()
            dropout_counts.columns = ["Trạng thái", "Số lượng"]
            dropout_counts["Trạng thái"] = dropout_counts["Trạng thái"].map({0: "Không bỏ học", 1: "Bỏ học"})

            fig_dropout = px.pie(dropout_counts, values="Số lượng", names="Trạng thái", title="Tỷ lệ bỏ học (Dropout Rate)", hole=0.3)
            fig_dropout.update_traces(textposition="inside", textinfo="percent+label", textfont=dict(size=20, weight="bold"))
            fig_dropout.update_layout(
                title=dict(text="<b>Tỷ lệ bỏ học (Dropout Rate)</b>", font=dict(size=28, color=text_color)),
                paper_bgcolor=bg_color,
                font=dict(color=text_color, size=18),
                legend=dict(font=dict(color=text_color, size=20)),
            )
            st.plotly_chart(fig_dropout, use_container_width=True, theme=None)
        else:
            st.info("Không có dữ liệu về trạng thái bỏ học (column 'predict').")

    # =======================
    # 3. HÀNH VI HỌC TẬP (CUMULATIVE)
    # =======================
    st.markdown("---")
    st.header("Hành vi học tập tích lũy theo thời gian")

    video_cols = [f"num_events_P{i}" for i in range(1, 6)]
    attempt_cols = [f"n_attempts_P{i}" for i in range(1, 6)]

    if not course_users.empty:
        video_cum = course_users[video_cols].sum()
        attempt_cum = course_users[attempt_cols].sum()

        start_date = pd.to_datetime(course.get("class_start", None))
        end_date = pd.to_datetime(course.get("class_end", None))

        if not pd.isna(start_date) and not pd.isna(end_date):
            duration = (end_date - start_date).days
            percents = [0.2, 0.4, 0.6, 0.8, 0.9]
            time_labels = [(start_date + pd.Timedelta(days=int(duration * p))).strftime("%b %Y") for p in percents]
        else:
            time_labels = ["P1 (20%)", "P2 (40%)", "P3 (60%)", "P4 (80%)", "P5 (90%)"]

        df_cum = pd.DataFrame(
            {"Thời gian": time_labels, "Video (tích lũy)": video_cum.values, "Exercise (tích lũy)": attempt_cum.values}
        )

        fig_cum = px.line(df_cum, x="Thời gian", y=["Video (tích lũy)", "Exercise (tích lũy)"], markers=True, height=420)
        fig_cum.update_layout(
            title=dict(text="<b>Hành vi học tập tích lũy theo thời gian</b>", font=dict(size=24, color=text_color)),
            paper_bgcolor=bg_color,
            plot_bgcolor=bg_color,
            font=dict(color=text_color, size=16),
            yaxis_title="Tổng lượt",
            hovermode="x unified",
            legend=dict(font=dict(color=text_color)),
        )
        fig_cum.update_xaxes(gridcolor=grid_color)
        fig_cum.update_yaxes(gridcolor=grid_color)
        st.plotly_chart(fig_cum, use_container_width=True, theme=None)

        # =======================
        # 4. HÀNH VI THEO TỪNG GIAI ĐOẠN (INCREMENTAL)
        # =======================
        st.header("Mức độ tham gia theo từng giai đoạn")

        video_inc = video_cum.diff().fillna(video_cum.iloc[0])
        attempt_inc = attempt_cum.diff().fillna(attempt_cum.iloc[0])

        df_inc = pd.DataFrame({"Giai đoạn": ["0–20%", "20–40%", "40–60%", "60–80%", "80–90%"], "Video": video_inc.values, "Exercise": attempt_inc.values})

        fig_inc = px.bar(df_inc, x="Giai đoạn", y=["Video", "Exercise"], barmode="group", height=380)
        fig_inc.update_layout(
            title=dict(text="<b>Mức độ tham gia theo từng giai đoạn</b>", font=dict(size=24, color=text_color)),
            paper_bgcolor=bg_color,
            plot_bgcolor=bg_color,
            font=dict(color=text_color, size=16),
            yaxis_title="Số lượt",
            legend=dict(font=dict(color=text_color)),
        )
        fig_inc.update_xaxes(gridcolor=grid_color)
        fig_inc.update_yaxes(gridcolor=grid_color)
        st.plotly_chart(fig_inc, use_container_width=True, theme=None)
    else:
        st.info("Không có dữ liệu hành vi học tập cho khóa học này.")
