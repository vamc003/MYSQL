CREATE DEFINER=`root`@`localhost` FUNCTION `fn_annual_salary`(
    p_monthly_salary DECIMAL(12,2)
) RETURNS decimal(14,2)
    DETERMINISTIC
BEGIN

    RETURN p_monthly_salary * 12;

END
