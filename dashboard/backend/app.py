
from flask import Flask, jsonify, render_template
import sys
from pathlib import Path
import pandas as pd
import numpy as np

# Adjust path to import our existing backtesting modules
sys.path.append(str(Path(__file__).resolve().parent.parent.parent / 'hft_system/05_research_environment'))
from backtester.main import PairTradingStrategy, Portfolio

app = Flask(__name__, template_folder='../frontend/templates', static_folder='../frontend/static')

# --- Global variable to store results ---
backtest_results = {}

@app.route('/')
def index():
    """Serves the main dashboard page."""
    return render_template('index.html')

@app.route('/api/run_backtest', methods=['POST'])
def run_backtest():
    """Runs the backtest and stores the results."""
    global backtest_results
    
    DATA_FILE = "../hft_system/05_research_environment/data_storage/market_data.csv"
    data = pd.read_csv(DATA_FILE, index_col='timestamp', parse_dates=True)

    portfolio = Portfolio()
    strategy = PairTradingStrategy(portfolio)

    for timestamp, tick in data.iterrows():
        strategy.on_market_data(timestamp, tick)

    # Store results for other API endpoints
    trades_df = pd.DataFrame(portfolio.trades)
    equity_df = pd.DataFrame(portfolio.equity_curve)

    backtest_results = {
        'final_cash': portfolio.cash,
        'total_trades': len(trades_df),
        'pnl': portfolio.cash - 100000.0,
        'trades': trades_df.to_dict(orient='records'),
        'equity_curve': {
            'timestamps': equity_df['timestamp'].dt.strftime('%Y-%m-%d %H:%M:%S').tolist(),
            'equity': equity_df['equity'].tolist()
        }
    }
    
    return jsonify({'status': 'success', 'message': 'Backtest complete.'})

@app.route('/api/get_results')
def get_results():
    """Returns the stored backtest results."""
    if not backtest_results:
        return jsonify({'error': 'No backtest results found. Please run a backtest first.'}), 404
    return jsonify(backtest_results)

if __name__ == '__main__':
    app.run(debug=True, port=5001)
