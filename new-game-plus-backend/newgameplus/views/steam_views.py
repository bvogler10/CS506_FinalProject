import pandas as pd
import numpy as np
import requests
from django.http import JsonResponse
from django.conf import settings
from rest_framework.decorators import api_view
from ..recommender import load_clustered_data, load_clustered_metadata

clustered_df = load_clustered_data()
metadata_df = load_clustered_metadata()


excluded = {'appid','price','peak_ccu','windows','mac','linux','genre_cluster','price_cluster','ccu_cluster','categories_cluster'}
genre_cols = [
    col for col in clustered_df.columns
    if col not in excluded and clustered_df[col].dtype == 'int64' and clustered_df[col].nunique() == 2
]

STEAM_API_BASE_URL = "https://api.steampowered.com"
STEAM_API_KEY = settings.STEAM_API_KEY
CLUSTER_COLS = ['genre_cluster', 'categories_cluster', 'price_cluster', 'ccu_cluster', 'all_cluster']

@api_view(['GET'])
def get_owned_games(request):
    """
    Get a user's owned games plus enriched metadata from the Steam Store API.
    Example usage: /steam/get_owned_games/?steamid=12345678901234567
    """
    steamid = request.GET.get('steamid')
    if not steamid:
        return JsonResponse({'error': 'Missing steamid parameter'}, status=400)

    url = f"{STEAM_API_BASE_URL}/IPlayerService/GetOwnedGames/v0001/"
    params = {
        'key': STEAM_API_KEY,
        'steamid': steamid,
        'include_appinfo': True,
        'include_played_free_games': True
    }

    try:
        response = requests.get(url, params=params)
        data = response.json()

        if "games" not in data.get("response", {}):
            return JsonResponse({"error": "No games found or profile is private."}, status=404)

        games = data["response"]["games"]
        # Sort by playtime and limit to top 15
        top_games = sorted(games, key=lambda g: g["playtime_forever"], reverse=True)[:15]

        enriched_games = []
        for game in top_games:
            metadata = fetch_game_metadata(game["appid"])
            if metadata:
                enriched_game = {
                    **metadata,
                    "playtime_forever": game.get("playtime_forever", 0),
                    "img_icon_url": game.get("img_icon_url")
                }
                enriched_games.append(enriched_game)

        return JsonResponse({"games": enriched_games})

    except requests.exceptions.RequestException as e:
        return JsonResponse({'error': str(e)}, status=500)

def weighted_cosine(u, v, w):
    uw = u * w
    vw = v * w
    return uw.dot(vw) / (np.linalg.norm(uw) * np.linalg.norm(vw) + 1e-8)

def append_normalized_clusters(df, user, cols):
    for col in cols:
        max_val = df[col].max()
        df[col] = df[col] / max_val
        user_val = user.get(col, 0) / max_val
        yield user_val

@api_view(['GET'])
def recommend_games(request):
    steamid = request.GET.get('steamid')
    if not steamid:
        return JsonResponse({'error':'steamid missing'}, status=400)

    # 1) fetch & enrich the user's top game
    # game_ids = [  # demo, replace with real top-N
    #     1818750,
    #     383980,
    #     2217000,
    #     291550
    # ]
    user_games_url = f"{STEAM_API_BASE_URL}/IPlayerService/GetOwnedGames/v0001/"
    params = {
        'key': STEAM_API_KEY,
        'steamid': steamid,
        'include_appinfo': True,
        'include_played_free_games': True
    }
    response = requests.get(user_games_url, params=params)
    games = response.json().get("response", {}).get("games", [])
    top_games = sorted(games, key=lambda g: g["playtime_forever"], reverse=True)[:15]
    game_ids = [g["appid"] for g in top_games]
    enriched = []
    for appid in game_ids:
        m = fetch_game_metadata(appid)
        if m:
            # fill in CCU from your clustered_df
            row = clustered_df.loc[clustered_df.appid==appid, 'peak_ccu']
            m['peak_ccu'] = int(row.iloc[0]) if not row.empty else 1
            enriched.append(m)
    if not enriched:
        return JsonResponse({'error':'no metadata'}, status=500)

    # 2) build user profile vector
    def make_vec(game):
        row = clustered_df[clustered_df.appid == game['appid']]
        genre_vector = row[genre_cols].iloc[0].values if not row.empty else [0] * len(genre_cols)
        return np.array([game['price'], game['peak_ccu'], *genre_vector], dtype=float)

    user_vecs = np.vstack([make_vec(g) for g in enriched])
    user_profile = user_vecs.mean(axis=0)

    # 3) build comparison matrix
    comp = clustered_df[['appid','price','peak_ccu'] + genre_cols + ['genre_cluster', 'price_cluster', 'ccu_cluster', 'all_cluster']].copy()
    comp = clustered_df[
        (clustered_df['peak_ccu'] >= 500) &
        (clustered_df['price'] >= 2.99)
    ][['appid','price','peak_ccu'] + genre_cols + CLUSTER_COLS].copy()
    M = comp[['price','peak_ccu'] + genre_cols + CLUSTER_COLS].to_numpy(dtype=float)


    # 4) normalize numeric columns in M & user_profile
    def normalize_column(col, values, user_val, transform=None):
        if transform:
            values = transform(values)
            user_val = transform(user_val)
        mean, std = values.mean(), values.std()
        return (values - mean) / (std + 1e-8), (user_val - mean) / (std + 1e-8)

    M[:,0], user_profile[0] = normalize_column(M[:,0], M[:,0], user_profile[0])
    M[:,1], user_profile[1] = normalize_column(M[:,1], M[:,1], user_profile[1], transform=np.log1p)
    
    user_profile = np.append(user_profile, list(append_normalized_clusters(comp, enriched[0], CLUSTER_COLS)))

    # 5) build weight vector: [price, CCU, *genres] + [genre_cluster, price_cluster, ccu_cluster, all_cluster]
    w = np.array([0.5, 1.5] + [2.5]*len(genre_cols) + [1.0, 1.0, 0.5, 0.5, 1.0])

    # 6) compute weighted cosine similarities
    sims = np.array([weighted_cosine(user_profile, row, w) for row in M])

    comp['similarity'] = sims * np.log1p(comp['peak_ccu'])
    comp = comp[~comp.appid.isin(game_ids)]
    top = comp.nlargest(15,'similarity')

    # Merge with metadata
    top_merged = top.merge(metadata_df, on='appid', how='left')

    # Pick frontend-friendly fields
    frontend_fields = ['appid', 'name', 'header_image', 'short_description', 'price', 'peak_ccu', 'similarity']

    # Create the response and add the store link
    recommendations = []
    for _, row in top_merged[frontend_fields].iterrows():
        game = row.to_dict()
        game['store_url'] = f"https://store.steampowered.com/app/{game['appid']}"
        recommendations.append(game)

    # Return frontend data
    return JsonResponse({
        'recommendations': recommendations
    })

def fetch_game_metadata(appid):
    url = f"https://store.steampowered.com/api/appdetails?appids={appid}"
    try:
        r = requests.get(url).json()
        data = r.get(str(appid),{}).get('data',{})
        return {
            'appid': data.get('steam_appid'),
            'genres': [g['description'] for g in data.get('genres',[])],
            'price': data.get('price_overview',{}).get('final',0)/100
        }
    except:
        return None
