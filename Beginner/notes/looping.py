'''Learning how to loop in python'''

#include <stdio.h>
# int i;
#
# int main(void) {
#    for (i=0; i<10; i++)
#        printf("%d\n", i);
# }


# for (i=0; i<10; i++)
#     print("%d\n", i)


'''
for i in [4, 1, 3, 2]:
 |  |  |____________|
 |   \--------|--------\
 |            |         |
foreach [4, 1, 3, 2] as i do:
'''


# The following is an idiom to count 10 times
for i in range(10):  # foreach i in [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    print(i)


############################

# for (i=0; i<10; i++)
#     print("%d\n", i)
#     print("%d\n", i)

# For makes an implicit assigment:  i = next(it)
for i in range(10):  # foreach i in [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    print(i)  # iterator  -----------^
    print(i)


############################

# for (i=0; i<10; i++) {
#     print("%d\n", i);
#     i = 5; }  #  0  6  6  6  6  6  6  6 ...
# print("%d\n", i);

# Iterator has the state, not i. i is reassigned each time.
# For makes an implicit assigment:  i = next(it)
for i in range(10):  # foreach i in [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    print(i)  # iterator  -----------^
    i = 5;
print(i)


# For implicitely creates and manages an iterator to keep the
# looping state
class range2:
    '''Show how iterables work

    >>> iterable = range2(2)
    >>> it = iter(iterable)
    >>> next(it)
    0
    >>> next(it)
    1
    >>> next(it)
    Traceback (most recent call last):
    ...
    StopIteration
    '''

    def __init__(self, stop):
        self.counter = -1
        self.stop = stop

    def __iter__(self):
        return self

    def __next__(self):
        self.counter += 1
        if self.counter >= self.stop:
            raise StopIteration
        return self.counter
