
# 3 AC Specifics here:

## Intro
Would essentially use Quadruple 3 AC structure

## Assumptions
Assignments on left have all new variables, that is no overlapping identifier names
Maybe this shit helps in Basic Block Identifying

## data types
- int:
- string:
- char:
- float/double:
- array: 

## instructions and their types

- Unary: op = unary, lhs = variable to store into, op1 = '+,-, Nothing', op2 = variable with which you want to do things

- Binary: lineno,op,lhs,op1,op2
    - + : op = add
    - - : op  = sub
    - * : op = mul
    - \ : op = div
    - SHL: op = shl
    - SHR: op = shr
    - MOD: op = mod
    - OR: op = or
    - AND: op = and

- Array reference:
    - a = x[i]: lineno, op = 'loadfromarray', lhs='variable(temp here)',op1="array starting index",op2="refering index"
    - Similarly store to array required? Like x[i] = a? or model it as memory reference? But is bidirectional, might provide ease in breaking into two in asm
    - [Meeting] Good to separate it

- If statement:
    - our IR won't have if statement. We will simply have conditional jump and jump
    - lineno, op = , lhs = , op1 = , op2 = 

- Goto Statement:
    - Include conditional jumps here?

# Modelling check with above instructions

## Arithmetic
- Easy

## Labels
- Conversion of labels to line numbers. Any potential pit falls
- [Meeting] Assembly supports labels, no change required.

## if-else
- Can be modelled easily using if-goto

## while, repeat
- Have a loop condition, followed by jump stmt out of the loop, body, and update and jump back to check condition

## function calls
- Replace with a label
- Ask Sir about how we can look for arguments. Other than that can be essentially modelled as a program
- [Meeting] Give labels to functions, and the standard way for function argument IR is shown below: 
    ```
    param a
    param b
    param c
    call foo
    ```

## lambda call
- Maybe convert it to a simple function call in the IR?
[Not of concern for now]
- [Meeting] Yes, May have to keep a dict while converting to function to account for environ variables.

## Input-Output
- Ask Sir if we can directly use the interfacing provided by x86, and in turn refer it to the way we are using functions
- Yes.

## classes and objects
- Ask Sir about inheritance
- [Meeting] Classes boiled down to IR and details already exisiting in SymTable

# CODE Generation

What we need:
Register and Address descriptors
