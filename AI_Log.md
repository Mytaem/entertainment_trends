Mình cần cài những thư viện gì để crawl được YouTube và Spotify? Mình cũng muốn dùng pandas để xử lý dữ liệu. Hãy viết file requirements.txt giúp mình.
Để làm việc với YouTube API, Spotify Web API và xử lý dữ liệu, bạn cần các thư viện sau. Hãy copy nội dung này vào file requirements.txt:

Plaintext

# Data Manipulation
pandas==2.1.0
numpy==1.26.0

# API Clients
google-api-python-client==2.100.0  # Cho YouTube
spotipy==2.23.0                    # Cho Spotify

# Utilities
python-dotenv==1.0.0               # Để đọc file .env (giấu API Key)
tqdm==4.66.1                       # Thanh hiển thị tiến độ (Loading bar)
requests==2.31.0                   # Gọi HTTP request cơ bản
isodate==0.6.1                     # Xử lý format thời gian của YouTube (PT5M20S)

# Database Connector
psycopg2-binary==2.9.9             # Kết nối PostgreSQL
sqlalchemy==2.0.21
Sau đó chạy lệnh cài đặt:

Bash

pip install -r requirements.txt
Mình đã có API Key của Google Cloud Console. Bây giờ làm sao để lấy danh sách các video đang thịnh hành (Trending) tại Việt Nam? Viết cho mình đoạn code Python hoàn chỉnh để test thử.
AI Answer: Dưới đây là đoạn script Python sử dụng thư viện googleapiclient để lấy 50 video trending nhất tại Việt Nam.

Lưu ý: YouTube trả về duration dạng ISO 8601 (ví dụ PT5M), mình đã thêm hàm isodate để đổi sang giây cho bạn dễ tính toán.

File: src/test_youtube.py

Python

import os
from googleapiclient.discovery import build
import isodate
import pandas as pd

# Cấu hình
API_KEY = 'YOUR_GOOGLE_API_KEY_HERE'  # Thay key của bạn vào đây
YOUTUBE_API_SERVICE_NAME = 'youtube'
YOUTUBE_API_VERSION = 'v3'

def get_trending_videos():
    youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=API_KEY)

    # Gọi API lấy danh sách video
    request = youtube.videos().list(
        part="snippet,contentDetails,statistics",
        chart="mostPopular",
        regionCode="VN",
        maxResults=50
    )
    response = request.execute()

    video_list = []
    for item in response['items']:
        # Xử lý từng video
        try:
            video_id = item['id']
            title = item['snippet']['title']
            published_at = item['snippet']['publishedAt']
            channel_title = item['snippet']['channelTitle']
            
            # Xử lý thời lượng (Duration)
            duration_iso = item['contentDetails']['duration']
            duration_seconds = isodate.parse_duration(duration_iso).total_seconds()

            # Lấy thống kê view/like
            stats = item['statistics']
            view_count = stats.get('viewCount', 0)
            like_count = stats.get('likeCount', 0)
            comment_count = stats.get('commentCount', 0)

            video_list.append({
                'video_id': video_id,
                'title': title,
                'channel': channel_title,
                'published_at': published_at,
                'duration_sec': duration_seconds,
                'views': int(view_count),
                'likes': int(like_count),
                'comments': int(comment_count)
            })
        except Exception as e:
            print(f"Error parsing video {item['id']}: {e}")

    return pd.DataFrame(video_list)

if __name__ == "__main__":
    df = get_trending_videos()
    print(df.head())
    df.to_csv("data/raw/youtube_trending_vn.csv", index=False)
    print("Saved to data/raw/youtube_trending_vn.csv")
    lỗi: googleapiclient.errors.HttpError: <HttpError 403 when requesting ... "The request cannot be completed because you have exceeded your <a href="/youtube/v3/getting-started#quota">quota</a>.">. Làm sao để khắc phục? Mình cần crawl 10.000 dòng.
    AI Answer: Lỗi 403 "Quota Exceeded" nghĩa là bạn đã dùng hết hạn ngạch miễn phí (10.000 units/ngày) của Google.

Giải thích Cost:

Hàm videos().list tốn 1 unit mỗi lần gọi.

Hàm search().list tốn 100 units mỗi lần gọi (Rất đắt!).

Chiến lược để crawl 10.000 dòng:

Dùng nhiều API Key: Bạn cần tạo thêm 3-4 Project khác nhau trên Google Cloud Console để lấy thêm Key.

Tối ưu Code: Chỉ dùng videos().list (chart=mostPopular) kết hợp với loop qua các regionCode khác nhau (US, JP, KR, VN, UK...) thay vì dùng search().

Code xoay vòng Key (Key Rotation):

Dưới đây là hàm để tự động đổi Key khi bị lỗi:

Python

API_KEYS = ["KEY_1", "KEY_2", "KEY_3"]
current_key_index = 0

def get_service():
    global current_key_index
    try:
        return build('youtube', 'v3', developerKey=API_KEYS[current_key_index])
    except:
        print("Key lỗi, đang đổi key khác...")
        current_key_index += 1
        if current_key_index >= len(API_KEYS):
            raise Exception("Hết sạch Key rồi!")
        return get_service()
làm sao để lấy Client ID và Secret của Spotify?
AI Answer: Đúng rồi, Spotify dùng giao thức OAuth2 (Client Credentials Flow).

Vào Spotify Developer Dashboard.

Tạo App mới -> Lấy Client ID và Client Secret.

Đây là code kết nối dùng thư viện spotipy:

Python

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd

# Setup xác thực
auth_manager = SpotifyClientCredentials(
    client_id='YOUR_SPOTIFY_CLIENT_ID',
    client_secret='YOUR_SPOTIFY_CLIENT_SECRET'
)
sp = spotipy.Spotify(auth_manager=auth_manager)

def get_playlist_tracks(playlist_id):
    results = sp.playlist_tracks(playlist_id)
    tracks = results['items']
    
    # Spotify phân trang (Pagination) nếu playlist dài
    while results['next']:
        results = sp.next(results)
        tracks.extend(results['items'])
        
    data = []
    for item in tracks:
        track = item['track']
        if not track: continue
        
        data.append({
            'name': track['name'],
            'artist': track['artists'][0]['name'],
            'popularity': track['popularity'],
            'duration_ms': track['duration_ms'],
            'album_date': track['album']['release_date']
        })
    return pd.DataFrame(data)

# ID của Playlist 'Top 50 - Global' là: 37i9dQZEVXbMDoHDwVN2tF
df_spotify = get_playlist_tracks('37i9dQZEVXbMDoHDwVN2tF')
print(df_spotify.head())
lỗi 429 Too Many Requests.
AI Answer:Lỗi 429 là do bạn gửi request quá dồn dập. Spotify có giới hạn tốc độ.Cách fix: Bạn cần thêm hàm time.sleep() để nghỉ giữa các lần gọi.Cập nhật lại vòng lặp như sau:Pythonimport time
import random

playlist_ids = ['id1', 'id2', 'id3', ...] # Danh sách 100 ID

all_data = []
for pid in playlist_ids:
    print(f"Scraping playlist {pid}...")
    try:
        df = get_playlist_tracks(pid)
        all_data.append(df)
        
        # NGỦ NGẪU NHIÊN TỪ 1 ĐẾN 3 GIÂY
        sleep_time = random.uniform(1, 3)
        time.sleep(sleep_time) 
        
    except Exception as e:
        print(f"Lỗi khi lấy {pid}: {e}")

Mình cần đặt giả thuyết $H_0$ và $H_1$ để phân tích mối quan hệ giữa "Duration" (độ dài) và "Popularity" (độ phổ biến). Ý mình là muốn xem bài hát ngắn có trend hơn bài dài không.
AI Answer:Tuyệt vời, đây là một chủ đề phân tích rất hay cho ADY201m. Chúng ta sẽ dùng kiểm định tương quan Pearson hoặc Spearman.Thiết lập giả thuyết:$H_0$ (Null Hypothesis): Không có mối tương quan tuyến tính giữa độ dài bài hát (duration_ms) và độ phổ biến (popularity). (Hệ số tương quan $r = 0$).$H_1$ (Alternative Hypothesis): Có mối tương quan khác 0 giữa độ dài bài hát và độ phổ biến.Code thực hiện kiểm định:Pythonfrom scipy import stats

duration = df['duration_ms']
popularity = df['popularity']

# Tính hệ số tương quan Pearson
corr, p_value = stats.pearsonr(duration, popularity)

print(f"Hệ số tương quan Pearson: {corr}")
print(f"P-value: {p_value}")

if p_value < 0.05:
    print("Bác bỏ H0 -> Có mối liên hệ đáng kể giữa độ dài và độ hot.")
else:
    print("Chưa đủ bằng chứng bác bỏ H0 -> Độ dài không ảnh hưởng nhiều đến độ hot.")