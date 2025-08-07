"use client"

import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"

interface StrategyConfigurationProps {
  config: any // The strategy_config data
}

export function StrategyConfiguration({ config }: StrategyConfigurationProps) {
  const renderValue = (value: any) => {
    if (typeof value === 'boolean') {
      return (
        <Badge variant="outline" className={value ? "text-green-700 bg-green-50 border-green-200" : "text-gray-600 bg-gray-50 border-gray-200"}>
          {value ? 'True' : 'False'}
        </Badge>
      )
    }
    if (typeof value === 'number') {
      return <span className="font-medium text-slate-800">{value}</span>
    }
    if (typeof value === 'string') {
      return <span className="font-medium text-slate-800">{value}</span>
    }
    return <span className="text-gray-500">-</span>
  }

  const generalFields = [
    { key: 'name', label: 'name' },
    { key: 'symbol', label: 'symbol' },
    { key: 'time_horizon', label: 'time horizon' },
    { key: 'exchange', label: 'data exchange' },
    { key: 'sma', label: 'use_ml' },
    { key: 'ema', label: 'use_pattern' },
    { key: 'macd', label: 'use_filters' },
    { key: 'rsi', label: 'is_live' },
    { key: 'adx', label: 'simulator' },
    { key: 'bbands', label: 'execution' },
    { key: 'stoch', label: 'priority' },
    { key: 'atr', label: 'use_fib_levels' },
    { key: 'cci', label: 'use_head_shoulders' },
    { key: 'willr', label: 'use_cup_handle' }
  ]

  const filterFields = [
    { key: 'rsi', label: 'filters_use_rsi' },
    { key: 'stochrsi', label: 'filters_use_stoch_rsi' },
    { key: 'bbands', label: 'filters_use_bbands' },
    { key: 'sma', label: 'filters_use_sma' },
    { key: 'ema', label: 'filters_use_ema' },
    { key: 'macd', label: 'filters_use_macd' },
    { key: 'sar', label: 'filters_use_psar' },
    { key: 'adx', label: 'filters_use_adx' },
    { key: 'stoch', label: 'filters_use_stoch_osc' },
    { key: 'aroon', label: 'filters_use_longshort' },
    { key: 'mfi', label: 'filters_percent_required' }
  ]

  const patternsFields = [
    { key: 'cdl2crows', label: 'patterns_use_complete_patterns' },
    { key: 'cdl3blackcrows', label: 'patterns_use_incomplete_patterns' },
    { key: 'cdl3inside', label: 'patterns_list_complete_patterns' },
    { key: 'cdl3linestrike', label: 'patterns_list_incomplete_patterns' },
    { key: 'tp', label: 'patterns_window' },
    { key: 'sl', label: 'patterns_sl_ratio' },
    { key: 'sma_window', label: 'patterns_tp1_ratio' },
    { key: 'ema_window', label: 'patterns_tp2_ratio' },
    { key: 'rsi_window', label: 'patterns_allowed_error' },
    { key: 'adx_window', label: 'patterns_tie_breaker' }
  ]

  const emaFields = [
    { key: 'ema_window', label: 'ema_window' }
  ]

  const adxFields = [
    { key: 'adx_window', label: 'adx_window' }
  ]

  const liveFields = [
    { key: 'live_tp_sl', label: 'live_tp_sl', staticValue: 'static' },
    { key: 'tp', label: 'live_tp_percent' },
    { key: 'sl', label: 'live_sl_percent' }
  ]

  const renderSection = (title: string, fields: any[], bgColor: string = "bg-white") => (
    <Card className={`border border-gray-200 shadow-sm ${bgColor}`}>
      <CardHeader className="bg-gray-50 border-b border-gray-200 py-3 px-4">
        <CardTitle className="text-sm font-semibold text-gray-700 uppercase tracking-wide">
          {title}
        </CardTitle>
      </CardHeader>
      <CardContent className="p-4 space-y-3">
        {fields.map((field, index) => (
          <div key={index} className="flex justify-between items-center py-1">
            <span className="text-sm text-gray-600">{field.label}</span>
            <div className="text-right">
              {field.staticValue ? (
                <span className="font-medium text-slate-800">{field.staticValue}</span>
              ) : (
                renderValue(config[field.key])
              )}
            </div>
          </div>
        ))}
      </CardContent>
    </Card>
  )

  return (
    <div className="space-y-6">
      <div className="flex items-center gap-2 mb-6">
        <h2 className="text-2xl font-bold text-slate-800">Strategies</h2>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 xl:grid-cols-3 gap-6">
        {/* General Section */}
        {renderSection("General", generalFields)}

        {/* Filters Section */}
        {renderSection("Filters", filterFields)}

        {/* Patterns Use Section */}
        {renderSection("Patterns Use", patternsFields)}

        {/* EMA Section */}
        {renderSection("EMA", emaFields)}

        {/* ADX Section */}
        {renderSection("ADX", adxFields)}

        {/* Live Section */}
        {renderSection("Live", liveFields)}
      </div>
    </div>
  )
}
