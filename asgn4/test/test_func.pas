PROGRAM Sort (input, output);

CONSTANT
	MaxElts = 50;

TYPE 
	IntArrType = ARRAY [1..MaxElts] OF Integer;

VAR
	i, j, tmp, size: integer;
	arr: IntArrType;

PROCEDURE ReadArr(size: Integer; a: IntArrType);
BEGIN
    size := 1;
    {WHILE NOT eof DO }
    {BEGIN}
		{readln(a[size]);}
	{END;}
	{IF NOT eof THEN}
	{BEGIN}
		{size := size + 1;}
    {END;}
END;

BEGIN
	ReadArr(size, arr);
	i := size - 1;
END;
	    
