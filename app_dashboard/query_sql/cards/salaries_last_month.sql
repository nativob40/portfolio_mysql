SELECT sum(salary) AS Salaries_Last_Month
FROM employees.salaries
WHERE YEAR(DATE_FORMAT(to_date,'%Y-%m-%d')) = 2002 AND
      MONTH(DATE_FORMAT(to_date,'%Y-%m-%d')) = 8 AND
      DAY(DATE_FORMAT(to_date,'%Y-%m-%d')) = 1
