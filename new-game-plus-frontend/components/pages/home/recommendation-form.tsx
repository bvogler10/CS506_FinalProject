"use client";

import type React from "react";

import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { ArrowRight } from "lucide-react";

export default function RecommendationForm() {
  const [steamId, setSteamId] = useState("");
  const [isLoading, setIsLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!steamId.trim()) return;

    setIsLoading(true);
    // Here you would typically make an API call to your backend
    // For demo purposes, we're just simulating a delay
    setTimeout(() => {
      setIsLoading(false);
      // Redirect or show results
      alert(`Getting recommendations for Steam ID: ${steamId}`);
    }, 1500);
  };

  return (
    <form onSubmit={handleSubmit} className="flex flex-col gap-4">
      <div className="relative">
        <Input
          type="text"
          placeholder="Enter your Steam ID"
          value={steamId}
          onChange={(e) => setSteamId(e.target.value)}
          className="text-white placeholder:text-gray-500 h-12 pr-24"
        />
        <Button
          type="submit"
          disabled={isLoading || !steamId.trim()}
          className="absolute right-1 top-1 h-10 cursor-pointer"
        >
          {isLoading ? (
            <div className="h-5 w-5 animate-spin rounded-full border-2 border-white border-t-transparent" />
          ) : (
            <>
              Go <ArrowRight className="ml-2 h-4 w-4" />
            </>
          )}
        </Button>
      </div>
      <p className="text-sm text-gray-400">
        Don't know your Steam ID?{" "}
        <a href="#find-id" className="text-secondary hover:underline">
          Learn how to find it
        </a>
      </p>
    </form>
  );
}
