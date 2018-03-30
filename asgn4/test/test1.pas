PROGRAM Greeting;
VAR 
x, y, z, a: INTEGER; 
height, width : INTEGER; 
c: CHAR;
CONSTANT
x = 1;
y = 6;
TYPE
a1 = ARRAY[x..y] OF INTEGER;
//procedure Draw;
BEGIN
   x:=14;
   y:=21;
   z:=11;
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
   CASE x OF
    1: x:= x + 1;
    2: x:= x + 2;
    3: x:= x + 3;
   END;

END;
