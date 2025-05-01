import pandas as pd
import os
import kagglehub
from kagglehub import KaggleDatasetAdapter

APP_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_PATH = os.path.join(APP_DIR, 'data', 'games.csv')
CLUSTERED_MODEL_PICKLE_PATH = os.path.join(APP_DIR, "data", "clustered_steam_data.pkl")

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
def load_raw_data():
    # Generate the CSV file if it doesn't exist by calling the function
    prepare_data_if_missing()
    
    # Load the CSV filee
    df = pd.read_csv(CSV_PATH)
    
    return df.reset_index(drop=True)

def load_clustered_data():
    if not os.path.exists(CLUSTERED_MODEL_PICKLE_PATH):
        raise FileNotFoundError(f"Missing clustered data at: {CLUSTERED_MODEL_PICKLE_PATH}")
    return pd.read_pickle(CLUSTERED_MODEL_PICKLE_PATH)

def load_clustered_metadata():
    return pd.read_pickle(os.path.join(APP_DIR, "data", "clustered_steam_metadata.pkl"))
