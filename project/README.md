One major assumption in Assignment2 : SymbolTable contains entries for temporaries as well

- To do in codegen:
  1. Improve the code in handle_binary (and hence rest of similar functions)
  2. See if you can integrate the project
  3. Functions
  4. Objects and classes (both in semantics and codegen)

- Misc:
    1. Our current IR requires all function code to be together at the end
    2. Designator Type Checks while assignment and others operations, like AddOp and MulOp
    3. NOT relational operator not working fine
    4. Pointer Arithematic (define unary operations (\* and &) and enforce checks on arithematic)
    5. Symbol Table for Objects and classes 
    6. Floats (in the end)
    7. What do we have to do in type section?
    8. offsets stack (for functions)

# A monologue on Functions

Remember: Stack grows down.
The task is set out in briefly three phases: Before, After Entry, and Before Exit

## Before :white_check_mark:
```
push arg_3
push arg_2
push arg_1
call MyFunc
add esp, #Number of Bytes
```
The last line is needed to get the stack back to its original state.

## Entry Seq

```
push ebp
mov ebp,esp
```
Move the current stack pointer to the base pointer. This indicates the beggining of new stack

## Accessing the elements
The stack curretly has ebp and then return address. Therefore, to access the first pushed parameter on the stack, we do:
```
mov ebp+8, a
```
and so on. It will only start after ebp+8 because 4 and 0 are occupied by return address and pushed ebp

## Exit Sequence :white_check_mark:
```
mov esp,ebp
pop ebp
ret
```
The first line(moving ebp to esp) ensures that stack pointer points to the top of this frame. Pop the ebp. Then do ret, it takes the return address present on the stack and returns back.



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
