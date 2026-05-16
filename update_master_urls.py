import pandas as pd

MASTER_CSV = "tokyo_23ku_master.csv"
UPDATE_CSV = "url_update_template.csv"
OUTPUT_CSV = "tokyo_23ku_master_updated.csv"


def main():
    master_df = pd.read_csv(MASTER_CSV)
    update_df = pd.read_csv(UPDATE_CSV)

    for _, update_row in update_df.iterrows():
        base_municipality = update_row["base_municipality"]
        category = update_row["category"]
        target_url = update_row["target_url"]

        if pd.isna(target_url) or str(target_url).strip() == "":
            continue

        condition = (
            (master_df["base_municipality"] == base_municipality) &
            (master_df["category"] == category)
        )

        master_df.loc[condition, "target_url"] = target_url
        master_df.loc[condition, "recommended_action"] = "公式確認先"
        master_df.loc[condition, "status"] = "manual_registered"
        master_df.loc[condition, "comment"] = "公式確認先URLを登録済み。必要に応じて内容を確認してください。"

    master_df.to_csv(OUTPUT_CSV, index=False, encoding="utf-8-sig")

    print("URL反映が完了しました")
    print(f"出力: {OUTPUT_CSV}")


if __name__ == "__main__":
    main()