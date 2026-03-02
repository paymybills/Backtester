// Environment-aware API client
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

// Mock data for demo deployment
const MOCK_DATA = {
  dashboardStats: {
    total_strategies: 12,
    active_backtests: 3,
    avg_sharpe_ratio: 1.42,
    best_strategy_roi: 23.4
  },
  recentBacktests: [
    {
      id: "BT-001",
      strategy: "Mean Reversion v2",
      status: "Completed",
      duration: "2h 15m",
      sharpe: "1.34",
      roi: "18.2%",
      created_at: "2024-01-15T10:30:00Z"
    },
    {
      id: "BT-002",
      strategy: "Momentum Strategy", 
      status: "Running",
      duration: "45m",
      sharpe: "-",
      roi: "-",
      created_at: "2024-01-15T14:20:00Z"
    }
  ]
};

class ApiClient {
  private async request<T>(endpoint: string, options: RequestInit = {}): Promise<T> {
    const url = `${API_BASE_URL}${endpoint}`;
    
    try {
      const response = await fetch(url, {
        headers: {
          'Content-Type': 'application/json',
          ...options.headers,
        },
        ...options,
      });

      if (!response.ok) {
        throw new Error(`API request failed: ${response.statusText}`);
      }

      return response.json();
    } catch (error) {
      // Fallback to mock data in demo mode
      console.warn('API request failed, using mock data:', error);
      return this.getMockData(endpoint) as T;
    }
  }

  private getMockData(endpoint: string): any {
    switch (endpoint) {
      case '/dashboard/stats':
        return MOCK_DATA.dashboardStats;
      case '/dashboard/recent-backtests':
        return MOCK_DATA.recentBacktests;
      case '/strategies':
        return [
          { id: 'ma_crossover', name: 'Moving Average Crossover', type: 'Technical' },
          { id: 'rsi_strategy', name: 'RSI Strategy', type: 'Technical' }
        ];
      default:
        return {};
    }
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
}

export const apiClient = new ApiClient();