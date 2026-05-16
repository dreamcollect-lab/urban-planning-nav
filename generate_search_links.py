import pandas as pd
from urllib.parse import quote_plus

INPUT_CSV = "tokyo_23ku_master_updated.csv"
OUTPUT_CSV = "tokyo_23ku_search_links.csv"

SEARCH_KEYWORDS = {
    "official": "公式サイト",
    "road": "指定道路図",
    "district_plan": "地区計画",
    "building_guidance": "建築指導課",
}


def generate_google_search_url(query: str) -> str:
    encoded = quote_plus(query)
    return f"https://www.google.com/search?q={encoded}"


def main():
    df = pd.read_csv(INPUT_CSV)

    rows = []

    for _, row in df.iterrows():

        base_municipality = row["base_municipality"]
        category = row["category"]

        if category not in SEARCH_KEYWORDS:
            continue

        keyword = SEARCH_KEYWORDS[category]

        query = f"{base_municipality} {keyword}"

        search_url = generate_google_search_url(query)

        rows.append({
            "base_municipality": base_municipality,
            "category": category,
            "search_keyword": query,
            "google_search_url": search_url,
            "registered_url": row.get("target_url", "")
        })

    out_df = pd.DataFrame(rows)

    out_df.to_csv(
        OUTPUT_CSV,
        index=False,
        encoding="utf-8-sig"
    )

    print("検索URL生成完了")
    print(f"出力: {OUTPUT_CSV}")


if __name__ == "__main__":
    main()