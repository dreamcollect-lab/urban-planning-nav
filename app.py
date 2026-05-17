import html as html_lib
from pathlib import Path
from textwrap import dedent

import pandas as pd
import streamlit as st


# =========================================================
# 基本設定
# =========================================================

st.set_page_config(
    page_title="都市計画ナビ β",
    layout="wide",
)

BASE_DIR = Path(__file__).resolve().parent

RANKED_CSV = BASE_DIR / "official_site_links_ranked.csv"
EXTERNAL_CSV = BASE_DIR / "external_reference_links.csv"
EXTERNAL_ADD_CSV = BASE_DIR / "external_reference_links.add.csv"


# =========================================================
# HTML表示
# =========================================================

def render_html(markup: str):
    st.markdown(
        dedent(markup).strip(),
        unsafe_allow_html=True,
    )


def clean_text(value) -> str:
    if pd.isna(value):
        return ""
    return str(value).strip()


def esc(value) -> str:
    return html_lib.escape(clean_text(value), quote=True)


# =========================================================
# CSS
# =========================================================

CUSTOM_CSS = """
<style>
.stApp {
    background-color: #f7f4ee;
    color: #222222;
}

.main .block-container {
    padding-top: 0.8rem;
    max-width: 980px;
}

html {
    font-size: 85%;
}

.hero {
    background: #ffffff;
    border-left: 8px solid #f26a21;
    padding: 20px 26px;
    margin-bottom: 18px;
    border-bottom: 1px solid #eadfce;
}

.hero-label {
    font-size: 13px;
    letter-spacing: 0.12em;
    color: #f26a21;
    font-weight: 700;
    margin-bottom: 8px;
}

.hero-title {
    font-size: 30px;
    font-weight: 800;
    line-height: 1.2;
    color: #111111;
    margin-bottom: 6px;
}

.hero-text {
    font-size: 13px;
    color: #444444;
}

.section-title {
    border-left: 6px solid #f26a21;
    padding-left: 12px;
    font-size: 20px;
    font-weight: 800;
    margin: 18px 0 12px 0;
    color: #111111;
}

.summary-box {
    background: #ffffff;
    border: 1px solid #e5dacb;
    padding: 14px 18px;
    margin-bottom: 18px;
}

.menu-card {
    background: #ffffff;
    border: 1px solid #e5dacb;
    padding: 16px;
    margin-bottom: 14px;
}

.menu-title {
    font-size: 20px;
    font-weight: 800;
    margin-bottom: 10px;
    color: #111111;
}

.mini-heading {
    font-weight: 800;
    color: #f26a21;
    margin-top: 10px;
    margin-bottom: 6px;
    font-size: 15px;
}

.check-list {
    margin-bottom: 8px;
    line-height: 1.55;
}

.link-box {
    border-top: 1px solid #eee4d7;
    padding-top: 12px;
    padding-bottom: 12px;
}

.open-link {
    display: inline-block;
    width: 100%;
    box-sizing: border-box;
    background: #ffffff;
    color: #111111 !important;
    border: 2px solid #f26a21;
    border-radius: 4px;
    padding: 10px 12px;
    font-size: 14px;
    font-weight: 800;
    text-align: center;
    text-decoration: none !important;
}

.open-link:hover {
    background: #fff1e8;
    color: #111111 !important;
    text-decoration: none !important;
}

.url-missing-button {
    display: inline-block;
    width: 100%;
    box-sizing: border-box;
    background: #eeeeee;
    color: #777777;
    border: 2px solid #cccccc;
    border-radius: 4px;
    padding: 10px 12px;
    font-size: 14px;
    font-weight: 800;
    text-align: center;
}

.site-title {
    font-size: 16px;
    font-weight: 800;
    color: #111111;
    margin-bottom: 4px;
}

.site-meta {
    font-size: 13px;
    color: #777777;
    line-height: 1.6;
}

.note-box {
    background: #fff8ed;
    border: 1px solid #f3c98b;
    padding: 13px 15px;
    margin-top: 16px;
    color: #4a3310;
    font-size: 14px;
}

header[data-testid="stHeader"] {
    display: none;
}

div[data-testid="stToolbar"] {
    display: none;
}

button[kind="header"] {
    display: none;
}

#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}

[data-testid="stDecoration"] {
    display: none;
}

[data-testid="stStatusWidget"] {
    display: none;
}

@media (max-width: 768px) {
    .hero-title {
        font-size: 30px;
    }
}

/* =========================
   Streamlit UI 非表示
========================= */

header[data-testid="stHeader"] {
    display: none;
}

div[data-testid="stToolbar"] {
    display: none;
}

button[kind="header"] {
    display: none;
}

#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}

[data-testid="stDecoration"] {
    display: none;
}

[data-testid="stStatusWidget"] {
    display: none;
}

/* =========================
   Streamlit branding / toolbar 非表示 強化版
========================= */

header,
footer,
#MainMenu {
    display: none !important;
    visibility: hidden !important;
}

[data-testid="stHeader"],
[data-testid="stToolbar"],
[data-testid="stToolbarActions"],
[data-testid="stDecoration"],
[data-testid="stStatusWidget"],
[data-testid="stAppDeployButton"],
[data-testid="stDeployButton"],
[data-testid="stBaseButton-header"],
[data-testid="stMainMenu"],
[data-testid="stBottomBlockContainer"],
[data-testid="stElementToolbar"],
[data-testid="stPoweredBy"],
[data-testid="stAppViewBlockContainer"] > div:first-child:empty {
    display: none !important;
    visibility: hidden !important;
    height: 0 !important;
    min-height: 0 !important;
    max-height: 0 !important;
    overflow: hidden !important;
}

/* Streamlitロゴリンク系 */
a[href*="streamlit.io"],
a[href*="streamlit.app"],
a[aria-label*="Streamlit"],
a[title*="Streamlit"] {
    display: none !important;
    visibility: hidden !important;
}

/* 右下・左下に出る固定ボタン対策 */
div[style*="position: fixed"],
section[style*="position: fixed"] {
    z-index: 0 !important;
}

/* iframe周辺の余白対策 */
.stApp {
    padding-bottom: 0 !important;
}

</style>
"""

render_html(CUSTOM_CSS)


# =========================================================
# 定数
# =========================================================

TOKYO_23KU = [
    "千代田区", "中央区", "港区", "新宿区", "文京区", "台東区",
    "墨田区", "江東区", "品川区", "目黒区", "大田区", "世田谷区",
    "渋谷区", "中野区", "杉並区", "豊島区", "北区", "荒川区",
    "板橋区", "練馬区", "足立区", "葛飾区", "江戸川区",
]

CATEGORY_INFO = {
    "road": {
        "title": "1. 接道・再建築",
        "check_items": [
            "指定道路図",
            "建築基準法上の道路種別",
            "道路台帳",
            "道路幅員",
            "2項道路・狭あい道路",
        ],
    },
    "district_plan": {
        "title": "2. 用途地域・建築条件",
        "check_items": [
            "用途地域",
            "建ぺい率・容積率",
            "防火地域・準防火地域",
            "高度地区",
            "地区計画",
            "景観計画",
        ],
    },
    "hazard": {
        "title": "3. 災害リスク",
        "check_items": [
            "洪水ハザード",
            "内水ハザード",
            "高潮ハザード",
            "土砂災害警戒区域",
            "津波災害警戒区域",
        ],
    },
    "building_guidance": {
        "title": "4. 建築・開発制限",
        "check_items": [
            "建築指導",
            "建築確認",
            "開発許可",
            "日影規制",
            "宅地造成等工事規制区域",
            "造成宅地防災区域",
        ],
    },
}


# =========================================================
# 共通関数
# =========================================================

def load_csv(path: Path) -> pd.DataFrame:
    if not path.exists():
        return pd.DataFrame()

    for enc in ["utf-8-sig", "utf-8", "cp932", "shift_jis"]:
        try:
            return pd.read_csv(path, encoding=enc)
        except Exception:
            continue

    return pd.DataFrame()


def ensure_columns(df: pd.DataFrame, columns: list[str]) -> pd.DataFrame:
    for col in columns:
        if col not in df.columns:
            df[col] = ""
    return df


def detect_municipality(address: str, municipalities: list[str]) -> str:
    address = clean_text(address)

    for municipality in municipalities:
        if municipality and municipality in address:
            return municipality

    for ward in TOKYO_23KU:
        if ward in address:
            return ward

    return ""


def get_prefecture_from_municipality(municipality: str) -> str:
    if municipality in TOKYO_23KU:
        return "東京都"
    return ""


def is_valid_url(url) -> bool:
    url = clean_text(url)
    return url.startswith("http://") or url.startswith("https://")


def detect_file_type(url) -> str:
    url = clean_text(url).lower()

    if ".pdf" in url:
        return "PDF"

    if is_valid_url(url):
        return "Web"

    return "未登録"


def clean_title(title, url) -> str:
    title = clean_text(title)

    bad_titles = [
        "",
        "nan",
        "ページトップ",
        "本文へスキップします。",
        "こちらのページ",
    ]

    if title in bad_titles:
        return "ページタイトル未整理"

    return title


def filter_external_links(
    external_df: pd.DataFrame,
    selected_municipality: str,
    selected_prefecture: str,
    category: str,
) -> pd.DataFrame:
    if external_df.empty:
        return pd.DataFrame()

    df = external_df.copy()

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

    df = ensure_columns(df, required_columns)

    municipality_links = df[
        (df["display_scope"].astype(str).str.strip() == "municipality")
        & (df["municipality"].astype(str).str.strip() == selected_municipality)
        & (df["category"].astype(str).str.strip() == category)
    ].copy()

    prefecture_links = df[
        (df["display_scope"].astype(str).str.strip() == "prefecture")
        & (df["prefecture"].astype(str).str.strip() == selected_prefecture)
        & (df["category"].astype(str).str.strip() == category)
    ].copy()

    all_links = pd.concat(
        [municipality_links, prefecture_links],
        ignore_index=True,
    )

    if all_links.empty:
        return all_links

    all_links["priority"] = pd.to_numeric(
        all_links["priority"],
        errors="coerce",
    ).fillna(999)

    all_links["url_exists"] = all_links["url"].apply(
        lambda x: 1 if is_valid_url(x) else 0
    )

    all_links["subcategory_key"] = (
        all_links["subcategory"].astype(str).str.strip()
    )

    registered_subcategories = set(
        all_links[
            (all_links["url_exists"] == 1)
            & (all_links["subcategory_key"] != "")
        ]["subcategory_key"].tolist()
    )

    all_links = all_links[
        ~(
            (all_links["url_exists"] == 0)
            & (all_links["subcategory_key"].isin(registered_subcategories))
        )
    ].copy()

    all_links = all_links.sort_values(
        by=["url_exists", "priority"],
        ascending=[False, True],
    )

    return all_links


def render_reference_link(
    title: str,
    url: str,
    source_level: str,
    required_status: str,
    memo: str,
    subcategory: str,
):
    title = clean_title(title, url)
    file_type = detect_file_type(url)

    meta_items = []

    if source_level:
        meta_items.append(source_level)

    meta_items.append(file_type)

    meta_text = " / ".join(meta_items)

    render_html('<div class="link-box"></div>')

    col_button, col_info = st.columns([1.25, 4])

    with col_button:
        if is_valid_url(url):
            safe_url = esc(url)
            render_html(
                f'<a class="open-link" href="{safe_url}" target="_blank" rel="noopener noreferrer">公式サイトを確認</a>'
            )
        else:
            render_html(
                '<span class="url-missing-button">URL未登録</span>'
            )

    with col_info:
        render_html(
            f"""
            <div class="site-title">{esc(title)}</div>
            <div class="site-meta">{esc(meta_text)}</div>
            """
        )


def show_internal_links(
    category_df: pd.DataFrame,
    rank_name: str,
    max_count: int,
):
    if category_df.empty:
        return False

    rank_df = category_df[
        category_df["display_rank"].astype(str).str.strip() == rank_name
    ].copy()

    if rank_df.empty:
        return False

    rank_df["score"] = pd.to_numeric(
        rank_df["score"],
        errors="coerce",
    ).fillna(0)

    rank_df = rank_df.sort_values(
        by="score",
        ascending=False,
    ).head(max_count)

    for _, row in rank_df.iterrows():
        render_reference_link(
            title=row.get("title", ""),
            url=row.get("url", ""),
            source_level="区公式",
            required_status="確認候補",
            memo="公式サイト内ページ",
            subcategory="",
        )

    return True


def show_external_links(external_links: pd.DataFrame):
    if external_links.empty:
        return False

    for _, row in external_links.iterrows():
        title = clean_text(row.get("title", ""))
        subcategory = clean_text(row.get("subcategory", ""))
        url = clean_text(row.get("url", ""))
        source_level = clean_text(row.get("source_level", ""))
        required_status = clean_text(row.get("required_status", ""))
        memo = clean_text(row.get("memo", ""))

        display_title = title

        if not display_title:
            display_title = subcategory if subcategory else "確認先"

        render_reference_link(
            title=display_title,
            url=url,
            source_level=source_level,
            required_status=required_status,
            memo=memo,
            subcategory=subcategory,
        )

    return True


# =========================================================
# CSV読み込み
# =========================================================

ranked_df = load_csv(RANKED_CSV)
external_df = load_csv(EXTERNAL_CSV)
external_add_df = load_csv(EXTERNAL_ADD_CSV)

if not external_add_df.empty:
    external_df = pd.concat(
        [external_df, external_add_df],
        ignore_index=True,
    )

ranked_required_columns = [
    "base_municipality",
    "detected_category",
    "display_rank",
    "score",
    "title",
    "url",
]

external_required_columns = [
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

ranked_df = ensure_columns(ranked_df, ranked_required_columns)
external_df = ensure_columns(external_df, external_required_columns)


# =========================================================
# 画面
# =========================================================

render_html("""
<div class="hero">
    <div class="hero-label">FIELD リサーチナビゲーション</div>
    <div class="hero-title">都市計画ナビ β</div>
    <div class="hero-text">
        物件調査で必要な公式確認先を、自治体別に整理する一次調査ナビゲーションツール
    </div>
</div>
""")

if ranked_df.empty:
    st.warning(
        "official_site_links_ranked.csv が読み込めません。"
        "クロール候補なしで、external_reference_links.csv のみ表示します。"
    )

municipalities = sorted(
    list(
        set(TOKYO_23KU)
        | set(ranked_df["base_municipality"].dropna().astype(str).str.strip().tolist())
        | set(external_df["municipality"].dropna().astype(str).str.strip().tolist())
    )
)

municipalities = [m for m in municipalities if m]

render_html('<div class="section-title">住所入力</div>')

address = st.text_input(
    "調査したい住所",
    value="東京都渋谷区渋谷1-1-1",
)

selected_municipality = detect_municipality(address, municipalities)

if not selected_municipality:
    selected_municipality = st.selectbox(
        "自治体を選択してください",
        municipalities,
    )

selected_prefecture = get_prefecture_from_municipality(selected_municipality)

render_html(f"""
<div class="summary-box">
    <b>推定自治体：</b>{esc(selected_municipality)}<br>
    <b>都道府県：</b>{esc(selected_prefecture if selected_prefecture else "未判定")}<br>
    <b>表示内容：</b>公式確認先候補 / 都道府県・国・窓口確認先
</div>
""")

target_df = ranked_df[
    ranked_df["base_municipality"].astype(str).str.strip() == selected_municipality
].copy()

render_html('<div class="section-title">一次調査メニュー</div>')

for category, info in CATEGORY_INFO.items():
    with st.container():
        render_html('<div class="menu-card">')
        render_html(f'<div class="menu-title">{esc(info["title"])}</div>')
        render_html('<div class="mini-heading">確認事項</div>')

        for item in info["check_items"]:
            st.write(f"・{item}")

        render_html('<div class="mini-heading">公式確認先</div>')

        category_df = target_df[
            target_df["detected_category"].astype(str).str.strip() == category
        ].copy()

        external_links = filter_external_links(
            external_df=external_df,
            selected_municipality=selected_municipality,
            selected_prefecture=selected_prefecture,
            category=category,
        )

        shown_any = False

        if show_external_links(external_links):
            shown_any = True

        if not shown_any:
            if show_internal_links(
                category_df=category_df,
                rank_name="優先確認",
                max_count=3,
            ):
                shown_any = True

            if show_internal_links(
                category_df=category_df,
                rank_name="関連確認",
                max_count=2,
            ):
                shown_any = True

        if not shown_any:
            render_reference_link(
                title="確認先未登録",
                url="",
                source_level="未登録",
                required_status="URL未登録",
                memo="external_reference_links.csv または official_site_links_ranked.csv へ登録してください",
                subcategory=category,
            )

        render_html('</div>')

render_html("""
<div class="note-box">
    β版です。表示内容は該当判定ではなく、公式確認先の候補です。
    最終判断は自治体GIS、都道府県サイト、重要事項説明資料、自治体窓口で確認してください。
</div>            
""")

FEEDBACK_FORM_URL = "https://forms.gle/3ymwSTJ3jxo11RkP9"

render_html(f"""
<div class="note-box">
    <b>フィードバックのお願い</b><br>
    表示されている確認先に誤り・不足・追加希望がある場合は、
    下記フォームからお知らせください。<br><br>
    <a class="open-link" href="{FEEDBACK_FORM_URL}" target="_blank" rel="noopener noreferrer">
        フィードバックを送る
    </a>
</div>
""")