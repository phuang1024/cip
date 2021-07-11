User Manual
===========

Setup
-----

Read the Installing section for install directions.

Install the ``requests`` python package:

``pip install requests``

Installing Packages
-------------------

First, try pinging the server, to see if you can connect.

``cip ping``

If you see a python traceback error, it is likely that you
are unable to connect to the server.

You may also see a server shutting down message. If this is
the case, please wait up to 5 minutes before trying again.
The server will not process any requests while shutting down.

Next, install your package of choice:

``cip install wave``

The ``wave`` package is used in this example. It parses wave
audio files.

Cip will add the package files to ``~/.cip/include`` for header
files, and ``~/.cip/lib`` for shared libraries.

Make sure you add these paths to your C++ include path, so the
compiler and editor can detect them.

.. code-block:: bash

    # Add these to the end of your .bashrc file.

    export CPATH=$CPATH:~/.cip/include
    export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:~/.cip/lib
