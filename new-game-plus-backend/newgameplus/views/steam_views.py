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
    Get the list of games owned by a user by their Steam ID.
    Example usage:
    /steam/get_owned_games/?steamid=76561198133696370
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
        return JsonResponse(data)
    except requests.exceptions.RequestException as e:
        return JsonResponse({'error': str(e)}, status=500)
