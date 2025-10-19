SELECT load_employee_bonus_mart(2025, 10);

SELECT * FROM v_employee_bonus_summary 
WHERE year = 2025 AND month = 10
ORDER BY total_bonus DESC;

SELECT * FROM get_bonus_statistics(2025, 10);

SELECT 
    CASE 
        WHEN experience_years < 1 THEN 'До 1 года'
        WHEN experience_years < 2 THEN '1-2 года'
        ELSE 'Более 2 лет'
    END as experience_category,
    COUNT(*) as employee_count,
    ROUND(AVG(total_bonus), 2) as avg_bonus,
    ROUND(SUM(total_bonus), 2) as total_bonus_paid
FROM employee_bonus_mart
WHERE year = 2025 AND month = 10
GROUP BY 
    CASE 
        WHEN experience_years < 1 THEN 'До 1 года'
        WHEN experience_years < 2 THEN '1-2 года'
        ELSE 'Более 2 лет'
    END
ORDER BY avg_bonus DESC;

SELECT 
    employee_name,
    base_salary,
    experience_years,
    total_bonus,
    ROUND((total_bonus / base_salary * 100), 2) as bonus_percentage
FROM employee_bonus_mart
WHERE year = 2025 AND month = 10
ORDER BY total_bonus DESC
LIMIT 5;

SELECT 
    employee_name,
    rental_bonus,
    repair_bonus,
    total_bonus,
    ROUND((rental_bonus / total_bonus * 100), 2) as rental_percentage,
    ROUND((repair_bonus / total_bonus * 100), 2) as repair_percentage
FROM employee_bonus_mart
WHERE year = 2025 AND month = 10
AND total_bonus > 0
ORDER BY total_bonus DESC;
