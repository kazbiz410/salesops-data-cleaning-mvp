import pandas as pd
import re
import unicodedata

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

df = pd.read_csv("data/raw_companies.csv")
df["normalized_company_name"] = df["company_name"].apply(normalize_company_name)

grouped = (
    df.groupby("normalized_company_name")["company_name"]
    .apply(list)
    .reset_index(name="original_names")
)

print(grouped)
