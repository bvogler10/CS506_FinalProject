import pandas as pd
import numpy as np
import os
import kagglehub
from kagglehub import KaggleDatasetAdapter

APP_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_PATH = os.path.join(APP_DIR, 'data', 'games.csv')

# This function prepares the data by downloading the CSV file from KaggleHub if it doesn't exist
def prepare_data_if_missing():
    if os.path.exists(CSV_PATH):
        print(f"[INFO] CSV already exists at {CSV_PATH}")
        return

    print("[INFO] CSV not found. Downloading from KaggleHub...")
    os.makedirs(os.path.dirname(CSV_PATH), exist_ok=True)
    
    # Define the file name for the dataset
    file_name = "games_march2025_full.csv"
    
    # Download the dataset from KaggleHub
    df = kagglehub.load_dataset(
        KaggleDatasetAdapter.PANDAS,
        "artermiloff/steam-games-dataset",
        file_name
    )

    df.to_csv(CSV_PATH, index=False)
    print(f"[SUCCESS] CSV downloaded and saved to: {CSV_PATH}")

# This function loads the data from the CSV file
def load_data():
    # Generate the CSV file if it doesn't exist by calling the function
    prepare_data_if_missing()
    
    # Load the CSV file
    df = pd.read_csv(CSV_PATH)
    
    return df.reset_index(drop=True)

# This function gets recommendations for a given game using the model trained
# def get_recommendations(game_name, df, features, model, top_n=5):
#     try:
#         game_index = df[df['name'].str.lower() == game_name.lower()].index[0]
#     except IndexError:
#         return []

#     cluster_id = model.predict([features.iloc[game_index]])[0]
#     similar_indices = np.where(model.labels_ == cluster_id)[0]
#     similar_indices = [i for i in similar_indices if i != game_index]
#     recommended_games = df.iloc[similar_indices].sample(n=min(top_n, len(similar_indices)))
#     return recommended_games['name'].tolist()
