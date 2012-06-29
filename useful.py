#!/usr/bin/env python

# Copyright (C) 2012 John Chee

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

# http://stackoverflow.com/questions/10892272/union-python-dictioniaries-with-function-on-collision
def union_with(mempty, mappend, d1, d2):
  """
  Union two dictionaries applying mappend on collisions and supplying mempty on miss.

  >>> union_with([], lambda x, y: x + y, {}, {})
  {}
  >>> d1 = {'a' : [42], 'b' : [12], 'c' : [4]}
  >>> d2 = {'a' : [3], 'b' : [2], 'd' : [0]}
  >>> union_with([], lambda x, y: x + y, d1, d2)
  {'a': [42, 3], 'c': [4], 'b': [12, 2], 'd': [0]}
  >>> d1 = {'a' : [3], 'b' : [2], 'd' : [0]}
  >>> d2 = {'a' : [42], 'b' : [12], 'c' : [4]}
  >>> union_with([], lambda x, y: x + y, d1, d2)
  {'a': [3, 42], 'c': [4], 'b': [2, 12], 'd': [0]}
  >>> d1 = {'a' : 3, 'b' : 2, 'd' : 0}
  >>> d2 = {'a' : 42, 'b' : 12, 'c' : 4}
  >>> union_with(0, lambda x, y: x + y, d1, d2)
  {'a': 45, 'c': 4, 'b': 14, 'd': 0}
  """
  return {key : mappend(d1.get(key, mempty), d2.get(key, mempty)) for key in set(d1.keys() + d2.keys())}

def maybe_get(f_dict, default=None):
    """

    Executes the delayed lookup and returns default if a 'LookupError' exception is thrown during execution.

    >>> maybe_get(lambda: {"hello" : 42}["bar"]) == None
    True
    >>> maybe_get(lambda: {"hello" : 42}["hello"])
    42
    >>> maybe_get(lambda: range(0, 100)[100]) == None
    True
    >>> maybe_get(lambda: range(0, 5)[0])
    0

    You can even have arbitrary expressions that involve a lookup:
    >>> maybe_get(lambda: range(12, 20)[1] + 1)
    14

    """
    return maybe(f_dict, default, [LookupError])

def maybe(f, default=None, exceptions=[]):
    """

    Executes the delayed computation and returns default if an exception from 'exceptions' is thrown during execution.

    >>> maybe(lambda: 200/0, exceptions=[ZeroDivisionError]) == None
    True
    >>> maybe(lambda: 400/2, exceptions=[ZeroDivisionError])
    200

    """
    try:
        return f()
    except SystemExit:
        raise
    except Exception as exn:
        if any([isinstance(exn, e) for e in exceptions]):
            return default
        else:
            raise exn

def safe_shuffle(xs):
    import random

    new_xs = list(xs)
    random.shuffle(new_xs)
    return new_xs

def safe_reverse(xs):
    new_xs = list(xs)
    new_xs.reverse()
    return new_xs

# http://stackoverflow.com/questions/9766608/zipwith-analogue-in-python/9766650#9766650
def zipWith(f, xs, ys):
    map(f, xs, ys)

def repeat(n):
    """
    Return an infinite series of n's

    >>> x = repeat(42)
    >>> x.next()
    42
    >>> x.next()
    42
    """
    while True:
        yield n

def replicate(n, x):
    """
    Return 'n' 'x's as a list

    >>> replicate(-1, 'x')
    []
    >>> replicate(0, 42)
    []
    >>> replicate(1, 'a')
    ['a']
    >>> replicate(5, 1)
    [1, 1, 1, 1, 1]
    """
    return [x] * n

# http://stackoverflow.com/questions/3787908/python-determine-if-all-items-of-a-list-are-the-same-item
def all_same(items):
    """
    Are all the items in the list the same?

    >>> all_same([])
    True
    >>> all_same([42])
    True
    >>> all_same([True, False, True])
    False
    >>> all_same([True, True, True])
    True
    >>> all_same([None, None, None])
    True
    >>> all_same([None, 42, True])
    False
    """
    itemsIter = iter(items)
    i0 = maybe(lambda: itemsIter.next(), exceptions=[StopIteration])
    return all(x == i0 for x in itemsIter)

# http://stackoverflow.com/questions/4937491/matrix-transpose-in-python
def transpose(m):
    return zip(*m)

def all_nones(xs):
    """
    Is each element of 'xs' None?

    >>> all_nones([])
    True
    >>> all_nones([None, None, None])
    True
    >>> all_nones([1,2,3])
    False
    >>> all_nones([None, 1, None])
    False
    """
    return all(x == None for x in xs)

def update_list(xs, index, new_x):
    """
    Return a copy of xs with 'new_x' at index 'index'

    >>> update_list([1,2,3], -1, 42)
    [1, 2, 42]
    >>> update_list([], 2, 42)
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
    IndexError: list assignment index out of range
    >>> update_list([1,2,3], 3, 42)
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
    IndexError: list assignment index out of range
    >>> update_list([1,2,3], 2, 42)
    [1, 2, 42]
    >>> update_list([1,2,3,4,5], 0, 42)
    [42, 2, 3, 4, 5]
    """
    new_xs = list(xs)
    new_xs[index] = new_x
    return new_xs

def concat(xss):
    """
    Concatenate a list of lists

    >>> concat([])
    []
    >>> concat([[],[],[]])
    []
    >>> concat([[1,2,3], range(10,20), ['hello']])
    [1, 2, 3, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 'hello']
    """
    return reduce(lambda x1, x2: x1 + x2, xss, [])

if __name__ == '__main__':
    import doctest
    doctest.testmod()
