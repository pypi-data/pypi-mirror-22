.. image:: https://img.shields.io/pypi/v/backports.datetime_timestamp.svg
   :target: https://pypi.org/project/backports.datetime_timestamp

.. image:: https://img.shields.io/pypi/pyversions/backports.datetime_timestamp.svg

.. image:: https://img.shields.io/pypi/dm/backports.datetime_timestamp.svg

.. image:: https://img.shields.io/travis/jaraco/backports.datetime_timestamp/master.svg
   :target: http://travis-ci.org/jaraco/backports.datetime_timestamp


Backport of the `datetime.timestamp()
<http://docs.python.org/3.3/library/datetime.html#datetime.datetime.timestamp>`_ method added in Python 3.3.

    from backports.datetime_timestamp import timestamp
    import datetime

    dt = datetime.datetime.utcnow()
    # instead of dt.timestamp(), use
    timestamp(dt)


License
=======

License is indicated in the project metadata (typically one or more
of the Trove classifiers). For more details, see `this explanation
<https://github.com/jaraco/skeleton/issues/1>`_.


