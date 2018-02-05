
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
