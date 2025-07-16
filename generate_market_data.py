
import pandas as pd
import numpy as np

# Configuration
NUM_POINTS = 50000
OUTPUT_FILE = "/Users/akshatdalal/Desktop/akshat/programming/Algorithmic Trading Model/nano/hft_system/05_research_environment/data_storage/market_data.csv"

# Create a base random walk for the core price movement
base_price = 100.0
base_walk = base_price + np.random.randn(NUM_POINTS).cumsum() * 0.1

# Create two correlated assets
noise_a = np.random.randn(NUM_POINTS) * 0.05
noise_b = np.random.randn(NUM_POINTS) * 0.05
price_a = base_walk + noise_a
price_b = base_walk + noise_b + 2.0 # SYMB is slightly offset

# Create bid/ask spreads
spread = 0.02
bid_a = price_a - spread / 2
ask_a = price_a + spread / 2
bid_b = price_b - spread / 2
ask_b = price_b + spread / 2

# Create timestamps
timestamps = pd.to_datetime(np.arange(NUM_POINTS), unit='s', origin=pd.Timestamp('2025-07-15 09:30:00'))

# Create two dataframes and interleave them
df_a = pd.DataFrame({
    'timestamp': timestamps,
    'symbol': 'SYMA',
    'bid': bid_a,
    'ask': ask_a
})

df_b = pd.DataFrame({
    'timestamp': timestamps,
    'symbol': 'SYMB',
    'bid': bid_b,
    'ask': ask_b
})

# Interleave the data to simulate a real market feed
final_df = pd.concat([df_a, df_b]).sort_index(kind='merge').reset_index(drop=True)

# Save to CSV
final_df.to_csv(OUTPUT_FILE, index=False)

print(f"Generated {len(final_df)} data points to {OUTPUT_FILE}")
