import { Card, CardContent, CardHeader, CardTitle } from "./ui/card";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "./ui/table";
import { Badge } from "./ui/badge";
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, BarChart, Bar } from "recharts";

export function ReportScreen() {
  // Mock equity curve data
  const equityCurveData = [
    { date: "2023-01", portfolio: 100000, benchmark: 100000 },
    { date: "2023-02", portfolio: 102500, benchmark: 101200 },
    { date: "2023-03", portfolio: 98800, benchmark: 99800 },
    { date: "2023-04", portfolio: 105200, benchmark: 102100 },
    { date: "2023-05", portfolio: 108900, benchmark: 103500 },
    { date: "2023-06", portfolio: 112400, benchmark: 104800 },
    { date: "2023-07", portfolio: 115800, benchmark: 106200 },
    { date: "2023-08", portfolio: 118500, benchmark: 107100 },
    { date: "2023-09", portfolio: 121200, benchmark: 108500 },
    { date: "2023-10", portfolio: 119800, benchmark: 107800 },
    { date: "2023-11", portfolio: 123400, benchmark: 109200 },
    { date: "2023-12", portfolio: 126800, benchmark: 110500 },
  ];

  // Mock monthly returns data
  const monthlyReturnsData = [
    { month: "Jan", returns: 2.5 },
    { month: "Feb", returns: -2.1 },
    { month: "Mar", returns: 6.5 },
    { month: "Apr", returns: 3.5 },
    { month: "May", returns: 3.1 },
    { month: "Jun", returns: 2.8 },
    { month: "Jul", returns: 2.9 },
    { month: "Aug", returns: 2.3 },
    { month: "Sep", returns: 2.2 },
    { month: "Oct", returns: -1.2 },
    { month: "Nov", returns: 3.0 },
    { month: "Dec", returns: 2.8 },
  ];

  // Mock trades data
  const tradesData = [
    {
      id: "T001",
      date: "2023-12-28",
      symbol: "AAPL",
      side: "BUY",
      quantity: 100,
      price: 193.58,
      pnl: "+$1,247.80",
      pnlPercent: "+6.4%"
    },
    {
      id: "T002", 
      date: "2023-12-27",
      symbol: "MSFT",
      side: "SELL",
      quantity: 50,
      price: 374.51,
      pnl: "-$432.10",
      pnlPercent: "-2.3%"
    },
    {
      id: "T003",
      date: "2023-12-26",
      symbol: "GOOGL",
      side: "BUY",
      quantity: 75,
      price: 140.93,
      pnl: "+$2,891.25",
      pnlPercent: "+12.1%"
    },
    {
      id: "T004",
      date: "2023-12-22",
      symbol: "TSLA",
      side: "SELL", 
      quantity: 25,
      price: 254.50,
      pnl: "+$987.50",
      pnlPercent: "+15.8%"
    },
    {
      id: "T005",
      date: "2023-12-21",
      symbol: "NVDA",
      side: "BUY",
      quantity: 40,
      price: 495.22,
      pnl: "-$156.80",
      pnlPercent: "-0.8%"
    },
  ];

  // Performance metrics
  const performanceMetrics = [
    { label: "Total Return", value: "26.8%", benchmark: "10.5%" },
    { label: "Annualized Return", value: "24.2%", benchmark: "9.8%" },
    { label: "Sharpe Ratio", value: "1.84", benchmark: "0.92" },
    { label: "Max Drawdown", value: "-8.2%", benchmark: "-12.1%" },
    { label: "Win Rate", value: "68.4%", benchmark: "52.1%" },
    { label: "Profit Factor", value: "2.34", benchmark: "1.12" },
  ];

  return (
    <div className="space-y-6">
      {/* Page Header */}
      <div>
        <h1>Backtest Report</h1>
        <p className="text-muted-foreground">Detailed analysis of your strategy performance</p>
      </div>

      {/* Performance Metrics */}
      <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-4">
        {performanceMetrics.map((metric, index) => (
          <Card key={index} className="border-border/50 bg-card/50 backdrop-blur-sm hover:border-primary/30 transition-all duration-300">
            <CardHeader className="pb-2">
              <CardTitle className="text-xs text-muted-foreground">
                {metric.label}
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="text-lg font-bold text-primary">{metric.value}</div>
              <div className="text-xs text-muted-foreground">
                Benchmark: {metric.benchmark}
              </div>
            </CardContent>
          </Card>
        ))}
      </div>

      {/* Charts Section */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Equity Curve */}
        <Card className="border-border/50 bg-card/50 backdrop-blur-sm">
          <CardHeader>
            <CardTitle className="text-primary">Equity Curve</CardTitle>
          </CardHeader>
          <CardContent>
            <ResponsiveContainer width="100%" height={300}>
              <LineChart data={equityCurveData}>
                <CartesianGrid strokeDasharray="3 3" stroke="#333333" />
                <XAxis dataKey="date" stroke="#888888" />
                <YAxis stroke="#888888" />
                <Tooltip 
                  formatter={(value) => [`${value.toLocaleString()}`, '']} 
                  contentStyle={{ 
                    backgroundColor: '#111111', 
                    border: '1px solid #333333',
                    borderRadius: '8px',
                    color: '#ffffff'
                  }}
                />
                <Line 
                  type="monotone" 
                  dataKey="portfolio" 
                  stroke="#00ff88" 
                  strokeWidth={3}
                  name="Strategy"
                  dot={{ fill: '#00ff88', strokeWidth: 2, r: 4 }}
                />
                <Line 
                  type="monotone" 
                  dataKey="benchmark" 
                  stroke="#888888" 
                  strokeWidth={2}
                  strokeDasharray="5 5"
                  name="Benchmark"
                  dot={{ fill: '#888888', strokeWidth: 1, r: 2 }}
                />
              </LineChart>
            </ResponsiveContainer>
          </CardContent>
        </Card>

        {/* Monthly Returns */}
        <Card className="border-border/50 bg-card/50 backdrop-blur-sm">
          <CardHeader>
            <CardTitle className="text-primary">Monthly Returns</CardTitle>
          </CardHeader>
          <CardContent>
            <ResponsiveContainer width="100%" height={300}>
              <BarChart data={monthlyReturnsData}>
                <CartesianGrid strokeDasharray="3 3" stroke="#333333" />
                <XAxis dataKey="month" stroke="#888888" />
                <YAxis stroke="#888888" />
                <Tooltip 
                  formatter={(value) => [`${value}%`, 'Returns']} 
                  contentStyle={{ 
                    backgroundColor: '#111111', 
                    border: '1px solid #333333',
                    borderRadius: '8px',
                    color: '#ffffff'
                  }}
                />
                <Bar 
                  dataKey="returns" 
                  fill="#00ff88"
                  radius={[4, 4, 0, 0]}
                />
              </BarChart>
            </ResponsiveContainer>
          </CardContent>
        </Card>
      </div>

      {/* Trades Table */}
      <Card className="border-border/50 bg-card/50 backdrop-blur-sm">
        <CardHeader>
          <CardTitle className="text-primary">Recent Trades</CardTitle>
        </CardHeader>
        <CardContent>
          <Table>
            <TableHeader>
              <TableRow className="border-border/50">
                <TableHead className="text-muted-foreground">Trade ID</TableHead>
                <TableHead className="text-muted-foreground">Date</TableHead>
                <TableHead className="text-muted-foreground">Symbol</TableHead>
                <TableHead className="text-muted-foreground">Side</TableHead>
                <TableHead className="text-muted-foreground">Quantity</TableHead>
                <TableHead className="text-muted-foreground">Price</TableHead>
                <TableHead className="text-muted-foreground">P&L</TableHead>
                <TableHead className="text-muted-foreground">P&L %</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {tradesData.map((trade) => (
                <TableRow key={trade.id} className="border-border/30 hover:bg-muted/20 transition-colors">
                  <TableCell className="font-mono text-sm text-primary/80">{trade.id}</TableCell>
                  <TableCell>{trade.date}</TableCell>
                  <TableCell className="font-medium text-primary">{trade.symbol}</TableCell>
                  <TableCell>
                    <Badge className={trade.side === "BUY" ? "bg-primary/20 text-primary border-primary/30" : "bg-secondary text-secondary-foreground"}>
                      {trade.side}
                    </Badge>
                  </TableCell>
                  <TableCell>{trade.quantity}</TableCell>
                  <TableCell>${trade.price}</TableCell>
                  <TableCell className={trade.pnl.startsWith('+') ? 'text-primary font-medium' : 'text-destructive'}>
                    {trade.pnl}
                  </TableCell>
                  <TableCell className={trade.pnlPercent.startsWith('+') ? 'text-primary font-medium' : 'text-destructive'}>
                    {trade.pnlPercent}
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </CardContent>
      </Card>

      {/* Export Actions */}
      <div className="flex justify-end space-x-4">
        <button className="px-4 py-2 border border-border rounded-md hover:bg-muted transition-colors">
          Export CSV
        </button>
        <button className="px-4 py-2 border border-border rounded-md hover:bg-muted transition-colors">
          Export PDF
        </button>
        <button className="px-4 py-2 bg-primary text-primary-foreground rounded-md hover:bg-primary/90 transition-colors">
          Save Report
        </button>
      </div>
    </div>
  );
}