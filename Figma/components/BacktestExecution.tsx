import { Card, CardContent, CardHeader, CardTitle } from "./ui/card";
import { Input } from "./ui/input";
import { Label } from "./ui/label";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "./ui/select";
import { Button } from "./ui/button";
import { Progress } from "./ui/progress";
import { Badge } from "./ui/badge";
import { Calendar } from "./ui/calendar";
import { Popover, PopoverContent, PopoverTrigger } from "./ui/popover";
import { CalendarIcon, Play, Pause, Square } from "lucide-react";
import { useState } from "react";

export function BacktestExecution() {
  const [isRunning, setIsRunning] = useState(false);
  const [progress, setProgress] = useState(45);
  const [currentStep, setCurrentStep] = useState("Loading historical data...");

  const handleStart = () => {
    setIsRunning(true);
    // Simulate progress updates
    const interval = setInterval(() => {
      setProgress(prev => {
        if (prev >= 100) {
          clearInterval(interval);
          setIsRunning(false);
          setCurrentStep("Backtest completed successfully");
          return 100;
        }
        return prev + 5;
      });
    }, 1000);
  };

  const handlePause = () => {
    setIsRunning(false);
    setCurrentStep("Backtest paused");
  };

  const handleStop = () => {
    setIsRunning(false);
    setProgress(0);
    setCurrentStep("Backtest stopped");
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
                <Select>
                  <SelectTrigger>
                    <SelectValue placeholder="Choose a strategy" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="strategy1">Mean Reversion v2</SelectItem>
                    <SelectItem value="strategy2">Momentum Strategy</SelectItem>
                    <SelectItem value="strategy3">Pairs Trading</SelectItem>
                    <SelectItem value="strategy4">RSI Breakout</SelectItem>
                  </SelectContent>
                </Select>
              </div>

              <div className="grid grid-cols-2 gap-4">
                <div className="space-y-2">
                  <Label>Start Date</Label>
                  <Popover>
                    <PopoverTrigger asChild>
                      <Button variant="outline" className="w-full justify-start">
                        <CalendarIcon className="mr-2 h-4 w-4" />
                        Jan 1, 2023
                      </Button>
                    </PopoverTrigger>
                    <PopoverContent className="w-auto p-0" align="start">
                      <Calendar mode="single" />
                    </PopoverContent>
                  </Popover>
                </div>

                <div className="space-y-2">
                  <Label>End Date</Label>
                  <Popover>
                    <PopoverTrigger asChild>
                      <Button variant="outline" className="w-full justify-start">
                        <CalendarIcon className="mr-2 h-4 w-4" />
                        Dec 31, 2023
                      </Button>
                    </PopoverTrigger>
                    <PopoverContent className="w-auto p-0" align="start">
                      <Calendar mode="single" />
                    </PopoverContent>
                  </Popover>
                </div>
              </div>

              <div className="space-y-2">
                <Label htmlFor="initial-capital">Initial Capital ($)</Label>
                <Input id="initial-capital" type="number" placeholder="100000" />
              </div>

              <div className="space-y-2">
                <Label htmlFor="commission">Commission (%)</Label>
                <Input id="commission" type="number" step="0.01" placeholder="0.1" />
              </div>

              <div className="space-y-2">
                <Label htmlFor="slippage">Slippage (%)</Label>
                <Input id="slippage" type="number" step="0.01" placeholder="0.05" />
              </div>

              <div className="space-y-2">
                <Label htmlFor="data-source">Data Source</Label>
                <Select>
                  <SelectTrigger>
                    <SelectValue placeholder="Select data provider" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="yahoo">Yahoo Finance</SelectItem>
                    <SelectItem value="alpha-vantage">Alpha Vantage</SelectItem>
                    <SelectItem value="quandl">Quandl</SelectItem>
                    <SelectItem value="custom">Custom Data</SelectItem>
                  </SelectContent>
                </Select>
              </div>
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
                  {isRunning ? "~2 minutes" : "Not running"}
                </p>
              </div>
            </CardContent>
          </Card>

          <Card className="border-border/50 bg-card/50 backdrop-blur-sm">
            <CardHeader>
              <CardTitle className="text-primary">Quick Stats</CardTitle>
            </CardHeader>
            <CardContent className="space-y-3">
              <div className="flex justify-between">
                <span className="text-sm text-muted-foreground">Trades Processed</span>
                <span className="text-sm text-primary">127 / 284</span>
              </div>
              <div className="flex justify-between">
                <span className="text-sm text-muted-foreground">Current Return</span>
                <span className="text-sm text-primary font-medium">+12.4%</span>
              </div>
              <div className="flex justify-between">
                <span className="text-sm text-muted-foreground">Max Drawdown</span>
                <span className="text-sm text-destructive">-8.2%</span>
              </div>
              <div className="flex justify-between">
                <span className="text-sm text-muted-foreground">Sharpe Ratio</span>
                <span className="text-sm text-primary">1.34</span>
              </div>
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  );
}