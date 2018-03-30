PROGRAM Greeting;
VAR 
x, y, z, a: INTEGER; 
height, width : INTEGER; 
c: CHAR;
CONSTANT
x = 5;
y = 10;
TYPE
a1 = ARRAY[x..y] OF INTEGER;
//procedure Draw;
BEGIN
   x:=14;
   y:=21;
   z:=11;
   a1[6]:=a1[6]-y;
END;
