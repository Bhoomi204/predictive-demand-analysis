import pandas as pd
import os

def load_and_merge():
    # Get the directory where this script is located
    base_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(base_dir, '../data')
    prices = pd.read_csv(os.path.join(data_dir, 'commodity_prices.csv'), parse_dates=['date'])
    evs = pd.read_csv(os.path.join(data_dir, 'ev_production.csv'), parse_dates=['date'])
    df = pd.merge(prices, evs, on='date')
    df = df.sort_values('date')
    return df

if __name__ == "__main__":
    df = load_and_merge()
    print(df.head()) 