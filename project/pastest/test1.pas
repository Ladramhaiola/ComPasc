PROGRAM Greeting;

CONSTANT
x = 1;
y = 1;

TYPE
   a1 = ARRAY[x..10,y..10] OF INTEGER;

VAR 
a2: a1;
c : INTEGER;

BEGIN
   c := x+y;
   a2[7,8] := c;
   c := a2[7,8];
   WRITELN(c);
END;
