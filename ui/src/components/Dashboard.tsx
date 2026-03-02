import { Card, CardContent, CardHeader, CardTitle } from "./ui/card";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "./ui/table";
import { Badge } from "./ui/badge";
import { useState, useEffect } from "react";
import { TrendingUp, BarChart3, Activity, Award, ArrowUpRight, ArrowDownRight } from "lucide-react";
import { apiClient } from "@/lib/api";

export function Dashboard() {
  const [kpis, setKpis] = useState([
    { label: "Total Strategies", value: "0", change: "+0", positive: true, icon: BarChart3 },
    { label: "Active Backtests", value: "0", change: "0", positive: true, icon: Activity },
    { label: "Avg. Sharpe Ratio", value: "0.00", change: "+0.00", positive: true, icon: TrendingUp },
    { label: "Best Strategy ROI", value: "0%", change: "+0%", positive: true, icon: Award },
  ]);
  const [recentBacktests, setRecentBacktests] = useState<any[]>([]);

  useEffect(() => {
    fetchDashboardData();
  }, []);

  const fetchDashboardData = async () => {
    try {
      const [stats, backtests] = await Promise.all([
        apiClient.getDashboardStats() as any,
        apiClient.getRecentBacktests() as any
      ]);

      setKpis([
        { label: "Total Strategies", value: stats.total_strategies.toString(), change: "+2", positive: true, icon: BarChart3 },
        { label: "Active Backtests", value: stats.active_backtests.toString(), change: "0", positive: true, icon: Activity },
        { label: "Avg. Sharpe Ratio", value: stats.avg_sharpe_ratio.toFixed(2), change: "+0.18", positive: true, icon: TrendingUp },
        { label: "Best Strategy ROI", value: `${stats.best_strategy_roi}%`, change: "+5.2%", positive: parseFloat(stats.best_strategy_roi) >= 0, icon: Award },
      ]);

      setRecentBacktests(backtests);
    } catch (error) {
      console.error('Failed to fetch dashboard data:', error);
    }
  };

  const kpiGradients = [
    "from-violet-500/10 to-purple-500/10 border-violet-500/20",
    "from-cyan-500/10 to-blue-500/10 border-cyan-500/20",
    "from-emerald-500/10 to-green-500/10 border-emerald-500/20",
    "from-amber-500/10 to-orange-500/10 border-amber-500/20",
  ];

  const kpiIconColors = [
    "text-violet-400",
    "text-cyan-400",
    "text-emerald-400",
    "text-amber-400",
  ];

  const getStatusBadge = (status: string) => {
    switch (status) {
      case "Completed":
        return <Badge className="bg-emerald-500/15 text-emerald-400 border-emerald-500/30 font-medium">Completed</Badge>;
      case "Running":
        return <Badge className="bg-blue-500/15 text-blue-400 border-blue-500/30 animate-pulse font-medium">Running</Badge>;
      case "Failed":
        return <Badge className="bg-red-500/15 text-red-400 border-red-500/30 font-medium">Failed</Badge>;
      default:
        return <Badge variant="secondary">{status}</Badge>;
    }
  };

  return (
    <div className="space-y-6">
      {/* Page Header */}
      <div>
        <h1 className="text-2xl font-semibold tracking-tight">Dashboard</h1>
        <p className="text-muted-foreground">Overview of your backtesting activities</p>
      </div>

      {/* KPIs Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        {kpis.map((kpi, index) => {
          const Icon = kpi.icon;
          return (
            <Card key={index} className={`bg-gradient-to-br ${kpiGradients[index]} backdrop-blur-sm hover:scale-[1.02] transition-all duration-300 cursor-default group`}>
              <CardContent className="pt-5 pb-4">
                <div className="flex items-start justify-between mb-2">
                  <p className="text-sm font-medium text-muted-foreground">{kpi.label}</p>
                  <div className={`h-8 w-8 rounded-lg bg-background/50 flex items-center justify-center ${kpiIconColors[index]} group-hover:scale-110 transition-transform`}>
                    <Icon className="h-4 w-4" />
                  </div>
                </div>
                <div className="text-3xl font-bold tracking-tight">{kpi.value}</div>
                <div className="flex items-center gap-1 mt-1">
                  {kpi.positive ? (
                    <ArrowUpRight className="h-3 w-3 text-emerald-400" />
                  ) : (
                    <ArrowDownRight className="h-3 w-3 text-red-400" />
                  )}
                  <p className={`text-xs font-medium ${kpi.positive ? "text-emerald-400" : "text-red-400"}`}>
                    {kpi.change} from last week
                  </p>
                </div>
              </CardContent>
            </Card>
          );
        })}
      </div>

      {/* Recent Backtests */}
      <Card className="border-border/50 bg-card/50 backdrop-blur-sm overflow-hidden">
        <CardHeader className="border-b border-border/30">
          <CardTitle className="text-lg font-semibold">Recent Backtests</CardTitle>
        </CardHeader>
        <CardContent className="p-0">
          {recentBacktests.length === 0 ? (
            <div className="py-12 text-center">
              <p className="text-muted-foreground">No backtests yet. Configure a strategy and run your first backtest!</p>
            </div>
          ) : (
            <Table>
              <TableHeader>
                <TableRow className="border-border/30 hover:bg-transparent">
                  <TableHead className="text-muted-foreground text-xs uppercase tracking-wider">ID</TableHead>
                  <TableHead className="text-muted-foreground text-xs uppercase tracking-wider">Strategy</TableHead>
                  <TableHead className="text-muted-foreground text-xs uppercase tracking-wider">Status</TableHead>
                  <TableHead className="text-muted-foreground text-xs uppercase tracking-wider">Duration</TableHead>
                  <TableHead className="text-muted-foreground text-xs uppercase tracking-wider">Sharpe</TableHead>
                  <TableHead className="text-muted-foreground text-xs uppercase tracking-wider">ROI</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {recentBacktests.map((backtest: any) => (
                  <TableRow key={backtest.id} className="border-border/20 hover:bg-muted/10 transition-colors">
                    <TableCell className="font-mono text-xs text-muted-foreground">{backtest.id?.slice(0, 8)}</TableCell>
                    <TableCell className="font-medium">{backtest.strategy}</TableCell>
                    <TableCell>{getStatusBadge(backtest.status)}</TableCell>
                    <TableCell className="text-muted-foreground text-sm">{backtest.duration}</TableCell>
                    <TableCell className="text-primary font-medium">{backtest.sharpe}</TableCell>
                    <TableCell className="font-semibold">{backtest.roi}</TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          )}
        </CardContent>
      </Card>
    </div>
  );
}