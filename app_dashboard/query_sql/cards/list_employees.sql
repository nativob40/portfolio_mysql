SELECT COUNT(DATE_FORMAT(hire_date,'%Y-%m-%d')) AS New_Employees 
FROM employees.employees
WHERE YEAR(DATE_FORMAT(hire_date,'%Y-%m-%d')) = 2000

