import pandas as pd
from pathlib import Path

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = PROJECT_ROOT / "data" / "clean_recipes.csv"


def load_clean_data() -> pd.DataFrame:
    return pd.read_csv(DATA_PATH)


def build_tfidf_matrix(df: pd.DataFrame):
    vectorizer = TfidfVectorizer(
        stop_words="english",
        max_features=5000
    )

    tfidf_matrix = vectorizer.fit_transform(df["combined_text"])

    return tfidf_matrix


def recommend_recipes(recipe_title: str, df: pd.DataFrame, tfidf_matrix, top_n: int = 5) -> pd.DataFrame:
    recipe_title = recipe_title.lower()

    matching_recipes = df[
        df["name"].str.lower().str.contains(recipe_title, na=False)
    ]

    if matching_recipes.empty:
        print(f"No recipe found for: {recipe_title}")
        return pd.DataFrame()

    recipe_index = matching_recipes.index[0]

    similarity_scores = cosine_similarity(
        tfidf_matrix[recipe_index],
        tfidf_matrix
    ).flatten()

    similar_indices = similarity_scores.argsort()[::-1][1:top_n + 1]

    recommendations = df.iloc[similar_indices][
        ["name", "ingredients", "description"]
    ].copy()

    recommendations["similarity_score"] = similarity_scores[similar_indices]

    return recommendations.sort_values(by="similarity_score", ascending=False)


if __name__ == "__main__":
    df = load_clean_data()

    print("Dataset shape:")
    print(df.shape)

    print("\nBuilding TF-IDF matrix...")
    tfidf_matrix = build_tfidf_matrix(df)

    example_recipe = df.iloc[0]["name"]

    print("\nSelected recipe:")
    print(example_recipe)

    print("\nRecommended recipes:")
    recommendations = recommend_recipes(
        recipe_title=example_recipe,
        df=df,
        tfidf_matrix=tfidf_matrix,
        top_n=5
    )

    print(recommendations[["name", "similarity_score"]])