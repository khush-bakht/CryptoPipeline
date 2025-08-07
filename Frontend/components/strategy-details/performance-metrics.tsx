'use client'

import { useEffect, useState } from 'react'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Skeleton } from '@/components/ui/skeleton'

interface PerformanceMetrics {
  total_return: number
  daily_return: number
  weekly_return: number
  monthly_return: number
  cagr: number
  sharpe_ratio: number
  sortino_ratio: number
  calmar_ratio: number
  alpha: number
  beta: number
  r_squared: number
  information_ratio: number
  treynor_ratio: number
  profit_factor: number
  omega_ratio: number
  gain_to_pain_ratio: number
  payoff_ratio: number
  cpc_ratio: number
  risk_return_ratio: number
  common_sense_ratio: number
  max_drawdown: number
  max_drawdown_days: number
  avg_drawdown: number
  avg_drawdown_days: number
  current_drawdown: number
  current_drawdown_days: number
  drawdown_duration: number
  conditional_drawdown_at_risk: number
  ulcer_index: number
  risk_of_ruin: number
  var_95: number
  cvar_99: number
  downside_deviation: number
  volatility: number
  annualized_volatility: number
  skewness: number
  kurtosis: number
  winning_weeks: number
  losing_weeks: number
  winning_months: number
  losing_months: number
  winning_months_percent: number
  negative_months_percent: number
  total_profit: number
  net_profit: number
  avg_profit_per_trade: number
  avg_loss_per_trade: number
  profit_loss_ratio: number
  number_of_trades: number
  win_rate: number
  loss_rate: number
  average_win: number
  average_loss: number
  average_trade_duration: number
  largest_win: number
  largest_loss: number
  consecutive_wins: number
  consecutive_losses: number
  avg_trade_return: number
  profitability_per_trade: number
  recovery_factor: number
  total_long_return: number
  avg_long_return_per_trade: number
  num_long_trades: number
  win_rate_long_trades: number
  avg_long_trade_duration: number
  max_long_trade_return: number
  min_long_trade_return: number
  long_trades_percent: number
  total_short_return: number
  avg_short_return_per_trade: number
  num_short_trades: number
  win_rate_short_trades: number
  avg_short_trade_duration: number
  max_short_trade_return: number
  min_short_trade_return: number
  short_trades_percent: number
}

interface PerformanceMetricsProps {
  strategyName: string
}

export function PerformanceMetrics({ strategyName }: PerformanceMetricsProps) {
  const [metrics, setMetrics] = useState<PerformanceMetrics | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    const fetchMetrics = async () => {
      try {
        setLoading(true)
        const response = await fetch(`http://localhost:3001/api/strategy-metrics?strategy=${encodeURIComponent(strategyName)}`)
        
        if (!response.ok) {
          throw new Error(`Failed to fetch metrics: ${response.statusText}`)
        }
        
        const data = await response.json()
        // Convert string values to numbers
        const parsedData = Object.fromEntries(
          Object.entries(data).map(([key, value]) => [
            key,
            typeof value === 'string' && !isNaN(parseFloat(value)) ? parseFloat(value) : value
          ])
        ) as unknown as PerformanceMetrics
        setMetrics(parsedData)
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Failed to load metrics')
      } finally {
        setLoading(false)
      }
    }

    if (strategyName) {
      fetchMetrics()
    }
  }, [strategyName])

  if (loading) {
    return (
      <div className="space-y-6">
        <Skeleton className="h-8 w-48" />
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {Array.from({ length: 6 }).map((_, i) => (
            <Card key={i}>
              <CardHeader>
                <Skeleton className="h-6 w-32" />
              </CardHeader>
              <CardContent>
                <div className="space-y-3">
                  {Array.from({ length: 5 }).map((_, j) => (
                    <div key={j} className="flex justify-between">
                      <Skeleton className="h-4 w-24" />
                      <Skeleton className="h-4 w-16" />
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
          ))}
        </div>
      </div>
    )
  }

  if (error || !metrics) {
    return (
      <Card>
        <CardContent className="p-6">
          <p className="text-center text-muted-foreground">
            {error || 'No metrics available for this strategy'}
          </p>
        </CardContent>
      </Card>
    )
  }

  const formatValue = (value: number | string | null | undefined, isPercentage = false, isCurrency = false, decimals = 2) => {
    if (value === null || value === undefined || (typeof value === 'string' && value.trim() === '')) return 'N/A'
    
    const numericValue = typeof value === 'string' ? parseFloat(value) : value
    
    if (isNaN(numericValue)) return 'N/A'
    
    if (isCurrency) {
      return new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: 'USD',
        minimumFractionDigits: decimals
      }).format(numericValue)
    }
    
    if (isPercentage) {
      return `${numericValue.toFixed(decimals)}%`
    }
    
    return numericValue.toFixed(decimals)
  }

  const getValueColor = (value: number | string, isPositive = true) => {
    const numericValue = typeof value === 'string' ? parseFloat(value) : value
    if (isNaN(numericValue) || numericValue === 0) return 'text-gray-600'
    return isPositive ? (numericValue > 0 ? 'text-green-600' : 'text-red-600') : (numericValue < 0 ? 'text-green-600' : 'text-red-600')
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center gap-2">
        <h2 className="text-2xl font-bold text-slate-800">Comprehensive Evaluatory Metrics</h2>
      </div>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 items-end">
        {/* First Column: Performance Metrics and Monthly and Weekly Metrics */}
        <div className="flex flex-col space-y-6 h-full">
          {/* Performance Metrics */}
          <Card className="border-0 shadow-xl bg-white/90 backdrop-blur-sm flex-1">
            <CardHeader className="bg-gradient-to-r from-blue-50 to-indigo-50 border-b border-blue-100/50">
              <CardTitle className="text-lg text-slate-800">Performance Metrics</CardTitle>
            </CardHeader>
            <CardContent className="p-4 flex-1">
              <div className="space-y-3">
                <div>
                  <h4 className="text-sm font-semibold text-slate-700 mb-2">Returns</h4>
                  <div className="space-y-2 text-sm">
                    <div className="flex justify-between">
                      <span className="text-slate-600">Total Return</span>
                      <span className={`font-medium ${getValueColor(metrics.total_return)}`}>
                        {formatValue(metrics.total_return, true)}
                      </span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-slate-600">Daily Return</span>
                      <span className={`font-medium ${getValueColor(metrics.daily_return)}`}>
                        {formatValue(metrics.daily_return, true)}
                      </span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-slate-600">Weekly Return</span>
                      <span className={`font-medium ${getValueColor(metrics.weekly_return)}`}>
                        {formatValue(metrics.weekly_return, true)}
                      </span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-slate-600">Monthly Return</span>
                      <span className={`font-medium ${getValueColor(metrics.monthly_return)}`}>
                        {formatValue(metrics.monthly_return, true)}
                      </span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-slate-600">CAGR</span>
                      <span className={`font-medium ${getValueColor(metrics.cagr)}`}>
                        {formatValue(metrics.cagr, true)}
                      </span>
                    </div>
                  </div>
                </div>
                <div>
                  <h4 className="text-sm font-semibold text-slate-700 mb-2">Ratios</h4>
                  <div className="space-y-2 text-sm">
                    <div className="flex justify-between">
                      <span className="text-slate-600">Sharpe Ratio</span>
                      <span className="font-medium text-slate-800">{formatValue(metrics.sharpe_ratio)}</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-slate-600">Sortino Ratio</span>
                      <span className="font-medium text-slate-800">{formatValue(metrics.sortino_ratio)}</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-slate-600">Calmar Ratio</span>
                      <span className="font-medium text-slate-800">{formatValue(metrics.calmar_ratio)}</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-slate-600">Alpha</span>
                      <span className="font-medium text-slate-800">{formatValue(metrics.alpha)}</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-slate-600">Beta</span>
                      <span className="font-medium text-slate-800">{formatValue(metrics.beta)}</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-slate-600">R²</span>
                      <span className="font-medium text-slate-800">{formatValue(metrics.r_squared)}</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-slate-600">Information Ratio</span>
                      <span className="font-medium text-slate-800">{formatValue(metrics.information_ratio)}</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-slate-600">Treynor Ratio</span>
                      <span className="font-medium text-slate-800">{formatValue(metrics.treynor_ratio)}</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-slate-600">Profit Factor</span>
                      <span className="font-medium text-slate-800">{formatValue(metrics.profit_factor)}</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-slate-600">Omega Ratio</span>
                      <span className="font-medium text-slate-800">{formatValue(metrics.omega_ratio)}</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-slate-600">Gain to Pain Ratio</span>
                      <span className="font-medium text-slate-800">{formatValue(metrics.gain_to_pain_ratio)}</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-slate-600">Payoff Ratio</span>
                      <span className="font-medium text-slate-800">{formatValue(metrics.payoff_ratio)}</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-slate-600">CPC Ratio</span>
                      <span className="font-medium text-slate-800">{formatValue(metrics.cpc_ratio)}</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-slate-600">Risk-Return Ratio</span>
                      <span className="font-medium text-slate-800">{formatValue(metrics.risk_return_ratio)}</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-slate-600">Common Sense Ratio</span>
                      <span className="font-medium text-slate-800">{formatValue(metrics.common_sense_ratio)}</span>
                    </div>
                  </div>
                </div>
              </div>
            </CardContent>
          </Card>

          {/* Monthly and Weekly Metrics */}
          <Card className="border-0 shadow-xl bg-white/90 backdrop-blur-sm">
            <CardHeader className="bg-gradient-to-r from-cyan-50 to-blue-50 border-b border-cyan-100/50">
              <CardTitle className="text-lg text-slate-800">Monthly and Weekly Metrics</CardTitle>
            </CardHeader>
            <CardContent className="p-4">
              <div className="space-y-3">
                <div>
                  <h4 className="text-sm font-semibold text-slate-700 mb-2">Weekly</h4>
                  <div className="space-y-2 text-sm">
                    <div className="flex justify-between">
                      <span className="text-slate-600">Winning Weeks</span>
                      <span className="font-medium text-green-600">{formatValue(metrics.winning_weeks, false, false, 0)}</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-slate-600">Losing Weeks</span>
                      <span className="font-medium text-red-600">{formatValue(metrics.losing_weeks, false, false, 0)}</span>
                    </div>
                  </div>
                </div>
                <div>
                  <h4 className="text-sm font-semibold text-slate-700 mb-2">Monthly</h4>
                  <div className="space-y-2 text-sm">
                    <div className="flex justify-between">
                      <span className="text-slate-600">Winning Months</span>
                      <span className="font-medium text-green-600">{formatValue(metrics.winning_months, false, false, 0)}</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-slate-600">Losing Months</span>
                      <span className="font-medium text-red-600">{formatValue(metrics.losing_months, false, false, 0)}</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-slate-600">Winning Months (%)</span>
                      <span className="font-medium text-slate-800">{formatValue(metrics.winning_months_percent, true)}</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-slate-600">Negative Months (%)</span>
                      <span className="font-medium text-slate-800">{formatValue(metrics.negative_months_percent, true)}</span>
                    </div>
                  </div>
                </div>
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Second Column: Risk Metrics, Statistical Metrics, Profitability Metrics */}
        <div className="flex flex-col space-y-6 h-full">
          {/* Risk Metrics */}
          <Card className="border-0 shadow-xl bg-white/90 backdrop-blur-sm flex-1">
            <CardHeader className="bg-gradient-to-r from-red-50 to-pink-50 border-b border-red-100/50">
              <CardTitle className="text-lg text-slate-800">Risk Metrics</CardTitle>
            </CardHeader>
            <CardContent className="p-4 flex-1">
              <div className="space-y-3">
                <div>
                  <h4 className="text-sm font-semibold text-slate-700 mb-2">Drawdowns</h4>
                  <div className="space-y-2 text-sm">
                    <div className="flex justify-between">
                      <span className="text-slate-600">Max Drawdown</span>
                      <span className="font-medium text-red-600">{formatValue(metrics.max_drawdown, true)}</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-slate-600">Max Drawdown Days</span>
                      <span className="font-medium text-slate-800">{formatValue(metrics.max_drawdown_days, false, false, 0)}</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-slate-600">Avg Drawdown</span>
                      <span className="font-medium text-red-600">{formatValue(metrics.avg_drawdown, true)}</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-slate-600">Avg Drawdown Days</span>
                      <span className="font-medium text-slate-800">{formatValue(metrics.avg_drawdown_days, false, false, 0)}</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-slate-600">Current Drawdown</span>
                      <span className="font-medium text-red-600">{formatValue(metrics.current_drawdown, true)}</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-slate-600">Current Drawdown Days</span>
                      <span className="font-medium text-slate-800">{formatValue(metrics.current_drawdown_days, false, false, 0)}</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-slate-600">Drawdown Duration</span>
                      <span className="font-medium text-slate-800">{formatValue(metrics.drawdown_duration, false, false, 0)}</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-slate-600">Conditional Drawdown at Risk</span>
                      <span className="font-medium text-red-600">{formatValue(metrics.conditional_drawdown_at_risk, true)}</span>
                    </div>
                  </div>
                </div>
                <div>
                  <h4 className="text-sm font-semibold text-slate-700 mb-2">Risk Indicators</h4>
                  <div className="space-y-2 text-sm">
                    <div className="flex justify-between">
                      <span className="text-slate-600">Ulcer Index</span>
                      <span className="font-medium text-slate-800">{formatValue(metrics.ulcer_index, true)}</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-slate-600">Risk of Ruin</span>
                      <span className="font-medium text-red-600">{formatValue(metrics.risk_of_ruin, true)}</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-slate-600">VaR 95%</span>
                      <span className="font-medium text-red-600">{formatValue(metrics.var_95, true)}</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-slate-600">CVaR 99%</span>
                      <span className="font-medium text-red-600">{formatValue(metrics.cvar_99, true)}</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-slate-600">Downside Deviation</span>
                      <span className="font-medium text-slate-800">{formatValue(metrics.downside_deviation, true)}</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-slate-600">Volatility</span>
                      <span className="font-medium text-slate-800">{formatValue(metrics.volatility, true)}</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-slate-600">Annualized Volatility</span>
                      <span className="font-medium text-slate-800">{formatValue(metrics.annualized_volatility, true)}</span>
                    </div>
                  </div>
                </div>
              </div>
            </CardContent>
          </Card>

          {/* Statistical Metrics */}
          <Card className="border-0 shadow-xl bg-white/90 backdrop-blur-sm">
            <CardHeader className="bg-gradient-to-r from-purple-50 to-violet-50 border-b border-purple-100/50">
              <CardTitle className="text-lg text-slate-800">Statistical Metrics</CardTitle>
            </CardHeader>
            <CardContent className="p-4">
              <div className="space-y-3">
                <div>
                  <h4 className="text-sm font-semibold text-slate-700 mb-2">Distribution Metrics</h4>
                  <div className="space-y-2 text-sm">
                    <div className="flex justify-between">
                      <span className="text-slate-600">Skewness</span>
                      <span className="font-medium text-slate-800">{formatValue(metrics.skewness)}</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-slate-600">Kurtosis</span>
                      <span className="font-medium text-slate-800">{formatValue(metrics.kurtosis)}</span>
                    </div>
                  </div>
                </div>
              </div>
            </CardContent>
          </Card>

          {/* Profitability Metrics */}
          <Card className="border-0 shadow-xl bg-white/90 backdrop-blur-sm">
            <CardHeader className="bg-gradient-to-r from-yellow-50 to-orange-50 border-b border-yellow-100/50">
              <CardTitle className="text-lg text-slate-800">Profitability Metrics</CardTitle>
            </CardHeader>
            <CardContent className="p-4">
              <div className="space-y-3">
                <div>
                  <h4 className="text-sm font-semibold text-slate-700 mb-2">Profits and Losses</h4>
                  <div className="space-y-2 text-sm">
                    <div className="flex justify-between">
                      <span className="text-slate-600">Total Profit</span>
                      <span className="font-medium text-green-600">{formatValue(metrics.total_profit, true)}</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-slate-600">Net Profit</span>
                      <span className={`font-medium ${getValueColor(metrics.net_profit)}`}>
                        {formatValue(metrics.net_profit, true)}
                      </span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-slate-600">Avg Profit per Trade</span>
                      <span className="font-medium text-green-600">{formatValue(metrics.avg_profit_per_trade, true)}</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-slate-600">Avg Loss per Trade</span>
                      <span className="font-medium text-red-600">{formatValue(metrics.avg_loss_per_trade, true)}</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-slate-600">Profit Loss Ratio</span>
                      <span className="font-medium text-slate-800">{formatValue(metrics.profit_loss_ratio)}</span>
                    </div>
                  </div>
                </div>
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Third Column: Trade Metrics */}
        <div className="flex flex-col space-y-6 h-full">
          {/* Trade Metrics */}
          <Card className="border-0 shadow-xl bg-white/90 backdrop-blur-sm flex-1">
            <CardHeader className="bg-gradient-to-r from-green-50 to-emerald-50 border-b border-green-100/50">
              <CardTitle className="text-lg text-slate-800">Trade Metrics</CardTitle>
            </CardHeader>
            <CardContent className="p-4 flex-1">
              <div className="space-y-3">
                <div>
                  <h4 className="text-sm font-semibold text-slate-700 mb-2">Long Trades</h4>
                  <div className="space-y-2 text-sm">
                    <div className="flex justify-between">
                      <span className="text-slate-600">Total Long Return</span>
                      <span className={`font-medium ${getValueColor(metrics.total_long_return)}`}>
                        {formatValue(metrics.total_long_return, true)}
                      </span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-slate-600">Avg Long Return/Trade</span>
                      <span className={`font-medium ${getValueColor(metrics.avg_long_return_per_trade)}`}>
                        {formatValue(metrics.avg_long_return_per_trade, true)}
                      </span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-slate-600">Num Long Trades</span>
                      <span className="font-medium text-slate-800">{formatValue(metrics.num_long_trades, false, false, 0)}</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-slate-600">Win Rate Long</span>
                      <span className="font-medium text-slate-800">{formatValue(metrics.win_rate_long_trades, true)}</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-slate-600">Avg Long Trade Duration</span>
                      <span className="font-medium text-slate-800">{formatValue(metrics.avg_long_trade_duration, false, false, 2)} days</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-slate-600">Max Long Trade Return</span>
                      <span className={`font-medium ${getValueColor(metrics.max_long_trade_return)}`}>
                        {formatValue(metrics.max_long_trade_return, true)}
                      </span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-slate-600">Min Long Trade Return</span>
                      <span className={`font-medium ${getValueColor(metrics.min_long_trade_return)}`}>
                        {formatValue(metrics.min_long_trade_return, true)}
                      </span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-slate-600">Long Trades %</span>
                      <span className="font-medium text-slate-800">{formatValue(metrics.long_trades_percent, true)}</span>
                    </div>
                  </div>
                </div>
                <div>
                  <h4 className="text-sm font-semibold text-slate-700 mb-2">Short Trades</h4>
                  <div className="space-y-2 text-sm">
                    <div className="flex justify-between">
                      <span className="text-slate-600">Total Short Return</span>
                      <span className={`font-medium ${getValueColor(metrics.total_short_return)}`}>
                        {formatValue(metrics.total_short_return, true)}
                      </span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-slate-600">Avg Short Return/Trade</span>
                      <span className={`font-medium ${getValueColor(metrics.avg_short_return_per_trade)}`}>
                        {formatValue(metrics.avg_short_return_per_trade, true)}
                      </span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-slate-600">Num Short Trades</span>
                      <span className="font-medium text-slate-800">{formatValue(metrics.num_short_trades, false, false, 0)}</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-slate-600">Win Rate Short</span>
                      <span className="font-medium text-slate-800">{formatValue(metrics.win_rate_short_trades, true)}</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-slate-600">Avg Short Trade Duration</span>
                      <span className="font-medium text-slate-800">{formatValue(metrics.avg_short_trade_duration, false, false, 2)} days</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-slate-600">Max Short Trade Return</span>
                      <span className={`font-medium ${getValueColor(metrics.max_short_trade_return)}`}>
                        {formatValue(metrics.max_short_trade_return, true)}
                      </span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-slate-600">Min Short Trade Return</span>
                      <span className={`font-medium ${getValueColor(metrics.min_short_trade_return)}`}>
                        {formatValue(metrics.min_short_trade_return, true)}
                      </span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-slate-600">Short Trades %</span>
                      <span className="font-medium text-slate-800">{formatValue(metrics.short_trades_percent, true)}</span>
                    </div>
                  </div>
                </div>
                <div>
                  <h4 className="text-sm font-semibold text-slate-700 mb-2">Overall Trades</h4>
                  <div className="space-y-2 text-sm">
                    <div className="flex justify-between">
                      <span className="text-slate-600">Number of Trades</span>
                      <span className="font-medium text-slate-800">{formatValue(metrics.number_of_trades, false, false, 0)}</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-slate-600">Win Rate</span>
                      <span className="font-medium text-slate-800">{formatValue(metrics.win_rate, true)}</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-slate-600">Loss Rate</span>
                      <span className="font-medium text-slate-800">{formatValue(metrics.loss_rate, true)}</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-slate-600">Average Win</span>
                      <span className="font-medium text-green-600">{formatValue(metrics.average_win, true)}</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-slate-600">Average Loss</span>
                      <span className="font-medium text-red-600">{formatValue(metrics.average_loss, true)}</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-slate-600">Average Trade Duration</span>
                      <span className="font-medium text-slate-800">{formatValue(metrics.average_trade_duration, false, false, 2)} days</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-slate-600">Largest Win</span>
                      <span className="font-medium text-green-600">{formatValue(metrics.largest_win, true)}</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-slate-600">Largest Loss</span>
                      <span className="font-medium text-red-600">{formatValue(metrics.largest_loss, true)}</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-slate-600">Consecutive Wins</span>
                      <span className="font-medium text-slate-800">{formatValue(metrics.consecutive_wins, false, false, 0)}</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-slate-600">Consecutive Losses</span>
                      <span className="font-medium text-slate-800">{formatValue(metrics.consecutive_losses, false, false, 0)}</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-slate-600">Avg Trade Return</span>
                      <span className={`font-medium ${getValueColor(metrics.avg_trade_return)}`}>
                        {formatValue(metrics.avg_trade_return, true)}
                      </span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-slate-600">Profitability/Trade</span>
                      <span className="font-medium text-green-600">{formatValue(metrics.profitability_per_trade, true)}</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-slate-600">Recovery Factor</span>
                      <span className="font-medium text-slate-800">{formatValue(metrics.recovery_factor)}</span>
                    </div>
                  </div>
                </div>
              </div>
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  )
}
