-- Kiểm tra tổng số dòng của từng bảng thô
SELECT 'YouTube' as Platform, COUNT(*) as Total_Rows FROM raw_youtube
UNION ALL
SELECT 'TikTok' as Platform, COUNT(*) as Total_Rows FROM raw_tiktok;


-- Tạo bảng sạch staging_social_data
CREATE TABLE staging_social_data AS 
SELECT 
    hashtag AS content_id,
    'TikTok' AS platform,
    caption AS title,
    -- Quy đổi likes từ text sang số
    CASE 
        WHEN likes LIKE '%K' THEN (REPLACE(likes, 'K', '')::NUMERIC * 1000)::INT
        WHEN likes LIKE '%M' THEN (REPLACE(likes, 'M', '')::NUMERIC * 1000000)::INT
        ELSE likes::INT 
    END AS likes,
    publish_time::TIMESTAMP AS upload_date
FROM raw_tiktok
UNION ALL
SELECT 
    video_id AS content_id,
    'YouTube' AS platform,
    title,
    likes::INT,
    publish_time::TIMESTAMP AS upload_date
FROM raw_youtube;

-- Xem 10 dòng đầu tiên để kiểm tra cột likes đã là số chưa
SELECT platform, title, likes, upload_date 
FROM staging_social_data 
LIMIT 10;

SELECT 
    platform, 
    COUNT(*) as total_content, 
    SUM(likes) as total_likes,
    ROUND(AVG(likes), 0) as average_likes
FROM staging_social_data
GROUP BY platform;
--Tìm nội dung "đỉnh" nhất của mỗi bên:
(SELECT 'YouTube' as Platform, title, likes FROM staging_social_data WHERE platform = 'YouTube' ORDER BY likes DESC LIMIT 1)
UNION ALL
(SELECT 'TikTok' as Platform, title, likes FROM staging_social_data WHERE platform = 'TikTok' ORDER BY likes DESC LIMIT 1);

-- Tìm tất cả nội dung có chứa chữ 'Trúc Nhân' trong tiêu đề
SELECT platform, title, likes, upload_date
FROM staging_social_data
WHERE title ILIKE '%Trúc Nhân%'
ORDER BY likes DESC;


-- Phân loại video theo mức độ nổi tiếng
SELECT 
    title,
    platform,
    likes,
    CASE 
        WHEN likes >= 100000 THEN '🔥 Siêu Hot'
        WHEN likes >= 10000 THEN '⭐ Xu hướng'
        ELSE '📉 Bình thường'
    END AS engagement_level
FROM staging_social_data
ORDER BY likes DESC;

-- Tính tỷ lệ phần trăm nội dung của mỗi nền tảng
SELECT 
    platform, 
    COUNT(*) AS quantity,
    ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER(), 2) || '%' AS percentage
FROM staging_social_data
GROUP BY platform;
--Kiểm tra phân bổ Video theo khung giờ (Golden Hour)
SELECT 
    EXTRACT(HOUR FROM upload_date) AS khung_gio,
    COUNT(*) AS so_luong_video
FROM staging_social_data
GROUP BY khung_gio
ORDER BY so_luong_video DESC;

--So sánh tương tác trung bình giữa 2 nền tảng
SELECT 
    platform, 
    ROUND(AVG(likes), 0) AS likes_trung_binh,
    SUM(likes) AS tong_luot_like
FROM staging_social_data
GROUP BY platform;
---------------
SELECT 
    content_id, 
    platform, 
    title, 
    likes, 
    upload_date 
FROM staging_social_data 
ORDER BY upload_date DESC 
LIMIT 15;
