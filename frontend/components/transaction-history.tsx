"use client"

import { useState, useEffect } from "react"
import { Button } from "@/components/ui/button"
import { Card, CardContent } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Loader2, AlertCircle, ExternalLink } from "lucide-react"
import { Alert, AlertDescription, AlertTitle } from "@/components/ui/alert"
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table"

type Transaction = {
  id: string
  hash: string
  type: string
  timestamp: number
  blockNumber: number
}

export function TransactionHistory() {
  const [transactions, setTransactions] = useState<Transaction[]>([])
  const [isLoading, setIsLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    fetchTransactions()
  }, [])

  const fetchTransactions = async () => {
    setIsLoading(true)
    setError(null)

    try {
      // In a real implementation, this would call your backend API
      // which would use the BlockchainTracer class to get transaction history
      // For demo purposes, we'll simulate a response

      // Simulate API call delay
      await new Promise((resolve) => setTimeout(resolve, 1500))

      // Generate mock transactions
      const mockTransactions: Transaction[] = Array(5)
        .fill(0)
        .map((_, index) => ({
          id: `tx-${index}`,
          hash:
            "0x" +
            Array(64)
              .fill(0)
              .map(() => Math.floor(Math.random() * 16).toString(16))
              .join(""),
          type: ["ml_model", "scientific_study", "donation", "green_h2"][Math.floor(Math.random() * 4)],
          timestamp: Math.floor(Date.now() / 1000) - index * 86400,
          blockNumber: 1000000 - index * 100,
        }))

      setTransactions(mockTransactions)
    } catch (err: any) {
      console.error("Error fetching transactions:", err)
      setError(err.message || "Failed to fetch transaction history")
    } finally {
      setIsLoading(false)
    }
  }

  const formatTimestamp = (timestamp: number) => {
    return new Date(timestamp * 1000).toLocaleString()
  }

  const formatHash = (hash: string) => {
    return `${hash.substring(0, 10)}...${hash.substring(hash.length - 8)}`
  }

  const getTypeColor = (type: string) => {
    const colors: Record<string, string> = {
      ml_model: "bg-emerald-100 text-emerald-800",
      scientific_study: "bg-blue-100 text-blue-800",
      donation: "bg-purple-100 text-purple-800",
      green_h2: "bg-green-100 text-green-800",
    }

    return colors[type] || "bg-slate-100 text-slate-800"
  }

  return (
    <div>
      <h2 className="text-2xl font-bold mb-4">Transaction History</h2>

      {error && (
        <Alert variant="destructive" className="mb-4">
          <AlertCircle className="h-4 w-4" />
          <AlertTitle>Error</AlertTitle>
          <AlertDescription>{error}</AlertDescription>
        </Alert>
      )}

      {isLoading ? (
        <div className="flex justify-center items-center py-12">
          <Loader2 className="h-8 w-8 animate-spin text-slate-400" />
        </div>
      ) : transactions.length > 0 ? (
        <Card>
          <CardContent className="p-0">
            <Table>
              <TableHeader>
                <TableRow>
                  <TableHead>Transaction Hash</TableHead>
                  <TableHead>Type</TableHead>
                  <TableHead>Timestamp</TableHead>
                  <TableHead>Block</TableHead>
                  <TableHead className="text-right">Actions</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {transactions.map((tx) => (
                  <TableRow key={tx.id}>
                    <TableCell className="font-mono">{formatHash(tx.hash)}</TableCell>
                    <TableCell>
                      <Badge className={getTypeColor(tx.type)}>{tx.type.replace("_", " ")}</Badge>
                    </TableCell>
                    <TableCell>{formatTimestamp(tx.timestamp)}</TableCell>
                    <TableCell>{tx.blockNumber.toLocaleString()}</TableCell>
                    <TableCell className="text-right">
                      <Button variant="ghost" size="sm" className="h-8 w-8 p-0">
                        <ExternalLink className="h-4 w-4" />
                        <span className="sr-only">View details</span>
                      </Button>
                    </TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </CardContent>
        </Card>
      ) : (
        <div className="text-center py-8">
          <p className="text-slate-500">No transactions found.</p>
          <Button onClick={fetchTransactions} variant="outline" className="mt-4">
            Refresh
          </Button>
        </div>
      )}
    </div>
  )
}
