import { Button } from "@/components/ui/button"
import { GamepadIcon as GameController, Search, ArrowRight, User, Gamepad2 } from "lucide-react"
import Link from "next/link"
import Image from "next/image"
import SteamIdGuide from "@/components/pages/home/steam-id-guide"
import RecommendationForm from "@/components/pages/home/recommendation-form"

export default function LandingPage() {
  return (
    <div className="flex min-h-screen flex-col">
      <main className="flex-1">
        
        {/* Hero Section */}
        <section className="relative overflow-hidden py-20 md:py-32">
          <div className="absolute inset-0 z-0 bg-gradient-to-b from-background/20 to-gray-950"></div>
          <div className="absolute inset-0 z-0 opacity-3">
            <Image
              src="/steam-games.png?height=1080&width=1920"
              alt="Gaming background"
              fill
              className="object-cover"
              priority
            />
          </div>
          <div className="container relative z-10 mx-auto px-4 text-center">
            <h1 className="mb-6 text-4xl font-extrabold sm:text-5xl md:text-6xl bg-clip-text text-transparent bg-gradient-to-r from-muted to-primary">
              Discover Your Next Favorite Game
            </h1>
            <p className="mx-auto mb-8 max-w-2xl text-xl">
              New Game Plus uses our speciality trained models to analyze your Steam library and recommend games you'll love.
              No more endless scrolling through the store.
            </p>
            <div className="mx-auto max-w-md">
              <RecommendationForm />
            </div>
          </div>
        </section>

        {/* How It Works Section */}
        <section id="how-it-works" className="py-20 bg-gray-900">
          <div className="container mx-auto px-4">
            <h2 className="mb-12 text-center text-3xl font-bold">How It Works</h2>
            <div className="grid gap-8 md:grid-cols-3">
              <div className="flex flex-col items-center text-center p-6 rounded-lg bg-gray-800">
                <div className="mb-4 rounded-full bg-secondary p-3">
                  <User className="h-6 w-6 text-secondary-foreground" />
                </div>
                <h3 className="mb-2 text-xl font-bold">Enter Your Steam ID</h3>
                <p className="text-gray-400">
                  Provide your Steam ID so we can analyze your gaming preferences and history.
                </p>
              </div>
              <div className="flex flex-col items-center text-center p-6 rounded-lg bg-gray-800">
                <div className="mb-4 rounded-full bg-secondary p-3">
                  <Search className="h-6 w-6 text-secondary-foreground" />
                </div>
                <h3 className="mb-2 text-xl font-bold">Analysis</h3>
                <p className="text-gray-400">
                  Our models analyze your playtime, game genres, and more to understand your preferences.
                </p>
              </div>
              <div className="flex flex-col items-center text-center p-6 rounded-lg bg-gray-800">
                <div className="mb-4 rounded-full bg-secondary p-3">
                  <Gamepad2 className="h-6 w-6 text-secondary-foreground" />
                </div>
                <h3 className="mb-2 text-xl font-bold">Get Recommendations</h3>
                <p className="text-gray-400">
                  Receive personalized game recommendations that match your unique gaming style.
                </p>
              </div>
            </div>
          </div>
        </section>

        {/* Find Your Steam ID Section */}
        <section id="find-id" className="py-20">
          <div className="container mx-auto px-4">
            <h2 className="mb-12 text-center text-3xl font-bold">How to Find Your Steam ID</h2>
            <SteamIdGuide />
          </div>
        </section>

        {/* Testimonials/Stats Section */}
        <section id="about" className="py-20 bg-gray-900">
          <div className="container mx-auto px-4">
            <div className="grid gap-12 md:grid-cols-2 items-center">
              <div>
                <h2 className="mb-6 text-3xl font-bold">Powered by Gamers, for Gamers</h2>
                <p className="mb-6 text-gray-400">
                  New Game Plus was created by a team of passionate gamers who were tired of the Steam store algorithm
                  recommending the same games over and over.
                </p>
                <p className="mb-6 text-gray-400">
                  Our recommendation engine goes beyond the obvious choices to find hidden gems that match your unique
                  gaming preferences.
                </p>
                <div className="flex flex-wrap gap-4">
                  <div className="flex flex-col">
                    <span className="text-3xl font-bold text-accent">90,000+</span>
                    <span className="text-sm text-gray-400">Games Analyzed</span>
                  </div>
                </div>
              </div>
              <div className="relative h-[400px] rounded-lg overflow-hidden">
                <Image src="/gaming-setup.jpg" alt="Gaming setup" fill className="object-cover" />
              </div>
            </div>
          </div>
        </section>
      </main>
    </div>
  )
}
