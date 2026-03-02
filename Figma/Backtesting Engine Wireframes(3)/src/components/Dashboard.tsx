import { Card, CardContent, CardHeader, CardTitle } from "./ui/card";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "./ui/table";
import { Badge } from "./ui/badge";

export function Dashboard() {
  // Mock KPI data
  const kpis = [
    { label: "Total Strategies", value: "12", change: "+2" },
    { label: "Active Backtests", value: "3", change: "0" },
    { label: "Avg. Sharpe Ratio", value: "1.42", change: "+0.18" },
    { label: "Best Strategy ROI", value: "23.4%", change: "+5.2%" },
  ];

  // Mock recent backtests data
  const recentBacktests = [
    { id: "BT-001", strategy: "Mean Reversion v2", status: "Completed", duration: "2h 15m", sharpe: "1.34", roi: "18.2%" },
    { id: "BT-002", strategy: "Momentum Strategy", status: "Running", duration: "45m", sharpe: "-", roi: "-" },
    { id: "BT-003", strategy: "Pairs Trading", status: "Failed", duration: "1h 32m", sharpe: "-", roi: "-" },
    { id: "BT-004", strategy: "RSI Breakout", status: "Completed", duration: "3h 8m", sharpe: "0.89", roi: "12.7%" },
    { id: "BT-005", strategy: "MACD Cross", status: "Completed", duration: "1h 55m", sharpe: "2.11", roi: "31.5%" },
  ];

  const getStatusBadge = (status: string) => {
    switch (status) {
      case "Completed":
        return <Badge className="bg-primary/20 text-primary border-primary/30">Completed</Badge>;
      case "Running":
        return <Badge className="bg-primary/10 text-primary border-primary/20 animate-pulse">Running</Badge>;
      case "Failed":
        return <Badge variant="destructive">Failed</Badge>;
      default:
        return <Badge variant="secondary">{status}</Badge>;
    }
  };

  return (
    <div className="space-y-6">
      {/* Page Header */}
      <div>
        <h1>Dashboard</h1>
        <p className="text-muted-foreground">Overview of your backtesting activities</p>
      </div>

      {/* KPIs Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        {kpis.map((kpi, index) => (
          <Card key={index} className="border-border/50 bg-card/50 backdrop-blur-sm hover:border-primary/30 transition-all duration-300">
            <CardHeader className="pb-2">
              <CardTitle className="text-sm font-medium text-muted-foreground">
                {kpi.label}
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold text-primary">{kpi.value}</div>
              <p className="text-xs text-primary/80">
                {kpi.change} from last week
              </p>
            </CardContent>
          </Card>
        ))}
      </div>

      {/* Recent Backtests */}
      <Card className="border-border/50 bg-card/50 backdrop-blur-sm">
        <CardHeader>
          <CardTitle className="text-primary">Recent Backtests</CardTitle>
        </CardHeader>
        <CardContent>
          <Table>
            <TableHeader>
              <TableRow className="border-border/50">
                <TableHead className="text-muted-foreground">Backtest ID</TableHead>
                <TableHead className="text-muted-foreground">Strategy</TableHead>
                <TableHead className="text-muted-foreground">Status</TableHead>
                <TableHead className="text-muted-foreground">Duration</TableHead>
                <TableHead className="text-muted-foreground">Sharpe Ratio</TableHead>
                <TableHead className="text-muted-foreground">ROI</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {recentBacktests.map((backtest) => (
                <TableRow key={backtest.id} className="border-border/30 hover:bg-muted/20 transition-colors">
                  <TableCell className="font-mono text-primary/80">{backtest.id}</TableCell>
                  <TableCell className="font-medium">{backtest.strategy}</TableCell>
                  <TableCell>{getStatusBadge(backtest.status)}</TableCell>
                  <TableCell className="text-muted-foreground">{backtest.duration}</TableCell>
                  <TableCell className="text-primary">{backtest.sharpe}</TableCell>
                  <TableCell className="text-primary font-medium">{backtest.roi}</TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </CardContent>
      </Card>
    </div>
  );
}