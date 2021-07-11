Packaging in C++
================

Overview
--------

In typical C++ packages, you will provide header files
(``.h``, ``.hpp``) and shared library files (``.so``).

The header files can be included in any program like normal:

.. code-block:: cpp

    #include "mypackage.hpp"

However, instead of compiling the ``.cpp`` file, the compiler
will link the executable to the shared library file.

When compiling a file that includes Cip packages:

.. code-block:: bash

    g++ file.cpp -L ~/.cip/lib -lpkg1 -lpkg2

Make sure you change pkg1 and pkg2 to the actual package name.

The ``-L`` flag tells the linker where to search for library
files. Then, each ``-l`` flag links a library file.
