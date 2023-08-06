Base Converter
==============

This library works as a base converter up to base 30
You can conver both from base 10 to any other bases (up to 30) as well as back to base 10

----

toBaseTen 
=========
This function takes arguments: number that you want to convert and its base
It will return an int in base 10

Examples:

>>> toBaseTen(2112, 3)
68

>>> toBaseTen('AB12', 12)
61904

>>> toBaseTen('AB12', 16)
111828

----

toAnyBase 
=========
This function takes 2 arguments: number (in base 10, if you have number in any other base, 
please use toBaseTen function first to get get your number in base 10) and base that you
want to convert your number to.
It will return a string

Examples:

>>> toAnyBase(23412,30)
'Q0C'

>>>	toAnyBase(23412,15)
'6E0C'

>>> toAnyBase(12, 2)
'1100'