PROGRAM Greeting;
VAR 
x, y, z, a: INTEGER; 
height, width : INTEGER; 
c: CHAR;
CONSTANT
x = 5;
//procedure Draw;
BEGIN
   x:=14;
   y:=21;
   z:=11;
   a:=z+x-y;
   c:=a-y-z*y*a+x;
   WRITELN(MyMessage);
END;
