import os
import json
import time
import pandas as pd
from pathlib import Path
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from tqdm import tqdm
from dotenv import load_dotenv
from datetime import datetime

# ==========================================
# PHẦN 1: NẠP CẤU HÌNH (QUAN TRỌNG NHẤT)
# ==========================================

# 1. Tự động tìm file .env nằm CÙNG THƯ MỤC với file code này
base_dir = Path(__file__).resolve().parent
env_file = base_dir / '.env'

print(f"📂 Đang đọc cấu hình từ: {env_file}")
load_dotenv(dotenv_path=env_file, override=True)

# 2. Lấy API Key
API_KEY = os.getenv("YOUTUBE_API_KEY")

if not API_KEY:
    print("❌ LỖI NGHIÊM TRỌNG: Không tìm thấy YOUTUBE_API_KEY!")
    print("👉 Hãy chắc chắn file .env nằm cạnh file youtube.py và có nội dung đúng.")
    raise SystemExit(1)
else:
    print(f"✅ Đã nạp API Key: {API_KEY[:5]}...********")

# 3. Lấy Quốc gia & Danh mục (Xử lý lỗi NameError cũ của bạn)
env_countries = os.getenv("COUNTRIES", "VN")
COUNTRIES = [c.strip().upper() for c in env_countries.split(",") if c.strip()]

env_cats = os.getenv("CATEGORY_IDS", "")
CATEGORY_IDS = [c.strip() for c in env_cats.split(",") if c.strip()]

# Map tên để hiển thị cho đẹp
CATEGORY_MAP = {
    "1":  "Film & Animation",
    "2":  "Autos & Vehicles",
    "10": "Music",
    "15": "Pets & Animals",
    "17": "Sports",
    "19": "Travel & Events",
    "20": "Gaming",
    "22": "People & Blogs",
    "23": "Comedy",
    "24": "Entertainment",
    "25": "News & Politics",
    "26": "Howto & Style",
    "27": "Education",
    "28": "Science & Tech",
    "29": "Nonprofits & Activism",
}

print(f"🌍 Quốc gia cần quét ({len(COUNTRIES)}): {COUNTRIES}")
print(f"📂 Danh mục cần quét: {CATEGORY_IDS if CATEGORY_IDS else 'Tất cả (Mặc định)'}")

# ==========================================
# PHẦN 2: LOGIC THU THẬP DỮ LIỆU
# ==========================================

youtube = build("youtube", "v3", developerKey=API_KEY)

# Cấu hình nhỏ
MAX_PAGES = 1  # Số trang muốn quét mỗi danh mục (1 trang = 50 video)
PER_COUNTRY_CAP = 200 # Giới hạn số video tối đa mỗi nước để test cho nhanh

def fetch_videos():
    all_items = []
    
    # Tính tổng số lượt quét để hiện thanh loading
    cats_to_scan = CATEGORY_IDS if CATEGORY_IDS else [None]
    total_ops = len(COUNTRIES) * len(cats_to_scan)

    with tqdm(total=total_ops, desc="Đang tải dữ liệu") as pbar:
        for country in COUNTRIES:
            country_items = []
            
            for cat_id in cats_to_scan:
                next_page_token = None
                
                # Quét nhiều trang
                for _ in range(MAX_PAGES):
                    try:
                        # Tạo request
                        params = {
                            "part": "id,snippet,statistics,contentDetails",
                            "chart": "mostPopular",
                            "regionCode": country,
                            "maxResults": 50,
                            "pageToken": next_page_token
                        }
                        if cat_id:
                            params["videoCategoryId"] = cat_id

                        response = youtube.videos().list(**params).execute()

                        # Xử lý kết quả
                        for item in response.get("items", []):
                            stats = item.get("statistics", {})
                            snippet = item.get("snippet", {})
                            
                            # Lấy ID danh mục an toàn
                            c_id = snippet.get("categoryId", "0")

                            video_data = {
                                "video_id": item["id"],
                                "title": snippet.get("title"),
                                # Chuyển số liệu sang dạng số (int)
                                "category_id": int(c_id) if c_id.isdigit() else 0,
                                "category_name": CATEGORY_MAP.get(c_id, "Unknown"),
                                "views": int(stats.get("viewCount", 0)),
                                "likes": int(stats.get("likeCount", 0)),
                                "comments": int(stats.get("commentCount", 0)),
                                "publish_time": snippet.get("publishedAt"),
                                "country": country
                            }
                            country_items.append(video_data)

                        next_page_token = response.get("nextPageToken")
                        if not next_page_token:
                            break
                        
                    except HttpError as e:
                        # Bỏ qua lỗi nếu danh mục không hỗ trợ ở quốc gia đó
                        if e.resp.status not in [400, 404]:
                            print(f"\n⚠️ Lỗi Google API ({country}): {e}")
                        break
                    except Exception as ex:
                        print(f"\n⚠️ Lỗi lạ: {ex}")
                        break
                
                pbar.update(1)
            
            # Gộp dữ liệu của quốc gia này vào danh sách tổng
            all_items.extend(country_items)

    return all_items

# ==========================================
# PHẦN 3: LƯU FILE
# ==========================================

if __name__ == "__main__":
    data = fetch_videos()

    if not data:
        print("\n❌ KHÔNG CÓ DỮ LIỆU ĐƯỢC TẢI VỀ.")
        print("👉 Gợi ý: Kiểm tra xem trong file .env phần CATEGORY_IDS có bị sai số không?")
    else:
        # Tạo DataFrame
        df = pd.DataFrame(data)
        
        # Lọc trùng lặp
        df = df.drop_duplicates(subset=['video_id', 'country'])
        
        # Tạo tên file theo thời gian
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        os.makedirs("data", exist_ok=True)
        
        # Xuất JSON
        json_path = f"data/youtube_trending_{ts}.json"
        df.to_json(json_path, orient="records", indent=2, force_ascii=False)
        
        # Xuất CSV
        csv_path = f"data/youtube_trending_{ts}.csv"
        df.to_csv(csv_path, index=False, encoding="utf-8-sig")

        print(f"\n✅ THÀNH CÔNG! Đã thu thập {len(df)} video.")
        print(f"📂 File đã lưu tại: {json_path}")