"""
Author: Nicole Wang
Date: Updated June 2025

This script analyzes the relationship between Reddit mentions and cryptocurrency price changes.
It pulls subreddit activity using the PushShift API and runs a regression to examine the impact
of Reddit attention on crypto price movement.
"""

import pandas as pd
import requests
import statsmodels.api as sm
from time import sleep

# ------------------------------
# Load Cryptocurrency Trading Data
# ------------------------------

def load_crypto_data(file_path):
    """Loads historical cryptocurrency trading data from a CSV file."""
    df = pd.read_csv(file_path)
    df = df[df['Date'] >= '2021-01-01']  # Filter for 2021 data
    return df

# ------------------------------
# Scrape Reddit Mentions Using PushShift API
# ------------------------------

def get_reddit_mentions(crypto_list, start_date, end_date):
    """Fetches the number of Reddit mentions for each cryptocurrency."""
    mentions = {}
    base_url = "https://api.pushshift.io/reddit/search/submission/"

    for crypto in crypto_list:
        params = {
            "q": crypto,
            "after": start_date,
            "before": end_date,
            "subreddit": "wallstreetbets",
            "size": 0,
            "aggs": "created_utc"
        }
        try:
            response = requests.get(base_url, params=params)
            response.raise_for_status()
            data = response.json()
            mentions[crypto] = len(data.get('data', []))
        except (requests.RequestException, ValueError) as e:
            print(f"Error fetching mentions for {crypto}: {e}")
            mentions[crypto] = None
        sleep(1)  # Prevent API rate limit
    return mentions

# ------------------------------
# Prepare Data for Regression
# ------------------------------

def prepare_data(trading_df, mentions_dict):
    """Merges trading data with Reddit mentions and prepares for regression."""
    trading_df['Mentions'] = trading_df['Currency'].map(mentions_dict)
    trading_df['Change %'] = trading_df['Change %'].str.rstrip('%').astype(float)
    trading_df.dropna(inplace=True)
    return trading_df

# ------------------------------
# Run Regression Analysis
# ------------------------------

def run_regression(data):
    """Performs OLS regression of price change on Reddit mentions."""
    X = sm.add_constant(data[['Mentions']])  # Independent variable
    y = data['Change %']  # Dependent variable
    model = sm.OLS(y, X).fit()
    print(model.summary())
    return model

# ------------------------------
# Main Execution
# ------------------------------

if __name__ == "__main__":
    crypto_file = "crypto_data.csv"  # Replace with your dataset
    crypto_list = [
        "Bitcoin", "Ethereum", "Tether", "BNB", "Binance USD",
        "XRP", "Dogecoin", "Cardano", "Polygon", "Polkadot"
    ]

    # Load and process data
    crypto_data = load_crypto_data(crypto_file)
    reddit_mentions = get_reddit_mentions(crypto_list, "2021-01-01", "2021-12-31")
    merged_data = prepare_data(crypto_data, reddit_mentions)

    # Run regression
    regression_model = run_regression(merged_data)
