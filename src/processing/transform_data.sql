
#Kiểm tra bằng con số 
SELECT 'TikTok' as platform, COUNT(*) as total_rows FROM raw_tiktok
UNION ALL
SELECT 'YouTube' as platform, COUNT(*) as total_rows FROM raw_youtube;

#Tạo bảng "Sạch" (Chuẩn hóa số liệu)
CREATE TABLE tiktok_final AS
SELECT 
    hashtag,
    caption,
    publish_time,
    is_trending,
    has_clickbait,
    -- Giữ nguyên các trường khác và xử lý cột Likes
    CASE 
        WHEN likes LIKE '%M' THEN CAST(REPLACE(likes, 'M', '') AS FLOAT) * 1000000
        WHEN likes LIKE '%K' THEN CAST(REPLACE(likes, 'K', '') AS FLOAT) * 1000
        ELSE CAST(NULLIF(likes, '') AS FLOAT)
    END AS likes,
    -- Xử lý cột Comments
    CASE 
        WHEN comments LIKE '%M' THEN CAST(REPLACE(comments, 'M', '') AS FLOAT) * 1000000
        WHEN comments LIKE '%K' THEN CAST(REPLACE(comments, 'K', '') AS FLOAT) * 1000
        ELSE CAST(NULLIF(comments, '') AS FLOAT)
    END AS comments
FROM raw_tiktok;


#Phân tích Giả thuyết 1: Thời điểm đăng tải
SELECT 
    EXTRACT(HOUR FROM publish_time) AS hour_of_day,
    COUNT(*) AS total_videos,
    SUM(is_trending) AS trending_videos,
    ROUND(AVG(is_trending) * 100, 2) AS trending_rate_percentage
FROM tiktok_final
GROUP BY hour_of_day
ORDER BY hour_of_day
#. Phân tích Giả thuyết 2: Nội dung giật gân (Clickbait)
SELECT 
    CASE WHEN has_clickbait = 1 THEN 'Nhóm Clickbait' ELSE 'Nhóm Bình Thường' END AS loai_noi_dung,
    COUNT(*) AS so_luong_video,
    ROUND(AVG(likes)::numeric, 0) AS luot_thich_trung_binh,
    ROUND(AVG(comments)::numeric, 0) AS binh_luan_trung_binh
FROM tiktok_final
GROUP BY has_clickbait;
#Thu ngay dang trong tuan
SELECT 
    TO_CHAR(publish_time, 'Day') AS thu_trong_tuan,
    COUNT(*) AS tong_video,
    ROUND(AVG(likes)::numeric, 0) AS likes_trung_binh,
    ROUND(AVG(is_trending) * 100, 2) AS ty_le_trending
FROM tiktok_final
GROUP BY thu_trong_tuan, EXTRACT(DOW FROM publish_time)
ORDER BY EXTRACT(DOW FROM publish_time);
#Phân tích độ dài Caption: Viết ngắn hay viết dài?
SELECT 
    CASE 
        WHEN LENGTH(caption) < 50 THEN 'Ngắn (<50 ký tự)'
        WHEN LENGTH(caption) BETWEEN 50 AND 150 THEN 'Vừa (50-150 ký tự)'
        ELSE 'Dài (>150 ký tự)'
    END AS do_dai_caption,
    COUNT(*) AS so_luong,
    ROUND(AVG(is_trending) * 100, 2) AS ty_le_viral
FROM tiktok_final
GROUP BY do_dai_caption;


