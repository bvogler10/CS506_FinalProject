"use client";

import { useState } from "react";
import Image from "next/image";
import { Card, CardContent, CardFooter } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Users, ExternalLink } from "lucide-react";
import { formatNumber } from "@/lib/utils";
import { SimilarityMeter } from "@/components/pages/recommendation/similarity-meter";

interface Game {
  appid: number;
  name: string;
  header_image: string;
  short_description: string;
  price: string;
  peak_ccu: number;
  similarity: number;
  store_url: string;
}

interface GameCardProps {
  game: Game;
}

export function GameCard({ game }: GameCardProps) {
  const [isHovered, setIsHovered] = useState(false);

  const handleClick = () => {
    window.open(game.store_url, "_blank", "noopener,noreferrer");
  };

  return (
    <Card
      className={`bg-gray-800 border-gray-700 overflow-hidden transition-all duration-300 h-full flex flex-col ${
        isHovered ? "transform scale-[1.02] shadow-xl shadow-primary/20" : ""
      } cursor-pointer`}
      onClick={handleClick}
      onMouseEnter={() => setIsHovered(true)}
      onMouseLeave={() => setIsHovered(false)}
    >
      <div className="relative aspect-[460/215] w-full overflow-hidden">
        <img
          src={game.header_image}
          alt={game.name}
          className="object-cover transition-transform duration-500"
          style={{
            transform: isHovered ? "scale(1.05)" : "scale(1)",
          }}
        />
        <div className="absolute top-2 right-2">
          <Badge
            variant="secondary"
            className="bg-gray-900/80 text-white border-none"
          >
            ${game.price}
          </Badge>
        </div>
      </div>

      <CardContent className="p-4 flex-grow">
        <h3 className="font-bold text-lg mb-2 line-clamp-1">{game.name}</h3>
        <p className="text-gray-300 text-sm line-clamp-3 mb-4">
          {game.short_description}
        </p>

        <div className="flex items-center gap-2 text-gray-400 text-sm mb-3">
          <Users className="h-4 w-4" />
          <span>Peak Players: {formatNumber(game.peak_ccu)}</span>
        </div>

        <div className="mt-2">
          <SimilarityMeter similarity={game.similarity} />
        </div>
      </CardContent>

      <CardFooter className="p-4 pt-0 border-t border-gray-700 mt-auto">
        <div className="w-full flex justify-between items-center">
          <span className="text-xs text-gray-500">App ID: {game.appid}</span>
          <div className="flex items-center gap-1 text-accent text-sm">
            <span>View on Steam</span>
            <ExternalLink className="h-3 w-3" />
          </div>
        </div>
      </CardFooter>
    </Card>
  );
}
