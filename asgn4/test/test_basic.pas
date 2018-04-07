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

BEGIN

   SCAN(a);
   a1[7,8,9]:=a1[6,7,8]-"YO";

END;
