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

For instructions on including installed packages in your projects,
read the "Packaging in C++" section.

Uploading Packages
------------------

To upload a package, you need an account. Run ``cip account create``
and follow the console instructions to create an account.

Next, create a file called ``cip.json`` and enter the following information:

.. code-block:: json

    {
        "name": "package-name",
        "description": "An example package."
        "author": "You",
        "version": "0.0.1",
        "files": [
            "*.so",
            "*.hpp"
        ],
        "dependencies": [
        ]
    }

Run ``cip build`` to create a tarball file of your package.
The tarball will be found in ``dist/package_0.0.1.tar.gz``
File names vary.

Next, upload the tarball file:

``cip upload dist/package_0.0.1.tar.gz``

You will be prompted for your username and password. If the upload
is successful, you will see a success message. Otherwise, the error
will be shown.

You can install your package with ``cip install package``
