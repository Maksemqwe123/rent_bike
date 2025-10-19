CREATE TABLE IF NOT EXISTS employee_bonus_mart (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    year INTEGER NOT NULL,
    month INTEGER NOT NULL,
    employee_name VARCHAR(50) NOT NULL,
    employee_id UUID NOT NULL,
    base_salary DECIMAL(10,2) NOT NULL,
    experience_years DECIMAL(3,1) NOT NULL,
    experience_bonus_percent DECIMAL(5,2) NOT NULL,
    rental_revenue DECIMAL(10,2) DEFAULT 0,
    rental_bonus DECIMAL(10,2) DEFAULT 0,
    repair_revenue DECIMAL(10,2) DEFAULT 0,
    repair_bonus DECIMAL(10,2) DEFAULT 0,
    total_bonus DECIMAL(10,2) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(year, month, employee_id)
);

CREATE INDEX IF NOT EXISTS idx_bonus_mart_year_month ON employee_bonus_mart(year, month);
CREATE INDEX IF NOT EXISTS idx_bonus_mart_employee ON employee_bonus_mart(employee_id);
CREATE INDEX IF NOT EXISTS idx_bonus_mart_created ON employee_bonus_mart(created_at);

CREATE OR REPLACE FUNCTION calculate_experience_bonus_percent(experience_years DECIMAL)
RETURNS DECIMAL(5,2) AS $$
BEGIN
    IF experience_years < 1.0 THEN
        RETURN 5.00;
    ELSIF experience_years < 2.0 THEN
        RETURN 10.00;
    ELSE
        RETURN 15.00;
    END IF;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION calculate_work_experience(hire_date TIMESTAMP)
RETURNS DECIMAL(3,1) AS $$
BEGIN
    RETURN EXTRACT(YEAR FROM AGE(CURRENT_DATE, hire_date));
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION load_employee_bonus_mart(
    target_year INTEGER DEFAULT EXTRACT(YEAR FROM CURRENT_DATE),
    target_month INTEGER DEFAULT EXTRACT(MONTH FROM CURRENT_DATE)
)
RETURNS VOID AS $$
DECLARE
    rec RECORD;
    experience_years DECIMAL(3,1);
    experience_bonus_percent DECIMAL(5,2);
    rental_revenue DECIMAL(10,2);
    rental_bonus DECIMAL(10,2);
    repair_revenue DECIMAL(10,2);
    repair_bonus DECIMAL(10,2);
    total_bonus DECIMAL(10,2);
BEGIN
    DELETE FROM employee_bonus_mart 
    WHERE year = target_year AND month = target_month;
    
    FOR rec IN 
        SELECT 
            s.id as employee_id,
            s.name as employee_name,
            s.salary as base_salary,
            s.created as hire_date
        FROM staff s
    LOOP
        experience_years := calculate_work_experience(rec.hire_date);
        
        experience_bonus_percent := calculate_experience_bonus_percent(experience_years);
        
        SELECT COALESCE(SUM(rb.time * b.rent_price), 0)
        INTO rental_revenue
        FROM rent_book rb
        JOIN bicycle b ON rb.bicycle_id = b.id
        WHERE rb.staff_id = rec.employee_id
        AND rb.paid = true
        AND EXTRACT(YEAR FROM rb.created) = target_year
        AND EXTRACT(MONTH FROM rb.created) = target_month;
        
        rental_bonus := rental_revenue * 0.30;
        
        SELECT COALESCE(SUM(sb.price), 0)
        INTO repair_revenue
        FROM service_book sb
        WHERE sb.staff_id = rec.employee_id
        AND EXTRACT(YEAR FROM sb.created) = target_year
        AND EXTRACT(MONTH FROM sb.created) = target_month;
        
        repair_bonus := repair_revenue * 0.80;
        
        total_bonus := (rental_bonus + repair_bonus) * (experience_bonus_percent / 100.0);
        
        INSERT INTO employee_bonus_mart (
            year,
            month,
            employee_name,
            employee_id,
            base_salary,
            experience_years,
            experience_bonus_percent,
            rental_revenue,
            rental_bonus,
            repair_revenue,
            repair_bonus,
            total_bonus
        ) VALUES (
            target_year,
            target_month,
            rec.employee_name,
            rec.employee_id,
            rec.base_salary,
            experience_years,
            experience_bonus_percent,
            rental_revenue,
            rental_bonus,
            repair_revenue,
            repair_bonus,
            total_bonus
        );
        
    END LOOP;
    
    RAISE NOTICE 'Витрина данных загружена для %/%', target_month, target_year;
    RAISE NOTICE 'Обработано сотрудников: %', (SELECT COUNT(*) FROM employee_bonus_mart WHERE year = target_year AND month = target_month);
    
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION load_employee_bonus_mart_year(target_year INTEGER DEFAULT EXTRACT(YEAR FROM CURRENT_DATE))
RETURNS VOID AS $$
DECLARE
    month_num INTEGER;
BEGIN
    FOR month_num IN 1..12 LOOP
        PERFORM load_employee_bonus_mart(target_year, month_num);
    END LOOP;
    
    RAISE NOTICE 'Витрина данных загружена за весь % год', target_year;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE VIEW v_employee_bonus_summary AS
SELECT 
    year,
    month,
    employee_name,
    base_salary,
    experience_years,
    experience_bonus_percent,
    rental_revenue,
    rental_bonus,
    repair_revenue,
    repair_bonus,
    total_bonus,
    ROUND((total_bonus / base_salary * 100), 2) as bonus_percentage_of_salary,
    created_at
FROM employee_bonus_mart
ORDER BY year DESC, month DESC, total_bonus DESC;

CREATE OR REPLACE FUNCTION get_bonus_statistics(
    target_year INTEGER DEFAULT EXTRACT(YEAR FROM CURRENT_DATE),
    target_month INTEGER DEFAULT EXTRACT(MONTH FROM CURRENT_DATE)
)
RETURNS TABLE (
    total_employees INTEGER,
    total_bonus_paid DECIMAL(10,2),
    avg_bonus_per_employee DECIMAL(10,2),
    max_bonus DECIMAL(10,2),
    min_bonus DECIMAL(10,2),
    total_rental_revenue DECIMAL(10,2),
    total_repair_revenue DECIMAL(10,2)
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        COUNT(*)::INTEGER as total_employees,
        SUM(ebm.total_bonus) as total_bonus_paid,
        ROUND(AVG(ebm.total_bonus), 2) as avg_bonus_per_employee,
        MAX(ebm.total_bonus) as max_bonus,
        MIN(ebm.total_bonus) as min_bonus,
        SUM(ebm.rental_revenue) as total_rental_revenue,
        SUM(ebm.repair_revenue) as total_repair_revenue
    FROM employee_bonus_mart ebm
    WHERE ebm.year = target_year AND ebm.month = target_month;
END;
$$ LANGUAGE plpgsql;
