CREATE TABLE IF NOT EXISTS employees (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    department VARCHAR(100) NOT NULL
);

CREATE TABLE IF NOT EXISTS leaves (
    id INT AUTO_INCREMENT PRIMARY KEY,
    employee_id INT NOT NULL,
    from_date DATE NOT NULL,
    to_date DATE NOT NULL,
    reason VARCHAR(255),
    status VARCHAR(50) DEFAULT 'Pending',
    FOREIGN KEY (employee_id) REFERENCES employees(id)
);

INSERT INTO employees (name, department)
SELECT 'Amit', 'IT'
WHERE NOT EXISTS (
    SELECT 1 FROM employees
    WHERE name = 'Amit' AND department = 'IT'
);

INSERT INTO employees (name, department)
SELECT 'Priya', 'HR'
WHERE NOT EXISTS (
    SELECT 1 FROM employees
    WHERE name = 'Priya' AND department = 'HR'
);

INSERT INTO employees (name, department)
SELECT 'Rahul', 'Finance'
WHERE NOT EXISTS (
    SELECT 1 FROM employees
    WHERE name = 'Rahul' AND department = 'Finance'
);
