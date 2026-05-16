import time
import pandas as pd
import requests
from bs4 import BeautifulSoup
from urllib.parse import quote_plus, urlparse, parse_qs, unquote

INPUT_CSV = "tokyo_23ku_master_updated.csv"
OUTPUT_CSV = "candidate_urls.csv"

SEARCH_KEYWORDS = {
    "official": "公式サイト",
    "road": "指定道路図 道路台帳 建築基準法道路",
    "district_plan": "地区計画",
    "building_guidance": "建築指導課 建築確認",
}

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}


def clean_duckduckgo_url(url: str) -> str:
    if "uddg=" in url:
        parsed = urlparse(url)
        query = parse_qs(parsed.query)
        if "uddg" in query:
            return unquote(query["uddg"][0])
    return url


def search_duckduckgo(query: str, max_results: int = 5) -> list[dict]:
    search_url = f"https://duckduckgo.com/html/?q={quote_plus(query)}"

    try:
        response = requests.get(
            search_url,
            headers=HEADERS,
            timeout=20
        )
        response.raise_for_status()

    except Exception as e:
        return [{
            "title": "",
            "url": "",
            "error": str(e)
        }]

    soup = BeautifulSoup(response.text, "html.parser")

    results = []

    for result in soup.select(".result")[:max_results]:
        title_tag = result.select_one(".result__title a")
        snippet_tag = result.select_one(".result__snippet")

        if not title_tag:
            continue

        title = title_tag.get_text(" ", strip=True)
        url = title_tag.get("href", "")
        url = clean_duckduckgo_url(url)
        snippet = snippet_tag.get_text(" ", strip=True) if snippet_tag else ""

        results.append({
            "title": title,
            "url": url,
            "snippet": snippet,
            "error": ""
        })

    return results


def score_url(base_municipality: str, category: str, title: str, url: str, snippet: str) -> int:
    text = f"{title} {url} {snippet}"

    score = 0

    if base_municipality in text:
        score += 3

    if "lg.jp" in url:
        score += 3

    if "city" in url:
        score += 1

    if category == "road":
        for word in ["指定道路", "道路台帳", "建築基準法", "道路"]:
            if word in text:
                score += 2

    if category == "district_plan":
        for word in ["地区計画", "まちづくり"]:
            if word in text:
                score += 2

    if category == "building_guidance":
        for word in ["建築指導", "建築確認", "建築課", "建築"]:
            if word in text:
                score += 2

    if category == "official":
        for word in ["公式", "ホームページ"]:
            if word in text:
                score += 2

    return score


def main():
    df = pd.read_csv(INPUT_CSV)

    rows = []

    target_df = df[
        (df["base_municipality"] != "全自治体共通") &
        (df["category"].isin(SEARCH_KEYWORDS.keys()))
    ]

    for _, row in target_df.iterrows():
        base_municipality = row["base_municipality"]
        category = row["category"]
        keyword = SEARCH_KEYWORDS[category]

        query = f"{base_municipality} {keyword}"

        print(f"検索中: {query}")

        results = search_duckduckgo(query, max_results=5)

        for rank, result in enumerate(results, start=1):
            title = result.get("title", "")
            url = result.get("url", "")
            snippet = result.get("snippet", "")
            error = result.get("error", "")

            score = score_url(
                base_municipality,
                category,
                title,
                url,
                snippet
            )

            rows.append({
                "base_municipality": base_municipality,
                "category": category,
                "search_query": query,
                "rank": rank,
                "score": score,
                "title": title,
                "url": url,
                "snippet": snippet,
                "error": error,
            })

        time.sleep(2)

    out_df = pd.DataFrame(rows)

    out_df = out_df.sort_values(
        by=["base_municipality", "category", "score", "rank"],
        ascending=[True, True, False, True]
    )

    out_df.to_csv(
        OUTPUT_CSV,
        index=False,
        encoding="utf-8-sig"
    )

    print("候補URL収集完了")
    print(f"出力: {OUTPUT_CSV}")


if __name__ == "__main__":
    main()