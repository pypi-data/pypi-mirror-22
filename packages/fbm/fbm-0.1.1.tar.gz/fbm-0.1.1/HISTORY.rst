0.1.1: 2017-06-10
~~~~~~~~~~~~~~~~~

* Fixed a bug where changing the method would only change the string but not
the actual function called.

* Better behavior when ``daviesharte`` fails. Now switches methods for future
realizations and sets eigenvals to ``None``.

* Added testing for ``daviesharte`` to ``hosking`` fallback.

* Added ``__str__`` and ``__repr__`` functions.

* Changed from ``distutils`` to ``setuptools``.

* Added wheel support.

* Added ``HISTORY.rst``.


0.1.0: 2017-06-09
~~~~~~~~~~~~~~~~~

* Turned fbm.py into an actual python package available on pypi.

* ``FBM`` class for monte carlo simulating multiple realizations of fBm with the
same parameters.

* ``fbm``, ``fgn``, ``times`` functions for one-off realizations.
