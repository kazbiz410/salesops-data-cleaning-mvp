import pandas as pd

df = pd.read_csv("data/raw_companies.csv")
print(df)
print("\n--- columns ---")
print(df.columns.tolist())
print("\n--- shape ---")
print(df.shape)
