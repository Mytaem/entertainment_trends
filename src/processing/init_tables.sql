-- Bước 1: Tạo bảng thô cho TikTok 
CREATE TABLE raw_tiktok (
    id SERIAL PRIMARY KEY,
    hashtag TEXT,
    caption TEXT,
    publish_time TEXT,
    likes TEXT,        
    comments TEXT,     
    is_trending INTEGER,
    has_clickbait INTEGER
);

-- Bước 2: Tạo bảng thô cho YouTube 
CREATE TABLE raw_youtube (
    id SERIAL PRIMARY KEY,
    video_id TEXT,      
    category_id INTEGER, 
    title TEXT,         
    channel_title TEXT,
    category_name TEXT,
    views BIGINT,      
    likes BIGINT,       
    comments BIGINT,   
    publish_time TIMESTAMP, 
    country TEXT       
);

-- Bước 3: Tạo bảng Staging 
CREATE TABLE staging_social_data (
    stg_id SERIAL PRIMARY KEY,
    platform VARCHAR(10),       -- 'TikTok' hoặc 'YouTube'
    content_title TEXT,
    category_name TEXT,
    country TEXT,
    clean_publish_time TIMESTAMP,
    view_count BIGINT,
    like_count BIGINT,
    comment_count BIGINT,
    is_trending BOOLEAN,
    is_clickbait BOOLEAN
);