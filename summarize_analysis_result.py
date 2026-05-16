import pandas as pd

INPUT_CSV = "municipality_analysis_result.csv"
OUTPUT_CSV = "municipality_analysis_summary.csv"


def judge_action(status: str, detected_types: str) -> str:
    detected_types = "" if pd.isna(detected_types) else detected_types

    if status != "ok":
        return "要確認：ページ取得エラー"

    if any(x in detected_types for x in ["arcgis", "geojson", "wms_wfs", "query_api"]):
        return "自動取得候補"

    if "pdf" in detected_types:
        return "PDF確認候補"

    if "hazard" in detected_types:
        return "ハザード確認候補"

    return "ナビ表示候補"


def make_comment(row) -> str:
    status = row.get("status", "")
    detected_types = "" if pd.isna(row.get("detected_types", "")) else row.get("detected_types", "")
    category = row.get("category", "")

    if status != "ok":
        return "ページが開けていません。URL確認またはタイムアウト調整が必要です。"

    if detected_types:
        return f"検出タイプ：{detected_types}"

    if category == "official":
        return "公式トップページです。ナビ用URLとして保持します。"

    return "通信上の自動取得候補は未検出です。公式確認先として保持します。"


def main():
    df = pd.read_csv(INPUT_CSV)

    df["recommended_action"] = df.apply(
        lambda row: judge_action(row["status"], row.get("detected_types", "")),
        axis=1
    )

    df["comment"] = df.apply(make_comment, axis=1)

    columns = [
        "prefecture",
        "municipality",
        "category",
        "target_url",
        "status",
        "detected_types",
        "recommended_action",
        "comment",
        "important_urls",
        "error",
    ]

    df = df[columns]

    df.to_csv(OUTPUT_CSV, index=False, encoding="utf-8-sig")

    print("集計完了")
    print(f"出力: {OUTPUT_CSV}")


if __name__ == "__main__":
    main()