Program TestObjects;
 
Type
   DrawingObject = Object
      x, y : INTEGER;
      height, width : INTEGER;       // replaced 'single' by 'integer' for now
   end;
 
Var
  Rectangle : DrawingObject;
   x, y	    :  INTEGER;

begin
 
  Rectangle.x:= 50;  //  the fields specific to the variable "Rectangle"
  Rectangle.y:= 100;
  Rectangle.width:= 40;
  Rectangle.height:= 40;
   x := Rectangle.x + Rectangle.y;
   WRITELN(x);
   
end;
