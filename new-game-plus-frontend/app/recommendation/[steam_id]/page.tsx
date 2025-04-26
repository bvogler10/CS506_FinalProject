"use client";

import RecommendationAPI from "@/api/RecommendationAPI";
import { GameCard } from "@/components/pages/recommendation/game-card";
import { useParams } from "next/navigation";
import { useEffect, useState } from "react";

export default function RecommendationsPage() {
  const { steam_id } = useParams();
  const [recommendations, setRecommendations] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchRecommendations = async () => {
      if (typeof steam_id !== "string") return;

      try {
        const data = await RecommendationAPI.getRecommendations(steam_id);
        setRecommendations(data);
      } catch (error) {
        console.error("Error fetching recommendations:", error);
        setError("Failed to load recommendations. Error: " + error);
      } finally {
        setLoading(false);
      }
    };

    fetchRecommendations();
  }, [steam_id]);

  return (
    <div className="min-h-screen bg-gray-950 text-gray-50 flex flex-col">
      <main className="container mx-auto px-4 py-8 flex-1">
        <div className="mb-8 text-center">
          <h2 className="text-xl font-semibold mb-2">
            Personalized Recommendations for Steam ID: {steam_id}
          </h2>
          <p className="text-gray-400">
            Based on your gaming history, we think you'll love these titles.
            Games are ranked by similarity to your preferences.
          </p>
        </div>

        {loading ? (
          <div className="flex flex-col items-center justify-center mt-20">
            <div className="w-12 h-12 border-4 border-primary border-t-transparent rounded-full animate-spin"></div>
            <p className="mt-4 text-gray-400 text-lg">
              Loading recommendations...
            </p>
          </div>
        ) : error ? (
          <div className="flex flex-col items-center justify-center mt-20">
            <p className="text-red-400 text-lg">{error}</p>
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
            {recommendations.map((game) => (
              <GameCard key={game.appid} game={game} />
            ))}
          </div>
        )}
      </main>
    </div>
  );
}
