import { Card, CardContent, CardHeader, CardTitle } from "./ui/card";
import { Input } from "./ui/input";
import { Label } from "./ui/label";
import { Textarea } from "./ui/textarea";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "./ui/select";
import { Button } from "./ui/button";
import { Separator } from "./ui/separator";

export function StrategyConfiguration() {
  return (
    <div className="space-y-6">
      {/* Page Header */}
      <div>
        <h1>Strategy Configuration</h1>
        <p className="text-muted-foreground">Define your trading strategy parameters</p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Basic Information */}
        <Card className="border-border/50 bg-card/50 backdrop-blur-sm">
          <CardHeader>
            <CardTitle className="text-primary">Basic Information</CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="space-y-2">
              <Label htmlFor="strategy-name">Strategy Name</Label>
              <Input id="strategy-name" placeholder="e.g., Mean Reversion v2" />
            </div>
            
            <div className="space-y-2">
              <Label htmlFor="description">Description</Label>
              <Textarea 
                id="description" 
                placeholder="Brief description of your strategy..."
                className="h-24"
              />
            </div>

            <div className="space-y-2">
              <Label htmlFor="asset-class">Asset Class</Label>
              <Select>
                <SelectTrigger>
                  <SelectValue placeholder="Select asset class" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="stocks">Stocks</SelectItem>
                  <SelectItem value="forex">Forex</SelectItem>
                  <SelectItem value="crypto">Cryptocurrency</SelectItem>
                  <SelectItem value="commodities">Commodities</SelectItem>
                </SelectContent>
              </Select>
            </div>

            <div className="space-y-2">
              <Label htmlFor="timeframe">Timeframe</Label>
              <Select>
                <SelectTrigger>
                  <SelectValue placeholder="Select timeframe" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="1m">1 Minute</SelectItem>
                  <SelectItem value="5m">5 Minutes</SelectItem>
                  <SelectItem value="1h">1 Hour</SelectItem>
                  <SelectItem value="1d">1 Day</SelectItem>
                  <SelectItem value="1w">1 Week</SelectItem>
                </SelectContent>
              </Select>
            </div>
          </CardContent>
        </Card>

        {/* Technical Parameters */}
        <Card className="border-border/50 bg-card/50 backdrop-blur-sm">
          <CardHeader>
            <CardTitle className="text-primary">Technical Parameters</CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="space-y-2">
              <Label htmlFor="entry-signal">Entry Signal</Label>
              <Select>
                <SelectTrigger>
                  <SelectValue placeholder="Select entry condition" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="rsi-oversold">RSI Oversold</SelectItem>
                  <SelectItem value="ma-crossover">MA Crossover</SelectItem>
                  <SelectItem value="bollinger-bands">Bollinger Bands</SelectItem>
                  <SelectItem value="macd-signal">MACD Signal</SelectItem>
                </SelectContent>
              </Select>
            </div>

            <div className="space-y-2">
              <Label htmlFor="exit-signal">Exit Signal</Label>
              <Select>
                <SelectTrigger>
                  <SelectValue placeholder="Select exit condition" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="rsi-overbought">RSI Overbought</SelectItem>
                  <SelectItem value="stop-loss">Stop Loss</SelectItem>
                  <SelectItem value="take-profit">Take Profit</SelectItem>
                  <SelectItem value="time-based">Time Based</SelectItem>
                </SelectContent>
              </Select>
            </div>

            <div className="grid grid-cols-2 gap-4">
              <div className="space-y-2">
                <Label htmlFor="stop-loss">Stop Loss (%)</Label>
                <Input id="stop-loss" type="number" placeholder="5.0" />
              </div>
              <div className="space-y-2">
                <Label htmlFor="take-profit">Take Profit (%)</Label>
                <Input id="take-profit" type="number" placeholder="10.0" />
              </div>
            </div>

            <div className="space-y-2">
              <Label htmlFor="position-size">Position Size (%)</Label>
              <Input id="position-size" type="number" placeholder="10.0" />
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Strategy Logic */}
      <Card className="border-border/50 bg-card/50 backdrop-blur-sm">
        <CardHeader>
          <CardTitle className="text-primary">Strategy Logic (Python Code)</CardTitle>
        </CardHeader>
        <CardContent>
          <Textarea 
            placeholder={`def strategy_logic(data):
    # Your strategy implementation here
    # Example:
    rsi = calculate_rsi(data['close'], 14)
    
    # Entry condition
    if rsi < 30:
        return 'BUY'
    
    # Exit condition  
    elif rsi > 70:
        return 'SELL'
    
    return 'HOLD'`}
            className="h-48 font-mono text-sm"
          />
        </CardContent>
      </Card>

      {/* Action Buttons */}
      <div className="flex justify-end space-x-4">
        <Button variant="outline" className="border-border hover:bg-muted">Save Draft</Button>
        <Button variant="outline" className="border-primary/30 text-primary hover:bg-primary/10">Validate Strategy</Button>
        <Button className="bg-primary hover:bg-primary/90 text-primary-foreground">Save Strategy</Button>
      </div>
    </div>
  );
}