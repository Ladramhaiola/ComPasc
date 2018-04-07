PROGRAM Greeting;

VAR 
x, y, z, a: INTEGER; 
height, width : INTEGER; 
c: CHAR;

CONSTANT
x = 5;
y = 6;

TYPE
   a1 = ARRAY[x..10] OF INTEGER;

BEGIN
   z := 7;
   IF a1[6]<z THEN
      BEGIN
   	 a1[7] := z;
      END;
   ELSE
      BEGIN
   	 z := a1[6];
      END;

END;
