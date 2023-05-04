SELECT DISTINCT  
        departments.dept_name as departamento,
        DATE_FORMAT(hire_date, "%Y") as año,
        COUNT(employees.emp_no) as Cant_Emp
        

FROM employees.employees
INNER JOIN dept_emp
ON employees.employees.emp_no = dept_emp.emp_no
INNER JOIN departments
ON dept_emp.dept_no = departments.dept_no
WHERE departments.dept_name IN ('Development','Production','Finance','Sales','Human Resources')
GROUP BY DATE_FORMAT(hire_date, "%Y"),departments.dept_name
ORDER BY departments.dept_name,DATE_FORMAT(hire_date, "%Y")