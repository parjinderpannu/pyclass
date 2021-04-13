'Complete analysis of the Kaprekar process'
# https://en.wikipedia.org/wiki/6174_(number)

def kap(n):
    '''compute one step in the Kaprekar process

    >>> kap('3524')
    '3087'
    >>> kap('0027')
    '7173'
    >>> kap('8352')
    '6174'
    >>> kap('6174')
    '6174'
    >>> kap('0001')
    '0999'
    '''
    big = int(''.join(sorted(n, reverse=True)))
    small = int(''.join(sorted(n)))
    return '%04d' % (big - small)


def gen_graph():
    ''' Perform a graphical analysis of the kap function into a graphviz format.
        Build the graph like this:

        $ python3 kap.py | dot -Tsvg > kap.svg
    '''

    #1 Convert data to a convenient form for analysis
    kapdict = {}
    for i in range(10000):
        kapdict['%04d' % i] = kap('%04d' % i)

    #2 Analyze the data
    rests = set(kapdict.values())
    firsts = set(kapdict) - rests

    groupdict = {}
    for i in firsts:
        tgt = kap(i)
        groupdict.setdefault(tgt, []).append(i)

    #3 Format the output
    print('''\
    digraph {
    graph [rankdir=LR];
    edge [color=blue, fontcolor=blue, fontsize=10]
    ''')
    for tgt in rests:
        print('    %s -> %s;' % (tgt, kapdict[tgt]))

    print('node [shape=rectangle];')
    for tgt, group in groupdict.items():
         block = ', '.join(group[:3])
         print('"%s, ..." -> %s [label=%d];' % (block, tgt, len(group)))
    print('}')


if __name__ == '__main__':
    import doctest
    doctest.testmod()

    gen_graph()


'''Advice on code building.

Build interactively with global variables
and then move into a function with doctrings.

Test as you go and LOOK at your data:
1) type  2) size  3) convert to list and slice
Only use human eyes to gaze upon sorted data

Slip into three sections:
1) Convert data to a convenient form
2) Analyze the data
3) Format the output
'''
