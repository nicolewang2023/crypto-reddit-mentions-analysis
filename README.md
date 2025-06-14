# crypto-reddit-mentions-analysis

This project investigates the relationship between cryptocurrency price movements and Reddit activity using Python. Specifically, it measures how the frequency of mentions on the r/wallstreetbets subreddit correlates with daily percentage changes in cryptocurrency trading volumes.

## Objective

To assess whether online discussions in retail investor communities impact short-term market behavior, using Reddit mentions as a proxy for sentiment or attention.

## Data Sources

- **Cryptocurrency data**: Historical trading data (price, volume, change %) loaded from `crypto_data.csv`
- **Reddit data**: Reddit post counts pulled from the r/wallstreetbets subreddit via the PushShift API

## Methodology

1. Load and filter cryptocurrency data for the year 2021
2. Query Reddit for the number of posts mentioning each major cryptocurrency
3. Merge Reddit mentions with corresponding trading records
4. Run a linear regression to assess how mention counts relate to price or volume changes

## Tools & Libraries

- Python, Pandas, Requests
- PushShift API (Reddit data)
- Statsmodels (regression)

## Sample Output

The regression model estimates the impact of Reddit mentions on daily price change (%). A summary of coefficients, significance levels, and R² is printed via `statsmodels`.

## Future Work

- Expand subreddit scope (e.g., r/cryptocurrency, r/bitcoin)
- Include sentiment analysis of post content
- Model time-lagged effects (mentions today → prices tomorrow)
- Use a larger dataset or real-time feed
