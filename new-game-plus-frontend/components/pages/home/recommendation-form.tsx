"use client";

import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { ArrowRight } from "lucide-react";
import { useRouter } from "next/navigation";

export default function RecommendationForm() {
  const [steamId, setSteamId] = useState("");
  const router = useRouter();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!steamId.trim()) return;

    e.preventDefault();
    if (steamId.trim()) {
      router.push(`/recommendations/${steamId}`);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="flex flex-col gap-4">
      <div className="relative">
        <Input
          type="text"
          placeholder="Enter your Steam ID..."
          value={steamId}
          onChange={(e) => setSteamId(e.target.value)}
          className="h-12 pr-24"
        />
        <Button
          type="submit"
          className="absolute right-1 top-1 h-10 cursor-pointer"
        >
          Go <ArrowRight className="ml-2 h-4 w-4" />
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
