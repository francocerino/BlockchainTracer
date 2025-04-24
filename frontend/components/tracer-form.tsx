"use client"

import type React from "react"

import { useState } from "react"
import { Button } from "@/components/ui/button"
import { Textarea } from "@/components/ui/textarea"
import { Label } from "@/components/ui/label"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { Card, CardContent } from "@/components/ui/card"
import { Loader2, CheckCircle2, AlertCircle } from "lucide-react"
import { Alert, AlertDescription, AlertTitle } from "@/components/ui/alert"

type DataType = "ml_model" | "scientific_study" | "donation" | "green_h2" | "other"

export function TracerForm() {
  const [dataType, setDataType] = useState<DataType>("ml_model")
  const [data, setData] = useState("")
  const [metadata, setMetadata] = useState("")
  const [isSubmitting, setIsSubmitting] = useState(false)
  const [result, setResult] = useState<any>(null)
  const [error, setError] = useState<string | null>(null)

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setIsSubmitting(true)
    setError(null)
    setResult(null)

    try {
      if (typeof window === "undefined" || !window.ethereum) {
        throw new Error("Please connect your wallet first")
      }

      const accounts = await window.ethereum.request({ method: "eth_accounts" })
      if (!accounts || accounts.length === 0) {
        throw new Error("Please connect your wallet first")
      }

      // In a real implementation, this would call your backend API
      // which would use the BlockchainTracer class to trace the data
      // For demo purposes, we'll simulate a successful response

      // Simulate API call delay
      await new Promise((resolve) => setTimeout(resolve, 2000))

      // Parse metadata JSON if provided
      let metadataObj = {}
      if (metadata.trim()) {
        try {
          metadataObj = JSON.parse(metadata)
        } catch (err) {
          throw new Error("Invalid metadata JSON format")
        }
      }

      // Simulate successful blockchain transaction
      const mockResult = {
        success: true,
        data_hash:
          "0x" +
          Array(64)
            .fill(0)
            .map(() => Math.floor(Math.random() * 16).toString(16))
            .join(""),
        transaction_hash:
          "0x" +
          Array(64)
            .fill(0)
            .map(() => Math.floor(Math.random() * 16).toString(16))
            .join(""),
        block_number: Math.floor(Math.random() * 1000000),
        data_package: {
          type: dataType,
          timestamp: Math.floor(Date.now() / 1000),
          metadata: metadataObj,
          recorder: accounts[0],
        },
      }

      setResult(mockResult)
    } catch (err: any) {
      console.error("Error submitting data:", err)
      setError(err.message || "Failed to submit data to blockchain")
    } finally {
      setIsSubmitting(false)
    }
  }

  return (
    <div>
      <h2 className="text-2xl font-bold mb-4">Trace Data on Blockchain</h2>

      {error && (
        <Alert variant="destructive" className="mb-4">
          <AlertCircle className="h-4 w-4" />
          <AlertTitle>Error</AlertTitle>
          <AlertDescription>{error}</AlertDescription>
        </Alert>
      )}

      {result ? (
        <div className="space-y-4">
          <Alert className="mb-4">
            <CheckCircle2 className="h-4 w-4" />
            <AlertTitle>Success!</AlertTitle>
            <AlertDescription>Your data has been successfully recorded on the blockchain.</AlertDescription>
          </Alert>

          <Card>
            <CardContent className="pt-6 space-y-4">
              <div>
                <Label className="text-sm text-slate-500">Data Hash</Label>
                <div className="font-mono text-sm bg-slate-100 dark:bg-slate-800 p-2 rounded overflow-x-auto">
                  {result.data_hash}
                </div>
              </div>

              <div>
                <Label className="text-sm text-slate-500">Transaction Hash</Label>
                <div className="font-mono text-sm bg-slate-100 dark:bg-slate-800 p-2 rounded overflow-x-auto">
                  {result.transaction_hash}
                </div>
              </div>

              <div>
                <Label className="text-sm text-slate-500">Block Number</Label>
                <div className="font-mono text-sm">{result.block_number}</div>
              </div>

              <Button onClick={() => setResult(null)} variant="outline">
                Trace New Data
              </Button>
            </CardContent>
          </Card>
        </div>
      ) : (
        <form onSubmit={handleSubmit} className="space-y-4">
          <div className="space-y-2">
            <Label htmlFor="dataType">Data Type</Label>
            <Select value={dataType} onValueChange={(value) => setDataType(value as DataType)}>
              <SelectTrigger>
                <SelectValue placeholder="Select data type" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="ml_model">ML Model</SelectItem>
                <SelectItem value="scientific_study">Scientific Study</SelectItem>
                <SelectItem value="donation">NGO Donation</SelectItem>
                <SelectItem value="green_h2">Green Hydrogen</SelectItem>
                <SelectItem value="other">Other</SelectItem>
              </SelectContent>
            </Select>
          </div>

          <div className="space-y-2">
            <Label htmlFor="data">Data (JSON or Text)</Label>
            <Textarea
              id="data"
              placeholder="Enter your data here"
              value={data}
              onChange={(e) => setData(e.target.value)}
              className="min-h-[150px]"
              required
            />
            <p className="text-xs text-slate-500">This data will be hashed before being stored on the blockchain.</p>
          </div>

          <div className="space-y-2">
            <Label htmlFor="metadata">Metadata (Optional JSON)</Label>
            <Textarea
              id="metadata"
              placeholder='{"key": "value", "author": "name"}'
              value={metadata}
              onChange={(e) => setMetadata(e.target.value)}
              className="min-h-[100px]"
            />
            <p className="text-xs text-slate-500">Additional information about your data in JSON format.</p>
          </div>

          <Button type="submit" disabled={isSubmitting} className="w-full">
            {isSubmitting ? (
              <>
                <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                Recording on Blockchain...
              </>
            ) : (
              "Record on Blockchain"
            )}
          </Button>
        </form>
      )}
    </div>
  )
}
