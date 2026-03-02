import { Card, CardContent, CardHeader, CardTitle } from "./ui/card";
import { Input } from "./ui/input";
import { Label } from "./ui/label";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "./ui/select";
import { Button } from "./ui/button";
import { Progress } from "./ui/progress";
import { Badge } from "./ui/badge";
import { Play, Pause, Square } from "lucide-react";
import { useState, useEffect } from "react";
import { apiClient } from "../lib/api";
import { useToast } from "./ui/use-toast";

export function BacktestExecution() {
  const { toast } = useToast();
  const [strategies, setStrategies] = useState<any[]>([]);
  const [selectedStrategy, setSelectedStrategy] = useState("");
  const [startDate, setStartDate] = useState("2023-01-01");
  const [endDate, setEndDate] = useState("2023-12-31");
  const [initialCapital, setInitialCapital] = useState(100000);
  const [commission, setCommission] = useState(0.001);
  const [slippage, setSlippage] = useState(0.0005);
  const [dataSource, setDataSource] = useState("synthetic");
  const [ticker, setTicker] = useState("AAPL");
  const [timeframe, setTimeframe] = useState("1d");  // NEW: Add timeframe state

  const [isRunning, setIsRunning] = useState(false);
  const [backtestId, setBacktestId] = useState<string | null>(null);
  const [progress, setProgress] = useState(0);
  const [currentStep, setCurrentStep] = useState("Ready to start");
  const [estimatedTime, setEstimatedTime] = useState<string | null>(null);

  // Load strategies on mount
  useEffect(() => {
    loadStrategies();
  }, []);

  // Poll for backtest status when running
  useEffect(() => {
    if (!isRunning || !backtestId) return;

    const interval = setInterval(async () => {
      try {
        const status = await apiClient.getBacktestStatus(backtestId);
        setProgress(status.progress);
        setCurrentStep(status.current_step);
        setEstimatedTime(status.estimated_time_remaining || null);

        if (status.status === "completed") {
          setIsRunning(false);
          toast({
            title: "Backtest Complete",
            description: "Your backtest has finished successfully. Check the Report tab for results.",
          });
        } else if (status.status === "failed") {
          setIsRunning(false);
          toast({
            title: "Backtest Failed",
            description: status.current_step,
            variant: "destructive",
          });
        }
      } catch (error) {
        console.error("Error polling backtest status:", error);
      }
    }, 1000);

    return () => clearInterval(interval);
  }, [isRunning, backtestId]);

  const loadStrategies = async () => {
    try {
      const data = await apiClient.get<any[]>('/strategies');
      setStrategies(data);
      if (data.length > 0) {
        setSelectedStrategy(data[0].name);
      }
    } catch (error) {
      console.error('Failed to load strategies:', error);
      toast({
        title: "Error",
        description: "Failed to load strategies. Make sure you've created some strategies first.",
        variant: "destructive",
      });
    }
  };

  const handleStart = async () => {
    if (!selectedStrategy) {
      toast({
        title: "No Strategy Selected",
        description: "Please select a strategy before starting the backtest.",
        variant: "destructive",
      });
      return;
    }

    try {
      setIsRunning(true);
      setProgress(0);
      setCurrentStep("Initializing backtest...");

      const config = {
        strategy_name: selectedStrategy,
        start_date: startDate,
        end_date: endDate,
        initial_capital: initialCapital,
        commission: commission,
        slippage: slippage,
        data_source: dataSource,
        ticker: ticker,
        timeframe: timeframe,  // NEW: Include timeframe in config
      };

      const response = await apiClient.startBacktest(config);
      setBacktestId(response.backtest_id);

      toast({
        title: "Backtest Started",
        description: `Running backtest for ${selectedStrategy}`,
      });
    } catch (error: any) {
      console.error("Failed to start backtest:", error);
      setIsRunning(false);
      toast({
        title: "Failed to Start",
        description: error.message || "Could not start backtest",
        variant: "destructive",
      });
    }
  };

  const handlePause = async () => {
    if (!backtestId) return;

    try {
      await apiClient.pauseBacktest(backtestId);
      setIsRunning(false);
      setCurrentStep("Backtest paused");
      toast({
        title: "Backtest Paused",
        description: "You can resume it later.",
      });
    } catch (error) {
      console.error("Failed to pause backtest:", error);
    }
  };

  const handleStop = async () => {
    if (!backtestId) return;

    try {
      await apiClient.stopBacktest(backtestId);
      setIsRunning(false);
      setProgress(0);
      setCurrentStep("Backtest stopped");
      setBacktestId(null);
      toast({
        title: "Backtest Stopped",
        description: "The backtest has been terminated.",
      });
    } catch (error) {
      console.error("Failed to stop backtest:", error);
    }
  };

  return (
    <div className="space-y-6">
      {/* Page Header */}
      <div>
        <h1>Backtest Execution</h1>
        <p className="text-muted-foreground">Configure and run your strategy backtest</p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Settings Panel */}
        <div className="lg:col-span-2 space-y-6">
          <Card className="border-border/50 bg-card/50 backdrop-blur-sm">
            <CardHeader>
              <CardTitle className="text-primary">Backtest Settings</CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="space-y-2">
                <Label htmlFor="strategy-select">Select Strategy</Label>
                <Select value={selectedStrategy} onValueChange={setSelectedStrategy}>
                  <SelectTrigger>
                    <SelectValue placeholder="Choose a strategy" />
                  </SelectTrigger>
                  <SelectContent>
                    {strategies.length === 0 ? (
                      <SelectItem value="none" disabled>No strategies available</SelectItem>
                    ) : (
                      strategies.map((strategy) => (
                        <SelectItem key={strategy.id} value={strategy.name}>
                          {strategy.name}
                        </SelectItem>
                      ))
                    )}
                  </SelectContent>
                </Select>
                {strategies.length === 0 && (
                  <p className="text-xs text-muted-foreground">
                    Create a strategy in the Strategy Config tab first.
                  </p>
                )}
              </div>

              <div className="grid grid-cols-2 gap-4">
                <div className="space-y-2">
                  <Label>Start Date</Label>
                  <Input
                    type="date"
                    value={startDate}
                    onChange={(e) => setStartDate(e.target.value)}
                    className="w-full"
                  />
                </div>

                <div className="space-y-2">
                  <Label>End Date</Label>
                  <Input
                    type="date"
                    value={endDate}
                    onChange={(e) => setEndDate(e.target.value)}
                    className="w-full"
                  />
                </div>
              </div>

              <div className="space-y-2">
                <Label htmlFor="initial-capital">Initial Capital ($)</Label>
                <Input
                  id="initial-capital"
                  type="number"
                  value={initialCapital}
                  onChange={(e) => setInitialCapital(parseFloat(e.target.value) || 100000)}
                />
              </div>

              <div className="space-y-2">
                <Label htmlFor="commission">Commission (%)</Label>
                <Input
                  id="commission"
                  type="number"
                  step="0.001"
                  value={commission}
                  onChange={(e) => setCommission(parseFloat(e.target.value) || 0.001)}
                />
              </div>

              <div className="space-y-2">
                <Label htmlFor="slippage">Slippage (%)</Label>
                <Input
                  id="slippage"
                  type="number"
                  step="0.0001"
                  value={slippage}
                  onChange={(e) => setSlippage(parseFloat(e.target.value) || 0.0005)}
                />
              </div>

              <div className="space-y-2">
                <Label htmlFor="data-source">Data Source</Label>
                <Select value={dataSource} onValueChange={setDataSource}>
                  <SelectTrigger>
                    <SelectValue placeholder="Select data provider" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="synthetic">Synthetic (Demo Data)</SelectItem>
                    <SelectItem value="yahoo">Yahoo Finance (Real Data)</SelectItem>
                    <SelectItem value="alpha-vantage" disabled>Alpha Vantage (API Key Required)</SelectItem>
                    <SelectItem value="quandl" disabled>Quandl (Coming Soon)</SelectItem>
                  </SelectContent>
                </Select>
              </div>

              {dataSource === "yahoo" && (
                <>
                  <div className="space-y-2">
                    <Label htmlFor="ticker">Stock Ticker</Label>
                    <Input
                      id="ticker"
                      type="text"
                      placeholder="AAPL, TSLA, MSFT, etc."
                      value={ticker}
                      onChange={(e) => setTicker(e.target.value.toUpperCase())}
                    />
                    <p className="text-xs text-muted-foreground">
                      Enter a valid stock ticker symbol from Yahoo Finance
                    </p>
                  </div>

                  <div className="space-y-2">
                    <Label htmlFor="timeframe">Timeframe</Label>
                    <Select value={timeframe} onValueChange={setTimeframe}>
                      <SelectTrigger>
                        <SelectValue placeholder="Select timeframe" />
                      </SelectTrigger>
                      <SelectContent>
                        <SelectItem value="1m">1 Minute ⚠️ (max 7 days)</SelectItem>
                        <SelectItem value="5m">5 Minutes ⚠️ (max 60 days)</SelectItem>
                        <SelectItem value="15m">15 Minutes (max 2 years)</SelectItem>
                        <SelectItem value="1h">1 Hour (max 2 years)</SelectItem>
                        <SelectItem value="1d">1 Day ✅ (Recommended - Any range)</SelectItem>
                        <SelectItem value="1w">1 Week (Any range)</SelectItem>
                      </SelectContent>
                    </Select>
                    <p className="text-xs text-muted-foreground">
                      ⚠️ Yahoo Finance limits historical intraday data. Use 1 Day for date ranges over 60 days.
                    </p>
                  </div>
                </>
              )}
            </CardContent>
          </Card>
        </div>

        {/* Execution Panel */}
        <div className="space-y-6">
          <Card className="border-border/50 bg-card/50 backdrop-blur-sm">
            <CardHeader>
              <CardTitle className="text-primary">Execution Control</CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="flex space-x-2">
                <Button
                  onClick={handleStart}
                  disabled={isRunning}
                  className="flex-1 bg-primary hover:bg-primary/90 text-primary-foreground"
                >
                  <Play className="mr-2 h-4 w-4" />
                  Start
                </Button>
                <Button
                  variant="outline"
                  onClick={handlePause}
                  disabled={!isRunning}
                  className="border-border hover:bg-muted"
                >
                  <Pause className="h-4 w-4" />
                </Button>
                <Button
                  variant="outline"
                  onClick={handleStop}
                  className="border-destructive/30 text-destructive hover:bg-destructive/10"
                >
                  <Square className="h-4 w-4" />
                </Button>
              </div>

              <div className="space-y-2">
                <div className="flex justify-between items-center">
                  <Label>Progress</Label>
                  <span className="text-sm text-muted-foreground">{progress}%</span>
                </div>
                <Progress value={progress} className="w-full" />
              </div>

              <div className="space-y-2">
                <Label>Current Status</Label>
                <div className="flex items-center space-x-2">
                  <Badge className={isRunning ? "bg-primary/20 text-primary border-primary/30 animate-pulse" : "bg-secondary text-secondary-foreground"}>
                    {isRunning ? "Running" : "Idle"}
                  </Badge>
                </div>
                <p className="text-sm text-muted-foreground">{currentStep}</p>
              </div>

              <div className="space-y-2">
                <Label>Estimated Time Remaining</Label>
                <p className="text-sm">
                  {estimatedTime || (isRunning ? "Calculating..." : "Not running")}
                </p>
              </div>
            </CardContent>
          </Card>

          {isRunning && (
            <Card className="border-border/50 bg-card/50 backdrop-blur-sm">
              <CardHeader>
                <CardTitle className="text-primary">Backtest Info</CardTitle>
              </CardHeader>
              <CardContent className="space-y-3">
                <div className="flex justify-between">
                  <span className="text-sm text-muted-foreground">Strategy</span>
                  <span className="text-sm text-primary font-medium">{selectedStrategy}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-sm text-muted-foreground">Period</span>
                  <span className="text-sm">{startDate} to {endDate}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-sm text-muted-foreground">Initial Capital</span>
                  <span className="text-sm">${initialCapital.toLocaleString()}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-sm text-muted-foreground">Backtest ID</span>
                  <span className="text-xs font-mono">{backtestId?.slice(0, 8)}...</span>
                </div>
              </CardContent>
            </Card>
          )}
        </div>
      </div>
    </div>
  );
}