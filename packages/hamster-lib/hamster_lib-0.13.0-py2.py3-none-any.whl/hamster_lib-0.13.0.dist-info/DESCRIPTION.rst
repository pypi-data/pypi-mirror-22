===============================
hamster-lib
===============================

.. image:: https://img.shields.io/travis/projecthamster/hamster-lib/master.svg
        :target: https://travis-ci.org/projecthamster/hamster_lib

.. image:: https://img.shields.io/pypi/v/hamster-lib.svg?maxAge=2592000
         :target: https://pypi.python.org/pypi/hamster-gtk/

.. image:: https://img.shields.io/codecov/c/github/projecthamster/hamster-lib/master.svg
        :target: https://codecov.io/github/projecthamster/hamster-lib

.. image:: https://readthedocs.org/projects/hamster-lib/badge/?version=latest
        :target: http://hamster-lib.docs.projecthamster.org/en/latest/
        :alt: Documentation Status

.. image:: https://requires.io/github/projecthamster/hamster-lib/requirements.svg?branch=master
        :target: https://requires.io/github/projecthamster/hamster-lib/requirements/?branch=master
        :alt: Requirements Status

(A badges refer to ``master``)

A library for common timetracking functionality.

``hamster-lib`` aims to be a replacement for ``projecthamster``  backend
library.  While we are not able to function as a  straight forward drop-in
replacement we try very hard to stay as compatible as possible. As a
consequence clients are able to switch to ``hamster-lib``  merely by changing
some basic calls. Most of the semantics and return values will be as before.

This itself points to a major architectural shift in the way ``hamster-lib``
approaches timetracking. We are firm believers in *do one thing, and do it
well*. The tried and tested unix toolbox principle. As such we focus on
providing useful backend functionality and helper methods so clients (dbus
interfaces, CLIs or graphical UIs) can build upon a solid and consistent base
and focus on their specific requirements.

Features
--------
* Full python >=2.7 and >=3.4 compatibility
* Full unicode support
* >= 95% test coverage
* Extensive documentation
* Focus on clean, maintainable code.
* Free software: GPL3
* All you need for production, test or dev environments comes out of the box
  with regular python tools.

First Steps
-----------
* Build dev environment: ``make develop``
* Build the documentation locally: ``make docs``
* Run just the tests: ``make test``
* Run entire test suite including linters and coverage: ``make test-all``

Additional Resources
--------------------
* `Documentation by 'read the docs' <http://hamster-lib.docs.projecthamster.org/en/latest>`_
* `CI thanks to Travis-CI <https://travis-ci.org/projecthamster/hamster-lib>`_
* `Coverage reports by 'codecov' <https://codecov.io/gh/projecthamster/hamster-lib>`_
* `Dependency monitoring by 'requires.io' <https://requires.io/github/projecthamster/hamster-lib/requirements/?branch=master>`_

News: Version 0.13.0
---------------------
This release features only few public functional changes:

#. Raw fact parsing has been moved to a helper method. This should make it easier
   for clients to parse raw fact strings even if they do not qualify as valid
   Fact instances.
#. Facts now provide a ``serialied_string`` method that encodes all relevant data.
#. We now ship ``config helpers`` that provide a baseline config that can easily be
   extended instead of each client having to implement this all over
   again.

For a more detailed overview about what new as well as a list of all the
smaller improvements, please refer to the changelog.

Happy tracking; Eric.

Todo
----
This early release is mainly meant as a rough proof-of-concept at this stage.
It showcases our API as well as our general design decisions.  As such there
are a few functionalities/details of the original ``projecthamster`` backend
that we wish to allow for, but are not provided so far.  These are:

* Autocomplete related methods
* Trophies (The jury is still out on if and how we want to support those.)
* Migrations from old databases.

Incompatibilities
------------------
Despite our efforts to stay backwards compatible we did deliberately break the
way ``Facts`` without end dates are handled. We think allowing for them in any
persistent backend creates a data consistency nightmare and so far there seems
no conceivable use case for it, let alone an obvious semantic.  What we do
allow for is *one* ``ongoing fact``. That is a fact that has a start, but no
end date. For details, please refer to the documentation.

Credits
---------
Tools used in rendering this package:

*  Cookiecutter_
*  `cookiecutter-pypackage`_

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage




History
=======

0.13.0 (2017-06-07)
--------------------
* ``helpers.time.extract_time_info`` checks that ``end > start``. [LIB-30]
* Some attributes of the internal ``XMLWriter`` class have been renamed. [LIB-109]
* ``stop_tmp_fact`` now accepts hints about the end (date-)time. [LIB-129]
* A new method ``update_tmp_fact`` has been added. [LIB-132]
* Added ``Fact.serialized_string``. [LIB-216]
* Raw fact parsing has been moved to a separate helper method. [LIB-230]
* Added backend related config helpers. [LIB-235]
* We now use the built-in ``configparser`` module under python 3. [LIB-236]

0.12.0 (2016-08-05)
--------------------
* Added support for tags! ``hamster_lib.objects.Tag`` instances can be appended
  to ``Fact.tags`` and will be stored by the sqlalchemy backend. We also
  provide comprehensive CRUD methods as part of the brand new
  ``storage.TagManager``.
* Major refactoring of *raw fact* parsing. In particular the way timeinfo is
  extracted from the string. We are now very clear and explicit about the
  supported timeinfo formats. Anything unmatched before the ``@`` token will be
  considered the ``activity.name``. This means in particular that our activity
  names may contain whitespace!
* Added new ``partial`` parameter to ``time.complete_timeframe`` which defaults
  to ``False`` which maintains the functions previous behaviour. Setting it to
  ``True`` however will cause it to only 'complete' those bits of the timeframe
  where there is at least some partial (time or date) information available.
* Moved time related helpers to a dedicated submodule:
  ``hamster_lib.helpers.time``
* Added ``HamsterControl.update_config`` method to allow config updates at
  runtime.
* Renamed ``get_config`` helper to ``load_config`` and limit it to deal just
  with config retrieval. It no longer ensures a default config is written and
  returned. Your client will need to handle any such fallback behaviour now.
* Use ``tox-travis`` to ensure proper multi python version testing on Travis-CI
* Minor fixes in ``config_helpers._get_config_instance``
* Renamed requirements/\*.txt to \*.pip

0.11.0 (2016-07-06)
--------------------
* Renamed this package to ``hamster-lib`` as it now an offical part of
  `projecthamster <https://github.com/projecthamster>`_. It was previously
  named and distributed as `hamsterlib <https://pypi.python.org/pypi/hamsterlib/0.1.0>`_
* Add documentation checker ``pep257`` to testsuite.
* Fixed docstrings.
* Removed ``hamster_lib.objects.Fact.serialized_name``.
* Improved test factories
* Made ``hamster_lib.objects.*`` *hashable*.
* Provide consistent and improved ``__repr__`` methods for
  ``hamster_lib.objects`` classes.
* ``FactManager._get_all`` can now return facts completely*or* partially within
  the timeframe. As a consequence, we removed
  ``FactManager._timeframe_is_free``.
* Added a set of helper function to ease common configuration related tasks.
  In particular they make it easy to store a given config at its canonical
  file system location.
* Improved ``ActivityManager.get_all`` to enable it to return *all* activities.

0.10.0 (2016-04-20)
-------------------
* Add ``ical`` export facilities. Brand new writer using the ``icalendar`` library.
* Add ``xml`` export facilities.
* Switch to `semantic versioning <http://semver.org>`_
* Added GPL3 boilerplate
* Provide documentation on packaging and ``requirements.txt``.
* Add support for `editorconfig <http://editorconfig.org>`_
* Introduce fine grained, storage backend dependent config options.

0.0.3 (2016-04-08)
-------------------
* fact managers ``save`` method now enforces new ``fact_min_delta`` setting.
* Fixed broken packing in ``setup.py``.
* Storage manager methods now use extensive logging.
* Documentation moved to 'alabaster' theme and content extended.
* Remove usage of ``future.builtins.str``.
* Adjusted ``release`` make target.

0.0.2 (2016-04-07)
------------------
* First release on PyPi
* Improved documentation
* Support for *ongoing facts*.
* Updated requirements

0.0.1 (2016-04-03)
---------------------
* First release on github


