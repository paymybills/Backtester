// API client for the backtesting engine backend
const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api';

export interface BacktestConfig {
  strategy_name: string;
  start_date: string;
  end_date: string;
  initial_capital: number;
  commission: number;
  slippage: number;
  data_source: string;
}

export interface BacktestStatus {
  id: string;
  status: 'running' | 'completed' | 'failed' | 'paused';
  progress: number;
  current_step: string;
  estimated_time_remaining?: string;
  results?: any[];
}

export interface BacktestResults {
  backtest_id: string;
  strategy_name: string;
  metrics: {
    total_return: number;
    annualized_return: number;
    sharpe_ratio: number;
    sortino_ratio: number;
    max_drawdown: number;
    win_rate: number;
    total_trades: number;
  };
  portfolio_data: Array<{
    date: string;
    portfolio_value: number;
    daily_return: number;
    cumulative_return: number;
  }>;
  trades: Array<{
    id: string;
    date: string;
    type: string;
    price: number;
    shares: number;
    commission: number;
  }>;
  completed_at: string;
}

class ApiClient {
  private async request<T>(endpoint: string, options: RequestInit = {}): Promise<T> {
    const url = `${API_BASE_URL}${endpoint}`;

    const response = await fetch(url, {
      headers: {
        'Content-Type': 'application/json',
        ...options.headers,
      },
      ...options,
    });

    if (!response.ok) {
      let errorMessage = `API request failed: ${response.statusText}`;
      try {
        const errorData = await response.json();
        errorMessage = errorData.detail || errorData.message || errorMessage;
      } catch {
        // If response body is not JSON, use the status text
      }
      throw new Error(errorMessage);
    }

    return response.json();
  }

  async get<T>(endpoint: string): Promise<T> {
    return this.request<T>(endpoint);
  }

  async post<T>(endpoint: string, data?: any): Promise<T> {
    return this.request<T>(endpoint, {
      method: 'POST',
      body: data ? JSON.stringify(data) : undefined,
    });
  }

  // Dashboard endpoints
  async getDashboardStats() {
    return this.request('/dashboard/stats');
  }

  async getRecentBacktests() {
    return this.request('/dashboard/recent-backtests');
  }

  // Strategy endpoints
  async getStrategies() {
    return this.request('/strategies');
  }

  async createStrategy(strategy: any) {
    return this.request('/strategies', {
      method: 'POST',
      body: JSON.stringify(strategy),
    });
  }

  // Backtest endpoints
  async startBacktest(config: BacktestConfig): Promise<{ backtest_id: string }> {
    return this.request('/backtests/start', {
      method: 'POST',
      body: JSON.stringify(config),
    });
  }

  async getBacktestStatus(backtestId: string): Promise<BacktestStatus> {
    return this.request(`/backtests/${backtestId}/status`);
  }

  async getBacktestResults(backtestId: string): Promise<BacktestResults> {
    return this.request(`/backtests/${backtestId}/results`);
  }

  async pauseBacktest(backtestId: string) {
    return this.request(`/backtests/${backtestId}/pause`, {
      method: 'POST',
    });
  }

  async stopBacktest(backtestId: string) {
    return this.request(`/backtests/${backtestId}/stop`, {
      method: 'POST',
    });
  }

  async getAllBacktests() {
    return this.request('/backtests');
  }

  // Optimizer endpoints
  async startOptimization(config: any): Promise<{ optimization_id: string }> {
    return this.request('/optimize', {
      method: 'POST',
      body: JSON.stringify(config),
    });
  }

  async getOptimizationStatus(optId: string): Promise<BacktestStatus> {
    return this.request(`/optimize/${optId}`);
  }
}

export const apiClient = new ApiClient();