CREATE DEFINER=`root`@`localhost` TRIGGER `trg_salary_updated` AFTER UPDATE ON `employees` FOR EACH ROW BEGIN

    IF OLD.salary <> NEW.salary THEN

        INSERT INTO employee_salaries
        (
            employee_id,
            salary,
            effective_from
        )
        VALUES
        (
            NEW.employee_id,
            NEW.salary,
            CURRENT_DATE
        );

    END IF;

END;
