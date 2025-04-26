"use client";

import { useState, FormEvent } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";
import { GamepadIcon, Search } from "lucide-react";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";

export function Navbar() {
  const [steamId, setSteamId] = useState("");
  const router = useRouter();

  const handleSubmit = (e: FormEvent) => {
    e.preventDefault();
    if (steamId.trim()) {
      router.push(`/recommendations/${steamId}`);
    }
  };

  return (
    <div className="bg-gray-900 border-b border-gray-800">
      <div className="container mx-auto px-4">
        <div className="h-16 flex items-center justify-between">
          <Link
            href="/"
            className="flex items-center gap-2 hover:opacity-90 transition-opacity"
          >
            <GamepadIcon className="h-6 w-6 text-secondary" />
            <span className="font-bold text-xl bg-clip-text text-primary">
              NewGamePlus
            </span>
          </Link>

          <form
            onSubmit={handleSubmit}
            className="relative max-w-sm w-full hidden sm:block"
          >
            <div className="relative">
              <Input
                type="text"
                placeholder="Enter Steam ID for recommendations..."
                value={steamId}
                onChange={(e) => setSteamId(e.target.value)}
              />
              <Button
                type="submit"
                size="icon"
                className="absolute right-0 top-0 h-full bg-transparent hover:bg-transparent text-gray-400 hover:text-purple-400"
              >
                <Search className="h-4 w-4" />
                <span className="sr-only">Search</span>
              </Button>
            </div>
          </form>
        </div>
      </div>
    </div>
  );
}
