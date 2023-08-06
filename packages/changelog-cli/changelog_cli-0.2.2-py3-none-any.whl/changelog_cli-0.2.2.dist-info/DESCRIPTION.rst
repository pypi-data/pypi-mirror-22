Changelog CLI
=============

|PyPI version| |Build Status| |Code Health| |Coverage Status|

A command line interface for managing your CHANGELOG.md files.

Commands
--------

``changelog init`` -> Creates a CHANGELOG.md

``changelog (new|change|fix|break) <message>`` -> adds a line to the
appropriate section

``changelog release --major|minor|patch|suggest)`` -> Cuts a release for
the changelog, incrementing the version

.. |PyPI version| image:: https://badge.fury.io/py/changelog-cli.svg
   :target: https://badge.fury.io/py/changelog-cli
.. |Build Status| image:: https://travis-ci.org/mc706/changelog-cli.svg?branch=master
   :target: https://travis-ci.org/mc706/changelog-cli
.. |Code Health| image:: https://landscape.io/github/mc706/changelog-cli/master/landscape.svg?style=flat
   :target: https://landscape.io/github/mc706/changelog-cli/master
.. |Coverage Status| image:: https://coveralls.io/repos/github/mc706/changelog-cli/badge.svg?branch=master
   :target: https://coveralls.io/github/mc706/changelog-cli?branch=master


