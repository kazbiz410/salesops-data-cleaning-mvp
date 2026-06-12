import pandas as pd
import re
import unicodedata
import streamlit as st

st.set_page_config(page_title="SalesOps Data Cleaning MVP", layout="wide")
st.title("SalesOps Data Cleaning MVP")
st.write("CSVの表記ゆれを整えて、クレンジング結果を確認する最小MVPです。")

def normalize_company_name(name: str) -> str:
    if pd.isna(name):
        return ""

    text = str(name)
    text = text.strip()
    text = unicodedata.normalize("NFKC", text)
    text = text.lower()
    text = text.replace("(株)", "株式会社")
    text = text.replace("㈱", "株式会社")
    text = re.sub(r"[.,]", "", text)
    text = re.sub(r"\s+", " ", text).strip()

    if text.endswith("株式会社") and not text.startswith("株式会社"):
        text = "株式会社" + text[:-4]

    return text

uploaded_file = st.file_uploader(
    "CSVファイルをアップロードしてください",
    type=["csv"]
)

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    st.subheader("元データ")
    st.dataframe(df, use_container_width=True)

    if "company_name" in df.columns:
        df["normalized_company_name"] = df["company_name"].apply(normalize_company_name)

        st.subheader("クレンジング結果")
        st.dataframe(df, use_container_width=True)

        grouped = (
            df.groupby("normalized_company_name")["company_name"]
            .apply(list)
            .reset_index(name="original_names")
        )

        st.subheader("名寄せ候補")
        st.dataframe(grouped, use_container_width=True)

        csv_data = df.to_csv(index=False).encode("utf-8-sig")
        st.download_button(
            label="クレンジング済みCSVをダウンロード",
            data=csv_data,
            file_name="cleaned_companies.csv",
            mime="text/csv",
        )
    else:
        st.error("company_name 列が見つかりません。")
else:
    st.info("まずはCSVファイルをアップロードしてください。")
