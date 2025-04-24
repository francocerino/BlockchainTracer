"use client"

import type React from "react"

import { useState } from "react"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Textarea } from "@/components/ui/textarea"
import { Label } from "@/components/ui/label"
import { Card, CardContent } from "@/components/ui/card"
import { Loader2, CheckCircle2, XCircle, AlertCircle } from "lucide-react"
import { Alert, AlertDescription, AlertTitle } from "@/components/ui/alert"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"

export function VerifyData() {
  const [verifyMethod, setVerifyMethod] = useState<"hash" | "data">("hash")
  const [dataHash, setDataHash] = useState("")
  const [originalData, setOriginalData] = useState("")
  const [isVerifying, setIsVerifying] = useState(false)
  const [verificationResult, setVerificationResult] = useState<any>(null)
  const [error, setError] = useState<string | null>(null)

  const handleVerifyByHash = async (e: React.FormEvent) => {
    e.preventDefault()
    setIsVerifying(true)
    setError(null)
    setVerificationResult(null)

    try {
      if (!dataHash.trim()) {
        throw new Error("Please enter a data hash")
      }

      // In a real implementation, this would call your backend API
      // which would use the BlockchainTracer class to retrieve the record
      // For demo purposes, we'll simulate a response

      // Simulate API call delay
      await new Promise((resolve) => setTimeout(resolve, 1500))

      // Simulate blockchain record retrieval
      const mockRecord = {
        data_package: {
          hash: dataHash,
          type: "ml_model",
          timestamp: Math.floor(Date.now() / 1000) - 86400, // 1 day ago
          metadata: {
            author: "John Doe",
            version: "1.0.0",
          },
          recorder:
            "0x" +
            Array(40)
              .fill(0)
              .map(() => Math.floor(Math.random() * 16).toString(16))
              .join(""),
        },
        signature:
          "0x" +
          Array(130)
            .fill(0)
            .map(() => Math.floor(Math.random() * 16).toString(16))
            .join(""),
        tx_hash:
          "0x" +
          Array(64)
            .fill(0)
            .map(() => Math.floor(Math.random() * 16).toString(16))
            .join(""),
        block_number: Math.floor(Math.random() * 1000000),
        block_timestamp: Math.floor(Date.now() / 1000) - 86400,
        blockchain_verification: {
          verified: true,
          block_number: Math.floor(Math.random() * 1000000),
          timestamp: Math.floor(Date.now() / 1000) - 86400,
        },
      }

      setVerificationResult(mockRecord)
    } catch (err: any) {
      console.error("Error verifying data:", err)
      setError(err.message || "Failed to verify data")
    } finally {
      setIsVerifying(false)
    }
  }

  const handleVerifyData = async (e: React.FormEvent) => {
    e.preventDefault()
    setIsVerifying(true)
    setError(null)
    setVerificationResult(null)

    try {
      if (!originalData.trim()) {
        throw new Error("Please enter the original data")
      }

      // In a real implementation, this would call your backend API
      // which would use the BlockchainTracer class to verify the data
      // For demo purposes, we'll simulate a response

      // Simulate API call delay
      await new Promise((resolve) => setTimeout(resolve, 1500))

      // Randomly determine if verification is successful (for demo)
      const isVerified = Math.random() > 0.3

      if (isVerified) {
        setVerificationResult({
          verified: true,
          data_hash:
            "0x" +
            Array(64)
              .fill(0)
              .map(() => Math.floor(Math.random() * 16).toString(16))
              .join(""),
          blockchain_record: {
            data_package: {
              type: "ml_model",
              timestamp: Math.floor(Date.now() / 1000) - 86400,
              metadata: {
                author: "John Doe",
                version: "1.0.0",
              },
            },
            tx_hash:
              "0x" +
              Array(64)
                .fill(0)
                .map(() => Math.floor(Math.random() * 16).toString(16))
                .join(""),
            block_number: Math.floor(Math.random() * 1000000),
          },
        })
      } else {
        setVerificationResult({
          verified: false,
          message: "The provided data does not match any records on the blockchain.",
        })
      }
    } catch (err: any) {
      console.error("Error verifying data:", err)
      setError(err.message || "Failed to verify data")
    } finally {
      setIsVerifying(false)
    }
  }

  const formatTimestamp = (timestamp: number) => {
    return new Date(timestamp * 1000).toLocaleString()
  }

  return (
    <div>
      <h2 className="text-2xl font-bold mb-4">Verify Blockchain Data</h2>

      {error && (
        <Alert variant="destructive" className="mb-4">
          <AlertCircle className="h-4 w-4" />
          <AlertTitle>Error</AlertTitle>
          <AlertDescription>{error}</AlertDescription>
        </Alert>
      )}

      <Tabs value={verifyMethod} onValueChange={(v) => setVerifyMethod(v as "hash" | "data")}>
        <TabsList className="grid w-full grid-cols-2 mb-4">
          <TabsTrigger value="hash">Verify by Hash</TabsTrigger>
          <TabsTrigger value="data">Verify Data</TabsTrigger>
        </TabsList>

        <TabsContent value="hash">
          {verificationResult ? (
            <Card>
              <CardContent className="pt-6 space-y-4">
                <Alert>
                  <CheckCircle2 className="h-4 w-4" />
                  <AlertTitle>Record Found!</AlertTitle>
                  <AlertDescription>The record was found on the blockchain and verified.</AlertDescription>
                </Alert>

                <div className="space-y-4">
                  <div>
                    <Label className="text-sm text-slate-500">Data Type</Label>
                    <div className="font-medium">{verificationResult.data_package.type}</div>
                  </div>

                  <div>
                    <Label className="text-sm text-slate-500">Timestamp</Label>
                    <div className="font-medium">{formatTimestamp(verificationResult.data_package.timestamp)}</div>
                  </div>

                  <div>
                    <Label className="text-sm text-slate-500">Metadata</Label>
                    <div className="font-mono text-sm bg-slate-100 dark:bg-slate-800 p-2 rounded overflow-x-auto">
                      {JSON.stringify(verificationResult.data_package.metadata, null, 2)}
                    </div>
                  </div>

                  <div>
                    <Label className="text-sm text-slate-500">Transaction Hash</Label>
                    <div className="font-mono text-sm bg-slate-100 dark:bg-slate-800 p-2 rounded overflow-x-auto">
                      {verificationResult.tx_hash}
                    </div>
                  </div>

                  <div>
                    <Label className="text-sm text-slate-500">Block Number</Label>
                    <div className="font-medium">{verificationResult.block_number}</div>
                  </div>

                  <Button onClick={() => setVerificationResult(null)} variant="outline">
                    Verify Another Record
                  </Button>
                </div>
              </CardContent>
            </Card>
          ) : (
            <form onSubmit={handleVerifyByHash} className="space-y-4">
              <div className="space-y-2">
                <Label htmlFor="dataHash">Data Hash</Label>
                <Input
                  id="dataHash"
                  placeholder="Enter the data hash to verify"
                  value={dataHash}
                  onChange={(e) => setDataHash(e.target.value)}
                  required
                />
                <p className="text-xs text-slate-500">
                  Enter the hash of the data you want to verify on the blockchain.
                </p>
              </div>

              <Button type="submit" disabled={isVerifying} className="w-full">
                {isVerifying ? (
                  <>
                    <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                    Verifying...
                  </>
                ) : (
                  "Verify Record"
                )}
              </Button>
            </form>
          )}
        </TabsContent>

        <TabsContent value="data">
          {verificationResult ? (
            <Card>
              <CardContent className="pt-6 space-y-4">
                {verificationResult.verified ? (
                  <>
                    <Alert>
                      <CheckCircle2 className="h-4 w-4" />
                      <AlertTitle>Verification Successful!</AlertTitle>
                      <AlertDescription>The data matches a record on the blockchain.</AlertDescription>
                    </Alert>

                    <div className="space-y-4">
                      <div>
                        <Label className="text-sm text-slate-500">Data Hash</Label>
                        <div className="font-mono text-sm bg-slate-100 dark:bg-slate-800 p-2 rounded overflow-x-auto">
                          {verificationResult.data_hash}
                        </div>
                      </div>

                      <div>
                        <Label className="text-sm text-slate-500">Data Type</Label>
                        <div className="font-medium">{verificationResult.blockchain_record.data_package.type}</div>
                      </div>

                      <div>
                        <Label className="text-sm text-slate-500">Timestamp</Label>
                        <div className="font-medium">
                          {formatTimestamp(verificationResult.blockchain_record.data_package.timestamp)}
                        </div>
                      </div>

                      <div>
                        <Label className="text-sm text-slate-500">Transaction Hash</Label>
                        <div className="font-mono text-sm bg-slate-100 dark:bg-slate-800 p-2 rounded overflow-x-auto">
                          {verificationResult.blockchain_record.tx_hash}
                        </div>
                      </div>
                    </div>
                  </>
                ) : (
                  <Alert variant="destructive">
                    <XCircle className="h-4 w-4" />
                    <AlertTitle>Verification Failed</AlertTitle>
                    <AlertDescription>{verificationResult.message}</AlertDescription>
                  </Alert>
                )}

                <Button onClick={() => setVerificationResult(null)} variant="outline">
                  Verify Another Data
                </Button>
              </CardContent>
            </Card>
          ) : (
            <form onSubmit={handleVerifyData} className="space-y-4">
              <div className="space-y-2">
                <Label htmlFor="originalData">Original Data</Label>
                <Textarea
                  id="originalData"
                  placeholder="Enter the original data to verify"
                  value={originalData}
                  onChange={(e) => setOriginalData(e.target.value)}
                  className="min-h-[150px]"
                  required
                />
                <p className="text-xs text-slate-500">
                  Enter the original data to verify if it matches a record on the blockchain.
                </p>
              </div>

              <Button type="submit" disabled={isVerifying} className="w-full">
                {isVerifying ? (
                  <>
                    <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                    Verifying...
                  </>
                ) : (
                  "Verify Data"
                )}
              </Button>
            </form>
          )}
        </TabsContent>
      </Tabs>
    </div>
  )
}
