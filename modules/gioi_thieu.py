import streamlit as st
import pandas as pd
from modules.theme_system import get_theme_colors

def show(theme='Light'):
    colors = get_theme_colors(theme)
    
    # Custom CSS for this page
    st.markdown(f"""
    <style>
        .intro-banner {{
            background: linear-gradient(135deg, #0061f2 0%, #00c6f9 100%);
            border-radius: 16px;
            padding: 40px;
            color: white;
            text-align: center;
            margin-bottom: 30px;
            box-shadow: 0 10px 30px rgba(0, 97, 242, 0.3);
        }}
        .intro-title {{
            font-size: 36px;
            font-weight: 700;
            margin-bottom: 10px;
            text-transform: uppercase;
            letter-spacing: 1px;
        }}
        .intro-main-title {{
            font-size: 52px;
            font-weight: 800;
            margin-bottom: 20px;
            line-height: 1.4;
        }}
        .intro-subtitle {{
            font-size: 28px;
            opacity: 0.9;
            font-weight: 500;
        }}
        
        /* Team Members */
        .member-card {{
            background: {colors['bg_card']};
            border-radius: 12px;
            padding: 20px;
            display: flex;
            align-items: center;
            gap: 15px;
            border: 1px solid {colors['border_color']};
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
            height: 100%;
            transition: transform 0.3s ease;
        }}
        .member-card:hover {{
            transform: translateY(-5px);
        }}

        .member-info h4 {{
            margin: 0;
            font-size: 24px;
            color: {colors['text_primary']};
            font-weight: 700;
        }}
        .member-info p {{
            margin: 0;
            font-size: 18px;
            color: {colors['text_secondary']};
        }}
        .member-role {{
            font-size: 18px !important;
            color: {colors['accent_blue']} !important;
            margin-top: 2px !important;
        }}
        
        /* Footer */
        .intro-footer {{
            background: white;
            color: #000000 !important;
            padding: 15px;
            text-align: center;
            border-radius: 12px;
            margin-top: 20px;
            font-weight: 600;
            font-size: 20px;
        }}

        /* General Markdown Content Increase */
        div[data-testid="stMarkdownContainer"] p {{
            font-size: 20px !important;
            line-height: 1.6 !important;
        }}
        div[data-testid="stMarkdownContainer"] h3 {{
            font-size: 30px !important;
            font-weight: 700 !important;
        }}
        div[data-testid="stMarkdownContainer"] li {{
            font-size: 20px !important;
        }}
    </style>
    """, unsafe_allow_html=True)

    # BANNER
    st.markdown("""
    <div class="intro-banner">
        <div class="intro-title">Đề tài</div>
        <div class="intro-main-title">
            Dự đoán khả năng bỏ học của học viên trong các khóa học MOOC<br>
            bằng bài toán phân loại 2 nhãn<br>
        </div>
        <div class="intro-subtitle">
            Predicting Student Dropout in MOOC Courses<br>
            Using a Two-Label Classification Model
        </div>
    </div>
    """, unsafe_allow_html=True)

    # TEAM MEMBERS
    st.subheader("Nhóm 3 - DS317.Q11")
    
    # Row 1
    c1, c2, c3 = st.columns(3)
    
    members_1 = [
        {"name": "Tăng Gia Hân", "id": "22520394", "role": "Trưởng nhóm"},
        {"name": "Trà Minh Hy", "id": "22520594", "role": "Thư kí"},
        {"name": "Tăng Mỹ Hân", "id": "22520395", "role": "Thành viên"},
    ]
    
    for i, col in enumerate([c1, c2, c3]):
        m = members_1[i]
        with col:
            st.markdown(f"""
            <div class="member-card">
                <div class="member-info">
                    <h4>{m['name']}</h4>
                    <p>{m['id']}</p>
                    <p class="member-role">{m['role']}</p>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
    st.markdown("<br>", unsafe_allow_html=True)
            
    # Row 2
    c1, c2, c3 = st.columns(3) # Use 3 cols but fill first 2 to center somewhat? Or just 2 cols? Image shows 3 top, 2 bottom left aligned.
    
    members_2 = [
        {"name": "Huỳnh Bá Khang", "id": "22520613", "role": "Thành viên"},
        {"name": "Nguyễn Lâm Khôi Nguyên", "id": "22520975", "role": "Thành viên"},
    ]
    
    with c1:
        m = members_2[0]
        st.markdown(f"""
        <div class="member-card">
            <div class="member-info">
                <h4>{m['name']}</h4>
                <p>{m['id']}</p>
                <p class="member-role">{m['role']}</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
    with c2:
        m = members_2[1]
        st.markdown(f"""
        <div class="member-card">
            <div class="member-info">
                <h4>{m['name']}</h4>
                <p>{m['id']}</p>
                <p class="member-role">{m['role']}</p>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # Footer
    st.markdown("""
    <div class="intro-footer">
        TRƯỜNG ĐẠI HỌC CÔNG NGHỆ THÔNG TIN, ĐẠI HỌC QUỐC GIA THÀNH PHỐ HỒ CHÍ MINH (UIT)
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    # PROJECT INFO TABS
    st.subheader("Thông tin về dự án")
    
    tab1, tab2, tab3, tab4 = st.tabs(["① Tổng quan", "📱 Ứng dụng", "⚡ Tính mới", "📄 Bộ dữ liệu"])
    
    with tab1:
        st.markdown("""
        ### Tên dự án
        **Dự đoán khả năng bỏ học của học viên trong các khóa học MOOC.**

        ### Mục tiêu
        Xây dựng mô hình học máy nhằm dự đoán sớm nguy cơ bỏ học của học viên trong các khóa học MOOC dựa trên dữ liệu hành vi học tập và thông tin ngữ cảnh.

        ### Mô tả ngắn
        Dự án khai thác bộ dữ liệu MOOCCubeX, kết hợp các đặc trưng hành vi theo thời gian, tương tác học tập và thông tin khóa học để phân loại học viên thành hai nhóm: tiếp tục học và bỏ học. Kết quả giúp nền tảng MOOC phát hiện sớm học viên có nguy cơ cao và hỗ trợ can thiệp kịp thời.

        ### Link Đồ Án Nhóm
        [**ThucHanhDS317.Q11**](https://github.com/MinHeHeHeHe/ThucHanhDS317.Q11)
        """)
        
    with tab2:
        st.markdown("""
        ### Hệ thống cảnh báo sớm (Early Warning System)
        Phát hiện sớm học viên có nguy cơ bỏ học và gửi cảnh báo cho giảng viên hoặc hệ thống quản lý học tập.

        ### Cá nhân hóa học tập
        Hỗ trợ đề xuất tài nguyên, lộ trình hoặc nội dung phù hợp với mức độ tham gia của từng học viên.

        ### Hỗ trợ quản lý đào tạo
        Giúp nền tảng MOOC đánh giá hiệu quả khóa học, cải thiện tỷ lệ hoàn thành và nâng cao trải nghiệm người học.
        """)
        
    with tab3:
        st.markdown("""
        - **Kết hợp đa nguồn dữ liệu**: Hành vi học tập, tương tác, thông tin khóa học và đặc điểm học viên.
        - **Phân tích hành vi học tập theo chuỗi thời gian**, thay vì chỉ dùng các thống kê tĩnh.
        - **Áp dụng các mô hình học máy và học sâu** để dự đoán nguy cơ bỏ học ở giai đoạn sớm.
        - **Hướng đến cảnh báo sớm mang tính cá nhân hóa**, hỗ trợ can thiệp đúng thời điểm cho từng học viên.
        """)
        
    with tab4:
        st.markdown("""
        ### Nguồn dữ liệu
        Sử dụng bộ dữ liệu [**MOOCCubeX**](https://github.com/THU-KEG/MOOCCubeX), thu thập từ nền tảng MOOC XuetangX.

        ### Thành phần chính
        - Thông tin học viên
        - Thông tin khóa học
        - Hành vi học tập (xem video, làm bài tập, đăng nhập, thảo luận)
        - Dữ liệu tương tác và kết quả học tập theo thời gian

        ### Đặc điểm dữ liệu
        - Quy mô lớn, đa dạng và có tính chuỗi thời gian.
        - Phù hợp cho các bài toán phân tích hành vi và dự đoán bỏ học.
        """)
