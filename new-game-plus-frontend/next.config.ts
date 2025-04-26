import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  images: {
    domains: [
      'cdn.akamai.steamstatic.com',
      'steamcdn-a.akamaihd.net',
      'media.steampowered.com',
      'cdn.cloudflare.steamstatic.com',
      'steamcdn.cloudflare.steamstatic.com',
    ],
  },
};

export default nextConfig;
