PROGRAM Greeting;

VAR 
x, y, z, a: INTEGER; 
height, width : INTEGER; 
c: CHAR;

CONSTANT
x = 5;
y = 6;
z = 7;
   
TYPE
   a1 = ARRAY[x..10,y..10,z..10] OF INTEGER;

FUNCTION MyFunc(size: INTEGER);
BEGIN
    size := size + 1;
END;


BEGIN

   height = x + y * z * MyFunc(x);

END;
