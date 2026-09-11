CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_get_employee`(
    IN p_employee_id INT
)
BEGIN

    SELECT
        employee_id,
        first_name,
        last_name,
        email,
        job_title,
        department_id,
        salary,
        employment_status
    FROM employees
    WHERE employee_id = p_employee_id;

END
