| |travisci| |versions| |impls| |wheel| |coverage| |br-coverage|


.. |travisci| image:: https://api.travis-ci.org/jonathaneunice/enpassant.svg
    :target: http://travis-ci.org/jonathaneunice/enpassant

.. |versions| image:: https://img.shields.io/pypi/pyversions/enpassant.svg
    :alt: Supported versions
    :target: https://pypi.python.org/pypi/enpassant

.. |impls| image:: https://img.shields.io/pypi/implementation/enpassant.svg
    :alt: Supported implementations
    :target: https://pypi.python.org/pypi/enpassant

.. |wheel| image:: https://img.shields.io/pypi/wheel/enpassant.svg
    :alt: Wheel packaging support
    :target: https://pypi.python.org/pypi/enpassant

.. |coverage| image:: https://img.shields.io/badge/test_coverage-100%25-blue.svg
    :alt: Test line coverage
    :target: https://pypi.python.org/pypi/enpassant

.. |br-coverage| image:: https://img.shields.io/badge/branch_coverage-99%25-blue.svg
    :alt: Test branch coverage
    :target: https://pypi.python.org/pypi/enpassant

Simple *en passant* assignment, giving Python clearer conditional statements

Usage
=====

::

    from __future__ import print_function # Python 2/3 compat
    from enpassant import *
    result = Passer()

    while result / expensive_request():
        print(result.report())

        # assuming report() is a method of the object
        # expensive_request() would naturally hand back

Discussion
==========

Many languages support *en passant* (in passing) assignment, like so::

    if result = expensive_request():
        print(result.report())

In Python, that's a syntax error.
This leads to more code lines and, in some cases, less
visual clarity::

    result = expensive_request()
    if result:
        print(result.report())

Or worse, in the case of looping structures::

    result = expensive_request()
    while result:
        print(result.report())
        result = expensive_request()

It doesn't look so bad here, in a highly distilled example. But in real
programs, the called function often has parameters to be managed, and the
surrounding code is invariably longer and more complicated. The more complicated
the surrounding computations and requests, the simpler the comparison itself
should be. As the `Zen of Python <http://www.python.org/dev/peps/pep-0020/>`_
intones: "Simple is better than complex." and "Readability counts."

I hope that Python will eventually provide a concise way of handling this, such
as::

    while expensive_request() as result:
        print(result.report())

But in the meanwhile, ``enpassant`` provides a workaround.

How it Works
============

::

    from enpassant import *
    result = Passer()

    while result / expensive_request():
        print(result.report())

Here ``result / expensive_request()`` is read "the result of the
expensive_request." ``result`` is merely a proxy object that, when it
encounters the division operator, returns the denominator. That is, ``result
/ whatever == whatever``. But it also *remembers* the denominator value.
Then, whenever you want the result value provided (presumably, later in the
body of your loop or conditional), simply access it through ``result``. If
you want the full object returned by ``expensive_request()`` you can get it
via ``result.value``. Or or the result has items or attributes, they are
available by indexing or naming the attribute directly. *Easy peasy!*

NB: If you change the items or attributes of ``result``, those settings are
also forwarded to the underlying object. ``result`` is not a copy, but a
true proxy, and as close to the actual object returned as I can make it
given current Python strictures.

Some Details
============

``enpassant`` "assignment" is transparent to conditional expressions,
because the value of the expression is always the value of the denominator.
But ``Passers`` are also guaranteed to have a Boolean value identical to
that of the value they contain, should you wish to use them in subsequent
tests.

The ``result`` in the example above isn't the pure result of the following
function call (or expression), but rather a proxy to it. Item (``[]``)
and attribute (``.``) access work directly on ``result`` because
``Passer`` objects pass on *getitem* and *get-attribute* requests to their
enclosed value. Usually, this is a convenience, and avoids having to
needlessly state that it's really ``result.value`` that's being indexed or
dereferenced. But if you need the specific object returned (say for an
object identity or ``isinstance`` test, use ``result.value`` directly.

Alternative Value Access
========================

It is also possible to retrieve the value of a ``Passer`` by calling it::

    if result / expensive_request():
        print(result().report())

This technique makes clear that the value is being rendered via some
process, rather than just presented as a normal Python name / variable. And
the resulting object from ``result()`` is the true and complete result of
the earlier function call, with no need for implicit / auto-magical
forwarding of items and attributes. Which style makes sense is a matter of
judgment and taste.

Or, if you prefer something terser, the ``+`` (unary positive) operation
will also yield the value::

    if result / expensive_request():
        print(+result.report())

Alternative Invocations
=======================

.. |larrow| unicode:: 0x2190 .. leftwards arrow

If you prefer the less-than (``<``) or less-than-or-equal (``<=``) operators
as indicators that ``result`` takes the value of the following value, they
are supported as aliases of the division operation (``/``). Thus, the
following are identical::

    if result / expensive_request():
        print(result.report())

    if result < expensive_request():
        print(result.report())

    if result <= expensive_request():
        print(result.report())

It's a matter of preference which seems most logical, appropriate, and
expressive. None of them are as good Note, however, that the operation usually
known as division (``/``) has a much higher precedence (i.e. tighter binding to
its operands) than the typical comparison operations (``<`` and ``<=``). If used
with a more complex expressions, either know your precedence or use parenthesis
to disambiguate!

It'd be swell if Python supported arbitrary symbols. Unicode has what would
be reasonable alternative assignment markers, such as |larrow| (`LEFTARDS
ARROW <http://www.fileformat.info/info/unicode/char/2190/index.htm>`_), but
alas! Until Python gets more Unicode-savvy, we have to choose some existing
ASCII operator to repurpose.

It is also possible to use a function call idiom if you prefer::

    if result(expensive_request()):
        print(result.report())

This has the virtue of looking like a "wrapping" of the expensive
request value, rather than reusing / overloading an existing operation.

Grabber and Similar
===================

I've experimented with other forms of collecting and rendering values.
This version of ``enpassant`` includes the results of one of those experiments.
Objects of the ``Grabber`` class can have their attributes set on their first
access. Subsequent uses of that attribute yield the set value.::

    info = Grabber()
    info.name('Joe')
    assert info.name == 'Joe'

The challenge with this approach is that once set, attribute values cannot be
reset.

Notes
=====

* Se ``CHANGES.yml`` for the change log.

* `En passant <http://en.wikipedia.org/wiki/En_passant>`_ is a chess
  term.

* En passant assignment / naming is discussed in
  `Issue1714448 <http://bugs.python.org/issue1714448>`_
  and `PEP 379 <http://www.python.org/dev/peps/pep-0379/>`_, which have
  been rejected and withdrawn, respectively. But that is years gone
  by. I hope the idea will be productively reconsidered in the future.

* Automated multi-version testing managed with
  `pytest <http://pypi.python.org/pypi/pytest>`_,
  `pytest-cov <http://pypi.python.org/pypi/pytest-cov>`_,
  `coverage <https://pypi.python.org/pypi/coverage/4.0b1>`_, and
  `tox <http://pypi.python.org/pypi/tox>`_.
  Packaging linting with `pyroma <https://pypi.python.org/pypi/pyroma>`_.

* Successfully packaged for, and
  tested against, all early 2017 versions of Python: 2.6, 2.7, 3.2, 3.3,
  3.4, 3.5, and 3.6, as well as latest PyPy and PyPy3.

* On Python 2.6, uses Raymond Hettinger's `ordereddict <https://pypi.python.org/pypi/ordereddict>`_
  module (which is included in the source tree for ease of installation)
  to provide ``OrderedDict``. Thank you, Raymond!

* The `simplere <http://pypi.python.org/pypi/simplere>`_ package similarly
  provides en passant handling (and other helpers) for the important, common
  case of regular expression searches.

* An alterantive module: `dataholder <https://pypi.python.org/pypi/dataholder/1.0.1>`_.

* The author, `Jonathan Eunice <mailto:jonathan.eunice@gmail.com>`_ or
  `@jeunice on Twitter <http://twitter.com/jeunice>`_
  welcomes your comments and suggestions.

Installation
============

To install or upgrade to the latest version::

    pip install -U enpassant

You may need to prefix these with ``sudo`` to authorize
installation. In environments without super-user privileges, you may want to
use ``pip``'s ``--user`` option, to install only for a single user, rather
than system-wide. You may also need version-specific versions of ``pip``,
such as ``pip2`` and ``pip3``, depending on your system configuration.
