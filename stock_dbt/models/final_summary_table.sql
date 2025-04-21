select
  ticker,
  count(*) as total_days,
  avg((high + low) / 2) as avg_price,
  min(date) as start_date,
  max(date) as end_date
from {{ source('stock_data', 'raw_stock_prices') }}
group by ticker
