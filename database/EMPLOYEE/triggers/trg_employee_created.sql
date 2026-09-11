CREATE DEFINER=`root`@`localhost` TRIGGER `trg_employee_created` AFTER INSERT ON `employees` FOR EACH ROW BEGIN

    INSERT INTO employee_audit
    (
        employee_id,
        action_type
    )
    VALUES
    (
        NEW.employee_id,
        'EMPLOYEE_CREATED'
    );

END;
