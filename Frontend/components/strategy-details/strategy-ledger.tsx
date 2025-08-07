"use client"

import { useState } from "react"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { ChevronLeft, ChevronRight } from 'lucide-react'

interface StrategyLedgerProps {
  ledger: any[]
}

const ITEMS_PER_PAGE = 15

export function StrategyLedger({ ledger }: StrategyLedgerProps) {
  const [currentPage, setCurrentPage] = useState(1)

  const totalPages = Math.ceil(ledger.length / ITEMS_PER_PAGE)
  const startIndex = (currentPage - 1) * ITEMS_PER_PAGE
  const endIndex = startIndex + ITEMS_PER_PAGE
  const currentLedger = ledger.slice(startIndex, endIndex)

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleString()
  }

  const getPnLColor = (pnl: number) => {
    if (pnl > 0) return "text-green-600 bg-green-50 border-green-200"
    if (pnl < 0) return "text-red-600 bg-red-50 border-red-200"
    return "text-gray-600 bg-gray-50 border-gray-200"
  }

  const getActionBadgeColor = (action: string) => {
    switch (action.toLowerCase()) {
      case "buy":
        return "bg-blue-50 text-blue-700 border-blue-200"
      case "tp":
        return "bg-green-50 text-green-700 border-green-200"
      case "sl":
        return "bg-red-50 text-red-700 border-red-200"
      case "sell":
        return "bg-orange-50 text-orange-700 border-orange-200"
      case "direction_change":
        return "bg-purple-50 text-purple-700 border-purple-200"
      default:
        return "bg-gray-50 text-gray-700 border-gray-200"
    }
  }
  

  return (
    <Card className="border-0 shadow-xl bg-white/90 backdrop-blur-sm">
      <CardHeader className="bg-gradient-to-r from-purple-50 to-pink-50 border-b border-purple-100/50">
        <CardTitle className="text-xl text-slate-800">Strategy Ledger</CardTitle>
        <p className="text-sm text-slate-600">Detailed transaction history</p>
      </CardHeader>
      <CardContent className="p-0">
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead className="bg-gradient-to-r from-slate-50 to-purple-50/30 border-b border-purple-100/50">
              <tr>
                <th className="text-left p-4 font-semibold text-slate-700 text-sm">Date/Time</th>
                <th className="text-left p-4 font-semibold text-slate-700 text-sm">Action</th>
                <th className="text-left p-4 font-semibold text-slate-700 text-sm">Buy Price</th>
                <th className="text-left p-4 font-semibold text-slate-700 text-sm">Sell Price</th>
                <th className="text-left p-4 font-semibold text-slate-700 text-sm">PnL %</th>
                <th className="text-left p-4 font-semibold text-slate-700 text-sm">PnL Sum</th>
                <th className="text-left p-4 font-semibold text-slate-700 text-sm">Balance</th>
              </tr>
            </thead>
            <tbody>
              {currentLedger.map((trade, index) => (
                <tr
                  key={index}
                  className={`border-b border-purple-50/50 hover:bg-gradient-to-r hover:from-purple-25/50 hover:to-pink-25/50 transition-all duration-300 ${
                    index % 2 === 0 ? "bg-white/50" : "bg-purple-25/20"
                  }`}
                >
                  <td className="p-4 text-sm text-slate-800">{formatDate(trade.datetime)}</td>
                  <td className="p-4">
                    <Badge variant="outline" className={getActionBadgeColor(trade.action)}>
                      {trade.action}
                    </Badge>
                  </td>
                  <td className="p-4 text-sm text-slate-600">${(trade.buy_price || 0).toFixed(2)}</td>
                  <td className="p-4 text-sm text-slate-600">${(trade.sell_price || 0).toFixed(2)}</td>
                  <td className="p-4">
                    <Badge variant="outline" className={getPnLColor(trade.pnl_percent || 0)}>
                      {(trade.pnl_percent || 0).toFixed(2)}%
                    </Badge>
                  </td>
                  <td className="p-4">
                    <Badge variant="outline" className={getPnLColor(trade.pnl_sum || 0)}>
                      {(trade.pnl_sum || 0).toFixed(2)}
                    </Badge>
                  </td>
                  <td className="p-4 text-sm text-slate-700">${(trade.balance || 0).toFixed(2)}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>

        {/* Pagination */}
        {totalPages > 1 && (
          <div className="flex items-center justify-between p-6 bg-gradient-to-r from-purple-50/30 to-pink-50/30 border-t border-purple-100/50">
            <div className="text-sm text-slate-600">
              Showing {startIndex + 1} to {Math.min(endIndex, ledger.length)} of {ledger.length} trades
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
                    pageNum = i + 1
                  } else if (currentPage <= 3) {
                    pageNum = i + 1
                  } else if (currentPage >= totalPages - 2) {
                    pageNum = totalPages - 4 + i
                  } else {
                    pageNum = currentPage - 2 + i
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
                  )
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
      </CardContent>
    </Card>
  )
}
