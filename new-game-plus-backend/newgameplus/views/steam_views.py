import pandas as pd
import numpy as np
import requests
from django.http import JsonResponse
from django.conf import settings
from rest_framework.decorators import api_view
from ..recommender import load_clustered_data

clustered_df = load_clustered_data()
excluded = {'appid','price','peak_ccu','windows','mac','linux','genre_cluster','price_cluster','ccu_cluster'}
genre_cols = [c for c in clustered_df.columns 
              if c not in excluded 
              and clustered_df[c].nunique()==2 
              and clustered_df[c].dtype=='int64']

STEAM_API_BASE_URL = "https://api.steampowered.com"
STEAM_API_KEY      = settings.STEAM_API_KEY

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

@api_view(['GET'])
def recommend_games(request):
    # steamid = request.GET.get('steamid')
    # if not steamid:
    #     return JsonResponse({'error':'steamid missing'}, status=400)

    # 1) fetch & enrich the user's top game
    user_ids = [  # demo, replace with real top-N
        1145360,
        367520,
        250900
    ]
    enriched = []
    for appid in user_ids:
        m = fetch_game_metadata(appid)
        if m:
            # fill in CCU from your clustered_df
            row = clustered_df.loc[clustered_df.appid==appid, 'peak_ccu']
            m['peak_ccu'] = int(row.iloc[0]) if not row.empty else 1
            enriched.append(m)
    if not enriched:
        return JsonResponse({'error':'no metadata'}, status=500)

    # 2) build user profile vector
    def make_vec(g):
        v = []
        # price, normalized later
        v.append(g['price'])
        # ccu, normalized later
        v.append(g['peak_ccu'])
        # genres
        for col in genre_cols:
            v.append(1 if col in g['genres'] else 0)
        return np.array(v, dtype=float)

    user_vecs = np.vstack([make_vec(g) for g in enriched])
    user_profile = user_vecs.mean(axis=0)

    # 3) build comparison matrix
    comp = clustered_df[['appid','price','peak_ccu'] + genre_cols].copy()
    comp = comp[comp.peak_ccu >= 100]  # filter
    M = comp[['price','peak_ccu'] + genre_cols].to_numpy(dtype=float)

    # 4) normalize numeric columns in M & user_profile
    #    price
    pr_mean, pr_std = M[:,0].mean(), M[:,0].std()
    M[:,0] = (M[:,0] - pr_mean)/ (pr_std+1e-8)
    user_profile[0] = (user_profile[0] - pr_mean)/(pr_std+1e-8)
    #    peak_ccu (log then norm)
    M[:,1] = np.log1p(M[:,1])
    cc_mean, cc_std = M[:,1].mean(), M[:,1].std()
    M[:,1] = (M[:,1] - cc_mean)/(cc_std+1e-8)
    user_profile[1] = (np.log1p(user_profile[1]) - cc_mean)/(cc_std+1e-8)

    # 5) build weight vector: [price, CCU, *genres]
    w = np.array([0.4, 0.4] + [5.0]*len(genre_cols))

    # 6) compute weighted cosine similarities
    sims = np.array([weighted_cosine(user_profile, row, w) for row in M])

    comp['similarity'] = sims
    comp = comp[~comp.appid.isin(user_ids)]
    top = comp.nlargest(15,'similarity')

    return JsonResponse({'recommendations':
        top[['appid','price','peak_ccu','similarity']].to_dict(orient='records')
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
