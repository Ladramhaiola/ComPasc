PROGRAM Sort (input, output);

CONSTANT
	MaxElts = 50;

TYPE 
	IntArrType = ARRAY [1..MaxElts] OF Integer;

VAR
	i, j, tmp, size: integer;
	arr: IntArrType;

{ procedure Print(x: INTEGER;y: INTEGER); }
{ BEGIN }
{     x := x + y; }
{ END; }

{ FUNCTION Print1(x: INTEGER;y: INTEGER): INTEGER; }
{ BEGIN }
{     Print1 := x + y; }
{ END; }

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
	    
