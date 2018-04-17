PROGRAM Greeting;

CONSTANT
x = 5;
y = 6;
z = 7;
   
VAR
   a : INTEGER;

FUNCTION MyFunc(size: INTEGER; temp: INTEGER;): INTEGER;
VAR 
MyFunc : INTEGER;
   yo  : INTEGER;
BEGIN
    MyFunc := size + 1;
   yo := MyFunc*temp + size - 8;
END;


BEGIN
   a := x + y;
   MyFunc(x,y);
END;
