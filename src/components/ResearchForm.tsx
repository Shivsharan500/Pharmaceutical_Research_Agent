import { useState } from 'react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Search, Atom, Sparkles } from 'lucide-react';

interface ResearchFormProps {
  onSubmit: (moleculeName: string) => void;
  isLoading: boolean;
}

export const ResearchForm = ({ onSubmit, isLoading }: ResearchFormProps) => {
  const [moleculeName, setMoleculeName] = useState('');

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (moleculeName.trim() && !isLoading) {
      onSubmit(moleculeName.trim());
    }
  };

  const exampleMolecules = ['Ibuprofen', 'Metformin', 'Omeprazole', 'Atorvastatin'];

  return (
    <div className="w-full max-w-2xl mx-auto space-y-8 animate-fade-in">
      {/* Hero section */}
      <div className="text-center space-y-4">
        <div className="flex items-center justify-center gap-3 mb-6">
          <div className="relative">
            <Atom className="w-12 h-12 text-primary animate-pulse-glow" />
            <div className="absolute inset-0 w-12 h-12 bg-primary/20 blur-xl rounded-full" />
          </div>
        </div>
        <h1 className="font-display text-4xl md:text-5xl lg:text-6xl font-bold text-glow tracking-tight">
          <span className="text-foreground">Pharma</span>
          <span className="text-primary">Research</span>
        </h1>
        <p className="text-muted-foreground text-lg max-w-lg mx-auto">
          AI-powered multi-agent system for comprehensive pharmaceutical molecule analysis
        </p>
      </div>

      {/* Form */}
      <form onSubmit={handleSubmit} className="space-y-6">
        <div className="relative group">
          <div className="absolute inset-0 bg-gradient-to-r from-primary/20 via-accent/20 to-primary/20 rounded-xl blur-xl opacity-0 group-hover:opacity-100 transition-opacity duration-500" />
          <div className="relative glass rounded-xl p-2 gradient-border">
            <div className="flex gap-2">
              <div className="relative flex-1">
                <Search className="absolute left-4 top-1/2 -translate-y-1/2 w-5 h-5 text-muted-foreground" />
                <Input
                  type="text"
                  placeholder="Enter molecule name (e.g., Aspirin, Paracetamol)"
                  value={moleculeName}
                  onChange={(e) => setMoleculeName(e.target.value)}
                  disabled={isLoading}
                  className="pl-12 h-14 bg-transparent border-0 focus:ring-0 text-lg"
                />
              </div>
              <Button
                type="submit"
                variant="hero"
                size="xl"
                disabled={!moleculeName.trim() || isLoading}
                className="min-w-[160px]"
              >
                <Sparkles className="w-5 h-5" />
                Analyze
              </Button>
            </div>
          </div>
        </div>

        {/* Example molecules */}
        <div className="flex flex-wrap items-center justify-center gap-2">
          <span className="text-sm text-muted-foreground">Try:</span>
          {exampleMolecules.map((molecule) => (
            <button
              key={molecule}
              type="button"
              onClick={() => setMoleculeName(molecule)}
              disabled={isLoading}
              className="px-3 py-1.5 text-sm rounded-full bg-secondary/50 text-muted-foreground hover:text-foreground hover:bg-secondary border border-border/50 hover:border-primary/50 transition-all duration-300 disabled:opacity-50"
            >
              {molecule}
            </button>
          ))}
        </div>
      </form>

      {/* Features */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4 pt-8">
        {[
          { title: 'Market Intelligence', desc: 'IQVIA data & trends analysis' },
          { title: 'Patent Research', desc: 'USPTO, EPO, WIPO scanning' },
          { title: 'Regulatory Insights', desc: 'FDA, EMA compliance check' },
        ].map((feature, i) => (
          <div
            key={feature.title}
            className="glass rounded-xl p-5 text-center group hover:border-primary/30 transition-all duration-300"
            style={{ animationDelay: `${i * 100}ms` }}
          >
            <div className="w-10 h-10 rounded-lg bg-primary/10 flex items-center justify-center mx-auto mb-3 group-hover:bg-primary/20 transition-colors">
              <div className="w-2 h-2 rounded-full bg-primary" />
            </div>
            <h3 className="font-medium text-foreground mb-1">{feature.title}</h3>
            <p className="text-sm text-muted-foreground">{feature.desc}</p>
          </div>
        ))}
      </div>
    </div>
  );
};
