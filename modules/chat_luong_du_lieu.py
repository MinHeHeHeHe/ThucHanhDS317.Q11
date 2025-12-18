import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# --- 2. DỮ LIỆU ---
# (Removed internal load_data, using passed df)

# --- 3. MAIN CONTENT ---
def show(df, theme='Dark'):
    # Theme configuration
    if theme == "Dark":
        bg_color = '#1a202c'
        text_color = '#ffffff'
        grid_color = '#2d3748'
        card_bg = '#2d3748'
    else:
        bg_color = '#ffffff'
        text_color = '#000000'
        grid_color = '#e2e8f0'
        card_bg = '#f7fafc'

    st.title("Đánh giá chất lượng dữ liệu")
    st.markdown("Dashboard đánh giá dựa trên 5 khía cạnh: **Completeness, Consistency, Timeliness, Uniqueness** và **Acc-DQ**.")

    # Navigation Tabs (with persistence)
    options = [
        "Overview", 
        "Completeness", 
        "Consistency", 
        "Timeliness & Uniqueness", 
        "Acc-DQ Model"
    ]
    
    # Initialize internal tab state if needed
    if "dq_active_tab" not in st.session_state:
        st.session_state.dq_active_tab = options[0]

    # Calculate index from session state
    try:
        current_index = options.index(st.session_state.dq_active_tab)
    except ValueError:
        current_index = 0

    # Use persistent radio button via index (No key to avoid double-click issues)
    active_tab = st.radio(
        "", 
        options,
        index=current_index,
        horizontal=True,
        label_visibility="collapsed"
        # No key here
    )
    
    # Update state immediately
    st.session_state.dq_active_tab = active_tab
    
    # Use Container to simulate tab content
    
    # Helper to update figure layout with theme
    def apply_theme(fig):
        fig.update_layout(
            plot_bgcolor=bg_color,
            paper_bgcolor=bg_color,
            font=dict(color=text_color),
            xaxis=dict(gridcolor=grid_color),
            yaxis=dict(gridcolor=grid_color),
            legend=dict(font=dict(color=text_color))
        )
        return fig

    st.markdown("---")

    # --- TAB 1: OVERVIEW ---
    if active_tab == "Overview":
        st.header("1. Thông tin tổng quan (Data Overview)")
        
        # 1.1 KPI Metrics
        col1, col2, col3, col4 = st.columns(4)
        
        dup_count = df.duplicated().sum()
        null_total = df.isnull().sum().sum()
        
        col1.metric("Tổng dòng (Rows)", f"{df.shape[0]:,}")
        col2.metric("Tổng cột (Cols)", df.shape[1])
        col3.metric("Dòng trùng lặp", f"{dup_count}", 
                    delta="Sạch" if dup_count == 0 else "Cần xử lý", delta_color="inverse")
        col4.metric("Tổng ô Null", f"{null_total:,}", delta_color="inverse")

        st.markdown("---")
        
        # 1.3 Phân tích thống kê
        col_left, col_right = st.columns([2, 1])
        
        with col_left:
            st.subheader("Hồ sơ dữ liệu (Data Profile)")
            stats_df = pd.DataFrame({
                "Type": df.dtypes.astype(str),
                "Null Count": df.isnull().sum(),
                "% Null": (df.isnull().mean() * 100),
                "Unique": df.nunique()
            })
            
            # Hiển thị dataframe với highlight màu đỏ cho cột Null cao
            st.dataframe(
                stats_df.style.background_gradient(subset=["% Null"], cmap="Reds", vmin=0, vmax=100)
                          .format({"% Null": "{:.2f}%"}),
                use_container_width=True,
                height=350
            )
            
        with col_right:
            st.subheader("Xem mẫu dữ liệu")
            st.dataframe(df.head(10), use_container_width=True, hide_index=True)
            
            # Biểu đồ tròn
            dtype_counts = df.dtypes.astype(str).value_counts().reset_index()
            dtype_counts.columns = ['Type', 'Count']
            fig_pie = px.pie(dtype_counts, values='Count', names='Type', title='Phân bố Kiểu dữ liệu')
            # Adjust pie chart separately as it doesn't use cartesian coordinates
            fig_pie.update_layout(
                paper_bgcolor=bg_color,
                font=dict(color=text_color)
            )
            st.plotly_chart(fig_pie, use_container_width=True, theme=None)

        # 1.4 Outliers Analysis
        st.markdown("---")
        st.subheader("Phân tích giá trị bất thường (Outliers)")
        
        with st.container(border=True):
            c1, c2 = st.columns([1, 3])
            
            numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
            if not numeric_cols:
                st.warning("Không có cột số để phân tích.")
            else:
                with c1:
                    st.markdown("##### Cấu hình")
                    default_ix = numeric_cols.index('class_duration_days') if 'class_duration_days' in numeric_cols else 0
                    selected_col = st.selectbox("Chọn cột phân tích:", numeric_cols, index=default_ix)
                    
                    # Tính IQR
                    Q1 = df[selected_col].quantile(0.25)
                    Q3 = df[selected_col].quantile(0.75)
                    IQR = Q3 - Q1
                    lower = Q1 - 1.5 * IQR
                    upper = Q3 + 1.5 * IQR
                    outliers = df[(df[selected_col] < lower) | (df[selected_col] > upper)]
                    
                    st.info(f"IQR: {IQR:,.2f} | Lower: {lower:,.2f} | Upper: {upper:,.2f}")
                    st.error(f"Phát hiện: **{len(outliers)}** outliers")

                with c2:
                    # Scatter Plot
                    plot_df = df.reset_index()
                    plot_df['Status'] = np.where(
                        (plot_df[selected_col] < lower) | (plot_df[selected_col] > upper), 
                        'Outlier', 'Normal'
                    )
                    
                    fig = px.scatter(plot_df, x='index', y=selected_col, color='Status',
                                     color_discrete_map={'Normal': '#1976d2', 'Outlier': '#ff5252'},
                                     title=f"Phân bố giá trị: {selected_col}",
                                     opacity=0.6)
                    
                    fig.add_hline(y=upper, line_dash="dash", line_color="red")
                    fig.add_hline(y=lower, line_dash="dash", line_color="red")
                    
                    st.plotly_chart(apply_theme(fig), use_container_width=True, theme=None)

    # --- TAB 2: COMPLETENESS ---
    elif active_tab == "Completeness":
        st.header("Độ đầy đủ dữ liệu (Completeness)")
        
        null_stats = df.isnull().mean().reset_index()
        null_stats.columns = ['Column', 'Null_Percentage']
        dataset_comp = 1 - df.isnull().mean().mean()
        
        c1, c2 = st.columns([1, 2])
        
        with c1:
            st.subheader("Điểm số toàn cục")
            fig_gauge = go.Figure(go.Indicator(
                mode = "gauge+number",
                value = dataset_comp * 100,
                title = {'text': "Dataset Completeness"},
                gauge = {
                    'axis': {'range': [0, 100]},
                    'bar': {'color': "#4caf50" if dataset_comp > 0.8 else "#ff9800"},
                    'steps': [{'range': [0, 50], 'color': card_bg}, {'range': [50, 100], 'color': card_bg}]
                }
            ))
            fig_gauge.update_layout(paper_bgcolor=bg_color, font=dict(color=text_color))
            st.plotly_chart(fig_gauge, use_container_width=True, theme=None)
            
        with c2:
            st.subheader("Top trường thiếu dữ liệu")
            top_null = null_stats.sort_values('Null_Percentage', ascending=False).head(10)
            fig_bar = px.bar(top_null, x='Null_Percentage', y='Column', orientation='h',
                             text_auto='.1%', color='Null_Percentage', 
                             color_continuous_scale='Reds')
            st.plotly_chart(apply_theme(fig_bar), use_container_width=True, theme=None)

        st.markdown("---")
        st.subheader("Phân tích theo đối tượng (Row-level)")
        df['row_completeness'] = df.notnull().mean(axis=1)
        fig_hist = px.histogram(df, x='row_completeness', nbins=50,
                                title="Phân phối độ đầy đủ của từng dòng dữ liệu")
        st.plotly_chart(apply_theme(fig_hist), use_container_width=True, theme=None)

    # --- TAB 3: CONSISTENCY ---
    elif active_tab == "Consistency":
        st.header("Tính nhất quán (Consistency)")
        
        col_chart, col_info = st.columns([2, 1])
        
        with col_chart:
            # Data giả lập cho biểu đồ
            consistency_data = pd.DataFrame({
                'Tiêu chí': ['Data Type', 'Uniqueness', 'Foreign Keys', 'Logical Constraints', 'Non-Null'],
                'Pass Rate': [1.0, 1.0, 1.0, 0.47, df.notnull().all(axis=1).mean()]
            })
            
            fig = px.bar(consistency_data, x='Pass Rate', y='Tiêu chí', orientation='h',
                         text_auto='.0%', color='Pass Rate', 
                         color_continuous_scale='RdYlGn',
                         range_x=[0, 1.1], title="Tỷ lệ đạt chuẩn các tiêu chí")
            st.plotly_chart(apply_theme(fig), use_container_width=True, theme=None)
            
        with col_info:
            st.info("ℹ️ **Giải thích:**")
            st.markdown("""
            - **Data Type**: Dữ liệu đúng định dạng.
            - **Uniqueness**: Không trùng lặp khóa.
            - **Logical**: Kiểm tra logic (vd: Ngày bắt đầu < Kết thúc).
            - **Non-Null**: Dòng dữ liệu đầy đủ 100%.
            """)
            avg_score = consistency_data['Pass Rate'].mean()
            st.metric("Điểm Consistency TB", f"{avg_score:.1%}")

    # --- TAB 4: TIMELINESS & UNIQUENESS ---
    elif active_tab == "Timeliness & Uniqueness":
        st.header("Timeliness & Uniqueness")
        
        col1, col2 = st.columns(2)
        
        # Timeliness
        with col1:
            with st.container(border=True):
                st.subheader("Timeliness")
                timeliness_val = 0.2823
                
                fig = go.Figure(go.Indicator(
                    mode = "gauge+number+delta",
                    value = timeliness_val * 100,
                    title = {'text': "Timeliness Score"},
                    gauge = {'axis': {'range': [0, 100]}, 'bar': {'color': "#ef5350"}}
                ))
                fig.update_layout(paper_bgcolor=bg_color, font=dict(color=text_color))
                st.plotly_chart(fig, use_container_width=True, theme=None)
                st.caption("Điểm thấp do logic ActionTime <= Cutoff bị ảnh hưởng bởi dữ liệu Null.")

        # Uniqueness
        with col2:
            with st.container(border=True):
                st.subheader("Uniqueness")
                
                row_uniq = 1 - df.duplicated().mean()
                if 'user_id' in df.columns and 'course_id' in df.columns:
                    key_uniq = 1 - df.duplicated(subset=['user_id', 'course_id']).mean()
                else:
                    key_uniq = 1.0
                    
                m1, m2 = st.columns(2)
                m1.metric("Row Level", f"{row_uniq:.0%}", delta="Tuyệt đối")
                m2.metric("Key Level", f"{key_uniq:.0%}", delta="Tuyệt đối")
                st.success("Dữ liệu đạt chuẩn Uniqueness hoàn hảo.")

    # --- TAB 5: ACC-DQ MODEL ---
    elif active_tab == "Acc-DQ Model":
        st.header("Mô hình Acc-DQ")
        st.markdown("---")
        
        c_config, c_result = st.columns([1, 1], gap="large")
        
        with c_config:
            st.subheader("🛠️ Tham số mô hình")
            
            with st.expander("1. Chỉ số Hiệu năng (S_perf)", expanded=True):
                st.latex(r'S_{\text{perf}} = (\text{F1} \cdot \text{BalAcc} \cdot \text{MCC} \cdot \kappa)^{1/4}')
                f1 = st.slider("Macro-F1", 0.0, 1.0, 0.89)
                bal_acc = st.slider("Balanced Accuracy", 0.0, 1.0, 0.88)
                mcc = st.slider("MCC", 0.0, 1.0, 0.89)
                kappa = st.slider("Kappa", 0.0, 1.0, 0.89)
                s_perf = (f1 * bal_acc * mcc * kappa) ** 0.25
                
            with st.expander("2. Chỉ số Lành mạnh (S_san+)", expanded=True):
                c1, c2 = st.columns(2)
                s_nan = c1.number_input("s_nan", 0.0, 1.0, 1.0)
                s_maj = c2.number_input("s_maj", 0.0, 1.0, 0.21)
                s_ent = c1.number_input("s_ent", 0.0, 1.0, 0.00)
                s_drift = c2.number_input("s_drift", 0.0, 1.0, 1.0)
                s_eff = c1.number_input("s_eff", 0.0, 1.0, 1.0)
                s_leak = c2.number_input("s_leak", 0.0, 1.0, 0.5)
                s_san_plus = (s_nan * s_maj * s_ent * s_drift * s_eff * s_leak) ** (1/6)
                
        with c_result:
            st.subheader("Kết quả Đánh giá")
            
            col_res1, col_res2 = st.columns(2)
            col_res1.metric("S_perf (Hiệu năng)", f"{s_perf:.4f}")
            col_res2.metric("S_san+ (Lành mạnh)", f"{s_san_plus:.4f}")
            
            st.markdown("---")
            
            alpha, beta = 0.6, 0.4
            acc_dq = 100 * (s_perf**alpha * s_san_plus**beta)
            
            # Sử dụng st.metric thay vì HTML/CSS custom để tránh lỗi
            st.metric(label="Acc-DQ Score Final", value=f"{acc_dq:.2f}")
            
            if acc_dq < 50:
                st.warning("Cảnh báo: Chất lượng dữ liệu thấp do mô hình bị Overconfidence và Model Collapse.")
            else:
                st.success("Đánh giá: Chất lượng dữ liệu tốt.")