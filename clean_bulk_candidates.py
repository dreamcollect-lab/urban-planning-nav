from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent

INPUT = BASE_DIR / "external_reference_links.bulk_candidates.csv"
OUTPUT = BASE_DIR / "external_reference_links.review_candidates.csv"

REMOVE_KEYWORDS = [
    "ページ先頭",
    "本文へ移動",
    "スキップ",
    "できごと",
    "マンホール",
    "喫煙所",
    "英語版",
    "音声版",
    "耳で聴く",
    "仕様書",
    "協定書",
    "工事説明",
    "自転車",
    "メール",
    "イベント",
    "愛称",
]

KEEP_KEYWORDS = [
    "指定道路",
    "道路台帳",
    "建築基準法",
    "道路種別",
    "用途地域",
    "都市計画",
    "都市計画図",
    "ハザード",
    "洪水",
    "内水",
    "高潮",
    "土砂災害",
    "建築確認",
    "開発許可",
    "建築指導",
    "位置指定道路",
]

def clean_text(v):
    if pd.isna(v):
        return ""
    return str(v).strip()

df = pd.read_csv(INPUT, encoding="utf-8-sig")

for col in ["title", "url", "memo"]:
    if col not in df.columns:
        df[col] = ""

df["title_text"] = df["title"].apply(clean_text)
df["memo_text"] = df["memo"].apply(clean_text)
df["search_text"] = df["title_text"] + " " + df["memo_text"]

def has_remove_keyword(text):
    return any(k in text for k in REMOVE_KEYWORDS)

def has_keep_keyword(text):
    return any(k in text for k in KEEP_KEYWORDS)

df = df[
    (~df["search_text"].apply(has_remove_keyword))
    & (df["search_text"].apply(has_keep_keyword))
].copy()

df = df.drop(columns=["title_text", "memo_text", "search_text"], errors="ignore")

df.to_csv(OUTPUT, index=False, encoding="utf-8-sig")

print(f"作成完了: {OUTPUT}")
print(f"残件数: {len(df)}")