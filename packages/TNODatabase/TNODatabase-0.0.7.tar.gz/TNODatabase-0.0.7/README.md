TNODatabase
===============================

version number: 0.0.7
author: Kyle Franson, Lynus Zullo

Introduction
------------

-  This package allows for easy user interface with the TNO database set
   up on DESOPER.
-  Gives users the ability to add or remove candidates and see relevant
   information regarding both observations and orbits.

Architecture
------------

-  The database has four major tables:
	-  TNOBS: Individual observations of candidates.  Includes information
   such as ra, dec, mag, and much much more!
	-  TNORBIT: Orbits of both reported and unreported candidates.  Includes
   information such as chisq, a, e, i.  Each orbit has an ID, which is
   the same as the designation for known candidates, and an orbitID,
   which helps us link observations to orbits.
	-  TNOLINK: List of observations that are associated to a particular
   orbit.  Links observations to orbit with a unique orbitID.
	-  TNOSTAT: Contains information about quality of candidates.

Requirements
------------

-  Easyaccess module (http://matias-ck.com/easyaccess/#/Home)
-  PyOrbfit (orbit fitting code)
-  Valid DES username and password

Installation / Usage
--------------------

To install use pip:

::

    $ pip install TNODatabase

Or clone the repo:

::

    $ git clone https://github.com/kfranson/TNODatabase.git
    $ python setup.py install

Configuration
-------------

-  The module has no menu or modifiable settings. There is no
   configuration

Troubleshooting
---------------

-  For all troubleshooting question contact either lynusz@umich.edu or
   kfranson@umich.edu

FAQ
---

-  Q: How do I get started?
-  A: After installing (‘pip install TNODatabase’) you will want to
   create a new python project and ‘import TNODatabase’. Next, create a
   class object inside your file ‘db = TNODatabase.Connect()’. Now you
   should be able to call any function you want. ‘db.[function\_name]’

-  Q: How do I add a candidate?
-  A: Users can add a candidate by passing either a csv file, a pandas
   data frame, or a minor planet center text file. The relevant
   functions are:
	-  add\_candidate\_from\_csv(csv\_file, season, name(optional))
	-  add\_candidate\_from\_mpc(file\_name, canid)
	-  add\_candidate(can\_table, season, name(optional),
   designation(optional))
-  Q: How can I see information about a candidate?
-  A: The most basic way to see information about a candidate is to use
   the appropriate SQL query inside of easyaccess. However, there are
   several functions inside of TNODatabase that streamline the process.
   Call these and provide appropriate arguments.

-  In order to see comprehensive documentation simply type in terminal
   ‘help(TNODatabase)’

Contributing
------------

-  Lynus Zullo (lynusz@umich.edu)
-  Kyle Franson (kfranson@umich.edu)
