import { Tabs, TabsContent, TabsList, TabsTrigger } from "./components/ui/tabs";
import { Dashboard } from "./components/Dashboard";
import { StrategyConfiguration } from "./components/StrategyConfiguration";
import { BacktestExecution } from "./components/BacktestExecution";
import { ReportScreen } from "./components/ReportScreen";
import { OptimizerScreen } from "./components/OptimizerScreen";
import { Toaster } from "./components/ui/toaster";
import { LayoutDashboard, Settings, Play, FileText, Zap, Sparkles } from "lucide-react";

export default function App() {
  return (
    <div className="min-h-screen bg-background">
      {/* Premium Header */}
      <header className="relative border-b border-border/50 bg-card/80 backdrop-blur-xl px-6 py-4 overflow-hidden">
        {/* Subtle gradient accent line at top */}
        <div className="absolute top-0 left-0 right-0 h-[2px] bg-gradient-to-r from-violet-500 via-cyan-500 to-emerald-500 opacity-80" />

        <div className="flex items-center justify-between relative z-10">
          <div className="flex items-center gap-3">
            <div className="h-9 w-9 rounded-lg bg-gradient-to-br from-violet-500 to-cyan-500 flex items-center justify-center shadow-lg shadow-violet-500/20">
              <Zap className="h-5 w-5 text-white" />
            </div>
            <div>
              <h1 className="text-xl font-bold tracking-tight bg-gradient-to-r from-foreground to-foreground/70 bg-clip-text">
                Backtesting Platform
              </h1>
              <p className="text-xs text-muted-foreground">Strategy Development & Analysis Engine</p>
            </div>
          </div>
          <div className="flex items-center gap-3">
            <div className="text-sm text-muted-foreground flex items-center gap-2 px-3 py-1.5 rounded-full bg-background/50 border border-border/50">
              <div className="w-2 h-2 bg-emerald-400 rounded-full animate-pulse shadow-sm shadow-emerald-400/50" />
              System Ready
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="container mx-auto px-6 py-6">
        <Tabs defaultValue="dashboard" className="space-y-6">
          <TabsList className="grid w-full grid-cols-5 bg-card/50 backdrop-blur-sm border border-border/30 rounded-xl p-1">
            <TabsTrigger value="dashboard" className="flex items-center gap-2 rounded-lg data-[state=active]:bg-gradient-to-r data-[state=active]:from-violet-500/10 data-[state=active]:to-cyan-500/10 data-[state=active]:border-violet-500/20 transition-all duration-300">
              <LayoutDashboard className="h-4 w-4" />
              Dashboard
            </TabsTrigger>
            <TabsTrigger value="strategy" className="flex items-center gap-2 rounded-lg data-[state=active]:bg-gradient-to-r data-[state=active]:from-violet-500/10 data-[state=active]:to-cyan-500/10 data-[state=active]:border-violet-500/20 transition-all duration-300">
              <Settings className="h-4 w-4" />
              Strategy Config
            </TabsTrigger>
            <TabsTrigger value="execution" className="flex items-center gap-2 rounded-lg data-[state=active]:bg-gradient-to-r data-[state=active]:from-violet-500/10 data-[state=active]:to-cyan-500/10 data-[state=active]:border-violet-500/20 transition-all duration-300">
              <Play className="h-4 w-4" />
              Execution
            </TabsTrigger>
            <TabsTrigger value="report" className="flex items-center gap-2 rounded-lg data-[state=active]:bg-gradient-to-r data-[state=active]:from-violet-500/10 data-[state=active]:to-cyan-500/10 data-[state=active]:border-violet-500/20 transition-all duration-300">
              <FileText className="h-4 w-4" />
              Report
            </TabsTrigger>
            <TabsTrigger value="optimizer" className="flex items-center gap-2 rounded-lg data-[state=active]:bg-gradient-to-r data-[state=active]:from-violet-500/10 data-[state=active]:to-cyan-500/10 data-[state=active]:border-violet-500/20 transition-all duration-300">
              <Sparkles className="h-4 w-4" />
              Optimizer
            </TabsTrigger>
          </TabsList>

          <TabsContent value="dashboard">
            <Dashboard />
          </TabsContent>

          <TabsContent value="strategy">
            <StrategyConfiguration />
          </TabsContent>

          <TabsContent value="execution">
            <BacktestExecution />
          </TabsContent>

          <TabsContent value="report">
            <ReportScreen />
          </TabsContent>

          <TabsContent value="optimizer">
            <OptimizerScreen />
          </TabsContent>
        </Tabs>
      </main>

      <Toaster />
    </div>
  );
}