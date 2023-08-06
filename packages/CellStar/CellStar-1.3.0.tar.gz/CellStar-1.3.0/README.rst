CellStar
========
version 1.3.0

Introduction
------------
Automatic tracking of cells in time-lapse microscopy is required to investigate a multitude of biological questions. To limit manipulations during cell line preparation and phototoxicity during imaging, brightfield imaging is often considered. Since the segmentation and tracking of cells in brightfield images is considered to be a difficult and complex task, a number of software solutions have been already developed.
 
CellStar is one of such algorithms. It is optimized to segment and track images of budding yeast cells growing in monolayer (e.g. images from microfluidic chambers), however the algorithm can be also used to track other round objects (in brightfield as well as fluorescent images).

The important part of that solution is parameter fitting mechanism which allows to train and use CellStar for many different types of imagery.

Please visit our website http://www.cellstar-algorithm.org/ for more details.

Distributions
-------------
There are three ways of using CellStar:

- python package https://github.com/Fafa87/cellstar

- plugin for CellProfiler 2.2 http://cellstar-algorithm.strikingly.com/#download

- matlab version for manual curation http://cellstar-algorithm.strikingly.com/#download

The plugin package includes not only the plugin itself but also examples of its usage to guide users on how to achieve best segmentation on a given type of imagery.

Wide range of example usages
----------------------------
During the testing phase of our plugin it turned out that combining parameter fitting and CellProfiler pipeline flow can result in a very flexible solution. In order to show that and also provide a quick starting point for users the `Official user guide <https://drive.google.com/file/d/0B3to8FwFxuTHNnJZbXRIdTdWTFE/view>`_ was prepared.

It contains the ready to use segmentation solution for a wide range of various imagery which includes:

- complete pipeline description

- method selection discussions

- CellProfiler Analyst usage for advanced filtering

The pipelines listed in the document along with the actual imagery are available as a part of plugin version. Every case can be easily to recreate the results.

.. image:: http://res.cloudinary.com/hrscywv4p/image/upload/c_limit,fl_lossy,h_1440,w_720,f_auto,q_auto/v1/92051/tiles_ytp2ac.jpg
