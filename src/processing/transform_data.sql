#TẠO CẤU TRÚC BẢNG THÔ (DÙNG ĐỂ NẠP DATA)
-- 1. Xóa bảng cũ nếu đã tồn tại để tránh lỗi xung đột cấu trúc
DROP TABLE IF EXISTS raw_tiktok;
DROP TABLE IF EXISTS raw_youtube;

-- 2. Tạo bảng thô cho TikTok: Tất cả để dạng TEXT để nhận dữ liệu có chữ K, M từ JSON
CREATE TABLE raw_tiktok (
    hashtag TEXT,
    caption TEXT,
    publish_time TEXT,
    scrape_time TEXT,
    likes TEXT,
    comments TEXT,
    views TEXT,
    shares TEXT,
    is_trending INTEGER,
    has_clickbait INTEGER
);

-- 3. Tạo bảng thô cho YouTube: Dữ liệu YouTube thường chuẩn hơn nên để BIGINT cho số
CREATE TABLE raw_youtube (
    video_id TEXT,
    title TEXT,
    category_name TEXT,
    views BIGINT,
    likes BIGINT,
    comments BIGINT,
    publish_time TEXT,
    country TEXT
);

#CHẾ BIẾN DỮ LIỆU SẠCH (TẠO BẢNG FINAL)
-- 1. Xóa bảng Final cũ
DROP TABLE IF EXISTS tiktok_final;

-- 2. Tạo bảng tiktok_final với dữ liệu đã được tính toán chuẩn hóa
CREATE TABLE tiktok_final AS
SELECT 
    hashtag,
    caption,
    publish_time::timestamp AS publish_time, 
    scrape_time::timestamp AS scrape_time,
    is_trending,
    has_clickbait,
    -- Chuẩn hóa cột Likes (Xử lý K thành 1000, M thành 1000000)
    CASE 
        WHEN likes LIKE '%M' THEN CAST(REPLACE(likes, 'M', '') AS FLOAT) * 1000000
        WHEN likes LIKE '%K' THEN CAST(REPLACE(likes, 'K', '') AS FLOAT) * 1000
        ELSE CAST(NULLIF(REPLACE(likes, ',', ''), '') AS FLOAT)
    END AS likes,
    -- Chuẩn hóa cột Comments
    CASE 
        WHEN comments LIKE '%M' THEN CAST(REPLACE(comments, 'M', '') AS FLOAT) * 1000000
        WHEN comments LIKE '%K' THEN CAST(REPLACE(comments, 'K', '') AS FLOAT) * 1000
        ELSE CAST(NULLIF(REPLACE(comments, ',', ''), '') AS FLOAT)
    END AS comments,
    -- Chuẩn hóa cột Views
    CASE 
        WHEN views LIKE '%M' THEN CAST(REPLACE(views, 'M', '') AS FLOAT) * 1000000
        WHEN views LIKE '%K' THEN CAST(REPLACE(views, 'K', '') AS FLOAT) * 1000
        ELSE CAST(NULLIF(REPLACE(views, ',', ''), '') AS FLOAT)
    END AS views,
    -- Chuẩn hóa cột Shares
    CASE 
        WHEN shares LIKE '%M' THEN CAST(REPLACE(shares, 'M', '') AS FLOAT) * 1000000
        WHEN shares LIKE '%K' THEN CAST(REPLACE(shares, 'K', '') AS FLOAT) * 1000
        ELSE CAST(NULLIF(REPLACE(shares, ',', ''), '') AS FLOAT)
    END AS shares
FROM raw_tiktok;

#KIỂM TRA SỐ LƯỢNG DỮ LIỆU (ĐỂ GHI VÀO BÁO CÁO)
-- Đếm tổng số video TikTok đã nạp sạch
SELECT 'TikTok' AS platform, COUNT(*) AS total_records FROM tiktok_final
UNION ALL
-- Đếm tổng số video YouTube đã nạp
SELECT 'YouTube' AS platform, COUNT(*) AS total_records FROM raw_youtube;

#Bảng tổng hợp các chỉ số trung bình của toàn sàn
SELECT 
    COUNT(*) AS tong_so_video,
    ROUND(AVG(views)::numeric, 0) AS views_tb,
    ROUND(AVG(likes)::numeric, 0) AS likes_tb,
    ROUND(AVG(comments)::numeric, 0) AS comments_tb,
    ROUND(AVG(shares)::numeric, 0) AS shares_tb,
    ROUND(AVG((likes + comments + shares) / NULLIF(views, 0) * 100)::numeric, 2) AS engagement_rate_tb
FROM tiktok_final;

#Phân tích "Khung giờ vàng" (Giả thuyết 1)

SELECT EXTRACT(HOUR FROM publish_time) AS gio_dang, 
       ROUND(AVG(is_trending) * 100, 2) AS ty_le_trending_percent,
       ROUND(AVG((likes + comments + shares) / NULLIF(views, 0) * 100)::numeric, 2) AS engagement_rate
FROM tiktok_final 
GROUP BY 1 ORDER BY gio_dang ASC;

#Tác động của Clickbait đến lượt xem và tương tác (Giả thuyết 2)
SELECT CASE WHEN has_clickbait = 1 THEN 'Có Clickbait' ELSE 'Nội dung chuẩn' END AS loai_noi_dung,
       ROUND(AVG(views)::numeric, 0) AS views_tb,
       ROUND(AVG((likes + comments + shares) / NULLIF(views, 0) * 100)::numeric, 2) AS engagement_rate
FROM tiktok_final GROUP BY has_clickbait;

#So sánh độ sâu tương tác của Video Trending (Giả thuyết 3)
#Chứng minh video xu hướng có tỷ lệ Share và Comment vượt trội.
SELECT is_trending, 
       ROUND(AVG(comments)::numeric, 2) AS comments_tb, 
       ROUND(AVG(shares)::numeric, 2) AS shares_tb,
       ROUND(AVG(likes/NULLIF(views,0)*100)::numeric, 2) AS like_rate
FROM tiktok_final GROUP BY is_trending;

#Phân tích theo Thứ trong tuần
SELECT TO_CHAR(publish_time, 'Day') AS thu_trong_tuan, 
       COUNT(*) AS so_video, 
       ROUND(AVG(views)::numeric, 0) AS views_tb,
       ROUND(AVG((likes + comments + shares) / NULLIF(views, 0) * 100)::numeric, 2) AS engagement_rate
FROM tiktok_final 
GROUP BY 1, EXTRACT(DOW FROM publish_time) ORDER BY EXTRACT(DOW FROM publish_time);

