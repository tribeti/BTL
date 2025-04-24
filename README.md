# Trình kiểm tra vi phạm giao thông

Một script Python tự động kiểm tra vi phạm giao thông trên website CSGT (csgt.vn).

---

## 📝 Mô tả

Ứng dụng này sử dụng **tự động hóa trình duyệt web** (Selenium) để kiểm tra các lỗi vi phạm giao thông bằng cách nhập **biển số xe** và **loại phương tiện**. Script được tích hợp chức năng **giải CAPTCHA tự động bằng OCR** (EasyOCR) và được lập lịch **chạy tự động 2 lần mỗi ngày**.

---

## ⚙️ Tính năng

- Kiểm tra vi phạm giao thông tự động
- Tự động nhận diện và giải mã CAPTCHA (dựa trên EasyOCR)
- Tự động chạy vào lúc **6:00 sáng** và **12:00 trưa** hàng ngày

---

## 🧰 Yêu cầu hệ thống

- Python 3.x
- Trình duyệt Chrome (mới nhất)
- Chrome WebDriver tương ứng với phiên bản trình duyệt
- Kết nối Internet ổn định

---

## 🧱 Cài đặt

### 1. Tải mã nguồn

Clone dự án từ GitHub:

```bash
git clone https://github.com/your-username/vehicle-violation-checker.git
cd vehicle-violation-checker
```

### 2. Cài đặt thư viện cần thiết

```bash
pip install -r requirements.txt
```

**Hoặc cài từng gói:**

```bash
pip install selenium easyocr pillow schedule torch torchvision
```

> ✅ **Lưu ý:** `easyocr` yêu cầu thêm `torch` và `torchvision` để hoạt động chính xác.

### 3. Tải và cài đặt Chrome WebDriver

- Truy cập: https://sites.google.com/chromium.org/driver/
- Tải phiên bản phù hợp với Chrome đang sử dụng
- Giải nén và đặt trong cùng thư mục hoặc thêm vào biến môi trường `PATH`

---

## 🚀 Sử dụng

Chạy file `main.py`:

```bash
python main.py
```

Quy trình:

1. Nhập **biển số xe** cần kiểm tra
2. Chọn **loại phương tiện** (1: Ô tô, 2: Xe máy, 3: Xe khác)
3. Script sẽ tự động giải CAPTCHA
4. Hiển thị thông tin vi phạm (nếu có)

---

## ⏰ Lập lịch chạy tự động

Script được thiết lập để **chạy định kỳ** vào:

- 6:00 sáng
- 12:00 trưa

Để script hoạt động liên tục, bạn chỉ cần **chạy và để script hoạt động ở chế độ nền** (mở terminal liên tục hoặc sử dụng task scheduler nếu cần).

---

## 📌 Lưu ý

- Đảm bảo máy tính có **kết nối Internet ổn định**
- Đảm bảo website csgt.vn hoạt động bình thường tại thời điểm kiểm tra

---

## 📂 Thư mục

```
BTL/
│
├── main.py                 # Script chính
├── requirements.txt        # Danh sách thư viện
└── README.md               # Hướng dẫn sử dụng
```