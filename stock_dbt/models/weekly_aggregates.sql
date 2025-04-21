SELECT
  ticker,
  FORMAT_TIMESTAMP('%G-W%V', DATE_TRUNC(date, WEEK(MONDAY))) AS week_starting,
  COUNT(*) AS trading_days,
  AVG(close) AS avg_close,
  MAX(high) AS weekly_high,
  MIN(low) AS weekly_low
FROM {{ source('stock_data', 'raw_stock_prices') }}
GROUP BY ticker, week_starting
ORDER BY ticker, week_starting
