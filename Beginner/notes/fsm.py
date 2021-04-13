''' The regex 'a[^aeiou]c?d( )*e' generates complex code (compilation).
    That jumps between states, doesn't remember its history,
    and returns very little information:  True or False.
    In the case that is True, we also know the position of
    the start and end.

     a b c d e f h i j k l m n
0:  [1 0 0 0 0 0 0 0 0 0 0 0 0]
1:  [0 2 2 2 0 2 2 0 2 2 2 2 2]  
2:  [0 0 3 4 0 0 0 0 0 0 0 0 0]

    while state != final:
          c = next(it)
          state = table[state][c]


'''

def match(s):
    i = -1
    it = iter(s)
    state = 0
    while True:
        try:
            c = next(it)
            i += 1
        except StopIteration:
            return False
        if state == 0:
            if c == 'a':
                start = i
                state = 1
            else:
                state = 0
        elif state == 1:
            if c not in {'a', 'e', 'i', 'o', 'u'}:
                state = 2
            else:
                state = 0
        elif state == 2:
            if c == 'c':
                state = 3
            elif c == 'd':
                state = 4
            else:
                state = 0 
        elif state == 3:
            if c == 'd':
                state = 4
            else:
                state = 0            
        elif state == 4:
            if c == ' ':
                state = 4
            else:
                state = 5
        elif state == 5:
            if c == 'e':
                end = i
                return True, (start, end)
            else:
                state = 0
        else:
            return False
    
