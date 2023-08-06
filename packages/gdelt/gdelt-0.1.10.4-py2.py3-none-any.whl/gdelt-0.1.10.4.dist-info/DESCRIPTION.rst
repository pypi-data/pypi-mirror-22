.. -*- mode: rst -*-

.. image:: https://travis-ci.org/linwoodc3/gdeltPyR.svg?branch=master
    :target: https://travis-ci.org/linwoodc3/gdeltPyR

.. image:: https://ci.appveyor.com/api/projects/status/yc6u8v6uvg212dcm/branch/master?svg=true
    :target: https://ci.appveyor.com/project/linwoodc3/gdeltpyr/history

.. image:: https://badge.fury.io/py/gdelt.svg
    :target: https://pypi.python.org/pypi/gdelt

GDELT in Python with ``gdeltPyR``
=================================

``gdeltPyR`` is a Python-based framework to access and analyze `Global Database of Events, Language, and Tone (GDELT) 1.0 and 2.0 data <http://gdeltproject.org/data.html>`_ data in Python Pandas or R dataframes (R dataframe output feature coming soon). A user can enter a single date, date range (two strings), or several individual dates and return a `tidy data set ready for scientific or data-driven exploration <http://vita.had.co.nz/papers/tidy-data.pdf>`_.


`gdeltPyR` retrieves `Global Database of Events, Language, and Tone (GDELT) 1.0 and 2.0 data <http://gdeltproject.org/data.html>`_  via `[parallel HTTP GET requests <http://docs.python-requests.org/en/v0.10.6/user/advanced/#asynchronous-requests>`_ and is an alternative to `accessing GDELT data via Google BigQuery  <http://gdeltproject.org/data.html#googlebigquery>`_. Therefore, the more CPUs or cores you have, the less time it takes to pull more data.  Moreover, the more RAM you have, the more data you can pull.  And finally, for RAM-limited workflows, create a pipeline that pulls data, writes to disc, and flushes.  The only limitation with data pulls ``gdeltPyR`` is you hardware.

The GDELT Project advertises as the largest, most comprehensive, and highest resolution open database of human society ever created. It monitors print, broadcast, and web news media in over 100 languages from across every country in the world to keep continually updated on breaking developments anywhere on the planet. Its historical archives stretch back to January 1, 1979 and accesses the world’s breaking events and reaction in near-realtime as both the GDELT Event and Global Knowledge Graph update every 15 minutes.  Visit the `GDELT website to learn more about the project <(http://gdeltproject.org/#intro)>`_.

**New Features**
----------------

1.  Added geodataframe output.  This can be easily converted into a shapefile or `choropleth <https://en.wikipedia.org/wiki/Choropleth_map>`_ visualization.
2.  Added continuous integration testing for Windows, OSX, and Linux (Ubuntu)
3.  Normalized columns output; export data with SQL ready columns (no special characters, all lowercase)


Coming Soon (version 0.1.11, as of 29 May 2017)
-----------------------------------------------

*  Query Google's BigQuery directly from ``gdeltPyR`` using the `pandas.io.gbq` interface; requires authentication and Google Compute account
* Adding a query for `GDELT Visual Knowledge Graph (VGKG) <http://blog.gdeltproject.org/gdelt-visual-knowledge-graph-vgkg-v1-0-available/>`_
* Adding a query for `GDELT American Television Global Knowledge Graph (TV-GKG) <http://blog.gdeltproject.org/announcing-the-american-television-global-knowledge-graph-tv-gkg/>`_

Installation
------------

Latest release installs from PyPi::

    pip install gdelt

Latest dev version of ``gdeltPyR`` can be installed from GitHub.com::

    pip install git+https://github.com/linwoodc3/gdeltPyR




.. image:: https://twistedsifter.files.wordpress.com/2015/06/people-tweeting-about-sunrises-over-a-24-hour-period.gif?w=700&h=453
    :alt: GDELT can help you visualize the world's news!!!  Analyze GDELT data with gdeltPyR!!

Basic Usage
-----------

.. code-block:: python

    #############################
    # Import gdeltPyR; instantiate
    #############################

    import gdelt

    gd = gdelt.gdelt(version=2)

    results = gd.Search(['2016 10 19','2016 10 22'],table='events',coverage=True)





Full-on open source project with the following contributors:

* Linwood Creekmore


2016-09-25

  Released 0.1
  Initial check-in of gdeltPyR


2016-10-23
  Working on 0.1 release, basic functionality all there

2016-10-25
  Changed MANIFEST.in file; cleaned up egg.info

2016-10-30
  Edited the warning strings and aligned some code with PEP8

2016-10-31
  Added human readable CAMEO Codes column

2016-10-31
  Bug fix; file not loading or downloading on install

2016-11-03
  Added ability to pull GKG 1.0 data

2016-11-06
  GDELT changed url structure for 2.0 events database.

2016-11-07
  Typo on line 290 of base.py; removed and fixed bug.

2017-05-23
  Updated to 0.1.10
  Added geodataframe output
  Started adding unittests (datefuncs first), added docstrings for functions, and PEP8 adherence.
  Fixed datecheck error on current day;

2017-05-27
  Removed datetime parsing
  Added unittests for events before 2013, gkg v1 before apr 1, etc.




