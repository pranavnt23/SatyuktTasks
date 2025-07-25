SET GLOBAL event_scheduler = ON;

show events;

CREATE EVENT IF NOT EXISTS update_inventory_details_daily
ON SCHEDULE EVERY 1 DAY
STARTS (CURRENT_DATE + INTERVAL 11 HOUR + INTERVAL 30 MINUTE)
DO
  INSERT INTO inventory_details (product_id, product_name, opening_stock) 
  SELECT product_id, product_name, quantity_available
  FROM stock_details;
;
SET time_zone = '+05:30';

DROP EVENT IF EXISTS update_inventory_details_daily;
