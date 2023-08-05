PyPlanet
========

.. image:: https://travis-ci.org/PyPlanet/PyPlanet.svg?branch=master
  :target: https://travis-ci.org/PyPlanet/PyPlanet
.. image:: https://codecov.io/gh/PyPlanet/PyPlanet/branch/master/graph/badge.svg
  :target: https://codecov.io/gh/PyPlanet/PyPlanet

This repo contains the PyPlanet package.

**For installation, configuration and development instructions head towards our website:**
http://pypla.net/

Git Structure
-------------

Master is always the latest development environment. We develop features in different branches ``feature/*`` or ``app/*``.

Crafting releases is done at the ``release/vX.X.X`` branches. The branch is created from the master at the moment the freeze moment goes in.
Only bug fixes are accepted to be merged into the release/* branches, name these branches ``bugfix/ISSUE-ID``.

After releasing (from the release branch) it gets a version tag. From this point there is no way back, new bug releases will be crafted
from the release/version branch (``release/v0.1.0`` -> ``release/v0.1.2`` and is accepting merges from ``bugfix/*``).

Visualization of our current release schedule can be found here: `Release Schedule <https://github.com/PyPlanet/PyPlanet/projects/3>`_

Versioning
----------

All PyPlanet versions bellow 1.0.0 are not using semantic versioning.
After 1.0.0, there is a strict semantic versioning (v2) versioning policy in use.

Contributions
-------------

Pull requests and issues are more then welcome.
Please open a ticket before a pull request if you are not yet sure how to solve or want opinions before your implementation. (optional).


