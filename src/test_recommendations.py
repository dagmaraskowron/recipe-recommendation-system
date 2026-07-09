from pathlib import Path
import pandas as pd

from recommendation_system import (
    load_clean_data,
    build_tfidf_matrix,
    recommend_recipes
)


PROJECT_ROOT = Path(__file__).resolve().parents[1]
RESULTS_PATH = PROJECT_ROOT / "recommendation_examples.csv"


if __name__ == "__main__":
    df = load_clean_data()
    tfidf_matrix = build_tfidf_matrix(df)

    example_recipes = [
        "Chocolate Pie",
        "Chicken Soup",
        "Banana Bread"
    ]

    all_results = []

    for recipe in example_recipes:
        print(f"\nRecommendations for: {recipe}")
        print("-" * 50)

        recommendations = recommend_recipes(
            recipe_title=recipe,
            df=df,
            tfidf_matrix=tfidf_matrix,
            top_n=5
        )

        if recommendations.empty:
            print("No recommendations found.")
            continue

        print(recommendations[["name", "similarity_score"]])

        recommendations["input_recipe"] = recipe
        all_results.append(recommendations)

    if all_results:
        results_df = pd.concat(all_results, ignore_index=True)
        results_df.to_csv(RESULTS_PATH, index=False)

        print(f"\nRecommendation examples saved to: {RESULTS_PATH}")