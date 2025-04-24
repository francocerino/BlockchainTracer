// Ethereum window type
declare global {
  interface Window {
    ethereum?: {
      isMetaMask?: boolean
      request: (request: { method: string; params?: any[] }) => Promise<any>
      on: (eventName: string, callback: (...args: any[]) => void) => void
      removeListener: (eventName: string, callback: (...args: any[]) => void) => void
      removeAllListeners: (eventName: string) => void
    }
  }
}

// BlockchainTracer types
export interface DataPackage {
  hash: string
  type: string
  timestamp: number
  metadata: Record<string, any>
  recorder: string
}

export interface BlockchainRecord {
  success: boolean
  data_hash: string
  data_package: DataPackage
  signature: string
  signed_by: string
  transaction_hash: string
  block_number: number
}

export interface VerificationResult {
  verified: boolean
  data_hash?: string
  blockchain_record?: Partial<BlockchainRecord>
  message?: string
}

export interface TransactionDetails {
  transaction: {
    hash: string
    block_number: number
    from: string
    to: string
    value: string
    gas: number
    gas_price: string
    data: any
  }
  receipt: {
    status: number
    gas_used: number
    logs: any[]
  }
}
