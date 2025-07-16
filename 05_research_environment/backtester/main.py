# Copyright (c) 2025 [Your Firm Name]. All rights reserved.
#
# Backtester: A high-fidelity simulator for testing trading strategies.

import sys
from pathlib import Path

# Add the project root to the Python path
sys.path.append(str(Path(__file__).resolve().parent.parent.parent))

import pandas as pd

# Ensure the data_storage module can be found
sys.path.append(str(Path(__file__).resolve().parent.parent / 'data_storage'))
from storage_interface import StorageInterface
from ...risk_management.risk_manager import RiskManager
from ...analytics.analytics_engine import AnalyticsEngine

class PairTradingStrategy:
    def __init__(self, portfolio):
        self.portfolio = portfolio
        self.prices_a = []
        self.prices_b = []
        self.spread_history = []
        self.window = 20
        self.threshold = 2.0

    def on_market_data(self, timestamp, data):
        symbol = data['symbol']
        mid_price = (data['bid'] + data['ask']) / 2.0

        if symbol == 'SYMA':
            self.prices_a.append(mid_price)
        elif symbol == 'SYMB':
            self.prices_b.append(mid_price)

        # Only proceed if we have data for both
        if len(self.prices_a) > 0 and len(self.prices_b) > 0:
            spread = self.prices_a[-1] - self.prices_b[-1]
            self.spread_history.append(spread)

            if len(self.spread_history) > self.window:
                mean_spread = np.mean(self.spread_history[-self.window:])
                std_spread = np.std(self.spread_history[-self.window:])
                z_score = (spread - mean_spread) / std_spread

                # Trading Logic
                if z_score > self.threshold and self.portfolio.positions.get('SYMA', 0) == 0:
                    # Spread is wide, sell A and buy B
                    self.portfolio.execute_trade(timestamp, 'SYMA', 'SELL', data['bid'], 100)
                    self.portfolio.execute_trade(timestamp, 'SYMB', 'BUY', data['ask'], 100)
                elif z_score < -self.threshold and self.portfolio.positions.get('SYMA', 0) == 0:
                    # Spread is narrow, buy A and sell B
                    self.portfolio.execute_trade(timestamp, 'SYMA', 'BUY', data['ask'], 100)
                    self.portfolio.execute_trade(timestamp, 'SYMB', 'SELL', data['bid'], 100)
                elif abs(z_score) < 0.5 and self.portfolio.positions.get('SYMA', 0) != 0:
                    # Close positions when spread reverts to mean
                    self.portfolio.close_all_positions(timestamp, data)


class Portfolio:
    def __init__(self, initial_cash=100000.0, risk_manager=None):
        self.cash = initial_cash
        self.positions = {}
        self.trades = []
        self.equity_curve = []
        self.risk_manager = risk_manager

    def execute_trade(self, timestamp, symbol, side, price, quantity):
        trade = {'timestamp': timestamp, 'symbol': symbol, 'side': side, 'price': price, 'quantity': quantity}
        if self.risk_manager and not self.risk_manager.check_risk(self, trade):
            return

        cost = price * quantity
        if side == 'BUY':
            if self.cash >= cost:
                self.cash -= cost
                self.positions[symbol] = self.positions.get(symbol, 0) + quantity
        elif side == 'SELL':
            # Assuming we can short sell
            self.cash += cost
            self.positions[symbol] = self.positions.get(symbol, 0) - quantity
        
        self.trades.append({'timestamp': timestamp, 'symbol': symbol, 'side': side, 'price': price, 'quantity': quantity})
        self.update_equity(timestamp)

    def close_all_positions(self, timestamp, data):
        for symbol, quantity in list(self.positions.items()):
            if quantity > 0:
                self.execute_trade(timestamp, symbol, 'SELL', data['bid'], quantity)
            elif quantity < 0:
                self.execute_trade(timestamp, symbol, 'BUY', data['ask'], abs(quantity))

    def update_equity(self, timestamp):
        current_value = self.cash
        # In a real scenario, you'd need the current price of each asset
        # For simplicity, we'll just track cash for now.
        self.equity_curve.append({'timestamp': timestamp, 'equity': current_value})


class Backtester:
    def __init__(self, storage_interface, strategy, analytics_engine):
        self.storage = storage_interface
        self.strategy = strategy
        self.analytics_engine = analytics_engine

    def run(self):
        print("Running backtest...")
        data_stream = self.storage.get_market_data_stream()
        for timestamp, data in data_stream:
            self.strategy.on_market_data(timestamp, data)
        print("Backtest complete.")
        self.print_results()

    def print_results(self):
        print("\n--- Backtest Results ---")
        portfolio = self.strategy.portfolio
        print(f"Final Cash: ${portfolio.cash:,.2f}")
        
        total_trades = len(portfolio.trades)
        print(f"Total Trades: {total_trades}")

        if total_trades > 0:
            trades_df = pd.DataFrame(portfolio.trades)
            print("\nTrades Log:")
            print(trades_df.head())

            # Simple PnL calculation
            pnl = portfolio.cash - 100000.0
            print(f"\nNet Profit/Loss: ${pnl:,.2f}")

            # Print analytics
            analytics = self.analytics_engine.calculate_metrics()
            print("\n--- Analytics ---")
            for key, value in analytics.items():
                print(f"{key}: {value}")
        else:
            print("No trades were executed.")


if __name__ == '__main__':
    import numpy as np
    DATA_FILE = "/Users/akshatdalal/Desktop/akshat/programming/Algorithmic Trading Model/nano/hft_system/05_research_environment/data_storage/market_data.csv"
    
    storage = StorageInterface(DATA_FILE)
    risk_manager = RiskManager(config={})
    portfolio = Portfolio(risk_manager=risk_manager)
    strategy = PairTradingStrategy(portfolio)
    analytics_engine = AnalyticsEngine(portfolio)
    
    backtester = Backtester(storage, strategy, analytics_engine)
    backtester.run()
