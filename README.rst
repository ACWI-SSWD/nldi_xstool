===========
NLDI XSTool
===========


.. image:: https://img.shields.io/pypi/v/nldi_xstool.svg
        :target: https://pypi.python.org/pypi/nldi_xstool

.. image:: https://img.shields.io/travis/rmcd-mscb/nldi_xstool.svg
        :target: https://travis-ci.com/rmcd-mscb/nldi_xstool

.. image:: https://readthedocs.org/projects/nldi-xstool/badge/?version=latest
        :target: https://nldi-xstool.readthedocs.io/en/latest/?version=latest
        :alt: Documentation Status




Tool for extracting cross-sections


* Free software: MIT license
* Documentation: https://nldi-xstool.readthedocs.io.


Development
-----------
* conda env create -f .\requirements_dev.yml
* conda activate nldi_xstool
* pip install -e .


Features
--------

* nldi_xstool xsatpoint -f test1.json --lonlat -103.80119 40.2684  --width 1000 --numpoints 101
* nldi_xstool xsatendpts -f test2.json -s -103.801134 40.267335 -e -103.800787 40.272798 -c epsg:4326 -n 101

Credits
-------

CLI developed from example: https://github.com/pallets/click/blob/master/examples/repo/repo.py

This package was created with _Cookiecutter and the _Scientific-python-cookiecutter.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _Scientific_python_cookiecutter: https://github.com/NSLS-II/scientific-python-cookiecutter

Disclaimer
----------

This software is preliminary or provisional and is subject to revision. It is
being provided to meet the need for timely best science. The software has not
received final approval by the U.S. Geological Survey (USGS). No warranty,
expressed or implied, is made by the USGS or the U.S. Government as to the
functionality of the software and related material nor shall the fact of release
constitute any such warranty. The software is provided on the condition that
neither the USGS nor the U.S. Government shall be held liable for any damages
resulting from the authorized or unauthorized use of the software.

