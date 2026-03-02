import { Card, CardContent, CardHeader, CardTitle } from "./ui/card";
import { Input } from "./ui/input";
import { Label } from "./ui/label";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "./ui/select";
import { Button } from "./ui/button";
import { Progress } from "./ui/progress";
import { Badge } from "./ui/badge";
import { Play, Sparkles, AlertCircle } from "lucide-react";
import { useState, useEffect, useMemo } from "react";
import { apiClient } from "../lib/api";
import { useToast } from "./ui/use-toast";

const STRATEGY_OPTS = {
    "ma-crossover": { label: "MA Crossover", params: ["short_window", "long_window"] },
    "rsi": { label: "RSI Strategy", params: ["period", "oversold", "overbought"] },
    "macd": { label: "MACD Strategy", params: ["fast_period", "slow_period", "signal_period"] },
    "bollinger-bands": { label: "Bollinger Bands", params: ["period", "num_std"] },
};

export function OptimizerScreen() {
    const { toast } = useToast();

    const [strategyType, setStrategyType] = useState("ma-crossover");
    const [startDate, setStartDate] = useState("2023-01-01");
    const [endDate, setEndDate] = useState("2023-12-31");
    const [initialCapital, setInitialCapital] = useState("100000");
    const [ticker, setTicker] = useState("AAPL");

    // Param grids
    const [param1, setParam1] = useState("short_window");
    const [param1Values, setParam1Values] = useState("10, 20, 30");
    const [param2, setParam2] = useState("long_window");
    const [param2Values, setParam2Values] = useState("50, 100, 200");

    const [isRunning, setIsRunning] = useState(false);
    const [optId, setOptId] = useState<string | null>(null);
    const [progress, setProgress] = useState(0);
    const [currentStep, setCurrentStep] = useState("");
    const [results, setResults] = useState<any[]>([]);

    // Cleanup on unmount
    useEffect(() => {
        let interval: any;
        if (isRunning && optId) {
            interval = setInterval(async () => {
                try {
                    const status = await apiClient.getOptimizationStatus(optId);
                    setProgress(status.progress);
                    setCurrentStep(status.current_step);

                    if (status.status === "completed") {
                        setIsRunning(false);
                        setResults(status.results || []);
                        toast({ title: "Optimization Complete!" });
                    } else if (status.status === "failed") {
                        setIsRunning(false);
                        toast({ title: "Optimization Failed", description: status.current_step, variant: "destructive" });
                    }
                } catch (e) {
                    console.error(e);
                }
            }, 1000);
        }
        return () => clearInterval(interval);
    }, [isRunning, optId]);

    const handleStart = async () => {
        // Parse params
        const p1 = param1Values.split(",").map(v => Number(v.trim())).filter(v => !isNaN(v));
        const p2 = param2Values.split(",").map(v => Number(v.trim())).filter(v => !isNaN(v));

        if (p1.length === 0 || p2.length === 0) {
            toast({ title: "Invalid Parameters", description: "Provide comma separated numbers", variant: "destructive" });
            return;
        }

        try {
            setIsRunning(true);
            setProgress(0);
            setResults([]);

            const config = {
                strategy_type: strategyType,
                param_grid: {
                    [param1]: p1,
                    [param2]: p2
                },
                data_source: "yahoo",
                ticker: ticker,
                start_date: startDate,
                end_date: endDate,
                timeframe: "1d",
                initial_capital: Number(initialCapital)
            };

            const res = await apiClient.startOptimization(config);
            setOptId(res.optimization_id);
            setCurrentStep("Initializing optimizer...");
        } catch (e: any) {
            toast({ title: "Error starting optimizer", description: e.message, variant: "destructive" });
            setIsRunning(false);
        }
    };

    // Build heatmap matrix
    const heatmapData = useMemo(() => {
        if (!results.length) return null;

        // Extract unique values for axes
        const xValues = Array.from(new Set(results.map(r => r[param1]))).sort((a, b) => Number(a) - Number(b));
        const yValues = Array.from(new Set(results.map(r => r[param2]))).sort((a, b) => Number(a) - Number(b));

        // Find min and max for color scaling (using Sharpe Ratio)
        const sharpes = results.map(r => r.sharpe_ratio);
        const maxSharpe = Math.max(...sharpes);
        const minSharpe = Math.min(...sharpes);

        const matrix = yValues.map(y => {
            return xValues.map(x => {
                const row = results.find(r => r[param1] === x && r[param2] === y);
                return row || null;
            });
        });

        return { xValues, yValues, matrix, minSharpe, maxSharpe };
    }, [results, param1, param2]);

    // Color interpolator from red (bad) to green/emerald (good)
    const getColor = (val: number, min: number, max: number) => {
        if (max === min) return `rgba(16, 185, 129, 0.5)`;
        const ratio = (val - min) / (max - min);
        // 0 = red (rose-500), 1 = green (emerald-500)
        // Using HSL: red is 346, emerald is 160
        const hue = 346 + ratio * (160 - 346 > 0 ? 160 - 346 : 360 + 160 - 346);
        const finalHue = hue % 360;
        return `hsla(${finalHue}, 80%, 50%, 0.7)`;
    };

    return (
        <div className="space-y-6">
            <div>
                <h1 className="text-2xl font-semibold tracking-tight">Strategy Optimizer</h1>
                <p className="text-muted-foreground flex items-center gap-2">
                    <Sparkles className="h-4 w-4 text-violet-400" />
                    Find the mathematical sweet spot for your indicator parameters
                </p>
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
                {/* Settings Panel */}
                <div className="lg:col-span-1 space-y-6">
                    <Card className="border-border/50 bg-card/50 backdrop-blur-sm shadow-xl shadow-black/5">
                        <CardHeader>
                            <CardTitle className="text-primary text-lg">Sweep Configuration</CardTitle>
                        </CardHeader>
                        <CardContent className="space-y-4">
                            <div className="space-y-2">
                                <Label>Strategy</Label>
                                <Select value={strategyType} onValueChange={v => {
                                    setStrategyType(v);
                                    const p = (STRATEGY_OPTS as any)[v].params;
                                    setParam1(p[0]); setParam2(p[1]);
                                }}>
                                    <SelectTrigger><SelectValue /></SelectTrigger>
                                    <SelectContent>
                                        {Object.entries(STRATEGY_OPTS).map(([k, v]) => (
                                            <SelectItem key={k} value={k}>{v.label}</SelectItem>
                                        ))}
                                    </SelectContent>
                                </Select>
                            </div>

                            <div className="grid grid-cols-2 gap-4">
                                <div className="space-y-2"><Label>Ticker</Label><Input value={ticker} onChange={e => setTicker(e.target.value.toUpperCase())} /></div>
                                <div className="space-y-2"><Label>Capital</Label><Input type="number" value={initialCapital} onChange={e => setInitialCapital(e.target.value)} /></div>
                            </div>
                            <div className="grid grid-cols-2 gap-4">
                                <div className="space-y-2"><Label>Start Date</Label><Input type="date" value={startDate} onChange={e => setStartDate(e.target.value)} /></div>
                                <div className="space-y-2"><Label>End Date</Label><Input type="date" value={endDate} onChange={e => setEndDate(e.target.value)} /></div>
                            </div>

                            <div className="pt-4 border-t border-border/50">
                                <h4 className="text-sm font-medium mb-3">Parameter Grid</h4>
                                <div className="space-y-4">
                                    <div className="space-y-2">
                                        <Label>X-Axis: {(STRATEGY_OPTS as any)[strategyType]?.params[0]}</Label>
                                        <Input placeholder="10, 20, 30" value={param1Values} onChange={e => setParam1Values(e.target.value)} />
                                    </div>
                                    <div className="space-y-2">
                                        <Label>Y-Axis: {(STRATEGY_OPTS as any)[strategyType]?.params[1]}</Label>
                                        <Input placeholder="50, 100, 200" value={param2Values} onChange={e => setParam2Values(e.target.value)} />
                                    </div>
                                </div>
                            </div>

                            <Button onClick={handleStart} disabled={isRunning} className="w-full bg-gradient-to-r from-violet-600 to-cyan-600 hover:from-violet-500 hover:to-cyan-500 text-white border-0">
                                <Play className="mr-2 h-4 w-4" /> {isRunning ? "Optimizing..." : "Start Sweep"}
                            </Button>

                            {isRunning && (
                                <div className="space-y-2 pt-4">
                                    <div className="flex justify-between text-xs">
                                        <span>{currentStep}</span>
                                        <span>{progress}%</span>
                                    </div>
                                    <Progress value={progress} className="h-2" />
                                </div>
                            )}
                        </CardContent>
                    </Card>
                </div>

                {/* Heatmap Panel */}
                <div className="lg:col-span-2 space-y-6">
                    <Card className="border-border/50 bg-card/50 backdrop-blur-sm min-h-[500px] shadow-xl shadow-black/5 flex flex-col">
                        <CardHeader className="border-b border-border/30">
                            <CardTitle className="flex items-center justify-between">
                                <span>Performance Heatmap (Sharpe Ratio)</span>
                                {results.length > 0 && <Badge variant="outline" className="bg-emerald-500/10 text-emerald-400 border-emerald-500/20">Optimal Found</Badge>}
                            </CardTitle>
                        </CardHeader>
                        <CardContent className="flex-1 flex flex-col items-center justify-center p-6 relative">

                            {!heatmapData ? (
                                <div className="text-center text-muted-foreground flex flex-col items-center gap-3">
                                    <AlertCircle className="h-10 w-10 opacity-20" />
                                    <p>Run an optimization sweep to generate the heatmap.</p>
                                </div>
                            ) : (
                                <div className="w-full overflow-auto">
                                    <div className="flex">
                                        {/* Y-Axis labels */}
                                        <div className="flex flex-col justify-end pr-4 text-xs text-muted-foreground font-mono gap-1 mt-6">
                                            <div className="font-semibold text-foreground mb-2 text-right -rotate-90 origin-right translate-y-[-20px] translate-x-[-10px] whitespace-nowrap">{param2}</div>
                                            {heatmapData.yValues.map(y => (
                                                <div key={y} className="h-12 w-8 flex items-center justify-end">{y}</div>
                                            ))}
                                        </div>

                                        {/* Grid */}
                                        <div>
                                            {/* X-Axis labels */}
                                            <div className="flex gap-1 mb-2 ml-[2px]">
                                                <div className="font-semibold text-xs text-foreground absolute top-4 left-1/2 -translate-x-1/2">{param1}</div>
                                                {heatmapData.xValues.map(x => (
                                                    <div key={x} className="w-16 text-center text-xs text-muted-foreground font-mono">{x}</div>
                                                ))}
                                            </div>

                                            {/* Cells */}
                                            <div className="flex flex-col gap-1">
                                                {heatmapData.matrix.map((row, i) => (
                                                    <div key={i} className="flex gap-1">
                                                        {row.map((cell, j) => {
                                                            if (!cell) return <div key={j} className="w-16 h-12 bg-muted/20 rounded-md"></div>;
                                                            const isBest = cell.sharpe_ratio === heatmapData.maxSharpe;
                                                            return (
                                                                <div
                                                                    key={j}
                                                                    className={`w-16 h-12 rounded-md flex flex-col items-center justify-center text-[10px] transition-transform hover:scale-110 cursor-crosshair relative group ${isBest ? 'ring-2 ring-white z-10' : ''}`}
                                                                    style={{ backgroundColor: getColor(cell.sharpe_ratio, heatmapData.minSharpe, heatmapData.maxSharpe) }}
                                                                >
                                                                    <span className="font-bold text-white drop-shadow-md">{cell.sharpe_ratio.toFixed(2)}</span>
                                                                    {isBest && <span className="absolute -top-1 -right-1 flex h-3 w-3"><span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-white opacity-75"></span><span className="relative inline-flex rounded-full h-3 w-3 bg-white"></span></span>}

                                                                    {/* Tooltip on hover */}
                                                                    <div className="absolute opacity-0 group-hover:opacity-100 transition-opacity bg-black/90 backdrop-blur-md text-white p-2 text-xs rounded shadow-xl -top-14 left-1/2 -translate-x-1/2 pointer-events-none z-50 w-32 hidden group-hover:block">
                                                                        <div className="font-bold mb-1 border-b border-white/20 pb-1">S: {cell.sharpe_ratio.toFixed(2)}</div>
                                                                        <div>Return: {(cell.total_return * 100).toFixed(1)}%</div>
                                                                        <div>Win: {(cell.win_rate * 100).toFixed(0)}%</div>
                                                                    </div>
                                                                </div>
                                                            );
                                                        })}
                                                    </div>
                                                ))}
                                            </div>
                                        </div>
                                    </div>

                                    {/* Legend */}
                                    <div className="mt-8 flex items-center justify-center gap-4 text-xs text-muted-foreground">
                                        <span>Lower Sharpe</span>
                                        <div className="w-48 h-2 rounded-full bg-gradient-to-r from-rose-500 via-yellow-500 to-emerald-500"></div>
                                        <span>Higher Sharpe</span>
                                    </div>
                                </div>
                            )}
                        </CardContent>
                    </Card>

                    {results.length > 0 && heatmapData && (
                        <Card className="border-border/50 bg-card/50 backdrop-blur-sm shadow-xl shadow-black/5">
                            <CardHeader className="py-4">
                                <CardTitle className="text-sm">Best Combination Discovered</CardTitle>
                            </CardHeader>
                            <CardContent className="pb-4">
                                {(() => {
                                    const best = results.find(r => r.sharpe_ratio === heatmapData.maxSharpe) || results[0];
                                    return (
                                        <div className="grid grid-cols-4 gap-4 text-sm">
                                            <div className="bg-background/40 p-3 rounded-lg border border-border/50">
                                                <p className="text-muted-foreground text-xs mb-1 uppercase">Parameters</p>
                                                <p className="font-mono font-semibold">{param1}: {Math.round(best[param1])} <br /> {param2}: {Math.round(best[param2])}</p>
                                            </div>
                                            <div className="bg-background/40 p-3 rounded-lg border border-border/50">
                                                <p className="text-muted-foreground text-xs mb-1 uppercase">Sharpe Ratio</p>
                                                <p className="font-bold text-emerald-400">{best.sharpe_ratio.toFixed(2)}</p>
                                            </div>
                                            <div className="bg-background/40 p-3 rounded-lg border border-border/50">
                                                <p className="text-muted-foreground text-xs mb-1 uppercase">Total Return</p>
                                                <p className="font-bold text-emerald-400">{(best.total_return * 100).toFixed(1)}%</p>
                                            </div>
                                            <div className="bg-background/40 p-3 rounded-lg border border-border/50">
                                                <p className="text-muted-foreground text-xs mb-1 uppercase">Win Rate</p>
                                                <p className="font-bold text-cyan-400">{(best.win_rate * 100).toFixed(1)}%</p>
                                            </div>
                                        </div>
                                    );
                                })()}
                            </CardContent>
                        </Card>
                    )}
                </div>
            </div>
        </div>
    );
}
