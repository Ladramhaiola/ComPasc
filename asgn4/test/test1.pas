PROGRAM Greeting;

VAR 
x, y, z, a: INTEGER; 
height, width : INTEGER; 
c: CHAR;

CONSTANT
x = 1;
y = 6;

{TYPE}
{a1 = ARRAY[x..y] OF INTEGER;}

{procedure Print(x: INTEGER;y: INTEGER);}
{BEGIN}
    {x := x + y;}
{END;}

FUNCTION Print(x: INTEGER;y: INTEGER): INTEGER;
BEGIN
    Print := x + y;
END;

BEGIN
   x:=3;
   Print(x,y);
   {y:=21;}
   {z:=11;}
   {a1[6]:=a1[6]-y;}
   {IF a1[6]<z THEN}
      {BEGIN}
	 {a1[7] := z;}
      {END;}
   {ELSE}
      {BEGIN}
	 {z := a1[6];}
      {END;}

    {WHILE x < 5 DO}
    {BEGIN}
        {x := x + 1;}
    {END;}
   {REPEAT}
        {x := x + 1;}
    {UNTIL x<9;}

   {CASE x OF}
    {1: x:= x + 1;}
    {2: x:= x + 2;}
    {3: x:= x + 3;}
    {ELSE }
    {BEGIN}
        {x:= x + 5;}
    {END;}
   {END;}
END;
