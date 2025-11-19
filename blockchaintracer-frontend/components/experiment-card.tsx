'use client'

import { useState } from 'react'
import { Card, CardContent } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Button } from '@/components/ui/button'
import { ExternalLink, Copy, CheckCircle2, AlertCircle, ChevronDown, ChevronUp } from 'lucide-react'
import { ReproducibilityScore } from '@/components/reproducibility-score'

interface Experiment {
  id: string
  name: string
  description: string
  reproducibilityScore: number
  blockchainHash: string
  ipfsHash: string
  timestamp: string
  framework: string
  dataset: string
  verified: boolean
  metrics: Record<string, number>
}

interface ExperimentCardProps {
  experiment: Experiment
}

export function ExperimentCard({ experiment }: ExperimentCardProps) {
  const [expanded, setExpanded] = useState(false)
  const [copied, setCopied] = useState<string | null>(null)

  const copyToClipboard = (text: string, type: string) => {
    navigator.clipboard.writeText(text)
    setCopied(type)
    setTimeout(() => setCopied(null), 2000)
  }

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleString('en-US', {
      month: 'short',
      day: 'numeric',
      year: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    })
  }

  const getCardGradient = (score: number) => {
    if (score >= 85) return 'bg-gradient-to-br from-emerald-50 via-teal-50 to-cyan-50 dark:from-emerald-900/20 dark:via-teal-900/20 dark:to-cyan-900/20 border-emerald-200 dark:border-emerald-800/50'
    if (score >= 70) return 'bg-gradient-to-br from-amber-50 via-yellow-50 to-orange-50 dark:from-amber-900/20 dark:via-yellow-900/20 dark:to-orange-900/20 border-amber-200 dark:border-amber-800/50'
    if (score >= 50) return 'bg-gradient-to-br from-orange-50 via-rose-50 to-pink-50 dark:from-orange-900/20 dark:via-rose-900/20 dark:to-pink-900/20 border-orange-200 dark:border-orange-800/50'
    return 'bg-gradient-to-br from-rose-50 via-red-50 to-pink-50 dark:from-rose-900/20 dark:via-red-900/20 dark:to-pink-900/20 border-rose-200 dark:border-rose-800/50'
  }

  return (
    <Card className={`hover:shadow-lg transition-all duration-300 ${getCardGradient(experiment.reproducibilityScore)}`}>
      <CardContent className="p-6">
        <div className="flex items-start justify-between gap-4">
          <div className="flex-1 min-w-0">
            <div className="flex items-start gap-3 mb-2">
              <div className="flex-1">
                <div className="flex items-center gap-2 mb-1">
                  <h3 className="text-lg font-semibold text-slate-900 dark:text-slate-100">{experiment.name}</h3>
                  {experiment.verified && (
                    <CheckCircle2 className="w-5 h-5 text-emerald-600 dark:text-emerald-400 flex-shrink-0" />
                  )}
                </div>
                <p className="text-sm text-slate-700 dark:text-slate-300 mb-3">{experiment.description}</p>
                
                <div className="flex flex-wrap items-center gap-2 mb-3">
                  <Badge variant="secondary" className="bg-purple-100 text-purple-700 dark:bg-purple-900/50 dark:text-purple-300">{experiment.framework}</Badge>
                  <Badge variant="outline" className="border-blue-300 text-blue-700 dark:border-blue-700 dark:text-blue-300">{experiment.dataset}</Badge>
                  <span className="text-xs text-slate-600 dark:text-slate-400">{formatDate(experiment.timestamp)}</span>
                </div>
              </div>
            </div>

            {/* Blockchain & IPFS Info */}
            <div className="space-y-2 mb-3">
              <div className="flex items-center gap-2 text-xs flex-wrap">
                <span className="text-slate-700 dark:text-slate-300 font-medium">Blockchain:</span>
                <code className="bg-white/90 dark:bg-slate-800/80 px-2 py-1 rounded text-xs font-mono text-slate-800 dark:text-slate-200 border border-slate-200 dark:border-slate-700">
                  {experiment.blockchainHash.slice(0, 20)}...{experiment.blockchainHash.slice(-8)}
                </code>
                <Button
                  variant="ghost"
                  size="sm"
                  className="h-6 w-6 p-0 hover:bg-white/80 dark:hover:bg-slate-800/80"
                  onClick={() => copyToClipboard(experiment.blockchainHash, 'blockchain')}
                >
                  {copied === 'blockchain' ? (
                    <CheckCircle2 className="w-3 h-3 text-emerald-600" />
                  ) : (
                    <Copy className="w-3 h-3 text-slate-600 dark:text-slate-400" />
                  )}
                </Button>
                <Button variant="ghost" size="sm" className="h-6 px-2 hover:bg-white/80 dark:hover:bg-slate-800/80">
                  <ExternalLink className="w-3 h-3 text-slate-600 dark:text-slate-400" />
                </Button>
              </div>
              
              <div className="flex items-center gap-2 text-xs flex-wrap">
                <span className="text-slate-700 dark:text-slate-300 font-medium">IPFS:</span>
                <code className="bg-white/90 dark:bg-slate-800/80 px-2 py-1 rounded text-xs font-mono text-slate-800 dark:text-slate-200 border border-slate-200 dark:border-slate-700">
                  {experiment.ipfsHash}
                </code>
                <Button
                  variant="ghost"
                  size="sm"
                  className="h-6 w-6 p-0 hover:bg-white/80 dark:hover:bg-slate-800/80"
                  onClick={() => copyToClipboard(experiment.ipfsHash, 'ipfs')}
                >
                  {copied === 'ipfs' ? (
                    <CheckCircle2 className="w-3 h-3 text-emerald-600" />
                  ) : (
                    <Copy className="w-3 h-3 text-slate-600 dark:text-slate-400" />
                  )}
                </Button>
                <Button variant="ghost" size="sm" className="h-6 px-2 hover:bg-white/80 dark:hover:bg-slate-800/80">
                  <ExternalLink className="w-3 h-3 text-slate-600 dark:text-slate-400" />
                </Button>
              </div>
            </div>

            {/* Metrics (Expandable) */}
            {expanded && (
              <div className="mt-4 pt-4 border-t border-slate-300 dark:border-slate-700">
                <h4 className="text-sm font-medium mb-2 text-slate-900 dark:text-slate-100">Experiment Metrics</h4>
                <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
                  {Object.entries(experiment.metrics).map(([key, value]) => (
                    <div key={key} className="bg-white/90 dark:bg-slate-800/80 rounded-lg p-3 border border-slate-200 dark:border-slate-700">
                      <p className="text-xs text-slate-600 dark:text-slate-400 capitalize mb-1">
                        {key.replace(/([A-Z])/g, ' $1').trim()}
                      </p>
                      <p className="text-lg font-semibold text-slate-900 dark:text-slate-100">
                        {typeof value === 'number' && value < 1 ? value.toFixed(3) : value}
                      </p>
                    </div>
                  ))}
                </div>
              </div>
            )}

            <Button
              variant="ghost"
              size="sm"
              onClick={() => setExpanded(!expanded)}
              className="mt-2 text-slate-700 dark:text-slate-300 hover:bg-white/80 dark:hover:bg-slate-800/80"
            >
              {expanded ? (
                <>
                  <ChevronUp className="w-4 h-4 mr-1" />
                  Show less
                </>
              ) : (
                <>
                  <ChevronDown className="w-4 h-4 mr-1" />
                  Show metrics
                </>
              )}
            </Button>
          </div>

          {/* Reproducibility Score */}
          <div className="flex-shrink-0">
            <ReproducibilityScore score={experiment.reproducibilityScore} />
          </div>
        </div>
      </CardContent>
    </Card>
  )
}
