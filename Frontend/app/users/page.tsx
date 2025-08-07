"use client"

import { useEffect, useState } from "react"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Users, Sparkles, TrendingUp, Brain, BarChart3, Plus, RefreshCw, UserPlus } from 'lucide-react'
import Link from "next/link"
import { AddUserForm } from "@/components/user-management/add-user-form"
import { UsersList } from "@/components/user-management/users-list"
import { Toaster } from "sonner"

interface User {
  email: string
  name: string
  api_key?: string
  assigned_strategies: any[]
  created_at: string
  updated_at: string
}

interface StrategiesBySymbol {
  [symbol: string]: any[]
}

export default function UsersPage() {
  const [users, setUsers] = useState<User[]>([])
  const [strategiesBySymbol, setStrategiesBySymbol] = useState<StrategiesBySymbol>({})
  const [loading, setLoading] = useState(true)
  const [showAddForm, setShowAddForm] = useState(false)

  useEffect(() => {
    fetchUsers()
    fetchStrategies()
  }, [])

  const fetchUsers = async () => {
    try {
      const response = await fetch("http://localhost:3001/api/users")
      if (response.ok) {
        const data = await response.json()
        setUsers(data)
      }
    } catch (error) {
      console.error("Error fetching users:", error)
    } finally {
      setLoading(false)
    }
  }

  const fetchStrategies = async () => {
    try {
      const response = await fetch("http://localhost:3001/api/strategies/available")
      if (response.ok) {
        const data = await response.json()
        setStrategiesBySymbol(data)
      }
    } catch (error) {
      console.error("Error fetching strategies:", error)
    }
  }

  const handleUserAdded = () => {
    fetchUsers()
    setShowAddForm(false)
  }

  const handleUserDeleted = () => {
    fetchUsers()
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-rose-50 via-purple-50 to-teal-50">
      <Toaster position="top-right" />
      
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
                  className="text-purple-600 hover:bg-purple-50 font-medium hover:shadow-sm transition-all duration-200"
                >
                  <TrendingUp className="h-4 w-4 mr-2" />
                  Strategy Simulator
                </Button>
              </Link>
              <Link href="/users">
                <Button
                  variant="ghost"
                  className="text-teal-600 hover:bg-teal-50 font-medium bg-teal-50/80 shadow-sm border border-teal-100"
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
          <div className="inline-flex items-center gap-2 bg-white/70 backdrop-blur-sm px-6 py-3 rounded-full border border-teal-200/50 shadow-lg">
            <Users className="h-5 w-5 text-teal-500" />
            <span className="text-sm text-teal-700 font-semibold tracking-wide">
              User Management System
            </span>
          </div>
          <h1 className="text-4xl font-bold bg-gradient-to-r from-teal-600 via-cyan-600 to-blue-600 bg-clip-text text-transparent">
            Manage Users
          </h1>
          <p className="text-slate-600 text-lg max-w-2xl mx-auto">
            Add, manage, and assign trading strategies to users with comprehensive access control
          </p>
        </div>

        {/* Statistics */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <Card className="border-0 shadow-lg bg-gradient-to-br from-white/80 to-teal-50/50 backdrop-blur-sm">
            <CardContent className="p-6">
              <div className="flex items-center gap-4">
                <div className="p-3 bg-gradient-to-br from-teal-100 to-cyan-100 rounded-xl">
                  <Users className="h-6 w-6 text-teal-600" />
                </div>
                <div>
                  <p className="text-sm font-medium text-slate-600">Total Users</p>
                  <p className="text-2xl font-bold text-slate-800">{users.length}</p>
                </div>
              </div>
            </CardContent>
          </Card>

          <Card className="border-0 shadow-lg bg-gradient-to-br from-white/80 to-green-50/50 backdrop-blur-sm">
            <CardContent className="p-6">
              <div className="flex items-center gap-4">
                <div className="p-3 bg-gradient-to-br from-green-100 to-emerald-100 rounded-xl">
                  <UserPlus className="h-6 w-6 text-green-600" />
                </div>
                <div>
                  <p className="text-sm font-medium text-slate-600">Active Users</p>
                  <p className="text-2xl font-bold text-green-600">
                    {users.filter(u => u.api_key).length}
                  </p>
                </div>
              </div>
            </CardContent>
          </Card>

          <Card className="border-0 shadow-lg bg-gradient-to-br from-white/80 to-purple-50/50 backdrop-blur-sm">
            <CardContent className="p-6">
              <div className="flex items-center gap-4">
                <div className="p-3 bg-gradient-to-br from-purple-100 to-pink-100 rounded-xl">
                  <TrendingUp className="h-6 w-6 text-purple-600" />
                </div>
                <div>
                  <p className="text-sm font-medium text-slate-600">Strategies Assigned</p>
                  <p className="text-2xl font-bold text-purple-600">
                    {users.reduce((total, user) => total + (user.assigned_strategies?.length || 0), 0)}
                  </p>
                </div>
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Action Buttons */}
        <div className="flex justify-center gap-4">
          <Button
            onClick={() => setShowAddForm(!showAddForm)}
            className="bg-gradient-to-r from-teal-500 to-cyan-500 hover:from-teal-600 hover:to-cyan-600 text-white shadow-lg hover:shadow-xl transition-all duration-300 h-12 px-8 rounded-xl"
          >
            <Plus className="h-5 w-5 mr-2" />
            {showAddForm ? "Cancel" : "Add New User"}
          </Button>
          
          <Button
            onClick={fetchUsers}
            disabled={loading}
            variant="outline"
            className="border-teal-200 text-teal-600 hover:bg-teal-50 shadow-lg hover:shadow-xl transition-all duration-300 h-12 px-8 rounded-xl"
          >
            <RefreshCw className={`h-5 w-5 mr-2 ${loading ? "animate-spin" : ""}`} />
            Refresh
          </Button>
        </div>

        {/* Add User Form */}
        {showAddForm && (
          <AddUserForm
            onUserAdded={handleUserAdded}
            strategiesBySymbol={strategiesBySymbol}
          />
        )}

        {/* Users List */}
        {loading ? (
          <div className="flex flex-col items-center justify-center py-16 space-y-4">
            <div className="p-4 bg-gradient-to-br from-teal-100 to-cyan-100 rounded-full">
              <RefreshCw className="h-8 w-8 animate-spin text-teal-600" />
            </div>
            <div className="text-center">
              <p className="text-slate-600 font-medium">Loading users...</p>
              <p className="text-sm text-slate-500">Fetching user data</p>
            </div>
          </div>
        ) : (
          <UsersList users={users} onUserDeleted={handleUserDeleted} />
        )}
      </div>
    </div>
  )
}
