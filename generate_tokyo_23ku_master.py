import pandas as pd

OUTPUT_CSV = "tokyo_23ku_master.csv"

TOKYO_23KU = [
    "千代田区",
    "中央区",
    "港区",
    "新宿区",
    "文京区",
    "台東区",
    "墨田区",
    "江東区",
    "品川区",
    "目黒区",
    "大田区",
    "世田谷区",
    "渋谷区",
    "中野区",
    "杉並区",
    "豊島区",
    "北区",
    "荒川区",
    "板橋区",
    "練馬区",
    "足立区",
    "葛飾区",
    "江戸川区",
]

COMMON_LINKS = [
    {
        "category": "urban_plan",
        "name_suffix": "東京都都市計画情報",
        "url": "https://www2.wagmap.jp/tokyo_tokeizu/",
        "note": "東京都共通。用途地域、建ぺい率、容積率、防火地域、高度地区などの確認候補。",
    },
    {
        "category": "hazard",
        "name_suffix": "国土地理院ハザード",
        "url": "https://disaportal.gsi.go.jp/",
        "note": "全国共通。洪水、土砂災害、津波等の確認候補。",
    },
]

LOCAL_PLACEHOLDERS = [
    {
        "category": "official",
        "name_suffix": "公式サイト",
        "url": "",
        "note": "各区公式サイト。後で正確なURLを登録。",
    },
    {
        "category": "road",
        "name_suffix": "道路情報",
        "url": "",
        "note": "指定道路図、道路台帳、道路種別、幅員確認先。後で登録。",
    },
    {
        "category": "district_plan",
        "name_suffix": "地区計画",
        "url": "",
        "note": "地区計画、まちづくりルール確認先。後で登録。",
    },
    {
        "category": "building_guidance",
        "name_suffix": "建築指導課",
        "url": "",
        "note": "接道、再建築可否、建築基準法道路の最終確認先。後で登録。",
    },
]


def main():
    rows = []

    for ku in TOKYO_23KU:

        for item in LOCAL_PLACEHOLDERS:
            rows.append({
                "prefecture": "東京都",
                "municipality": f"{ku}{item['name_suffix']}",
                "base_municipality": ku,
                "category": item["category"],
                "target_url": item["url"],
                "status": "manual",
                "detected_types": "",
                "recommended_action": "公式URL登録待ち",
                "comment": item["note"],
                "important_urls": "",
                "error": "",
            })

    for item in COMMON_LINKS:
        rows.append({
            "prefecture": "東京都",
            "municipality": item["name_suffix"],
            "base_municipality": "全自治体共通",
            "category": item["category"],
            "target_url": item["url"],
            "status": "manual",
            "detected_types": "",
            "recommended_action": "共通公式リンク",
            "comment": item["note"],
            "important_urls": "",
            "error": "",
        })

    df = pd.DataFrame(rows)
    df.to_csv(OUTPUT_CSV, index=False, encoding="utf-8-sig")

    print("東京都23区マスタを作成しました")
    print(f"出力: {OUTPUT_CSV}")
    print(f"行数: {len(df)}")


if __name__ == "__main__":
    main()