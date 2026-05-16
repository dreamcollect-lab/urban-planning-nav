import pandas as pd


INPUT_CSV = "official_site_links.csv"
OUTPUT_CSV = "official_site_links_ranked.csv"


CATEGORY_RULES = {
    "road": {
        "label": "道路・接道確認",
        "must_keywords": [
            "指定道路",
            "道路台帳",
            "建築基準法道路",
            "道路種別",
            "幅員",
            "狭あい",
            "2項道路",
            "認定道路",
            "私道",
            "douro",
            "doro",
            "road",
            "shitei",
        ],
    },
    "district_plan": {
        "label": "都市計画・用途地域",
        "must_keywords": [
            "都市計画情報",
            "都市計画概要",
            "用途地域",
            "建ぺい率",
            "建蔽率",
            "容積率",
            "高度地区",
            "防火地域",
            "準防火地域",
            "地区計画",
            "景観計画",
            "都市計画図",
            "toshikeikaku",
            "toshi",
        ],
    },
    "hazard": {
        "label": "ハザード・災害リスク",
        "must_keywords": [
            "ハザードマップ",
            "洪水",
            "内水",
            "高潮",
            "土砂災害",
            "津波",
            "浸水",
            "防災マップ",
            "hazard",
        ],
    },
    "building_guidance": {
        "label": "建築指導・建築確認",
        "must_keywords": [
            "建築指導",
            "建築確認",
            "建築基準法",
            "建築審査",
            "開発許可",
            "日影規制",
            "kenchiku",
        ],
    },
}


STRONG_EXCLUDE_KEYWORDS = [
    "ページトップ",
    "本文へスキップ",
    "こちらのページ",
    "エントリー期間",
    "アンケート",
    "審議会",
    "速記録",
    "議事録",
    "開催します",
    "説明会",
    "ニュース",
    "お知らせ",
    "イベント",
    "広報",
    "採用",
    "求人",
    "助成",
    "あっせん",
    "防犯",
    "交通事故",
    "救急",
    "火災",
    "災害支援",
    "ボランティア",
    "小学校",
    "中学校",
    "建て替え事業",
    "施工者",
    "ページトップ",
    "faq",
    "koho",
    "news",
    "event",
    "calendar",
]


WEAK_EXCLUDE_KEYWORDS = [
    "くらし",
    "相談",
    "申請",
    "手続き",
    "施設",
    "料金",
]


ADDITIONAL_TOPICS = [
    ["用途地域", "購入判断・重要事項説明", "都市計画GISまたは都市計画図で確認"],
    ["建ぺい率・容積率", "購入判断・重要事項説明", "収益性、増改築余地に影響"],
    ["防火地域・準防火地域", "重要事項説明", "建築コスト、建築制限に影響"],
    ["高度地区", "購入判断・重要事項説明", "建物高さ、収益性に影響"],
    ["地区計画", "購入判断・重要事項説明", "用途、形態、壁面後退等に影響"],
    ["景観計画・景観条例", "重要事項説明", "外観、広告物、建築制限に影響"],
    ["指定道路図", "購入判断・重要事項説明", "再建築可否、接道義務に直結"],
    ["道路台帳・幅員", "購入判断・重要事項説明", "道路幅員、容積率、セットバックに影響"],
    ["建築基準法上の道路種別", "購入判断・重要事項説明", "再建築可否に直結"],
    ["洪水ハザード", "購入判断・重要事項説明", "災害リスク、説明義務、価格に影響"],
    ["内水ハザード", "購入判断・重要事項説明", "自治体により別マップの場合あり"],
    ["高潮ハザード", "購入判断・重要事項説明", "湾岸部などで重要"],
    ["土砂災害警戒区域", "重要事項説明", "都道府県サイト確認が必要な場合あり"],
    ["津波災害警戒区域", "重要事項説明", "都道府県サイト確認が必要な場合あり"],
    ["宅地造成等工事規制区域", "重要事項説明", "盛土規制法・都道府県確認が必要"],
    ["造成宅地防災区域", "重要事項説明", "自治体サイトにない場合あり"],
    ["日影規制", "購入判断・重要事項説明", "用途地域だけでは判断できないため別確認"],
]


def contains_any(text, keywords):
    text = str(text).lower()
    return any(str(k).lower() in text for k in keywords)


def calc_score(row):
    category = str(row.get("detected_category", ""))
    title = str(row.get("title", ""))
    url = str(row.get("url", ""))
    depth = row.get("depth", "")

    text = f"{title} {url}"

    if category not in CATEGORY_RULES:
        return -999

    if contains_any(text, STRONG_EXCLUDE_KEYWORDS):
        return -999

    score = 0

    for kw in CATEGORY_RULES[category]["must_keywords"]:
        if str(kw).lower() in text.lower():
            score += 20

    if contains_any(text, WEAK_EXCLUDE_KEYWORDS):
        score -= 10

    if "pdf" in url.lower():
        score += 5

    if "map" in url.lower():
        score += 8

    if "gis" in url.lower():
        score += 10

    if "ハザードマップ" in text:
        score += 15

    if "指定道路" in text:
        score += 20

    if "道路台帳" in text:
        score += 20

    if "用途地域" in text:
        score += 20

    if "都市計画情報" in text:
        score += 20

    if "建築基準法" in text:
        score += 20

    try:
        if int(depth) >= 2:
            score += 3
    except Exception:
        pass

    return score


def display_rank(score):
    if score >= 40:
        return "優先確認"
    if score >= 20:
        return "関連確認"
    if score >= 10:
        return "参考"
    return "除外"


def main():
    df = pd.read_csv(INPUT_CSV)

    df["score"] = df.apply(calc_score, axis=1)
    df["display_rank"] = df["score"].apply(display_rank)

    df = df[df["display_rank"] != "除外"].copy()

    df["category_label"] = df["detected_category"].map(
        lambda x: CATEGORY_RULES.get(x, {}).get("label", x)
    )

    df = df.sort_values(
        by=["base_municipality", "detected_category", "score"],
        ascending=[True, True, False]
    )

    df.to_csv(OUTPUT_CSV, index=False, encoding="utf-8-sig")

    topics_df = pd.DataFrame(
        ADDITIONAL_TOPICS,
        columns=["確認項目", "用途", "確認理由"]
    )
    topics_df.to_csv(
        "important_explanation_topics.csv",
        index=False,
        encoding="utf-8-sig"
    )

    print("ランキング改善版 完了")
    print(f"出力: {OUTPUT_CSV}")
    print(f"件数: {len(df)}")


if __name__ == "__main__":
    main()