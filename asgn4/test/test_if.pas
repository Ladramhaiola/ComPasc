PROGRAM Greeting;

CONSTANT
x = 5;
y = 6;

TYPE
   a1 = ARRAY[x..10] OF INTEGER;

VAR 
z, a	      : INTEGER; 
height, width : INTEGER; 
c	      : CHAR;
   a2	      : a1;

BEGIN
   z := 7;
   IF a2[6]<z THEN
      BEGIN
   	 a2[7] := z;
      END;
   ELSE
      BEGIN
   	 z := a2[6];
      END;

END;
