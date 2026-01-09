Tôi đang research về CHỦ ĐỀ : XU HƯỚNG GIẢI TRÍ (YOUTUBE/SPOTIFY TRENDING),việc của tôi là thu thập nguồn data để phân tích, hãy chỉ ra giúp tôi các nguồn để crawl
Dưới đây là các NGUỒN DATA UY TÍN & THỰC TẾ để crawl / thu thập dữ liệu phục vụ research XU HƯỚNG GIẢI TRÍ (YouTube / Spotify Trending). Anh chia theo mức độ “chuẩn nghiên cứu → dễ crawl → dễ phân tích” để em chọn đúng hướng 👇

I. NGUỒN CHÍNH THỐNG (API – khuyến nghị dùng cho research)
1. YouTube Data API v3
📌 Phân tích xu hướng video, creator, nội dung
Dữ liệu crawl được
Video trending theo quốc gia
View, like, comment, publish time
Channel info (subscriber, category)
Tags, title, description
Endpoint quan trọng
videos?chart=mostPopular
search?order=viewCount
commentThreads
🔗 https://developers.google.com/youtube/v3
💡 Dùng cho:
Phân tích nội dung viral
So sánh trend VN vs US
Phân loại chủ đề giải trí (music, vlog, shorts)

2. Spotify Web API
📌 Phân tích xu hướng âm nhạc & podcast
Dữ liệu crawl được
Spotify Top 50 / Viral 50 (theo quốc gia)
Audio features (tempo, energy, valence…)
Artist popularity
Playlist metadata
Endpoint quan trọng
/playlists/{id}
/tracks/{id}/audio-features
/artists/{id}
🔗 https://developer.spotify.com/documentation/web-api
💡 Dùng cho:
Phân tích nhạc trending
So sánh xu hướng cảm xúc âm nhạc
Dự đoán hit song

II. NGUỒN TREND THEO THỜI GIAN (CỰC QUAN TRỌNG)
3. Google Trends
📌 Xu hướng tìm kiếm liên quan giải trí
Dữ liệu
Keyword popularity theo thời gian
So sánh nhiều từ khóa
Theo khu vực (VN, Global)
🔗 https://trends.google.com
🔗 Python: pytrends
💡 Dùng cho:
Phát hiện trend sớm (before viral)
Mapping YouTube / Spotify ↔ search behavior

4. Chartmetric (có phí)
📌 Music intelligence chuyên nghiệp
Dữ liệu
Cross-platform trend (Spotify, YouTube, TikTok)
Artist growth
Playlist reach
🔗 https://chartmetric.com
💡 Dùng cho: paper / thesis / báo cáo doanh nghiệp

III. NGUỒN WEB SCRAPING (KHÔNG CÓ API / DỄ LÀM)
5. YouTube Trending Page (Scraping)
🔗 https://www.youtube.com/feed/trending
Crawl được
Title
View count
Category
Rank trending
⚠️ Không ổn định lâu dài → dùng cho snapshot analysis

6. Spotify Charts (Web)
🔗 https://charts.spotify.com
Crawl được
Rank bài hát
Artist
Số stream
Quốc gia / ngày
💡 Phù hợp làm time-series analysis

IV. NGUỒN MXH BỔ TRỢ (BẮT TREND NHANH)
7. TikTok Trending
📌 Nguồn phát sinh trend giải trí
Dữ liệu
Hashtag trending
Sound viral
View growth
🔗 https://www.tiktok.com/trends
⚠️ Crawl khó → dùng Selenium / Playwright

8. Twitter / X
📌 Phản ứng cộng đồng & viral discussion
Dữ liệu
Trending hashtag
Tweet volume
Sentiment
🔗 https://developer.x.com

V. DATASET CÓ SẴN (NHANH – PHÙ HỢP NCKH)
9. Kaggle
📌 Dataset YouTube / Spotify đã clean
Ví dụ:
YouTube Trending Videos Dataset
Spotify Top Charts
Music popularity dataset
🔗 https://www.kaggle.com/datasets
💡 Phù hợp khi deadline gấp

VI. GỢI Ý KIẾN TRÚC PIPELINE THU THẬP DATA
[YouTube API] ─┐
               ├─→ Data Lake → Feature Engineering → Trend Analysis
[Spotify API] ─┤
               ├─→ Google Trends (validate)
[Web Scraping] ─┘


VII. GỢI Ý CÂU HỎI NGHIÊN CỨU (RẤT HAY)
Video trending trước hay search trend trước?
Nhạc có tempo cao có dễ viral hơn?
Creator nhỏ có thể vào trending không?
TikTok → Spotify → YouTube: dòng chảy trend?

VIII. Nếu em muốn, anh có thể giúp tiếp
✅ Viết crawler Python (YouTube / Spotify)
✅ Thiết kế schema database
✅ Gợi ý đề tài NCKH / paper quốc tế
✅ Vẽ biểu đồ trend + dashboard
👉 Em đang làm bài học / NCKH / startup / báo cáo doanh nghiệp? Anh sẽ tối ưu nguồn cho đúng mục tiêu.
Dự liệu tôi cần khoảng hơn 10000 data, vậy tôi sẽ làm trên những nền tảng nào
Với yêu cầu >10.000 data (records) để phân tích xu hướng giải trí (YouTube / Spotify Trending), anh khuyên KHÔNG nên dàn trải quá nhiều nền tảng, mà chọn ít nhưng “đẻ data nhiều – ổn định – dễ mở rộng”.
Dưới đây là cấu hình nền tảng TỐI ƯU THỰC TẾ 👇

✅ CẤU HÌNH KHUYẾN NGHỊ (ĐỦ >10.000 DATA, PHÙ HỢP RESEARCH)
🔴 BẮT BUỘC (Core Data – 80% dataset)
1️⃣ YouTube Data API
📌 Nguồn data lớn nhất – giàu nhất
Vì sao chọn
Mỗi ngày mỗi quốc gia có ~200 video trending
10 quốc gia × 30 ngày = ~60.000 video
Mỗi video có 20–50 feature
Data thu được
video_id, title, tags
view_count, like_count, comment_count
publish_time, category
channel_id, subscriber_count
👉 Chỉ cần YouTube là đã vượt 10.000 record

2️⃣ Spotify Web API
📌 Chuẩn để phân tích xu hướng âm nhạc
Quy mô data
Top 50 + Viral 50
50 × 2 × 20 quốc gia × 30 ngày
→ ~60.000 track records
Data mạnh
popularity
audio_features (danceability, energy, tempo…)
artist popularity
👉 RẤT PHÙ HỢP làm ML / clustering / trend prediction

🟡 BỔ TRỢ (Trend Validation – 15%)
3️⃣ Google Trends
📌 Xác nhận xu hướng theo hành vi người dùng
Data
interest_over_time
interest_by_region
Không tính là record content, nhưng:
validate trend
phát hiện trend sớm
👉 Dùng làm feature phụ

🟢 MỞ RỘNG (Nếu cần paper mạnh – 5%)
4️⃣ Spotify Charts (Web scraping)
📌 https://charts.spotify.com
Rank theo ngày
Stream count
Quốc gia
👉 Dùng khi muốn time-series chính xác

5️⃣ TikTok (tùy chọn)
📌 Nếu nghiên cứu nguồn phát sinh trend
hashtag
sound
view growth
⚠️ Crawl khó – không cần nếu mới làm research

📊 GỢI Ý CẤU HÌNH DATASET (>10.000 RECORD)
Nền tảng
Số record/tháng (ước tính)
YouTube Trending (10 quốc gia)
40.000 – 60.000
Spotify Top + Viral
40.000 – 60.000
Google Trends
feature phụ
TỔNG
>80.000 record

👉 Chỉ cần 2 nền tảng: YouTube + Spotify là đủ và dư

🧠 GỢI Ý DATA SCHEMA (để dễ phân tích)
YouTube
video_id | title | category | views | likes | comments | publish_time | country

Spotify
track_id | artist | popularity | tempo | energy | danceability | date | country


🎯 KẾT LUẬN NGẮN GỌN (QUAN TRỌNG)
🔥 Nếu cần >10.000 data cho research → CHỌN:
✅ YouTube Data API
✅ Spotify Web API
❌ Không cần TikTok lúc đầu
❌ Không cần crawl MXH phức tạp

🚀 Anh có thể hỗ trợ tiếp
Viết crawler Python (YouTube + Spotify)
Tối ưu quota API
Gợi ý đề tài nghiên cứu cụ thể
Thiết kế pipeline + database
👉 Em đang làm NCKH sinh viên / thesis / báo cáo học phần / startup insight? Nói anh biết để anh tối ưu hướng crawl cho đúng chuẩn 👌
tôi muốn có hơn 10000 nguôn data để phân tích nhưng tôi muốn dữ liệu của tôi phải ở nhiều lĩnh vực khác nhau: âm nhạc, video, hài hước,...
Rất rõ yêu cầu 👍
👉 >10.000 data, đa lĩnh vực giải trí (âm nhạc – video – hài hước – lifestyle – gaming…)
👉 Mục tiêu phân tích xu hướng, không lệch 1 domain
Anh sẽ trả lời theo góc nhìn thiết kế DATASET CHUẨN NGHIÊN CỨU, không chỉ liệt kê nền tảng.

🎯 CHIẾN LƯỢC TỐI ƯU NHẤT (ĐA LĨNH VỰC – >10.000 DATA)
Chìa khóa:
🔹 Ít nền tảng nhưng nhiều category
🔹 Mỗi nền tảng đóng vai trò 1 kiểu nội dung

I. NỀN TẢNG BẮT BUỘC (CORE – 70% DATA)
1️⃣ YouTube Data API
📌 Xương sống cho đa lĩnh vực giải trí
Lý do chọn
Có rất nhiều category
Trending theo quốc gia + thời gian
Data public, chuẩn nghiên cứu
🎭 Lĩnh vực bao phủ
Category YouTube
Lĩnh vực
Music
Âm nhạc
Comedy
Hài hước
Entertainment
Giải trí tổng hợp
People & Blogs
Vlog
Gaming
Game
Film & Animation
Phim, hoạt hình

📊 Quy mô
~200 video trending/ngày/quốc gia
10 quốc gia × 30 ngày → ~60.000 video
👉 Chỉ YouTube đã đủ đa lĩnh vực

2️⃣ Spotify Web API
📌 Chuyên sâu âm nhạc (không thể thiếu)
Bao phủ
Nhạc pop, rap, EDM, indie
Podcast giải trí
📊 Quy mô
Top 50 + Viral 50
20 quốc gia × 30 ngày
→ ~60.000 track
👉 Tách riêng âm nhạc để phân tích sâu

II. NỀN TẢNG PHẢN ÁNH HÀNH VI (15% DATA)
3️⃣ TikTok (Hashtag + Sound)
📌 Nguồn phát sinh trend hài hước / viral
Lĩnh vực
Hài hước
Challenge
Meme
Sound viral
📊 Quy mô
200 hashtag/sound
Mỗi hashtag ~50–100 video summary
→ 10.000+ record
⚠️ Crawl khó → chỉ lấy metadata

4️⃣ Google Trends
📌 Xác nhận xu hướng xã hội
Lĩnh vực
Tên bài hát
Creator
Show giải trí
Meme
👉 Không tính là content chính, dùng làm feature hỗ trợ

III. MỞ RỘNG THEO “HÀI HƯỚC – CỘNG ĐỒNG” (OPTIONAL)
5️⃣ Reddit
📌 Community-based humor & trends
Subreddit
r/funny
r/videos
r/memes
r/music
📊 Quy mô
5 subreddit × 30 post/ngày × 30 ngày
→ ~4.500 post

6️⃣ X (Twitter)
📌 Reaction + meme lifecycle
Trending hashtag
Tweet volume

IV. CẤU HÌNH DATASET KHUYẾN NGHỊ (CHUẨN & ĐẸP)
Lĩnh vực
Nền tảng
Record
Video đa lĩnh vực
YouTube
30.000 – 50.000
Âm nhạc
Spotify
30.000 – 50.000
Hài hước / Viral
TikTok
10.000 – 20.000
Xu hướng xã hội
Google Trends
Feature phụ
TỔNG


>70.000 data


V. THIẾT KẾ DATASET THEO LĨNH VỰC (RẤT QUAN TRỌNG)
🎵 Music
platform | track_id | artist | popularity | tempo | energy | date | country

🎥 Video
platform | video_id | category | views | likes | comments | publish_time

😂 Humor / Viral
platform | hashtag | content_type | views | growth_rate | date


VI. KẾT LUẬN NGẮN GỌN (CHỐT PHƯƠNG ÁN)
✅ Muốn >10.000 data + đa lĩnh vực
👉 BẮT BUỘC: YouTube + Spotify
👉 MỞ RỘNG: TikTok
👉 VALIDATE: Google Trends
❌ Không nên chỉ dùng 1 nền tảng
❌ Không nên crawl quá sâu TikTok lúc đầu

🚀 Anh hỗ trợ được gì tiếp?
Vẽ sơ đồ pipeline crawl
Viết code crawl Python (multi-platform)
Gợi ý đề tài nghiên cứu chuẩn hội đồng
Tư vấn dataset structure để publish (Kaggle / paper)
👉 Cho anh biết:
Em làm bài học phần, NCKH sinh viên hay thesis?
Anh sẽ tinh chỉnh dataset cho đúng “chuẩn chấm điểm” 💯
hãy cho tôi Thiết kế kiến trúc hệ thống (Docker Diagram) với Những yếu tố nào (thời điểm đăng tải, mức độ tương tác, tiêu đề, phản hồi tiêu cực) ảnh hưởng đáng kể đến khả năng một nội dung lọt vào danh sách Trending trên YouTube và Spotify? Câu hỏi này được chia nhỏ thành các giả thuyết cụ thể , và sẽ được kiểm định thông qua dữ liệu thu thập từ APIs của hai nền tảng.
Dưới đây là thiết kế kiến trúc hệ thống dạng Docker (Docker Diagram) + bộ giả thuyết (hypotheses) chia nhỏ để kiểm định câu hỏi:
“Những yếu tố nào (thời điểm đăng tải, mức độ tương tác, tiêu đề, phản hồi tiêu cực) ảnh hưởng đáng kể đến khả năng một nội dung lọt Trending trên YouTube và Spotify?”
Mình thiết kế theo hướng: thu thập dữ liệu từ API → chuẩn hóa → tạo feature → gán nhãn Trending/Not → kiểm định giả thuyết + mô hình hóa.

1) Docker Diagram (kiến trúc tổng thể)
A. Luồng dữ liệu cấp cao
Scheduler chạy theo giờ/ngày
Collectors gọi API YouTube/Spotify để lấy “candidate items” + metrics
Đẩy vào Queue để xử lý không nghẽn
ETL/Normalizer chuẩn hóa schema chung
Feature Builder tạo biến nghiên cứu (interaction rate, publish timing, title features…)
Sentiment/Toxicity xử lý phản hồi tiêu cực (từ comment/description text…)
DB + Object Storage lưu dữ liệu thô + dữ liệu chuẩn hóa
Stats/Model Service chạy kiểm định giả thuyết (logistic regression, mixed effects…)
Dashboard/Notebook xem kết quả
B. ASCII Docker Diagram (dễ đưa vào report)
                  ┌──────────────────────────────┐
                   │        docker-compose         │
                   └──────────────────────────────┘

┌──────────────┐        ┌───────────────┐       ┌───────────────┐
│   Scheduler  │  cron  │  YT Collector │       │ SP Collector  │
│  (Airflow/   ├───────►│ (YouTube API) │       │ (Spotify API) │
│   Prefect)   │        └───────┬───────┘       └───────┬───────┘
└───────┬──────┘                │                       │
        │                        │                       │
        │                        └──────────┬────────────┘
        │                                   │
        ▼                                   ▼
┌──────────────────┐                ┌──────────────────┐
│ Message Queue     │   events/job   │  Raw Storage      │
│ (Redis/RabbitMQ)  ├───────────────►│  (MinIO/S3)       │
└─────────┬────────┘                └─────────┬────────┘
          │                                   │
          ▼                                   │
┌──────────────────┐                         │
│ ETL / Normalizer  │  clean+join+dedupe      │
│ (Python/FastAPI)  ├───────────────┐         │
└─────────┬────────┘               │         │
          ▼                        ▼         ▼
┌──────────────────┐        ┌────────────────────┐
│ Feature Builder   │        │ Sentiment/Toxicity │
│ (rates, timing,   │        │ (comments/text)    │
│ title NLP feats)  │        └─────────┬──────────┘
└─────────┬────────┘                  │
          └──────────────┬────────────┘
                         ▼
                 ┌──────────────────┐
                 │ Analytics DB      │
                 │ (Postgres)        │
                 └───────┬──────────┘
                         ▼
                 ┌──────────────────┐
                 │ Stats/Model       │
                 │ (Jupyter/MLflow)  │
                 └───────┬──────────┘
                         ▼
                 ┌──────────────────┐
                 │ Dashboard         │
                 │ (Metabase/Grafana)│
                 └──────────────────┘


2) Các service Docker nên có (tối thiểu)
scheduler: Airflow/Prefect (hoặc cron container)
yt_collector: YouTube Data API collector
sp_collector: Spotify Web API collector (+ optional charts scraper nếu cần stream chart)
queue: Redis/RabbitMQ
etl_normalizer: chuẩn hóa schema + dedupe + join
feature_builder: tạo biến nghiên cứu
sentiment_service: sentiment/toxicity cho phản hồi tiêu cực
postgres: lưu bảng chuẩn hóa + features
minio: lưu raw json responses, log, snapshots
notebook hoặc stats_model: kiểm định giả thuyết / mô hình
dashboard: Metabase/Grafana

3) Điểm rất quan trọng về “Trending label”
YouTube
Có thể lấy danh sách Trending theo quốc gia (tùy API/quyền hạn hiện hành), hoặc snapshot trang/nguồn trending tương ứng.
Gán nhãn: is_trending = 1 nếu item xuất hiện trong trending list tại thời điểm snapshot.
Spotify
Spotify Web API không có “trending list” chuẩn như YouTube. Thực tế thường dùng:
Spotify Charts (Top/ Viral theo quốc gia/ngày) để làm label tương đương “Trending”
Hoặc dùng track popularity (0–100) làm proxy (nhưng không “trending list” thật sự)
Nếu bạn nói “kiểm định bằng API Spotify”, mình khuyến nghị nhãn:
is_charting = 1 nếu track nằm trong chart playlist/ charts dataset tại ngày đó.
Nếu bạn buộc “chỉ API” mà không dùng charts: bạn vẫn làm được nghiên cứu “khả năng đạt popularity cao”, nhưng không đúng nghĩa ‘lọt Trending list’ như YouTube.

4) Biến nghiên cứu: mapping đúng với câu hỏi của bạn
(A) Thời điểm đăng tải (Timing)
publish_hour_local (0–23)
publish_dow (Mon–Sun)
publish_is_weekend
age_hours_at_snapshot (bao nhiêu giờ kể từ lúc đăng đến lúc đo)
(B) Mức độ tương tác (Engagement)
YouTube
views, likes, comments
like_rate = likes/views
comment_rate = comments/views
view_velocity = Δviews / Δtime (cực quan trọng, cần đo lặp theo giờ)
Spotify
popularity (API có)
Nếu dùng charts: streams, rank, rank_change
(Spotify API không cung cấp likes/dislikes/comments cho track kiểu mạng xã hội)
(C) Tiêu đề (Title features)
YouTube
title_length, caps_ratio, emoji_count
has_trending_keywords (từ khóa nhạc/hài/official/mv…)
NLP embedding/TF-IDF
Spotify
track_name_length, explicit, artist_followers (artist endpoint)
(D) Phản hồi tiêu cực (Negative feedback)
YouTube (làm được tương đối tốt)
Sentiment/ токсicity từ comments
neg_comment_ratio, toxicity_mean
controversy = std(sentiment) hoặc tỷ lệ cực đoan
Spotify (hạn chế nếu chỉ API)
Spotify API không có comment/dislike/skip rate.
Proxy gợi ý (nếu chấp nhận mở rộng):
sentiment từ mạng xã hội (X/Reddit) theo track/artist
hoặc dùng “biến bất ổn chart”: rớt hạng nhanh là dấu hiệu phản ứng kém

5) Bộ giả thuyết chia nhỏ (để kiểm định)
Nhóm H1: Timing
H1a (YouTube): Video đăng vào “khung giờ vàng” (theo timezone quốc gia) có xác suất vào Trending cao hơn.
H1b (Spotify): Track phát hành vào các ngày “release cycle” (ví dụ Fri) có xác suất charting cao hơn.
H1c (Cross-platform): Nội dung “trẻ” (age_hours thấp) có odds vào trending/charting cao hơn (hiệu ứng bệ phóng sớm).
Nhóm H2: Engagement (tốc độ quan trọng hơn tổng)
H2a (YouTube): view_velocity là yếu tố dự báo trending mạnh hơn views tại một thời điểm.
H2b (YouTube): like_rate và comment_rate tăng odds trending sau khi đã kiểm soát view_velocity.
H2c (Spotify): (Nếu có charts) stream_velocity (tốc độ tăng streams/rank) dự báo charting mạnh hơn popularity tĩnh.
Nhóm H3: Title / Text
H3a (YouTube): Tiêu đề có đặc trưng “hook” (độ dài vừa, có từ khóa/emoji/caps hợp lý) tăng odds trending.
H3b (YouTube): Tiêu đề “giật tít quá mức” (caps_ratio cao, ký tự đặc biệt quá nhiều) có thể tăng click nhưng không tăng trending khi kiểm soát dislike proxy/negative sentiment.
H3c (Spotify): Track name + artist popularity đóng góp đáng kể vào khả năng charting (proxy: popularity + artist_followers).
Nhóm H4: Negative feedback
H4a (YouTube): Tỷ lệ bình luận tiêu cực cao làm giảm xác suất trending (giữ nguyên engagement).
H4b (YouTube): “Controversy” có thể có hiệu ứng chữ U: vừa phải có lợi (bàn tán), quá cao bất lợi.
H4c (Spotify): Nếu dùng proxy (social sentiment hoặc rớt hạng nhanh), phản hồi tiêu cực liên quan đến “fall-off” nhanh khỏi chart.
Nhóm H5: Khác biệt theo lĩnh vực (music/comedy/gaming…)
H5a: Ảnh hưởng của timing/engagement/title khác nhau theo category (interaction terms).
H5b: Comedy phụ thuộc mạnh vào “title hook + comment_rate”, còn Music phụ thuộc mạnh vào “velocity”.

6) Cách kiểm định (đúng kiểu nghiên cứu)
Biến phụ thuộc
YouTube: is_trending_at_t = 1/0
Spotify: is_charting_at_date = 1/0 (khuyến nghị dùng charts label)
Mô hình thống kê khuyến nghị
Logistic Regression (giải thích được, phù hợp hypothesis)
logit(P(trending)) ~ timing + velocity + rates + title_feats + neg_sent + controls
Mixed-effects / Hierarchical
random effects theo country, category, channel/artist
giúp không bias vì creator lớn
Survival / Time-to-trend
“mất bao lâu để vào trending” là biến rất hay nếu bạn snapshot theo giờ
Controls (biến kiểm soát bắt buộc)
country, category
channel_subscribers (YT) / artist_followers (Spotify)
duration (video length) nếu có
is_official, is_verified (nếu lấy được)

7) Output bạn nên có trong report
Docker architecture diagram (như trên)
Data dictionary (schema + feature definitions)
Hypothesis table (H1–H5)
Model table (odds ratio, p-value, CI)
Ablation: bỏ velocity xem rớt bao nhiêu
Cross-platform comparison: yếu tố nào “phổ quát”, yếu tố nào “riêng nền tảng”

Nếu bạn muốn, mình có thể viết luôn:
docker-compose.yml mẫu (Postgres + MinIO + Redis + collectors + feature + sentiment)
schema Postgres (tables: raw_events, items, snapshots, features, labels)
template notebook kiểm định H1–H5 (logistic + mixed effects)
Bạn định thu dữ liệu theo mốc thời gian nào (mỗi 1 giờ hay mỗi 6 giờ / mỗi ngày)? Chọn nhịp lấy mẫu sẽ quyết định bạn có đo được velocity “chuẩn” hay không.

CHỦ ĐỀ 4: XU HƯỚNG GIẢI TRÍ (YOUTUBE/SPOTIFY TRENDING)

Mục tiêu crawl: YouTube Data API v3, Spotify Web API.

Nhiệm vụ: Thu thập thông tin video/bài hát top trending (View, Like, Comment, Title, Duration, Upload time). ADY201m

Chào bạn, với môn ADY201m (thường là môn về kỹ thuật thu thập và xử lý dữ liệu), chủ đề Xu hướng giải trí là một chủ đề rất hay và thực tế.

Dưới đây là hướng dẫn chi tiết cách triển khai code Python để crawl dữ liệu từ YouTube Data API v3 và Spotify Web API theo đúng yêu cầu của bạn.

PHẦN 1: YOUTUBE DATA API V3
YouTube API cung cấp chính xác các trường dữ liệu bạn cần thông qua endpoint videos().list với tham số chart='mostPopular'.

1. Chuẩn bị
Tạo project trên Google Cloud Console.

Kích hoạt YouTube Data API v3.

Tạo API Key.

Cài thư viện: pip install google-api-python-client pandas isodate

(Lưu ý: thư viện isodate dùng để xử lý Duration dạng ISO 8601 của YouTube).

2. Code mẫu (Python)
Python
from googleapiclient.discovery import build
import pandas as pd
import isodate

# CẤU HÌNH
API_KEY = 'YOUR_YOUTUBE_API_KEY_HERE'
YOUTUBE_API_SERVICE_NAME = 'youtube'
YOUTUBE_API_VERSION = 'v3'

def get_youtube_trending(region_code='VN', max_results=50):
    youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=API_KEY)

    # Gọi API lấy video thịnh hành
    request = youtube.videos().list(
        part='snippet,statistics,contentDetails',
        chart='mostPopular',
        regionCode=region_code, # VN cho Việt Nam, US cho Mỹ...
        maxResults=max_results
    )
    response = request.execute()

    data = []
    for item in response['items']:
        # Xử lý thời lượng (Duration) từ dạng PT15M33S sang giây hoặc phút
        duration_iso = item['contentDetails']['duration']
        duration_seconds = isodate.parse_duration(duration_iso).total_seconds()

        video_info = {
            'Title': item['snippet']['title'],
            'Upload Time': item['snippet']['publishedAt'],
            'View': int(item['statistics'].get('viewCount', 0)),
            'Like': int(item['statistics'].get('likeCount', 0)),
            'Comment': int(item['statistics'].get('commentCount', 0)),
            'Duration (s)': duration_seconds,
            'Channel': item['snippet']['channelTitle']
        }
        data.append(video_info)
    
    return pd.DataFrame(data)

# CHẠY THỬ
df_youtube = get_youtube_trending()
print(df_youtube.head())
# df_youtube.to_csv('youtube_trending.csv', index=False)
PHẦN 2: SPOTIFY WEB API
Lưu ý quan trọng: Spotify Web API KHÔNG cung cấp số lượt nghe (Play/View count) cụ thể cho từng bài hát qua API (họ giấu thông tin này). Họ chỉ cung cấp chỉ số Popularity (0-100).

Nếu đề bài bắt buộc phải có số View chính xác, bạn có thể phải giải trình về hạn chế của API, hoặc sử dụng thư viện BeautifulSoup/Selenium để cào từ giao diện web (nhưng cách này phức tạp và dễ bị chặn).

Dưới đây là cách dùng API chuẩn.

1. Chuẩn bị
Truy cập Spotify for Developers.

Tạo App để lấy Client ID và Client Secret.

Cài thư viện: pip install spotipy pandas

2. Code mẫu (Python)
Spotify không có endpoint "Trending" chung chung như YouTube, cách tốt nhất là crawl Playlist Top 50 (Ví dụ: Top 50 Vietnam).

Python
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd

# CẤU HÌNH
CLIENT_ID = 'YOUR_SPOTIFY_CLIENT_ID'
CLIENT_SECRET = 'YOUR_SPOTIFY_CLIENT_SECRET'

# ID của Playlist "Top 50 - Vietnam" (Có thể tìm ID này trên link chia sẻ playlist spotify)
PLAYLIST_ID = '37i9dQZEVXbLdGSmz6xU5l' 

def get_spotify_trending():
    # Xác thực
    client_credentials_manager = SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

    # Lấy track từ playlist
    results = sp.playlist_tracks(PLAYLIST_ID)
    tracks = results['items']

    data = []
    for item in tracks:
        track = item['track']
        
        # Spotify API không trả về Like/View, thay vào đó là Popularity
        song_info = {
            'Title': track['name'],
            'Artist': track['artists'][0]['name'],
            'Upload Time': track['album']['release_date'], # Ngày phát hành album
            'Duration (ms)': track['duration_ms'],
            'Popularity (0-100)': track['popularity'], # Thay thế cho View/Like
            'Spotify URL': track['external_urls']['spotify']
        }
        data.append(song_info)

    return pd.DataFrame(data)

# CHẠY THỬ
df_spotify = get_spotify_trending()
print(df_spotify.head())
# df_spotify.to_csv('spotify_trending.csv', index=False)
CÁC MẸO CHO BÀI ASSIGNMENT (ADY201m)
Xử lý dữ liệu (Data Cleaning):

YouTube Duration: API trả về dạng PT5M20S (ISO 8601). Bắt buộc phải dùng thư viện isodate hoặc viết hàm regex để chuyển về số giây/phút thì mới tính toán thống kê được.

Thời gian (Upload Time): Nên convert về dạng datetime object của Pandas để dễ sort hoặc vẽ biểu đồ theo thời gian.

Hạn chế của Spotify:

Trong báo cáo, hãy ghi rõ: "Spotify Web API official không public số lượt stream count (View). Em sử dụng chỉ số Popularity để thay thế độ thịnh hành." Điều này cho thấy bạn hiểu rõ tài liệu kỹ thuật.

Hạn ngạch (Quota):

YouTube API giới hạn 10.000 đơn vị/ngày. Mỗi lần gọi videos().list tốn 1 đơn vị. Bạn thoải mái test nhưng đừng chạy vòng lặp vô tận.

Mở rộng (Bonus):

Bạn có thể so sánh tiêu đề (Title) của Top YouTube và Top Spotify xem có sự trùng lặp không (người nghe nhạc trên YouTube có giống trên Spotify không).

Chúc bạn hoàn thành tốt bài Assignment! Nếu cần giải thích thêm đoạn code nào, cứ hỏi nhé.

cào 10k data

Để cào được 10.000 (10k) dòng dữ liệu từ YouTube và Spotify API là một thách thức không nhỏ vì các danh sách "Trending/Top" thường rất ngắn (chỉ khoảng 50-200 item mỗi quốc gia).

Để đạt con số 10k, bạn không thể chỉ cào Trending Việt Nam. Bạn cần chiến lược "Quét diện rộng" (Multi-region) hoặc "Tìm kiếm theo từ khóa" (Search Query).

Dưới đây là chiến lược và code mẫu tối ưu để đạt 10k data mà không bị khóa API (đặc biệt là YouTube).

PHẦN 1: CHIẾN LƯỢC YOUTUBE (Quan trọng: Quản lý Quota)
Bài toán Quota (Hạn ngạch):

YouTube Free Tier cho: 10.000 units/ngày.

Lệnh search() (Tìm kiếm): Tốn 100 units/lần gọi. (Chỉ gọi được 100 lần là hết quota -> Cào được tối đa 5.000 video). -> KHÔNG KHẢ THI CHO 10K.

Lệnh videos().list (Lấy Trending): Tốn 1 unit/lần gọi. (Gọi được 10.000 lần -> Cào thoải mái). -> KHẢ THI.

Giải pháp: Duyệt qua danh sách các mã quốc gia (Region Code) trên thế giới để lấy Top Trending của nhiều nước (Mỹ, Anh, Nhật, Hàn, Ấn Độ...).

Giả sử 1 nước có 50-200 video trending.

Cần khoảng 50-60 nước để đủ 10k data.

Code mẫu YouTube (Multi-Region Scraper)
Python
from googleapiclient.discovery import build
import pandas as pd
import isodate
import time

# CẤU HÌNH
API_KEY = 'YOUR_API_KEY'
YOUTUBE = build('youtube', 'v3', developerKey=API_KEY)

# Danh sách mã quốc gia (ISO 3166-1 alpha-2)
COUNTRY_CODES = [
    'VN', 'US', 'KR', 'JP', 'IN', 'GB', 'CA', 'DE', 'FR', 'BR', 
    'RU', 'MX', 'ID', 'TH', 'PH', 'ES', 'IT', 'AU', 'TW', 'MY',
    'SA', 'TR', 'PL', 'SE', 'AR', 'NL', 'CO', 'ZA', 'UA', 'EG',
    # Bạn có thể thêm nhiều mã khác nếu chưa đủ data
]

def get_video_details(video_items, region):
    data = []
    for item in video_items:
        try:
            # Xử lý duration
            duration_iso = item['contentDetails'].get('duration', 'PT0S')
            duration_sec = isodate.parse_duration(duration_iso).total_seconds()
            
            # Lấy thống kê (có thể bị ẩn)
            stats = item.get('statistics', {})
            
            row = {
                'Video ID': item['id'],
                'Title': item['snippet']['title'],
                'Published At': item['snippet']['publishedAt'],
                'Channel': item['snippet']['channelTitle'],
                'Views': int(stats.get('viewCount', 0)),
                'Likes': int(stats.get('likeCount', 0)),
                'Comments': int(stats.get('commentCount', 0)),
                'Duration (s)': duration_sec,
                'Region': region  # Để biết video này trending ở đâu
            }
            data.append(row)
        except Exception as e:
            continue
    return data

def crawl_youtube_10k():
    all_videos = []
    
    print("Bắt đầu cào dữ liệu...")
    
    for region in COUNTRY_CODES:
        print(f"--> Đang lấy Trending của {region}...")
        next_page_token = None
        
        # Lấy tối đa khoảng 200 video mỗi nước (4 trang, mỗi trang 50)
        for _ in range(4): 
            try:
                request = YOUTUBE.videos().list(
                    part='snippet,statistics,contentDetails',
                    chart='mostPopular',
                    regionCode=region,
                    maxResults=50,
                    pageToken=next_page_token
                )
                response = request.execute()
                
                # Xử lý data
                items = response.get('items', [])
                if not items: break
                
                all_videos.extend(get_video_details(items, region))
                
                # Pagination
                next_page_token = response.get('nextPageToken')
                if not next_page_token: break
                
            except Exception as e:
                print(f"Lỗi tại {region}: {e}")
                break
        
        print(f"    Hiện có tổng: {len(all_videos)} videos")
        if len(all_videos) >= 10000:
            print("ĐÃ ĐẠT MỤC TIÊU 10K!")
            break

    # Chuyển thành DataFrame và lọc trùng lặp (vì 1 video có thể trending ở nhiều nước)
    df = pd.DataFrame(all_videos)
    df_unique = df.drop_duplicates(subset=['Video ID'])
    
    print(f"Tổng thu được: {len(df)} dòng. Sau khi lọc trùng: {len(df_unique)} dòng.")
    df_unique.to_csv('youtube_10k_dataset.csv', index=False, encoding='utf-8-sig')

# CHẠY
crawl_youtube_10k()
PHẦN 2: CHIẾN LƯỢC SPOTIFY (Dễ thở hơn)
Spotify không có giới hạn ngặt nghèo như YouTube (chỉ cần handle rate limit - lỗi 429). Để lấy 10k bài hát, chúng ta dùng phương pháp Search theo năm phát hành.

Giải pháp: Loop qua các năm (ví dụ từ 2015 đến 2025). Mỗi năm search lấy 1000 bài hát phổ biến nhất.

Code mẫu Spotify (Search Loop)
Python
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd
import time

# CẤU HÌNH
CLIENT_ID = 'YOUR_ID'
CLIENT_SECRET = 'YOUR_SECRET'

sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET))

def crawl_spotify_10k():
    all_tracks = []
    years = range(2015, 2025) # Quét từ năm 2015 đến 2024
    
    for year in years:
        print(f"--> Đang cào dữ liệu nhạc năm {year}...")
        
        # Spotify cho phép offset tối đa 1000 items cho search
        for offset in range(0, 1000, 50): 
            try:
                # Query cú pháp: "year:2023"
                results = sp.search(q=f'year:{year}', type='track', limit=50, offset=offset)
                tracks = results['tracks']['items']
                
                if not tracks: break
                
                for t in tracks:
                    row = {
                        'Track ID': t['id'],
                        'Track Name': t['name'],
                        'Artist': t['artists'][0]['name'],
                        'Album': t['album']['name'],
                        'Release Date': t['album']['release_date'],
                        'Popularity': t['popularity'],
                        'Duration (ms)': t['duration_ms']
                    }
                    all_tracks.append(row)
                
                # Nghỉ nhẹ để tránh lỗi 429 (Too Many Requests)
                time.sleep(0.5)
                
            except Exception as e:
                print(f"Lỗi: {e}. Đang chờ 5s...")
                time.sleep(5)
                continue
                
        print(f"    Tổng hiện tại: {len(all_tracks)}")
        if len(all_tracks) >= 10000: break

    # Lưu file
    df = pd.DataFrame(all_tracks)
    # Lọc trùng (đề phòng 1 bài hát hiện ở nhiều query)
    df_unique = df.drop_duplicates(subset=['Track ID'])
    
    print(f"Hoàn thành! Đã lưu {len(df_unique)} bài hát.")
    df_unique.to_csv('spotify_10k_dataset.csv', index=False, encoding='utf-8-sig')

# CHẠY
crawl_spotify_10k()
LƯU Ý KHI LÀM BÁO CÁO (ADY201m)
Duplicate: Khi cào Multi-region (YouTube), một video như MV của BlackPink có thể Trending ở cả VN, US và KR.

Xử lý: Bạn phải dùng lệnh df.drop_duplicates(subset=['Video ID']) như trong code trên.

Báo cáo: Hãy ghi vào báo cáo là "Sau khi cào raw data, em thực hiện Data Cleaning để loại bỏ dữ liệu trùng lặp".

Thời gian chạy: Cào 10k dòng sẽ mất khoảng 5-10 phút chạy script. Hãy đảm bảo mạng ổn định.

Backup: Code trên nên chạy từng phần hoặc lưu file CSV liên tục (mode='a') nếu sợ máy bị crash giữa chừng.

nói thêm về API

Để hiểu sâu hơn về API (Application Programming Interface - Giao diện lập trình ứng dụng), đặc biệt trong bối cảnh bạn đang làm bài tập crawl dữ liệu (YouTube/Spotify), mình sẽ giải thích theo cách trực quan nhất từ lý thuyết đến thực tế nhé.

1. API là gì? (Ví dụ dễ hiểu nhất)
Hãy tưởng tượng bạn đang ở một Nhà hàng sang trọng.

Bạn (Client/User): Là người lập trình muốn lấy dữ liệu.

Nhà bếp (Server/Database): Là hệ thống máy chủ của YouTube/Spotify chứa hàng tỷ video và bài hát.

Người bồi bàn (API): Là cầu nối trung gian.

Quy trình:

Bạn không thể chạy thẳng vào nhà bếp để tự lục lọi tủ lạnh (Vì lý do bảo mật và lộn xộn).

Bạn gọi Người bồi bàn (API) và đưa ra yêu cầu (Request): "Cho tôi xem danh sách Top Trending".

Người bồi bàn mang yêu cầu đó vào bếp.

Nhà bếp chế biến và đưa món ăn cho bồi bàn.

Bồi bàn mang thức ăn (Dữ liệu - Response) ra cho bạn.

=> API chính là "người bồi bàn" giúp hai phần mềm khác nhau (Code Python của bạn và Server của Google) nói chuyện được với nhau.

2. Cơ chế hoạt động kỹ thuật (Request & Response)
Trong lập trình, quy trình "gọi món" diễn ra như sau:

A. Gửi yêu cầu (Request)
Bạn gửi một đường link (URL) đến máy chủ. Ví dụ với YouTube: GET https://www.googleapis.com/youtube/v3/videos?chart=mostPopular&key=YOUR_API_KEY

Trong đó có các thành phần quan trọng:

Endpoint (Điểm cuối): .../youtube/v3/videos. Đây là "địa chỉ cụ thể" trong nhà bếp. Bạn muốn lấy "Videos" chứ không phải "Channels" hay "Comments".

Method (Phương thức):

GET: Dùng để lấy dữ liệu (Crawl data dùng cái này 99%).

POST: Dùng để gửi dữ liệu mới lên (ví dụ: upload video).

DELETE: Xóa dữ liệu.

Parameters (Tham số): chart=mostPopular. Đây là "yêu cầu cụ thể" (Tôi muốn video thịnh hành, không phải video ngẫu nhiên).

API Key/Token: key=.... Đây là "thẻ thành viên" hoặc "vé vào cửa". Nếu không có chìa khóa này, API sẽ chặn bạn lại ngay lập tức.

B. Nhận phản hồi (Response)
Server sẽ trả về kết quả, thường là dưới dạng JSON (JavaScript Object Notation). Nó giống như một văn bản có cấu trúc cây thư mục.

Ví dụ JSON trả về:

JSON
{
  "kind": "youtube#videoListResponse",
  "items": [
    {
      "id": "Video_ID_123",
      "snippet": {
        "title": "Sơn Tùng M-TP - Video Mới",
        "views": 1000000
      }
    }
  ]
}
Code Python của bạn sẽ đọc file này (response['items'][0]['snippet']['title']) để lấy ra chữ "Sơn Tùng M-TP - Video Mới".

3. Tại sao Crawl Data lại cần API? (So với cào web thường)
Có hai cách để lấy dữ liệu:

Cào giao diện (Web Scraping - BeautifulSoup/Selenium): Giống như bạn chụp ảnh menu nhà hàng về rồi ngồi gõ lại. Nếu nhà hàng đổi thiết kế menu, bạn phải làm lại từ đầu. Rất dễ lỗi.

Dùng API (Official): Giống như nhà hàng gửi hẳn file Excel thực đơn cho bạn.

Ưu điểm: Dữ liệu sạch, cấu trúc rõ ràng, hợp pháp, ít bị chặn IP.

Nhược điểm: Bị giới hạn số lượng (Quota).

4. Các thuật ngữ "sống còn" khi làm việc với API
Khi bạn làm bài Assignment ADY201m, bạn sẽ gặp các thuật ngữ này liên tục:

Rate Limit (Giới hạn tốc độ): Ví dụ Spotify quy định "Chỉ được gọi 10 lần trong 1 giây". Nếu bạn gọi vòng lặp quá nhanh, bạn sẽ bị lỗi 429: Too Many Requests.

Cách xử lý: Dùng time.sleep(0.5) trong code Python để kìm hãm tốc độ lại.

Quota (Hạn ngạch): Ví dụ YouTube cho 10.000 điểm/ngày.

Lấy 1 list video tốn 1 điểm.

Search từ khóa tốn 100 điểm.

Cách xử lý: Tính toán kỹ trước khi chạy lệnh, nếu hết Quota thì phải chờ sang ngày hôm sau (theo giờ Mỹ) hoặc đổi API Key khác.

Authentication (Xác thực):

API Key: Đơn giản, dùng cho dữ liệu công khai (YouTube Data API dùng cái này).

OAuth 2.0: Phức tạp hơn, cần đăng nhập để lấy dữ liệu cá nhân (Ví dụ: Lấy danh sách bài hát bạn đã like trên Spotify). Code Spotify của bạn dùng Client Credentials là một dạng đơn giản của cái này.

5. Status Codes (Mã trạng thái) cần nhớ
Khi gọi API, bạn cần print cái status_code ra để biết tình hình:

200 (OK): Thành công, có dữ liệu.

400 (Bad Request): Bạn gửi sai cú pháp (ví dụ thiếu tham số bắt buộc).

401 (Unauthorized): API Key sai hoặc hết hạn.

403 (Forbidden): Bạn không có quyền truy cập hoặc Hết Quota (YouTube hay báo lỗi này khi hết tiền).

404 (Not Found): Endpoint sai (ví dụ gõ nhầm đường link).

429 (Too Many Requests): Gửi quá nhanh, cần nghỉ một chút.

500 (Internal Server Error): Lỗi của server Google/Spotify (ít gặp, nhưng nếu gặp thì do họ chứ không phải do bạn).

Tóm lại
Với bài tập của bạn:

YouTube Data API là cái kho video khổng lồ, chìa khóa là API Key, giới hạn là Quota.

Spotify Web API là kho nhạc, chìa khóa là Client ID/Secret, giới hạn là Rate Limit (tốc độ gửi).

Hiểu rõ cơ chế này giúp bạn debug nhanh hơn: Thấy lỗi 403 biết ngay là hết Quota, thấy lỗi 429 biết ngay là cần thêm time.sleep().

cách crawl 10k data từ youtube và spotify

Để cào được 10.000 (10k) dòng dữ liệu từ YouTube và Spotify với tài khoản miễn phí là một bài toán khó về mặt kỹ thuật (do giới hạn Quota và Rate Limit). Nếu chỉ cào đơn thuần (ví dụ: chỉ lấy Trending Việt Nam), bạn sẽ chỉ lấy được khoảng 50-100 dòng.

Dưới đây là Chiến lược "Quét diện rộng" và code Python tối ưu để đạt mục tiêu 10k data.

PHẦN 1: CHIẾN LƯỢC YOUTUBE (Multi-Region Scraper)
Vấn đề:

API search (tìm từ khóa) tốn 100 điểm quota/lần → Chỉ cào được tối đa 500 video là hết sạch quota trong ngày.

API videos().list (Trending) chỉ tốn 1 điểm/lần → Cào được hàng chục nghìn video.

Giải pháp: Duyệt qua danh sách mã quốc gia (Region Code) của khoảng 50-60 nước trên thế giới để lấy Top Trending của từng nước. (Ví dụ: 1 nước lấy 200 video × 50 nước = 10.000 video).

Code Python (YouTube)
Python
from googleapiclient.discovery import build
import pandas as pd
import isodate
import time

# --- CẤU HÌNH ---
API_KEY = 'YOUR_YOUTUBE_API_KEY' # Thay key của bạn vào đây
youtube = build('youtube', 'v3', developerKey=API_KEY)

# Danh sách mã quốc gia (ISO 3166-1 alpha-2) - Càng nhiều càng tốt
COUNTRY_CODES = [
    'VN', 'US', 'KR', 'JP', 'IN', 'GB', 'CA', 'DE', 'FR', 'BR', 
    'RU', 'MX', 'ID', 'TH', 'PH', 'ES', 'IT', 'AU', 'TW', 'MY',
    'SA', 'TR', 'PL', 'SE', 'AR', 'NL', 'CO', 'ZA', 'UA', 'EG',
    'SG', 'NZ', 'DK', 'FI', 'NO', 'IE', 'CH', 'PT', 'GR', 'HK'
]

def crawl_youtube_10k():
    all_videos = []
    video_ids_seen = set() # Dùng set để kiểm tra trùng lặp nhanh hơn

    print("--- BẮT ĐẦU CÀO YOUTUBE (MỤC TIÊU: 10K) ---")

    for country in COUNTRY_CODES:
        print(f"--> Đang lấy Trending tại: {country}...")
        
        next_page_token = None
        # Mỗi nước lấy tối đa 4 trang (khoảng 200 video)
        for _ in range(4): 
            try:
                request = youtube.videos().list(
                    part='snippet,statistics,contentDetails',
                    chart='mostPopular',
                    regionCode=country,
                    maxResults=50,
                    pageToken=next_page_token
                )
                response = request.execute()

                for item in response.get('items', []):
                    vid_id = item['id']
                    
                    # Nếu video này đã lấy ở nước khác rồi thì bỏ qua
                    if vid_id in video_ids_seen:
                        continue
                    
                    # Xử lý Duration (ISO 8601 -> Seconds)
                    dur_str = item['contentDetails'].get('duration', 'PT0S')
                    dur_sec = isodate.parse_duration(dur_str).total_seconds()

                    stats = item.get('statistics', {})
                    
                    video_data = {
                        'Video ID': vid_id,
                        'Title': item['snippet']['title'],
                        'Published At': item['snippet']['publishedAt'],
                        'Channel': item['snippet']['channelTitle'],
                        'View Count': int(stats.get('viewCount', 0)),
                        'Like Count': int(stats.get('likeCount', 0)),
                        'Comment Count': int(stats.get('commentCount', 0)),
                        'Duration (s)': dur_sec,
                        'Trending Region': country 
                    }
                    
                    all_videos.append(video_data)
                    video_ids_seen.add(vid_id)

                # Pagination: Kiểm tra xem còn trang sau không
                next_page_token = response.get('nextPageToken')
                if not next_page_token:
                    break # Hết danh sách của nước này

            except Exception as e:
                print(f"Lỗi tại {country}: {e}")
                break
        
        print(f"    Tổng hiện tại: {len(all_videos)} videos")
        
        # Nếu đủ 10k thì dừng ngay
        if len(all_videos) >= 10000:
            print("!!! ĐÃ ĐẠT MỐC 10.000 DATA !!!")
            break

    # Lưu file
    df = pd.DataFrame(all_videos)
    df.to_csv('youtube_10k_dataset.csv', index=False, encoding='utf-8-sig')
    print("Đã lưu file: youtube_10k_dataset.csv")

# Chạy hàm
crawl_youtube_10k()
PHẦN 2: CHIẾN LƯỢC SPOTIFY (Year-Loop Search)
Vấn đề: Spotify giới hạn mỗi lần search chỉ trả về tối đa 50 kết quả, và giới hạn độ sâu (offset) tối đa là 1000 kết quả cho một từ khóa. Bạn không thể search "music" và lấy 10.000 bài được.

Giải pháp: Chia nhỏ việc tìm kiếm theo Năm phát hành (Year). (Ví dụ: Quét từ năm 2014 đến 2024. Mỗi năm lấy 1.000 bài hát phổ biến nhất → 10 năm = 10.000 bài).

Code Python (Spotify)
Python
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd
import time

# --- CẤU HÌNH ---
CLIENT_ID = 'YOUR_SPOTIFY_CLIENT_ID'
CLIENT_SECRET = 'YOUR_SPOTIFY_CLIENT_SECRET'

auth_manager = SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
sp = spotipy.Spotify(auth_manager=auth_manager)

def crawl_spotify_10k():
    all_tracks = []
    track_ids_seen = set()

    # Quét dữ liệu 10 năm gần nhất (2015 - 2024)
    years = range(2015, 2025) 
    
    print("--- BẮT ĐẦU CÀO SPOTIFY (MỤC TIÊU: 10K) ---")

    for year in years:
        print(f"--> Đang quét nhạc năm: {year}...")
        
        # Mỗi năm lấy 1000 bài (Giới hạn offset của Spotify là 1000)
        # Bước nhảy 50 (limit tối đa mỗi request)
        for offset in range(0, 1000, 50):
            try:
                # Query: lấy track theo năm
                results = sp.search(q=f'year:{year}', type='track', limit=50, offset=offset)
                items = results['tracks']['items']
                
                if not items:
                    break

                for item in items:
                    t_id = item['id']
                    if t_id in track_ids_seen:
                        continue

                    track_data = {
                        'Track ID': t_id,
                        'Track Name': item['name'],
                        'Artist': item['artists'][0]['name'],
                        'Album': item['album']['name'],
                        'Release Date': item['album']['release_date'],
                        'Popularity': item['popularity'], # Chỉ số quan trọng thay thế View
                        'Duration (ms)': item['duration_ms'],
                        'Explicit': item['explicit']
                    }
                    all_tracks.append(track_data)
                    track_ids_seen.add(t_id)

                # QUAN TRỌNG: Nghỉ 0.5s để không bị Spotify chặn (Rate Limit)
                time.sleep(0.5)

            except Exception as e:
                print(f"Lỗi hoặc bị chặn (Rate Limit): {e}")
                time.sleep(5) # Nếu lỗi thì nghỉ 5s rồi thử tiếp
                continue
        
        print(f"    Tổng hiện tại: {len(all_tracks)} tracks")
        if len(all_tracks) >= 10000:
            break

    # Lưu file
    df = pd.DataFrame(all_tracks)
    df.to_csv('spotify_10k_dataset.csv', index=False, encoding='utf-8-sig')
    print("Đã lưu file: spotify_10k_dataset.csv")

# Chạy hàm
crawl_spotify_10k()
MỘT SỐ LƯU Ý KHI LÀM BÀI (Rất quan trọng)
Backup API Key: Với YouTube, khi chạy script trên, khả năng cao là gần cuối sẽ bị hết Quota (nếu bạn chạy đi chạy lại test nhiều lần). Hãy chuẩn bị sẵn 2-3 tài khoản Google Cloud khác nhau để thay thế API_KEY nếu bị lỗi 403 Quota Exceeded.

Thời gian chạy:

YouTube: Khá nhanh, khoảng 2-3 phút.

Spotify: Sẽ chậm hơn (khoảng 10-15 phút) do phải có lệnh time.sleep(0.5). Đừng xóa dòng này, nếu xóa bạn sẽ bị khóa IP tạm thời.

Lý giải trong báo cáo: Khi nộp bài, hãy giải thích rõ phương pháp lấy 10k data này: "Do giới hạn API, em đã sử dụng phương pháp Multi-region Scanning (đối với YouTube) và Historical Querying (đối với Spotify) để đảm bảo độ lớn và tính đa dạng của tập dữ liệu." -> Câu này sẽ được điểm cao.

phương pháp Multi-region Scanning (đối với YouTube) và Historical Querying (đối với Spotify) 

Đây là hai thuật ngữ kỹ thuật mô tả chiến lược thu thập dữ liệu (Data Collection Strategy) nhằm vượt qua các rào cản giới hạn của API miễn phí.

Dưới đây là phần giải thích chi tiết để bạn có thể hiểu sâu cơ chế và dùng nội dung này để viết vào báo cáo môn ADY201m (phần Methodology - Phương pháp thực hiện).

1. Multi-region Scanning (Quét đa vùng) - Dành cho YouTube
Tại sao cần phương pháp này?
Vấn đề: YouTube API có giới hạn Quota (hạn ngạch) rất gắt gao. Lệnh tìm kiếm từ khóa (search) tốn 100 điểm/lần, trong khi lệnh lấy danh sách thịnh hành (videos.list) chỉ tốn 1 điểm/lần. Tuy nhiên, danh sách thịnh hành của một quốc gia chỉ có khoảng 50-200 video.

Mục tiêu: Cần 10.000 video mà không được tốn quá nhiều Quota.

Cơ chế hoạt động
Thay vì cố gắng đào sâu vào dữ liệu của một quốc gia (điều không thể làm được vì hết danh sách), chúng ta sẽ quét bề mặt của nhiều quốc gia khác nhau.

Input: Một danh sách mã quốc gia chuẩn ISO (ví dụ: ['VN', 'US', 'JP', 'KR', 'GB', ...]).

Process: Thuật toán sẽ lặp qua từng mã quốc gia này, gửi yêu cầu đến API: "Cho tôi xem Top Trending hiện tại của Mỹ", sau đó là "Của Nhật", "Của Hàn Quốc"...

Aggregation (Gộp): Dữ liệu từ các nước được gộp chung vào một danh sách lớn.

Deduplication (Khử trùng): Vì một video nổi tiếng (như nhạc K-pop) có thể lọt Top Trending ở cả Hàn Quốc, Việt Nam và Mỹ, nên hệ thống cần lọc bỏ các Video ID trùng lặp để đảm bảo tính duy nhất.

Ưu điểm trong báo cáo
Tối ưu chi phí (Quota Efficiency): Lấy 10.000 video chỉ tốn khoảng 200-300 điểm Quota (rất rẻ so với 100.000 điểm nếu dùng search).

Tính đa dạng (Diversity): Bộ dữ liệu sẽ phản ánh xu hướng toàn cầu (Global Trend) thay vì chỉ cục bộ một khu vực.

2. Historical Querying (Truy vấn theo lịch sử) - Dành cho Spotify
Tại sao cần phương pháp này?
Vấn đề: Spotify Web API có giới hạn Deep Paging (Phân trang sâu). Khi bạn tìm kiếm (Search), API chỉ cho phép bạn xem tối đa 1.000 kết quả đầu tiên (offset = 1000). Bạn không thể cuộn xuống kết quả thứ 10.001 được.

Mục tiêu: Cần lấy số lượng lớn (10k) bài hát phổ biến mà không bị chặn bởi giới hạn 1.000 item.

Cơ chế hoạt động
Chúng ta "chia để trị" bằng cách cắt nhỏ không gian tìm kiếm theo thời gian (Năm phát hành). Thay vì tìm "Những bài hát hay nhất mọi thời đại" (API sẽ trả về hàng triệu bài nhưng chỉ cho xem 1.000 bài đầu), ta tìm từng lát cắt nhỏ.

Segmentation (Phân đoạn): Chia thời gian thành các năm: 2015, 2016, ..., 2024.

Iterative Querying (Truy vấn lặp):

Vòng lặp 1: Tìm q='year:2015', lấy 1.000 bài hát phổ biến nhất năm 2015.

Vòng lặp 2: Tìm q='year:2016', lấy 1.000 bài hát phổ biến nhất năm 2016.

... tiếp tục đến năm 2024.

Result: 10 năm x 1.000 bài/năm = 10.000 bài hát.

Ưu điểm trong báo cáo
Vượt rào cản kỹ thuật (Bypass Limitation): Khắc phục hoàn toàn giới hạn offset limit 1000 của Spotify.

Dữ liệu phong phú (Rich Dataset): Đảm bảo thu thập được cả những bài hát "Old but Gold" (cũ nhưng vẫn hot) lẫn những bài mới phát hành, tạo ra bức tranh toàn cảnh về thị hiếu âm nhạc qua các năm.

Bảng so sánh tóm tắt (Dùng cho slide thuyết trình)
Đặc điểm	Multi-region Scanning (YouTube)	Historical Querying (Spotify)
Đối tượng API	YouTube Data API v3	Spotify Web API
Rào cản chính	Quota (Hạn ngạch) sử dụng trong ngày	Offset Limit (Giới hạn hiển thị kết quả)
Chiến lược	Mở rộng theo Không gian (Địa lý)	Chia nhỏ theo Thời gian (Năm)
Tham số khóa	regionCode (ví dụ: 'VN', 'US')	q (query) với filter year:YYYY
Kết quả	Dataset đa văn hóa, xu hướng toàn cầu	Dataset đa thời đại, lịch sử âm nhạc
Rủi ro	Dữ liệu trùng lặp (cần lọc kỹ)	Tốc độ chậm (do phải sleep tránh lỗi 429)
Nếu giáo viên hỏi: "Tại sao em không dùng lệnh Search bình thường?" Bạn trả lời: "Thưa thầy/cô, lệnh Search của YouTube quá tốn kém tài nguyên (gấp 100 lần), còn lệnh Search của Spotify thì bị giới hạn số lượng kết quả trả về. Hai phương pháp trên là cách tối ưu nhất để sinh viên có thể xây dựng bộ dữ liệu lớn (Large Scale Dataset) mà không cần trả phí cho bản Enterprise."