import json
import psycopg2

# 1. Kết nối Database
conn = psycopg2.connect(
    host="localhost",
    database="ady_database",
    user="mytam_admin",
    password="password123",
    port="5432"
)
cur = conn.cursor()
print("Kết nối thành công!")

# 2. Xóa dữ liệu cũ trong bảng TikTok để nạp file mới
cur.execute("TRUNCATE TABLE raw_tiktok RESTART IDENTITY;")
cur.execute("TRUNCATE TABLE raw_youtube RESTART IDENTITY;")

# 3. Nạp dữ liệu YouTube
# Bạn có thể thay đường dẫn file bên dưới nếu cần
with open('data/raw/youtube_trending_20260119_230758.json', 'r', encoding='utf-8') as f:
    yt_data = json.load(f)
    for item in yt_data:
        cur.execute("""
            INSERT INTO raw_youtube (video_id, title, views, likes, comments, publish_time, country)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (item['video_id'], item['title'], item['views'], item['likes'], 
              item['comments'], item['publish_time'], item['country']))
print(f"Đã nạp xong YouTube!")

# 4. Nạp dữ liệu TikTok (Dùng file merged mới nhất)
with open('data/raw/tiktok_dataset_merged (1).json', 'r', encoding='utf-8') as f:
    tt_data = json.load(f)
    for item in tt_data:
        cur.execute("""
            INSERT INTO raw_tiktok (hashtag, caption, publish_time, likes, comments, is_trending, has_clickbait)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (item['hashtag'], item['caption'], item['publish_time'], 
              str(item['likes']), str(item['comments']), 
              item['is_trending'], item['has_clickbait']))
print(f"Đã nạp xong TikTok mới!")

# 5. Lưu và Đóng
conn.commit()
cur.close()
conn.close()
print("Hoàn thành tất cả!")