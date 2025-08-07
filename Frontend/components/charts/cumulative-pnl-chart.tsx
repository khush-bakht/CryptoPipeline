"use client"

import { Area, AreaChart, ResponsiveContainer, Tooltip, XAxis, YAxis, CartesianGrid } from "recharts"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { TrendingUp, TrendingDown } from "lucide-react"

interface PnLDataPoint {
  datetime: string
  pnl_sum: number
}

interface CumulativePnLChartProps {
  data: PnLDataPoint[]
}

export function CumulativePnLChart({ data }: CumulativePnLChartProps) {
  const chartData = data.map(point => ({
    date: new Date(point.datetime).toLocaleDateString(),
    pnl: point.pnl_sum || 0
  }))

  // Calculate performance metrics
  const totalPnL = data.length > 0 ? data[data.length - 1]?.pnl_sum || 0 : 0
  const isPositive = totalPnL >= 0
  const performanceColor = isPositive ? "text-emerald-600" : "text-red-600"
  const performanceIcon = isPositive ? TrendingUp : TrendingDown

  return (
    <Card className="border-0 shadow-xl bg-white/95 backdrop-blur-sm overflow-hidden">
      <CardHeader className="bg-gradient-to-r from-slate-50 to-gray-50 border-b border-slate-200/50">
        <div className="flex items-center justify-between">
          <CardTitle className="text-xl font-semibold text-slate-800 flex items-center gap-2">
            <div className="p-2 bg-gradient-to-br from-emerald-100 to-teal-100 rounded-lg">
              <TrendingUp className="h-5 w-5 text-emerald-600" />
            </div>
            Cumulative P&L Performance
          </CardTitle>
          <div className="flex items-center gap-2">
            <TrendingUp className={`h-4 w-4 ${performanceColor}`} />
            <span className={`text-sm font-semibold ${performanceColor}`}>
              {totalPnL.toFixed(2)}
            </span>
          </div>
        </div>
      </CardHeader>
      <CardContent className="p-6">
        <div className="h-80">
          <ResponsiveContainer width="100%" height="100%">
            <AreaChart data={chartData} margin={{ top: 10, right: 30, left: 0, bottom: 0 }}>
              <defs>
                <linearGradient id="pnlGradient" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="5%" stopColor="#10b981" stopOpacity={0.4}/>
                  <stop offset="95%" stopColor="#10b981" stopOpacity={0.05}/>
                </linearGradient>
                <linearGradient id="pnlGradientNegative" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="5%" stopColor="#ef4444" stopOpacity={0.4}/>
                  <stop offset="95%" stopColor="#ef4444" stopOpacity={0.05}/>
                </linearGradient>
              </defs>
              <CartesianGrid 
                strokeDasharray="3 3" 
                stroke="#f1f5f9" 
                vertical={false}
              />
              <XAxis 
                dataKey="date" 
                axisLine={false}
                tickLine={false}
                tick={{ fontSize: 11, fill: '#64748b', fontWeight: 500 }}
                tickMargin={8}
              />
              <YAxis 
                axisLine={false}
                tickLine={false}
                tick={{ fontSize: 11, fill: '#64748b', fontWeight: 500 }}
                tickMargin={8}
                tickFormatter={(value) => `${value.toFixed(1)}`}
              />
              <Tooltip 
                contentStyle={{
                  backgroundColor: 'white',
                  border: '1px solid #e2e8f0',
                  borderRadius: '12px',
                  boxShadow: '0 10px 25px -5px rgb(0 0 0 / 0.1), 0 4px 6px -2px rgb(0 0 0 / 0.05)',
                  padding: '12px 16px'
                }}
                labelStyle={{
                  fontWeight: 600,
                  color: '#1e293b'
                }}
                formatter={(value: any) => [`${value.toFixed(2)}`, 'P&L']}
                labelFormatter={(label) => `Date: ${label}`}
              />
              <Area
                type="monotone"
                dataKey="pnl"
                stroke={isPositive ? "#10b981" : "#ef4444"}
                strokeWidth={3}
                fill={isPositive ? "url(#pnlGradient)" : "url(#pnlGradientNegative)"}
              />
            </AreaChart>
          </ResponsiveContainer>
        </div>
        
  
        
      </CardContent>
    </Card>
  )
}
