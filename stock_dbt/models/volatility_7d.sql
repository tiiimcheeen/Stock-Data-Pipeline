SELECT
  ticker,
  date,
  STDDEV(close) OVER (
    PARTITION BY ticker
    ORDER BY date
    ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
  ) AS volatility_7d
FROM {{ source('stock_data', 'raw_stock_prices') }}

