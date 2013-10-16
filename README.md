=========
pypet
=========

The new python parameter exploration toolkit. pypet manages exploration of the parameter space and
data storage into HDF5_ files for you.

===========================
IMPORTANT!
===========================

The current program is a **BETA** version,
please treat it as such and use very carefully.

Moreover, you WILL NOT be able to use trajectories that were created with the *ALPHA*
version any more. I am sorry if you have already explored a lot of parameter spaces.
If this bugs you a lot, let me know and I'll take a look whether I could write
a converter.

Note that until the 0.1.0 version there still might be some changes to the API. Yet, with  0.1.0
I will guarantee a stable API :-)

If you find some bugs or have some questions
feel free to contact me (see below).

Thanks!

Release of the official 0.1.0 version at end of October,
beginning of November :-)

---------------------
Requirements
---------------------

Python 2.6 or 2.7

* tables >= 2.3.1

* pandas >= 0.12.0

* numpy >= 1.6.1

* scipy >= 0.9.0

For git integration you additionally need

* GitPython


=========================
What is pypet all about?
=========================


Whenever you do numerical simulations in science, you come across two major challenges.
First, you need some way to save your data. Secondly, you extensively explore the parameter space.
In order to accomplish both you write some hacky IO functionality to get it done the quick and
dirty way. This means storing stuff into text files, as MATLAB m-files, or whatever comes in handy.

After a while and many simulations later, you want to look back at some of your very
first results. But because of
unforeseen circumstances, you changed a lot of your code. As a consequence, you can no longer
use your old data, but you need to write a hacky converter to format your previous results
to your new needs.
The more complexity you add to your simulations, the worse it gets, and you spend way
too much time handling your data and results than doing science.

Indeed, this was a situation I was confronted with pretty soon during my PhD.
So this project was born. I wanted to tackle the IO problems more generally and produce code
that was not specific to my current simulations, but I could also use for future scientific
projects right out of the box.

The python parameter exploration toolkit (*pypet*) provides a framework to define *parameters* that
you need to run your simulations.
You can actively explore these by following a *trajectory* through the space spanned
by the parameters.
And finally, you can get your *results* together and store everything appropriately to disk.
Currently the storage method of choice is HDF5_.

.. _HDF5: http://www.hdfgroup.org/HDF5/

---------------------------
Package Organization
---------------------------

This project encompasses these core modules:

*  The `pypet.parameters` module including  containers for parameters and results.

*  The `pypet.trajectory` module for managing the parameters and results,
   and providing a way to *explore* your parameter space. Somewhat related is also the
   `pypet.naturalnaming` module, that provides functionality to access and put data into
   the *trajectory*.

*  The `pypet.environment` module for handling the running of simulations.

*  The `pypet.storageservice` for saving your data to disk.

---------------------------
Install
---------------------------

Simply install via `pip install --pre pypet`

Or

Package release can also be found on `pypi.python.org`_. Download, unpack and `python setup.py install` it.

By the way, the source code is available at `github.com/SmokinCaterpillar/pypet`_.

.. _`pypi.python.org`: https://pypi.python.org/pypi/pypet

.. _`github.com/SmokinCaterpillar/pypet`: https://github.com/SmokinCaterpillar/pypet

---------------------------
Documentation
---------------------------

Documentation can be found on `pypet.readthedocs.org`_

If you have questions feel free to contact me at **robert.meyer (at) ni.tu-berlin.de**

.. _`pypet.readthedocs.org`: http://pypet.readthedocs.org/

---------------------------
Acknowledgements
---------------------------


*   Thanks to Robert Pröpper and Philipp Meier for answering all my Python questions.

    You might wanna check out their SpykeViewer_ 
    tool for visualization of MEA recordings and NEO_ data


*   Thanks to Owen Mackwood for his SNEP toolbox which provided the initial ideas
    for this project.


*   Thanks to the `BCCN Berlin`_,
    the Research Training Group GRK 1589/1, and the
    `Neural Information Processing Group`_ for support.

.. _SpykeViewer: https://github.com/rproepp/spykeviewer

.. _NEO: http://pythonhosted.org/neo

.. _`BCCN Berlin`: http://www.bccn-berlin.de

.. _`Neural Information Processing Group`: http://www.ni.tu-berlin.de

================
Main Features
================

* **Novel tree container** `Trajectory`, for handling and managing of
  parameters and results of numerical simulations

* **Grouping** of parameters and results

* Accessing handled items via **natural naming**, e.g. `traj.parameters.traffic.ncars`

* Support for many different **data formats**

    * python native data types: bool, int, float, str, complex

    * list, tuple, dict

    * Numpy arrays and matrices

    * SciPy sparse matrices

    * pandas_ DataFrames

    * BRIAN_ Quantities

    * BRIAN_ Monitors

* Easily **extendible** to other data formats!

* **Exploration** of the parameter space of your simulations

* **Merging** of *trajectories* residing in the same space

* Support for **multiprocessing**, distribute your individual simulation runs to several
  processes.

* **Storage** of simulation data, i.e. the *trajectory*, *parameters*, and *results* into
  **HDF5** files

* **Dynamic Loading**, load only the data you need at the moment and free it afterwards

* **Resuming** a crashed simulation (maybe due to power shut down) after the latest completed run

* **Annotations** of parameters, results and groups, these annotations are stored as HDF5 node attributes

* **Git Integration**, make automatic commits of your source code every time you run an experiment


.. _pandas: http://pandas.pydata.org/

.. _BRIAN: http://briansimulator.org/


======================
Quick Working Example
======================

The best way to show how stuff works is by giving examples. I will start right away with a
very simple code snippet.

Well, what we have in mind is some sort of numerical simulation. For now we will keep it simple,
let's say we need to simulate the multiplication of 2 values, i.e. `z=x*y`.
We have two objectives, a) we want to store results of this simulation `z` and
b) we want to explore the parameter space and try different values of `x` and `y`.

Let's take a look at the snippet at once:

::

    from pypet.environment import Environment
    from pypet.utils.explore import cartesian_product

    def multiply(traj):
        z=traj.x*traj.y
        traj.f_add_result('z',z=z, comment='I am the product of two reals!')

    # Create an environment that handles running
    env = Environment(trajectory='Example1_No1',filename='./HDF/example_01.hdf5',
                      file_title='ExampleNo1', log_folder='./LOGS/')

    # Get the trajectory from the environment
    traj = env.v_trajectory

    # Add both parameters
    traj.f_add_parameter('x', 1.0, comment='Im the first dimension!')
    traj.f_add_parameter('y', 1.0, comment='Im the second dimension!')

    # Explore the parameters with a cartesian product:
    traj.f_explore(cartesian_product({'x':[1.0,2.0,3.0,4.0], 'y':[6.0,7.0,8.0]}))

    # Run the simulation
    env.f_run(multiply)

And now let's go through it one by one. At first we have a job to do, that is multiplying two real
values:

::

    def multiply(traj):
        z=traj.x * traj.y
        traj.f_add_result('z',z)


This is our function multiply. The function uses a so called `Trajectory`
container which manages our parameters. We can access the parameters simply by natural naming,
as seen above via `traj.x` and `traj.y`. The result `z` is simply added as a result with name `'z'` to the `traj` object.

After the definition of the job that we want to simulate, we create an environment which
will run the simulation.

::

    # Create an environment that handles running
    env = Environment(trajectory='Example1_01',filename='./HDF/example_01.hdf5',
                      file_title='Example_01', log_folder='./LOGS/',
                      comment = 'I am the first example!')


The environment uses some parameters here, that is the name of the new trajectory, a filename to
store the trajectory into, the title of the file, a folder for the log files, and a
comment that is added to the trajectory. There are more options available like
the number of processors for multiprocessing or how verbose the final hdf5 file is supposed to be. Check out the documentation_ if you want to know more.
The environment will automatically generate a trajectory for us which we can access via:

::

    # Get the trajectory from the environment
    traj = env.v_trajectory

Now we need to populate our trajectory with our parameters. They are added with the default values
of `x=y=1.0`:

::

    # Add both parameters
    traj.f_add_parameter('x', 1.0, comment='Im the first dimension!')
    traj.f_add_parameter('y', 1.0, comment='Im the second dimension!')

Well, calculating `1.0*1.0` is quite boring, we want to figure out more products, that is
the results of the cartesian product set `{1.0,2.0,3.0,4.0} x {6.0,7.0,8.0}`.
Therefore, we use `f_explore` in combination with the builder function
`cartesian_product`:

::

    # Explore the parameters with a cartesian product:
    traj.f_explore(cartesian_product({'x':[1.0,2.0,3.0,4.0], 'y':[6.0,7.0,8.0]}))

Finally, we need to tell the environment to run our job `multiply`:

::

    # Run the simulation
    env.f_run(multiply)

And that's it. The environment and the storage service will have taken care about the storage
of our trajectory and the results we have computed.

So have fun using this tool!

Cheers,
    Robert


.. _documentation: http://pypet.readthedocs.org/

================================
Miscellaneous
================================

--------------------------------
Tests
--------------------------------

Tests can be found in `pypet/tests`.
Note that they involve heavy file IO and it might not be the case
that you have privileges on your system to write files to a temporary folder.
The tests suite will make use of the `tempfile.gettempdir()` function to
access a temporary folder.

You can run all tests with `$ python all_tests.py` which can also be found under
`pypet/tests`.
You can pass additional arguments as `$ python all_tests.py -k --folder='myfolder/'` with
`-k` to keep the hdf5 files created by the tests (if you want to inspect them, otherwise
they will be deleted after the completed tests)
and `--folder=` to specify a folder where to store the hdf5 files instead of the temporary one.


------------------------------------
License
------------------------------------
Read LICENSE


------------------------------------
Legal Notice
------------------------------------

pypet was created by Robert Meyer at the Neural Information Processing Group (TU Berlin),
supported by the Research Training Group GRK 1589/1.

------------------------------------
Contact
------------------------------------

**robert.meyer (at) ni.tu-berlin.de**

Marchstr. 23

MAR 5.046

D-10587 Berlin