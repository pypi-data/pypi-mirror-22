cmdlr
################

``cmdlr`` is a extensible command line tool use for subscribe online comic sites.



Install
=============

Make sure your python >= 3.4 and already install the pip, then...

.. code:: bash

    pip3 install cmdlr



How to use
==========

Set Your Local Comics Directory
-------------------------------

.. code:: bash

    cmdlr opt --output-dir <DIR>


Default comics directory is ``~/comics``.

Check which site be supported 
-----------------------------

.. code:: bash

    cmdlr azr --list

Subscribe a comic
-----------------

.. code:: bash

    cmdlr -s <COMIC>

The ``<COMIC>`` can be a *comic_id* or *comic's url* (the url usually is comic index page, but defined by analyzer independent).

Check current subscribed status
-------------------------------

.. code:: bash

    cmdlr --list-all

It will listing all subscribed comics in your database.

.. code:: bash

    cmdlr -l

It will listing all comics with new volumes.

If you want differ detail level, please combine ``-v`` option like...

.. code:: bash

    cmdlr -vl

or more...

.. code:: bash

    cmdlr -l -vv

Download all your comics
-------------------------

.. code:: bash

    cmdlr -d

All "no downloaded volumes" will be downloaded into your output directory.

Check comic sites update
---------------------------

.. code:: bash

    cmdlr -r

               # or
    cmdlr -rd  # check updated then download



Subscription Database
==========================

You can backup database manually if you want. The database location is...

.. code:: bash

    ~/.cmdlr.db



How to create a new analyzer plugin?
======================================

Very easy:

1. Clone ``cmdlr`` project from http://bitbucket.org/civalin/cmdlr.
2. Check ``src/cmdlr/comicanalyzer.py`` to learn what function you need to implement. And reference other analyzer plugin to create yours.
3. Put your ``.py`` plugin file into ``src/cmdlr/analyzers`` directory.
4. Run ``./cmdlr.py`` under project directory to test the plugin.
5. When you done, don't forget make a pull request to me. Thanks!

Happy hacking! :D



LICENSE
=========

MIT License

Copyright (c) 2014~2015 CIVA LIN



Changelog
=========

2.1.4
---------

- Analyzer: fix `8c` analyzer malfunction by web site changed.

2.1.3
---------

- Analyzer: set `u17` analyzer reject pay chapter.

2.1.2
---------

- Analyzer: set `u17` analyzer reject vip chapter.

2.1.1
---------

- Analyzer: `u17` tweak for site changed.

2.1.0
---------

- Tweaked: use `--list-all` to list all comic which user subscribed. and `-l` only show comic with no downloaded volumes.
- Analyzer: `8c` tweak for site changed.

2.0.6
---------

- Analyzer: `cartoonmad` tweak for site changed.

2.0.5
---------

- fixed: remove debug code.

2.0.4
---------

- Analyzer: `8comic` tweak for site changed.

2.0.3
---------

- Fixed: cbz convert error when volume name contain ``.`` character.
- Fixed: better sorting when using ``-l``
- Added: ``-l`` option can search keyword in title.
- Enhanced: volume disappeard info when using ``-l``.

2.0.2
---------

- Enhanced: Better exception processing.

2.0.1
---------

- Enhanced: Truly avoid the title conflict.
- Enhanced: Windows platform path assign.

2.0.0
---------

This is a fully rewrite version

- Backend DB: ``tinydb`` -> ``sqlite``
- Collect more data.
- Remove search function.
- make it extensible.

1.1.0
---------

- Init release.
