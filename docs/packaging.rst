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

Create a Package
----------------

First, write your header and source files. This example will name
them ``project.cpp`` and ``project.hpp``, but you can name your files
anything.

Compile the C++ file into machine code:

``g++ -c -fPIC project.cpp -o project.o``

You can add other flags like ``-Wall`` and ``-O3``.

Next, make a shared library file from the machine code:

``g++ -shared project.o -o libproject.so``

The output **must** start with ``lib`` and end with ``.so``

Now, you can distribute the header ``project.hpp`` and the library
``libproject.so``, and other users can use them as described above.

For instructions on how to upload a package to the Cip server, please
read the Manual section.
