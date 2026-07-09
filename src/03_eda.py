import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]

DATA_PATH = PROJECT_ROOT / "data" / "clean_recipes.csv"
IMAGES_DIR = PROJECT_ROOT / "images"
IMAGES_DIR.mkdir(exist_ok=True)

PASTEL_PINK = "#F8BBD0"
DARK_PINK = "#C2185B"
LIGHT_PURPLE = "#D7BDE2"


def save_plot(filename: str) -> None:
    plt.tight_layout()
    plt.savefig(IMAGES_DIR / filename, dpi=300, bbox_inches="tight")
    plt.close()


if __name__ == "__main__":
    df = pd.read_csv(DATA_PATH)

    print("Dataset shape:")
    print(df.shape)

    print("\nFirst rows:")
    print(df[["name", "ingredients", "steps"]].head())

    df["ingredients_length"] = df["ingredients"].astype(str).apply(len)
    df["steps_length"] = df["steps"].astype(str).apply(len)
    df["name_length"] = df["name"].astype(str).apply(len)
    df["number_of_ingredients"] = df["ingredients"].astype(str).apply(lambda x: len(x.split()))

    print("\nText length statistics:")
    print(df[["ingredients_length", "steps_length", "name_length", "number_of_ingredients"]].describe())

    plt.figure(figsize=(8, 5))
    sns.histplot(
        df["ingredients_length"],
        bins=40,
        color=PASTEL_PINK
    )
    plt.title("Distribution of Ingredients Text Length")
    plt.xlabel("Ingredients text length")
    plt.ylabel("Number of recipes")
    save_plot("01_ingredients_length_distribution.png")

    plt.figure(figsize=(8, 5))
    sns.histplot(
        df["steps_length"],
        bins=40,
        color=LIGHT_PURPLE
    )
    plt.title("Distribution of Recipe Steps Length")
    plt.xlabel("Steps text length")
    plt.ylabel("Number of recipes")
    save_plot("02_steps_length_distribution.png")

    plt.figure(figsize=(8, 5))
    sns.histplot(
        df["number_of_ingredients"],
        bins=40,
        color=PASTEL_PINK
    )
    plt.title("Distribution of Number of Ingredients")
    plt.xlabel("Number of ingredient words")
    plt.ylabel("Number of recipes")
    save_plot("03_number_of_ingredients_distribution.png")

    tags_series = (
        df["tags"]
        .astype(str)
        .str.replace("[", " ", regex=False)
        .str.replace("]", " ", regex=False)
        .str.replace("'", " ", regex=False)
        .str.replace(",", " ", regex=False)
        .str.split()
        .explode()
    )

    top_tags = tags_series.value_counts().head(10)

    plt.figure(figsize=(9, 5))
    sns.barplot(
        x=top_tags.values,
        y=top_tags.index,
        color=DARK_PINK
    )
    plt.title("Top 10 Most Common Recipe Tags")
    plt.xlabel("Count")
    plt.ylabel("Tag")
    save_plot("04_top_recipe_tags.png")

    print("\nEDA completed. Plots saved in images folder.")