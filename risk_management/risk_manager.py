
class RiskManager:
    def __init__(self, config):
        self.config = config

    def check_risk(self, portfolio, trade):
        # Check max position size
        if 'max_position_size' in self.config:
            current_size = portfolio.positions.get(trade['symbol'], 0)
            if current_size + trade['quantity'] > self.config['max_position_size']:
                print(f"Risk check failed: max position size exceeded for {trade['symbol']}")
                return False

        # Check stop loss
        if 'stop_loss' in self.config:
            # This is a simple implementation. A more robust implementation would track the entry price of the position.
            pass

        return True
