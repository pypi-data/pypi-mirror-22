python-classtools-autocode
==========================

Project page : `official <http://classtools-autocode.readthedocs.io>`__,
`backup <https://smarie.github.io/python-classtools-autocode/>`__

What's new
----------

-  Doc now generated from markdown using
   `mkdocs <http://www.mkdocs.org/>`__

Want to contribute ?
--------------------

Contributions are welcome ! Simply Fork this project on github, commit
your contributions, and create pull requests.

Here is a non-exhaustive list of interesting open topics:
https://github.com/smarie/python-classtools-autocode/issues to reference
new features or bugfixes.

*Packaging*
-----------

This project uses ``setuptools_scm`` to synchronise the version number.
Therefore the following command should be used for development snapshots
as well as official releases:

.. code:: bash

    python setup.py egg_info bdist_wheel rotate -m.whl -k3


