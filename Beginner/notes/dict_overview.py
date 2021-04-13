'''
Dicts are used everywhere in Python. They are of central importance:

    * Modules have a dictionary
    * Classes have a dictionary
    * Instances have a dictionary
    * globals() is a dictionary
    * locals() is a dictionary
    * users can make a dictionary

People who use dictionaries to reason about problems
typically shorter, faster, clearer code and can solve
really hard problems.

Metaphor or analogy or visualization using a Real Dictionary of English

O.E.D. -- Huge dict of English > 300,000 words

Key        -> Value
Word       -> Definition
Nonplussed -> Stunned into submission, not knowing how to react.

Dictionaries have directionality.  They arranged for fast lookup from key to value.
You COULD do a reverse lookup but that would entail a slow, page-by-page, linear search which is O(n).

Gobsmacked -> Stunned into submission, not knowing how to react.

Dicts have unique keys but may have duplicated values.
This is another reason not to reverse lookups, you could have many matches.

Nonplussed -> Thrown for a loop.

You can change the value for a given key at any time without reordering the dictionary.

Dizzified -> Stunned into submission, not knowing how to react.

If keys could be mutated, they would become unfindable.
If you could change both the key and the value, all concept of identity is lost.

Rachel S -> wife
Rachel H -> wife
You can have more than one key pointing to the value.

Dicts require immutable keys for findability and for identity:

    Mutable:    list        set         dict
    Immutable:  int    float   complex   bool    str   unicode   None   tuple

Covfefe --> goes in the "C" range so that people can find it.
    dicts are called "unordered collections" -- they don't remember insertion order
        that said, internally, they are highly ordered for fast lookup
    Real dictionaries are ordered alphabetically.  Lookup strategy:  bisection     Speed:  O(log n)
    Python dictionaries are ordered by hash value. Lookup strategy:  hashing       Speed:  O(1)

Video for how it works internally:
    https://www.youtube.com/watch?v=npw4s1QTmPg

What order dictionaries display in:
    * Python 2.7, we use a single unchanging hash function.  The order is arbitrary but fixed across runs.
    * Python 3.5, we use a randomized hash function.  The order is fully random but fixed within a single run.
    * Python 3.6. the hash is still randomized but dicts display in insertion order.

In computer school, what they are SUPPOSED to teach:
    * O(1) hashing beats O(log n) binary search which beats O(n) linear search.

'''

from pprint import pprint

print('How to make compound keys:')
pref = {}
pref['raymond', 'hettinger'] = 'red'
pref['rachel', 'hettinger'] = 'blue'
pref['raymond', 'romano'] = 'orange'
pref['rachel', 'ray'] = 'green'
pprint(pref, width=30)

print('\nForward lookups are fast, easy, and clear with regular dict:')
e2s = dict(one='uno', two='dos', three='tres', four='cuatro', five='cinco')
pprint(e2s, width=20)

print('\nForward lookup:')
eng = 'three'
print(eng, '-->', e2s[eng])

print('\nReverse lookup:')
span = 'cuatro'
for e, s in e2s.items():
    if s == span:
        print(s, '-->', e)

print('\nMultiple reverse lookups -- The slow way')
span_words = ['cuatro', 'cuatro', 'uno', 'tres', 'dos', 'tres', 'dos']
for span in span_words:
    for e, s in e2s.items():
        if s == span:
            print(s, '-->', e)

print('\nHow to reverse a dictionary -- Simple case of a bijection (one-to-one and onto)')
s2e = {}
for e, s in e2s.items():
    s2e[s] = e
pprint(s2e, width=20)

print('\nMultiple reverse lookups -- The fast way')
for span in span_words:
    print(span, '-->', s2e[span])

print('\nHow to model a one to many mapping')
print('The "one" is the scalar key')
print('The "many" is collection of values')

e2s = dict(
    one = ['uno'],
    two = ['dos'],
    three = ['tres'],
    four = ['cuatro'],
    five = ['cinco'],
    trio = ['tres'],
    free = ['libre', 'gratis'],
)
pprint(e2s)

print('\nShow every possible pairing of an English word with Spanish')
print('This is flattening')
for eng, span_words in e2s.items():
    for span in span_words:
        print(eng, '-->', span)

print('\nHow to reverse a one-to-mapping -- In wordy way')
s2e = {}
for eng, span_words in e2s.items():
    for span in span_words:
        if span not in s2e:
            s2e[span] = []
        s2e[span].append(eng)
pprint(s2e)

# Patterns of doing unconditional lookups:
# d.get(k, default) -> d[k] if k in d else default             No side-effect.
# d.pop(k, default) -> d[k] if k in d else default             Side-effect: removes existing keys
# d.setdefault(k, default) -> d[k] if k in d else default      Side-effect: adds missing keys and the default

print('\nHow to reverse a one-to-mapping -- In a beautiful and elegant way')
s2e = {}
for eng, span_words in e2s.items():
    for span in span_words:
        s2e.setdefault(span, []).append(eng)
pprint(s2e)

#########################################################
# Grouping by using a one-to-mapping
# The key to the dict is called a "feature"
# The value will be a collection of elements with that feature

# lists: are ordered and allows duplicates                          s.append(e)
# sets:  are unordered and eliminate duplicates                     s.add(e)
# Counter: is like a set but it counts duplicates                   s[e] += 1
# deques: are ordered, allow duplicates, and are doubled-end        s.append(e) or s.appendleft(e)

names = ''' raymond rachel matthew tom bill david susan roger
            shelly jack rodney amber sheila bob dave rachel
            bob sue adam sue mary habib drew timothy tom
            janet hank matt amber
'''.split()
pprint(names)

print('\nTask 1:  Group names by the length of the name preserving order and with duplicates')
d = {}
for name in names:
    feature = len(name)
    d.setdefault(feature, []).append(name)
pprint(d)

print('\nTask 2:  Group names by the first letter of the name and eliminate the duplicates')
d = {}
for name in names:
    feature = name[0]
    d.setdefault(feature, set()).add(name)
pprint(d)

print('\nTask 3:  Group names by the last letter of the name while preserving order and counting duplicates')
from collections import Counter
d = {}
for name in names:
    feature = name[-1]
    d.setdefault(feature, Counter())[name] += 1
pprint(d)

print('\nTask 4:  Group name by the number of vowels "aeiouy" putting the newest names first')
from collections import deque
d = {}
for name in names:
    feature = sum([name.count(vowel) for vowel in 'aeiouy'])
    d.setdefault(feature, deque()).appendleft(name)
pprint(d, width=240)


