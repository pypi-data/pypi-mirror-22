=========
 CHANGES
=========

4.0.0 (2017-05-16)
==================

- Add support for Python 3.4, 3.5, 3.6 and PyPy.

- Fix #264614: Test for node filter didn't do what it was expected to do.

- Import ISite from zope.component after it was moved there from
  zope.location.

3.6.0 (2009-02-01)
==================

- Converted from using zope.app.container to zope.container.

3.5.1 (2009-01-29)
==================

- Add compatibility for newer zope.traversing releases that require us
  to explicitly set up testing. This also works with older releases.

3.5.0 (2009-01-17)
==================

- Get rid of zope.app.zapi dependency, replacing its uses with
  direct imports.

- Clean up dependencies, move testing and rotterdam dependencies
  to extra requires.

- Fix mailing list address to zope-dev@zope.org instead of retired
  zope3-dev@zope.org. Change `cheeseshop` to `pypi` in the package
  url.

- Replace __used_for__ in adapters.py with zope.component.adapts
  calls to make more sense.

- Remove obsolete zpkg files, zcml include file for mkzopeinstance-based
  installations, versions.txt that makes no sense now.

3.4.0 (2007-10-28)
==================

- Initial release independent of the main Zope tree.

v1.2 (2004-02-19) -- 'Scruffy'
==============================

- Moved to `zope.app.tree`

- It is now called 'ZopeTree' again.  Hoorray!

- Refactored browser stuff into its own browser subpackage.

- Separated the handling of tree state from the cookie functionality
  to provide a base class for views based on other tree state sources.

v1.1 (2004-02-16) -- 'Zapp'
===========================

- Added support for displaying lines in a tree (Stephan Richter)

  - Changes in `Node.getFlatDict()` to provide more data.  Removed
    'depth' from node info, but added 'row-state' and
    'last-level-node'.  Changed interface and test accordingly.

  - Updated templates for `StaticTree` skin and example.  Note that
    third party templates from 1.0.x will not work anymore and must be
    updated as well!

v1.0.1 (2004-01-16) -- 'Nibbler'
================================

- Added last remaining pieces for unit tests

- Updated documentation

- Rounded some rough edges in the skin

- Integrated it into the Zope3 distribution below the `zope.products`
  package

v1.0 (2003-11-24) -- 'Lur'
==========================

- Ported to Zope 3

- Renamed it to 'statictree'

- Much more unit tests

- Added filter functionality

- Provided sample implementations as well as an alternate
  rotterdam-like skin using the static tree
