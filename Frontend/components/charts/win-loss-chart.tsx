"use client"

import { PieChart, Pie, Cell, ResponsiveContainer, Tooltip, Legend } from "recharts"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"

interface WinLossChartProps {
  wins: number
  losses: number
}

export function WinLossChart({ wins, losses }: WinLossChartProps) {
  const total = wins + losses
  const winRate = total > 0 ? (wins / total * 100).toFixed(1) : 0
  const lossRate = total > 0 ? (losses / total * 100).toFixed(1) : 0

  const data = [
    { name: 'Wins', value: wins, percentage: winRate },
    { name: 'Losses', value: losses, percentage: lossRate }
  ]

  const COLORS = ['#10b981', '#ef4444']

  return (
    <Card className="border-0 shadow-xl bg-white/90 backdrop-blur-sm">
      <CardHeader className="bg-gradient-to-r from-purple-50 to-pink-50 border-b border-purple-100/50">
        <CardTitle className="text-xl text-slate-800">Win/Loss Distribution</CardTitle>
        <p className="text-sm text-slate-600">Trade outcome breakdown</p>
      </CardHeader>
      <CardContent className="p-6">
        <div className="h-80">
          <ResponsiveContainer width="100%" height="100%">
            <PieChart>
              <Pie
                data={data}
                cx="50%"
                cy="50%"
                innerRadius={60}
                outerRadius={100}
                paddingAngle={5}
                dataKey="value"
              >
                {data.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                ))}
              </Pie>
              <Tooltip 
                formatter={(value: any, name: string) => [
                  `${value} trades (${data.find(d => d.name === name)?.percentage}%)`,
                  name
                ]}
              />
              <Legend />
            </PieChart>
          </ResponsiveContainer>
        </div>
      </CardContent>
    </Card>
  )
}
