
# Precise 3 AC Here

Inspired from [here](http://arantxa.ii.uam.es/~modonnel/Compilers/07_2_intermediateCodeGen-Quadruples.pdf)

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
Linenumber, cmp, *EMPTY*, VAR_1, VAR_2
```
This directly maps with the cmp instruction present in x86.


## Unconditional Jump

``` 
Linenumber, jmp, *EMPTY* , TARGET, *EMPTY*
```

## Conditional Jumps

```
Linenumber, jcondition, *EMPTY*, TARGET, *EMPTY*
```
where
```
jcondition = [je,jne,jz,jg,jl,jge,jle]
```


## Memory reference
- Load from mem
for cases like: x = a[i]
```
Linenumber,"loadref", LHS, Array_start, Index_to_access
```

- Store to mem
for cases like a[i] = x
```
Linenumber,"storeref", Array_start, Index_to_access, To_store_from
```

## Labels
```
Linenumber, "label", *EMPTY*, Label_Name, *EMPTY*
```

## Input and Output
- Print
```
Linenumber, "print", *EMPTY*, MESSAGE, *EMPTY* 
```

## Functions
We'll follow cdecl standard function param pushing
parse from right to left, so that param 1 is top of the stack
```
Linenumber, "Param", *EMPTY* , ARG2, *EMPTY*
Linenumber, "call", *EMPTY*, Function_name, *EMPTY*
Linenumber, "return", *EMPTY*, *EMPTY*, *EMPTY*
Linenumber, "returnval", *EMPTY*, VALUE, **EMPTY**
```
