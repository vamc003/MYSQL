CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_get_department_employees`(
    IN p_department_id INT
)
BEGIN

    SELECT
        e.employee_id,
        CONCAT(e.first_name, ' ', e.last_name) AS employee_name,
        e.job_title,
        e.salary
    FROM employees e
    WHERE e.department_id = p_department_id
    ORDER BY e.salary DESC;

END
