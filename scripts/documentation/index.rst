.. Leica-GeoCOM-for-drone-tracking documentation master file, created by
   sphinx-quickstart on Mon May 14 22:10:03 2018.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Leica-GeoCOM-for-drone-tracking documentation
=============================================

The GitHub repository of the whole project is publicly available here_.

.. _here : https://github.com/rvermeiren/Leica-GeoCOM-for-drone-tracking

This documentation gathers information that can be found in the comments of the Python scripts alx_track.py_ and GeoCom.py_.

.. _alx_track.py : https://github.com/rvermeiren/Leica-GeoCOM-for-drone-tracking/blob/master/scripts/src/alx_track.py
.. _GeoCom.py : https://github.com/rvermeiren/Leica-GeoCOM-for-drone-tracking/blob/master/scripts/src/GeoCom.py

The Main script is alx_track.py_. It interacts with the total station to request measurements and displays them
on the standard output.

GeoCOM functions are all functions from Leica's GeoCOM protocol that are implemented in the file GeoCom.py_.

.. toctree::
   :maxdepth: 2

   alx_track
   GeoCom


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

