SELECT dept_name as departamento,
       sum(salary) as Salario_Mes,
       roundAVG(salary),2) as AVG
FROM employees.dept_emp
INNER JOIN employees.departments ON dept_emp.dept_no = departments.dept_no
INNER JOIN employees.salaries ON dept_emp.emp_no = salaries.emp_no
WHERE YEAR(DATE_FORMAT(salaries.to_date,'%Y-%m-%d'))=2002
GROUP BY dept_name
ORDER BY sum(salary) desc