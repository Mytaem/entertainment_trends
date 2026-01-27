from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import pandas as pd
import time
from tqdm import tqdm
from dotenv import load_dotenv
import os
from datetime import datetime

load_dotenv(override=True)
API_KEY = os.getenv("YOUTUBE_API_KEY")

if not API_KEY:
    print("Không tìm thấy YOUTUBE_API_KEY trong .env! Kiểm tra lại file.")
    raise SystemExit(1)

youtube = build("youtube", "v3", developerKey=API_KEY)

countries = ["VN","US","KR","JP","IN","BR","ID","MX","DE","FR","GB","CA","AU","TH","PH","MY","SG","TW","ES","IT"]

CATEGORY_MAP = {
    "10": "Music",
    "23": "Comedy",
    "24": "Entertainment",
    "20": "Gaming",
    "22": "People&Blogs",
    "25": "News&Politics",
    "26": "Howto&Style",
    "27": "Education",
    "28": "Science&Tech",
    "1":  "Film&Animation",
}

categories = list(CATEGORY_MAP.keys())

TARGET_TOTAL = 10000
PER_CATEGORY_TARGET = TARGET_TOTAL // len(categories)   
PER_COUNTRY_CAP = 1200                                 
MAX_PER_REQUEST = 50
MAX_PAGES_PER_CAT = 5                                  
SLEEP_SEC = 0.15

os.makedirs("data/youtube", exist_ok=True)

def fetch_most_popular(region_code: str, category_id: str, pages: int = 1):
    rows = []
    page_token = None

    for _ in range(pages):
        req = youtube.videos().list(
            part="id,snippet,statistics,contentDetails",
            chart="mostPopular",
            regionCode=region_code,
            videoCategoryId=category_id,
            maxResults=MAX_PER_REQUEST,
            pageToken=page_token
        )
        res = req.execute()

        for item in res.get("items", []):
            sn = item.get("snippet", {}) or {}
            st = item.get("statistics", {}) or {}
            cd = item.get("contentDetails", {}) or {}

            rows.append({
                "video_id": item.get("id"),
                "title": sn.get("title"),
                "publish_time": sn.get("publishedAt"),
                "channel_title": sn.get("channelTitle"),
                "category_id": sn.get("categoryId", category_id),
                "category_name": CATEGORY_MAP.get(category_id, "Unknown"),
                "country": region_code,
                "duration": cd.get("duration"),
                "views": int(st.get("viewCount", 0) or 0),
                "likes": int(st.get("likeCount", 0) or 0),
                "comments": int(st.get("commentCount", 0) or 0),
            })

        page_token = res.get("nextPageToken")
        if not page_token:
            break

        time.sleep(SLEEP_SEC)

    return rows

all_rows = []
print("Bắt đầu thu thập trending videos...")

total_calls = len(countries) * len(categories)
pbar = tqdm(total=total_calls, desc="Country x Category", ncols=100)

for country in countries:
    country_rows = []
    for cat in categories:
        try:
            rows = fetch_most_popular(country, cat, pages=MAX_PAGES_PER_CAT)
            country_rows.extend(rows)
        except HttpError as e:
            print(f"\nLỗi tại {country} - category {cat}: {e}")
        except Exception as e:
            print(f"\nLỗi tại {country} - category {cat}: {e}")
        finally:
            pbar.update(1)

    if country_rows:
        df_country = pd.DataFrame(country_rows)
        df_country = df_country.sort_values(["video_id", "views"], ascending=[True, False]) \
                               .drop_duplicates(subset=["video_id"], keep="first")
        if len(df_country) > PER_COUNTRY_CAP:
            df_country = df_country.sample(PER_COUNTRY_CAP, random_state=42)
        all_rows.extend(df_country.to_dict("records"))

pbar.close()

df = pd.DataFrame(all_rows)

if df.empty:
    print("Không có dữ liệu. Kiểm tra API key / quota / YouTube Data API v3.")
    raise SystemExit(1)

df["publish_time"] = pd.to_datetime(df["publish_time"], errors="coerce", utc=True)
df = df.sort_values(["video_id", "views"], ascending=[True, False]).drop_duplicates(subset=["video_id"], keep="first")

# CÂN BẰNG CATEGORY
counts = df["category_name"].value_counts()
min_take = min(PER_CATEGORY_TARGET, counts.min() if len(counts) else 0)

balanced_parts = []
for cat_name in sorted(df["category_name"].dropna().unique()):
    dcat = df[df["category_name"] == cat_name]
    take_n = min(min_take, len(dcat))
    balanced_parts.append(dcat.sample(take_n, random_state=42))

df_balanced = pd.concat(balanced_parts, ignore_index=True)


if len(df_balanced) < TARGET_TOTAL:
    remaining = TARGET_TOTAL - len(df_balanced)
    df_extra = df[~df["video_id"].isin(df_balanced["video_id"])].copy()
    df_extra["engagement"] = df_extra["likes"] + df_extra["comments"]
    df_extra = df_extra.sort_values(["engagement", "views"], ascending=False)
    df_balanced = pd.concat([df_balanced, df_extra.head(remaining)], ignore_index=True)

df_balanced = df_balanced.sort_values(["country", "category_name", "views"], ascending=[True, True, False])

ts = datetime.now().strftime("%Y%m%d_%H%M%S")
out_path = f"data/youtube/youtube_trending_balanced_{ts}.csv"
df_balanced.to_csv(out_path, index=False, encoding="utf-8-sig")

print(f"Thu thập tổng (raw dedupe): {len(df)}")
print(f"Dataset cân bằng xuất ra: {len(df_balanced)}")
print(f"File lưu tại: {out_path}")
print(df_balanced["category_name"].value_counts().to_string())
