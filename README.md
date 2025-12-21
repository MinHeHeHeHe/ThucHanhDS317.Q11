# BI MOOCCubeX Dashboard

Ứng dụng BI Dashboard dành cho việc phân tích và dự đoán dữ liệu học tập từ MOOCCubeX, được xây dựng trên nền tảng Streamlit. Với đề tài Dự đoán khả năng bỏ học của học viên trong các khóa học MOOC bằng bài toán phân loại 2 nhãn (0: không bỏ học, 1: bỏ học).

## 🛠️ Cấu trúc cài đặt (Installation)

Dự án yêu cầu Python (phiên bản 3.9 trở lên) và các thư viện cần thiết. Để cài đặt môi trường, bạn thực hiện các bước sau:

1. **Clone repository hoặc tải mã nguồn về máy.**
2. **Cài đặt các thư viện phụ thuộc:**

   Sử dụng lệnh `pip` để cài đặt các thư viện được liệt kê trong file `requirements.txt` (nếu có) hoặc cài đặt trực tiếp các thư viện chính:

   ```bash
   pip install streamlit pandas plotly scikit-learn
   ```

## 🚀 Cách chạy ứng dụng (How to Run)

Để khởi động Dashboard, hãy mở terminal tại thư mục gốc của dự án và chạy lệnh sau:

```bash
streamlit run app.py
```

Sau khi chạy lệnh, ứng dụng sẽ khởi tạo server local. Bạn có thể truy cập Dashboard qua địa chỉ mặc định trong trình duyệt:
`http://localhost:8501`

## 📂 Cấu trúc cây thư mục dự án (Project Structure)

Dưới đây là sơ đồ tổ chức các file và thư mục trong dự án:

```text
ThucHanhDS317.Q11/
├── .streamlit/                # Cấu hình giao diện Streamlit
│   └── config.toml            # Thiết lập theme (Light/Dark) và giao diện
├── data/                      # Thư mục chứa dữ liệu CSV của dự án
│   ├── course_info_final_P5.csv   # Thông tin chi tiết các khóa học
│   ├── df_not_fill.csv            # Dữ liệu phục vụ phân tích chất lượng
│   ├── test_P1_pred.csv           # Dự đoán kết quả Giai đoạn 1
│   ├── test_P2_pred.csv           # Dự đoán kết quả Giai đoạn 2
│   ├── test_P3_pred.csv           # Dự đoán kết quả Giai đoạn 3
│   ├── test_P4_pred.csv           # Dự đoán kết quả Giai đoạn 4
│   ├── test_P5_pred.csv           # Dự đoán kết quả Giai đoạn 5
│   └── train_validate.csv         # Dữ liệu huấn luyện và kiểm định
├── modules/                   # Các Module tính năng của ứng dụng
│   ├── chat_luong_du_lieu.py      # Phân tích và đánh giá chất lượng dữ liệu
│   ├── course_view.py             # Giao diện chi tiết từng khóa học
│   ├── data_loader.py             # logic tải và xử lý dữ liệu tập trung
│   ├── gioi_thieu.py              # Trang giới thiệu dự án
│   ├── ket_qua_phan_tich_du_doan.py # Báo cáo kết quả model dự đoán
│   ├── khoa_hoc.py                # Quản lý danh sách và lọc khóa học
│   ├── styles.py                  # Định nghĩa các style CSS tùy chỉnh
│   ├── theme_system.py            # Hệ thống chuyển đổi giao diện (Light/Dark)
│   ├── tong_quan.py               # Trang tổng quan chung
│   ├── tong_quan_hien_tai.py      # Trang tổng quan và dự đoán theo giai đoạn
│   └── user_view.py               # Phân tích hành vi người dùng chi tiết
├── app.py                     # File chạy chính của ứng dụng Streamlit
├── course_dashboard.py        # Module hỗ trợ hiển thị dashboard khóa học
├── README.md                  # Tài liệu hướng dẫn sử dụng dự án
└── .gitignore                 # Các file không đưa lên git
```

## ✨ Các tính năng chính

*   **Tổng quan (Overview):** Hiển thị các chỉ số đo lường chính và xu hướng học tập.
*   **Tổng quan hiện tại:** Phân tích chi tiết và dự đoán tỷ lệ bỏ học theo từng giai đoạn (1-5).
*   **Chất lượng dữ liệu:** Kiểm tra các giá trị thiếu, ngoại lệ và tính nhất quán của dữ liệu.
*   **Chi tiết khóa học:** Dashboard riêng cho từng khóa học với biểu đồ phân bổ điểm và tỷ lệ bỏ học.
*   **Kết quả dự đoán:** Bảng thống kê chi tiết hiệu suất của các mô hình học máy.
