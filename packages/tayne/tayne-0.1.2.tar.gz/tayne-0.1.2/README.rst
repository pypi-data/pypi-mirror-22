*****
tayne
*****

Companion to entr_.

.. _entr: http://entrproject.org/

=====
Usage
=====

Create a configuration file in the same directory called ``.taynerc``::

    [tayne]
    patterns =
        **/*.py
        **/*.ini
    command = py.test tayne.py && pycodestyle tayne.py

Then invoke as follows::

    tayne

Or::

    tayne | entr

=======
License
=======

© 2017 Eddie Antonio Santos. ISC Licensed.
