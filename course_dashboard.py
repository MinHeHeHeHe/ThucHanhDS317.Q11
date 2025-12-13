import streamlit as st
import pandas as pd
import os
import plotly.express as px
import plotly.graph_objects as go
from modules.data_loader import load_users, load_courses


def build_behavior_timeseries(df_users_course):
    """
    Trả về dataframe:
    Tháng | Video Views | Attempts | Label
    """
    records = []

    for _, row in df_users_course.iterrows():
        enroll_time = pd.to_datetime(row['enroll_time'])
        duration = row.get('class_duration_days', 0)

        if pd.isna(enroll_time) or duration <= 0:
            continue

        phase_ratios = [0.2, 0.4, 0.6, 0.8, 0.9]

        for i, r in enumerate(phase_ratios, 1):
            phase_date = enroll_time + pd.Timedelta(days=int(duration * r))
            month_label = phase_date.strftime("%Y-%m")

            records.append({
                "Month": month_label,
                "Video Views": row.get(f"num_events_P{i}", 0),
                "Attempts": row.get(f"n_attempts_P{i}", 0),
                "Label": row.get("label", 0)
            })

    return pd.DataFrame(records)

# Khóa Session State mới cho User Detail
if 'current_user_id' not in st.session_state:
    st.session_state.current_user_id = None
    
# --- Hàm hiển thị nội dung User Dashboard ---
def display_user_dashboard(USER_ID: str):
    """Hiển thị giao diện chi tiết của học viên."""
    
    st.header(f"Chi tiết học viên: **{USER_ID}**")
    st.markdown("---")
    
    # --- Đọc dữ liệu user và course ---
    try:
        df_users = load_users()
        df_courses = load_courses()
        
        # Lấy COURSE_ID từ session state
        COURSE_ID = st.session_state.selected_course_id
        
        # Lọc dữ liệu user
        user_data = df_users[(df_users['user_id'] == USER_ID) & (df_users['course_id'] == COURSE_ID)]
        course_data = df_courses[df_courses['course_id'] == COURSE_ID].iloc[0]
        
        if user_data.empty:
            st.error(f"Không tìm thấy dữ liệu cho User ID: {USER_ID}")
            return
        
        user = user_data.iloc[0]
        enroll_time_formatted = pd.to_datetime(user['enroll_time']).strftime('%m/%d/%Y')
        
    except Exception as e:
        st.error(f"Lỗi khi đọc dữ liệu: {e}")
        return
    
    col1, col2, col3, col4, col5 = st.columns([1.5, 1, 1, 1,1])
    
    # CARD 1: Thông tin User
    with col1:
        st.markdown(f"""
        <div class='metric-card'>
            <div class='metric-label'>Thông tin cơ bản</div>
            <div style='font-size: 14px; line-height: 1.8;'>
                <b>User ID:</b> {user.get('user_id', '-')}<br>
                <b>Course ID:</b> {user.get('course_id', '-')}<br>
                <b>Ngày đăng kí:</b> {enroll_time_formatted}<br>
                <b>Số khóa học:</b> {int(user.get('user_num_prev_courses', 0) or 0) + 1}<br>
                <b>Thời gian còn lại:</b> {user.get('remaining_time', 0):.0f} ngày
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # CARD 2: Video Count
    with col2:
        num_videos = int(user.get('num_videos_P5', 0) or 0)
        st.markdown(f"""
        <div class='metric-card'>
            <div class='metric-label'>Video</div>
            <div class='metric-value'>{num_videos}</div>
            <div style='font-size: 12px; color: #666; margin-top: 8px;'>Đã xem</div>
        </div>
        """, unsafe_allow_html=True)
    
    # CARD 3: Comment Count
    with col3:
        n_comments = int(user.get('n_comments_P5', 0) or 0)
        st.markdown(f"""
        <div class='metric-card'>
            <div class='metric-label'>Comment</div>
            <div class='metric-value'>{n_comments}</div>
            <div style='font-size: 12px; color: #666; margin-top: 8px;'>Số bình luận</div>
        </div>
        """, unsafe_allow_html=True)
    
    # CARD 4: Exercise Count
    with col4:
        n_attempts = int(user.get('n_attempts_P5', 0) or 0)
        st.markdown(f"""
        <div class='metric-card'>
            <div class='metric-label'>Problem</div>
            <div class='metric-value'>{n_attempts}</div>
            <div style='font-size: 12px; color: #666; margin-top: 8px;'>Đã làm</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")

# CARD 4: Gauge Chart - Tiến trình Thời gian
    with col5:        
        # Dữ liệu
        duration_days = user.get('class_duration_days', 0)
        remaining_time = user.get('remaining_time', 0)
        
        # Thời gian đã trôi qua = Duration - Remaining
        time_elapsed = duration_days - remaining_time
        
        # Phần trăm đã trôi qua
        time_progress_percent = (time_elapsed / duration_days) * 100 if duration_days > 0 else 0
        
        # Vẽ Gauge Chart
        fig_time_gauge = go.Figure(go.Indicator(
            mode = "gauge+number",
            value = time_progress_percent,
            title = {'text': "Tiến trình Thời gian (%)", 'font': {'size': 14}},
            gauge = {
                'axis': {'range': [None, 100], 'tickwidth': 1},
                'bar': {'color': "darkblue"},
                'steps': [
                    {'range': [0, 50], 'color': 'lightgray'},
                    {'range': [50, 100], 'color': 'gray'}
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': 90
                }
            }
        ))
        
        fig_time_gauge.update_layout(
            height=180, 
            margin=dict(l=10, r=10, t=40, b=10)
        )
        st.plotly_chart(fig_time_gauge, use_container_width=True)

    # --- Hàng 2: Biểu đồ ---
    col_chart_left, col_chart_right = st.columns(2)
    
    # CARD 5: Phân phối điểm số 
    with col_chart_left:
        with st.container(border=True):
            st.subheader("Phân phối điểm số")
            
            # Tính toán
            num_videos_watched = user.get('num_videos_P5', 0) or 0
            total_videos = course_data.get('video_count', 0) or 0
            accuracy_rate = user.get('accuracy_rate_P5', 0) or 0
            
            video_percentage = (num_videos_watched / total_videos) * 100 if total_videos > 0 else 0
            exercise_percentage = accuracy_rate * 100
            
            # DataFrame cho biểu đồ
            df_scores = pd.DataFrame({
                'Hoạt động': ['Video', 'Exercise'],
                'Điểm (%)': [video_percentage, exercise_percentage],
                'Nhãn': [f"{video_percentage:.1f}%", f"{exercise_percentage:.1f}%"]
            })
            
            # Biểu đồ cột
            color_map = {'Video': "#852D95", 'Exercise': "#1C70CA"}
            fig = px.bar(
                df_scores,
                x='Hoạt động',
                y='Điểm (%)',
                text='Nhãn',
                color='Hoạt động',
                color_discrete_map=color_map,
                height=380
            )
            
            fig.update_traces(
                textposition='inside',
                textfont=dict(color='white', size=16),
                marker_line_width=0
            )
            
            fig.update_layout(
                title=dict(text='Phân phối điểm số', x=0.5, font=dict(size=18)),
                yaxis=dict(
                    title='Điểm (%)',
                    range=[0, 100],
                    tickvals=[0, 20, 40, 60, 80, 100],
                    showgrid=True,
                    gridcolor='#E6E6E6'
                ),
                xaxis=dict(title='Hoạt động'),
                showlegend=False,
                plot_bgcolor='white',
                margin=dict(l=20, r=20, t=60, b=20)
            )
            
            fig.update_traces(
                hovertemplate="<b>%{x}</b><br>Điểm: %{y:.1f}%<extra></extra>"
            )
            
            st.plotly_chart(fig, use_container_width=True)
    
    # CARD 6: Lượt xem video và làm bài tập theo giai đoạn (Biểu đồ đường)
    with col_chart_right:
        with st.container(border=True):
            st.subheader("Lượt xem video và làm bài tập theo giai đoạn")
            
            # Định nghĩa các giai đoạn
            periods_percent = [0.20, 0.40, 0.60, 0.80, 0.90]
            video_cols = [f'num_events_P{i}' for i in range(1, 6)]
            attempt_cols = [f'n_attempts_P{i}' for i in range(1, 6)]
            
            # Tính toán nhãn thời gian
            duration_days = user.get('class_duration_days', 0)
            time_labels = []
            
            if duration_days > 0:
                enroll_ts = pd.to_datetime(user.get('enroll_time', None))
                if pd.isna(enroll_ts):
                    time_labels = [f'P{i} ({int(p*100)}%)' for i, p in enumerate(periods_percent, 1)]
                else:
                    for percent in periods_percent:
                        days_added = int(duration_days * percent)
                        new_date = enroll_ts + pd.Timedelta(days=days_added)
                        time_labels.append(new_date.strftime('%b %Y'))
            else:
                time_labels = [f'P{i} ({int(p*100)}%)' for i, p in enumerate(periods_percent, 1)]
            
            # Trích xuất dữ liệu
            video_views = [user.get(col, 0) for col in video_cols]
            attempt_attempts = [user.get(col, 0) for col in attempt_cols]
            
            # DataFrame cho biểu đồ
            df_chart = pd.DataFrame({
                'Giai đoạn': time_labels,
                'Lượt xem video': video_views,
                'Lượt làm bài tập': attempt_attempts
            })
            
            # Vẽ biểu đồ đường
            if not df_chart.empty:
                fig_monthly = px.line(
                    df_chart,
                    x='Giai đoạn',
                    y=['Lượt xem video', 'Lượt làm bài tập'],
                    markers=True,
                    height=380
                )
                
                fig_monthly.update_layout(
                    title='Lượt xem video và làm bài tập theo giai đoạn',
                    xaxis_title='Giai đoạn',
                    yaxis_title='Số lượt',
                    hovermode="x unified",
                    legend=dict(x=0, y=1)
                )
                
                st.plotly_chart(fig_monthly, use_container_width=True)
            else:
                st.info("⚠️ Không có dữ liệu sự kiện theo giai đoạn.")


    # Số ngày Hoạt động (Video vs Submit) (Biểu đồ Cột Stacked)
    
    st.subheader("Số ngày hoạt động (Nộp bài vs. Xem Video)")
    
    active_days_video_cols = [f'num_active_days_P{i}' for i in range(1, 6)]
    active_days_submit_cols = [f'active_days_P{i}' for i in range(1, 6)]
    
    # Đảm bảo `Giai đoạn` cùng độ dài với các cột active days (5 mốc)
    df_active = pd.DataFrame({
        'Giai đoạn': time_labels,
        'Video Active Days': [user.get(col, 0) for col in active_days_video_cols],
        'Submit Active Days': [user.get(col, 0) for col in active_days_submit_cols]
    })
    
    # Melt để vẽ cột nhóm (grouped bar)
    df_melted_active = df_active.melt(
        id_vars='Giai đoạn', 
        value_vars=['Video Active Days', 'Submit Active Days'],
        var_name='Hoạt động', 
        value_name='Số ngày'
    )
    
    fig_active = px.bar(
        df_melted_active,
        x='Giai đoạn',
        y='Số ngày',
        color='Hoạt động',
        barmode='group', # Grouped Bar Chart
        height=350
    )
    
    fig_active.update_layout(
        title_text="Số ngày Hoạt động theo Giai đoạn",
        xaxis_tickangle=-45
    )
    st.plotly_chart(fig_active, use_container_width=True)


    # CARD : Biểu đồ Donut cho Nhãn Đầu ra (Label)
    st.subheader("Dự đoán Khả năng Bỏ học")


def navigate_to_user_detail(user_id: str):
    """Chuyển sang chế độ xem chi tiết học viên."""
    st.session_state.current_user_id = user_id
    st.session_state.current_view = 'user_detail' 

def navigate_to_dashboard():
    """Chuyển sang Course Dashboard, ẩn User ID."""
    st.session_state.current_user_id = None # Reset User ID
    st.session_state.current_view = 'dashboard'

def navigate_to_user_list():
    """Chuyển sang User List, ẩn User ID."""
    st.session_state.current_user_id = None # Reset User ID
    st.session_state.current_view = 'user_list'


# --- Cấu hình phân trang User List ---
def go_to_user_page(page_num):
    """Cập nhật trang hiện tại."""
    st.session_state.user_page = page_num

def display_user_list(COURSE_ID):
    """Hiển thị nội dung User List trong tab."""
    
    if 'last_course_id' not in st.session_state or st.session_state.last_course_id != COURSE_ID:
        st.session_state.user_page = 1
        st.session_state.last_course_id = COURSE_ID

    # Đọc dữ liệu user
    try:
        df_users = load_users()
        df_filtered_users = df_users[df_users['course_id'] == COURSE_ID].copy()
        if 'enroll_time' in df_filtered_users.columns:
            df_filtered_users['enroll_time'] = pd.to_datetime(df_filtered_users['enroll_time']).dt.strftime('%m/%d/%Y')
    except FileNotFoundError:
        st.error(f"Lỗi: Không tìm thấy file. Vui lòng kiểm tra đường dẫn.")
        return
    except Exception as e:
        st.error(f"Lỗi khi đọc file CSV: {e}")
        return

    st.header("Danh sách học viên")
    total_users = len(df_filtered_users)
    st.markdown(f"Quản lý và xem tất cả người dùng hệ thống ({total_users} học viên)")

    # Thanh tìm kiếm
    search_user = st.text_input("🔍 Tìm kiếm bằng ID ...", placeholder="Tìm kiếm bằng ID ...")

    if search_user:
        st.session_state.user_page = 1
        df_display = df_filtered_users[
            df_filtered_users['user_id'].astype(str).str.contains(search_user, case=False, na=False)
        ]
    else:
        df_display = df_filtered_users.copy()


    # --- Cấu hình Phân trang ---
    PAGE_SIZE = 10 
    total_display_users = len(df_display)
    total_pages = (total_display_users + PAGE_SIZE - 1) // PAGE_SIZE 
    if total_pages == 0: total_pages = 1

    # Đảm bảo trang hiện tại không vượt quá giới hạn
    if st.session_state.user_page > total_pages:
        st.session_state.user_page = total_pages
    elif st.session_state.user_page < 1:
        st.session_state.user_page = 1

    start_index = (st.session_state.user_page - 1) * PAGE_SIZE
    end_index = start_index + PAGE_SIZE
    users_on_page = df_display.iloc[start_index:end_index]


    # --- Hiển thị Bảng Người Dùng ---
    st.markdown("---")

    col_avatar, col_user_id, col_enroll, col_view = st.columns([1, 3, 2, 1])
    with col_avatar: st.markdown("**AVATAR**")
    with col_user_id: st.markdown("**USER ID**")
    with col_enroll: st.markdown("**ĐĂNG KÝ**")
    with col_view: st.markdown("**XEM**")
    st.markdown("---")

    if total_display_users > 0:
        for index, user in users_on_page.iterrows():
            col_avatar, col_user_id, col_enroll, col_view = st.columns([1, 3, 2, 1])
            
            with col_avatar:
                st.markdown("👤")
            with col_user_id:
                st.markdown(f"**{user['user_id']}**")
            with col_enroll:
                st.markdown(f"🗓️ {user['enroll_time']}")
            with col_view:
                # Dùng on_click callback để chuyển sang User Dashboard
                st.button(":material/visibility:", 
                            key=f"user_view_{user['user_id']}_{index}",
                            on_click=lambda uid=user['user_id']: navigate_to_user_detail(uid))
            
            st.markdown("---")
    else:
        st.info("Không tìm thấy học viên nào phù hợp với tìm kiếm.")


    # --- Hiển thị Phân trang (Pagination) ---
    col_prev, col_pages, col_next = st.columns([1, 4, 1])

    with col_prev:
        st.button("⟨⟨", disabled=(st.session_state.user_page == 1), key="user_prev_btn_tab",
                    on_click=lambda: go_to_user_page(st.session_state.user_page - 1))

    with col_next:
        st.button("⟩⟩", disabled=(st.session_state.user_page == total_pages or total_pages == 0), key="user_next_btn_tab",
                    on_click=lambda: go_to_user_page(st.session_state.user_page + 1))
            
    with col_pages:
        st.markdown(f"<div style='text-align: center; padding-top: 10px;'>Trang {st.session_state.user_page} / {total_pages}</div>", unsafe_allow_html=True)

# --- Hàm hiển thị Course Dashboard ---

def display_course_dashboard(course, COURSE_ID):
    st.header("Tổng quan Khóa học")

    # Hàng 1: Ngày tháng, Video, Bài tập, Certificate
    col1, col2, col3, col4 = st.columns([2, 1.5, 1.5, 1.5])
    
    # 1. Start/End Dates
    with col1:
        st.markdown(
            f"""
            <div class='metric-card' style='padding: 18px 24px;'>
                <div class='metric-label'>Thời gian diễn ra</div>
                <div class='metric-value' style='font-size: 24px; font-weight: 500;'>
                    🗓️ {course['class_start']} <br> 
                    🗓️ {course['class_end']}
                </div>
            </div>
            """, 
            unsafe_allow_html=True
        )

    # 2. Video Count
    with col2:
        st.markdown(f"""
        <div class='metric-card'>
            <div class='metric-label'>Số Video</div>
            <div class='metric-value'>{course['video_count']:,}</div>
        </div>
        """, unsafe_allow_html=True)

    # 3. Exercise Count
    with col3:
        st.markdown(f"""
        <div class='metric-card'>
            <div class='metric-label'>Số Bài tập</div>
            <div class='metric-value'>{course['exercise_count']:,}</div>
        </div>
        """, unsafe_allow_html=True)

    # 4. Certificate Status
    with col4:
        if course['certificate'] == 1:
            icon_html = '<span class="material-symbols-outlined" style="font-size:36px; color:#F19E39; line-height: 1;">workspace_premium</span>'
            status_text = "Certificate"
            value_class = 'metric-label'
        else:
            icon_html = '<span class="material-symbols-outlined" style="font-size:36px; color:#999; line-height: 1;">unlicense</span>'
            status_text = "No Certificate"
            value_class = 'metric-label' 
        
        st.markdown(f"""
        <div class='metric-card' style='text-align: center;'>
            <div class='metric-label' style='margin-bottom: 5px;'>Chứng chỉ</div>
            <div class='metric-value' style='display: flex; flex-direction: column; justify-content: center; align-items: center;'>
                {icon_html}
                <div style='font-size: 18px; font-weight: 600; color: #fff; margin-top: 5px;'>{status_text}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("---")

    ## Phân phối Nội dung và Điểm

    col_left, col_right = st.columns(2)

    # --- PHẦN TRÁI: Phân phối điểm trong khóa học (Biểu đồ tròn) ---
    with col_left:
        st.header("Phân phối điểm trong khóa học")
        score_columns = ['assignment', 'video', 'exam', 'discussion', 'article']
        score_data = course[score_columns].fillna(0)
        df_scores = pd.DataFrame({
            'Phần': score_data.index,
            'Tỷ lệ': score_data.values
        }).query('`Tỷ lệ` > 0')

        if not df_scores.empty:
            fig = px.pie(
                df_scores, 
                values='Tỷ lệ', 
                names='Phần', 
                title='Tỷ lệ đóng góp của từng phần (Assignment, Exam, etc.)',
                hole=0.3
            )
            fig.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Không có dữ liệu phân phối điểm (assignment, video, exam, discussion, article) cho khóa học này.")

    # --- PHẦN PHẢI: Phân phối bỏ học trong toàn khóa ---
    with col_right:
        st.header("Dự đoán tỉ lệ bỏ học trong toàn khóa")
        
        try:
            df_users = load_users()
            
            course_users = df_users[df_users['course_id'] == COURSE_ID]
            
            if not course_users.empty and 'label' in course_users.columns:
                dropout_counts = course_users['label'].value_counts().reset_index()
                dropout_counts.columns = ['Trạng thái', 'Số lượng']
                
                # Map labels (0 -> Không bỏ học, 1 -> Bỏ học)
                dropout_counts['Trạng thái'] = dropout_counts['Trạng thái'].map({0: 'Không bỏ học', 1: 'Bỏ học'})
                
                # Create Chart
                fig_dropout = px.pie(
                    dropout_counts,
                    values='Số lượng',
                    names='Trạng thái',
                    title='Tỷ lệ bỏ học (Dropout Rate)',
                    color='Trạng thái',
                    hole=0.3
                )
                
                fig_dropout.update_traces(textposition='inside', textinfo='percent+label')
                st.plotly_chart(fig_dropout, use_container_width=True)
                
            else:
                st.info("Không có dữ liệu về trạng thái bỏ học (column 'label').")
                
        except Exception as e:
            st.error(f"Lỗi khi vẽ biểu đồ bỏ học: {e}")

    st.subheader("Hành vi học tập theo thời gian")

    try:
        df_users = load_users()
        df_users = df_users[df_users['course_id'] == COURSE_ID]

        periods = [0.2, 0.4, 0.6, 0.8, 0.9]
        video_cols = [f'num_events_P{i}' for i in range(1, 6)]
        attempt_cols = [f'n_attempts_P{i}' for i in range(1, 6)]

        # Tính mốc thời gian theo tháng-năm
        start_date = pd.to_datetime(course['class_start'])
        duration_days = course.get('class_duration_days', 0)

        time_labels = []
        for p in periods:
            d = start_date + pd.Timedelta(days=int(duration_days * p))
            time_labels.append(d.strftime('%d/%m/%Y'))

        df_behavior = pd.DataFrame({
            "Thời gian": time_labels,
            "Lượt xem video": df_users[video_cols].sum().values,
            "Lượt làm bài tập": df_users[attempt_cols].sum().values
        })

        fig_line = px.line(
            df_behavior,
            x="Thời gian",
            y=["Lượt xem video", "Lượt làm bài tập"],
            markers=True
        )

        fig_line.update_layout(
            height=420,
            yaxis_title="Số lượt",
            hovermode="x unified"
        )

        st.plotly_chart(fig_line, use_container_width=True)

    except Exception as e:
        st.warning(f"Không thể vẽ biểu đồ hành vi học tập: {e}")

    st.subheader("Mức độ tham gia theo giai đoạn (%)")

    df_percent = df_behavior.copy()
    df_percent["Video (%)"] = df_percent["Lượt xem video"] / df_percent["Lượt xem video"].max() * 100
    df_percent["Exercise (%)"] = df_percent["Lượt làm bài tập"] / df_percent["Lượt làm bài tập"].max() * 100

    fig_bar = px.bar(
        df_percent,
        x="Thời gian",
        y=["Video (%)", "Exercise (%)"],
        barmode="group"
    )

    fig_bar.update_layout(
        yaxis_title="Mức độ (%)",
        height=380
    )

    st.plotly_chart(fig_bar, use_container_width=True)



# --- Hàm điều hướng chính ---

def navigate_to_main_page():
    """Callback để quay lại danh sách khóa học (không gọi st.rerun)"""
    st.session_state.selected_course_id = None
    if 'khoa_show_dashboard' in st.session_state:
        del st.session_state.khoa_show_dashboard

# --- Hàm Show Chính (Áp dụng Tabs) ---

def show():
    # --- Cấu hình trang (Tùy chọn) ---
    try:
        st.set_page_config(layout="wide", page_title="Course Detail")
    except Exception:
        pass

    st.markdown("""
        <link href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@24,400,0,0"
            rel="stylesheet">
        <style>
        .material-symbols-outlined {
        font-variation-settings:
            'FILL' 1,
            'wght' 400,
            'GRAD' 0,
            'opsz' 24;
        vertical-align: middle;
        }
        </style>
    """, unsafe_allow_html=True)

    
    # --- Khởi tạo session state ---
    if 'user_page' not in st.session_state:
        st.session_state.user_page = 1
    if 'current_view' not in st.session_state:
        st.session_state.current_view = 'dashboard'
    if 'current_user_id' not in st.session_state:
        st.session_state.current_user_id = None
    
    # --- Kiểm tra ID khóa học ---
    if 'selected_course_id' not in st.session_state or st.session_state.selected_course_id is None:
        st.warning("⚠️ Vui lòng chọn một khóa học từ trang chính.")
        if st.button("Quay lại Danh sách Khóa học", key="fallback_main_btn"):
            navigate_to_main_page()
            st.rerun()
        st.stop()

    COURSE_ID = st.session_state.selected_course_id

    # --- Đọc dữ liệu (Chỉ đọc để lấy thông tin course_name) ---
    try:
        df = load_courses()
        df['class_start'] = pd.to_datetime(df['class_start']).dt.strftime('%m/%d/%Y')
        df['class_end'] = pd.to_datetime(df['class_end']).dt.strftime('%m/%d/%Y')
    except Exception as e:
        st.error(f"Lỗi khi đọc file CSV: {e}")
        st.stop()

    course_data = df[df['course_id'] == COURSE_ID]
    if course_data.empty:
        st.error(f"Không tìm thấy dữ liệu cho Course ID: {COURSE_ID}")
        if st.button("Quay lại Danh sách Khóa học", key="fallback_main_btn_2"):
            navigate_to_main_page()
            st.rerun()
        st.stop()
    course = course_data.iloc[0]


    # --- Header và Nút Quay Lại ---
    st.markdown("""
    <style>
        /* Sửa lỗi nút quay lại bị tràn và tròn (vì nó dùng key 'nav_back_main_tab')*/
        .back-button-container button[key*="nav_back_main_tab"] {
            border-radius: 8px !important;
            border: 1px solid #4299e1 !important;
            background: rgba(66, 153, 225, 0.1) !important;
            color: #4299e1 !important;
            padding: 8px 12px !important;
            font-size: 16px !important;
            min-height: 38px !important;
            white-space: nowrap; /* Đảm bảo chữ không bị ngắt dòng */
        }
        .back-button-container button[key*="nav_back_main_tab"]:hover {
             background: #4299e1 !important;
             color: white !important;
        }
                div[data-testid="stForm"] > div:has(> div[data-testid="stRadio"]) > label {
            display: none !important; 
        }

        /* 2. CSS để fix lỗi st.radio hiển thị nhãn phụ */
        .stRadio > label p {
            display: none;
        }
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="back-button-container">', unsafe_allow_html=True)
    st.button("⟨⟨", key="nav_back_main_tab", on_click=navigate_to_main_page)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Tiêu đề chính
    st.title(f"**Khóa học {course['course_name']}**")
    st.markdown(f"""
        <div style="font-size:16px; color:#a0aec0; display:flex; align-items:center; gap:6px;">
        <span class="material-symbols-outlined" style="font-size:20px;">
            account_balance
        </span>
        Được cung cấp bởi <b>{course['school_name']}</b>
        </div>
        """, unsafe_allow_html=True)
    st.markdown(f"Course ID: **{course['course_id']}**")
    st.markdown("---")

    # --- TẠO TAB ĐỘNG ---
    tab_titles = ["📊 Course Dashboard", "👥 User List"]
    
    # 1. Nếu có user được chọn, THÊM tab thứ 3
    is_user_detail_active = st.session_state.current_user_id is not None
    if is_user_detail_active:
        tab_titles.append(f"👤 User: {st.session_state.current_user_id}")

    # 2. Tính toán active tab index dựa trên current_user_id
    if is_user_detail_active:
        # Auto-switch sang tab User Detail (index 2)
        active_tab_index = 2
    elif st.session_state.current_view == 'user_list':
        active_tab_index = 1
    else:
        active_tab_index = 0
    
    # 3. Dùng radio button thay vì st.tabs() để hỗ trợ auto-switch
    st.markdown("""
    <style>
        /* Styling radio buttons để trông giống tabs (giữ nguyên) */
        .stRadio > div[role="radiogroup"] {
            display: flex;
            gap: 4px !important;
            flex-direction: row;
        }
        /* Đảm bảo các nút radio được xếp theo hàng ngang */
        .stRadio [role="radiogroup"] > label {
             margin: 0 !important;
             padding: 0 !important;
        }
        .stRadio [role="radiogroup"] > label > div {
             padding: 10px 15px !important; /* Điều chỉnh padding cho nút tab */
             border-radius: 8px;
        }
    </style>
    """, unsafe_allow_html=True)
    
    active_tab = st.radio(
        "Chọn tab",
        tab_titles,
        index=active_tab_index,
        horizontal=True,
        label_visibility="collapsed",
        key="course_detail_tabs" 
    )
    
    st.markdown("---")
    
    # 4. Hiển thị nội dung dựa trên active_tab
    active_index = tab_titles.index(active_tab)

    # RESET USER DETAIL KHI RỜI TAB DETAIL
    if active_index != 2:
        st.session_state.current_user_id = None
    
    if active_index == 0:
        st.session_state.current_view = 'dashboard'
        display_course_dashboard(course, COURSE_ID)

    elif active_index == 1:
        # Tab 2: User List
        if st.session_state.current_view != 'user_list':
            navigate_to_user_list()
        display_user_list(COURSE_ID)

    elif active_index == 2 and is_user_detail_active:
        # Tab 3: User Detail
        if st.session_state.current_view != 'user_detail':
            st.session_state.current_view = 'user_detail'
        display_user_dashboard(st.session_state.current_user_id)