# Done:

1. Variable declaration (entry into symbol table)
2. Constant Declaration (in const section).
3. Arithematic and Boolean expressions.
4. For the else part in CASE statement, we have the constraint that it should be compound

# Doubts:

1. What do we have to do in type section?
2. Handling 'Factor' in all it's cases.
3. Handling arrays in RHS.(Done, need to test)
4. Is there use of doublestar? (*..* is comments)

# To Do
- Functions:
1. Param list
2. Adding in Symbol Table check
3. Label statement with Func

- Multi-dimensional arrays

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
