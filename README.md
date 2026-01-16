# ADY201m - YouTube Trending Content Analysis

**Student ID:** Dương Thị Mỹ Tâm QE20009
                Trần Vân Khánh QE200083
**Project Name:** YouTube Trending & Viral Factor Analysis
**Course:** ADY201m - AI, Data Science with Python & SQL

---

## 📖 Giới thiệu (Introduction)
Dự án này nhằm mục đích xây dựng một quy trình dữ liệu (Data Pipeline) từ khâu thu thập (Crawling) đến phân tích (Analytics) để trả lời các câu hỏi về yếu tố tạo nên một video "Trending" trên YouTube.

**Mục tiêu chính:**
* Thu thập dữ liệu của 10.000+ video từ YouTube API.
* Lưu trữ dữ liệu thô (Raw Data) vào Data Lake (MinIO).
* Kiểm chứng giả thuyết về "Khung giờ vàng" và "Tương tác tiêu cực" (Dislike/Negative Comments).

## 🛠 Tech Stack
* **Language:** Python 3.9+
* **Data Lake:** MinIO (Object Storage)
* **Database:** PostgreSQL/MySQL (Metadata)
* **Containerization:** Docker & Docker Compose
* **Analysis:** Pandas, SQL, Jupyter Notebook

---

## 📂 Cấu trúc dự án (Project Structure)
```
Student_ID_Project_Name/
├── configs/               # Chứa file cấu hình (DB, API Keys)
├── data/                  # Dữ liệu mẫu (Sample data only)
├── docker/                # Dockerfile cho các service
├── notebooks/             # Jupyter Notebooks phân tích & EDA
├── reports/               # Các báo cáo định kỳ (PDF)
├── src/                   # Source code chính
│   ├── ingestion/         # Code thu thập dữ liệu (Crawler)
│   ├── processing/        # Code làm sạch & chuẩn hóa dữ liệu
│   └── utils/             # Các hàm tiện ích chung
├── .gitignore             # File loại bỏ file rác, env
├── AI_Log.md              # Nhật ký sử dụng AI
├── docker-compose.yml     # Khởi chạy toàn bộ hệ thống
├── README.md              # Hướng dẫn setup dự án
└── requirements.txt       # Các thư viện Python cần thiết

