import { Card, CardContent, CardHeader, CardTitle } from "./ui/card";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "./ui/table";
import { Badge } from "./ui/badge";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "./ui/select";
import { XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, BarChart, Bar, Area, AreaChart } from "recharts";
import { useState, useEffect } from "react";
import { apiClient } from "@/lib/api";
import { TrendingUp, TrendingDown, Target, Percent, Layers } from "lucide-react";

export function ReportScreen() {
  const [backtests, setBacktests] = useState<any[]>([]);
  const [selectedBacktest, setSelectedBacktest] = useState<string>("");
  const [results, setResults] = useState<any>(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    loadBacktests();
  }, []);

  const loadBacktests = async () => {
    try {
      const data = await apiClient.get<any[]>('/backtests');
      const completed = data.filter((bt: any) => bt.status === 'completed');
      setBacktests(completed);
      if (completed.length > 0 && !selectedBacktest) {
        setSelectedBacktest(completed[0].id);
      }
    } catch (error) {
      console.error('Failed to load backtests:', error);
    }
  };

  const loadBacktestResults = async (backtestId: string) => {
    setLoading(true);
    try {
      const data = await apiClient.get<any>(`/backtests/${backtestId}`);
      setResults(data);
    } catch (error) {
      console.error('Failed to load backtest results:', error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    if (selectedBacktest) loadBacktestResults(selectedBacktest);
  }, [selectedBacktest]);

  if (backtests.length === 0) {
    return (
      <div className="flex items-center justify-center h-[60vh]">
        <div className="text-center space-y-3">
          <div className="h-16 w-16 rounded-2xl bg-gradient-to-br from-violet-500/20 to-cyan-500/20 border border-violet-500/30 flex items-center justify-center mx-auto">
            <Layers className="h-8 w-8 text-violet-400" />
          </div>
          <h2 className="text-xl font-semibold">No Completed Backtests</h2>
          <p className="text-muted-foreground text-sm">Run a backtest first to see results here.</p>
        </div>
      </div>
    );
  }

  if (loading || !results) {
    return (
      <div className="flex items-center justify-center h-[60vh]">
        <div className="text-center space-y-2">
          <div className="h-8 w-8 border-2 border-primary border-t-transparent rounded-full animate-spin mx-auto" />
          <p className="text-sm text-muted-foreground">Loading backtest results...</p>
        </div>
      </div>
    );
  }

  const equityData = results.portfolio_data.map((row: any, index: number) => ({
    day: index + 1,
    equity: row.total,
    date: row.Date,
  }));

  const returnsData = results.portfolio_data
    .filter((_: any, i: number) => i > 0)
    .map((row: any, index: number) => ({
      day: index + 1,
      returns: row.daily_returns * 100,
    }));

  const monthlyReturns = results.portfolio_data.reduce((acc: any[], row: any, index: number) => {
    if (index === 0) return acc;
    const month = new Date(row.Date).toLocaleDateString('en-US', { month: 'short', year: 'numeric' });
    const existing = acc.find((item: any) => item.month === month);
    if (existing) {
      existing.returns += row.daily_returns * 100;
    } else {
      acc.push({ month, returns: row.daily_returns * 100 });
    }
    return acc;
  }, []);

  const metricCards = [
    {
      label: "Total Return",
      value: `${(results.metrics.total_return * 100).toFixed(2)}%`,
      positive: results.metrics.total_return >= 0,
      icon: results.metrics.total_return >= 0 ? TrendingUp : TrendingDown,
      gradient: "from-emerald-500/15 to-green-500/15 border-emerald-500/25",
      iconColor: results.metrics.total_return >= 0 ? "text-emerald-400" : "text-red-400",
    },
    {
      label: "Sharpe Ratio",
      value: results.metrics.sharpe_ratio.toFixed(2),
      positive: results.metrics.sharpe_ratio > 0,
      icon: Target,
      gradient: "from-violet-500/15 to-purple-500/15 border-violet-500/25",
      iconColor: "text-violet-400",
    },
    {
      label: "Max Drawdown",
      value: `${(results.metrics.max_drawdown * 100).toFixed(2)}%`,
      positive: false,
      icon: TrendingDown,
      gradient: "from-red-500/15 to-rose-500/15 border-red-500/25",
      iconColor: "text-red-400",
    },
    {
      label: "Win Rate",
      value: results.metrics.trade_win_rate !== undefined
        ? `${results.metrics.trade_win_rate.toFixed(1)}%`
        : results.metrics.winning_days
          ? `${(results.metrics.winning_days * 100).toFixed(1)}%`
          : '0.0%',
      positive: true,
      icon: Percent,
      gradient: "from-cyan-500/15 to-blue-500/15 border-cyan-500/25",
      iconColor: "text-cyan-400",
    },
  ];

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-2xl font-semibold tracking-tight">Backtest Report</h1>
          <p className="text-muted-foreground">Detailed analysis and performance metrics</p>
        </div>
        <Select value={selectedBacktest} onValueChange={setSelectedBacktest}>
          <SelectTrigger className="w-[320px] bg-card/50 backdrop-blur-sm border-border/50">
            <SelectValue placeholder="Select a backtest" />
          </SelectTrigger>
          <SelectContent>
            {backtests.map((bt) => (
              <SelectItem key={bt.id} value={bt.id}>
                {bt.config?.strategy_name} — {bt.completed_at ? new Date(bt.completed_at).toLocaleDateString() : 'N/A'}
              </SelectItem>
            ))}
          </SelectContent>
        </Select>
      </div>

      {/* Metric Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        {metricCards.map((metric, index) => {
          const Icon = metric.icon;
          return (
            <Card key={index} className={`bg-gradient-to-br ${metric.gradient} backdrop-blur-sm hover:scale-[1.02] transition-all duration-300`}>
              <CardContent className="pt-5 pb-4">
                <div className="flex items-start justify-between mb-2">
                  <p className="text-sm font-medium text-muted-foreground">{metric.label}</p>
                  <div className={`h-8 w-8 rounded-lg bg-background/50 flex items-center justify-center ${metric.iconColor}`}>
                    <Icon className="h-4 w-4" />
                  </div>
                </div>
                <div className={`text-3xl font-bold tracking-tight ${metric.positive ? "" : "text-red-400"}`}>
                  {metric.value}
                </div>
              </CardContent>
            </Card>
          );
        })}
      </div>

      {/* Equity Curve - Area Chart */}
      <Card className="border-border/50 bg-card/50 backdrop-blur-sm overflow-hidden">
        <CardHeader className="border-b border-border/30">
          <CardTitle className="text-lg font-semibold">Equity Curve</CardTitle>
        </CardHeader>
        <CardContent className="pt-6">
          <ResponsiveContainer width="100%" height={320}>
            <AreaChart data={equityData}>
              <defs>
                <linearGradient id="equityGradient" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="5%" stopColor="#8b5cf6" stopOpacity={0.3} />
                  <stop offset="95%" stopColor="#8b5cf6" stopOpacity={0.0} />
                </linearGradient>
              </defs>
              <CartesianGrid strokeDasharray="3 3" stroke="hsl(var(--border))" opacity={0.3} />
              <XAxis dataKey="day" stroke="hsl(var(--muted-foreground))" fontSize={12} />
              <YAxis stroke="hsl(var(--muted-foreground))" fontSize={12} tickFormatter={(v: number) => `$${(v / 1000).toFixed(0)}k`} />
              <Tooltip
                contentStyle={{ backgroundColor: 'hsl(var(--card))', border: '1px solid hsl(var(--border))', borderRadius: '8px' }}
                labelStyle={{ color: 'hsl(var(--muted-foreground))' }}
                formatter={(value: number) => [`$${value.toFixed(2)}`, 'Portfolio']}
              />
              <Area type="monotone" dataKey="equity" stroke="#8b5cf6" strokeWidth={2} fill="url(#equityGradient)" />
            </AreaChart>
          </ResponsiveContainer>
        </CardContent>
      </Card>

      {/* 2-col layout for returns + monthly */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <Card className="border-border/50 bg-card/50 backdrop-blur-sm">
          <CardHeader className="border-b border-border/30">
            <CardTitle className="text-lg font-semibold">Daily Returns</CardTitle>
          </CardHeader>
          <CardContent className="pt-6">
            <ResponsiveContainer width="100%" height={260}>
              <BarChart data={returnsData}>
                <CartesianGrid strokeDasharray="3 3" stroke="hsl(var(--border))" opacity={0.3} />
                <XAxis dataKey="day" stroke="hsl(var(--muted-foreground))" fontSize={11} />
                <YAxis stroke="hsl(var(--muted-foreground))" fontSize={11} tickFormatter={(v: number) => `${v.toFixed(1)}%`} />
                <Tooltip
                  contentStyle={{ backgroundColor: 'hsl(var(--card))', border: '1px solid hsl(var(--border))', borderRadius: '8px' }}
                  formatter={(value: number) => [`${value.toFixed(2)}%`, 'Return']}
                />
                <Bar dataKey="returns" fill="#8b5cf6" radius={[2, 2, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </CardContent>
        </Card>

        <Card className="border-border/50 bg-card/50 backdrop-blur-sm">
          <CardHeader className="border-b border-border/30">
            <CardTitle className="text-lg font-semibold">Monthly Performance</CardTitle>
          </CardHeader>
          <CardContent className="pt-6">
            <ResponsiveContainer width="100%" height={260}>
              <BarChart data={monthlyReturns}>
                <CartesianGrid strokeDasharray="3 3" stroke="hsl(var(--border))" opacity={0.3} />
                <XAxis dataKey="month" stroke="hsl(var(--muted-foreground))" fontSize={11} />
                <YAxis stroke="hsl(var(--muted-foreground))" fontSize={11} tickFormatter={(v: number) => `${v.toFixed(1)}%`} />
                <Tooltip
                  contentStyle={{ backgroundColor: 'hsl(var(--card))', border: '1px solid hsl(var(--border))', borderRadius: '8px' }}
                  formatter={(value: number) => [`${value.toFixed(2)}%`, 'Return']}
                />
                <Bar dataKey="returns" fill="#06b6d4" radius={[2, 2, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </CardContent>
        </Card>
      </div>

      {/* Trade History */}
      <Card className="border-border/50 bg-card/50 backdrop-blur-sm overflow-hidden">
        <CardHeader className="border-b border-border/30">
          <CardTitle className="text-lg font-semibold">Trade History</CardTitle>
        </CardHeader>
        <CardContent className="p-0">
          {results.trades && results.trades.length > 0 ? (
            <Table>
              <TableHeader>
                <TableRow className="border-border/30 hover:bg-transparent">
                  <TableHead className="text-muted-foreground text-xs uppercase tracking-wider">Date</TableHead>
                  <TableHead className="text-muted-foreground text-xs uppercase tracking-wider">Symbol</TableHead>
                  <TableHead className="text-muted-foreground text-xs uppercase tracking-wider">Side</TableHead>
                  <TableHead className="text-muted-foreground text-xs uppercase tracking-wider">Qty</TableHead>
                  <TableHead className="text-muted-foreground text-xs uppercase tracking-wider">Price</TableHead>
                  <TableHead className="text-muted-foreground text-xs uppercase tracking-wider">P&L</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {results.trades.map((trade: any, index: number) => (
                  <TableRow key={index} className="border-border/20 hover:bg-muted/10 transition-colors">
                    <TableCell className="text-sm">{new Date(trade.date).toLocaleDateString()}</TableCell>
                    <TableCell className="font-medium">{trade.ticker}</TableCell>
                    <TableCell>
                      <Badge className={trade.side === 'BUY'
                        ? 'bg-emerald-500/15 text-emerald-400 border-emerald-500/30'
                        : 'bg-red-500/15 text-red-400 border-red-500/30'
                      }>
                        {trade.side}
                      </Badge>
                    </TableCell>
                    <TableCell>{trade.quantity}</TableCell>
                    <TableCell className="font-mono">${trade.price.toFixed(2)}</TableCell>
                    <TableCell className={`font-semibold ${trade.pnl >= 0 ? 'text-emerald-400' : 'text-red-400'}`}>
                      {trade.pnl >= 0 ? '+' : ''}{trade.pnl.toFixed(2)}%
                    </TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          ) : (
            <div className="py-8 text-center text-muted-foreground text-sm">No trades executed in this backtest</div>
          )}
        </CardContent>
      </Card>

      {/* Detailed Metrics */}
      <Card className="border-border/50 bg-card/50 backdrop-blur-sm">
        <CardHeader className="border-b border-border/30">
          <CardTitle className="text-lg font-semibold">Detailed Performance Metrics</CardTitle>
        </CardHeader>
        <CardContent className="pt-6">
          <div className="grid grid-cols-2 md:grid-cols-3 gap-6">
            {[
              { label: "Annualized Return", value: `${(results.metrics.annualized_return * 100).toFixed(2)}%` },
              { label: "Sortino Ratio", value: results.metrics.sortino_ratio.toFixed(2) },
              { label: "Total Trades", value: results.trades?.length || 0 },
              { label: "Winning Days", value: results.metrics.winning_days ? `${(results.metrics.winning_days * 100).toFixed(2)}%` : '0.00%' },
              { label: "Total Days", value: results.portfolio_data.length },
              { label: "Strategy", value: results.config?.strategy_name },
            ].map((item, i) => (
              <div key={i} className="space-y-1">
                <p className="text-xs text-muted-foreground uppercase tracking-wider">{item.label}</p>
                <p className="text-lg font-semibold">{item.value}</p>
              </div>
            ))}
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
