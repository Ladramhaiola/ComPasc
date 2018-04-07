- Misc:
    1. Our current IR requires all function code to be together at the end
    2. Designator Type Checks while assignment and others operations, like AddOp and MulOp
    3. Functon calls in Factor (return value to be assigned to a temporary)
    4. Pointer Arithematic (define unary operations (\* and &) and enforce checks on arithematic)
    5. Symbol Table for Objects and classes 
    6. Floats (in the end)
    7. What do we have to do in type section?
    8. offsets stack (for functions)

# Testing

|    Feature | IR | Assembly |
| ---------- |----| -------- |
| Arithmetic |:white_check_mark:|:white_check_mark:|
| LoadRef    |:white_check_mark:|   |
| StoreRef   |:white_check_mark:|   |
| If-Else    |:white_check_mark:|   |
| Case       |:white_check_mark:|   |
| While      |:white_check_mark:|   |
| Repeat     |:white_check_mark:|   |
| Lambda     |                  |   |
