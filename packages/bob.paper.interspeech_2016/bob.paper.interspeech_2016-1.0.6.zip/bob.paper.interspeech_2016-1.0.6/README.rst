.. vim: set fileencoding=utf-8 :
.. Thu 23 Jun 13:43:22 2016
.. image:: http://img.shields.io/badge/docs-stable-yellow.svg
   :target: http://pythonhosted.org/bob.paper.interspeech_2016/index.html
.. image:: http://img.shields.io/badge/docs-latest-orange.svg
   :target: https://www.idiap.ch/software/bob/docs/latest/bioidiap/bob.paper.interspeech_2016/master/index.html
.. image:: https://gitlab.idiap.ch/bob/bob.paper.interspeech_2016/badges/master/build.svg
   :target: https://gitlab.idiap.ch/bob/bob.paper.interspeech_2016/commits/master
.. image:: https://img.shields.io/badge/gitlab-project-0000c0.svg
   :target: https://gitlab.idiap.ch/bob/bob.paper.interspeech_2016
.. image:: http://img.shields.io/pypi/v/bob.paper.interspeech_2016.svg
   :target: https://pypi.python.org/pypi/bob.paper.interspeech_2016
.. image:: http://img.shields.io/pypi/dm/bob.paper.interspeech_2016.svg
   :target: https://pypi.python.org/pypi/bob.paper.interspeech_2016


=====================================================================
 Cross-database evaluation of audio-based spoofing detection systems
=====================================================================

This package is part of the Bob_ toolkit and it allows to reproduce the experimental results published in the following paper::

    @inproceedings{KorshunovInterspeech2016,
        author = {P. Korshunov AND S. Marcel},
        title = {Cross-database evaluation of audio-based spoofing detection systems},
        year = {2016},
        month = sep,
        booktitle = {Interspeech},
        pages={1705--1709},
        address = {San Francisco, CA, USA},
    }

If you use this package and/or its results, please cite the paper.


Installation
------------

Follow our `installation`_ instructions for installing ``conda`` and core Bob_ packages. Then, using the Python
from the installed conda environment, bootstrap and buildout this package::

  $ python bootstrap-buildout.py
  $ ./bin/buildout


Contact
-------

For questions or reporting issues to this software package, contact our
development `mailing list`_.


.. Place your references here:
.. _bob: https://www.idiap.ch/software/bob
.. _installation: https://www.idiap.ch/software/bob/install
.. _mailing list: https://www.idiap.ch/software/bob/discuss
.. _user guide: http://pythonhosted.org/bob.paper.interspeech_2016

