'use client'

import { useState } from 'react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { ExternalLink, Search, Shield, CheckCircle2, Copy, FileText, Database } from 'lucide-react'
import { ReproducibilityScore } from '@/components/reproducibility-score'
import { ExperimentCard } from '@/components/experiment-card'

// Mock data for experiments
const experiments = [
  {
    id: '1',
    name: 'ResNet-50 Image Classification',
    description: 'Training ResNet-50 on ImageNet with augmentation pipeline',
    reproducibilityScore: 92,
    blockchainHash: '0x7f9fade1c0d57a7af66ab4ead7c2eb2b9a0a1d2c3e4f5a6b7c8d9e0f1a2b3c4d',
    ipfsHash: 'QmT5NvUtoM5nWFfrQdVrFtvGfKFmG7AHE8P34isapyhCxX',
    timestamp: '2025-01-15T10:30:00Z',
    framework: 'PyTorch',
    dataset: 'ImageNet',
    verified: true,
    metrics: {
      accuracy: 0.923,
      loss: 0.245,
      epochs: 100
    }
  },
  {
    id: '2',
    name: 'BERT Fine-tuning for NLP',
    description: 'Fine-tuning BERT-base for sentiment analysis on IMDB dataset',
    reproducibilityScore: 87,
    blockchainHash: '0x8a1bcde2f3d68b9c0a1f2e3d4c5b6a7d8e9f0a1b2c3d4e5f6a7b8c9d0e1f2a3b',
    ipfsHash: 'QmY8KvBnrFtvGfKFmG7AHE8P34isapyhCxXNvUtoM5nWF',
    timestamp: '2025-01-14T14:20:00Z',
    framework: 'TensorFlow',
    dataset: 'IMDB',
    verified: true,
    metrics: {
      accuracy: 0.891,
      f1Score: 0.887,
      epochs: 5
    }
  },
  {
    id: '3',
    name: 'GAN for Image Synthesis',
    description: 'StyleGAN2 training on CelebA-HQ for high-res face generation',
    reproducibilityScore: 78,
    blockchainHash: '0x9b2cdef3a4e79c0d1b2f3e4d5c6b7a8d9e0f1a2b3c4d5e6f7a8b9c0d1e2f3a4b',
    ipfsHash: 'QmZ9LwCosGuhG8HJF9Q45jtbqziDyYQmY8KvBnrFtvGfK',
    timestamp: '2025-01-13T09:15:00Z',
    framework: 'PyTorch',
    dataset: 'CelebA-HQ',
    verified: true,
    metrics: {
      fid: 12.3,
      inception: 8.95,
      epochs: 250
    }
  },
  {
    id: '4',
    name: 'Time Series Forecasting',
    description: 'LSTM model for stock price prediction using historical data',
    reproducibilityScore: 65,
    blockchainHash: '0xa3deff4b5f80d1e2c3f4e5d6c7b8a9d0e1f2a3b4c5d6e7f8a9b0c1d2e3f4a5b',
    ipfsHash: 'QmA1MxDptGviH9KGN0R56kubrzEyZqnY9LwCosGuhG8HJ',
    timestamp: '2025-01-12T16:45:00Z',
    framework: 'Keras',
    dataset: 'S&P 500',
    verified: false,
    metrics: {
      mse: 0.0234,
      mae: 0.112,
      epochs: 150
    }
  }
]

export default function Home() {
  const [searchQuery, setSearchQuery] = useState('')

  const filteredExperiments = experiments.filter(exp =>
    exp.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
    exp.description.toLowerCase().includes(searchQuery.toLowerCase())
  )

  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-50 via-blue-50 to-cyan-50 dark:from-slate-950 dark:via-purple-950 dark:to-blue-950">
      {/* Header */}
      <header className="border-b border-border/50 bg-white/80 dark:bg-slate-900/80 backdrop-blur-lg">
        <div className="container mx-auto px-4 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <div className="flex items-center justify-center w-10 h-10 rounded-lg bg-gradient-to-br from-purple-500 to-blue-500">
                <Shield className="w-6 h-6 text-white" />
              </div>
              <div>
                <h1 className="text-2xl font-bold bg-gradient-to-r from-purple-600 to-blue-600 dark:from-purple-400 dark:to-blue-400 bg-clip-text text-transparent">MLTracer</h1>
                <p className="text-sm text-slate-600 dark:text-slate-400">Immutable ML Experiment Registry</p>
              </div>
            </div>
            <div className="flex items-center gap-4">
              <Button variant="outline" size="sm">
                <FileText className="w-4 h-4 mr-2" />
                Documentation
              </Button>
              <Button size="sm" className="bg-gradient-to-r from-purple-500 to-blue-500 hover:from-purple-600 hover:to-blue-600 text-white">
                <Database className="w-4 h-4 mr-2" />
                New Experiment
              </Button>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="container mx-auto px-4 py-8">
        {/* Stats Overview */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-8">
          <Card className="border-purple-200 dark:border-purple-800 bg-gradient-to-br from-purple-50 to-purple-100 dark:from-purple-950 dark:to-purple-900">
            <CardHeader className="pb-3">
              <CardDescription className="text-purple-600 dark:text-purple-400">Total Experiments</CardDescription>
              <CardTitle className="text-3xl text-purple-700 dark:text-purple-300">1,247</CardTitle>
            </CardHeader>
          </Card>
          <Card className="border-blue-200 dark:border-blue-800 bg-gradient-to-br from-blue-50 to-blue-100 dark:from-blue-950 dark:to-blue-900">
            <CardHeader className="pb-3">
              <CardDescription className="text-blue-600 dark:text-blue-400">Verified On-chain</CardDescription>
              <CardTitle className="text-3xl text-blue-700 dark:text-blue-300">1,189</CardTitle>
            </CardHeader>
          </Card>
          <Card className="border-cyan-200 dark:border-cyan-800 bg-gradient-to-br from-cyan-50 to-cyan-100 dark:from-cyan-950 dark:to-cyan-900">
            <CardHeader className="pb-3">
              <CardDescription className="text-cyan-600 dark:text-cyan-400">Avg. Reproducibility</CardDescription>
              <CardTitle className="text-3xl text-cyan-700 dark:text-cyan-300">84.2</CardTitle>
            </CardHeader>
          </Card>
          <Card className="border-pink-200 dark:border-pink-800 bg-gradient-to-br from-pink-50 to-pink-100 dark:from-pink-950 dark:to-pink-900">
            <CardHeader className="pb-3">
              <CardDescription className="text-pink-600 dark:text-pink-400">Active Researchers</CardDescription>
              <CardTitle className="text-3xl text-pink-700 dark:text-pink-300">342</CardTitle>
            </CardHeader>
          </Card>
        </div>

        {/* Search Bar */}
        <div className="mb-6">
          <div className="relative">
            <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-muted-foreground" />
            <Input
              type="text"
              placeholder="Search experiments by name, framework, or dataset..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="pl-10 h-12 bg-white/80 dark:bg-slate-900/80 backdrop-blur-sm"
            />
          </div>
        </div>

        {/* Experiments List */}
        <div className="space-y-4">
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-xl font-semibold text-slate-800 dark:text-slate-200">Recent Experiments</h2>
            <div className="flex items-center gap-2 text-sm text-slate-600 dark:text-slate-400">
              <CheckCircle2 className="w-4 h-4 text-emerald-500" />
              <span>Blockchain verified</span>
            </div>
          </div>
          
          {filteredExperiments.map((experiment) => (
            <ExperimentCard key={experiment.id} experiment={experiment} />
          ))}
        </div>
      </main>
    </div>
  )
}
