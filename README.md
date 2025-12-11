# ThucHanhDS317.Q11

Dự án Dashboard phân tích dữ liệu MOOCCubeX sử dụng Streamlit.

## Yêu cầu cài đặt

Dự án yêu cầu cài đặt Python và các thư viện sau:

- streamlit
- pandas
- plotly

Bạn có thể cài đặt các thư viện này bằng lệnh pip:

```bash
pip install streamlit pandas plotly
```

## Cách chạy ứng dụng

1. Đảm bảo bạn đang ở thư mục gốc của dự án (nơi chứa file `app.py`).
2. Chạy lệnh sau trong terminal:

```bash
streamlit run app.py
```

3. Ứng dụng sẽ tự động mở trong trình duyệt mặc định của bạn tại địa chỉ `http://localhost:8501`.

## Cấu trúc dự án

- `app.py`: File chính để chạy ứng dụng.
- `modules/`: Chứa các module thành phần và giao diện (tong_quan, chat_luong_du_lieu, khoa_hoc, styles, theme_system).
- `train_validate.csv`: Dữ liệu đầu vào cho dashboard.
