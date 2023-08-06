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

::

    $ rpn
    > 10  
    10.0
    > 5*
    5.0
    50.0
    > 2+
    2.0
    52.0
    >

Licence
-------

Copyright (c) 2017 Masaya SUZUKI <suzukimasaya428@gmail.com>

Released under the MIT license
