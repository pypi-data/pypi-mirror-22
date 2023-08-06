
| |travisci| |version| |versions| |impls| |wheel| |coverage| |br-coverage|

.. |travisci| image:: https://api.travis-ci.org/jonathaneunice/namedentities.svg
    :target: http://travis-ci.org/jonathaneunice/namedentities

.. |version| image:: http://img.shields.io/pypi/v/namedentities.svg?style=flat
    :alt: PyPI Package latest release
    :target: https://pypi.python.org/pypi/namedentities

.. |versions| image:: https://img.shields.io/pypi/pyversions/namedentities.svg
    :alt: Supported versions
    :target: https://pypi.python.org/pypi/namedentities

.. |impls| image:: https://img.shields.io/pypi/implementation/namedentities.svg
    :alt: Supported implementations
    :target: https://pypi.python.org/pypi/namedentities

.. |wheel| image:: https://img.shields.io/pypi/wheel/namedentities.svg
    :alt: Wheel packaging support
    :target: https://pypi.python.org/pypi/namedentities

.. |coverage| image:: https://img.shields.io/badge/test_coverage-100%25-6600CC.svg
    :alt: Test line coverage
    :target: https://pypi.python.org/pypi/namedentities

.. |br-coverage| image:: https://img.shields.io/badge/test_coverage-100%25-6600CC.svg
    :alt: Test branch coverage
    :target: https://pypi.python.org/pypi/namedentities

.. |oplus| unicode:: 0x2295 .. oplus

When reading HTML, named entities are neater and often easier to comprehend
than numeric entities (whether in decimal or hexidecimal notation), Unicode
characters, or a mixture. The |oplus| character, for example, is easier to
recognize and remember as ``&oplus;`` than ``&#8853;`` or ``&#x2295;`` or
``\u2295``. It's also a lot mroe compact than its verbose Unicode descriptor,
``CIRCLED PLUS``.

Because they use only pure 7-bit ASCII characters, entities are safer to
use in databases, files, emails, and other contexts, especially given the
many encodings (UTF-8 and such) required to fit Unicode into byte-oriented
storage--and the many platform variations and quirks seen along the way.

This module helps convert from whatever mixture of characters and/or
entities you have into named HTML entities. Or, if you prefer,
into numeric HTML entities (either decimal or
hexadecimal). It will even help you go the other way,
mapping entities into Unicode.

Usage
=====

Python 2::

    from __future__ import print_function # Python 2/3 compatibiltiy
    from namedentities import *

    u = u'both em\u2014and&#x2013;dashes&hellip;'

    print("named:  ", repr(named_entities(u)))
    print("numeric:", repr(numeric_entities(u)))
    print("hex:"   ", repr(hex_entities(u)))
    print("unicode:", repr(unicode_entities(u)))

yields::

    named:   'both em&mdash;and&ndash;dashes&hellip;'
    numeric: 'both em&#8212;and&#8211;dashes&#8230;'
    hex:     'both em&#x2014;and&#x2013;dashes&#x2026;'
    unicode: u'both em\u2014and\u2013dashes\u2026'

You can do just about the same thing in Python 3, but you have to use a
``print`` function rather than a ``print`` statement, and prior to 3.3, you
have to skip the ``u`` prefix that in Python 2 marks string literals as
being Unicode literals. In Python 3.3 and following, however, you can start
using the ``u`` marker again, if you like. While all Python 3 strings are
Unicode, it helps with cross-version code compatibility. (You can use the
``six`` cross-version compatibility library, as the tests do.)

One good use for ``unicode_entities`` is to create cross-platform,
cross-Python-version strings that conceptually contain
Unicode characters, but spelled out as named (or numeric) HTML entities. For
example::

    unicode_entities('This &rsquo;thing&rdquo; is great!')

This has the advantage of using only ASCII characters and common
string encoding mechanisms, yet rendering full Unicode strings upon
reconstitution.  You can use the other functions, say ``named_entities()``,
to go from Unicode characters to named entities.

Other APIs
==========

``entities(text, kind)`` takes text and the kind of entities
you'd like returned. ``kind`` can be ``'named'`` (the default), ``'numeric'``
(a.k.a. ``'decimal'``),
``'hex'``, ``'unicode'``, or ``'none'`` (or the actual ``None``).
It's an alternative to the
more explicit individual functions such as ``named_entities``,
and can be useful when the kind of entitites you want to
generate is data-driven.

``unescape(text)`` changes all entities (save the HTML and XML syntactic
marers ``<``, ``>``, and ``&``)
into Unicode characters. It has a near-alias, ``unicode_entities(text)``
that parallelism with the other APIs.

Encodings Akimbo
================

This module helps map string between HTML entities (named, numeric, or hex)
and Unicode characters. It makes those mappings--previously somewhat obscure
and nitsy--easy. Yay us! It will not, however, specifically help you with
"encodings" of Unicode characters such as UTF-8; for these, use Python's
built-in features.

Python 3 tends to handle encoding/decoding pretty transparently.
Python 2, however, does not. Use the ``decode``
string method to get (byte) strings including UTF-8 into Unicode;
use ``encode`` to convert true ``unicode`` strings into UTF-8. Please convert
them to Unicode *before* processing with ``namedentities``::

    s = "String with some UTF-8 characters..."
    print(named_entities(s.decode("utf-8")))

The best strategy is to convert data to full Unicode as soon as
possible after ingesting it. Process everything uniformly in Unicode.
Then encode back to UTF-8 etc. as you write the data out. This strategy is
baked-in to Python 3, but must be manually accomplished in Python 2.

Escaping
========

Converting the character entities used in text strings to more
convenient encodings is the primary point of this module. This
role is different from that of "escaping" key characters
such as ``&``, ``<`` and ``>`` (and possibly quotation marks such as ``'``
and ``"``) that have special meaning in
HTML and XML. Still, the tasks overlap. They're both about
transforming strings using entity representations, and when
you want to do one, you will often need to do both. ``namedentities``
therefore provides a mechanism to make this convenient.

Any of this modudle's functions take an optional ``escape``
keyword argument. If set to ``True``, strings are pre-processed
with the equivalent of the Python standard library's
``html.escape`` so that ``&``, ``<`` and ``>`` are replaced
with ``&amp;``, ``&lt;``, and ``&gt;`` respectively.
Quotations are not escaped, by default.

If you provide a function instead of ``True``, that function
will be used as the escape transformation. E.g.:

    import html
    hex_entities('...', escape=html.escape)

Will escape all of the HTML relevant characters, including quotations.


Notes
=====

* Version 1.9.4 achieves 100% branch testing coverage.

* Version 1.9 adds the convenience HTML escaping.

* Version 1.8.1 starts automatic test branch coverage with 96% coverage.

* Version 1.8 acheives 100% test line coverage.

* See ``CHANGES.yml`` for more historical changes.

* Doesn't attempt to encode ``&lt;``, ``&gt;``, or
  ``&amp;`` (or their numerical equivalents) to avoid interfering
  with HTML escaping.

* Automated multi-version testing managed with the wonderful
  `pytest <http://pypi.python.org/pypi/pytest>`_,
  `pytest-cov <http://pypi.python.org/pypi/pytest-cov>`_,
  `coverage <http://pypi.python.org/pypi/coverage>`_,
  and `tox <http://pypi.python.org/pypi/tox>`_.
  Continuous integration testing
  with `Travis-CI <https://travis-ci.org/jonathaneunice/namedentities>`_.
  Packaging linting with `pyroma <https://pypi.python.org/pypi/pyroma>`_.

  Successfully packaged for, and
  tested against, all late-model versions of Python: 2.6, 2.7, 3.2, 3.3,
  3.4, 3.5, 3.6, 3.7 pre-release, and late-model PyPy and PyPy3.

* This module started as basically a packaging of `Ian Beck's recipe
  <http://beckism.com/2009/03/named_entities_python/>`_. While it's
  moved forward since then, Ian's contribution to the core remains
  key. Thank you, Ian!

* The author, `Jonathan Eunice <mailto:jonathan.eunice@gmail.com>`_
  or `@jeunice on Twitter <http://twitter.com/jeunice>`_ welcomes
  your comments and suggestions.


Installation
============

To install or upgrade to the latest version::

    pip install -U namedentities

You may need to prefix these with ``sudo`` to authorize
installation. In environments without super-user privileges, you may want to
use ``pip``'s ``--user`` option, to install only for a single user, rather
than system-wide. You may also need to use version-specific ``pip2`` and
``pip3`` installers, depending on your local system configuration and desired
version of Python.

Testing
=======

To run the module tests, use one of these commands::

    tox                # normal run - speed optimized
    tox -e py36        # run for a specific version only (e.g. py27, py36)
    tox -c toxcov.ini  # run full coverage tests
