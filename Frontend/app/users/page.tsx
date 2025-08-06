"use client"

import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Users, Sparkles, Construction, TrendingUp, Brain, BarChart3 } from "lucide-react"
import Link from "next/link"

export default function UsersPage() {
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
                <Button variant="ghost" className="text-teal-600 hover:bg-teal-50 font-medium bg-teal-50">
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
              <div className="mx-auto mb-4 p-4 bg-gradient-to-br from-teal-100 to-cyan-100 rounded-full w-fit">
                <Construction className="h-12 w-12 text-teal-600" />
              </div>
              <CardTitle className="text-2xl bg-gradient-to-r from-teal-600 to-cyan-600 bg-clip-text text-transparent">
                Coming Soon
              </CardTitle>
              <CardDescription className="text-slate-600">
                User management features are currently under development
              </CardDescription>
            </CardHeader>
            <CardContent className="text-center">
              <div className="inline-flex items-center gap-2 bg-teal-50 px-4 py-2 rounded-full border border-teal-200 mb-6">
                <Sparkles className="h-4 w-4 text-teal-500" />
                <span className="text-sm text-teal-700 font-medium">Stay tuned for updates</span>
              </div>
              <p className="text-sm text-slate-500 mb-6">
                We're working hard to bring you comprehensive user management tools including role-based access, user
                analytics, and team collaboration features.
              </p>
              <Link href="/">
                <Button className="bg-gradient-to-r from-teal-500 to-cyan-500 hover:from-teal-600 hover:to-cyan-600 text-white">
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
