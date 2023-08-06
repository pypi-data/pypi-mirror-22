Change Log
==========

**1.2.12**  (May 31, 2017)

    Updated Python 2 / 3 compatibility strategy to be Python 3
    centric. Should be more future-proofed.

    Updated testing.


**1.2.11**  (February 17, 2017)

    Updates testing. Again.  Python 3.2 support again dropped, for the
    last time, given failure on Travis CI. It's old, anyway. Time to
    upgrade!


**1.2.10**  (February 17, 2017)

    Updates testing.  Python 3.2 support re-established, given still
    supported on Travis CI. Docs tweaked.


**1.2.9**  (January 23, 2017)

    Updates testing. Newly qualified under 2.7.13 and 3.6, as well as
    most recent builds of pypy and pypy3. Python 3.2 support withdrawn
    given obsolescence.


**1.2.8**  (August 26, 2015)

    Substantial documentation reorg.


**1.2.7**  (August 23, 2015)

    Starts automated measurement of test branch coverage. Inital runs
    show 100% branch coverage. Hooah!


**1.2.6**  (August 20, 2015)

    Bumped to 100% test coverage.


**1.2.5**  (August 19, 2015)

    Added automated measurement of test coverage. Line coverage
    started at 92%. Bumped to 97%.


**1.2.0**  (August 14, 2015)

    Realized imports were overly restrictive, requiring clients of
    module to needlessly (and contra docs) manually import ``re`` and
    construct the ``match`` object. Fixed. Bumped minor version number
    to reflect de facto API change.


**1.1.1**  (August 14, 2015)

    Simplified ``setup.py`` and packaging. Tweaked docs.


**1.1.0** 

    Adds multi-pattern and case insensitive Glob subclass. Added wheel
    packaging. Rearranged and extended testing structure. Updated
    setup and docs.


**1.0.10** 

    Added ``bdist_wheel`` package support. Extended testing matrix to
    3.5 pre-release builds. Switched to Apache License.


**1.0.5** 

    In several dot-releases, have added support for Travis-CI cloud-
    based continuous integration testing, Sphinx-based documentation,
    and readthedocs.org hosted documentation. The Travis bit has
    required a separate Github repository be created. It is managed
    out of the same development directory, overlaying the existing
    Mercurial / Bitbucket repo. So far, that has caused no problems.

    Documentation somewhat improved.


**1.0.0** 

    Cleaned up source for better PEP8 conformance

    Bumped version number to 1.0 as part of move to `semantic
    versioning <http://semver.org>`_, or at least enough of it so as
    to not screw up Python installation procedures (which don't seem
    to understand 0.401 is a lesser version that 0.5, because 401 > 5)



