"use client"

import { Card, CardContent } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { CheckCircle } from 'lucide-react'

interface StrategyHeaderProps {
  strategy: {
    name: string
    symbol: string
    exchange: string
    time_horizon: string
    tp: number
    sl: number
    total_return?: number
    total_trades?: number
  }
  currentPnl: number
  totalTrades: number
  winRate: number
  ledger?: any[]
}

export function StrategyHeader({ strategy, currentPnl, totalTrades, winRate, ledger = [] }: StrategyHeaderProps) {
  // Use total return from backend or calculate from backtest data
  const calculateTotalReturn = () => {
    const initialBalance = 1000;
  
    if (strategy.total_return !== undefined) {
      return strategy.total_return;
    }
  
    if (ledger && ledger.length > 0) {
      const lastPnlSum = ledger[ledger.length - 1]?.pnl_sum;
      return lastPnlSum;
    }
    return 160.59; // fallback dummy value
  };
  

  const totalReturn = calculateTotalReturn()
  const actualTotalTrades = strategy.total_trades !== undefined ? strategy.total_trades : totalTrades


  const historicalPerformance = [
    { period: "1d Return", value: -2.42, isPositive: false },
    { period: "7d Return", value: 3.49, isPositive: true },
    { period: "15d Return", value: -17.75, isPositive: false },
    { period: "30d Return", value: -9.11, isPositive: false },
    { period: "45d Return", value: -6.90, isPositive: false },
    { period: "60d Return", value: 5.97, isPositive: true },
  ]

  return (
    <Card className="border-0 shadow-xl bg-white/95 backdrop-blur-sm">
      <CardContent className="p-8">
        <div className="flex gap-8">
          {/* Left Section - Strategy Info */}
          <div className="flex-shrink-0 w-64">
            {/* Strategy Name with Check Icon */}
            <div className="flex items-center gap-3 mb-4">
              <CheckCircle className="h-6 w-6 text-green-500" />
              <h1 className="text-xl font-bold text-slate-800">{strategy.name}</h1>
            </div>

            {/* Total Return */}
            <div className="mb-3">
              <span className="text-sm text-slate-600">Total Return : </span>
              <span className="text-sm font-semibold text-green-600">{totalReturn.toFixed(2)}%</span>
            </div>

            {/* Total Trades */}
            <div className="mb-4">
              <span className="text-sm text-slate-600">Total trades : </span>
              <span className="text-sm font-semibold text-slate-800">{actualTotalTrades}</span>
            </div>

            {/* Badges */}
            <div className="flex gap-2">
              <Badge variant="outline" className="bg-gray-100 text-gray-700 border-gray-300 text-xs px-2 py-1">
                {strategy.time_horizon?.trim()}
              </Badge>
              <Badge variant="outline" className="bg-gray-100 text-gray-700 border-gray-300 text-xs px-2 py-1">
                {strategy.symbol?.toLowerCase().trim()}
              </Badge>
            </div>
          </div>

          {/* Center Section - Trading Info Grid */}
          <div className="flex-1">
            <div className="grid grid-cols-3 gap-0">
              {/* Row 1 */}
              <div className="border border-gray-200 p-4 bg-gray-50/50">
                <div className="flex items-center gap-1 mb-2">
                  <span className="text-sm text-slate-600">Forecast</span>
                </div>
                <div className="text-center text-lg font-semibold text-slate-800">-</div>
              </div>

              <div className="border border-gray-200 border-l-0 p-4 bg-gray-50/50">
                <div className="flex items-center gap-1 mb-2">
                  <span className="text-sm text-slate-600">Forecast Time</span>
                </div>
                <div className="text-center text-lg font-semibold text-slate-800">-</div>
              </div>

              <div className="border border-gray-200 border-l-0 p-4 bg-gray-50/50">
                <div className="flex items-center gap-1 mb-2">
                  <span className="text-sm text-slate-600">Next Forecast</span>
                </div>
                <div className="text-center">
                  <div className="text-sm font-semibold text-slate-800">-</div>
                  <div className="text-sm text-slate-600"></div>
                </div>
              </div>

              {/* Row 2 */}
              <div className="border border-gray-200 border-t-0 p-4 bg-gray-50/50">
                <div className="flex items-center gap-1 mb-2">
                  <span className="text-sm text-slate-600">Entry Price</span>
                </div>
                <div className="text-center text-lg font-semibold text-slate-800">
                  -
                </div>
              </div>

              <div className="border border-gray-200 border-l-0 border-t-0 p-4 bg-gray-50/50">
                <div className="flex items-center gap-1 mb-2">
                  <span className="text-sm text-slate-600">Current Price</span>
                </div>
                <div className="text-center text-lg font-semibold text-slate-800">-</div>
              </div>

              <div className="border border-gray-200 border-l-0 border-t-0 p-4 bg-gray-50/50">
                <div className="flex items-center gap-1 mb-2">
                  <span className="text-sm text-slate-600">Current P&L</span>
                </div>
                <div className="text-center text-lg font-semibold text-green-600">
                  0%
                </div>
              </div>
            </div>
          </div>

          {/* Right Section - Historical Performance */}
          <div className="flex-shrink-0 w-80">
            <div className="flex items-center gap-1 mb-4">
              <span className="text-sm font-semibold text-slate-800">Historical performance</span>
            </div>

            <div className="grid grid-cols-3 gap-4">
              {historicalPerformance.map((item, index) => (
                <div key={index} className="text-center">
                  <div className="text-xs text-slate-600 mb-1">{item.period}</div>
                  <div className={`text-sm font-bold ${item.isPositive ? 'text-green-600' : 'text-red-600'}`}>
                    {item.isPositive ? '+' : ''}{item.value.toFixed(2)}%
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      </CardContent>
    </Card>
  )
}
