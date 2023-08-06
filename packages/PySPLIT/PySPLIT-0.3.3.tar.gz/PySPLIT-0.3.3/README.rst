=======
PySPLIT
=======

PySPLIT is a toolkit for generating, analyzing, and visualizing `HYSPLIT <http://matplotlib.org/>`_ air parcel trajectories.

For general information, refer to the 'SciPy 2015 conference proceedings <>'_ (and/or the YouTube video of this talk).  Please cite this proceedings if you use PySPLIT!

==========
What's New
==========

10/17/2015
----------

The PySPLIT README now under construction!  Check back for updates about new features and example workflows.

Since July 2015, when the 'conference proceedings <>'_ was published, PySPLIT has been overhauled.  Instead of pure NumPy, PySPLIT now uses pandas/geopandas.  Many of the function calls remain the same, but some functionality has changed.  PySPLIT is vastly different under the hood, however, and is faster and more flexible than ever!

====================
The PySPLIT Workflow
====================

Generating Trajectories
-----------------------

PySPLIT can interface with the downloaded version of HYSPLIT and GDAS1 data to perform bulk trajectory generation.  Thousands of simple forwards or backwards trajectories originating from a single geographic location may be generated with a single call, shown below.  In the same call, the corresponding reversed and simplified trajectories may also be generated.  Prior to trajectory generation, we suggest that you dig into the HYSPLIT files and choose your output meteorological variables, and adjust your TRATIO to 0.25.  Here, we generate 5 years of summer and winter back trajectories arriving at 500, 1500, and 2500 meters above ground level at noon in Minneapolis, Minnesota, where PySPLIT was born:

Insert code showing generation and keyword options

The trajectories are stored in the given directoy, with subdirectories containing the reverse (forwards) and clipped or simplified versions of the trajectories.

Future updates to PySPLIT in this arena will include the ability to use other ARL-formatted datasets, the ability to select specific days (rather than generating trajectories a month at a time), and interaction with various HYSPLIT parameters.

Loading Trajectories
--------------------

PySPLIT can load ANY HYSPLIT trajectory, not just the ones generated via the PySPLIT interface to HYSPLIT.

Here, we load all of the trajectories we generated in the previous section.  This procedure reads the trajectory information from file, creates PySPLIT Trajectory instances, and puts those in a TrajectoryGroup:

INSERT CODE showing loading and kw options

This loading procedure was overhauled during the transition to pandas/geopandas, and is approximately 5-10x faster than the old procedure!

PySPLIT Architecture
--------------------

The following diagram shows the PySPLIT object-oriented stuff.

INSERT THESIS chart

The Basics
----------

Working with Trajectory and TrajectoryGroup Instances
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Each Trajectory is essentially a geopandas GeoDataFrame, with meteorological data, datetime information, and path information indexed by time step.  The Trajectory may be sorted, sliced, manipulated, and concatenated with other Trajectory instances just like a regular (Geo)DataFrame.  Although the Trajectory path is available as a series of Points in the geometry column, for convenience a Line geometry stored outside the GeoDataFrame is also included.  See the above diagram for other attributes stored outside of the main GeoDataFrame.

A typical workflow involves cycling through each Trajectory in a TrajectoryGroup, performing an analysis or series of analyses:

INSERT CODE showing loop through Trajectory instances.

New TrajectoryGroups can be made by passing a list of Trajectorys:

INSERT CODE showing creation of TG with Traj that meet a particular criterion

Visualizing Trajectorys
~~~~~~~~~~~~~~~~~~~~~~~


Advanced
--------

Cluster Analysis
~~~~~~~~~~~~~~~~

Calculating Integration Error
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Moisture Uptake
~~~~~~~~~~~~~~~

