"use client"

import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Brain, Sparkles, Construction, TrendingUp, Users, BarChart3 } from "lucide-react"
import Link from "next/link"

export default function ModelsPage() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-rose-50 via-purple-50 to-teal-50">
      {/* Navigation */}
      <nav className="bg-white/80 backdrop-blur-md border-b border-purple-100 sticky top-0 z-50">
        <div className="container mx-auto px-6 py-4">
          <div className="flex items-center justify-between">
            <Link href="/" className="flex items-center gap-3">
              <div className="p-2 bg-gradient-to-br from-purple-400 to-pink-400 rounded-xl">
                <Sparkles className="h-6 w-6 text-white" />
              </div>
              <div>
                <h1 className="text-xl font-bold bg-gradient-to-r from-purple-600 to-pink-600 bg-clip-text text-transparent">
                  TradingHub
                </h1>
                <p className="text-xs text-purple-500">Your Trading Companion</p>
              </div>
            </Link>

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
                <Button variant="ghost" className="text-indigo-600 hover:bg-indigo-50 font-medium bg-indigo-50">
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
              <Button className="bg-gradient-to-r from-purple-500 to-pink-500 hover:from-purple-600 hover:to-pink-600 text-white">
                Get Started
              </Button>
            </div>
          </div>
        </div>
      </nav>

      <div className="container mx-auto p-6">
        <div className="flex items-center justify-center min-h-[60vh]">
          <Card className="max-w-md w-full bg-white/80 backdrop-blur-sm border-0 shadow-lg">
            <CardHeader className="text-center pb-4">
              <div className="mx-auto mb-4 p-4 bg-gradient-to-br from-indigo-100 to-purple-100 rounded-full w-fit">
                <Construction className="h-12 w-12 text-indigo-600" />
              </div>
              <CardTitle className="text-2xl bg-gradient-to-r from-indigo-600 to-purple-600 bg-clip-text text-transparent">
                Coming Soon
              </CardTitle>
              <CardDescription className="text-slate-600">
                AI model management features are currently under development
              </CardDescription>
            </CardHeader>
            <CardContent className="text-center">
              <div className="inline-flex items-center gap-2 bg-indigo-50 px-4 py-2 rounded-full border border-indigo-200 mb-6">
                <Sparkles className="h-4 w-4 text-indigo-500" />
                <span className="text-sm text-indigo-700 font-medium">AI-powered trading ahead</span>
              </div>
              <p className="text-sm text-slate-500 mb-6">
                We're developing advanced machine learning models for market prediction, risk assessment, and automated
                trading strategy optimization.
              </p>
              <Link href="/">
                <Button className="bg-gradient-to-r from-indigo-500 to-purple-500 hover:from-indigo-600 hover:to-purple-600 text-white">
                  Return to Dashboard
                </Button>
              </Link>
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  )
}
