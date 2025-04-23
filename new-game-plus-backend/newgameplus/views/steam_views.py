import requests
from django.http import JsonResponse
from django.conf import settings
from rest_framework.decorators import api_view

# Base Steam API config
STEAM_API_BASE_URL = "https://api.steampowered.com"
STEAM_API_KEY = settings.STEAM_API_KEY

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

def fetch_game_metadata(appid):
    """
    Fetch specific metadata from the Steam Store API for a given appid.
    """
    url = f"https://store.steampowered.com/api/appdetails?appids={appid}"
    try:
        response = requests.get(url)
        data = response.json()
        if data[str(appid)]["success"]:
            game_data = data[str(appid)]["data"]
            return {
                "appid": game_data.get("steam_appid"),
                "name": game_data.get("name"),
                "genres": [g["description"] for g in game_data.get("genres", [])],
                "categories": [c["description"] for c in game_data.get("categories", [])],
                "platforms": game_data.get("platforms", {}),
                "price": game_data.get("price_overview", {}).get("final") / 100 if game_data.get("price_overview") else 0,
            }
    except Exception as e:
        print(f"Error fetching metadata for {appid}: {e}")
    return None