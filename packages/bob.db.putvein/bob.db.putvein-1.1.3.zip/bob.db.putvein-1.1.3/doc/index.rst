.. vim: set fileencoding=utf-8 :
.. Thu 18 Aug 2016 18:14:18 CEST

.. _bob.db.putvein:

===================
 PUT Vein Database
===================

This package is part of the signal-processing and machine learning toolbox
Bob_. It contains an interface for the `PUT Vein Dataset`_. This package does
not contain the original data files, which need to be obtained through the link
above.

The vein pattern recognition is one of the most promising and intensively
developing field of studies in biometrics research. One of main obstacles in
creating new methods of segmentation and classification of vein patterns was a
lack of benchmarking dataset that would allow to obtain comparable results. Put
Vein Database was created to overcame this problem and crate common platform
for algorithms comparison.

PUT Vein pattern database is free available for research purposes can be
applied as common platform for evaluation and comparison of new segmentation
and classification algorithms. Enabling comparison of algorithms without
different hardware systems used by researchers will help to chose the best
algorithm, thus helping in biometrics systems design.

PUT Vein pattern database consists of 2400 images presenting human vein
patterns. Half of images contains a palmar vein pattern (1200 images) and
another half contains a wrist vein pattern (another 1200 images). Data was
acquired from both hands of 50 students, with means it has a 100 different
patterns for palm and wrist region. Pictures ware taken in 3 series, 4 pictures
each, with at least one week interval between each series. In case of palm
region volunteers ware asked to put his/her hand on the device to cover
acquisition window, in way that line below their fingers coincident with its
edge. No additional positioning systems ware used. In case of wrist region only
construction allowing to place palm and wrist in comfortable way was used to
help position a hand.


Documentation
-------------

.. toctree::
   :maxdepth: 2

   py_api


Indices and tables
------------------

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`


.. Place your references here:
.. _bob: https://www.idiap.ch/software/bob
.. _put vein dataset: http://biometrics.put.poznan.pl/vein-dataset/
