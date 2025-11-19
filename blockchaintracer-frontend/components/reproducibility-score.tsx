'use client'

interface ReproducibilityScoreProps {
  score: number
}

export function ReproducibilityScore({ score }: ReproducibilityScoreProps) {
  const getColor = (score: number) => {
    if (score >= 85) return 'text-emerald-600 dark:text-emerald-400'
    if (score >= 70) return 'text-amber-600 dark:text-amber-400'
    if (score >= 50) return 'text-orange-600 dark:text-orange-400'
    return 'text-rose-600 dark:text-rose-400'
  }

  const getBackgroundColor = (score: number) => {
    if (score >= 85) return 'bg-emerald-100 dark:bg-emerald-900/30 border border-emerald-300 dark:border-emerald-700'
    if (score >= 70) return 'bg-amber-100 dark:bg-amber-900/30 border border-amber-300 dark:border-amber-700'
    if (score >= 50) return 'bg-orange-100 dark:bg-orange-900/30 border border-orange-300 dark:border-orange-700'
    return 'bg-rose-100 dark:bg-rose-900/30 border border-rose-300 dark:border-rose-700'
  }

  const getLabel = (score: number) => {
    if (score >= 85) return 'Excellent'
    if (score >= 70) return 'Good'
    if (score >= 50) return 'Fair'
    return 'Poor'
  }

  const circumference = 2 * Math.PI * 45
  const strokeDashoffset = circumference - (score / 100) * circumference

  return (
    <div className="flex flex-col items-center gap-2">
      <div className="relative w-28 h-28">
        <svg className="transform -rotate-90 w-28 h-28">
          <circle
            cx="56"
            cy="56"
            r="45"
            stroke="currentColor"
            strokeWidth="8"
            fill="none"
            className="text-slate-200 dark:text-slate-700"
          />
          {/* Progress circle */}
          <circle
            cx="56"
            cy="56"
            r="45"
            stroke="currentColor"
            strokeWidth="8"
            fill="none"
            strokeDasharray={circumference}
            strokeDashoffset={strokeDashoffset}
            strokeLinecap="round"
            className={getColor(score)}
            style={{ transition: 'stroke-dashoffset 0.5s ease' }}
          />
        </svg>
        <div className="absolute inset-0 flex flex-col items-center justify-center">
          <span className={`text-2xl font-bold ${getColor(score)}`}>{score}</span>
          <span className="text-xs text-slate-600 dark:text-slate-400">/ 100</span>
        </div>
      </div>
      <div className={`px-3 py-1 rounded-full text-xs font-medium ${getBackgroundColor(score)} ${getColor(score)}`}>
        {getLabel(score)}
      </div>
      <span className="text-xs text-slate-600 dark:text-slate-400 text-center">Reproducibility</span>
    </div>
  )
}
