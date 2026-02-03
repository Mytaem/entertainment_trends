import asyncio
import json
import re
import os
import random
from datetime import datetime, timezone, timedelta
from playwright.async_api import async_playwright

# ===================== CONFIG =====================
OUT_FILE = os.path.join(os.getcwd(), "tiktok_dataset_clean.json")
MAX_PER_HASHTAG = 80

hashtags = [
    "mrbeast", "runningman", "runningmanvietnamseason3", "quangtrung", "tamlongcuulong",
    "pepsi", "vansunhuy", "wag", "luongthethanh", "daihoidang", "mucthanky",
    "theroseconcert", "mck", "binz", "jsol", "thenextliveconcert", "dangcongsanvietnam",
    "minecraftbuilding", "giadinhhaha", "tiengyeunayanhdichduockhong", "ninhanhbui",
    "vucattuong", "nguyentungduong", "dopamine", "neji", "daihoixiv", "18",
    "hwanginyeop", "chunhat", "huongtram", "cuoi", "hanbin", "teamwork",
    "lienbinhphat", "genfestmbillion", "nba", "hanbin_tempest", "exitsign",
    "tanmuc", "papagocouple", "vu", "2026newyeareffecttutorial", "u23china",
    "genfest2026", "dreaminaisnextgeneditor", "mangtetvenha", "genfest2025",
    "chunhatvuive", "meandthee", "phapsugangter", "vnleague2025", "runningmanmua3",
    "haanhtuanconcert", "hagl", "hoangduyen", "protectcortis", "hsxs",
    "genfestpresentmbillion", "liveconcert", "lygiasam_lijiasen_lijiasen", "camlai",
    "dola", "bauduc", "justatee", "wanghedi", "vittihon", "bocongan",
    "xuhuong", "trending", "fyp", "viral", "nhachay", "giaitri", "tinnhanh",
    "reviewanngon", "thuthuat", "congnghe", "學習", "vpop", "kpop", "dance",
    "funny", "meme", "pets", "food", "travel", "beauty", "fashion", "fitness",
    "motivation", "education", "art", "photography", "vlog", "storytime",
    "lifehacks", "diy", "tutorial", "gaming", "asmr", "music"
]

# ===================== HELPERS =====================
def parse_video_id(url: str):
    m = re.search(r'/video/(\d+)', url)
    return m.group(1) if m else None

def decode_timestamp_from_id(video_id: str):
    try:
        ts = int(video_id) >> 32
        now = int(datetime.now(timezone.utc).timestamp())
        if 1500000000 <= ts <= now + 86400 * 365 * 5:
            return datetime.fromtimestamp(ts, tz=timezone.utc)
    except:
        pass
    return None

def clean_caption(text: str):
    if not text:
        return ""
    text = re.sub(r'\s*[\d\.,KM]+\s*(Likes|Lượt thích|Comments|Bình luận).*', '', text, flags=re.I)
    text = re.sub(r'^Video TikTok từ\s+@\w+.*?:', '', text, flags=re.I)
    return text.strip(' "\n')

def to_number(s: str) -> float:
    if not s:
        return 0.0
    s = s.upper().replace(',', '')
    if 'K' in s:
        return float(s.replace('K', '')) * 1_000
    if 'M' in s:
        return float(s.replace('M', '')) * 1_000_000
    try:
        return float(s)
    except:
        return 0.0

def extract_metric(pattern, text):
    m = re.search(pattern, text, re.I)
    return m.group(1).replace(',', '') if m else "0"

def is_clickbait(caption: str) -> int:
    if not caption:
        return 0
    caption = caption.lower()
    keywords = [
        "sốc", "shock", "bí mật", "không tin nổi", "bóc phốt",
        "drama", "bí kíp", "hack", "secret", "exposed",
        "you won't believe", "crazy", "insane"
    ]
    if caption.count('!') >= 3 or caption.count('?') >= 2:
        return 1
    return int(any(k in caption for k in keywords))

def is_trending(likes, comments, views, shares, pub_dt, scrape_dt):
    er = (likes + comments + shares) / views if views > 0 else 0
    recent = False
    if pub_dt:
        recent = (scrape_dt - pub_dt).days <= 3

    return int(
        (views >= 100_000 and er >= 0.05) or
        (likes >= 10_000 and comments >= 500 and shares >= 1_500) or
        (recent and likes >= 10_000) or
        (views >= 100_000 and likes >= 10_000)
    )

# ===================== SCRAPER =====================
async def scrape_video(context, url, hashtag, scrape_time):
    page = await context.new_page()
    try:
        await page.goto(url, timeout=60000, wait_until="networkidle")
        await page.wait_for_timeout(random.randint(4000, 7000))

        meta = await page.get_attribute('meta[name="description"]', 'content') or ""

        caption = clean_caption(meta)

        likes_raw = extract_metric(r'([\d\.,]+[KM]?)\s*(Likes|Lượt thích)', meta)
        comments_raw = extract_metric(r'([\d\.,]+[KM]?)\s*(Comments|Bình luận)', meta)
        views_raw = extract_metric(r'([\d\.,]+[KM]?)\s*(Views|Lượt xem)', meta)
        shares_raw = extract_metric(r'([\d\.,]+[KM]?)\s*(Shares|Chia sẻ)', meta)

        likes = to_number(likes_raw)
        comments = to_number(comments_raw)
        views = to_number(views_raw)
        shares = to_number(shares_raw)

        video_id = parse_video_id(url)
        pub_dt = decode_timestamp_from_id(video_id)

        video_age_hours = (
            (scrape_time - pub_dt).total_seconds() / 3600
            if pub_dt else None
        )

        engagement_rate = (
            (likes + comments + shares) / views
            if views > 0 else 0
        )

        return {
            "hashtag": hashtag,
            "url": url,
            "caption": caption,

            "likes": likes,
            "comments": comments,
            "views": views,
            "shares": shares,

            "likes_raw": likes_raw,
            "comments_raw": comments_raw,
            "views_raw": views_raw,
            "shares_raw": shares_raw,

            "engagement_rate": round(engagement_rate, 6),
            "video_age_hours": round(video_age_hours, 2) if video_age_hours else None,

            "has_clickbait": is_clickbait(caption),
            "is_trending": is_trending(
                likes, comments, views, shares, pub_dt, scrape_time
            ),

            "publish_time": pub_dt.isoformat() if pub_dt else None,
            "scrape_time": scrape_time.isoformat()
        }

    except Exception as e:
        print(f"Lỗi video {url[-15:]}: {e}")
        return None
    finally:
        await page.close()

# ===================== MAIN =====================
async def main():
    results = []
    seen = set()

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context(
            locale="vi-VN",
            timezone_id="Asia/Ho_Chi_Minh"
        )

        for tag in hashtags:
            print(f"\n### #{tag}")
            page = await context.new_page()
            await page.goto(f"https://www.tiktok.com/search/video?q=%23{tag}", timeout=90000)
            await page.wait_for_timeout(6000)

            for _ in range(20):
                await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
                await page.wait_for_timeout(random.randint(2000, 4000))

            links = await page.query_selector_all('a[href*="/video/"]')
            urls = []
            for a in links:
                href = await a.get_attribute("href")
                if href and "/video/" in href:
                    full = "https://www.tiktok.com" + href if href.startswith('/') else href
                    if full not in seen:
                        seen.add(full)
                        urls.append(full)
                if len(urls) >= MAX_PER_HASHTAG:
                    break

            scrape_time = datetime.now(timezone.utc)

            for url in urls:
                data = await scrape_video(context, url, tag, scrape_time)
                if data:
                    results.append(data)

                with open(OUT_FILE, "w", encoding="utf-8") as f:
                    json.dump(results, f, ensure_ascii=False, indent=2)

            await page.close()

        await browser.close()

    print(f"\n✅ DONE: {len(results)} videos → {OUT_FILE}")

if __name__ == "__main__":
    asyncio.run(main())
