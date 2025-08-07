"use client"

import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import { TrendingUp, Users, Brain, BarChart3, Sparkles, Heart, Star } from 'lucide-react'
import Link from "next/link"

export default function HomePage() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-rose-50 via-purple-50 to-teal-50">
      {/* Navigation */}
      <nav className="bg-white/80 backdrop-blur-md border-b border-purple-100 sticky top-0 z-50">
        <div className="container mx-auto px-6 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <div className="p-2 bg-gradient-to-br from-purple-400 to-pink-400 rounded-xl">
                <Sparkles className="h-6 w-6 text-white" />
              </div>
              <div>
                <h1 className="text-xl font-bold bg-gradient-to-r from-purple-600 to-pink-600 bg-clip-text text-transparent">
                  TradingHub
                </h1>
                <p className="text-xs text-purple-500">Simplifying the Art of Trading</p>
              </div>
            </div>

            {/* Navigation Menu */}
            <div className="hidden md:flex items-center gap-6">
              <Link href="/strategies">
                <Button variant="ghost" className="text-purple-600 hover:bg-purple-50 font-medium">
                  <TrendingUp className="h-4 w-4 mr-2" />
                  Strategy Simulator
                </Button>
              </Link>
              <Link href="/users">
                <Button variant="ghost" className="text-teal-600 hover:bg-teal-50 font-medium">
                  <Users className="h-4 w-4 mr-2" />
                  User Management
                </Button>
              </Link>
              <Link href="/models">
                <Button variant="ghost" className="text-indigo-600 hover:bg-indigo-50 font-medium">
                  <Brain className="h-4 w-4 mr-2" />
                  Models
                </Button>
              </Link>
              <Link href="/analytics">
                <Button variant="ghost" className="text-emerald-600 hover:bg-emerald-50 font-medium">
                  <BarChart3 className="h-4 w-4 mr-2" />
                  Analytics
                </Button>
              </Link>
            </div>

            <div className="flex items-center gap-4">
              <Button variant="ghost" className="text-purple-600 hover:bg-purple-50 hidden sm:flex">
                <Heart className="h-4 w-4 mr-2" />
                Favorites
              </Button>
              <Button className="bg-gradient-to-r from-purple-500 to-pink-500 hover:from-purple-600 hover:to-pink-600 text-white">
                Get Started
              </Button>
            </div>
          </div>
        </div>
      </nav>

      {/* Hero Section */}
      <div className="container mx-auto px-6 py-12">
        <div className="text-center mb-12">
          <div className="inline-flex items-center gap-2 bg-white/60 backdrop-blur-sm px-4 py-2 rounded-full border border-purple-200 mb-6">
            <Star className="h-4 w-4 text-purple-500" />
            <span className="text-sm text-purple-700 font-medium">Welcome to the Trading Era</span>
          </div>
          <h1 className="text-5xl font-bold mb-6 bg-gradient-to-r from-purple-600 via-pink-600 to-teal-600 bg-clip-text text-transparent">
            Trade Smarter
            <br />
            With Confidence
          </h1>
          <p className="text-xl text-slate-600 max-w-2xl mx-auto leading-relaxed">
            Whether you're new to the markets or an experienced trader, our tools provide the clarity and control you need to navigate financial decisions with confidence.
          </p>
        </div>

        {/* Quick Access Cards */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-12">
          <Link href="/strategies">
            <Card className="relative overflow-hidden border-0 shadow-lg hover:shadow-xl transition-all duration-300 hover:-translate-y-1 bg-gradient-to-br from-purple-50 to-pink-50 cursor-pointer">
              <CardHeader className="pb-3">
                <div className="flex items-center justify-between mb-3">
                  <div className="p-3 rounded-xl bg-gradient-to-br from-purple-400 to-pink-400">
                    <TrendingUp className="h-6 w-6 text-white" />
                  </div>
                  <Badge variant="secondary" className="bg-green-100 text-green-700 text-xs">
                    Active
                  </Badge>
                </div>
                <CardTitle className="text-slate-800 text-lg">Strategy Simulator</CardTitle>
                <CardDescription className="text-slate-600 text-sm leading-relaxed">
                  Explore new ideas and refine your trading logic before going live.
                </CardDescription>
              </CardHeader>
              <CardContent className="pt-0">
                <Button className="w-full bg-white/80 hover:bg-white text-slate-700 border border-white/50">
                  Explore Now
                </Button>
              </CardContent>
              <div className="absolute top-0 right-0 w-20 h-20 bg-gradient-to-br from-white/20 to-transparent rounded-bl-full" />
            </Card>
          </Link>

          <Link href="/users">
            <Card className="relative overflow-hidden border-0 shadow-lg hover:shadow-xl transition-all duration-300 hover:-translate-y-1 bg-gradient-to-br from-teal-50 to-cyan-50 cursor-pointer">
              <CardHeader className="pb-3">
                <div className="flex items-center justify-between mb-3">
                  <div className="p-3 rounded-xl bg-gradient-to-br from-teal-400 to-cyan-400">
                    <Users className="h-6 w-6 text-white" />
                  </div>
                  <Badge variant="secondary" className="bg-orange-100 text-orange-700 text-xs">
                    Coming Soon
                  </Badge>
                </div>
                <CardTitle className="text-slate-800 text-lg">User Management</CardTitle>
                <CardDescription className="text-slate-600 text-sm leading-relaxed">
                  Organize accounts, track user sessions, and manage profiles securely.
                </CardDescription>
              </CardHeader>
              <CardContent className="pt-0">
                <Button className="w-full bg-white/80 hover:bg-white text-slate-700 border border-white/50">
                  Preview
                </Button>
              </CardContent>
              <div className="absolute top-0 right-0 w-20 h-20 bg-gradient-to-br from-white/20 to-transparent rounded-bl-full" />
            </Card>
          </Link>

          <Link href="/models">
            <Card className="relative overflow-hidden border-0 shadow-lg hover:shadow-xl transition-all duration-300 hover:-translate-y-1 bg-gradient-to-br from-indigo-50 to-purple-50 cursor-pointer">
              <CardHeader className="pb-3">
                <div className="flex items-center justify-between mb-3">
                  <div className="p-3 rounded-xl bg-gradient-to-br from-indigo-400 to-purple-400">
                    <Brain className="h-6 w-6 text-white" />
                  </div>
                  <Badge variant="secondary" className="bg-orange-100 text-orange-700 text-xs">
                    Coming Soon
                  </Badge>
                </div>
                <CardTitle className="text-slate-800 text-lg">AI Models</CardTitle>
                <CardDescription className="text-slate-600 text-sm leading-relaxed">
                  Leverage intelligent systems to interpret price action and market signals.
                </CardDescription>
              </CardHeader>
              <CardContent className="pt-0">
                <Button className="w-full bg-white/80 hover:bg-white text-slate-700 border border-white/50">
                  Preview
                </Button>
              </CardContent>
              <div className="absolute top-0 right-0 w-20 h-20 bg-gradient-to-br from-white/20 to-transparent rounded-bl-full" />
            </Card>
          </Link>

          <Link href="/analytics">
            <Card className="relative overflow-hidden border-0 shadow-lg hover:shadow-xl transition-all duration-300 hover:-translate-y-1 bg-gradient-to-br from-emerald-50 to-teal-50 cursor-pointer">
              <CardHeader className="pb-3">
                <div className="flex items-center justify-between mb-3">
                  <div className="p-3 rounded-xl bg-gradient-to-br from-emerald-400 to-teal-400">
                    <BarChart3 className="h-6 w-6 text-white" />
                  </div>
                  <Badge variant="secondary" className="bg-orange-100 text-orange-700 text-xs">
                    Coming Soon
                  </Badge>
                </div>
                <CardTitle className="text-slate-800 text-lg">Analytics</CardTitle>
                <CardDescription className="text-slate-600 text-sm leading-relaxed">
                  Gain deeper insight into trends, patterns, and key trading metrics.
                </CardDescription>
              </CardHeader>
              <CardContent className="pt-0">
                <Button className="w-full bg-white/80 hover:bg-white text-slate-700 border border-white/50">
                  Preview
                </Button>
              </CardContent>
              <div className="absolute top-0 right-0 w-20 h-20 bg-gradient-to-br from-white/20 to-transparent rounded-bl-full" />
            </Card>
          </Link>
        </div>

        {/* Stats Section */}
        <Card className="bg-white/60 backdrop-blur-sm border-0 shadow-lg">
          <CardContent className="p-8">
            <div className="grid grid-cols-1 md:grid-cols-3 gap-8 text-center">
              <div>
                <div className="text-3xl font-bold bg-gradient-to-r from-purple-600 to-pink-600 bg-clip-text text-transparent mb-2">
                  14+
                </div>
                <p className="text-slate-600">Strategies Available</p>
              </div>
              <div>
                <div className="text-3xl font-bold bg-gradient-to-r from-teal-600 to-cyan-600 bg-clip-text text-transparent mb-2">
                  3
                </div>
                <p className="text-slate-600">Connected Platforms</p>
              </div>
              <div>
                <div className="text-3xl font-bold bg-gradient-to-r from-indigo-600 to-purple-600 bg-clip-text text-transparent mb-2">
                  24/7
                </div>
                <p className="text-slate-600">Continuous Data Updates</p>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Footer */}
      <footer className="bg-white/40 backdrop-blur-sm border-t border-purple-100 mt-16">
        <div className="container mx-auto px-6 py-8">
          <div className="text-center text-slate-600">
            <p className="flex items-center justify-center gap-2">
              Built for <Heart className="h-4 w-4 text-pink-500" /> traders who demand precision and clarity
            </p>
          </div>
        </div>
      </footer>
    </div>
  )
}
