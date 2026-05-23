from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent

INPUT = BASE_DIR / "external_reference_links.review_candidates.csv"
OUTPUT = BASE_DIR / "external_reference_links.ready_for_add.csv"

REMOVE_KEYWORDS = [
    "ページ先頭",
    "本文へ移動",
    "スキップ",
    "できごと",
    "マンホール",
    "喫煙所",
    "英語版",
    "中国語",
    "やさしい日本語",
    "音声版",
    "耳で聴く",
    "仕様書",
    "協定書",
    "工事説明",
    "自転車",
    "メール",
    "イベント",
    "愛称",
    "避難所",
    "実験",
    "社会実験",
    "相談会",
    "募集",
    "講座",
    "お知らせ",
    "新旧対照表",
    "景観まちづくり",
    "地域住宅計画",
    "違法貸しルーム",
    "事業用建築物",
    "安全安心な建物づくり",
    "建築審査会",
]

KEEP_KEYWORDS = [
    "指定道路",
    "道路台帳",
    "道路種別",
    "建築基準法上の道路",
    "位置指定道路",
    "用途地域",
    "都市計画情報",
    "都市計画図",
    "用途地域等",
    "建ぺい率",
    "容積率",
    "ハザードマップ",
    "洪水",
    "内水",
    "高潮",
    "土砂災害",
    "建築確認",
    "開発許可",
    "建築指導",
    "許可・認定",
    "建築物の許可",
]

CATEGORY_REQUIRED_KEYWORDS = {
    "road": [
        "指定道路",
        "道路台帳",
        "道路種別",
        "建築基準法上の道路",
        "位置指定道路",
        "幅員",
        "区有通路",
        "路線図",
        "境界",
    ],
    "district_plan": [
        "用途地域",
        "都市計画情報",
        "都市計画図",
        "用途地域等",
        "建ぺい率",
        "容積率",
        "地区計画",
        "高度地区",
        "防火地域",
    ],
    "hazard": [
        "ハザードマップ",
        "洪水",
        "内水",
        "高潮",
        "土砂災害",
        "浸水",
        "水害",
    ],
    "building_guidance": [
        "建築確認",
        "開発許可",
        "建築指導",
        "許可・認定",
        "建築物の許可",
        "位置指定道路",
        "建築基準法",
    ],
}

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


def contains_any(text, keywords):
    return any(keyword in text for keyword in keywords)


def main():
    if not INPUT.exists():
        raise FileNotFoundError(f"{INPUT} が見つかりません。")

    df = pd.read_csv(INPUT, encoding="utf-8-sig")

    for col in OUTPUT_COLUMNS:
        if col not in df.columns:
            df[col] = ""

    df["title"] = df["title"].apply(clean_text)
    df["subcategory"] = df["subcategory"].apply(clean_text)
    df["memo"] = df["memo"].apply(clean_text)
    df["category"] = df["category"].apply(clean_text)
    df["url"] = df["url"].apply(clean_text)

    df["search_text"] = (
        df["title"] + " " + df["subcategory"] + " " + df["memo"] + " " + df["url"]
    )

    # 1. 明らかなノイズを削除
    df = df[~df["search_text"].apply(lambda x: contains_any(x, REMOVE_KEYWORDS))].copy()

    # 2. 全体の重要キーワードに一致するものだけ残す
    df = df[df["search_text"].apply(lambda x: contains_any(x, KEEP_KEYWORDS))].copy()

    # 3. categoryごとの必須キーワードに一致するものだけ残す
    keep_rows = []

    for _, row in df.iterrows():
        category = clean_text(row["category"])
        text = clean_text(row["search_text"])
        required_keywords = CATEGORY_REQUIRED_KEYWORDS.get(category, [])

        if not required_keywords:
            continue

        if contains_any(text, required_keywords):
            keep_rows.append(row)

    if keep_rows:
        out_df = pd.DataFrame(keep_rows)
    else:
        out_df = pd.DataFrame(columns=OUTPUT_COLUMNS)

    # 4. 表示用に整える
    out_df = out_df[OUTPUT_COLUMNS].copy()
    out_df["required_status"] = "確認候補"
    out_df["source_level"] = out_df["source_level"].replace("", "区公式候補")
    out_df["display_scope"] = out_df["display_scope"].replace("", "municipality")

    out_df["priority"] = pd.to_numeric(
        out_df["priority"],
        errors="coerce",
    ).fillna(50).astype(int)

    # 5. 重複URLを削除
    out_df = out_df.drop_duplicates(
        subset=["municipality", "category", "url"],
        keep="first",
    )

    out_df.to_csv(OUTPUT, index=False, encoding="utf-8-sig")

    print(f"作成完了: {OUTPUT}")
    print(f"入力件数: {len(df)}")
    print(f"出力件数: {len(out_df)}")


if __name__ == "__main__":
    main()