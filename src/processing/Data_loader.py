import json
import psycopg2
from minio import Minio
import io
import re

# 1. Kết nối MinIO
minio_client = Minio("localhost:9000", "minioadmin", "minioadmin", secure=False)

# 2. Kết nối PostgreSQL
db_config = {"host": "localhost", "database": "ady_database", "user": "mytam_vankhanh", "password": "123", "port": "5432"}

def clean_numeric_value(value):
    if value is None or value == "": return 0
    val_str = str(value).upper().replace(' ', '').replace(',', '')
    try:
        if 'K' in val_str: return int(float(val_str.replace('K', '')) * 1000)
        if 'M' in val_str: return int(float(val_str.replace('M', '')) * 1000000)
        clean_val = re.sub(r'[^\d.]', '', val_str)
        return int(float(clean_val)) if clean_val else 0
    except: return 0

try:
    conn = psycopg2.connect(**db_config)
    cur = conn.cursor()

    # --- PHẦN 1: NẠP TIKTOK ---
    cur.execute("""
        CREATE TABLE IF NOT EXISTS tiktok_final (
            hashtag TEXT, caption TEXT, publish_time TEXT, scrape_time TIMESTAMP,
            likes BIGINT, comments BIGINT, views BIGINT, shares BIGINT,
            is_trending INTEGER, has_clickbait INTEGER
        );
    """)
    cur.execute("TRUNCATE TABLE tiktok_final;")
    
    resp_tt = minio_client.get_object("tiktok-raw", "tiktok_raw.json")
    tt_data = json.loads(resp_tt.read().decode('utf-8'))
    for item in tt_data:
        cur.execute("INSERT INTO tiktok_final VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)", 
            (item.get('hashtag'), item.get('caption'), item.get('publish_time'), item.get('scrape_time'),
             clean_numeric_value(item.get('likes')), clean_numeric_value(item.get('comments')),
             clean_numeric_value(item.get('views')), clean_numeric_value(item.get('shares')),
             item.get('is_trending', 0), item.get('has_clickbait', 0)))
    print(f"🚀 Đã nạp {len(tt_data)} video TikTok từ MinIO.")

    # --- PHẦN 2: NẠP YOUTUBE ---
    cur.execute("""
        CREATE TABLE IF NOT EXISTS youtube_final (
            video_id TEXT, title TEXT, category_name TEXT, 
            views BIGINT, likes BIGINT, comments BIGINT, 
            publish_time TEXT, country TEXT
        );
    """)
    cur.execute("TRUNCATE TABLE youtube_final;")
    
    # Kiểm tra đúng tên file youtube trong MinIO của bạn
    resp_yt = minio_client.get_object("youtube-raw", "youtube_raw.json")
    yt_data = json.loads(resp_yt.read().decode('utf-8'))
    for item in yt_data:
        cur.execute("INSERT INTO youtube_final VALUES (%s,%s,%s,%s,%s,%s,%s,%s)", 
            (item.get('video_id'), item.get('title'), item.get('category_name'),
             item.get('views', 0), item.get('likes', 0), item.get('comments', 0),
             item.get('publish_time'), item.get('country')))
    print(f"🎬 Đã nạp {len(yt_data)} video YouTube từ MinIO.")

    conn.commit()
    cur.close()
    conn.close()
    print("✨ TẤT CẢ DỮ LIỆU ĐÃ SẴN SÀNG TRÊN POSTGRESQL!")

except Exception as e:
    print(f"❌ Lỗi: {e}")