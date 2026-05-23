import pandas as pd
from pathlib import Path

SOURCE_FILE = Path("manual_review_ready_for_add.csv")
ADD_FILE = Path("external_reference_links.add.csv")
BACKUP_FILE = Path("external_reference_links.add.backup.csv")

COLUMNS = [
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

def main():
    if not SOURCE_FILE.exists():
        raise FileNotFoundError(f"{SOURCE_FILE} が見つかりません。")

    if not ADD_FILE.exists():
        raise FileNotFoundError(f"{ADD_FILE} が見つかりません。")

    source_df = pd.read_csv(SOURCE_FILE, encoding="utf-8-sig")
    add_df = pd.read_csv(ADD_FILE, encoding="utf-8-sig")

    missing_source = [c for c in COLUMNS if c not in source_df.columns]
    missing_add = [c for c in COLUMNS if c not in add_df.columns]

    if missing_source:
        raise ValueError(f"{SOURCE_FILE} に不足列があります: {missing_source}")

    if missing_add:
        raise ValueError(f"{ADD_FILE} に不足列があります: {missing_add}")

    source_df = source_df[COLUMNS].copy()
    add_df = add_df[COLUMNS].copy()

    add_df.to_csv(BACKUP_FILE, index=False, encoding="utf-8-sig")

    before_count = len(add_df)

    merged_df = pd.concat([add_df, source_df], ignore_index=True)

    merged_df = merged_df.drop_duplicates(
        subset=["municipality", "category", "title", "url"],
        keep="first"
    )

    after_count = len(merged_df)
    added_count = after_count - before_count

    merged_df.to_csv(ADD_FILE, index=False, encoding="utf-8-sig")

    print("完了しました。")
    print(f"追記前件数: {before_count}")
    print(f"追記候補件数: {len(source_df)}")
    print(f"実際に追加された件数: {added_count}")
    print(f"追記後件数: {after_count}")
    print(f"バックアップ: {BACKUP_FILE}")
    print(f"更新ファイル: {ADD_FILE}")

if __name__ == "__main__":
    main()