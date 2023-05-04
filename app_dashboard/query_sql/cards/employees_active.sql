SELECT COUNT(DATE_FORMAT(to_date,'%Y-%m-%d')) AS Active_Employees
 FROM employees.dept_emp_latest_date 
 WHERE YEAR(DATE_FORMAT(to_date,'%Y-%m-%d'))=9999