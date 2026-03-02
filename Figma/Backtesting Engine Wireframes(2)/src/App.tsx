import { Tabs, TabsContent, TabsList, TabsTrigger } from "./components/ui/tabs";
import { Dashboard } from "./components/Dashboard";
import { StrategyConfiguration } from "./components/StrategyConfiguration"; 
import { BacktestExecution } from "./components/BacktestExecution";
import { ReportScreen } from "./components/ReportScreen";
import { LayoutDashboard, Settings, Play, FileText } from "lucide-react";

export default function App() {
  return (
    <div className="min-h-screen bg-background">
      {/* Header */}
      <header className="border-b border-border bg-card px-6 py-4">
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-xl font-semibold">Backtesting Platform</h1>
            <p className="text-sm text-muted-foreground">Strategy Development & Analysis</p>
          </div>
          <div className="text-sm text-muted-foreground flex items-center gap-2">
            <div className="w-2 h-2 bg-primary rounded-full animate-pulse"></div>
            System Ready
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="container mx-auto px-6 py-6">
        <Tabs defaultValue="dashboard" className="space-y-6">
          <TabsList className="grid w-full grid-cols-4">
            <TabsTrigger value="dashboard" className="flex items-center gap-2">
              <LayoutDashboard className="h-4 w-4" />
              Dashboard
            </TabsTrigger>
            <TabsTrigger value="strategy" className="flex items-center gap-2">
              <Settings className="h-4 w-4" />
              Strategy Config
            </TabsTrigger>
            <TabsTrigger value="execution" className="flex items-center gap-2">
              <Play className="h-4 w-4" />
              Execution
            </TabsTrigger>
            <TabsTrigger value="report" className="flex items-center gap-2">
              <FileText className="h-4 w-4" />
              Report
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
        </Tabs>
      </main>
    </div>
  );
}