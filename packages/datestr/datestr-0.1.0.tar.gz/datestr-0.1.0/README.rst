DateStr Package
===============

**DateStr** package provide a wrapper object around relativedelta to manage date and datetime strings

Installation :
==============


.. code-block:: shell

    pip install datestr

Examples :
==========

**Example 1:**

.. code-block:: python

    >>> from datestr import Date
    >>> Date('2017-06-04').relativedelta(days=2)
    '2017-06-06'
    >>> type(Date('2017-06-04').relativedelta(days=2))
    <class 'str'>


**Example 2:**

.. code-block:: python

    >>> from datestr import Date
    >>> Date('2017-06-04').relativedelta(month=2, day=3)
    '2017-02-03'
    >>> Date('2017-06-04').relativedelta(last_day=True)
    '2017-06-30'
    >>> Date('2017-06-04').relativedelta(months=4, last_day=True)
    '2017-10-31'

**Example 3:**

.. code-block:: python

    >>> from datestr import Date
    >>> Date('2017-06-04').relativedelta(hour=12)
    >>> '2017-06-04'
    >>> Date('2017-06-04').relativedelta(hour=12, rtype='datetime')
    >>> '2017-06-04 12:00:00'

**Example 4:**

.. code-block:: python

    >>> from datestr import Date
    >>> Date('2017-06-04 04:30:00').relativedelta(days=4, hour=12)
    >>> '2017-06-08 12:30:00'
    >>> Date('2017-06-04 04:30:00').relativedelta(days=4, hour=12, rtype='date')
    >>> '2017-06-08'


**Example 5:**

.. code-block:: python

    >>> from datestr import Date
    >>> from datetime import datetime, date
    >>> Date(date(2018, 6, 3)).relativedelta()
    >>> '2018-06-03'
    >>> Date(datetime(2018, 6, 3, 12, 15, 30)).relativedelta()
    >>> '2018-06-03 12:15:30'

Licence
=======

This software is made available under the LGPL v3 license.

Bug Tracker
===========

Please, feel free to report bugs or suggestions in the `Bug Tracker <https://github.com/chermed/datestr/issues>`_!

Credits:
========

Mohamed Cherkaoui <http://mohamedcherkaoui.com>



News
====

0.1.0
-----

*Release date: 04-Jun-2017*

* First stable version
