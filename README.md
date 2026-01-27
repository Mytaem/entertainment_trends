ADY201m - TikTok & YouTube Content Trend Analysis

Student Info: * Dương Thị Mỹ Tâm - QE200009 

                          Trần Vân Khánh - QE200083 


Project Name: Analysis of Viral and Trending Factors on Digital Content Platforms Course: ADY201m – AI, Data Science with Python & SQL 

📖 Giới thiệu (Introduction)
Dự án tập trung nghiên cứu sự khác biệt giữa hai cơ chế hình thành xu hướng: nội dung ngắn, lan truyền nhanh trên TikTok và nội dung dài, bền vững trên YouTube. Bằng cách xây dựng hệ thống thu thập dữ liệu tự động, nhóm hướng tới việc xác định các yếu tố then chốt giúp một nội dung trở nên viral hoặc lọt vào danh sách Trending.

Mục tiêu chính:


Thu thập dữ liệu: Xây dựng dataset từ dữ liệu công khai trên TikTok (Hashtag-based) và YouTube (Trending-based).


Chuẩn hóa: Đồng nhất cấu trúc metadata (thời gian, tương tác, tiêu đề) để so sánh chéo giữa hai nền tảng.


Kiểm chứng giả thuyết: Phân tích tác động của "Khung giờ vàng", "Tiêu đề giật gân (Clickbait)" và "Mức độ duy trì tương tác".

🛠 Tech Stack (Advanced Tech Stack)
Dựa trên kiến trúc hệ thống đề xuất:


Language: Python (Playwright cho TikTok, Data API cho YouTube).


Data Ingestion: Python Crawler & YouTube Data API.


Storage: JSON/CSV (Raw Data) & SQL Database (PostgreSQL).


Containerization: Docker & Docker Compose.


Analysis & Version Control: Pandas, SQL, GitHub.

📂 Cấu trúc dự án (Project Structure)
Plaintext
QE200009_QE200083_Content_Trend_Analysis/
├── configs/               # Cấu hình Database & API Keys (YouTube API)
├── data/                  # Dữ liệu thô (JSON/CSV) từ TikTok & YouTube
├── docker/                # Dockerfile cho PostgreSQL và các môi trường chạy Python
├── notebooks/             # Jupyter Notebooks: EDA và Kiểm định giả thuyết (Hypothesis Testing)
├── reports/               # Báo cáo ADY201m (Research Proposal, Data Report)
├── src/                   # Source code chính
│   ├── ingestion/         # TikTok Crawler (Playwright) & YouTube API Script
│   ├── processing/        # Code làm sạch, chuẩn hóa múi giờ và định dạng metadata
│   └── utils/             # Các hàm bổ trợ xử lý chuỗi và tính toán engagement rate
├── .gitignore             # Loại bỏ các file .env và dữ liệu nặng
├── AI_Log.md              # Nhật ký sử dụng AI hỗ trợ dự án
├── docker-compose.yml     # Khởi chạy hệ thống (PostgreSQL, Dockerized App)
├── README.md              # Hướng dẫn cài đặt và vận hành pipeline
└── requirements.txt       # Thư viện: playwright, google-api-python-client, pandas, sqlalchemy
🎯 Câu hỏi nghiên cứu & Giả thuyết
Dự án tập trung giải quyết các bài toán:


Khung giờ đăng tải: Liệu đăng video vào buổi tối có thực sự tăng khả năng lên xu hướng? 


Yếu tố Clickbait: Tiêu đề và Caption giật gân ảnh hưởng thế nào đến tương tác ban đầu? 


Tính bền vững: Mối liên hệ giữa tương tác sớm và khả năng duy trì vị trí trong danh sách Trending.
