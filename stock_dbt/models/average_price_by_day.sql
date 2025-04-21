SELECT
  DATE(date) AS trade_date,
  ticker,
  ROUND(AVG(high - low), 2) AS avg_range
FROM
  {{ source('stock_data', 'raw_stock_prices') }}
GROUP BY
  trade_date,
  ticker
ORDER BY
  trade_date,
  ticker
