
import numpy as np

class AnalyticsEngine:
    def __init__(self, portfolio):
        self.portfolio = portfolio

    def calculate_metrics(self):
        pnl = self.portfolio.cash - 100000.0
        equity_curve = [e['equity'] for e in self.portfolio.equity_curve]
        returns = np.diff(equity_curve) / equity_curve[:-1]
        sharpe_ratio = np.mean(returns) / np.std(returns) * np.sqrt(252)  # Assuming daily data
        max_drawdown = self.calculate_max_drawdown(equity_curve)

        return {
            'pnl': pnl,
            'sharpe_ratio': sharpe_ratio,
            'max_drawdown': max_drawdown
        }

    def calculate_max_drawdown(self, equity_curve):
        peak = equity_curve[0]
        max_drawdown = 0
        for equity in equity_curve:
            if equity > peak:
                peak = equity
            drawdown = (peak - equity) / peak
            if drawdown > max_drawdown:
                max_drawdown = drawdown
        return max_drawdown
