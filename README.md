# Pyregex

A user-hostile regex engine in Python with a really simple syntax. Uses backtracking for epsilon transitions instead of guessing options concurrently, so it's rather inefficient. Written for educational purposes over a weekend, so it's just for laff.

## Construction:

Takes as input a regex in normal infix notation and uses [Dijkstra's shunting yard algorithm](http://en.wikipedia.org/wiki/Shunting-yard_algorithm) to convert it into its equivalent parseable reverse Polish notation. Once converted to RPN, the expression is parsed and used to construct a non-deterministic finite automaton with [Thompson's construction algorithm](http://en.wikipedia.org/wiki/Thompson%27s_construction_algorithm) from the partial NFAs as described [here](http://swtch.com/~rsc/regexp/regexp1.html).

## Usage:

`main.py` is the main entry point of the program and takes two command line args, a pattern and a string to match against, in the order. (see `main.py -h`)

Requires . for explicit concatenation in the pattern for now.

### Examples:

```
$ ./main.py 'a.b' 'ab'
True

$ ./main.py 'ab' 'ab'
False    //  ^ should've been a.b

$ ./main.py '((a.a)*.(b.b)*)*' 'aabb'
True

$ ./main.py '(D.o.e.s. .t.h.i.s. .w.o.r.k)?.(n.o)?.(y.e.s)?' 'no'
True

$ ./main.py '(a.b).(a|b)' 'aba'
True
```


## Supported operators:
* `?` - One or zero
* `*` - Zero or many
* `+` - One or many
* `|` - Alternation (ie. `match('a|b', 'a') and match('a|b', 'b') == True`).
