import pandas as pd

MASTER_CSV = "tokyo_23ku_master_updated.csv"
CANDIDATE_CSV = "candidate_urls.csv"
OUTPUT_CSV = "tokyo_23ku_master_auto.csv"


def main():

    master_df = pd.read_csv(MASTER_CSV)
    candidate_df = pd.read_csv(CANDIDATE_CSV)

    # rank1のみ使う
    top_df = candidate_df[candidate_df["rank"] == 1]

    updated_count = 0

    for _, row in top_df.iterrows():

        municipality = row["base_municipality"]
        category = row["category"]
        url = row["url"]

        if pd.isna(url) or str(url).strip() == "":
            continue

        condition = (
            (master_df["base_municipality"] == municipality) &
            (master_df["category"] == category)
        )

        matched_rows = master_df[condition]

        if matched_rows.empty:
            continue

        current_url = matched_rows.iloc[0]["target_url"]

        # 空欄だけ更新
        if pd.isna(current_url) or str(current_url).strip() == "":

            master_df.loc[condition, "target_url"] = url

            master_df.loc[condition, "status"] = "auto_collected"

            master_df.loc[
                condition,
                "recommended_action"
            ] = "自動収集URL"

            master_df.loc[
                condition,
                "comment"
            ] = "検索結果1位URLを自動採用。要確認。"

            updated_count += 1

    master_df.to_csv(
        OUTPUT_CSV,
        index=False,
        encoding="utf-8-sig"
    )

    print("自動URL反映完了")
    print(f"更新件数: {updated_count}")
    print(f"出力: {OUTPUT_CSV}")


if __name__ == "__main__":
    main()