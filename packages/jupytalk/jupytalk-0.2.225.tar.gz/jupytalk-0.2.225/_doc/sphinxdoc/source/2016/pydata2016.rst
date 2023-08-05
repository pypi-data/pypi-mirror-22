
.. _l-pydata2016:

PyData 06/14/2016 in Paris
==========================

.. sharenet::
    :facebook: 1
    :linkedin: 2
    :twitter: 3
    :head: False

Content
+++++++

**Main presentation**

* :ref:`10plottinglibrariesrst`

A couple of notebooks require to be run to see the results because
a naive conversion does not take into account javascript dependencies
(pythreejs, vega, brython) or does not work at all because
it involves a server (bqplot).

**Static libraries**

* :ref:`imbasemaprst`
* :ref:`imbiopythonrst`
* :ref:`imete3rst`
* :ref:`imlifelinesrst`
* :ref:`immatplotlibrst`
* :ref:`immissingnorst`
* :ref:`imnetworkxrst`
* :ref:`imreportlabrst`
* :ref:`imseabornrst`

**Interactive libraries**

* :ref:`jsbokehrst`
* :ref:`jslightningpythonrst`
* :ref:`jsmpld3rst`
* :ref:`jsplotlyrst`
* :ref:`jspydymassspringdamperrst`
* :ref:`jspygalrst`
* :ref:`jspythreejsrst`
* :ref:`jsvegarst`

**Pure javascript**

* :ref:`jsonlytreantrst`

**Big Data**

* :ref:`bigdatashaderrst`

**GUI**

* :ref:`guigeoplotlibrst`

**Mix between Python and Javascript**

* :ref:`pyjsbqplotrst`
* :ref:`pyjsbrythonrst`
* :ref:`pyjscvispyrst`

**Not covered by this presentation**

* `altair <https://github.com/ellisonbg/altair>`_: an example on how to wrap `Vega <https://github.com/vega/ipyvega>`_
  in a more Pythonic way
* `flexx <https://flexx.readthedocs.io/en/stable/>`_ : very promising way to plug javascript graphs
  written in Python, this module contains a tools which converts Python into javascript
* `graphviz <http://www.graphviz.org/>`_: famous library to draw graph, trees.
  I skipped because all the wrappers are not self contained and require to install
  `graphviz <http://www.graphviz.org/>`_ first.
* `HoloViews <http://ioam.github.io/holoviews/>`_: useful to build complex and linked graphs,
  look at `Pandas Conversion <http://ioam.github.io/holoviews/Tutorials/Pandas_Conversion.html>`_
* `ipyleaflet <https://github.com/ellisonbg/ipyleaflet>`_:
  offers similar tools than `folium <http://folium.readthedocs.io/en/latest/>`_,
  see an example on how to interact with `bqplot <https://github.com/bloomberg/bqplot>`_:
  `An Analysis of Well-Being in San Francisco <https://github.com/SylvainCorlay/bayeshack>`_
* `nglview <http://arose.github.io/nglview/latest/>`_: animate molecular structures
* `pandastable <https://pypi.python.org/pypi/pandastable>`_ : IDE to look at dataframes
* `python-gantt <http://xael.org/pages/python-gantt-en.html>`_ : to draw
  `Gantt charts <https://en.wikipedia.org/wiki/Gantt_chart>`_
* `pytraj <http://amber-md.github.io/pytraj/latest/index.html>`_: analyze of molecular dynamics trajectories and displays
* `pyxley <http://pyxley.readthedocs.io/en/latest/why.html>`_: web app on Flask
* `toyplot <https://toyplot.readthedocs.io/en/stable/>`_: PDF, SVG, MP4 rendering
* `vaex <https://www.astro.rug.nl/~breddels/vaex/>`_: the speaker just after me and the library is able
  to cope with big data at a very high scale

**Dig into building a Jupyter extension**

* `Js extensions <https://carreau.gitbooks.io/jupyter-book/content/Jsextensions.html>`_
* `Distributing Jupyter Extensions as Python Packages <http://jupyter-notebook.readthedocs.io/en/latest/examples/Notebook/Distributing%20Jupyter%20Extensions%20as%20Python%20Packages.html>`_
* `Notebook extensions <https://github.com/jupyter/scipy-advanced-tutorial/blob/master/Part1/04-notebook-extensions.md>`_

.. _l-pydataparis-notes:

From others presentations
+++++++++++++++++++++++++

The presentation which follows showed how to use
`d3.js <https://d3js.org/>`_. It was amazingly easy and understandable:
*Building Visualisations in d3.js for Python Programmers* by Thomas Parslow.

The talk on `software-carpentry <http://software-carpentry.org>`_ was also quite interesting
as they developed strong experience in animating workshop.
Surprising to see so many initiatives to educate people on programming.

Some links taken from presentations:

* `pyspark-ide-starter <https://github.com/ybenoit/pyspark-ide-starter>`_: setup for Spark
* `From scikit-learn to Spark ML <http://blog.xebia.fr/2015/10/08/from-scikit-learn-to-spark-ml/>`_:
  tutorial to switch from *scikit-learn* to *pyspark*

The presentation by `Nexedis <https://www.nexedi.com/>`_ was quite impressive. They introduced their
stack to process data mostly based on open source projects:

* `Fluentd <http://www.fluentd.org/>`_: a software which collects and sends data
  from your laptop. Acccording to the speaker (Jean-Paul Smets),
  it loses 1 byte out of 10 millions,
  even if you close your laptop at anytime.
* `Re6st <https://lab.nexedi.com/nexedi/re6stnet>`_: Resilient, Scalable, IPv6 Network,
  find routes between two locations in Internet. According to the speaker, it is much more reliable
  than standard routing which always takes the same paths.
  It is like taking small roads instead of highways.
* `neoppod <https://lab.nexedi.com/nexedi/neoppod>`_:
  NEO is a distributed, redundant and scalable implementation of ZODB API.
  NEO stands for Nexedi Enterprise Object.
* `Erp5 <https://www.erp5.com/>`_: written in Python,
  see `Python Success Stories <https://www.python.org/about/success/nexedi/>`_.
  ERP5 is a full featured high end Open Source / Libre Software solution published under
  GPL license and used for mission critical ERP / CRM / MRP / SCM / PDM applications
  by industrial organisations and government agencies.
* `SlapOS <http://community.slapos.org/wiki>`_:
  SlapOS is a decentralized Cloud Computing technology that can automate the
  deployment and configuration of applications in a heterogeneous environment.
* `MariaDB <https://github.com/MariaDB/server>`_:
  MariaDB is designed as a drop-in replacement of MySQL(R) with more
  features, new storage engines, fewer bugs, and better performance.
* `wendelin.core <https://pypi.python.org/pypi/wendelin.core>`_
  Out-of-core NumPy arrays. `ZBigArray <http://www.wendelin.io/wendelin-Core.Tutorial.2016>`_
  can cope with any size of data from any container (memory, file, data base, ...)
  and should work with `sikit-learn <http://scikit-learn.org/>`_ (to be continued).

The most interesting part of the talk was about the way the company decided
to base their processes on a particular libraries, especially for *Fluentd*.

No connection but I heard the following in presentations.
Github added a new features which allows users to edit directly from the browser.
It is very useful to fix typos and documentation:
`Editing files in your repository <https://help.github.com/articles/editing-files-in-your-repository/>`_.
Somebody would to add
`Functional PCA <https://en.wikipedia.org/wiki/Functional_principal_component_analysis>`_
to *scikit-learn*.
`thebe <https://oreillymedia.github.io/thebe/>`_ is a javascript libraries
which makes it easy to call a server to run Python code from a web page,
kind of simplified notebook to build documentation
(`source <https://github.com/oreillymedia/thebe>`_).
A paper:
`Sparse pairwise Markov model learning for anomaly detection in heterogeneous data <https://hal-institut-mines-telecom.archives-ouvertes.fr/hal-01167391>`_.
The MIT proposes a pretrained CNN (Convolution Neural Network) for places:

* `Places CNN <http://places.csail.mit.edu/downloadCNN.html>`_,
  `Pre-release of Places365-CNNs <https://github.com/metalbubble/places365>`_
