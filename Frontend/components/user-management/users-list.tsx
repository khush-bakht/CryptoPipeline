"use client"

import { useState } from "react"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import { Trash2, Users, Calendar, Key } from 'lucide-react'
import { toast } from "sonner"
import {
  AlertDialog,
  AlertDialogAction,
  AlertDialogCancel,
  AlertDialogContent,
  AlertDialogDescription,
  AlertDialogFooter,
  AlertDialogHeader,
  AlertDialogTitle,
  AlertDialogTrigger,
} from "@/components/ui/alert-dialog"

interface User {
  email: string
  name: string
  api_key?: string
  assigned_strategies: any[]
  created_at: string
  updated_at: string
}

interface UsersListProps {
  users: User[]
  onUserDeleted: () => void
}

export function UsersList({ users, onUserDeleted }: UsersListProps) {
  const [deletingUser, setDeletingUser] = useState<string | null>(null)

  const handleDeleteUser = async (email: string) => {
    setDeletingUser(email)

    try {
      const response = await fetch(`http://localhost:3001/api/users/${encodeURIComponent(email)}`, {
        method: "DELETE",
      })

      if (!response.ok) {
        const errorData = await response.json()
        throw new Error(errorData.error || "Failed to delete user")
      }

      toast.success("User deleted successfully!")
      onUserDeleted()
    } catch (error) {
      toast.error(error instanceof Error ? error.message : "Failed to delete user")
    } finally {
      setDeletingUser(null)
    }
  }

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    })
  }

  if (users.length === 0) {
    return (
      <Card className="border-0 shadow-xl bg-white/90 backdrop-blur-sm">
        <CardContent className="p-12 text-center">
          <div className="p-4 bg-gradient-to-br from-slate-100 to-purple-100 rounded-full w-fit mx-auto mb-4">
            <Users className="h-8 w-8 text-slate-500" />
          </div>
          <h3 className="text-lg font-semibold text-slate-800 mb-2">No Users Found</h3>
          <p className="text-slate-600">Add your first user to get started.</p>
        </CardContent>
      </Card>
    )
  }

  return (
    <Card className="border-0 shadow-xl bg-white/90 backdrop-blur-sm">
      <CardHeader className="bg-gradient-to-r from-teal-50 to-cyan-50 border-b border-teal-100/50">
        <CardTitle className="text-xl text-slate-800 flex items-center gap-2">
          <Users className="h-5 w-5" />
          All Users ({users.length})
        </CardTitle>
      </CardHeader>
      <CardContent className="p-0">
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead className="bg-gradient-to-r from-slate-50 to-teal-50/30 border-b border-teal-100/50">
              <tr>
                <th className="text-left p-4 font-semibold text-slate-700 text-sm">User Details</th>
                <th className="text-left p-4 font-semibold text-slate-700 text-sm">API Access</th>
                <th className="text-left p-4 font-semibold text-slate-700 text-sm">Assigned Strategies</th>
                <th className="text-left p-4 font-semibold text-slate-700 text-sm">Created</th>
                <th className="text-right p-4 font-semibold text-slate-700 text-sm">Actions</th>
              </tr>
            </thead>
            <tbody>
              {users.map((user, index) => (
                <tr
                  key={user.email}
                  className={`border-b border-teal-50/50 hover:bg-gradient-to-r hover:from-teal-25/50 hover:to-cyan-25/50 transition-all duration-300 ${
                    index % 2 === 0 ? "bg-white/50" : "bg-teal-25/20"
                  }`}
                >
                  <td className="p-4">
                    <div>
                      <div className="font-semibold text-slate-800">{user.name}</div>
                      <div className="text-sm text-slate-600">{user.email}</div>
                    </div>
                  </td>
                  <td className="p-4">
                    <div className="flex items-center gap-2">
                      <Key className="h-4 w-4 text-slate-400" />
                      {user.api_key ? (
                        <Badge variant="outline" className="bg-green-50 text-green-700 border-green-200">
                          Configured
                        </Badge>
                      ) : (
                        <Badge variant="outline" className="bg-gray-50 text-gray-600 border-gray-200">
                          Not Set
                        </Badge>
                      )}
                    </div>
                  </td>
                  <td className="p-4">
                    <div className="flex flex-wrap gap-1">
                      {user.assigned_strategies && user.assigned_strategies.length > 0 ? (
                        user.assigned_strategies.map((strategy: any) => (
                          <Badge
                            key={strategy.name}
                            variant="outline"
                            className="bg-purple-50 text-purple-700 border-purple-200 text-xs"
                          >
                            {strategy.symbol?.toUpperCase()}
                          </Badge>
                        ))
                      ) : (
                        <Badge variant="outline" className="bg-gray-50 text-gray-600 border-gray-200 text-xs">
                          None
                        </Badge>
                      )}
                    </div>
                  </td>
                  <td className="p-4">
                    <div className="flex items-center gap-2 text-sm text-slate-600">
                      <Calendar className="h-4 w-4" />
                      {formatDate(user.created_at)}
                    </div>
                  </td>
                  <td className="p-4 text-right">
                    <AlertDialog>
                      <AlertDialogTrigger asChild>
                        <Button
                          variant="outline"
                          size="sm"
                          className="border-red-200 text-red-600 hover:bg-red-50"
                          disabled={deletingUser === user.email}
                        >
                          <Trash2 className="h-4 w-4" />
                        </Button>
                      </AlertDialogTrigger>
                      <AlertDialogContent>
                        <AlertDialogHeader>
                          <AlertDialogTitle>Delete User</AlertDialogTitle>
                          <AlertDialogDescription>
                            Are you sure you want to delete <strong>{user.name}</strong> ({user.email})?
                            This action cannot be undone and will remove all associated data.
                          </AlertDialogDescription>
                        </AlertDialogHeader>
                        <AlertDialogFooter>
                          <AlertDialogCancel>Cancel</AlertDialogCancel>
                          <AlertDialogAction
                            onClick={() => handleDeleteUser(user.email)}
                            className="bg-red-600 hover:bg-red-700"
                          >
                            {deletingUser === user.email ? "Deleting..." : "Delete User"}
                          </AlertDialogAction>
                        </AlertDialogFooter>
                      </AlertDialogContent>
                    </AlertDialog>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </CardContent>
    </Card>
  )
}
