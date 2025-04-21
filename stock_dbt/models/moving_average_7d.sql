SELECT
  ticker,
  date,
  close,
  AVG(close) OVER (
    PARTITION BY ticker
    ORDER BY date
    ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
  ) AS moving_avg_7d
FROM {{ source('stock_data', 'raw_stock_prices') }}

