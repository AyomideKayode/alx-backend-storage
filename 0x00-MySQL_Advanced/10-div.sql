-- Create function SafeDiv
DELIMITER $$

CREATE FUNCTION SafeDiv(a INT, b INT)
RETURNS INT
BEGIN
    DECLARE result INT;
	    
    -- Check if b is equal to 0
    IF b = 0 THEN
        SET result = 0; -- Return 0 if b is 0
    ELSE
        SET result = a / b; -- Divide a by b if b is not 0
    END IF;
				    
    RETURN result; -- Return the result
END $$

DELIMITER ;

