# Copyright (c) 2025 [Your Firm Name]. All rights reserved.
#
# StorageInterface: Provides an API for accessing historical market data.

import pandas as pd

class StorageInterface:
    def __init__(self, data_path):
        self.data_path = data_path
        self.data = pd.read_csv(self.data_path, index_col='timestamp', parse_dates=True)

    def get_market_data_stream(self):
        """Yields market data ticks one by one."""
        for timestamp, row in self.data.iterrows():
            yield timestamp, row

