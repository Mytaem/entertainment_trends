from minio import Minio
import os

# 1. Kết nối đến MinIO (Cổng API là 9000)
client = Minio(
    "localhost:9000",
    access_key="minioadmin",
    secret_key="minioadmin",
    secure=False
)

# 2. Danh sách các file và bucket tương ứng
files_to_upload = [
    {"path": "data/raw/tiktok_dataset_merged (1).json", "bucket": "tiktok-raw", "name": "tiktok_raw.json"},
    {"path": "data/raw/youtube_trending_20260119_230758.json", "bucket": "youtube-raw", "name": "youtube_raw.json"}
]

# 3. Chạy vòng lặp để upload
for item in files_to_upload:
    try:
        # Kiểm tra nếu file tồn tại ở máy cục bộ
        if os.path.exists(item["path"]):
            client.fput_object(item["bucket"], item["name"], item["path"])
            print(f"✅ Đã đẩy file {item['name']} lên MinIO thành công!")
        else:
            print(f"❌ Không tìm thấy file tại: {item['path']}")
    except Exception as e:
        print(f"❌ Lỗi khi upload {item['name']}: {e}")