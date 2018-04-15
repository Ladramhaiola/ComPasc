PROGRAM Greeting;

CONSTANT
x = 5;
y = 6;
z = 7;
   

FUNCTION MyFunc(size: INTEGER; temp: INTEGER;): INTEGER;
VAR 
MyFunc	      : INTEGER; 
BEGIN
    MyFunc := size + 1;
END;


BEGIN
   MyFunc(x,y);
END;
