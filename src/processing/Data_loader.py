import json
import psycopg2

# 1. Kết nối Database 
conn = psycopg2.connect(
    host="localhost",
    database="ady_database",
    user="mytam_vankhanh",
    password="123",
    port="5432"
)
cur = conn.cursor()
print("Kết nối thành công!")

# 2. Xóa dữ liệu cũ (Dọn dẹp bảng trước khi nạp)
cur.execute("TRUNCATE TABLE raw_tiktok RESTART IDENTITY CASCADE;")
cur.execute("TRUNCATE TABLE raw_youtube RESTART IDENTITY CASCADE;")

# 3. Nạp dữ liệu YouTube
with open('data/raw/youtube_trending_20260119_230758.json', 'r', encoding='utf-8') as f:
    yt_data = json.load(f)
    for item in yt_data:
        cur.execute("""
            INSERT INTO raw_youtube (video_id, title, views, likes, comments, publish_time, country)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (item['video_id'], item['title'], item['views'], item['likes'], 
              item['comments'], item['publish_time'], item['country']))

# 4. Nạp dữ liệu TikTok

with open('data/raw/tiktok_dataset_merged (1).json', 'r', encoding='utf-8') as f:
    tt_data = json.load(f)
    for item in tt_data:
        cur.execute("""
            INSERT INTO raw_tiktok (hashtag, caption, publish_time, likes, comments, is_trending, has_clickbait)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (
            item.get('hashtag'), 
            item.get('caption'), 
            item.get('publish_time'), 
            str(item.get('likes')),    # Ép thành chuỗi để nhận được chữ "K"
            str(item.get('comments')), # Ép thành chuỗi
            item.get('is_trending'), 
            item.get('has_clickbait')
        ))
# 5. Lưu và Đóng
conn.commit()
cur.close()
conn.close()
print("Hoàn thành nạp dữ liệu!")