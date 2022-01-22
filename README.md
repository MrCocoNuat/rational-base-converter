# rational-base-converter
CLI utility to convert rational numbers from one rational base to another rational base

Examples:

```
$ python base.py 2102 -i=3/2
11
$ python base.py -o=16 154298
25ABA
$ python base.py -i=1 11111111
8
$ python base.py -i=5/3 1423.12 -o=7/6
6543210531525134431454126031052363531223066/6543216426303566530223
```

Usage:

Converts `NUMBER` from rational `INPUT_BASE` to rational `OUTPUT_BASE`

`$ python base.py NUMBER [OPTIONS]`

`-i=INPUT_BASE`, default `10`

`-o=OUTPUT_BASE`, default `10`

`-a=ALPHABET`, default `0123456789ABCDEFGHIJLMNOPQRSTUVWXYZ`

`-h` print help, do nothing else

Number bases must either be in the form `a/b` where `a` and `b` 
are integers, or `a`, just an integer, equivalent to `a/1`.

Number bases must be specified in decimal, or base 10.

Note that if `a` and `b` are not coprime, the representation of
any given number in base `a/b` is not unique. The output will
be the one with maximal low-order nits.

Number bases cannot be less than or equal to 0.

TEMP: Number bases cannot be less than or equal to 1.

If any base is equal to 1, the unary representation is used, 
and only strings made of the unit character which second in 
the alphabet (default of `1`) will be accepted or returned.

The alphabet used must have at least as many characters
as the numerators of the input and output number bases
Thus, if you use a numerator larger than 36, you must supply
a custom alphabet.

The number can either be supplied with a radix point (`AB.CD`),
or with a fraction bar (`AB/CD`), or as an integer (`AB`).
All forms are interpreted correctly. Due to these restrictions,
it is impossible to give an irrational input number. 

The output number is always in fractional form, unless it is
an integer, in which case it is given in integer form.
