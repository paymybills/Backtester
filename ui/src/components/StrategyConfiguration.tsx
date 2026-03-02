import { Card, CardContent, CardHeader, CardTitle } from "./ui/card";
import { Input } from "./ui/input";
import { Label } from "./ui/label";
import { Textarea } from "./ui/textarea";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "./ui/select";
import { Button } from "./ui/button";
import { Badge } from "./ui/badge";
import { Slider } from "./ui/slider";
import { useState, useEffect } from "react";
import { useToast } from "./ui/use-toast";
import { apiClient } from "../lib/api";
import { TrendingUp, Activity, BarChart3, Layers, Sparkles, Save, CheckCircle } from "lucide-react";

interface StrategyFormData {
  name: string;
  description: string;
  asset_class: string;
  timeframe: string;
  entry_signal: string;
  exit_signal: string;
  stop_loss?: number;
  take_profit?: number;
  position_size: number;
  custom_code?: string;
  parameters: Record<string, any>;
}

const STRATEGY_TYPES = [
  {
    value: "ma-crossover",
    label: "Moving Average Crossover",
    icon: TrendingUp,
    description: "Buy when short MA crosses above long MA",
    color: "from-violet-500/20 to-purple-500/20",
    borderColor: "border-violet-500/30",
    params: [
      { key: "short_window", label: "Short Window", type: "number", default: 10, min: 2, max: 100 },
      { key: "long_window", label: "Long Window", type: "number", default: 30, min: 5, max: 500 },
    ],
  },
  {
    value: "rsi",
    label: "RSI Strategy",
    icon: Activity,
    description: "Buy oversold, sell overbought via RSI",
    color: "from-cyan-500/20 to-blue-500/20",
    borderColor: "border-cyan-500/30",
    params: [
      { key: "period", label: "RSI Period", type: "number", default: 14, min: 2, max: 50 },
      { key: "oversold", label: "Oversold Threshold", type: "slider", default: 30, min: 10, max: 50 },
      { key: "overbought", label: "Overbought Threshold", type: "slider", default: 70, min: 50, max: 90 },
    ],
  },
  {
    value: "macd",
    label: "MACD Strategy",
    icon: BarChart3,
    description: "MACD line vs signal line crossover",
    color: "from-emerald-500/20 to-green-500/20",
    borderColor: "border-emerald-500/30",
    params: [
      { key: "fast_period", label: "Fast EMA Period", type: "number", default: 12, min: 2, max: 50 },
      { key: "slow_period", label: "Slow EMA Period", type: "number", default: 26, min: 5, max: 100 },
      { key: "signal_period", label: "Signal Period", type: "number", default: 9, min: 2, max: 50 },
    ],
  },
  {
    value: "bollinger-bands",
    label: "Bollinger Bands",
    icon: Layers,
    description: "Trade when price hits the bands",
    color: "from-amber-500/20 to-orange-500/20",
    borderColor: "border-amber-500/30",
    params: [
      { key: "period", label: "Period", type: "number", default: 20, min: 5, max: 100 },
      { key: "num_std", label: "Std Dev Multiplier", type: "slider", default: 2.0, min: 0.5, max: 4.0, step: 0.1 },
    ],
  },
  {
    value: "ensemble",
    label: "Ensemble Multi-Factor ✨",
    icon: Sparkles,
    description: "Combines SMA + RSI + MACD + BBands voting",
    color: "from-pink-500/20 to-rose-500/20",
    borderColor: "border-pink-500/30",
    params: [
      { key: "buy_threshold", label: "Buy Confidence Threshold", type: "slider", default: 0.6, min: 0.1, max: 1.0, step: 0.05 },
      { key: "sell_threshold", label: "Sell Confidence Threshold", type: "slider", default: -0.6, min: -1.0, max: -0.1, step: 0.05 },
    ],
  },
];

export function StrategyConfiguration() {
  const { toast } = useToast();
  const [formData, setFormData] = useState<StrategyFormData>({
    name: "",
    description: "",
    asset_class: "",
    timeframe: "",
    entry_signal: "",
    exit_signal: "",
    stop_loss: undefined,
    take_profit: undefined,
    position_size: 10.0,
    custom_code: "",
    parameters: {},
  });

  const [isLoading, setIsLoading] = useState(false);
  const [savedStrategies, setSavedStrategies] = useState<any[]>([]);

  useEffect(() => {
    loadStrategies().catch(console.error);
  }, []);

  const loadStrategies = async () => {
    try {
      const data = await apiClient.get<any[]>('/strategies');
      setSavedStrategies(data);
    } catch (error) {
      console.error('Failed to load strategies:', error);
    }
  };

  const selectedStrategyType = STRATEGY_TYPES.find(s => s.value === formData.entry_signal);

  const handleStrategyTypeSelect = (value: string) => {
    const strategyType = STRATEGY_TYPES.find(s => s.value === value);
    if (!strategyType) return;

    const defaultParams: Record<string, any> = {};
    strategyType.params.forEach(p => {
      defaultParams[p.key] = p.default;
    });

    setFormData(prev => ({
      ...prev,
      entry_signal: value,
      parameters: defaultParams,
      name: prev.name || strategyType.label,
    }));
  };

  const updateParam = (key: string, value: number) => {
    setFormData(prev => ({
      ...prev,
      parameters: { ...prev.parameters, [key]: value },
    }));
  };

  const saveStrategy = async () => {
    if (!formData.name.trim()) {
      toast({ title: "Error", description: "Strategy name is required", variant: "destructive" });
      return;
    }
    if (!formData.entry_signal) {
      toast({ title: "Error", description: "Please select a strategy type", variant: "destructive" });
      return;
    }

    setIsLoading(true);
    try {
      await apiClient.post('/strategies', formData);
      toast({ title: "Strategy Saved", description: `"${formData.name}" saved successfully` });
      await loadStrategies();
      setFormData({
        name: "", description: "", asset_class: "", timeframe: "",
        entry_signal: "", exit_signal: "", stop_loss: undefined,
        take_profit: undefined, position_size: 10.0, custom_code: "", parameters: {},
      });
    } catch (error: any) {
      toast({ title: "Save Failed", description: error.message || "Failed to save strategy", variant: "destructive" });
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="space-y-6">
      {/* Page Header */}
      <div>
        <h1 className="text-2xl font-semibold tracking-tight">Strategy Configuration</h1>
        <p className="text-muted-foreground">Choose a strategy type and tune its parameters</p>
      </div>

      {/* Saved Strategies */}
      {savedStrategies.length > 0 && (
        <Card className="border-border/50 bg-card/50 backdrop-blur-sm">
          <CardHeader className="pb-3">
            <CardTitle className="text-sm font-medium text-muted-foreground">
              Saved Strategies ({savedStrategies.length})
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="flex flex-wrap gap-2">
              {savedStrategies.map((s) => (
                <Badge key={s.id} variant="outline" className="px-3 py-1.5 text-xs border-primary/30 bg-primary/5 hover:bg-primary/10 transition-colors cursor-default">
                  {s.name}
                </Badge>
              ))}
            </div>
          </CardContent>
        </Card>
      )}

      {/* Strategy Type Selector - Visual Cards */}
      <div>
        <Label className="text-sm font-medium text-muted-foreground mb-3 block">Select Strategy Type</Label>
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-5 gap-3">
          {STRATEGY_TYPES.map((strategy) => {
            const Icon = strategy.icon;
            const isSelected = formData.entry_signal === strategy.value;
            return (
              <button
                key={strategy.value}
                onClick={() => handleStrategyTypeSelect(strategy.value)}
                className={`group relative p-4 rounded-xl border text-left transition-all duration-300 hover:scale-[1.02] ${isSelected
                  ? `bg-gradient-to-br ${strategy.color} ${strategy.borderColor} border-2 shadow-lg`
                  : "bg-card/30 border-border/40 hover:border-border/80 hover:bg-card/60"
                  }`}
              >
                {isSelected && (
                  <div className="absolute top-2 right-2">
                    <CheckCircle className="h-4 w-4 text-primary" />
                  </div>
                )}
                <Icon className={`h-6 w-6 mb-2 ${isSelected ? "text-primary" : "text-muted-foreground group-hover:text-foreground"} transition-colors`} />
                <h3 className={`text-sm font-semibold mb-1 ${isSelected ? "text-foreground" : "text-muted-foreground group-hover:text-foreground"} transition-colors`}>
                  {strategy.label}
                </h3>
                <p className="text-xs text-muted-foreground leading-snug">{strategy.description}</p>
              </button>
            );
          })}
        </div>
      </div>

      {/* Dynamic Parameter Panel */}
      {selectedStrategyType && (
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {/* Parameters */}
          <Card className={`border-2 ${selectedStrategyType.borderColor} bg-gradient-to-br ${selectedStrategyType.color} backdrop-blur-sm transition-all duration-500`}>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <selectedStrategyType.icon className="h-5 w-5 text-primary" />
                {selectedStrategyType.label} Parameters
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-5">
              {selectedStrategyType.params.map((param) => (
                <div key={param.key} className="space-y-2">
                  <div className="flex justify-between items-center">
                    <Label className="text-sm">{param.label}</Label>
                    <span className="text-sm font-mono text-primary font-semibold">
                      {formData.parameters[param.key] ?? param.default}
                    </span>
                  </div>
                  {param.type === "slider" ? (
                    <Slider
                      value={[formData.parameters[param.key] ?? param.default]}
                      onValueChange={([val]) => updateParam(param.key, val)}
                      min={param.min}
                      max={param.max}
                      step={param.step || 1}
                      className="py-1"
                    />
                  ) : (
                    <Input
                      type="number"
                      value={formData.parameters[param.key] ?? param.default}
                      onChange={(e) => updateParam(param.key, parseFloat(e.target.value) || param.default)}
                      min={param.min}
                      max={param.max}
                      className="bg-background/50"
                    />
                  )}
                  <p className="text-xs text-muted-foreground">
                    Range: {param.min} – {param.max}
                  </p>
                </div>
              ))}
            </CardContent>
          </Card>

          {/* Strategy Info & Save */}
          <Card className="border-border/50 bg-card/50 backdrop-blur-sm">
            <CardHeader>
              <CardTitle className="text-primary">Strategy Details</CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="space-y-2">
                <Label htmlFor="strategy-name">Strategy Name</Label>
                <Input
                  id="strategy-name"
                  placeholder="e.g., Aggressive RSI v2"
                  value={formData.name}
                  onChange={(e) => setFormData(prev => ({ ...prev, name: e.target.value }))}
                  className="bg-background/50"
                />
              </div>

              <div className="space-y-2">
                <Label htmlFor="description">Description</Label>
                <Textarea
                  id="description"
                  placeholder="Brief description of your strategy..."
                  className="h-20 bg-background/50"
                  value={formData.description}
                  onChange={(e) => setFormData(prev => ({ ...prev, description: e.target.value }))}
                />
              </div>

              <div className="space-y-2">
                <Label>Asset Class</Label>
                <Select value={formData.asset_class} onValueChange={(v) => setFormData(prev => ({ ...prev, asset_class: v }))}>
                  <SelectTrigger className="bg-background/50"><SelectValue placeholder="Select asset class" /></SelectTrigger>
                  <SelectContent>
                    <SelectItem value="stocks">Stocks</SelectItem>
                    <SelectItem value="forex">Forex</SelectItem>
                    <SelectItem value="crypto">Cryptocurrency</SelectItem>
                    <SelectItem value="commodities">Commodities</SelectItem>
                  </SelectContent>
                </Select>
              </div>

              <div className="grid grid-cols-2 gap-4">
                <div className="space-y-2">
                  <Label>Stop Loss (%)</Label>
                  <Input
                    type="number" placeholder="5.0"
                    value={formData.stop_loss || ""}
                    onChange={(e) => setFormData(prev => ({ ...prev, stop_loss: parseFloat(e.target.value) || undefined }))}
                    className="bg-background/50"
                  />
                </div>
                <div className="space-y-2">
                  <Label>Take Profit (%)</Label>
                  <Input
                    type="number" placeholder="10.0"
                    value={formData.take_profit || ""}
                    onChange={(e) => setFormData(prev => ({ ...prev, take_profit: parseFloat(e.target.value) || undefined }))}
                    className="bg-background/50"
                  />
                </div>
              </div>

              <Button
                className="w-full mt-4 bg-primary hover:bg-primary/90 text-primary-foreground font-semibold"
                onClick={saveStrategy}
                disabled={isLoading}
              >
                <Save className="mr-2 h-4 w-4" />
                {isLoading ? "Saving..." : "Save Strategy"}
              </Button>
            </CardContent>
          </Card>
        </div>
      )}
    </div>
  );
}