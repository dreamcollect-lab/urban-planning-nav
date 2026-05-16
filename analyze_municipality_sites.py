import asyncio
import pandas as pd
from playwright.async_api import async_playwright

INPUT_CSV = "municipalities.csv"
OUTPUT_CSV = "municipality_analysis_result.csv"

KEYWORDS = {
    "arcgis": ["arcgis", "mapserver", "featureserver"],
    "geojson": ["geojson"],
    "wms_wfs": ["wms", "wfs", "getfeature", "getmap"],
    "pdf": [".pdf"],
    "query_api": ["query?"],
    "hazard": ["hazard", "disaportal"],
}


def classify_url(url: str) -> list[str]:
    lower_url = url.lower()
    hits = []

    for category, words in KEYWORDS.items():
        for word in words:
            if word in lower_url:
                hits.append(category)
                break

    return hits


async def analyze_site(row: dict) -> dict:
    detected_urls = []
    detected_types = set()

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        page.on("request", lambda request: detected_urls.append(request.url))

        try:
            await page.goto(row["target_url"], wait_until="domcontentloaded", timeout=20000)
            await page.wait_for_timeout(7000)
            status = "ok"
            error = ""

        except Exception as e:
            status = "error"
            error = str(e)

        await browser.close()

    important_urls = []

    for url in detected_urls:
        hits = classify_url(url)

        if hits:
            important_urls.append(url)

            for hit in hits:
                detected_types.add(hit)

    important_urls = list(dict.fromkeys(important_urls))

    return {
        "prefecture": row["prefecture"],
        "municipality": row["municipality"],
        "category": row.get("category", ""),
        "target_url": row["target_url"],
        "status": status,
        "detected_types": ",".join(sorted(detected_types)),
        "important_urls": " | ".join(important_urls[:20]),
        "error": error,
    }


async def main():
    df = pd.read_csv(INPUT_CSV)

    results = []

    for _, row in df.iterrows():
        row_dict = row.to_dict()
        print(f"解析中: {row_dict['municipality']} / {row_dict['category']}")

        result = await analyze_site(row_dict)
        results.append(result)

    out_df = pd.DataFrame(results)
    out_df.to_csv(OUTPUT_CSV, index=False, encoding="utf-8-sig")

    print("完了しました")
    print(f"出力: {OUTPUT_CSV}")


if __name__ == "__main__":
    asyncio.run(main())