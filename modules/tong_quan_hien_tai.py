import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from modules.data_loader import load_test_predictions, load_users, load_courses

def show(df_original, theme='Light'):
    """Display the overview phase selection page with dynamic data loading"""

    # Theme colors
    if theme == "Dark":
        bg_color = '#1a202c'
        text_color = '#ffffff'
        grid_color = '#2d3748'
    else:
        bg_color = '#ffffff'
        text_color = '#1a202c'
        grid_color = '#e2e8f0'

    # Synchronize selected_phase with query parameters for persistence
    query_phase = st.query_params.get("phase", "1")
    try:
        initial_phase_idx = [1, 2, 3, 4, 5].index(int(query_phase))
    except (ValueError, TypeError):
        initial_phase_idx = 0

    st.markdown('<p style="font-size: 25px; font-weight: bold; margin-bottom: 5px;">Chọn giai đoạn</p>', unsafe_allow_html=True)

    def on_phase_change():
        st.query_params["phase"] = str(st.session_state.phase_selector)

    selected_phase = st.selectbox(
        "Chọn giai đoạn",
        options=[1, 2, 3, 4, 5],
        index=initial_phase_idx,
        key="phase_selector",
        label_visibility="collapsed",
        on_change=on_phase_change
    )

    # Calculate global metrics for the selected phase
    df_current_phase = load_test_predictions(selected_phase)
    
    # Column names based on phase
    video_col = f"num_videos_P{selected_phase}"
    attempt_col = f"n_attempts_P{selected_phase}"
    
    total_videos = int(df_current_phase[video_col].sum()) if video_col in df_current_phase.columns else 0
    total_attempts = int(df_current_phase[attempt_col].sum()) if attempt_col in df_current_phase.columns else 0

    # Calculate static global metrics (independent of phase)
    df_courses = load_courses()
    total_all_videos = int(df_courses['video_count'].sum()) if 'video_count' in df_courses.columns else 0
    total_all_exercises = int(df_courses['exercise_count'].sum()) if 'exercise_count' in df_courses.columns else 0

    # Metric Card Styling
    st.markdown(f"""
    <style>
        .metric-card {{
            background: {'linear-gradient(135deg, #1e2530 0%, #2d3748 100%)' if theme == 'Dark' else 'linear-gradient(135deg, #ffffff 0%, #f7fafc 100%)'};
            padding: 24px;
            border-radius: 16px;
            box-shadow: 0 8px 32px {'rgba(0, 0, 0, 0.4)' if theme == 'Dark' else 'rgba(0, 0, 0, 0.1)'};
            border: 1px solid {'rgba(255, 255, 255, 0.05)' if theme == 'Dark' else 'rgba(0, 0, 0, 0.05)'};
            text-align: center;
            margin-bottom: 25px;
        }}
        .metric-label {{
            color: {text_color};
            font-size: 18px;
            font-weight: 600;
            margin-bottom: 8px;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }}
        .metric-value {{
            color: {text_color};
            font-size: 36px;
            font-weight: 700;
        }}
    </style>
    """, unsafe_allow_html=True)

    # Display Cards - Row 1: Phase-dependent metrics
    col_m1, col_m2, col_m3, col_m4 = st.columns(4)
    with col_m1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Tổng số lượt xem Video (Giai đoạn {selected_phase})</div>
            <div class="metric-value">{total_videos:,}</div>
        </div>
        """, unsafe_allow_html=True)
    with col_m2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Tổng số lượt nộp Bài (Giai đoạn {selected_phase})</div>
            <div class="metric-value">{total_attempts:,}</div>
        </div>
        """, unsafe_allow_html=True)

    # Display Cards - Row 2: Global static metrics
    with col_m3:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Tổng số Video (Tất cả các Khóa học)</div>
            <div class="metric-value">{total_all_videos:,}</div>
        </div>
        """, unsafe_allow_html=True)
    with col_m4:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Tổng số Bài tập (Tất cả các Khóa học)</div>
            <div class="metric-value">{total_all_exercises:,}</div>
        </div>
        """, unsafe_allow_html=True)

    phases, counts, colors, names = [], [], [], []
    
    for p in range(1, selected_phase + 1):
        df_phase = load_test_predictions(p)
        phase_label = f'Giai đoạn {p}'
        
        if p < selected_phase:
            # For previous phases, use 'label' column (1 = dropout)
            count = (df_phase['label'] == 1).sum() if 'label' in df_phase.columns else 0
            phases.append(phase_label)
            counts.append(count)
            colors.append('#4299e1') # Blue for Label
            names.append('Nhãn thực tế')
        else:
            # For the current selected phase, use 'predict' column (1 = dropout)
            count = (df_phase['predict'] == 1).sum() if 'predict' in df_phase.columns else 0
            phases.append(phase_label)
            counts.append(count)
            colors.append('#ed8936') # Orange for Prediction
            names.append('Dự đoán')

    fig_bar = go.Figure()
    for i in range(len(phases)):
        # Show legend only once for each group
        show_legend = True
        if i > 0:
             if names[i] == names[i-1]:
                 show_legend = False
                 
        fig_bar.add_trace(go.Bar(
            x=[phases[i]],
            y=[counts[i]],
            name=names[i],
            text=[f"{counts[i]:,}"],
            textposition='outside',
            textfont=dict(size=18, weight='bold'),
            marker_color=colors[i],
            showlegend=show_legend,
            legendgroup=names[i],
            cliponaxis=False # ✅ Prevent clipping of text labels
        ))

    max_y = max(counts) if counts else 0
    y_range = [0, max_y * 1.25] if max_y > 0 else [0, 100]

    fig_bar.update_layout(
        plot_bgcolor=bg_color,
        paper_bgcolor=bg_color,
        font=dict(color=text_color, size=18),
        title=dict(
            text=f'<b>Dự đoán số lượng học viên bỏ học (Giai đoạn {selected_phase})</b>',
            font=dict(size=28, color=text_color, family='Arial, sans-serif'),
            x=0.02,
            xanchor='left'
        ),
        xaxis=dict(showgrid=False, title='', tickfont=dict(size=18, color=text_color)),
        yaxis=dict(
            showgrid=True,
            gridcolor=grid_color,
            title='<b>Số lượng học viên</b>',
            titlefont=dict(size=20, color=text_color),
            tickfont=dict(size=18, color=text_color),
            range=y_range # ✅ Dynamic range to provide space for labels
        ),
        height=500,
        margin=dict(l=50, r=20, t=120, b=50), # ✅ Increased top margin (t=100 -> 120)
        barmode='group',
        bargap=0.3,
        legend=dict(font=dict(color=text_color, size=20))
    )


    st.plotly_chart(fig_bar, use_container_width=True)

    # ---------------------------------------------------------
    # Aggregate Dropout Rate Pie Chart
    # ---------------------------------------------------------
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    if not df_current_phase.empty and "predict" in df_current_phase.columns:
        dropout_counts = df_current_phase["predict"].value_counts().reset_index()
        dropout_counts.columns = ["Trạng thái", "Số lượng"]
        dropout_counts["Trạng thái"] = dropout_counts["Trạng thái"].map({0: "Không bỏ học", 1: "Bỏ học"})

        fig_pie = px.pie(
            dropout_counts, 
            values="Số lượng", 
            names="Trạng thái", 
            hole=0.3,
            color="Trạng thái",
            color_discrete_map={"Không bỏ học": "#4299e1", "Bỏ học": "#ed8936"}
        )
        
        fig_pie.update_traces(
            textposition="inside", 
            textinfo="percent+label", 
            textfont=dict(size=20, weight="bold")
        )
        
        fig_pie.update_layout(
            title=dict(
                text=f"<b>Tỷ lệ bỏ học trong toàn bộ các Khóa học (Giai đoạn {selected_phase})</b>", 
                font=dict(size=28, color=text_color),
                x=0.02,
                xanchor='left'
            ),
            paper_bgcolor=bg_color,
            font=dict(color=text_color, size=18),
            legend=dict(font=dict(color=text_color, size=20)),
            height=600,
            margin=dict(l=50, r=20, t=100, b=50)
        )
        st.plotly_chart(fig_pie, use_container_width=True)
    else:
        st.info(f"Không có dữ liệu dự đoán cho giai đoạn {selected_phase}.")
