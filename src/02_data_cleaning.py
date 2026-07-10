import pandas as pd
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]

RAW_DATA_PATH = PROJECT_ROOT / "data" / "recipes.csv"
CLEAN_DATA_PATH = PROJECT_ROOT / "data" / "clean_recipes.csv"

SAMPLE_SIZE = 20000
RANDOM_STATE = 42


def clean_text(text):
    if pd.isna(text):
        return ""

    text = str(text).lower()
    text = text.replace("\n", " ")
    text = text.replace("\r", " ")
    text = text.replace("[", " ")
    text = text.replace("]", " ")
    text = text.replace("'", " ")
    text = text.replace('"', " ")
    text = text.replace(",", " ")

    return text.strip()


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    selected_columns = [
        "id",
        "name",
        "description",
        "ingredients",
        "ingredients_raw",
        "steps",
        "servings",
        "serving_size",
        "tags"
    ]

    df = df[selected_columns]

    df = df.drop_duplicates()
    df = df.dropna(subset=["name", "ingredients", "steps"])

    if len(df) > SAMPLE_SIZE:
        df = df.sample(n=SAMPLE_SIZE, random_state=RANDOM_STATE)

    df["name"] = df["name"].astype(str).str.strip()
    df["description"] = df["description"].apply(clean_text)
    df["ingredients"] = df["ingredients"].apply(clean_text)
    df["ingredients_raw"] = df["ingredients_raw"].apply(clean_text)
    df["steps"] = df["steps"].apply(clean_text)
    df["tags"] = df["tags"].apply(clean_text)

    df = df[df["name"] != ""]
    df = df[df["ingredients"] != ""]
    df = df[df["steps"] != ""]

    df["combined_text"] = (
        df["name"].str.lower()
        + " "
        + df["description"]
        + " "
        + df["ingredients"]
        + " "
        + df["steps"]
        + " "
        + df["tags"]
    )

    df = df.reset_index(drop=True)

    return df


if __name__ == "__main__":
    df = pd.read_csv(RAW_DATA_PATH)

    print("Initial shape:")
    print(df.shape)

    print("\nMissing values before cleaning:")
    print(df.isnull().sum())

    clean_df = clean_data(df)

    print("\nClean shape:")
    print(clean_df.shape)

    print("\nMissing values after cleaning:")
    print(clean_df.isnull().sum())

    print("\nFirst 5 cleaned rows:")
    print(clean_df[["name", "ingredients", "steps"]].head())

    clean_df.to_csv(CLEAN_DATA_PATH, index=False)
