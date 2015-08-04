#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''@package py
Python Cookbook

  - Testing
  - Memory-Mapped File
  - Network
  - Thread
  - Django (Web framework)
  

## Command Line Options

    `-t`  Issue a warning when a source file mixes tabs and spaces for indentation in a way that
          makes it depend on the worth of a tab expressed in spaces.
        
    `-tt` Issue a error when a source file mixes tabs and spaces for indentation in a way that
          makes it depend on the worth of a tab expressed in spaces.
        
    `-O`  Turn on basic optimizations. This changes the file name extension for compiled (bytecode)
          files from *.pyc* to *.pyo*, and set the `__debug__` to `False`.
       
    `-OO` Discard docstrings in addition to the <em>-O</em> optimizations.

    


## Virtual Running Environment

```bash
# Create
sudo apt-get install python-virtualenv
virtualenv env-dir
cd env-dir

# Active
source bin/activate
```


## PEP

  - [PEP 257 - Docstring Conventions](http://legacy.python.org/dev/peps/pep-0257/)
  - [PEP 440 - Version Identification and Dependency Specification](http://legacy.python.org/dev/peps/pep-0440/)
  

## References

  - Core Python Applications Programming, 3rd Edition (2012)
  
      
Copyright (c) 2014 Li Yun <leven.cn@gmail.com>
All Rights Reserved.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
ARE DISCLAIMED.  IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
POSSIBILITY OF SUCH DAMAGE.
'''

def loop():
    '''Loop technique.
    @see zip()
    @see itertools
    '''
    seq = [1, 2, 3]
    seq2 = ['a', 'b']
    start_index = 1
    seq_tmp = []   

    # Iterator/Generator Slicing
    #
    # **NOTE**: It’s important to emphasize that `islice()` will consume data
    # on the supplied iterator. Since iterators can’t be rewound, that is
    # something to consider. If it’s important to go back, you should probably
    # just turn the data into a list first.
    for item in itertools.islice(my_generator(0), 5, 9):
        assert item in [5 ,6 ,7, 8]
        
    # Permutations & Combinations
    for item in itertools.permutations(seq):
        assert item in (
            (1, 2, 3),
            (1, 3, 2),
            (2, 1, 3),
            (2, 3, 1),
            (3, 1, 2),
            (3, 2, 1)
        )
    for item in itertools.permutations(seq, 2):
        assert item in (
            (1, 2),
            (1, 3),
            (2, 1),
            (2, 3),
            (3, 1),
            (3, 2)
        )
    for item in itertools.combinations(seq, 3):
        assert item in (
            (1, 2, 3),
        )
    for item in itertools.combinations(seq, 2):
        assert item in (
            (1, 2),
            (1, 3),
            (2, 3)
        )
    for item in itertools.combinations_with_replacement(seq, 3):
        assert item in (
            (1, 1, 1),
            (1, 1, 2),
            (1, 1, 3),
            (1, 2, 2),
            (1, 2, 3),
            (1, 3, 3),
            (2, 2, 2),
            (2, 2, 3),
            (2, 3, 3),
            (3, 3, 3)
        )
        
    # The easiest way to filter a sequence data is often to use a list (or
    # dictionary, tuple, etc.) comprehension.
    l = [1, 3, 5, -2, 0, 8]
    assert [i for i in l if i > 0] == [1, 3, 5, 8]
    assert [i if i > 0 else 0 for i in l] == [1, 3, 5, 0, 0, 8]
    d = {'A': 1, 'B': 2, 'C': 3}
    assert {key: value for key, value in d.items() if value > 1} == \
            {'B': 2, 'C': 3}  # Python 2: d.iteritems()
            
    # One potential downside of using a list comprehension is that it might
    # produce a large result if the original input is large. If this is a
    # concern, generator expression could be used to produce the filtered
    # values iteratively.
    for i in (i for i in l if i > 0):
        pass
        
    # Sometimes, the filtering criteria cannot be easily expressed in a list
    # comprehension or generator expression. For example, suppose that the
    # filtering process involves exception handling or some other complicated
    # detail.
    #
    # NOTE: the `filter()` returns a list in python 2, and an iterable in
    # Python 3.
    def is_int(val):
        try:
            int(val)
            return True
        except ValueError:
            return False
    assert list(filter(is_int, ['1', '-', '2', 'N/A', '-'])) == ['1', '2']
    
        
def file_io(filename):
    '''File I/O.
    
    The I/O system is built from layers. Text files are constructed by adding a
    text encoding/decoding layer on top of a buffered binary-mode file. The
    `buffer` attribute simply points at this underlying file. If you access it,
    you’ll bypass the text encoding/decoding layer. You could write raw bytes to
    a file opened in text mode using this technique.
    '''
        
    # Read fixed-size data directly into buffer without intermediate copying.
    #
    # Unlike `read()` method, `readinto()` method doesn't need to allocate new
    # objects and return them, avoiding making extra memory allocations.
    import functools
    size = 2
    buf = bytearray(size)
    try:
        with open(filename, 'rb') as f:
            for nbytes in iter(functools.partial(f.readinto, buf), 0):
                print(nbytes, buf)
    except IOError as err:
        print(err)
        
    # Read var-size binary file.
    try:
        with open(filename, 'rb') as f:
            print(f.read(2))
            print(f.read(6))
    except IOError as err:
        print(err)
     
                
def context_manager():
    '''Context Manager.

    @see contextlib
    '''
    # contextlib.suppress(*exception)
    #
    # Replace `try-except-pass`:
    #
    #     try:
    #         os.remove('not-exists')
    #     except FileNotFoundError:
    #         pass
    #
    # **NOTE**: This context manager is *reentrant*.
    # @since Python 3.4
    from contextlib import suppress
    import os
    with suppress(FileNotFoundError):
        os.remove('not-exists')
                
            
    # contextlib.ExitStack
    #
    # Replace `try-finally`:
    #
    #     cleanup_needed = True
    #     def do():
    #         return False
    #     def cleanup():
    #         pass
    #     try:
    #         result = do()
    #         if result:
    #             cleanup_needed = False
    #     finally:
    #         if cleanup_needed:
    #             cleanup()
    #
    # @since Python 3.3
    from contextlib import ExitStack
    def do():
        return False
    def cleanup():
        pass
    with ExitStack() as stack:
        stack.callback(cleanup)
        result = do()
        if result:
            stack.pop_all()
            
    # contextlib.redirect_stdout(new_file)
    #
    # **NOTE**: This context manager is *reusable* but *not reentrant*.
    # @since Python 3.4
    from contextlib import redirect_stdout
    import io
    f = io.StringIO()
    with redirect_stdout(f):
        help(io)
    s = f.getvalue()
    
    
def re_pattern():
    '''Regular Expression (RE) pattern.
    
    re1|re2 - or
    re1.re2 - any character except `\n`
    ^str - start of string
    str$ - end of string
    re* - 0+ occurrences
    re+ - 1+ occurrences
    re? - 0 or 1 occurrences
    re{N} - N occurrences
    re{M,N} - from M to N occurrences
    [...] - any single character from character set
    [x-y] - any single character from x to y
    [^...] - NOT any character from character set
    (...) - subgroup
    
    \d - digit, `[0-9]`
    \D - NOT digit, `[^0-9]`
    \w - alphanumeric character, `[A-Za-z0-9_]`
    \W - NOT alphanumeric character, `[^A-Za-z0-9_]`
    \s - white space, `[ \n\t\r\v\f]`
    \S - NOT white space, `[^ \n\t\r\v\f]`
    \bword\b - word boundary
    \A - ^
    \Z - $
    
    @see re    
    '''
    import re
    
    # Compile pattern object
    pattern = re.compile(r'patern-string')
    
    # Get match object
    match = pattern.match('string')          # Search from beginning
    match = pattern.search('string')         # Search until end

    # Get match object list with scanning the whole string
    match_list = pattern.findall('string')

    # Loop over a iterator with scanning the whole string
    for match in pattern.finditer('string'): 
        # handle match
        pass
    
    # Handle match object
    if match is not None:          # Match found
        result = match.group()     # string
        pos_start = match.start()  # int
        pos_end = match.end()      # int
        pos = match.span()         # tuple: (pos_start, pos_end)
    else:
        # Not match
        pass
    
    # Search and replace with strings
    # repl_tuple = (repl_str, count)
    repl_str = pattern.sub('replacement', 'origin', count=0)
    repl_tuple = pattern.subn('replacement', 'origin', count=0)
    
    # Search and replace with strings returned by functions
    def repl_func(match_obj):
        if match_obj.group() == 'something':
            return 'string 1'
        else:
            return 'string 2'
    repl_str = pattern.sub(repl_func, 'string', count=0)
    repl_tuple = pattern.subn(repl_func, 'string', count=0)    

    # Split strings on any of multiple delimiters
    #
    # **NOTE**: When using `re.split()`, you need to be a bit careful should
    # the regular expression pattern involve a capture group enclosed in
    # parentheses. If capture groups are used, then the matched text is also
    # included in the result.
    s = 'a b; cd, efg,hijkl,     mn'
    assert re.split(r'[;,\s]\s*', s) == ['a','b','cd','efg','hijkl','mn']
    assert re.split(r'(;|,|\s)\s*', s) == \
            ['a',' ','b',';','cd',',','efg',',','hijkl',',','mn']
    assert re.split(r'(?:;|,|\s)\s*', s) == ['a','b','cd','efg','hijkl','mn']
    
    
def shell_pattern():
    '''Shell-style wildcards pattern matching.
    
    Pattern | Meaning
    ---------------------------------------------
    *       | matches everything
    ---------------------------------------------
    ?       | matches any single character
    ---------------------------------------------
    [seq]   | matches any character in _seq_
    ---------------------------------------------
    [!seq]  | matches any character not in _seq_
    ---------------------------------------------
    
    For a literal match, wrap the meta-characters in brackets. Note that the
    filename separator ('/' on Unix) is not special to `fnmatch` module.
    
    Unlike `fnmatch.fnmatch()`, `glob` module treats file names beginning with
    a dot (.) as special cases.
    
    **NOTE**: The matching performed by `fnmatch` module sits somewhere
    between the functionality of simple string methods, such as
    `startswith()`, `endswith()`, and the full power of regular expressions.
    If you're just trying to provide a simple mechanism for allowing wildcards
    in data processing operations, it's often a reasonable solution.
    '''
    import fnmatch
    #import glob
    import os
    
    assert fnmatch.fnmatch('aaa.txt', '*.txt') == True
    assert fnmatch.fnmatch('aaa.txt', '?aa.txt') == True

    if os.name == 'posix': # On POSIX
        assert fnmatch.fnmatch('aaa.txt', '*.TXT') == False
    elif os.name == 'nt': # On Windows
        assert fnmatch.fnmatch('aaa.txt', '*.TXT') == True
        
    # Both POSIX and Windows (Case-insensitive)
    assert fnmatch.fnmatchcase('aaa.txt', '*.TXT') == False
    
    # Filter
    assert fnmatch.filter(['a.txt','b.txt', 'c.log'], '*.txt') == \
            ['a.txt','b.txt']
            
            
def sort_algorithm():
    '''Sort Algorithms.
    
    The reference implementation of `operator.itemgetter()`:

        def itemgetter(*items):
            if len(items) == 1:
                item = items[0]
                def g(obj):
                    return obj[item]
            else:
                def g(obj):
                    return tuple(obj[item] for item in items)
            return g
            
    The reference implementation of `operator.attrgetter()`:

        def attrgetter(*items):
            if len(items) == 1:
                attr = items[0]
                def g(obj):
                    return resolve_attr(obj, attr)
            else:
                def g(obj):
                    return tuple(resolve_attr(obj, attr) for attr in items)
            return g
        def resolve_attr(obj, attr):
            for name in attr.split("."):
                obj = getattr(obj, name)
            return obj
        
    @see sorted()
    @see operator.itemgetter()
    @see operator.attrgetter()
    '''
    import operator

    d = [
        {'name': 'b', 'value': 3},
        {'name': 'a', 'value': 2},
        {'name': 'c', 'value': 1}
    ]

    # Sort a list of dictionaries by name
    assert sorted(d, key=operator.itemgetter('name')) == [
        {'name': 'a', 'value': 2},
        {'name': 'b', 'value': 3},
        {'name': 'c', 'value': 1}
    ]

    # Sort a list of dictionaries by value
    assert sorted(d, key=operator.itemgetter('value')) == [
        {'name': 'c', 'value': 1},
        {'name': 'a', 'value': 2},
        {'name': 'b', 'value': 3}
    ]

    # Sort a list of dictionaries by two keys
    d = [
        {'name': 'b', 'v': 3, 'v2': 2},
        {'name': 'a', 'v': 3, 'v2': 1},
        {'name': 'c', 'v': 2, 'v2': 3}
    ]

    assert sorted(d, key=operator.itemgetter('v', 'v2')) == [
        {'name': 'c', 'v': 2, 'v2': 3},
        {'name': 'a', 'v': 3, 'v2': 1},
        {'name': 'b', 'v': 3, 'v2': 2}
    ]

    # Sort objects without native comparison support 
    class App:
        def __init__(self, id):
            self.id = id
    apps = [App(1), App(2), App(3)]
    assert sorted(apps, key=operator.attrgetter('id'))
    
    
def search_algorithm():
    '''Find the largest or smallest N items in a collection.

    **NOTE**: If you are looking for the _N_ smallest or largest items, and _N_
    is small compared to the overall size of the collection, the `nsmallest()`
    and `nlargest()` methods of `heapq` module provide superior performance.

    For larger _N_, it is more efficient to use the `sorted()` function first,
    and take a slice. Also, when `N==1`, it is more efficient to use the
    built-in `min()` and `max()` functions.

    **NOTE**: When doing these calculations, be aware that `zip()` creates an
    iterator that can only consumed once.
    '''
    import heapq

    # Find in a list of integers
    seq = [1, 8, 2, 23, 7, -2, 18, 23, 42, 37, 2]
    assert heapq.nlargest(3, seq) == [42, 37, 23]
    assert heapq.nsmallest(3, seq) == [-2, 1, 2]

    # Find in a list of dictionaries
    list_of_dict = [
        {'name': 'IBM', 'shares': 100, 'price': 91.1},
        {'name': 'AAPL', 'shares': 50, 'price': 543.22},
        {'name': 'FB', 'shares': 200, 'price': 21.09},
        {'name': 'HPQ', 'shares': 35, 'price': 31.74},
        {'name': 'YHOO', 'shares': 45, 'price': 16.35},
        {'name':'ACME', 'shares': 75, 'price': 115.65}
    ]
    assert heapq.nsmallest(3, list_of_dict, key=lambda s: s['price']) == [
            {'name': 'YHOO', 'shares': 45, 'price': 16.35},
            {'name': 'FB', 'shares': 200, 'price': 21.09},
            {'name': 'HPQ', 'shares': 35, 'price': 31.74}
        ]
            
    # Find in a dictionary
    d = {
        'IBM': 91.1,
        'AAPL': 543.22,
        'FB': 21.09
    }
    assert min(zip(d.values(), d.keys())) == (21.09, 'FB')
    assert max(zip(d.values(), d.keys())) == (543.22, 'AAPL')

    # Order a list as a heap, transformed in-place, in linear time
    heapq.heapify(seq)

    # Pop and return the smallest item from the heap, maintaining the heap
    # invariant.
    try:
        assert heapq.heappop(seq) == -2
    except IndexError as e:
        # Heap is empty
        pass
    

if __name__ == '__main__':
    import sys
    if len(sys.argv) != 1 and sys.argv[1] == 'install-python':
        # Install Python 3
        import subprocess
        subprocess.check_call('sudo apt-get update', shell=True)
        subprocess.check_call('sudo apt-get install \
                python3 python3-pip python3-dev build-essential', shell=True)
        subprocess.check_call('sudo pip3 install --upgrade virtualenv',
                shell=True)
    print('Hello Python!')
    
    context_manager()
    
    # Text Pattern
    re_pattern()
    shell_pattern()
    
    # Sort & Search Algorithms
    sort_algorithm()
    search_algorithm()

# Django Form
#
# <form action="{% url 'polls:vote' question.id %}" method="post">
# {% csrf_token %}
# {% for choice in question.choice_set.all %}
#    <input type="radio" name="choice" id="choice{{ forloop.counter }}" value="{{ choice.id }}" />
#    <label for="choice{{ forloop.counter }}">{{ choice.choice_text }}</label><br />
# {% endfor %}
# <input type="submit" value="Vote" />
# </form>
