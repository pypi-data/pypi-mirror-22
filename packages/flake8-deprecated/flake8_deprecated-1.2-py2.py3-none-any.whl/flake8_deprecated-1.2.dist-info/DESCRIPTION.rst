.. -*- coding: utf-8 -*-

.. image:: https://travis-ci.org/gforcada/flake8-deprecated.svg?branch=master
   :target: https://travis-ci.org/gforcada/flake8-deprecated

.. image:: https://coveralls.io/repos/gforcada/flake8-deprecated/badge.svg?branch=master&service=github
   :target: https://coveralls.io/github/gforcada/flake8-deprecated?branch=master

Flake8 deprecations plugin
==========================
No language, library or framework ever get everything right from the very beginning.
The project evolves, new features are added/changed/removed.

This means that projects relying on them must keep an eye on what's currently best practices.

This flake8 plugin helps you keeping up with method deprecations ans giving hints about what
they should be replaced with.

This plugin is based on a python checker that was in `plone.recipe.codeanalysis`_.

Install
-------
Install with pip::

    $ pip install flake8-deprecated

Requirements
------------
- Python 2.7, 3.5, 3.6
- flake8

TODO
----
- add a way to provide more deprecations on a per user basis(?), other plugins(?)
- add a way to ignore specific deprecations

License
-------
GPL 2.0

.. _`plone.recipe.codeanalysis`: https://pypi.python.org/pypi/plone.recipe.codeanalysis

.. -*- coding: utf-8 -*-

Changelog
=========

1.2 (2017-05-12)
----------------

- added support for sublimetext (stdin/filename handling)
  [iham]

- Release as universal wheels.
  [gforcada]

- Only test against Python 2.7, 3.5 and 3.6.
  It most probably works on earlier versions of 2.x and 3.x but it's pointless to test on them as well.
  [gforcada]

1.1 (2016-10-26)
----------------

- Fix compatibility with flake8 3.
  [gforcada]

- Require flake8 > 3.0.
  [gforcada]

1.0 (2016-02-27)
----------------
- Warn if using xmlconfig.file, self.loadZCML is the preferred option.
  [gforcada]

- Avoid false reports by suffixing an opening parenthesis on all methods.
  [gforcada]

- Add decorators from zope.interface and zope.component.
  [gforcada]

0.2 (2016-01-20)
----------------
- Suggest to use AccessControl and zope.interface decorators.
  [gforcada]

0.1 (2015-09-17)
----------------
- Initial release
  [gforcada]

- Create the flake8 plugin per se.
  [gforcada]



