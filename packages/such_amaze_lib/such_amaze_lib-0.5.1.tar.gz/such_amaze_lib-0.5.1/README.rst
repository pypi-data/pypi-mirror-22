Such Amaze Library
==================
| 
.. image:: http://cdn.meme.am/instances/62591861.jpg

BitBucket_

.. _BitBucket: https://bitbucket.org/BlaiseFulpin/such_amaze_lib

PyPi_

.. _PyPi: https://pypi.python.org/pypi/such_amaze_lib
Much Wow Functions
==================

``such_amaze_lib`` is a toolbox containing various useful functions and methods

How to install:
---------------

::

    pip install such_amaze_lib

Usage:
------

::

    >>> from such_amaze_lib import decorators
    >>> @decorators.wrapper_printer('NIK', 'POLISS')
    ... def villejuif():
    ...     print 'LA'
    ... 
    >>> print villejuif()
    NIK
    LA
    POLISS
    
Run pytest:
-----------

::

    cd such_amaze_lib
    py.test --doctest-mod -v .

Help:
-----
::

    >>> import such_amaze_lib
    >>> help(such_amaze_lib)