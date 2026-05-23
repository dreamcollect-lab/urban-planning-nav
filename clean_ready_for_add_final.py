import pandas as pd
from pathlib import Path

INPUT_FILE = Path("external_reference_links.ready_for_add.csv")
OUTPUT_FILE = Path("manual_review_ready_for_add.csv")
REMOVED_FILE = Path("manual_review_removed_candidates.csv")
REMOVE_LIST_FILE = Path("removal_list.csv")

KEEP_KEYWORDS = [
    "指定道路",
    "道路種別",
    "建築基準法上の道路",
    "道路台帳",
    "道路台帳平面図",
    "位置指定道路",
    "道路幅員",
    "用途地域",
    "都市計画情報",
    "都市計画図",
    "用途地域等",
    "ハザードマップ",
    "洪水",
    "内水",
    "高潮",
    "土砂災害",
    "浸水",
    "建築確認",
    "建築確認・許可",
    "許可・認定",
    "建築物の許可",
]

DROP_KEYWORDS = [
    "景観",
    "地区計画",
    "建築協定",
    "防災街区整備地区計画",
    "地域主体のまちづくり",
    "住宅・住環境",
    "総合治水",
    "都市整備",
    "各種計画など",
    "建物の維持管理",
    "地区のまちづくり",
    "宅地建物取引業者",
    "過去の用途地域",
    "誤記",
    "様式集",
    "こちらの案内",
    "確認候補",
    "建築確認台帳記載事項証明書",
    "事業者向け",
    "3D都市モデル",
    "国土交通省ハザードマップポータル",
    "水害・雪害・土砂災害対策",
    "水害・土砂災害対策実施要領",
]

REMOVE_TITLES = []

if REMOVE_LIST_FILE.exists():
    remove_df = pd.read_csv(REMOVE_LIST_FILE, encoding="utf-8-sig")

    if "title" not in remove_df.columns:
        raise ValueError("removal_list.csv に title 列がありません。1行目を title にしてください。")

    REMOVE_TITLES = remove_df["title"].dropna().astype(str).tolist()


def contains_any(text: str, keywords: list[str]) -> bool:
    text = str(text)
    return any(keyword in text for keyword in keywords)


def decide(row):
    title = str(row.get("title", ""))
    category = str(row.get("category", ""))
    subcategory = str(row.get("subcategory", ""))
    url = str(row.get("url", ""))

    target_text = " ".join([title, category, subcategory, url])

    # 1. 手動削除リストは最優先でDROP
    if title in REMOVE_TITLES:
        return "DROP"

    # 2. 明確な削除ワードがあればDROP
    if contains_any(target_text, DROP_KEYWORDS):
        return "DROP"

    # 3. 本命ワードがあればKEEP
    if contains_any(target_text, KEEP_KEYWORDS):
        return "KEEP"

    # 4. カテゴリ上は関係ありそうだが弱いもの
    if category in ["road", "hazard", "building_guidance"]:
        return "KEEP_REVIEW"

    return "DROP"


def set_priority(row):
    title = str(row.get("title", ""))
    category = str(row.get("category", ""))

    if category == "road":
        return 10

    if "用途地域" in title or "都市計画図" in title or "都市計画情報" in title:
        return 10

    if "ハザードマップ" in title or "洪水" in title or "浸水" in title or "土砂災害" in title:
        return 10

    if "建築確認" in title or "建築確認・許可" in title or "許可・認定" in title:
        return 20

    return 30


def main():
    if not INPUT_FILE.exists():
        raise FileNotFoundError(f"{INPUT_FILE} が見つかりません。")

    df = pd.read_csv(INPUT_FILE, encoding="utf-8-sig")

    required_columns = [
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

    missing_columns = [col for col in required_columns if col not in df.columns]
    if missing_columns:
        raise ValueError(f"必要な列が不足しています: {missing_columns}")

    df["review_decision"] = df.apply(decide, axis=1)

    keep_df = df[df["review_decision"].isin(["KEEP", "KEEP_REVIEW"])].copy()
    removed_df = df[df["review_decision"] == "DROP"].copy()

    keep_df["source_level"] = "区公式候補"
    keep_df["required_status"] = "確認候補"
    keep_df["display_scope"] = "municipality"
    keep_df["priority"] = keep_df.apply(set_priority, axis=1)

    keep_df = keep_df.drop_duplicates(subset=["municipality", "category", "title", "url"])
    removed_df = removed_df.drop_duplicates(subset=["municipality", "category", "title", "url"])

    keep_df.to_csv(OUTPUT_FILE, index=False, encoding="utf-8-sig")
    removed_df.to_csv(REMOVED_FILE, index=False, encoding="utf-8-sig")

    print("完了しました。")
    print(f"入力件数: {len(df)}")
    print(f"残した件数: {len(keep_df)}")
    print(f"削除候補件数: {len(removed_df)}")
    print(f"出力: {OUTPUT_FILE}")
    print(f"削除候補出力: {REMOVED_FILE}")


if __name__ == "__main__":
    main()