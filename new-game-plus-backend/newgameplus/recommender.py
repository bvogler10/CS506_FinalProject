import pandas as pd
import numpy as np
import os
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
import kagglehub
from kagglehub import KaggleDatasetAdapter

APP_DIR = os.path.dirname(os.path.abspath(__file__))

CSV_PATH = os.path.join(APP_DIR, 'data', 'games.csv')

# This function is used to convert the games.json file to a CSV file
# It only runs if the CSV file is missing
def prepare_data_if_missing():
    if os.path.exists(CSV_PATH):
        print(f"[INFO] CSV already exists at {CSV_PATH}")
        return

    print("[INFO] CSV not found. Downloading from KaggleHub...")
    os.makedirs(os.path.dirname(CSV_PATH), exist_ok=True)
    
    # Replace this with the actual path to the CSV inside the dataset
    file_path = "games_march2025_full.csv"  # <-- Update based on actual dataset structure
    
    df = kagglehub.load_dataset(
        KaggleDatasetAdapter.PANDAS,
        "artermiloff/steam-games-dataset",
        file_path
    )

    df.to_csv(CSV_PATH, index=False)
    print(f"[SUCCESS] CSV downloaded and saved to: {CSV_PATH}")

# This function loads the data from the CSV file
def load_data():
    # Generate the CSV file if it doesn't exist by calling the function
    prepare_data_if_missing()
    
    # Load the CSV file
    df = pd.read_csv(CSV_PATH)
    
    # Drop rows with missing data, for now just the average playtime
    df = df.dropna(subset=['average_playtime_forever'])
    
    return df.reset_index(drop=True)

# This function extracts features from the data to be used in the model
def extract_features(df):
    df = df.copy()

    # Normalize average playtime
    scaler = StandardScaler()
    df['playtime_scaled'] = scaler.fit_transform(df[['average_playtime_forever']])

    # Add more features here: price, genre, tags, etc.
    # For now we just use playtime
    features = df[['playtime_scaled']]

    return features

# This function trains the model by using KMeans++ clustering
def train_model(features, k=10):
    # Train the model using KMeans++
    model = KMeans(n_clusters=k, init='k-means++', random_state=42)
    model.fit(features)
    
    return model

# This function gets recommendations for a given game using the model trained
def get_recommendations(game_name, df, features, model, top_n=5):
    try:
        game_index = df[df['name'].str.lower() == game_name.lower()].index[0]
    except IndexError:
        return []

    cluster_id = model.predict([features.iloc[game_index]])[0]
    similar_indices = np.where(model.labels_ == cluster_id)[0]
    similar_indices = [i for i in similar_indices if i != game_index]
    recommended_games = df.iloc[similar_indices].sample(n=min(top_n, len(similar_indices)))
    return recommended_games['name'].tolist()
