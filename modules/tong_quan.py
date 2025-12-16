import streamlit as st
import pandas as pd
import plotly.graph_objects as go

def show(df, theme='Dark'):
    """Display the overview page with theme support"""
    
    # Theme colors
    if theme == "Dark":
        bg_color = '#1a202c'
        text_color = '#ffffff'
        grid_color = '#2d3748'
    else:
        bg_color = '#ffffff'
        text_color = '#1a202c'
        grid_color = '#e2e8f0'

    col1, col2, col3, col4 = st.columns(4)

    # Calculate metrics
    total_students = df['user_id'].nunique()
    total_courses = df['course_id'].nunique()
    total_enrollments = len(df)
    # Calculate dropout rate (mean of label column)
    dropout_rate = df['label'].mean() * 100 if 'label' in df.columns else 0

    with col1:
        st.markdown(f"""
        <div class='metric-card'>
            <div class='metric-label'>Học viên</div>
            <div class='metric-value'>{total_students:,}</div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div class='metric-card'>
            <div class='metric-label'>Các khóa học Hoạt Động</div>
            <div class='metric-value'>{total_courses:,}</div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
        <div class='metric-card'>
            <div class='metric-label'>Tổng số lượt học</div>
            <div class='metric-value'>{total_enrollments:,}</div>
        </div>
        """, unsafe_allow_html=True)

    with col4:
        st.markdown(f"""
        <div class='metric-card'>
            <div class='metric-label'>Tỷ lệ bỏ học trung bình</div>
            <div class='metric-value'>{dropout_rate:.2f}%</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Main content area
    col1, col2 = st.columns([2, 1])

    with col1:
        # Trend chart
        
        # Group by month and year
        df_trend = df.groupby(['start_year', 'start_month']).size().reset_index(name='count')
        df_trend = df_trend.sort_values(['start_year', 'start_month'])
        
        # Create date labels manually
        df_trend['date_label'] = df_trend.apply(
            lambda x: f"{int(x['start_year'])}-{int(x['start_month']):02d}", 
            axis=1
        )
        
        fig_trend = go.Figure()
        fig_trend.add_trace(go.Scatter(
            x=df_trend['date_label'],
            y=df_trend['count'],
            mode='lines+markers',
            name='2019',
            line=dict(color='#ed8936', width=2),
            marker=dict(size=6)
        ))
        
        fig_trend.update_layout(
            plot_bgcolor=bg_color,
            paper_bgcolor=bg_color,
            font=dict(color=text_color),
            title=dict(
                text='Xu hướng học viên',
                font=dict(size=18, color=text_color, family='Arial, sans-serif'),
                x=0.02,
                xanchor='left'
            ),
            xaxis=dict(
                showgrid=True,
                gridcolor=grid_color,
                title='',
                tickfont=dict(color=text_color)
            ),
            yaxis=dict(
                showgrid=True,
                gridcolor=grid_color,
                title='',
                tickfont=dict(color=text_color)
            ),
            height=600,
            margin=dict(l=10, r=10, t=50, b=10)
        )
        
        st.plotly_chart(fig_trend, use_container_width=True)

    with col2:
        # Top 5 table with enhanced HTML/CSS design
        
        # Create top courses by dropout count (label=1)
        if 'label' in df.columns:
            dropout_df = df[df['label'] == 1]
            top_courses = dropout_df.groupby('course_id').size().reset_index(name='dropout_count')
            top_courses = top_courses.nlargest(5, 'dropout_count')
        else:
            top_courses = pd.DataFrame(columns=['course_id', 'dropout_count'])
        
        # Enhanced table HTML with modern styling
        table_html = f"""<style>
.ranking-container {{
    background: linear-gradient(135deg, #1e2530 0%, #2d3748 100%);
    border-radius: 16px;
    padding: 20px;
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.4);
    border: 1px solid rgba(255, 255, 255, 0.05);
}}
.ranking-title {{
    color: {text_color};
    font-size: 18px;
    font-weight: 700;
    margin-bottom: 1rem;
    font-family: Arial, sans-serif;
}}
.ranking-table {{
    width: 100%;
    border-collapse: separate;
    border-spacing: 0 8px;
}}
.ranking-table thead th {{
    color: #ffffff;
    font-size: 15px;
    font-weight: 600;
    text-align: left;
    padding: 12px 16px;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    border-bottom: 2px solid rgba(66, 153, 225, 0.2);
}}
.ranking-table tbody tr {{
    background: rgba(26, 32, 44, 0.6);
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    border-radius: 8px;
}}
.ranking-table tbody tr:hover {{
    background: rgba(45, 55, 72, 0.8);
    transform: translateX(4px);
    box-shadow: 0 4px 12px rgba(66, 153, 225, 0.15);
}}
.ranking-table tbody td {{
    padding: 16px;
    color: #ffffff;
    font-size: 16px;
    border-top: 1px solid rgba(255, 255, 255, 0.03);
    border-bottom: 1px solid rgba(255, 255, 255, 0.03);
}}
.ranking-table tbody tr td:first-child {{
    border-left: 1px solid rgba(255, 255, 255, 0.03);
    border-radius: 8px 0 0 8px;
}}
.ranking-table tbody tr td:last-child {{
    border-right: 1px solid rgba(255, 255, 255, 0.03);
    border-radius: 0 8px 8px 0;
}}
.rank-number {{
    color: #ffffff;
    font-weight: 600;
    font-size: 18px;
}}
.course-code {{
    color: #ffffff;
    font-weight: bold !important;
    font-family: 'Courier New', monospace;
    font-size: 18px;
}}
.enrollment-badge {{
    background: linear-gradient(135deg, #2b6cb0 0%, #3182ce 100%);
    color: #ffffff !important;
    padding: 6px 14px;
    border-radius: 20px;
    font-size: 20px;
    font-weight: bold !important;
    display: inline-block;
    box-shadow: 0 2px 8px rgba(43, 108, 176, 0.3);
}}
</style>
<div class="ranking-container">
    <div class="ranking-title">Bảng xếp hạng khóa học bỏ học cao nhất</div> 
    <table class="ranking-table">
        <thead>
            <tr>
                <th style="width: 15%; text-align: center;">#</th>
                <th style="width: 50%;">Mã khóa học</th>
                <th style="width: 35%;">SỐ LƯỢNG BỎ HỌC</th>
            </tr>
        </thead>
        <tbody>
"""
        
        # Add rows dynamically
        for idx, (i, row) in enumerate(top_courses.iterrows()):
            table_html += f"""<tr>
<td style="text-align: center;"><div class="rank-number">{idx+1}</div></td>
<td><div class="course-code">{row['course_id']}</div></td>
<td><div class="enrollment-badge">{row['dropout_count']:,}</div></td>
</tr>"""
        table_html += """
        </tbody>
    </table>
</div>"""
        
        st.markdown(table_html, unsafe_allow_html=True)

    st.markdown('<div style="height: 30px;"></div>', unsafe_allow_html=True)

    # Second row
    col1, col2 = st.columns(2)

    with col1:
        # Phase selection and bar chart
        
        # Phase selector
        st.markdown('<p style="font-size: 25px; font-weight: bold; margin-bottom: 5px;">Chọn giai đoạn:</p>', unsafe_allow_html=True)
        
        selected_phase = st.selectbox(
            "Chọn giai đoạn", 
            options=[1, 2, 3, 4, 5],
            index=0,
            key="phase_selector",
            label_visibility="collapsed"
        )
        
        # Calculate actual counts from data
        # label=1 means dropout (bỏ học), label=0 means continue (không bỏ học)
        dropout_count = df['label'].sum()  # Count of students who dropped out
        continue_count = len(df) - dropout_count  # Count of students who continued
        
        # Prepare data for phases 1 to selected_phase
        phases = []
        counts = []
        colors = []
        names = []
        
        for p in range(1, selected_phase + 1):
            phase_label = f'Phase {p}'
            
            if p < selected_phase:
                # For previous phases, show Label (students who continued)
                phases.append(phase_label)
                counts.append(continue_count)
                colors.append('#4299e1')
                names.append('Label')
            else:
                # For current phase, show Predict (students who dropped out)
                phases.append(phase_label)
                counts.append(dropout_count)
                colors.append('#ed8936')
                names.append('Predict')
        
        # Create bar chart
        fig_bar = go.Figure()
        
        for i in range(len(phases)):
            show_legend = (i == 0) or (i == len(phases) - 1 and selected_phase > 1)
            fig_bar.add_trace(go.Bar(
                x=[phases[i]],
                y=[counts[i]],
                name=names[i],
                marker_color=colors[i],
                showlegend=show_legend,
                legendgroup=names[i]
            ))
        
        fig_bar.update_layout(
            plot_bgcolor=bg_color,
            paper_bgcolor=bg_color,
            font=dict(color=text_color),
            title=dict(
                text='Số lượng đăng ký khóa học',
                font=dict(size=24, color=text_color, family='Arial, sans-serif'),
                x=0.02,
                xanchor='left'
            ),
            xaxis=dict(
                showgrid=False,
                title='',
                tickfont=dict(size=14, color=text_color)
            ),
            yaxis=dict(
                showgrid=True,
                gridcolor=grid_color,
                title='Lượt đăng kí',
                titlefont=dict(size=18, color=text_color),
                tickfont=dict(size=14, color=text_color)
            ),
            height=500,
            margin=dict(l=20, r=20, t=50, b=20),
            barmode='group',
            bargap=0.3,
            legend=dict(
                font=dict(color=text_color, size=16)
            )
        )
        
        st.plotly_chart(fig_bar, use_container_width=True)

    with col2:
        # Pie chart
        
        # Calculate distribution based on label
        # label=1 means dropout (bỏ học), label=0 means continue (không bỏ học)
        dropout = df['label'].sum()  # Students who dropped out
        continue_study = len(df) - dropout  # Students who continued
        
        labels_pie = ['Không bỏ học', 'Bỏ học']
        values_pie = [continue_study, dropout]
        colors_pie = ['#48bb78', '#ed8936']
        
        fig_pie = go.Figure(data=[go.Pie(
            labels=labels_pie,
            values=values_pie,
            hole=0.5,
            marker=dict(colors=colors_pie),
            textinfo='percent',
            textfont=dict(color='#ffffff', size=20)
        )])
        
        # Add center annotation
        total_count = len(df)
        
        fig_pie.update_layout(
            plot_bgcolor=bg_color,
            paper_bgcolor=bg_color,
            font=dict(color=text_color, size=14),
            title=dict(
                text='Phân phối học viên bỏ học và không bỏ học',
                font=dict(size=18, color=text_color, family='Arial, sans-serif'),
                x=0.5,
                xanchor='center'
            ),
            height=600,
            margin=dict(l=20, r=20, t=70,b=20),
            showlegend=True,
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=-0.2,
                xanchor="center",
                x=0.5,
                font=dict(size=20, color=text_color)
            ),
            annotations=[dict(
                text=f'Tổng cộng<br>{total_count:,}',
                x=0.5, y=0.5,
                font=dict(size=24, color=text_color),
                showarrow=False
            )]
        )
        
        st.plotly_chart(fig_pie, use_container_width=True)
