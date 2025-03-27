import pandas as pd
import numpy as np
import os
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans

APP_DIR = os.path.dirname(os.path.abspath(__file__))

CSV_PATH = os.path.join(APP_DIR, 'data', 'steam_games.csv')
JSON_PATH = os.path.join(APP_DIR, 'data', 'games.json')

# This function is used to convert the games.json file to a CSV file
# It only runs if the CSV file is missing
def prepare_data_if_missing():
    # Check if the CSV file already exists
    if os.path.exists(CSV_PATH):
        print(f"[INFO] CSV already exists at {CSV_PATH}")
        return

    print("[INFO] CSV not found. Generating from games.json...")
    df = pd.read_json(JSON_PATH)
    df = df.T
    df['AppID'] = df.index

    # Rename columns to match the CSV version
    column_name_dict = {
        "name": "Name",
        "release_date": "Release date",
        "required_age": "Required age",
        "price": "Price",
        "dlc_count": "DLC count",
        "detailed_description": "Detailed description",
        "about_the_game": "About the game",
        "short_description": "Short description",
        "reviews": "Reviews",
        "header_image": "Header image",
        "website": "Website",
        "support_url": "Support url",
        "support_email": "Support email",
        "windows": "Windows",
        "mac": "Mac",
        "linux": "Linux",
        "metacritic_score": "Metacritic score",
        "metacritic_url": "Metacritic url",
        "achievements": "Achievements",
        "recommendations": "Recommendations",
        "notes": "Notes",
        "supported_languages": "Supported languages",
        "full_audio_languages": "Full audio languages",
        "packages": "Packages",
        "developers": "Developers",
        "publishers": "Publishers",
        "categories": "Categories",
        "genres": "Genres",
        "screenshots": "Screenshots",
        "movies": "Movies",
        "user_score": "User score",
        "score_rank": "Score rank",
        "positive": "Positive",
        "negative": "Negative",
        "estimated_owners": "Estimated owners",
        "average_playtime_forever": "Average playtime forever",
        "average_playtime_2weeks": "Average playtime two weeks",
        "median_playtime_forever": "Median playtime forever",
        "median_playtime_2weeks": "Median playtime two weeks",
        "peak_ccu": "Peak CCU",
        "tags": "Tags"
    }
    df.rename(columns=column_name_dict, inplace=True)

    def convert_tags(tags_dict):
        if isinstance(tags_dict, dict):
            return ",".join(tags_dict.keys())
        return np.nan

    def convert_list(items):
        if isinstance(items, list):
            if all(isinstance(i, str) for i in items):
                return ",".join(items)
            return ",".join(str(i) for i in items)
        return np.nan

    for col in df.columns:
        if df[col].apply(lambda x: isinstance(x, dict)).any():
            df[col] = df[col].apply(convert_tags)
        if df[col].apply(lambda x: isinstance(x, list)).any():
            df[col] = df[col].apply(convert_list)

    numeric_cols = [
        "Price", "DLC count", "Achievements", "Recommendations", "Positive", "Negative",
        "Average playtime forever", "Average playtime two weeks",
        "Median playtime forever", "Median playtime two weeks", "Peak CCU"
    ]
    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0).astype(int)

    df = df.reset_index(drop=True)
    df = df[['AppID'] + [col for col in df.columns if col != 'AppID']]
    df.to_csv(CSV_PATH, index=False)
    print(f"[SUCCESS] Cleaned CSV saved to: {CSV_PATH}")

# This function loads the data from the CSV file
def load_data():
    # Generate the CSV file if it doesn't exist by calling the function
    prepare_data_if_missing()
    
    # Load the CSV file
    df = pd.read_csv(CSV_PATH)
    
    # Drop rows with missing data, for now just the average playtime
    df = df.dropna(subset=['Average playtime forever'])
    
    return df.reset_index(drop=True)

# This function extracts features from the data to be used in the model
def extract_features(df):
    df = df.copy()

    # Normalize average playtime
    scaler = StandardScaler()
    df['playtime_scaled'] = scaler.fit_transform(df[['Average playtime forever']])

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
        game_index = df[df['Name'].str.lower() == game_name.lower()].index[0]
    except IndexError:
        return []

    cluster_id = model.predict([features.iloc[game_index]])[0]
    similar_indices = np.where(model.labels_ == cluster_id)[0]
    similar_indices = [i for i in similar_indices if i != game_index]
    recommended_games = df.iloc[similar_indices].sample(n=min(top_n, len(similar_indices)))
    return recommended_games['Name'].tolist()
