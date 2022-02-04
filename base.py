help_message = '''Usage:

Converts NUMBER from rational INPUT_BASE to rational OUTPUT_BASE

$ python base.py NUMBER [OPTIONS]

-i=INPUT_BASE, default 10
-o=OUTPUT_BASE, default 10
-a=ALPHABET, default "0123456789ABCDEFGHIJLMNOPQRSTUVWXYZ"

-h print help, do nothing else

Number bases must either be in the form a/b where a and b 
are integers, or a, just an integer, equivalent to a/1.

Number bases must be specified in decimal, or base 10.

Note that if a and b are not coprime, the representation of
any given number in base a/b is not unique. The output will
be the one with maximal low-order nits.

Number bases cannot be less than or equal to 0.

TEMP: Number bases cannot be less than or equal to 1.

If any base is equal to 1, the unary representation is used, 
and only strings made of the unit character which second in 
the alphabet (default of "1") will be accepted or returned.

The alphabet used must have at least as many characters
as the numerators of the input and output number bases
Thus, if you use a numerator larger than 36, you must supply
a custom alphabet.

The number can either be supplied with a radix point (AB.CD),
or with a fraction bar (AB/CD), or as an integer (AB).
All forms are interpreted correctly. Due to these restrictions,
it is impossible to give an irrational input number. 

The output number is always in fractional form, unless it is
an integer, in which case it is given in integer form.
'''

#TODO allow interactive mode if no number argument
#for piping?

debug = False

import sys

#initialize arguments as Nones
in_base = None
out_base = None
number = None
alphabet = None

#stderr utility
def err(*args,**kwargs):
    print(*args, file=sys.stderr, **kwargs)

#user probably doesn't know how to use:
if len(sys.argv) == 1:
    print("Type 'python base.py -h' to see usage help")
    exit(999)
    
#skip the execution name, ingest arguments
for arg in sys.argv[1:]: 
    #arg is an option?
    if arg[0] == "-":
        if arg == "-h":
            err(help_message)
            exit(0)
        if arg[:3] == "-i=":
            #not set yet?
            if in_base == None:
                in_base = arg[3:]
            else:
                err("Multiple -i options")
                exit(3)
            continue
        if arg[:3] == "-o=":
            #not set yet?
            if out_base == None:
                out_base = arg[3:]
            else:
                err("Multiple -o options")
                exit(4)
            continue
        if arg[:3] == "-a=":
            #not set yet?
            if alphabet == None:
                alphabet = arg[3:]
            else:
                err("Multiple -a options")
                exit(5)
            continue
        #now, arg is not a recognized option
        err("Unrecognized option:",arg)
        exit(2)
    #if execution reaches here, arg is not an option
    #number arg not set yet?
    if number == None:    
        number = arg
    else:
        err("Extra number argument:",arg)
        exit(1)

#supply default -i, -o, -a values
if in_base == None:
    in_base = "10"
if out_base == None:
    out_base = "10"
if alphabet == None:
    alphabet = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
if number == None:
    err("Missing number argument")
    exit(99)
    
#process -i argument
in_frac = in_base.split("/")
if len(in_frac) > 2: 
    err("Invalid rational number",in_base)
    exit(6)
if len(in_frac) == 1:
    in_frac.append("1") #denominator of integer
try:
    in_frac = tuple(map(int,in_frac))
except ValueError:
    err("Invalid rational number",in_base)
    exit(6)
#unpack
(in_n, in_d) = in_frac
#these are only used for validation of bases

#process -o argument
out_frac = out_base.split("/")
if len(out_frac) > 2: 
    err("Invalid rational number",out_base)
    exit(7)
if len(out_frac) == 1:
    out_frac.append("1") #denominator of integer
try:
    out_frac = tuple(map(int,out_frac))
except ValueError:
    err("Invalid rational number",out_base)
    exit(7)
#unpack
(out_n, out_d) = out_frac

#check for negative and zero and infinity bases
if in_d * out_d == 0:
    err("Bases have division by zero")
    exit(10)
if in_n * out_d == 0:
    err("Bases cannot be zero")
    exit(10)
if in_n * in_d < 0 or out_n * out_d < 0:
    err("Bases cannot be negative")
    exit(10)
    
#rectify bases
in_frac = tuple(map(abs,in_frac))
out_frac = tuple(map(abs,out_frac))

#TEMP
#Check for subunit bases
if in_frac[0] < in_frac[1] or out_frac[0] < out_frac[1]:
    err("TEMP: No bases less than 1")
    exit(-1)

#check alphabet is not illegal
if "." in alphabet:
    err("Cannot include '.' (radix point) character in alphabet")
    exit(11)
if "/" in alphabet:
    err("Cannot include '/' (fraction bar) character in alphabet")
    exit(11)

#check sufficient length of alphabet
if len(alphabet) < max(in_n,out_n):
    err("Insufficient alphabet for base numerator:",max(in_n,out_n))
    err("Current alphabet:",alphabet)
    exit(9)
if in_n == in_d and len(alphabet) < 2: #requires that a unit char exists
    err("Insufficient alphabet for unary base")
    exit(9)

#check number is composed of alphabet chars
if in_n == in_d: #unary
    for nit in number:
        if nit != alphabet[1]:
            if nit not in ("/"):
                err("Input base is 1 but number is not composed of only unit characters.")
                err("Radix point is not allowed in unary input")
                exit(8)
else: #not unary
    for nit in number: 
        if nit not in alphabet[:in_frac[0]]:
            if nit not in (".","/"):
                err("Number is not composed of valid alphabet characters")
                err("Current alphabet:",alphabet[:in_frac[0]])
                exit(8)

        
#set up character to value map
nits = {}
# e.g. for the default alphabet, "0"=0, "A"=10, "G"=16,... 
for i in range(len(alphabet)):
    nits[alphabet[i]] = i

#process number argument as either integer, radix-pointed, fraction
if number.count(".")+number.count("/") > 1:
    err("Number can only have one radix point or one fraction bar")
    exit(12)
if "." in number:
    #how many decimal places after point?
    places = len(number)-number.index(".")-1
    #multiply by the input base enough times to turn numerator into integer
    number = (number.replace(".",""),alphabet[1]+alphabet[0]*places)
elif "/" in number:
    number = (number[:number.index("/")],number[number.index("/")+1:])
else:
    number = (number,"1")
    
if debug: 
    print("Diagnostic: Converting",number,"from base",in_frac,"to base",out_frac)


    
import math

#rational addition
def add(f1,f2):
    n = f1[0]*f2[1]+f1[1]*f2[0]
    d = f1[1]*f2[1]
    g = math.gcd(n,d)
    return (n//g,d//g)

#rational addinverse
def neg(f1):
    return (-f1[0],f1[1])

#rational mulinverse
def rec(f1):
    return (f1[1],f1[0])

#rational mutiplication
def mul(f1,f2):
    n = f1[0]*f2[0]
    d = f1[1]*f2[1]
    g = math.gcd(n,d)
    return (n//g,d//g)

#two stage conversion, one to 10-ary rational
#and then one to the output base

#decimal is the accumulator that stores the 10-ary rational
#numerator and denominator separately
decimal_n = (0,1)
decimal_d = (0,1)
#because bases can be rational numbers, each of these needs to
#initially be stored as a fraction, not an integer

if debug:
    print("Number initialized as:",str(number))

#convert number's numerator
for nit in number[0]: #calculate with horner form
    decimal_n = mul(decimal_n,in_frac) 
    value = nits[nit] #numerical value?
    decimal_n = add(decimal_n,(value,1))
#convert number's denominator
for nit in number[1]: #again, horner
    decimal_d = mul(decimal_d,in_frac)
    value = nits[nit]
    decimal_d = add(decimal_d,(value,1))

if decimal_d == (0,1):
    #uh oh
    err("Number has a denominator of 0")
    exit(14)
    
#convert number into a decimal fraction
decimal = mul(decimal_n,rec(decimal_d))
#autoreduces fraction

#first half completed!
if debug:
    print("Number is equivalent to decimal:",decimal)

#conversion to output base
#every integer has a integer representation in any rational base
#if the rational base is not reduced, then it may not be unique

#flag this
integral = False
if decimal[1] == 1:
    integral = True

#is output unary?
if out_frac[0] == out_frac[1]:
    #print out
    #0 is the empty string!
    print(alphabet[1]*decimal[0],end="")
    if not integral:
        print("/"+alphabet[1]*decimal[1],end="")
    print()
    exit(0)

#for mutability
decimal = list(decimal)
number_out = ["",""]
#assemble numerator/denominator
for i in (0,1):
    while decimal[i] > 0:
        nit = alphabet[decimal[i] % out_frac[0]] #nit to append to the number
        decimal[i] = decimal[i]//out_frac[0]*out_frac[1]
        number_out[i] = nit + number_out[i]
#print out
print(number_out[0],end="")
if not integral:
    print("/"+number_out[1],end="")
print()
exit(0)
