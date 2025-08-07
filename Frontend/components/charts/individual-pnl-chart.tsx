"use client"

import { Bar, BarChart, ResponsiveContainer, Tooltip, XAxis, YAxis, Cell } from "recharts"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"

interface PnLDataPoint {
  datetime: string
  pnl_sum: number
}

interface IndividualPnLChartProps {
  data: PnLDataPoint[]
}

export function IndividualPnLChart({ data }: IndividualPnLChartProps) {
  const chartData = data.map((point, index) => {
    const prevPnL = index > 0 ? data[index - 1].pnl_sum : 0
    const individualPnL = (point.pnl_sum || 0) - prevPnL
    
    return {
      date: new Date(point.datetime).toLocaleDateString(),
      pnl: individualPnL,
      isProfit: individualPnL >= 0
    }
  }).filter(point => point.pnl !== 0) // Remove zero P&L entries

  return (
    <Card className="border-0 shadow-xl bg-white/90 backdrop-blur-sm">
      <CardHeader className="bg-gradient-to-r from-purple-50 to-pink-50 border-b border-purple-100/50">
        <CardTitle className="text-xl text-slate-800">Individual Trade P&L</CardTitle>
        <p className="text-sm text-slate-600">Per-trade profit and loss breakdown</p>
      </CardHeader>
      <CardContent className="p-6">
        <div className="h-80">
          <ResponsiveContainer width="100%" height="100%">
            <BarChart data={chartData} margin={{ top: 20, right: 30, left: 20, bottom: 5 }}>
              <XAxis 
                dataKey="date" 
                axisLine={false}
                tickLine={false}
                tick={false}
                angle={-45}
                textAnchor="end"
                height={80}
              />
              <YAxis 
                axisLine={false}
                tickLine={false}
                tick={{ fontSize: 12, fill: '#64748b' }}
              />
              <Tooltip 
                contentStyle={{
                  backgroundColor: 'white',
                  border: '1px solid #e2e8f0',
                  borderRadius: '8px',
                  boxShadow: '0 4px 6px -1px rgb(0 0 0 / 0.1)'
                }}
                formatter={(value: any) => [
                  `${value >= 0 ? '+' : ''}${value.toFixed(2)}%`,
                  'P&L'
                ]}
                labelFormatter={(label) => `Trade on ${label}`}
              />
              <Bar dataKey="pnl" radius={[2, 2, 0, 0]}>
                {chartData.map((entry, index) => (
                  <Cell 
                    key={`cell-${index}`} 
                    fill={entry.isProfit ? '#10b981' : '#ef4444'} 
                  />
                ))}
              </Bar>
            </BarChart>
          </ResponsiveContainer>
        </div>
        
        
      </CardContent>
    </Card>
  )
}
