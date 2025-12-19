import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


# =========================================================
# STATIC RESULTS (SHOW ONLY) — KHÔNG TÍNH TOÁN LẠI
# =========================================================
DQ_RESULTS = {
    "completeness": {
        "overall": 0.4885,  # 48.85%
        "notes": [
            "Completeness toàn bộ dataset = 0.4885 (mức thấp, dữ liệu khuyết thiếu nghiêm trọng).",
            "Thiếu chủ yếu ở các cột hành vi theo phase (video/problem/comment).",
            "Nguyên nhân: không phải user nào cũng có event; khi merge có thể phát sinh null."
        ],
        "top_missing_cols": [
            ("phase1_days", 0.90),
            ("cutoff_time_P1", 0.88),
            ("n_attempts_P1", 0.86),
            ("accuracy_rate_P1", 0.86),
            ("avg_score_P1", 0.86),
            ("avg_duration_per_event_P4", 0.82),
            ("avg_speed_P4", 0.82),
            ("max_speed_P4", 0.82),
            ("num_active_days_P4", 0.81),
            ("first_watch_time_P4", 0.80),
        ],
    },

    "consistency": {
        "overall": 0.6449,  # 64.49%
        "rule_pass_rates": [
            ("Non-Null", 0.0432),              # 4.32%
            ("Logical Constraints", 0.4715),   # 47.15%
            ("Data Type", 1.0),                # 100%
            ("Domain Range", 1.0),             # 100%
            ("Uniqueness", 1.0),               # 100%
            ("Foreign Keys", 1.0),             # 100%
        ],
        "notes": [
            "Điểm Consistency TB = 64.49%.",
            "Mạnh: Data Type, Domain Range, Uniqueness, Foreign Keys đều 100%.",
            "Yếu nghiêm trọng: Non-Null chỉ 4.32% và Logical Constraints 47.15%."
        ],
    },

    "timeliness": {
        "overall": 0.2823,  # 28.23%
        "phase_breakdown": [
            ("Phase 1", 0.5214),
            ("Phase 2", 0.5214),
            ("Phase 3", 0.5214),
            ("Phase 4", 0.5214),
            ("Phase 5", 0.5214),
        ],
        "notes": [
            "Overall Timeliness = 28.23% (thấp).",
            "Nguyên nhân chính: nhiều giá trị Null → fail theo strict rule is_not_null().",
            "Bất thường: Phase 2–5 trùng Phase 1 → nghi ngờ dữ liệu ActionTime bị sao chép/đồng nhất."
        ],
    },

    "uniqueness": {
        "row_level": 1.0,
        "key_level": 1.0,
        "notes": [
            "Row-level Uniqueness = 100% (không có dòng trùng).",
            "Key-level (user_id, course_id) = 100% (không trùng khóa)."
        ],
    },

    "acc_dq": {
        "s_perf": 0.8903,
        "s_san_plus": 0.0143,
        "acc_dq_score": 17.05,  # thang điểm 0-100
        "s_perf_components": [
            ("Macro-F1", 0.8939),
            ("Balanced Accuracy", 0.8793),
            ("MCC (normalized)", 0.8944),
            ("Cohen's Kappa (normalized)", 0.8939),
        ],
        "s_san_plus_components": [
            ("s_nan", 1.0000),
            ("s_maj", 0.2133),
            ("s_ent", 0.0000),
            ("s_drift", 1.0000),
            ("s_eff", 1.0000),
            ("s_leak", 0.5000),
        ],
        "notes": [
            "S_perf cao (~0.89) → mô hình dự đoán tốt.",
            "S_san+ rất thấp (~0.0143) → dấu hiệu Mode Collapse (s_maj thấp) và Overconfidence (s_ent ~ 0).",
            "Acc-DQ thấp (17.05) chủ yếu do S_san+ kéo xuống."
        ],
        "recommendations": [
            "Giảm overconfidence: tuning threshold (vd 0.5 → 0.4/0.3).",
            "Cân bằng dữ liệu tốt hơn: sampling / reweighting / focal loss (nếu có train lại).",
            "Rà soát leakage từ missingness (s_leak ~ 0.5 là mức trung bình)."
        ],
    },
}


# =========================================================
# HELPERS
# =========================================================
def _theme_tokens(theme: str):
    if str(theme).lower() == "dark":
        return {
            "bg": "#1a202c",
            "text": "#ffffff",
            "grid": "#2d3748",
            "card": "#2d3748",
        }
    return {
        "bg": "#ffffff",
        "text": "#111827",
        "grid": "#e5e7eb",
        "card": "#f7fafc",
    }


def _is_horizontal_bar(fig) -> bool:
    """Detect if any trace is horizontal bar (orientation='h')."""
    try:
        for tr in fig.data:
            ori = getattr(tr, "orientation", None)
            if ori == "h":
                return True
    except Exception:
        pass
    return False


def _apply_theme(fig, bg, text, grid):
    is_hbar = _is_horizontal_bar(fig)

    fig.update_layout(
        plot_bgcolor=bg,
        paper_bgcolor=bg,
        font=dict(color=text),
        margin=dict(
            l=150 if is_hbar else 70,
            r=50,
            t=70,
            b=70,
        ),
    )

    if hasattr(fig.layout, "xaxis"):
        fig.update_xaxes(
            gridcolor=grid,
            automargin=True,
            title_standoff=20   # ⬅️ khoảng cách title trục X
        )

    if hasattr(fig.layout, "yaxis"):
        fig.update_yaxes(
            gridcolor=grid,
            automargin=True,
            title_standoff=30   # ⬅️ FIX DÍNH “Column / Rule”
        )

    return fig

def _gauge(title, value_0_1, bg, text):
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=float(value_0_1) * 100,
        number={
            "suffix": "%",
            "font": {"size": 40}  # Cap font size for the value
        },
        title={
            "text": title,
            "font": {"size": 18}   # Standardize title size
        },
        gauge={
            "axis": {"range": [0, 100]},
            "bar": {"color": "#1C70CA"}
        },
    ))
    fig.update_layout(
        paper_bgcolor=bg,
        font=dict(color=text),
        margin=dict(l=30, r=30, t=50, b=20),
        height=220,  # Slightly shorter for better fitting
    )
    return fig


# =========================================================
# MAIN
# =========================================================
def show(df=None, theme="Dark"):
    # df nhận để tương thích app.py, nhưng KHÔNG dùng.
    tok = _theme_tokens(theme)
    bg_color, text_color, grid_color = tok["bg"], tok["text"], tok["grid"]

    st.title("Chất lượng dữ liệu")
    st.caption("Trang này chỉ hiển thị **kết quả đã tính sẵn** (không chạy lại tính toán).")

    tab_titles = ["Completeness", "Consistency", "Timeliness & Uniqueness", "Acc-DQ Model"]
    active_tab = st.radio(
        "",
        tab_titles,
        horizontal=True,
        label_visibility="collapsed",
        key="dq_static_tabs",
    )

    st.markdown("---")

    # =======================
    # TAB: COMPLETENESS
    # =======================
    if active_tab == "Completeness":
        st.header("Completeness")

        overall = DQ_RESULTS["completeness"]["overall"]
        c1, c2 = st.columns([1, 2], gap="large")

        with c1:
            st.plotly_chart(_gauge("Dataset Completeness", overall, bg_color, text_color),
                            use_container_width=True, theme=None)
            st.metric("Điểm Completeness", f"{overall:.4f}", f"{overall*100:.2f}%")

        with c2:
            top_missing = pd.DataFrame(
                DQ_RESULTS["completeness"]["top_missing_cols"],
                columns=["Column", "Null_Rate"]
            ).sort_values("Null_Rate", ascending=True)

            fig = px.bar(
                top_missing,
                x="Null_Rate",
                y="Column",
                orientation="h",
                text=top_missing["Null_Rate"].map(lambda x: f"{x*100:.1f}%"),
                title="Top cột thiếu dữ liệu (tỷ lệ Null)"
            )
            fig.update_traces(textposition="outside", cliponaxis=False)
            st.plotly_chart(_apply_theme(fig, bg_color, text_color, grid_color),
                            use_container_width=True, theme=None)

        st.subheader("Nhận xét")
        for n in DQ_RESULTS["completeness"]["notes"]:
            st.write("• " + n)

    # =======================
    # TAB: CONSISTENCY
    # =======================
    elif active_tab == "Consistency":
        st.header("Consistency")

        overall = DQ_RESULTS["consistency"]["overall"]
        rules_df = pd.DataFrame(
            DQ_RESULTS["consistency"]["rule_pass_rates"],
            columns=["Rule", "Pass_Rate"]
        )

        c1, c2 = st.columns([1, 2], gap="large")

        with c1:
            st.plotly_chart(_gauge("Consistency (Average)", overall, bg_color, text_color),
                            use_container_width=True, theme=None)
            st.metric("Consistency TB", f"{overall:.4f}", f"{overall*100:.2f}%")

        with c2:
            # ✅ FIX lệch %: dùng cùng df đã sort cho cả data + text
            sorted_df = rules_df.sort_values("Pass_Rate", ascending=True).reset_index(drop=True)

            fig = px.bar(
                sorted_df,
                x="Pass_Rate",
                y="Rule",
                orientation="h",
                text=sorted_df["Pass_Rate"].map(lambda x: f"{x*100:.2f}%"),
                title="Tỷ lệ đạt của từng quy tắc"
            )
            fig.update_layout(xaxis=dict(range=[0, 1.05]))
            fig.update_traces(textposition="outside", cliponaxis=False)
            st.plotly_chart(_apply_theme(fig, bg_color, text_color, grid_color),
                            use_container_width=True, theme=None)

        st.subheader("Nhận xét")
        for n in DQ_RESULTS["consistency"]["notes"]:
            st.write("• " + n)

    # =======================
    # TAB: TIMELINESS & UNIQUENESS
    # =======================
    elif active_tab == "Timeliness & Uniqueness":
        st.header("Timeliness & Uniqueness")

        left, right = st.columns(2, gap="large")

        # Timeliness
        with left:
            st.subheader("Timeliness")
            t_overall = DQ_RESULTS["timeliness"]["overall"]
            st.plotly_chart(_gauge("Overall Timeliness", t_overall, bg_color, text_color),
                            use_container_width=True, theme=None)
            st.metric("Timeliness", f"{t_overall:.4f}", f"{t_overall*100:.2f}%")

            phase_df = pd.DataFrame(
                DQ_RESULTS["timeliness"]["phase_breakdown"],
                columns=["Phase", "OnTime_Rate"]
            )

            fig = px.bar(
                phase_df,
                x="Phase",
                y="OnTime_Rate",
                text=phase_df["OnTime_Rate"].map(lambda x: f"{x*100:.2f}%"),
                title="Breakdown theo Phase"
            )
            fig.update_traces(textposition="outside", cliponaxis=False)

            y_max = float(phase_df["OnTime_Rate"].max())
            fig.update_layout(yaxis=dict(range=[0, max(0.65, y_max * 1.25)]))

            st.plotly_chart(_apply_theme(fig, bg_color, text_color, grid_color),
                            use_container_width=True, theme=None)

            st.subheader("Nhận xét")
            for n in DQ_RESULTS["timeliness"]["notes"]:
                st.write("• " + n)

        # Uniqueness
        with right:
            st.subheader("Uniqueness")
            u_row = DQ_RESULTS["uniqueness"]["row_level"]
            u_key = DQ_RESULTS["uniqueness"]["key_level"]

            m1, m2 = st.columns(2)
            m1.metric("Row-level", f"{u_row*100:.0f}%")
            m2.metric("Key-level (user_id, course_id)", f"{u_key*100:.0f}%")

            donut_df = pd.DataFrame(
                [{"Type": "Row-level", "Score": u_row}, {"Type": "Key-level", "Score": u_key}]
            )
            fig = px.pie(donut_df, values="Score", names="Type", hole=0.55, title="Uniqueness Scores")
            fig.update_layout(paper_bgcolor=bg_color, font=dict(color=text_color))
            st.plotly_chart(fig, use_container_width=True, theme=None)

            st.subheader("Nhận xét")
            for n in DQ_RESULTS["uniqueness"]["notes"]:
                st.write("• " + n)

    # =======================
    # TAB: ACC-DQ MODEL
    # =======================
    elif active_tab == "Acc-DQ Model":
        st.header("Acc-DQ Model")

        acc = DQ_RESULTS["acc_dq"]

        k1, k2, k3 = st.columns(3)
        k1.metric("S_perf", f"{acc['s_perf']:.4f}")
        k2.metric("S_san+", f"{acc['s_san_plus']:.4f}")
        k3.metric("Acc-DQ", f"{acc['acc_dq_score']:.2f}")

        st.markdown("---")

        c1, c2 = st.columns(2, gap="large")

        with c1:
            st.subheader("S_perf (Hiệu năng)")
            sp_df = pd.DataFrame(acc["s_perf_components"], columns=["Metric", "Value"])
            sp_sorted = sp_df.sort_values("Value", ascending=True)

            fig = px.bar(
                sp_sorted,
                x="Value",
                y="Metric",
                orientation="h",
                text=sp_sorted["Value"].map(lambda x: f"{x:.4f}"),
                title="Thành phần S_perf"
            )
            fig.update_layout(xaxis=dict(range=[0, 1.05]))
            fig.update_traces(textposition="outside", cliponaxis=False)
            st.plotly_chart(_apply_theme(fig, bg_color, text_color, grid_color),
                            use_container_width=True, theme=None)

        with c2:
            st.subheader("S_san+ (Lành mạnh)")
            ss_df = pd.DataFrame(acc["s_san_plus_components"], columns=["Metric", "Value"])
            ss_sorted = ss_df.sort_values("Value", ascending=True)

            fig = px.bar(
                ss_sorted,
                x="Value",
                y="Metric",
                orientation="h",
                text=ss_sorted["Value"].map(lambda x: f"{x:.4f}"),
                title="Thành phần S_san+"
            )
            fig.update_layout(xaxis=dict(range=[0, 1.05]))
            fig.update_traces(textposition="outside", cliponaxis=False)
            st.plotly_chart(_apply_theme(fig, bg_color, text_color, grid_color),
                            use_container_width=True, theme=None)

        st.subheader("Nhận xét")
        for n in acc["notes"]:
            st.write("• " + n)

        st.subheader("Đề xuất cải thiện")
        for r in acc["recommendations"]:
            st.write("• " + r)
