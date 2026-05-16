import pandas as pd

MASTER_CSV = "tokyo_23ku_master_auto.csv"
LINKS_CSV = "official_site_links.csv"
OUTPUT_CSV = "tokyo_23ku_master_crawled.csv"


def main():
    master_df = pd.read_csv(MASTER_CSV)
    links_df = pd.read_csv(LINKS_CSV)

    updated_count = 0

    for _, link_row in links_df.iterrows():
        municipality = link_row["base_municipality"]
        category = link_row["detected_category"]
        url = link_row["url"]
        title = link_row["title"]

        if pd.isna(url) or str(url).strip() == "":
            continue

        condition = (
            (master_df["base_municipality"] == municipality) &
            (master_df["category"] == category)
        )

        if master_df[condition].empty:
            continue

        current_url = master_df.loc[condition, "target_url"].iloc[0]

        # すでにURLが入っている場合は上書きしない
        if pd.notna(current_url) and str(current_url).strip() != "":
            continue

        master_df.loc[condition, "target_url"] = url
        master_df.loc[condition, "status"] = "official_site_crawled"
        master_df.loc[condition, "recommended_action"] = "公式サイト内候補URL"
        master_df.loc[condition, "comment"] = f"公式サイト内から候補URLを抽出：{title}。要確認。"

        updated_count += 1

    master_df.to_csv(
        OUTPUT_CSV,
        index=False,
        encoding="utf-8-sig"
    )

    print("公式サイト内リンクの反映完了")
    print(f"更新件数: {updated_count}")
    print(f"出力: {OUTPUT_CSV}")


if __name__ == "__main__":
    main()