rpn\_calculator
===============

RPN Calculator for CLI

Environment
-----------

-  Python 3.5.2
-  Python 2.7.12

Supported operations
--------------------

+-------------+------------------+
| Operation   | Distraction      |
+=============+==================+
| ``+``       | Addition         |
+-------------+------------------+
| ``-``       | Subtraction      |
+-------------+------------------+
| ``*``       | Multiplication   |
+-------------+------------------+
| ``/``       | Division         |
+-------------+------------------+
| ``%``       | Residue          |
+-------------+------------------+
| ``^``       | Power            |
+-------------+------------------+

Example
-------

Case: ``10 * 5 + 2``

Pattern 1
::

    $ rpn
    > 10  
    10
    > 5*
    50
    > 2+
    52
    >


Pattern 2
::

    $ rpn
    > 10 5* 2+
    52
    >

Pattern 3
::

    $ rpn -e "10 5* 2+"
    52

Licence
-------

Copyright (c) 2017 Masaya SUZUKI <suzukimasaya428@gmail.com>

Released under the MIT license
