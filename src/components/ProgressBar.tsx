import { useEffect, useState } from 'react';
import { cn } from '@/lib/utils';

interface ProgressBarProps {
  isActive: boolean;
  duration: number; // in milliseconds
  onComplete?: () => void;
}

const loadingMessages = [
  "Initializing multi-agent system...",
  "Deploying IQVIA Market Intelligence Analyst...",
  "Activating Export-Import Trade Analyst...",
  "Loading Patent Landscape Agent...",
  "Initiating Clinical Research Specialist...",
  "Connecting Regulatory Intelligence Expert...",
  "Syncing Competitive Intelligence Analyst...",
  "Processing molecular data structures...",
  "Analyzing market dynamics...",
  "Scanning patent databases...",
  "Evaluating clinical trial data...",
  "Compiling regulatory requirements...",
  "Generating comprehensive research report...",
  "Finalizing analysis results...",
];

export const ProgressBar = ({ isActive, duration, onComplete }: ProgressBarProps) => {
  const [progress, setProgress] = useState(0);
  const [messageIndex, setMessageIndex] = useState(0);

  useEffect(() => {
    if (!isActive) {
      setProgress(0);
      setMessageIndex(0);
      return;
    }

    const startTime = Date.now();
    const interval = setInterval(() => {
      const elapsed = Date.now() - startTime;
      const newProgress = Math.min((elapsed / duration) * 100, 100);
      setProgress(newProgress);

      // Update message based on progress
      const newMessageIndex = Math.floor((newProgress / 100) * (loadingMessages.length - 1));
      setMessageIndex(newMessageIndex);

      if (newProgress >= 100) {
        clearInterval(interval);
        onComplete?.();
      }
    }, 50);

    return () => clearInterval(interval);
  }, [isActive, duration, onComplete]);

  if (!isActive) return null;

  return (
    <div className="w-full max-w-2xl mx-auto space-y-6 animate-fade-in">
      {/* Progress container */}
      <div className="relative">
        {/* Background track */}
        <div className="h-4 rounded-full bg-secondary border border-border overflow-hidden">
          {/* Progress fill */}
          <div
            className="h-full rounded-full bg-gradient-to-r from-primary via-accent to-primary transition-all duration-100 relative"
            style={{ width: `${progress}%` }}
          >
            {/* Shine effect */}
            <div className="absolute inset-0 overflow-hidden rounded-full">
              <div className="absolute inset-0 bg-gradient-to-r from-transparent via-white/30 to-transparent animate-progress-shine" />
            </div>
          </div>
        </div>

        {/* Glow effect */}
        <div
          className="absolute top-0 h-4 rounded-full bg-primary/30 blur-md transition-all duration-100"
          style={{ width: `${progress}%` }}
        />
      </div>

      {/* Progress percentage */}
      <div className="flex justify-between items-center">
        <span className="font-display text-2xl text-glow text-primary">
          {progress.toFixed(1)}%
        </span>
        <span className="text-sm text-muted-foreground">
          {Math.ceil(((100 - progress) / 100) * (duration / 60000))} min remaining
        </span>
      </div>

      {/* Status message */}
      <div className="glass rounded-lg p-4 gradient-border">
        <div className="flex items-center gap-3">
          <div className="relative">
            <div className="w-3 h-3 rounded-full bg-primary animate-pulse" />
            <div className="absolute inset-0 w-3 h-3 rounded-full bg-primary animate-ping" />
          </div>
          <p className="text-sm text-foreground/80 font-medium">
            {loadingMessages[messageIndex]}
          </p>
        </div>
      </div>

      {/* Agent activity indicators */}
      <div className="grid grid-cols-3 gap-3">
        {['Market Analysis', 'Patent Research', 'Clinical Data'].map((agent, i) => (
          <div
            key={agent}
            className={cn(
              "glass rounded-lg p-3 text-center transition-all duration-500",
              progress > (i + 1) * 25 ? "border-primary/50" : "border-border/50"
            )}
          >
            <div
              className={cn(
                "w-2 h-2 rounded-full mx-auto mb-2 transition-all duration-500",
                progress > (i + 1) * 25 ? "bg-primary box-glow" : "bg-muted"
              )}
            />
            <span className="text-xs text-muted-foreground">{agent}</span>
          </div>
        ))}
      </div>
    </div>
  );
};
