"use client"

import { useEffect, useState } from "react"
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select"
import { RefreshCw, TrendingUp, Users, Brain, BarChart3, Sparkles, ChevronUp, ChevronDown, Filter, X, ArrowUpDown, ChevronLeft, ChevronRight, TrendingDown, DollarSign, Activity } from 'lucide-react'
import Link from "next/link"

interface Strategy {
  name: string
  exchange: string
  symbol: string
  time_horizon: string
  pnl: number
}

type SortOrder = 'asc' | 'desc' | 'none'

const ITEMS_PER_PAGE = 10

export default function StrategiesPage() {
  const [strategies, setStrategies] = useState<Strategy[]>([])
  const [loading, setLoading] = useState(true)
  const [filteredStrategies, setFilteredStrategies] = useState<Strategy[]>([])
  const [currentPage, setCurrentPage] = useState(1)
  
  // Filter states
  const [selectedSymbol, setSelectedSymbol] = useState<string>("all")
  const [selectedExchange, setSelectedExchange] = useState<string>("all")
  const [selectedTimeHorizon, setSelectedTimeHorizon] = useState<string>("all")
  const [pnlSortOrder, setPnlSortOrder] = useState<SortOrder>('none')

  useEffect(() => {
    fetchStrategies()
  }, [])

  useEffect(() => {
    let filtered = strategies.filter((strategy) => {
      const matchesSymbol = selectedSymbol === "all" || strategy.symbol === selectedSymbol
      const matchesExchange = selectedExchange === "all" || strategy.exchange === selectedExchange
      const matchesTimeHorizon = selectedTimeHorizon === "all" || strategy.time_horizon === selectedTimeHorizon

      return matchesSymbol && matchesExchange && matchesTimeHorizon
    })

    // Apply PnL sorting
    if (pnlSortOrder === 'asc') {
      filtered = filtered.sort((a, b) => a.pnl - b.pnl)
    } else if (pnlSortOrder === 'desc') {
      filtered = filtered.sort((a, b) => b.pnl - a.pnl)
    }

    setFilteredStrategies(filtered)
    setCurrentPage(1) // Reset to first page when filters change
  }, [strategies, selectedSymbol, selectedExchange, selectedTimeHorizon, pnlSortOrder])

  const fetchStrategies = async () => {
    try {
      setLoading(true)
      const response = await fetch("http://localhost:3001/api/strategies")
      const data = await response.json()
      setStrategies(data)
    } catch (error) {
      console.error("Error fetching strategies:", error)
    } finally {
      setLoading(false)
    }
  }

  // Get unique values for filter options
  const uniqueSymbols = [...new Set(strategies.map(s => s.symbol))]
  const uniqueExchanges = [...new Set(strategies.map(s => s.exchange))]
  const uniqueTimeHorizons = [...new Set(strategies.map(s => s.time_horizon))]

  // Pagination calculations
  const totalPages = Math.ceil(filteredStrategies.length / ITEMS_PER_PAGE)
  const startIndex = (currentPage - 1) * ITEMS_PER_PAGE
  const endIndex = startIndex + ITEMS_PER_PAGE
  const currentStrategies = filteredStrategies.slice(startIndex, endIndex)

  // Statistics calculations
  const totalStrategies = filteredStrategies.length
  const profitableStrategies = filteredStrategies.filter(s => s.pnl > 0).length
  const losingStrategies = filteredStrategies.filter(s => s.pnl < 0).length
  const averagePnL = filteredStrategies.length > 0 
    ? filteredStrategies.reduce((sum, s) => sum + s.pnl, 0) / filteredStrategies.length 
    : 0

  const getSymbolColor = (symbol: string) => {
    switch (symbol?.toLowerCase()) {
      case "btc":
        return "bg-gradient-to-r from-orange-100 to-amber-100 text-orange-800 border-orange-200 shadow-sm"
      case "sol":
        return "bg-gradient-to-r from-purple-100 to-violet-100 text-purple-800 border-purple-200 shadow-sm"
      case "xrp":
        return "bg-gradient-to-r from-blue-100 to-cyan-100 text-blue-800 border-blue-200 shadow-sm"
      default:
        return "bg-gradient-to-r from-gray-100 to-slate-100 text-gray-800 border-gray-200 shadow-sm"
    }
  }

  const getTimeHorizonColor = (timeHorizon: string) => {
    switch (timeHorizon?.toLowerCase()) {
      case "1h":
        return "bg-gradient-to-r from-emerald-100 to-teal-100 text-emerald-800 border-emerald-200 shadow-sm"
      case "4h":
        return "bg-gradient-to-r from-teal-100 to-cyan-100 text-teal-800 border-teal-200 shadow-sm"
      default:
        return "bg-gradient-to-r from-gray-100 to-slate-100 text-gray-800 border-gray-200 shadow-sm"
    }
  }

  const getPnlColor = (pnl: number) => {
    if (pnl > 0) return "bg-gradient-to-r from-green-100 to-emerald-100 text-green-800 border-green-200 shadow-sm font-semibold"
    if (pnl < 0) return "bg-gradient-to-r from-red-100 to-rose-100 text-red-800 border-red-200 shadow-sm font-semibold"
    return "bg-gradient-to-r from-gray-100 to-slate-100 text-gray-800 border-gray-200 shadow-sm"
  }

  const handlePnlSort = () => {
    if (pnlSortOrder === 'none') {
      setPnlSortOrder('desc')
    } else if (pnlSortOrder === 'desc') {
      setPnlSortOrder('asc')
    } else {
      setPnlSortOrder('none')
    }
  }

  const clearFilters = () => {
    setSelectedSymbol("all")
    setSelectedExchange("all")
    setSelectedTimeHorizon("all")
    setPnlSortOrder('none')
  }

  const hasActiveFilters = selectedSymbol !== "all" || selectedExchange !== "all" || selectedTimeHorizon !== "all" || pnlSortOrder !== 'none'

  return (
    <div className="min-h-screen bg-gradient-to-br from-rose-50 via-purple-50 to-teal-50">
      {/* Navigation */}
      <nav className="bg-white/90 backdrop-blur-xl border-b border-purple-100/50 sticky top-0 z-50 shadow-sm">
        <div className="container mx-auto px-6 py-4">
          <div className="flex items-center justify-between">
            <Link href="/" className="flex items-center gap-3 group">
              <div className="p-2 bg-gradient-to-br from-purple-400 to-pink-400 rounded-xl shadow-lg group-hover:shadow-xl transition-all duration-300 group-hover:scale-105">
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
            <div className="hidden md:flex items-center gap-2">
              <Link href="/strategies">
                <Button
                  variant="ghost"
                  className="text-purple-600 hover:bg-purple-50 font-medium bg-purple-50/80 shadow-sm border border-purple-100"
                >
                  <TrendingUp className="h-4 w-4 mr-2" />
                  Strategy Simulator
                </Button>
              </Link>
              <Link href="/users">
                <Button
                  variant="ghost"
                  className="text-teal-600 hover:bg-teal-50 font-medium hover:shadow-sm transition-all duration-200"
                >
                  <Users className="h-4 w-4 mr-2" />
                  User Management
                </Button>
              </Link>
              <Link href="/models">
                <Button
                  variant="ghost"
                  className="text-indigo-600 hover:bg-indigo-50 font-medium hover:shadow-sm transition-all duration-200"
                >
                  <Brain className="h-4 w-4 mr-2" />
                  Models
                </Button>
              </Link>
              <Link href="/analytics">
                <Button
                  variant="ghost"
                  className="text-emerald-600 hover:bg-emerald-50 font-medium hover:shadow-sm transition-all duration-200"
                >
                  <BarChart3 className="h-4 w-4 mr-2" />
                  Analytics
                </Button>
              </Link>
            </div>

            <div className="flex items-center gap-4">
              <Button className="bg-gradient-to-r from-purple-500 to-pink-500 hover:from-purple-600 hover:to-pink-600 text-white shadow-lg hover:shadow-xl transition-all duration-300 hover:scale-105">
                Get Started
              </Button>
            </div>
          </div>
        </div>
      </nav>

      <div className="container mx-auto p-6 space-y-8">
        {/* Header */}
        <div className="text-center space-y-4">
          <div className="inline-flex items-center gap-2 bg-white/70 backdrop-blur-sm px-6 py-3 rounded-full border border-purple-200/50 shadow-lg">
            <Sparkles className="h-5 w-5 text-purple-500" />
            <span className="text-sm text-purple-700 font-semibold tracking-wide">
              Live Strategy Dashboard
            </span>
          </div>
          <h1 className="text-4xl font-bold bg-gradient-to-r from-purple-600 via-pink-600 to-teal-600 bg-clip-text text-transparent">
            Trading Strategies
          </h1>
          <p className="text-slate-600 text-lg max-w-2xl mx-auto">
            Monitor and analyze your automated trading strategies with advanced filtering and real-time insights
          </p>
        </div>

        {/* Statistics Summary */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
          <Card className="border-0 shadow-lg bg-gradient-to-br from-white/80 to-purple-50/50 backdrop-blur-sm">
            <CardContent className="p-6">
              <div className="flex items-center gap-4">
                <div className="p-3 bg-gradient-to-br from-purple-100 to-pink-100 rounded-xl">
                  <Activity className="h-6 w-6 text-purple-600" />
                </div>
                <div>
                  <p className="text-sm font-medium text-slate-600">Total Strategies</p>
                  <p className="text-2xl font-bold text-slate-800">{totalStrategies}</p>
                </div>
              </div>
            </CardContent>
          </Card>

          <Card className="border-0 shadow-lg bg-gradient-to-br from-white/80 to-green-50/50 backdrop-blur-sm">
            <CardContent className="p-6">
              <div className="flex items-center gap-4">
                <div className="p-3 bg-gradient-to-br from-green-100 to-emerald-100 rounded-xl">
                  <TrendingUp className="h-6 w-6 text-green-600" />
                </div>
                <div>
                  <p className="text-sm font-medium text-slate-600">Profitable</p>
                  <p className="text-2xl font-bold text-green-600">{profitableStrategies}</p>
                </div>
              </div>
            </CardContent>
          </Card>

          <Card className="border-0 shadow-lg bg-gradient-to-br from-white/80 to-red-50/50 backdrop-blur-sm">
            <CardContent className="p-6">
              <div className="flex items-center gap-4">
                <div className="p-3 bg-gradient-to-br from-red-100 to-rose-100 rounded-xl">
                  <TrendingDown className="h-6 w-6 text-red-600" />
                </div>
                <div>
                  <p className="text-sm font-medium text-slate-600">Losing</p>
                  <p className="text-2xl font-bold text-red-600">{losingStrategies}</p>
                </div>
              </div>
            </CardContent>
          </Card>

          <Card className="border-0 shadow-lg bg-gradient-to-br from-white/80 to-blue-50/50 backdrop-blur-sm">
            <CardContent className="p-6">
              <div className="flex items-center gap-4">
                <div className="p-3 bg-gradient-to-br from-blue-100 to-cyan-100 rounded-xl">
                  <DollarSign className="h-6 w-6 text-blue-600" />
                </div>
                <div>
                  <p className="text-sm font-medium text-slate-600">Avg P&L</p>
                  <p className={`text-2xl font-bold ${averagePnL >= 0 ? 'text-green-600' : 'text-red-600'}`}>
                    {averagePnL >= 0 ? '+' : ''}{averagePnL.toFixed(2)}%
                  </p>
                </div>
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Refresh Control */}
        <div className="flex justify-center">
          <Button
            onClick={fetchStrategies}
            disabled={loading}
            className="bg-gradient-to-r from-purple-500 to-pink-500 hover:from-purple-600 hover:to-pink-600 text-white shadow-lg hover:shadow-xl transition-all duration-300 h-12 px-8 rounded-xl"
          >
            <RefreshCw className={`h-5 w-5 mr-2 ${loading ? "animate-spin" : ""}`} />
            Refresh Data
          </Button>
        </div>

        {/* Enhanced Filters */}
        <Card className="border-0 shadow-xl bg-gradient-to-r from-white/80 to-purple-50/50 backdrop-blur-sm">
          <CardContent className="p-6">
            <div className="flex items-center justify-between mb-6">
              <div className="flex items-center gap-3">
                <div className="p-2 bg-gradient-to-br from-purple-100 to-pink-100 rounded-lg">
                  <Filter className="h-5 w-5 text-purple-600" />
                </div>
                <div>
                  <h3 className="text-lg font-semibold text-slate-800">Smart Filters</h3>
                  <p className="text-sm text-slate-600">Refine your strategy search</p>
                </div>
              </div>
              {hasActiveFilters && (
                <Button
                  onClick={clearFilters}
                  variant="outline"
                  size="sm"
                  className="border-red-200 text-red-600 hover:bg-red-50 shadow-sm"
                >
                  <X className="h-4 w-4 mr-1" />
                  Clear All
                </Button>
              )}
            </div>
            
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
              <div className="space-y-3">
                <label className="text-sm font-semibold text-slate-700 flex items-center gap-2">
                  <div className="w-2 h-2 bg-orange-400 rounded-full"></div>
                  Symbol
                </label>
                <Select value={selectedSymbol} onValueChange={setSelectedSymbol}>
                  <SelectTrigger className="bg-white/90 border-purple-200/50 shadow-sm h-11 rounded-xl">
                    <SelectValue placeholder="All Symbols" />
                  </SelectTrigger>
                  <SelectContent className="rounded-xl">
                    <SelectItem value="all">All Symbols</SelectItem>
                    {uniqueSymbols.map((symbol) => (
                      <SelectItem key={symbol} value={symbol}>
                        {symbol.toUpperCase()}
                      </SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>

              <div className="space-y-3">
                <label className="text-sm font-semibold text-slate-700 flex items-center gap-2">
                  <div className="w-2 h-2 bg-emerald-400 rounded-full"></div>
                  Exchange
                </label>
                <Select value={selectedExchange} onValueChange={setSelectedExchange}>
                  <SelectTrigger className="bg-white/90 border-purple-200/50 shadow-sm h-11 rounded-xl">
                    <SelectValue placeholder="All Exchanges" />
                  </SelectTrigger>
                  <SelectContent className="rounded-xl">
                    <SelectItem value="all">All Exchanges</SelectItem>
                    {uniqueExchanges.map((exchange) => (
                      <SelectItem key={exchange} value={exchange}>
                        {exchange.charAt(0).toUpperCase() + exchange.slice(1)}
                      </SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>

              <div className="space-y-3">
                <label className="text-sm font-semibold text-slate-700 flex items-center gap-2">
                  <div className="w-2 h-2 bg-teal-400 rounded-full"></div>
                  Time Horizon
                </label>
                <Select value={selectedTimeHorizon} onValueChange={setSelectedTimeHorizon}>
                  <SelectTrigger className="bg-white/90 border-purple-200/50 shadow-sm h-11 rounded-xl">
                    <SelectValue placeholder="All Time Frames" />
                  </SelectTrigger>
                  <SelectContent className="rounded-xl">
                    <SelectItem value="all">All Time Frames</SelectItem>
                    {uniqueTimeHorizons.map((timeHorizon) => (
                      <SelectItem key={timeHorizon} value={timeHorizon}>
                        {timeHorizon}
                      </SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>
            </div>

            {hasActiveFilters && (
              <div className="mt-6 p-4 bg-gradient-to-r from-purple-50 to-pink-50 rounded-xl border border-purple-100">
                <div className="flex items-center gap-2 text-sm text-purple-700">
                  <Sparkles className="h-4 w-4" />
                  <span className="font-medium">
                    Showing {filteredStrategies.length} of {strategies.length} strategies
                  </span>
                </div>
              </div>
            )}
          </CardContent>
        </Card>

        {/* Enhanced Strategies Table */}
        <Card className="border-0 shadow-2xl bg-white/90 backdrop-blur-sm overflow-hidden">
          <CardHeader className="bg-gradient-to-r from-purple-50 via-pink-50 to-teal-50 border-b border-purple-100/50 p-6">
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-3">
                <div className="p-2 bg-gradient-to-br from-purple-500 to-pink-500 rounded-lg shadow-lg">
                  <TrendingUp className="h-6 w-6 text-white" />
                </div>
                <div>
                  <CardTitle className="text-xl text-slate-800">Active Strategies</CardTitle>
                  <CardDescription className="text-slate-600">
                    Page {currentPage} of {totalPages} • {filteredStrategies.length} total strategies
                  </CardDescription>
                </div>
              </div>
              <div className="flex items-center gap-2 text-sm text-slate-500">
                <div className="w-2 h-2 bg-green-400 rounded-full animate-pulse"></div>
                Live Updates
              </div>
            </div>
          </CardHeader>
          <CardContent className="p-0">
            {loading ? (
              <div className="flex flex-col items-center justify-center py-16 space-y-4">
                <div className="p-4 bg-gradient-to-br from-purple-100 to-pink-100 rounded-full">
                  <RefreshCw className="h-8 w-8 animate-spin text-purple-600" />
                </div>
                <div className="text-center">
                  <p className="text-slate-600 font-medium">Loading strategies...</p>
                  <p className="text-sm text-slate-500">Fetching real-time data</p>
                </div>
              </div>
            ) : (
              <>
                <div className="overflow-x-auto">
                  <table className="w-full">
                    <thead className="bg-gradient-to-r from-slate-50 to-purple-50/30 border-b border-purple-100/50">
                      <tr>
                        <th className="text-left p-6 font-semibold text-slate-700 text-sm uppercase tracking-wide">Strategy Name</th>
                        <th className="text-left p-6 font-semibold text-slate-700 text-sm uppercase tracking-wide">Exchange</th>
                        <th className="text-left p-6 font-semibold text-slate-700 text-sm uppercase tracking-wide">Symbol</th>
                        <th className="text-left p-6 font-semibold text-slate-700 text-sm uppercase tracking-wide">Time Frame</th>
                        <th className="text-left p-6 font-semibold text-slate-700 text-sm uppercase tracking-wide">
                          <button
                            onClick={handlePnlSort}
                            className="flex items-center gap-2 hover:text-purple-600 transition-colors group"
                          >
                            P&L Performance
                            <div className="flex flex-col">
                              {pnlSortOrder === 'asc' && <ChevronUp className="h-4 w-4 text-purple-600" />}
                              {pnlSortOrder === 'desc' && <ChevronDown className="h-4 w-4 text-purple-600" />}
                              {pnlSortOrder === 'none' && <ArrowUpDown className="h-4 w-4 text-slate-400 group-hover:text-purple-600" />}
                            </div>
                          </button>
                        </th>
                      </tr>
                    </thead>
                    <tbody>
                      {currentStrategies.map((strategy, index) => (
                        <tr
                          key={strategy.name}
                          className={`border-b border-purple-50/50 hover:bg-gradient-to-r hover:from-purple-25/50 hover:to-pink-25/50 transition-all duration-300 group ${
                            index % 2 === 0 ? "bg-white/50" : "bg-purple-25/20"
                          }`}
                        >
                          <td className="p-6">
                            <div className="font-semibold text-slate-800 group-hover:text-purple-700 transition-colors">
                              {strategy.name}
                            </div>
                          </td>
                          <td className="p-6">
                            <Badge variant="outline" className="bg-gradient-to-r from-emerald-100 to-teal-100 text-emerald-800 border-emerald-200 shadow-sm font-medium">
                              {strategy.exchange}
                            </Badge>
                          </td>
                          <td className="p-6">
                            <Badge variant="outline" className={getSymbolColor(strategy.symbol)}>
                              {strategy.symbol.toUpperCase()}
                            </Badge>
                          </td>
                          <td className="p-6">
                            <Badge variant="outline" className={getTimeHorizonColor(strategy.time_horizon)}>
                              {strategy.time_horizon}
                            </Badge>
                          </td>
                          <td className="p-6">
                            <Badge variant="outline" className={getPnlColor(strategy.pnl)}>
                              {strategy.pnl > 0 ? "+" : ""}
                              {strategy.pnl.toFixed(2)}%
                            </Badge>
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>

                {/* Pagination */}
                {totalPages > 1 && (
                  <div className="flex items-center justify-between p-6 bg-gradient-to-r from-purple-50/30 to-pink-50/30 border-t border-purple-100/50">
                    <div className="text-sm text-slate-600">
                      Showing {startIndex + 1} to {Math.min(endIndex, filteredStrategies.length)} of {filteredStrategies.length} strategies
                    </div>
                    <div className="flex items-center gap-2">
                      <Button
                        onClick={() => setCurrentPage(prev => Math.max(prev - 1, 1))}
                        disabled={currentPage === 1}
                        variant="outline"
                        size="sm"
                        className="border-purple-200 hover:bg-purple-50"
                      >
                        <ChevronLeft className="h-4 w-4" />
                        Previous
                      </Button>
                      
                      <div className="flex items-center gap-1">
                        {Array.from({ length: Math.min(5, totalPages) }, (_, i) => {
                          let pageNum;
                          if (totalPages <= 5) {
                            pageNum = i + 1;
                          } else if (currentPage <= 3) {
                            pageNum = i + 1;
                          } else if (currentPage >= totalPages - 2) {
                            pageNum = totalPages - 4 + i;
                          } else {
                            pageNum = currentPage - 2 + i;
                          }
                          
                          return (
                            <Button
                              key={pageNum}
                              onClick={() => setCurrentPage(pageNum)}
                              variant={currentPage === pageNum ? "default" : "outline"}
                              size="sm"
                              className={
                                currentPage === pageNum
                                  ? "bg-gradient-to-r from-purple-500 to-pink-500 text-white shadow-sm"
                                  : "border-purple-200 hover:bg-purple-50"
                              }
                            >
                              {pageNum}
                            </Button>
                          );
                        })}
                      </div>

                      <Button
                        onClick={() => setCurrentPage(prev => Math.min(prev + 1, totalPages))}
                        disabled={currentPage === totalPages}
                        variant="outline"
                        size="sm"
                        className="border-purple-200 hover:bg-purple-50"
                      >
                        Next
                        <ChevronRight className="h-4 w-4" />
                      </Button>
                    </div>
                  </div>
                )}

                {filteredStrategies.length === 0 && !loading && (
                  <div className="text-center py-16 space-y-4">
                    <div className="p-4 bg-gradient-to-br from-slate-100 to-purple-100 rounded-full w-fit mx-auto">
                      <Filter className="h-8 w-8 text-slate-500" />
                    </div>
                    <div>
                      <p className="text-slate-600 font-medium">No strategies found</p>
                      <p className="text-sm text-slate-500">Try adjusting your filters to see more results</p>
                    </div>
                  </div>
                )}
              </>
            )}
          </CardContent>
        </Card>
      </div>
    </div>
  )
}
