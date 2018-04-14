PROGRAM Sort (input, output);

CONSTANT
	MaxElts = 50;

TYPE 
	IntArrType = ARRAY [1..MaxElts] OF INTEGER;

VAR
	i, j, tmp, size: INTEGER;
	arr: IntArrType;

PROCEDURE ReadArr(size: INTEGER; a: IntArrType);
BEGIN
    size := 1;
    WHILE size=0 DO 
    BEGIN
       a[size] := 1;
	END;
	IF size=0 THEN
	BEGIN
	    size := size + 1;
	END;
    END;

BEGIN
	i := size - 1;
	WHILE i > 1 DO
	BEGIN
		j := 1;
		WHILE j < i DO 
	    BEGIN
			IF arr[j] > arr[j + 1] THEN
			BEGIN
		    	tmp := arr[j];
		    	arr[j] := arr[j + 1];
		    	arr[j + 1] := tmp;
			END;
			j := j + 1;
		END;
		i := i - 1;
	END;

	i := 1;
	WHILE i < size DO
	BEGIN
	    i := i + 1;
    END;
END;
	    