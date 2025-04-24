import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { TracerForm } from "@/components/tracer-form"
import { VerifyData } from "@/components/verify-data"
import { TransactionHistory } from "@/components/transaction-history"
import { WalletConnect } from "@/components/wallet-connect"

export default function Home() {
  return (
    <main className="min-h-screen bg-gradient-to-b from-slate-50 to-slate-100 dark:from-slate-950 dark:to-slate-900">
      <div className="container mx-auto px-4 py-12">
        <div className="mb-8 text-center">
          <h1 className="text-4xl font-extrabold tracking-tight lg:text-5xl mb-3">Blockchain Tracer</h1>
          <p className="text-lg text-slate-600 dark:text-slate-400 max-w-2xl mx-auto">
            Record and verify sensitive information on EVM-compatible blockchains with ease
          </p>
        </div>

        <div className="mb-8">
          <WalletConnect />
        </div>

        <Tabs defaultValue="trace" className="max-w-4xl mx-auto">
          <TabsList className="grid w-full grid-cols-3">
            <TabsTrigger value="trace">Trace Data</TabsTrigger>
            <TabsTrigger value="verify">Verify Data</TabsTrigger>
            <TabsTrigger value="history">Transaction History</TabsTrigger>
          </TabsList>
          <TabsContent value="trace" className="p-6 bg-white dark:bg-slate-800 rounded-lg shadow-sm mt-2">
            <TracerForm />
          </TabsContent>
          <TabsContent value="verify" className="p-6 bg-white dark:bg-slate-800 rounded-lg shadow-sm mt-2">
            <VerifyData />
          </TabsContent>
          <TabsContent value="history" className="p-6 bg-white dark:bg-slate-800 rounded-lg shadow-sm mt-2">
            <TransactionHistory />
          </TabsContent>
        </Tabs>
      </div>
    </main>
  )
}
