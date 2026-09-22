-- Coffee Shop Sales SQL Analysis

-- 1 Total Revenue
SELECT ROUND(SUM(transaction_qty*unit_price),2) AS total_revenue FROM coffee_sales;

-- 2 Revenue by Store Location
SELECT store_location, ROUND(SUM(transaction_qty*unit_price),2) AS total_revenue FROM coffee_sales GROUP BY store_location ORDER BY total_revenue DESC;

-- 3 Top 10 Best-Selling Products
SELECT product_detail, SUM(transaction_qty) AS total_quantity_sold FROM coffee_sales GROUP BY product_detail ORDER BY total_quantity_sold DESC LIMIT 10;

-- 4 Top 10 Revenue-Generating Products
SELECT product_detail, ROUND(SUM(transaction_qty*unit_price),2) AS total_revenue FROM coffee_sales GROUP BY product_detail ORDER BY total_revenue DESC LIMIT 10;

-- 5 Sales by Product Category
SELECT product_category, SUM(transaction_qty) AS total_quantity, ROUND(SUM(transaction_qty*unit_price),2) AS total_revenue FROM coffee_sales GROUP BY product_category ORDER BY total_revenue DESC;

-- 6 Monthly Revenue Trend
SELECT strftime('%Y-%m',transaction_date) AS month, ROUND(SUM(transaction_qty*unit_price),2) AS total_revenue FROM coffee_sales GROUP BY month ORDER BY month;

-- 7 Peak Hours
SELECT CAST(strftime('%H',transaction_time) AS INTEGER) AS hour, COUNT(*) AS transaction_count FROM coffee_sales GROUP BY hour ORDER BY hour;

-- 8 Day of Week
SELECT CASE CAST(strftime('%w',transaction_date) AS INTEGER) WHEN 0 THEN 'Sunday' WHEN 1 THEN 'Monday' WHEN 2 THEN 'Tuesday' WHEN 3 THEN 'Wednesday' WHEN 4 THEN 'Thursday' WHEN 5 THEN 'Friday' WHEN 6 THEN 'Saturday' END AS day_of_week, SUM(transaction_qty) AS total_quantity, ROUND(SUM(transaction_qty*unit_price),2) AS total_revenue FROM coffee_sales GROUP BY CAST(strftime('%w',transaction_date) AS INTEGER) ORDER BY CAST(strftime('%w',transaction_date) AS INTEGER);

-- 9 Average Order Value by Store
SELECT store_location, ROUND(AVG(transaction_qty*unit_price),2) AS average_order_value FROM coffee_sales GROUP BY store_location ORDER BY average_order_value DESC;

-- 10 Product Category Share
WITH category_revenue AS (SELECT product_category, SUM(transaction_qty*unit_price) AS revenue FROM coffee_sales GROUP BY product_category) SELECT product_category, ROUND(revenue,2) AS revenue, ROUND(100.0*revenue/(SELECT SUM(revenue) FROM category_revenue),2) AS revenue_share_pct FROM category_revenue ORDER BY revenue DESC;
