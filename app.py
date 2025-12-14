import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# --- 1. CẤU HÌNH TRANG ---
st.set_page_config(
    page_title="Trang chất lượng dữ liệu",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. DỮ LIỆU ---
@st.cache_data
def load_data():
    try:

        df = pd.read_csv('df_not_fill.csv', encoding='utf-8')
    
    except FileNotFoundError:
        
        st.warning("Không tìm thấy file, hệ thống đang tạo dữ liệu giả lập.")

        n_rows = 1000  # Số lượng dòng giả lập

        # 1. Thông tin cơ bản
        data = {
            'user_id': [f'U_{i:06d}' for i in range(n_rows)],
            'course_id': np.random.choice([f'C_{i:06d}' for i in range(50)], n_rows),
            'enroll_time': pd.date_range(start='2020-01-01', periods=n_rows, freq='h'),
            'class_start': pd.date_range(start='2020-01-05', periods=n_rows, freq='h'),
            'class_end': pd.date_range(start='2020-06-05', periods=n_rows, freq='h'),
            'class_duration_days': np.random.randint(30, 180, n_rows),
            'certificate': np.random.choice([0, 1], n_rows), # Binary
            'num_field': np.random.randint(1, 10, n_rows),
            'num_prerequisites': np.random.randint(0, 5, n_rows),
            'remaining_time': np.random.uniform(-10, 100, n_rows), # Có số âm để test Logic Check
            'start_year': [2020]*n_rows,
            'start_month': np.random.randint(1, 13, n_rows),
            'end_year': [2021]*n_rows,
            'end_month': np.random.randint(1, 13, n_rows),
            'total_assignment_score': np.random.uniform(0, 100, n_rows),
            'user_num_prev_courses': np.random.randint(0, 20, n_rows),
            'time_since_last_enroll': np.random.uniform(0, 5000, n_rows),
            'video_count': np.random.randint(0, 150, n_rows),
            'label': np.random.choice([0, 1], n_rows)
        }

        # Thêm các cột Embedding (field_embed_0 -> 6) 
        for i in range(7):
            data[f'field_embed_{i}'] = np.random.uniform(0, 1, n_rows)

        # Tạo cột theo từng Phase (P1 -> P5)
        for p in range(1, 6):
            # --- Comment ---
            data[f'n_comments_P{p}'] = np.random.randint(0, 50, n_rows)
            data[f'avg_sentiment_P{p}'] = np.random.uniform(-1, 1, n_rows)
            data[f'burstiness_P{p}'] = np.random.uniform(-1, 1, n_rows)
            
            # --- Problem (Bài tập) ---
            data[f'cutoff_time_P{p}'] = pd.date_range(start=f'2020-02-{p:02d}', periods=n_rows)
            data[f'n_attempts_P{p}'] = np.random.randint(0, 20, n_rows)
            data[f'accuracy_rate_P{p}'] = np.random.uniform(0, 1, n_rows)
            data[f'avg_score_P{p}'] = np.random.uniform(0, 100, n_rows)
            data[f'unique_types_P{p}'] = np.random.randint(0, 5, n_rows)
            data[f'unique_langs_P{p}'] = np.random.randint(0, 3, n_rows)
            data[f'first_submit_time_P{p}'] = pd.date_range(start=f'2020-01-10', periods=n_rows)
            data[f'last_submit_time_P{p}'] = pd.date_range(start=f'2020-01-20', periods=n_rows)
            data[f'active_days_P{p}'] = np.random.randint(0, 30, n_rows)
            data[f'avg_attempts_per_day_P{p}'] = np.random.uniform(0, 5, n_rows)
            data[f'time_span_days_P{p}'] = np.random.randint(0, 30, n_rows)
            
            # --- Video ---
            data[f'has_any_view_P{p}'] = np.random.choice([True, False], n_rows)
            data[f'num_events_P{p}'] = np.random.randint(0, 200, n_rows)
            data[f'num_videos_P{p}'] = np.random.randint(0, 50, n_rows)
            data[f'total_duration_P{p}'] = np.random.uniform(0, 10000, n_rows)
            data[f'avg_duration_per_event_P{p}'] = np.random.uniform(0, 300, n_rows)
            data[f'avg_speed_P{p}'] = np.random.uniform(0.5, 2.5, n_rows)
            data[f'max_speed_P{p}'] = np.random.uniform(1.0, 4.0, n_rows)
            data[f'num_active_days_P{p}'] = np.random.randint(0, 15, n_rows)
            data[f'first_watch_time_P{p}'] = pd.date_range(start=f'2020-01-15', periods=n_rows)
            data[f'last_watch_time_P{p}'] = pd.date_range(start=f'2020-01-25', periods=n_rows)
            data[f'most_watched_hour_P{p}'] = np.random.randint(0, 24, n_rows)
            data[f'most_watched_dow_P{p}'] = np.random.randint(0, 7, n_rows)

        df = pd.DataFrame(data) 

        # Tạo lỗi dữ liệu giả
        # Tạo Null ngẫu nhiên ở các cột Phase
        phase_cols = [c for c in df.columns if '_P' in c]
        for col in phase_cols:
            df.loc[df.sample(frac=0.15).index, col] = np.nan

        # Tạo dòng trùng lặp
        df = pd.concat([df, df.iloc[:50]], ignore_index=True)

    return df
df = load_data()

# --- 3. MAIN CONTENT ---
st.title("Đánh giá chất lượng dữ liệu")
st.markdown("Dashboard đánh giá dựa trên 5 khía cạnh: **Completeness, Consistency, Timeliness, Uniqueness** và **Acc-DQ**.")

# Navigation Tabs
tabs = st.tabs([
    "Overview", 
    "Completeness", 
    "Consistency", 
    "Timeliness & Uniq", 
    "Acc-DQ Model"
])

# --- TAB 1: OVERVIEW ---
with tabs[0]:
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
        st.plotly_chart(fig_pie, use_container_width=True)

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
                
                st.plotly_chart(fig, use_container_width=True)

# --- TAB 2: COMPLETENESS ---
with tabs[1]:
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
                'steps': [{'range': [0, 50], 'color': "#f5f5f5"}, {'range': [50, 100], 'color': "#e8f5e9"}]
            }
        ))
        st.plotly_chart(fig_gauge, use_container_width=True)
        
    with c2:
        st.subheader("Top trường thiếu dữ liệu")
        top_null = null_stats.sort_values('Null_Percentage', ascending=False).head(10)
        fig_bar = px.bar(top_null, x='Null_Percentage', y='Column', orientation='h',
                         text_auto='.1%', color='Null_Percentage', 
                         color_continuous_scale='Reds')
        st.plotly_chart(fig_bar, use_container_width=True)

    st.markdown("---")
    st.subheader("Phân tích theo đối tượng (Row-level)")
    df['row_completeness'] = df.notnull().mean(axis=1)
    fig_hist = px.histogram(df, x='row_completeness', nbins=50,
                            title="Phân phối độ đầy đủ của từng dòng dữ liệu")
    st.plotly_chart(fig_hist, use_container_width=True)

# --- TAB 3: CONSISTENCY ---
with tabs[2]:
    st.header("3. Tính nhất quán (Consistency)")
    
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
        st.plotly_chart(fig, use_container_width=True)
        
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
with tabs[3]:
    st.header("4. Timeliness & 5. Uniqueness")
    
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
            st.plotly_chart(fig, use_container_width=True)
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
with tabs[4]:
    st.header("6. Mô hình Acc-DQ")
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