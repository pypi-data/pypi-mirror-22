wendy
=====

A one-dimensional gravitational N-body code.

|Build Status| |Coverage Status| |Binder|

Overview
--------

``wendy`` solves the one-dimensional gravitational N-body problem to
machine precision with an efficient algorithm [O(log N) /
particle-collision]. Alternatively, it can solve the problem with
approximate integration, but with exact forces.

Author
------

Jo Bovy (University of Toronto): bovy - at - astro - dot - utoronto -
dot - ca

Installation
------------

Clone/fork/download the repository and install using

::

    sudo python setup.py install

or locally using

::

    python setup.py install --user

Usage
-----

Use ``wendy.nbody`` to initialize a generator object for initial *(x,v)*
with masses *m*. The generator then returns the state of the system at
equally-spaced time intervals:

::

    g= wendy.nbody(x,v,m,0.05) # delta t = 0.05
    next_x, next_v= next(g) # at t=0.05
    next_x, next_v= next(g) # at t=0.10
    ...

The generator initialization with ``wendy.nbody`` has options to (a)
solve the problem exactly or not using ``approx=`` and (b) include an
external harmonic oscillator potential ``omega^2 x^2 / 2`` with
``omega=`` (both for exact and approximate solutions).

Examples
--------

You can run these *without* installing ``wendy`` by clicking on |Binder|
and navigating to the ``examples/`` directory. Note that some of the
movies might fail to be rendered on the binder webpage, so you might
want to skip those when running the notebooks (or changing the
``subsamp`` input for them).

-  Phase mixing and violent relaxation in one dimension: `example
   notebook <examples/PhaseMixingViolentRelaxation.ipynb>`__ (run
   locally to see movies, or view on
   `nbviewer <http://nbviewer.jupyter.org/github/jobovy/wendy/blob/master/examples/PhaseMixingViolentRelaxation.ipynb?flush_cache=true>`__)

-  A self-gravitating, sech2 disk: `example
   notebook <examples/SelfGravitatingSech2Disk.ipynb>`__ (run locally to
   see movies, or view on
   `nbviewer <http://nbviewer.jupyter.org/github/jobovy/wendy/blob/master/examples/SelfGravitatingSech2Disk.ipynb?flush_cache=true>`__)

-  Adiabatic contraction: `example
   notebook <examples/AdiabaticContraction.ipynb>`__ (run locally to see
   movies, or view on
   `nbviewer <http://nbviewer.jupyter.org/github/jobovy/wendy/blob/master/examples/AdiabaticContraction.ipynb?flush_cache=true>`__)

-  Adiabatic vs. non-adiabatic energy injection for an exponential disk:
   `example notebook <examples/AdiabaticVsNonAdiabatic.ipynb>`__ (run
   locally to see movies, or view on
   `nbviewer <http://nbviewer.jupyter.org/github/jobovy/wendy/blob/master/examples/AdiabaticVsNonAdiabatic.ipynb?flush_cache=true>`__)

-  ``wendy`` scaling with particle number: `example
   notebook <examples/WendyScaling.ipynb>`__ (view on
   `nbviewer <http://nbviewer.jupyter.org/github/jobovy/wendy/blob/master/examples/WendyScaling.ipynb?flush_cache=true>`__)

.. |Build Status| image:: https://travis-ci.org/jobovy/wendy.svg?branch=master
   :target: https://travis-ci.org/jobovy/wendy
.. |Coverage Status| image:: https://codecov.io/gh/jobovy/wendy/branch/master/graph/badge.svg
   :target: https://codecov.io/gh/jobovy/wendy
.. |Binder| image:: http://mybinder.org/badge.svg
   :target: http://beta.mybinder.org/repo/jobovy/wendy
