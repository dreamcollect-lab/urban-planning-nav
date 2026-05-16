import time
import pandas as pd
import requests

from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse


INPUT_CSV = "tokyo_23ku_master_auto.csv"
OUTPUT_CSV = "official_site_links.csv"

MAX_DEPTH = 3
MAX_PAGES_PER_MUNICIPALITY = 20
SLEEP_SECONDS = 0.5

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 "
        "(Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 "
        "(KHTML, like Gecko) "
        "Chrome/124.0 Safari/537.36"
    )
}


CATEGORY_KEYWORDS = {
    "road": [
        "doro", "douro", "road", "shitei", "kasen",
        "道路", "指定道路", "道路台帳", "建築基準法道路",
        "道路種別", "幅員", "私道", "認定道路",
    ],
    "district_plan": [
        "toshikeikaku", "machizukuri", "keikaku", "toshi",
        "都市計画", "地区計画", "用途地域", "景観", "まちづくり",
    ],
    "building_guidance": [
        "kenchiku", "kijunho", "shido",
        "建築", "建築指導", "建築確認", "建築課", "建築基準法",
    ],
    "hazard": [
        "bosai", "hazard",
        "防災", "ハザード", "洪水", "浸水", "土砂",
    ],
}


CRAWL_HINTS = [
    "doro", "douro", "road", "toshi", "toshikeikaku",
    "machizukuri", "keikaku", "kenchiku", "bosai", "kankyo",
    "道路", "建築", "都市計画", "まちづくり", "地区計画", "防災", "環境",
]


EXCLUDE_WORDS = [
    "news", "event", "calendar", "twitter", "facebook", "instagram",
    "youtube", "rss", "line", "mail", "faq", "koho", "movie", "video",
    "採用", "広報", "イベント", "ニュース",
]


def is_same_domain(base_url: str, target_url: str) -> bool:
    return urlparse(base_url).netloc == urlparse(target_url).netloc


def should_exclude(url: str, title: str) -> bool:
    text = f"{url} {title}".lower()
    return any(word.lower() in text for word in EXCLUDE_WORDS)


def decode_html(response: requests.Response) -> str:
    content = response.content

    for enc in ["utf-8", "cp932", "shift_jis", "euc_jp"]:
        try:
            return content.decode(enc)
        except UnicodeDecodeError:
            continue

    response.encoding = response.apparent_encoding
    return response.text


def fetch_links(page_url: str, base_url: str) -> list[dict]:
    try:
        response = requests.get(
            page_url,
            headers=HEADERS,
            timeout=20
        )
        response.raise_for_status()
        html_text = decode_html(response)

    except Exception as e:
        return [{
            "title": "",
            "url": page_url,
            "error": f"request_error: {e}"
        }]

    try:
        soup = BeautifulSoup(html_text, "lxml")
    except Exception as e:
        return [{
            "title": "",
            "url": page_url,
            "error": f"parse_error: {e}"
        }]

    links = []

    for a in soup.find_all("a"):
        try:
            href = a.get("href")
            title = a.get_text(" ", strip=True)

            if not href:
                continue

            full_url = urljoin(page_url, href)

            if not is_same_domain(base_url, full_url):
                continue

            if should_exclude(full_url, title):
                continue

            links.append({
                "title": title,
                "url": full_url,
                "error": ""
            })

        except Exception as e:
            links.append({
                "title": "",
                "url": page_url,
                "error": f"link_error: {e}"
            })

    return links


def detect_categories(title: str, url: str) -> list[str]:
    text = f"{title} {url}".lower()
    detected = []

    for category, keywords in CATEGORY_KEYWORDS.items():
        if any(keyword.lower() in text for keyword in keywords):
            detected.append(category)

    return detected


def is_crawl_candidate(title: str, url: str) -> bool:
    text = f"{title} {url}".lower()
    return any(hint.lower() in text for hint in CRAWL_HINTS)


def crawl_municipality(municipality: str, official_url: str) -> list[dict]:
    rows = []

    queue = [{
        "title": "公式トップ",
        "url": official_url,
        "depth": 1
    }]

    visited = set()
    crawled_count = 0

    while queue:
        current = queue.pop(0)

        current_url = current["url"]
        current_title = current["title"]
        current_depth = current["depth"]

        if current_url in visited:
            continue

        if current_depth > MAX_DEPTH:
            continue

        if crawled_count >= MAX_PAGES_PER_MUNICIPALITY:
            break

        visited.add(current_url)
        crawled_count += 1

        print(f"depth={current_depth}: {current_title}")

        links = fetch_links(
            page_url=current_url,
            base_url=official_url
        )

        for link in links:
            title = link.get("title", "")
            url = link.get("url", "")
            error = link.get("error", "")

            categories = detect_categories(title, url)

            for category in categories:
                rows.append({
                    "base_municipality": municipality,
                    "detected_category": category,
                    "depth": current_depth,
                    "title": title,
                    "url": url,
                    "source_page_title": current_title,
                    "source_page_url": current_url,
                    "error": error,
                })

            if current_depth < MAX_DEPTH:
                if is_crawl_candidate(title, url):
                    if url not in visited:
                        queue.append({
                            "title": title,
                            "url": url,
                            "depth": current_depth + 1
                        })

        time.sleep(SLEEP_SECONDS)

    return rows


def main():
    df = pd.read_csv(INPUT_CSV)

    official_df = df[
        (df["category"] == "official") &
        (df["target_url"].notna()) &
        (df["target_url"].astype(str).str.strip() != "")
    ]

    all_rows = []

    for _, row in official_df.iterrows():
        municipality = row["base_municipality"]
        official_url = row["target_url"]

        print(f"\nクロール中: {municipality}")

        try:
            rows = crawl_municipality(
                municipality=municipality,
                official_url=official_url
            )
            all_rows.extend(rows)

        except Exception as e:
            all_rows.append({
                "base_municipality": municipality,
                "detected_category": "error",
                "depth": "",
                "title": "",
                "url": official_url,
                "source_page_title": "",
                "source_page_url": "",
                "error": f"municipality_error: {e}",
            })

        time.sleep(1)

    out_df = pd.DataFrame(all_rows)

    if not out_df.empty:
        out_df = out_df.drop_duplicates(
            subset=[
                "base_municipality",
                "detected_category",
                "url"
            ]
        )

        out_df = out_df.sort_values(
            by=[
                "base_municipality",
                "detected_category",
                "depth",
                "url"
            ]
        )

    out_df.to_csv(
        OUTPUT_CSV,
        index=False,
        encoding="utf-8-sig"
    )

    print("\nクロール完了")
    print(f"出力: {OUTPUT_CSV}")
    print(f"取得件数: {len(out_df)}")


if __name__ == "__main__":
    main()