ldap
=============

LDAP utils.

Installing

.. code:: sh

    $ pip install ldap

Help

.. code::

    $ ldap -h
    ldap -h
    usage: ldap [-h] [-v] [-d] {server} ...

    LDAP utils.

    optional arguments:
      -h, --help      show this help message and exit
      -v, --version   show program's version number and exit
      -d, --debug     enable debug logging

    available commands:
      {server}

.. code::

    $ ldap server -h
    usage: ldap server [-h] [-H HOST] [-P PORT]

    optional arguments:
      -h, --help       show this help message and exit
      -H, --host HOST  default: `localhost`
      -P, --port PORT  default: `3389`
