WITH bicycle_revenue AS (
    SELECT 
        b.id,
        b.brand,
        b.type,
        b.rent_price,
        COALESCE(SUM(rb.time * b.rent_price), 0) as total_revenue,
        COALESCE(SUM(sb.price), 0) as total_service_cost
    FROM bicycle b
    LEFT JOIN rent_book rb ON b.id = rb.bicycle_id AND rb.paid = true
    LEFT JOIN service_book sb ON b.id = sb.bicycle_id
    GROUP BY b.id, b.brand, b.type, b.rent_price
),
bicycle_profitability AS (
    SELECT 
        id,
        brand,
        type,
        rent_price,
        total_revenue,
        total_service_cost,
        (total_revenue - total_service_cost) as net_profit,
        CASE 
            WHEN total_service_cost > 0 THEN (total_revenue - total_service_cost) / total_service_cost
            ELSE total_revenue
        END as profitability_ratio
    FROM bicycle_revenue
)
SELECT 
    brand,
    type,
    rent_price,
    total_revenue,
    total_service_cost,
    net_profit,
    ROUND(profitability_ratio::numeric, 2) as profitability_ratio
FROM bicycle_profitability
ORDER BY profitability_ratio DESC, net_profit DESC
LIMIT 5;

SELECT 
    s.name as staff_name,
    s.salary,
    COUNT(sb.id) as service_count,
    ROUND(AVG(sb.price)::numeric, 2) as avg_service_price,
    ROUND(SUM(sb.price)::numeric, 2) as total_service_revenue,
    ROUND((SUM(sb.price) / s.salary)::numeric, 2) as revenue_to_salary_ratio,
    COUNT(DISTINCT sb.bicycle_id) as unique_bicycles_serviced
FROM staff s
LEFT JOIN service_book sb ON s.id = sb.staff_id
GROUP BY s.id, s.name, s.salary
ORDER BY revenue_to_salary_ratio DESC, service_count DESC;

SELECT 
    c.name as client_name,
    c.city,
    c.country,
    COUNT(rb.id) as total_rentals,
    ROUND(SUM(rb.time)::numeric, 2) as total_rental_hours,
    ROUND(SUM(rb.time * b.rent_price)::numeric, 2) as total_spent,
    ROUND(AVG(rb.time * b.rent_price)::numeric, 2) as avg_rental_cost,
    ROUND(MAX(rb.time * b.rent_price)::numeric, 2) as max_single_rental,
    COUNT(DISTINCT rb.bicycle_id) as unique_bicycles_rented
FROM client c
LEFT JOIN rent_book rb ON c.id = rb.client_id AND rb.paid = true
LEFT JOIN bicycle b ON rb.bicycle_id = b.id
GROUP BY c.id, c.name, c.city, c.country
HAVING COUNT(rb.id) > 0
ORDER BY total_spent DESC, total_rentals DESC
LIMIT 10;

SELECT 
    b.type as bicycle_type,
    COUNT(DISTINCT b.id) as total_bicycles,
    COUNT(rb.id) as total_rentals,
    ROUND(AVG(b.rent_price)::numeric, 2) as avg_rent_price,
    ROUND(SUM(rb.time * b.rent_price)::numeric, 2) as total_revenue,
    ROUND(AVG(rb.time)::numeric, 2) as avg_rental_duration,
    ROUND((COUNT(rb.id)::float / COUNT(DISTINCT b.id))::numeric, 2) as rentals_per_bicycle,
    ROUND((SUM(rb.time * b.rent_price) / COUNT(DISTINCT b.id))::numeric, 2) as revenue_per_bicycle
FROM bicycle b
LEFT JOIN rent_book rb ON b.id = rb.bicycle_id AND rb.paid = true
GROUP BY b.type
ORDER BY total_revenue DESC, rentals_per_bicycle DESC;

SELECT 
    d.type as detail_type,
    d.brand as detail_brand,
    COUNT(sb.id) as usage_count,
    ROUND(AVG(d.price)::numeric, 2) as avg_detail_price,
    ROUND(SUM(sb.price)::numeric, 2) as total_service_cost,
    ROUND(AVG(sb.price)::numeric, 2) as avg_service_cost,
    COUNT(DISTINCT sb.bicycle_id) as unique_bicycles_serviced,
    ROUND((SUM(sb.price) / COUNT(sb.id))::numeric, 2) as cost_per_service,
    ROUND((COUNT(sb.id)::float / COUNT(DISTINCT sb.bicycle_id))::numeric, 2) as services_per_bicycle
FROM detail d
INNER JOIN service_book sb ON d.id = sb.detail_id
INNER JOIN bicycle b ON sb.bicycle_id = b.id
GROUP BY d.type, d.brand
ORDER BY total_service_cost DESC, usage_count DESC;
