import asyncio
import json
import re
import os
import random
from datetime import datetime, timezone, timedelta
from playwright.async_api import async_playwright, TimeoutError as PlaywrightTimeoutError

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

OUT_FILE = os.path.join(os.getcwd(), "tiktok_dataset_clean.json")

def parse_video_id(url: str) -> str:
    m = re.search(r'/video/(\d+)', url)
    return m.group(1) if m else None

def decode_timestamp_from_id(video_id: str) -> str:
    try:
        vid = int(video_id)
        ts = vid >> 32
        now_ts = int(datetime.now(timezone.utc).timestamp())
        if 1500000000 <= ts <= now_ts + 86400 * 365 * 5:
            dt = datetime.fromtimestamp(ts, tz=timezone.utc)
            return dt.isoformat(timespec='seconds').replace('+00:00', '')
    except:
        pass
    return "N/A"

def clean_caption(text: str) -> str:
    # Loại bỏ phần stats, nguồn, dấu ngoặc kép thừa
    text = re.sub(r'\s*[\d\.,KM]+\s*(?:Likes|Lượt thích|Bình luận|Comments)[,\s]*', '', text, flags=re.I)
    text = re.sub(r'Video TikTok từ\s+@\w+\s*\([^)]*\)\s*:\s*', '', text, flags=re.I)
    text = re.sub(r'^["“”\s]+|["“”\s]+$', '', text.strip())
    return text.strip()

def extract_likes_comments(meta: str):
    # Ưu tiên tìm cặp đôi
    pair = re.search(
        r'([\d\.,]+[KM]?)\s*(?:Likes|Lượt thích).*?([\d\.,]+[KM]?)\s*(?:Comments|Bình luận)',
        meta, re.I | re.DOTALL | re.UNICODE
    )
    if pair:
        return pair.group(1).replace(',', ''), pair.group(2).replace(',', '')

    # Fallback riêng
    likes_m = re.search(r'([\d\.,]+[KM]?)\s*(?:Likes|Lượt thích)', meta, re.I | re.UNICODE)
    comm_m = re.search(r'([\d\.,]+[KM]?)\s*(?:Comments|Bình luận)', meta, re.I | re.UNICODE)

    likes = likes_m.group(1).replace(',', '') if likes_m else "0"
    comms = comm_m.group(1).replace(',', '') if comm_m else "0"
    return likes, comms

def is_clickbait(caption: str) -> int:
    lower = caption.lower()
    if lower.count('!') >= 3 or lower.count('?') >= 2:
        return 1
    words = ["bí mật", "shock", "sốc", "không tin nổi", "bất ngờ", "bạn sẽ", "đừng bỏ lỡ"]
    return 1 if any(w in lower for w in words) else 0

def is_trending(caption: str, likes_str: str) -> int:
    lower = caption.lower()
    if any(w in lower for w in ["trending", "xuhuong", "viral", "fyp"]):
        return 1
    try:
        val = re.sub(r'[KM]', lambda m: '000' if m.group() == 'K' else '000000', likes_str.upper())
        return 1 if float(val) >= 50000 else 0
    except:
        return 0

async def get_relative_time_fallback(page):
    for sel in [
        'span[data-e2e="browser-nickname"] span:last-child',
        'div[data-e2e="video-author-desc"] span',
        'time',
        'span[class*="Time" i]',
    ]:
        try:
            el = await page.query_selector(sel)
            if el:
                txt = (await el.inner_text()).strip()
                if txt and ("ago" in txt.lower() or re.search(r'\d{1,2}[-/]\d{1,2}', txt)):
                    return txt
        except:
            pass
    return "N/A"

async def scrape_video_detail(context, url, hashtag, scrape_time: datetime):
    page = await context.new_page()
    try:
        await page.goto(url, timeout=60000, wait_until="networkidle")
        await page.wait_for_timeout(random.randint(4000, 8000))

        try:
            await page.wait_for_selector('div[data-e2e="video-desc"]', timeout=15000)
        except:
            pass

        meta = await page.get_attribute('meta[name="description"]', 'content') or ""

        caption = clean_caption(meta)
        likes, comments = extract_likes_comments(meta)

        vid_id = parse_video_id(url)
        pub_time = decode_timestamp_from_id(vid_id) if vid_id else "N/A"

        if pub_time == "N/A":
            rel = await get_relative_time_fallback(page)
            if rel != "N/A":
                pub_time = estimate_from_relative(rel, scrape_time)  # hàm estimate bạn có thể copy từ trước

        return {
            "hashtag": hashtag,
            "caption": caption,
            "publish_time": pub_time,
            "likes": likes,
            "comments": comments,
            "is_trending": is_trending(caption, likes),
            "has_clickbait": is_clickbait(caption)
        }

    except Exception as e:
        print(f"  Lỗi {url.split('/')[-1]}: {str(e)[:80]}...")
        return None
    finally:
        await page.close()

async def main():
    final_data = []
    seen = set()
    MAX_PER_TAG = 100

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)  # False để bạn quan sát
        context = await browser.new_context(
            viewport={"width": 1280, "height": 900},
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36",
            locale="vi-VN",
            timezone_id="Asia/Ho_Chi_Minh"
        )

        for tag in hashtags:
            print(f"\n══════ #{tag} ══════")
            page = await context.new_page()
            try:
                await page.goto(f"https://www.tiktok.com/search/video?q=%23{tag}", timeout=90000)
                await page.wait_for_timeout(7000)

                print("Cuộn trang...")
                prev_h = 0
                for i in range(50):
                    h = await page.evaluate("document.body.scrollHeight")
                    if h == prev_h and i > 12:
                        print(f"  Dừng cuộn (không còn nội dung mới)")
                        break
                    prev_h = h
                    await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
                    await page.wait_for_timeout(random.randint(2500, 5500))
                    if i % 8 == 0:
                        print(f"  Cuộn {i+1}...")

                # Các selector fallback để lấy link video
                selectors = [
                    'div[data-e2e="search_video-item"] a',
                    'a[href*="/video/"]',
                    'div[data-e2e="search-common-link"] a',
                    'div[class*="DivItemContainer"] a[href*="/video/"]',
                ]

                urls = []
                for sel in selectors:
                    els = await page.query_selector_all(sel)
                    for el in els:
                        href = await el.get_attribute("href")
                        if href and "/video/" in href and len(href.split('/')) > 4:  # tránh link rác
                            full = "https://www.tiktok.com" + href if href.startswith('/') else href
                            if full not in seen:
                                urls.append(full)
                                seen.add(full)
                                if len(urls) >= MAX_PER_TAG:
                                    break
                    if len(urls) >= MAX_PER_TAG:
                        break

                urls = list(dict.fromkeys(urls))[:MAX_PER_TAG]
                print(f"→ Tìm thấy {len(urls)} link video hợp lệ")

                now = datetime.now()
                for idx, u in enumerate(urls, 1):
                    print(f"  {idx}/{len(urls)} → {u.split('/')[-1]}")
                    item = await scrape_video_detail(context, u, tag, now)
                    if item:
                        final_data.append(item)
                    if idx % 5 == 0 or idx == len(urls):
                        with open(OUT_FILE, "w", encoding="utf-8") as f:
                            json.dump(final_data, f, ensure_ascii=False, indent=2)

                print(f"Hoàn thành #{tag} → tổng {len(final_data)}")

            except Exception as e:
                print(f"Lỗi #{tag}: {str(e)[:120]}...")
            finally:
                await page.close()

        await browser.close()

    print(f"\nHoàn tất! {len(final_data)} bản ghi → {OUT_FILE}")

if __name__ == "__main__":
    asyncio.run(main())