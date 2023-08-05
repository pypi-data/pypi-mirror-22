==========
dotty_dict
==========


.. image:: https://img.shields.io/pypi/v/dotty_dict.svg
        :target: https://pypi.python.org/pypi/dotty_dict

.. image:: https://img.shields.io/travis/pawelzny/dotty_dict.svg
        :target: https://travis-ci.org/pawelzny/dotty_dict

.. image:: https://readthedocs.org/projects/dotty-dict/badge/?version=latest
        :target: https://dotty-dict.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status

.. image:: https://pyup.io/repos/github/pawelzny/dotty_dict/shield.svg
     :target: https://pyup.io/repos/github/pawelzny/dotty_dict/
     :alt: Updates


Dotty dictionary with support_for['dot.notation.keys'].

Dotty dict-like object allow to access deeply nested keys using dot notation.
Create Dotty from dict or other dict-like object to use magic of Dotty.

Ultimate goal is to match all Python dictionary method to work with deeply nested **Dotty** keys.


* Free software: MIT license
* Documentation: https://dotty-dict.readthedocs.io.


Features
--------
* Access and assign deeply nested dictionary key using dot notation
* Return None if key doesn't exist instead of KeyError exception
* Get deeply nested value or default value with .get() method

**TODO**

* Escape dot char for dictionary keys with dot: **dotty_dict['key\.key']**
* Delete deeply nested keys: **del dotty_dict['key.key']**
* Check if key exists in deeply nested dictionary: **key.key.key in dotty_dict**
* Check if key does not exist in deeply nested dictionary: **deeply.nested not in dotty_dict**
* Pop nested key: **pop( key.key.key[, default] )**
* Set default bug fix

Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage

