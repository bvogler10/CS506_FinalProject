const RecommendationAPI = {
    /**
     * Fetches a list of recommended games from the server.
     */
    getRecommendations: async (steamId: string) => {
        const response = await fetch(`http://127.0.0.1:8000/steam/recommend_games/?steamid=${steamId}`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
            },
        });

        if (!response.ok) {
            throw new Error(response.statusText);
        }
        
        const data = await response.json();

        // Return data.recommendations as that's what the server sends
        return data.recommendations;
    }
}

export default RecommendationAPI;