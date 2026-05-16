import pandas as pd

INPUT_CSV = "tokyo_23ku_master_auto.csv"
OUTPUT_CSV = "tokyo_23ku_master_auto.csv"

OFFICIAL_URLS = {
    "千代田区": "https://www.city.chiyoda.lg.jp/",
    "中央区": "https://www.city.chuo.lg.jp/",
    "港区": "https://www.city.minato.tokyo.jp/",
    "新宿区": "https://www.city.shinjuku.lg.jp/",
    "文京区": "https://www.city.bunkyo.lg.jp/",
    "台東区": "https://www.city.taito.lg.jp/",
    "墨田区": "https://www.city.sumida.lg.jp/",
    "江東区": "https://www.city.koto.lg.jp/",
    "品川区": "https://www.city.shinagawa.tokyo.jp/",
    "目黒区": "https://www.city.meguro.tokyo.jp/",
    "大田区": "https://www.city.ota.tokyo.jp/",
    "世田谷区": "https://www.city.setagaya.lg.jp/",
    "渋谷区": "https://www.city.shibuya.tokyo.jp/",
    "中野区": "https://www.city.tokyo-nakano.lg.jp/",
    "杉並区": "https://www.city.suginami.tokyo.jp/",
    "豊島区": "https://www.city.toshima.lg.jp/",
    "北区": "https://www.city.kita.tokyo.jp/",
    "荒川区": "https://www.city.arakawa.tokyo.jp/",
    "板橋区": "https://www.city.itabashi.tokyo.jp/",
    "練馬区": "https://www.city.nerima.tokyo.jp/",
    "足立区": "https://www.city.adachi.tokyo.jp/",
    "葛飾区": "https://www.city.katsushika.lg.jp/",
    "江戸川区": "https://www.city.edogawa.tokyo.jp/",
}


def main():
    df = pd.read_csv(INPUT_CSV)

    updated_count = 0

    for ku, url in OFFICIAL_URLS.items():
        condition = (
            (df["base_municipality"] == ku) &
            (df["category"] == "official")
        )

        if df[condition].empty:
            continue

        df.loc[condition, "target_url"] = url
        df.loc[condition, "status"] = "manual_seeded"
        df.loc[condition, "recommended_action"] = "公式確認先"
        df.loc[condition, "comment"] = "23区公式サイトURLを初期登録。必要に応じて確認。"

        updated_count += 1

    df.to_csv(OUTPUT_CSV, index=False, encoding="utf-8-sig")

    print("23区公式URLの登録完了")
    print(f"更新件数: {updated_count}")
    print(f"出力: {OUTPUT_CSV}")


if __name__ == "__main__":
    main()