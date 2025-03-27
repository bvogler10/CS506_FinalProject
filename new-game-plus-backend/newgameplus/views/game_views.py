from django.http import JsonResponse
from ..recommender import load_data, extract_features, train_model, get_recommendations

df = load_data()
features = extract_features(df)
model = train_model(features)

# Recommends games based on the hardcoded game
def recommend_games(request):
    print('Recommending games')
    results = get_recommendations("Terraria", df, features, model) # Hardcoded game for now for testing
    print('Results:', results)
    return JsonResponse({'recommendations': results})
