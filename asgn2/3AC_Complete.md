
# Precise 3 AC Here

## Assignment
```
Linenumber, unary, LHS, =, VAR
```

## Unary + or -
```
Linenumber, unary, LHS, + or -, VAR
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
Linenumber, op, LHS, VAR_1, VAR_2
```
where op can be:
```
op = ['<','>','<=','>=']
```

## Conditional/Unconditional Jump
- Just fucking jump
```
Linenumber, jmp, *EMPTY* , TARGET, *EMPTY*
```
- Jump on true
```
Linenumber, jtrue, *EMPTY*, TARGET, VAR
```
- Jump on False
```
Linenumber, jfalse, *EMPTY*, TARGET, VAR
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
Linenumber,"label",*EMPTY*,Label_Name,*EMPTY*
```

## Input and Output
```

```

## Functions
```
Linenumber, "Param", *EMPTY* , ARG1, *EMPTY*
Linenumber, "Param", *EMPTY* , ARG2, *EMPTY*
Linenumber, "call", *EMPTY*, Function_name, *EMPTY*
Linenumber, "return", *EMPTY*, *EMPTY*, *EMPTY*
Linenumber, "returnval", *EMPTY*, VALUE, **EMPTY**
```
