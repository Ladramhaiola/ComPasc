PROGRAM Greeting;

CONSTANT
x = 5;
y = 6;
z = 7;
   
VAR
   a : INTEGER;
   b : INTEGER;

FUNCTION MyFunc(size: INTEGER; temp: INTEGER;): INTEGER;
VAR 
MyFunc : INTEGER;
   yo  : INTEGER;
BEGIN
    yo := size + 1; // yo = 6
    MyFunc := yo*temp + size - 8; // MyFunc = 33
END;


BEGIN
   a := x + y; //a = 11
   b := MyFunc(x,y); //b should be 33 here
   WRITELN(b);
END;
