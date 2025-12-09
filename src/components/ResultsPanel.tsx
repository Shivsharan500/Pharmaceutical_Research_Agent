import { Button } from '@/components/ui/button';
import { Download, FileText, CheckCircle2, RotateCcw } from 'lucide-react';

interface ResultsPanelProps {
  moleculeName: string;
  onDownload: () => void;
  onNewSearch: () => void;
}

export const ResultsPanel = ({ moleculeName, onDownload, onNewSearch }: ResultsPanelProps) => {
  return (
    <div className="w-full max-w-2xl mx-auto space-y-8 animate-fade-in">
      {/* Success indicator */}
      <div className="text-center space-y-4">
        <div className="relative inline-flex">
          <CheckCircle2 className="w-20 h-20 text-primary" />
          <div className="absolute inset-0 w-20 h-20 bg-primary/30 blur-2xl rounded-full animate-pulse" />
        </div>
        <h2 className="font-display text-3xl md:text-4xl font-bold text-foreground">
          Analysis Complete
        </h2>
        <p className="text-muted-foreground text-lg">
          Comprehensive research report for <span className="text-primary font-semibold">{moleculeName}</span> is ready
        </p>
      </div>

      {/* Report preview card */}
      <div className="glass rounded-2xl p-6 gradient-border space-y-6">
        <div className="flex items-start gap-4">
          <div className="w-14 h-14 rounded-xl bg-primary/10 flex items-center justify-center flex-shrink-0">
            <FileText className="w-7 h-7 text-primary" />
          </div>
          <div className="flex-1 min-w-0">
            <h3 className="font-display text-xl font-semibold text-foreground mb-1">
              Research Report
            </h3>
            <p className="text-sm text-muted-foreground mb-3">
              Multi-agent pharmaceutical analysis document
            </p>
            <div className="flex flex-wrap gap-2">
              {['Market Analysis', 'Patent Landscape', 'Clinical Data', 'Regulatory Info'].map((tag) => (
                <span
                  key={tag}
                  className="px-2.5 py-1 text-xs rounded-full bg-secondary text-muted-foreground border border-border"
                >
                  {tag}
                </span>
              ))}
            </div>
          </div>
        </div>

        {/* Stats */}
        <div className="grid grid-cols-3 gap-4 py-4 border-t border-b border-border/50">
          {[
            { label: 'Agents Used', value: '6' },
            { label: 'Data Sources', value: '12+' },
            { label: 'Pages', value: '~25' },
          ].map((stat) => (
            <div key={stat.label} className="text-center">
              <div className="font-display text-2xl font-bold text-primary">{stat.value}</div>
              <div className="text-xs text-muted-foreground">{stat.label}</div>
            </div>
          ))}
        </div>

        {/* Download button */}
        <Button
          variant="hero"
          size="xl"
          className="w-full"
          onClick={onDownload}
        >
          <Download className="w-5 h-5" />
          Download PDF Report
        </Button>
      </div>

      {/* New search button */}
      <div className="text-center">
        <Button
          variant="ghost"
          size="lg"
          onClick={onNewSearch}
          className="text-muted-foreground hover:text-foreground"
        >
          <RotateCcw className="w-4 h-4" />
          Start New Research
        </Button>
      </div>
    </div>
  );
};
