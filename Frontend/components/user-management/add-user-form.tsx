"use client"

import { useState } from "react"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Badge } from "@/components/ui/badge"
import { X, Plus, Eye, EyeOff } from 'lucide-react'
import { toast } from "sonner"

interface Strategy {
  name: string
  symbol: string
  exchange: string
  time_horizon: string
}

interface StrategiesBySymbol {
  [symbol: string]: Strategy[]
}

interface AddUserFormProps {
  onUserAdded: () => void
  strategiesBySymbol: StrategiesBySymbol
}

export function AddUserForm({ onUserAdded, strategiesBySymbol }: AddUserFormProps) {
  const [formData, setFormData] = useState({
    name: "",
    email: "",
    password: "",
    api_key: "",
    api_secret: ""
  })
  const [assignedStrategies, setAssignedStrategies] = useState<Strategy[]>([])
  const [showPassword, setShowPassword] = useState(false)
  const [showApiSecret, setShowApiSecret] = useState(false)
  const [isSubmitting, setIsSubmitting] = useState(false)
  const [errors, setErrors] = useState<{[key: string]: string}>({})

  // Validation patterns
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
  const passwordRegex = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$/
  const apiKeyRegex = /^[A-Za-z0-9]{20,}$/

  const validateForm = () => {
    const newErrors: {[key: string]: string} = {}

    if (!formData.name.trim()) {
      newErrors.name = "Name is required"
    }

    if (!formData.email.trim()) {
      newErrors.email = "Email is required"
    } else if (!emailRegex.test(formData.email)) {
      newErrors.email = "Please enter a valid email address"
    }

    if (!formData.password) {
      newErrors.password = "Password is required"
    } else if (!passwordRegex.test(formData.password)) {
      newErrors.password = "Password must be at least 8 characters with uppercase, lowercase, number, and special character"
    }

    if (formData.api_key && !apiKeyRegex.test(formData.api_key)) {
      newErrors.api_key = "API Key must be at least 20 alphanumeric characters"
    }

    if (formData.api_secret && formData.api_secret.length < 20) {
      newErrors.api_secret = "API Secret must be at least 20 characters"
    }

    setErrors(newErrors)
    return Object.keys(newErrors).length === 0
  }

  const handleInputChange = (field: string, value: string) => {
    setFormData(prev => ({ ...prev, [field]: value }))
    // Clear error when user starts typing
    if (errors[field]) {
      setErrors(prev => ({ ...prev, [field]: "" }))
    }
  }

  const addStrategy = (strategy: Strategy) => {
    // Check if symbol already exists
    const symbolExists = assignedStrategies.some(s => s.symbol === strategy.symbol)
    if (symbolExists) {
      toast.error(`A strategy with symbol ${strategy.symbol.toUpperCase()} is already assigned`)
      return
    }

    setAssignedStrategies(prev => [...prev, strategy])
  }

  const removeStrategy = (strategyName: string) => {
    setAssignedStrategies(prev => prev.filter(s => s.name !== strategyName))
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    
    if (!validateForm()) {
      return
    }

    setIsSubmitting(true)

    try {
      const response = await fetch("http://localhost:3001/api/users", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          ...formData,
          assigned_strategies: assignedStrategies
        }),
      })

      if (!response.ok) {
        const errorData = await response.json()
        throw new Error(errorData.error || "Failed to add user")
      }

      toast.success("User added successfully!")
      
      // Reset form
      setFormData({
        name: "",
        email: "",
        password: "",
        api_key: "",
        api_secret: ""
      })
      setAssignedStrategies([])
      setErrors({})
      
      onUserAdded()
    } catch (error) {
      toast.error(error instanceof Error ? error.message : "Failed to add user")
    } finally {
      setIsSubmitting(false)
    }
  }

  return (
    <Card className="border-0 shadow-xl bg-white/90 backdrop-blur-sm">
      <CardHeader className="bg-gradient-to-r from-purple-50 to-pink-50 border-b border-purple-100/50">
        <CardTitle className="text-xl text-slate-800">Add New User</CardTitle>
      </CardHeader>
      <CardContent className="p-6">
        <form onSubmit={handleSubmit} className="space-y-6">
          {/* Basic Information */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div className="space-y-2">
              <Label htmlFor="name">Name *</Label>
              <Input
                id="name"
                value={formData.name}
                onChange={(e) => handleInputChange("name", e.target.value)}
                placeholder="Enter full name"
                className={errors.name ? "border-red-500" : ""}
              />
              {errors.name && <p className="text-sm text-red-600">{errors.name}</p>}
            </div>

            <div className="space-y-2">
              <Label htmlFor="email">Email *</Label>
              <Input
                id="email"
                type="email"
                value={formData.email}
                onChange={(e) => handleInputChange("email", e.target.value)}
                placeholder="Enter email address"
                className={errors.email ? "border-red-500" : ""}
              />
              {errors.email && <p className="text-sm text-red-600">{errors.email}</p>}
            </div>
          </div>

          {/* Password */}
          <div className="space-y-2">
            <Label htmlFor="password">Password *</Label>
            <div className="relative">
              <Input
                id="password"
                type={showPassword ? "text" : "password"}
                value={formData.password}
                onChange={(e) => handleInputChange("password", e.target.value)}
                placeholder="Enter password"
                className={errors.password ? "border-red-500 pr-10" : "pr-10"}
              />
              <Button
                type="button"
                variant="ghost"
                size="sm"
                className="absolute right-0 top-0 h-full px-3 py-2 hover:bg-transparent"
                onClick={() => setShowPassword(!showPassword)}
              >
                {showPassword ? <EyeOff className="h-4 w-4" /> : <Eye className="h-4 w-4" />}
              </Button>
            </div>
            {errors.password && <p className="text-sm text-red-600">{errors.password}</p>}
            <p className="text-xs text-slate-500">
              Must contain at least 8 characters with uppercase, lowercase, number, and special character
            </p>
          </div>

          {/* API Credentials */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div className="space-y-2">
              <Label htmlFor="api_key">API Key</Label>
              <Input
                id="api_key"
                value={formData.api_key}
                onChange={(e) => handleInputChange("api_key", e.target.value)}
                placeholder="Enter API key (optional)"
                className={errors.api_key ? "border-red-500" : ""}
              />
              {errors.api_key && <p className="text-sm text-red-600">{errors.api_key}</p>}
            </div>

            <div className="space-y-2">
              <Label htmlFor="api_secret">API Secret</Label>
              <div className="relative">
                <Input
                  id="api_secret"
                  type={showApiSecret ? "text" : "password"}
                  value={formData.api_secret}
                  onChange={(e) => handleInputChange("api_secret", e.target.value)}
                  placeholder="Enter API secret (optional)"
                  className={errors.api_secret ? "border-red-500 pr-10" : "pr-10"}
                />
                <Button
                  type="button"
                  variant="ghost"
                  size="sm"
                  className="absolute right-0 top-0 h-full px-3 py-2 hover:bg-transparent"
                  onClick={() => setShowApiSecret(!showApiSecret)}
                >
                  {showApiSecret ? <EyeOff className="h-4 w-4" /> : <Eye className="h-4 w-4" />}
                </Button>
              </div>
              {errors.api_secret && <p className="text-sm text-red-600">{errors.api_secret}</p>}
            </div>
          </div>

          {/* Strategy Assignment */}
          <div className="space-y-4">
            <Label>Assign Strategies</Label>
            <p className="text-sm text-slate-600">
              Select strategies to assign to this user. Only one strategy per symbol is allowed.
            </p>

            {/* Available Strategies by Symbol */}
            <div className="space-y-4">
              {Object.entries(strategiesBySymbol).map(([symbol, strategies]) => {
                const isSymbolAssigned = assignedStrategies.some(s => s.symbol === symbol)
                
                return (
                  <div key={symbol} className="border rounded-lg p-4">
                    <h4 className="font-semibold text-slate-700 mb-2 flex items-center gap-2">
                      {symbol.toUpperCase()}
                      {isSymbolAssigned && (
                        <Badge variant="outline" className="bg-green-50 text-green-700 border-green-200">
                          Assigned
                        </Badge>
                      )}
                    </h4>
                    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-2">
                      {strategies.map((strategy) => (
                        <Button
                          key={strategy.name}
                          type="button"
                          variant="outline"
                          size="sm"
                          disabled={isSymbolAssigned}
                          onClick={() => addStrategy(strategy)}
                          className="justify-start text-left h-auto p-3"
                        >
                          <div>
                            <div className="font-medium">{strategy.name}</div>
                            <div className="text-xs text-slate-500">
                              {strategy.exchange} • {strategy.time_horizon}
                            </div>
                          </div>
                        </Button>
                      ))}
                    </div>
                  </div>
                )
              })}
            </div>

            {/* Assigned Strategies */}
            {assignedStrategies.length > 0 && (
              <div className="space-y-2">
                <Label>Assigned Strategies ({assignedStrategies.length})</Label>
                <div className="flex flex-wrap gap-2">
                  {assignedStrategies.map((strategy) => (
                    <Badge
                      key={strategy.name}
                      variant="outline"
                      className="bg-purple-50 text-purple-700 border-purple-200 pr-1"
                    >
                      <span className="mr-2">
                        {strategy.name} ({strategy.symbol.toUpperCase()})
                      </span>
                      <Button
                        type="button"
                        variant="ghost"
                        size="sm"
                        className="h-4 w-4 p-0 hover:bg-purple-100"
                        onClick={() => removeStrategy(strategy.name)}
                      >
                        <X className="h-3 w-3" />
                      </Button>
                    </Badge>
                  ))}
                </div>
              </div>
            )}
          </div>

          {/* Submit Button */}
          <div className="flex justify-end">
            <Button
              type="submit"
              disabled={isSubmitting}
              className="bg-gradient-to-r from-purple-500 to-pink-500 hover:from-purple-600 hover:to-pink-600 text-white"
            >
              {isSubmitting ? "Adding User..." : "Add User"}
            </Button>
          </div>
        </form>
      </CardContent>
    </Card>
  )
}
