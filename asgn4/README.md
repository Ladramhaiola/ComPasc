# Done:

1. Variable declaration (entry into symbol table)
2. Constant Declaration (in const section).
3. Arithematic and Boolean expressions.
4. For the else part in CASE statement, we have the constraint that it should be compound

# Doubts:

1. What do we have to do in type section?
2. Handling 'Factor' in all it's cases.
3. Is there use of doublestar? (*..* is comments)
4. What is the point of VAR/FUNC while doing symTabOp?

# To Do
- Functions:
|Feature | Status |
| ------ | ------ |
| Param list | :white_check_mark: |
| Adding Func to Parent Scope | :white_check_mark: |
| Add Func Label | :white_check_mark: |
| Arg Count Consistency| :white_check_mark: |
| Return variable consistency | :white_check_mark: |

- Misc:
1. Our current IR requires all function code to be together at the end
2. Handling Break and Continue Statements together with loop and for
3. Designator Type Checks while assignment and others operations, like AddOp and MulOp

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
| Lambda     |                  |   |
