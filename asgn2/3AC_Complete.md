
# Precise 3 AC Here

Inspired from [here](http://arantxa.ii.uam.es/~modonnel/Compilers/07_2_intermediateCodeGen-Quadruples.pdf)
Some inspiration also from [x86 syntax](http://flint.cs.yale.edu/cs421/papers/x86-asm/asm.html) 

## Assignment
```
Linenumber, unary, LHS, + or = or -, VAR
```

## Binary Arithmetic

```
Linenumber, op, LHS, VAR_1, VAR_2
```
where op is 
```
op = ['+','-','*','/','MOD','OR','AND','SHL','SHR']
```

## Comparisons

```
Linenumber, CMP, *EMPTY*, VAR_1, VAR_2
```
This directly maps with the cmp instruction present in x86.


## Jumps

```
Linenumber, jcondition, *EMPTY*, TARGET, *EMPTY*
```
where
```
jcondition = [JMP,JE,JNE,JZ,JG,JL,JGE,JLE]
```


## Memory reference
- Load from mem
for cases like: x = a[i]
```
Linenumber,"LOADREF", LHS, Array_start, Index_to_access
```

- Store to mem
for cases like a[i] = x
```
Linenumber,"STOREREF", Array_start, Index_to_access, To_store_from
```

## Labels
If Function Label, put FUNC in third argument
```
Linenumber, "LABEL", *EMPTY*/FUNC, Label_Name, *EMPTY*
```

## Input and Output
- Input
```
Linenumber, "SCAN", *lhs*, *EMPTY*, *EMPTY* 
```
- Print
```
Linenumber, "PRINT", *EMPTY*, MESSAGE, *EMPTY* 
```

## Functions
We'll follow cdecl standard function param pushing
parse from right to left, so that param 1 is top of the stack
In the return label, if the return is of function Func_Name, enter Func_Name as last argument
```
Linenumber, "PARAM", *EMPTY* , ARG2, *EMPTY*
Linenumber, "CALL", *EMPTY*, Function_name, *EMPTY*
Linenumber, "RETURN", *EMPTY*, *EMPTY*, *EMPTY*/Func_Name
Linenumber, "RETURNVAL", *EMPTY*, VALUE, **EMPTY**
```
