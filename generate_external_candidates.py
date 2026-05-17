from pathlib import Path
import pandas as pd


BASE_DIR = Path(__file__).resolve().parent

INPUT_CSV = BASE_DIR / "official_site_links_ranked.csv"
OUTPUT_CSV = BASE_DIR / "external_reference_links.bulk_candidates.csv"


CATEGORY_MAP = {
    "road": {
        "subcategory": "道路関連",
        "memo": "クロール結果から抽出した道路・接道関連の確認候補",
    },
    "district_plan": {
        "subcategory": "都市計画情報",
        "memo": "クロール結果から抽出した用途地域・都市計画関連の確認候補",
    },
    "hazard": {
        "subcategory": "ハザード",
        "memo": "クロール結果から抽出した防災・ハザード関連の確認候補",
    },
    "building_guidance": {
        "subcategory": "建築確認",
        "memo": "クロール結果から抽出した建築指導・建築確認関連の確認候補",
    },
}


TOKYO_23KU = [
    "千代田区", "中央区", "港区", "新宿区", "文京区", "台東区",
    "墨田区", "江東区", "品川区", "目黒区", "大田区", "世田谷区",
    "渋谷区", "中野区", "杉並区", "豊島区", "北区", "荒川区",
    "板橋区", "練馬区", "足立区", "葛飾区", "江戸川区",
]


OUTPUT_COLUMNS = [
    "prefecture",
    "municipality",
    "category",
    "subcategory",
    "title",
    "url",
    "source_level",
    "required_status",
    "memo",
    "display_scope",
    "priority",
]


def clean_text(value):
    if pd.isna(value):
        return ""
    return str(value).strip()


def is_valid_url(url):
    url = clean_text(url)
    return url.startswith("http://") or url.startswith("https://")


def main():
    if not INPUT_CSV.exists():
        raise FileNotFoundError(f"{INPUT_CSV} が見つかりません。")

    df = pd.read_csv(INPUT_CSV, encoding="utf-8-sig")

    required = [
        "base_municipality",
        "detected_category",
        "display_rank",
        "score",
        "title",
        "url",
    ]

    for col in required:
        if col not in df.columns:
            df[col] = ""

    df["base_municipality"] = df["base_municipality"].apply(clean_text)
    df["detected_category"] = df["detected_category"].apply(clean_text)
    df["title"] = df["title"].apply(clean_text)
    df["url"] = df["url"].apply(clean_text)

    df = df[
        df["base_municipality"].isin(TOKYO_23KU)
        & df["detected_category"].isin(CATEGORY_MAP.keys())
        & df["url"].apply(is_valid_url)
    ].copy()

    df["score"] = pd.to_numeric(df["score"], errors="coerce").fillna(0)

    df = df.sort_values(
        by=["base_municipality", "detected_category", "score"],
        ascending=[True, True, False],
    )

    # 各区・各カテゴリ上位3件まで
    df = df.groupby(
        ["base_municipality", "detected_category"],
        as_index=False,
        group_keys=False,
    ).head(3)

    rows = []

    for _, row in df.iterrows():
        municipality = clean_text(row["base_municipality"])
        category = clean_text(row["detected_category"])
        title = clean_text(row["title"])
        url = clean_text(row["url"])

        if not title:
            title = "確認候補"

        category_info = CATEGORY_MAP.get(category, {})

        rows.append({
            "prefecture": "東京都",
            "municipality": municipality,
            "category": category,
            "subcategory": category_info.get("subcategory", ""),
            "title": title,
            "url": url,
            "source_level": "区公式候補",
            "required_status": "確認候補",
            "memo": category_info.get("memo", ""),
            "display_scope": "municipality",
            "priority": 50,
        })

    out_df = pd.DataFrame(rows, columns=OUTPUT_COLUMNS)

    out_df.to_csv(OUTPUT_CSV, index=False, encoding="utf-8-sig")

    print(f"作成完了: {OUTPUT_CSV}")
    print(f"出力件数: {len(out_df)}")


if __name__ == "__main__":
    main()