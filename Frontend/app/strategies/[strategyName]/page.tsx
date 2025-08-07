'use client'

import { useEffect, useState } from "react"
import { useParams, useRouter } from "next/navigation"
import { Button } from "@/components/ui/button"
import { ArrowLeft, RefreshCw, Sparkles } from 'lucide-react'
import Link from "next/link"
import { StrategyHeader } from "@/components/strategy-details/strategy-header"
import { PerformanceMetrics } from "@/components/strategy-details/performance-metrics"
import { CumulativePnLChart } from "@/components/charts/cumulative-pnl-chart"
import { WinLossChart } from "@/components/charts/win-loss-chart"
import { StrategyLedger } from "@/components/strategy-details/strategy-ledger"
import { IndividualPnLChart } from "@/components/charts/individual-pnl-chart"
import { StrategyConfiguration } from "@/components/strategy-details/strategy-configuration"

interface StrategyData {
  strategy: any
  ledger: any[]
  currentPnl: number
}

export default function StrategyDetailPage() {
  const params = useParams()
  const router = useRouter()
  const strategyName = params.strategyName as string
  
  const [data, setData] = useState<StrategyData | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    fetchStrategyData()
  }, [strategyName])

  const fetchStrategyData = async () => {
    try {
      setLoading(true)
      const response = await fetch(`http://localhost:3001/api/strategies/${strategyName}`)
      
      if (!response.ok) {
        throw new Error(`Strategy not found: ${response.statusText}`)
      }
      
      const strategyData = await response.json()
      setData(strategyData)
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to fetch strategy data')
    } finally {
      setLoading(false)
    }
  }

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-rose-50 via-purple-50 to-teal-50 flex items-center justify-center">
        <div className="text-center space-y-4">
          <div className="p-4 bg-gradient-to-br from-purple-100 to-pink-100 rounded-full w-fit mx-auto">
            <RefreshCw className="h-8 w-8 animate-spin text-purple-600" />
          </div>
          <div>
            <p className="text-slate-600 font-medium">Loading strategy details...</p>
            <p className="text-sm text-slate-500">Fetching {strategyName} data</p>
          </div>
        </div>
      </div>
    )
  }

  if (error || !data) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-rose-50 via-purple-50 to-teal-50 flex items-center justify-center">
        <div className="text-center space-y-4">
          <div className="p-4 bg-gradient-to-br from-red-100 to-rose-100 rounded-full w-fit mx-auto">
            <Sparkles className="h-8 w-8 text-red-600" />
          </div>
          <div>
            <p className="text-slate-600 font-medium">Strategy not found</p>
            <p className="text-sm text-slate-500">{error}</p>
          </div>
          <Link href="/strategies">
            <Button className="bg-gradient-to-r from-purple-500 to-pink-500 hover:from-purple-600 hover:to-pink-600 text-white">
              HOME PAGE
            </Button>
          </Link>
        </div>
      </div>
    )
  }

  const totalTrades = data.ledger?.length || 0
  const profitableTrades = data.ledger?.filter(trade => (trade.pnl_sum || 0) > 0).length || 0
  const losingTrades = totalTrades - profitableTrades
  const winRate = totalTrades > 0 ? (profitableTrades / totalTrades * 100) : 0

  return (
    <div className="min-h-screen bg-gradient-to-br from-rose-50 via-purple-50 to-teal-50">
      <nav className="bg-white/90 backdrop-blur-xl border-b border-purple-100/50 sticky top-0 z-50 shadow-sm">
        <div className="container mx-auto px-6 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-4">
              <Link href="/strategies">
                <Button variant="outline" size="sm" className="border-purple-200 hover:bg-purple-50">
                  <ArrowLeft className="h-4 w-4 mr-2" />
                  HOME PAGE
                </Button>
              </Link>
              <div className="h-6 w-px bg-purple-200"></div>
              <div className="flex items-center gap-2">
                <Sparkles className="h-5 w-5 text-purple-500" />
                <span className="font-semibold text-purple-700">Strategy Details</span>
              </div>
            </div>
            <Button
              onClick={fetchStrategyData}
              disabled={loading}
              className="bg-gradient-to-r from-purple-500 to-pink-500 hover:from-purple-600 hover:to-pink-600 text-white"
            >
              <RefreshCw className={`h-4 w-4 mr-2 ${loading ? "animate-spin" : ""}`} />
              Refresh
            </Button>
          </div>
        </div>
      </nav>

      <div className="container mx-auto p-6 space-y-8">
        <StrategyHeader 
          strategy={data.strategy}
          currentPnl={data.currentPnl}
          totalTrades={totalTrades}
          winRate={winRate}
          ledger={data.ledger || []}
        />
        <StrategyConfiguration config={data.strategy} />
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          <div className="lg:col-span-2">
            <CumulativePnLChart data={data.ledger || []} />
          </div>
        </div>
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          <div>
            <IndividualPnLChart data={data.ledger || []} />
          </div>
          <div>
            <WinLossChart wins={profitableTrades} losses={losingTrades} />
          </div>
        </div>
        <PerformanceMetrics strategyName={strategyName} />
        <StrategyLedger ledger={data.ledger || []} />
      </div>
    </div>
  )
}