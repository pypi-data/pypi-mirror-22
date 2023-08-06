============
Contributing
============

Preparing release
=================

Clean ``build`` directory::

    python setup.py clean -a

Remove previous distributions in ``dist`` directory::

    rm dist/*

Remove previous ``egg-info`` directory::

    rm -r *.egg-info

Bump project's version in ``rolca/__about__.py`` file and update the
changelog in ``docs/CHANGELOG.rst``.

.. note::

    Use `Semantic versioning`_.

Commit changes to git::

    git commit -a -m "Prepare release <new-version>"

Test the new version with Tox_::

    tox -r

Create source distribution::

    python setup.py sdist

Build wheel::

    python setup.py bdist_wheel

Upload distribution to PyPI_::

    twine upload dist/*

Tag the new version::

    git tag <new-version>

Push changes to the main `Rolca's git repository`_::

   git push <rolca-upstream-name> master <new-version>

.. _Semantic versioning: https://packaging.python.org/en/latest/distributing/#semantic-versioning-preferredR
.. _PyPi: https://pypi.python.org/
.. _Tox: http://tox.testrun.org/
.. _Rolca's git repository: https://github.com/dblenkus/rolca-core

