CREATE DEFINER=`root`@`localhost` EVENT `evt_salary_review` ON SCHEDULE EVERY 1 MONTH STARTS '2026-09-09 17:30:05' ON COMPLETION NOT PRESERVE ENABLE DO BEGIN

    UPDATE employees
    SET updated_at = CURRENT_TIMESTAMP
    WHERE employment_status = 'Active';

END;
