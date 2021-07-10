Security
========

**The Cip server is run on the Python http module,
which does not have many security features. Please
use care when uploading information to the server.**

Password Security
-----------------

In all cases when you are asked for a password, it is
hashed client side. We use SHA-2 algorithms, hundreds
of thousands of times each hash. This makes it harder
to brute force un-hash passwords, as each hash takes
longer. Currently, each hash takes about 0.1 seconds.

Server Security
---------------

The server is run on an AWS server. Please report any
security issues you encounter on GitHub.
