-- 1. Jurisdiction Hierarchy Table 
CREATE TABLE jurisdictions (
    id INT PRIMARY KEY,
    village VARCHAR(100),
    district VARCHAR(100),
    region VARCHAR(100),
    population INT
);

-- 2. Partners Table 
CREATE TABLE partners (
    id INT PRIMARY KEY,
    name VARCHAR(100),
    type VARCHAR(50)
);

-- 3. Activities Table 
CREATE TABLE activities (
    id INT PRIMARY KEY,
    partner_id INT,
    jurisdiction_id INT,
    activity_type VARCHAR(50),
    beneficiaries INT,
    budget DECIMAL(10,2),
    start_date DATE,
    FOREIGN KEY (partner_id) REFERENCES partners(id),
    FOREIGN KEY (jurisdiction_id) REFERENCES jurisdictions(id)
);

-- Insert jurisdictions
INSERT INTO jurisdictions (id, village, district, region, population) VALUES
(1, 'Bondhere', 'Bondhere', 'Banaadir', 45000),
(2, 'Hodan', 'Hodan', 'Banaadir', 62000),
(3, 'Garasbaley', 'Karan', 'Banaadir', 28000),
(4, 'Hargeisa Central', 'Hargeisa', 'Woqooyi Galbeed', 75000),
(5, 'Gabiley Town', 'Gabiley', 'Woqooyi Galbeed', 42000);

-- Insert partners
INSERT INTO partners (id, name, type) VALUES
(1, 'IRC Somalia', 'INGO'),
(2, 'Save the Children', 'INGO'),
(3, 'Somali Red Crescent', 'LNGO'),
(4, 'UNICEF', 'UN');

-- Insert activities
INSERT INTO activities (id, partner_id, jurisdiction_id, activity_type, beneficiaries, budget, start_date) VALUES
(1, 1, 1, 'Education', 1500, 250000, '2023-01-10'),
(2, 1, 2, 'Health', 3200, 180000, '2023-02-15'),
(3, 2, 3, 'Nutrition', 850, 120000, '2023-03-01'),
(4, 3, 4, 'WASH', 4200, 220000, '2023-01-20'),
(5, 4, 5, 'Education', 3000, 280000, '2023-03-15');

SELECT 
    j.district,
    j.region,
    COUNT(a.id) AS activity_count,
    SUM(a.beneficiaries) AS total_beneficiaries,
    SUM(a.budget) AS total_budget,
    ROUND(SUM(a.beneficiaries) * 100.0 / j.population, 2) AS coverage_pct
FROM jurisdictions j
LEFT JOIN activities a ON j.id = a.jurisdiction_id
GROUP BY j.district, j.region, j.population
ORDER BY j.region, j.district;

SELECT 
    p.name AS partner_name,
    p.type AS partner_type,
    COUNT(a.id) AS total_activities,
    SUM(a.beneficiaries) AS total_beneficiaries,
    SUM(a.budget) AS total_budget,
    COUNT(DISTINCT j.region) AS regions_covered
FROM partners p
LEFT JOIN activities a ON p.id = a.partner_id
LEFT JOIN jurisdictions j ON a.jurisdiction_id = j.id
GROUP BY p.id, p.name, p.type
ORDER BY total_beneficiaries DESC;

SELECT 
    region,
    SUM(population) AS total_population,
    SUM(beneficiaries) AS total_beneficiaries,
    ROUND(SUM(beneficiaries) * 100.0 / SUM(population), 2) AS coverage_pct
FROM jurisdictions j
LEFT JOIN (
    SELECT jurisdiction_id, SUM(beneficiaries) AS beneficiaries
    FROM activities 
    GROUP BY jurisdiction_id
) a ON j.id = a.jurisdiction_id
GROUP BY region
ORDER BY coverage_pct DESC;

SELECT 
    activity_type,
    COUNT(*) AS activity_count,
    SUM(beneficiaries) AS total_beneficiaries,
    SUM(budget) AS total_budget,
    ROUND(AVG(budget / beneficiaries), 2) AS cost_per_beneficiary
FROM activities
GROUP BY activity_type
ORDER BY total_beneficiaries DESC;

-- High and medium coverage districts
SELECT 
    district,
    'High Coverage' AS coverage_level,
    coverage_pct
FROM (
    SELECT 
        district,
        ROUND(SUM(beneficiaries) * 100.0 / population, 2) AS coverage_pct
    FROM jurisdictions j
    JOIN activities a ON j.id = a.jurisdiction_id
    GROUP BY district, population
) WHERE coverage_pct >= 50

UNION ALL

SELECT 
    district,
    'Medium Coverage' AS coverage_level,
    coverage_pct
FROM (
    SELECT 
        district,
        ROUND(SUM(beneficiaries) * 100.0 / population, 2) AS coverage_pct
    FROM jurisdictions j
    JOIN activities a ON j.id = a.jurisdiction_id
    GROUP BY district, population
) WHERE coverage_pct BETWEEN 25 AND 49.99

ORDER BY coverage_pct DESC;

-- High and medium coverage districts
SELECT 
    district,
    'High Coverage' AS coverage_level,
    coverage_pct
FROM (
    SELECT 
        district,
        ROUND(SUM(beneficiaries) * 100.0 / population, 2) AS coverage_pct
    FROM jurisdictions j
    JOIN activities a ON j.id = a.jurisdiction_id
    GROUP BY district, population
) WHERE coverage_pct >= 50

UNION ALL

SELECT 
    district,
    'Medium Coverage' AS coverage_level,
    coverage_pct
FROM (
    SELECT 
        district,
        ROUND(SUM(beneficiaries) * 100.0 / population, 2) AS coverage_pct
    FROM jurisdictions j
    JOIN activities a ON j.id = a.jurisdiction_id
    GROUP BY district, population
) WHERE coverage_pct BETWEEN 25 AND 49.99

ORDER BY coverage_pct DESC;
