Stackups program
================

.. contents::
   :local:
   
Introduction
------------

This program's purpose is to allow engineers and designers to verify clearances
between moving or stationary parts within a machine.  This check becomes more
critical when one recognizes that all the features of machined parts are
machined according to an allowable tolerance range.  These accumulated
tolerances can close operating gaps and thus result in malfunctioning
machinery.

It should be obvious that all the features of all the parts will not be at the
maximum of their tolerance range, nor at their minimum.  This program, in
addition to calculating gaps based on max/min tolerances, will also calculate
clearances based on the probability of features being at some median size.
This probability calculation is used by a majority of the major manufacturers
today (six sigma).

What other sources are there for a program of this sort?  That's a good
question.  I have not been able to find any that are publically available.
Most large companies write their own program and it is for internal use only.


Cost
----

This program is free for home use.  That is, you can learn how to use this
program at home.  But if you use it in a professional environment, i.e.,
to design a machine, this program cost $25 per seat.  You may pay for this
program per the link set up on the website `<http://newconceptzdesign.com/>`_.
This program is "donationware", meaning I depend on you good grace to pay
for this product.  (See the license agreement for more information.)  This
product has not been altered or impeded in any way pending your payment.

After initial payment, updates are free.  I appreciate your support!


How it works
------------

This program works within a Python [2] command prompt window (or more preferably,
in an ipython command prompt window).  This program works very similarly to
Python's standard "list" command, which is a basic, fundamental feature of
Python, and therefore this program will be easy to learn.  YOU DO NOT HAVE
TO KNOW THE PYTHON LANGUAGE TO USE THIS PROGRAM!

The fundamental element of the stackups program is called a stackunit, which
is comprised of a dimension related to a machine part, a tolerance for that
dimension, and a few other items related to that dimension.  A group of
stackunits are used to define a stack.  The majority of times many stacks are
evaluated within a given machine.  It is beneficial that these stacks are
managed as a group.  This program does that.

During the course of building up stacks, it is very often necessary to adjust
dimensions to obtain proper clearances.  In such a case the same dimension may
have been used in multiple stacks.  This program will automatically make the
necessary changes to all stacks.


Tutorial
--------

If you have never done a stackup, no problem.  A tutorial has been created to
show you how to do this, along with showing you how to use this program.  It
can be found at `<http://newconceptzdesign.com/>`_.


Changelog
---------

* version 1.0: intial release


---------------------------------------------------------------------

.. rubric:: Footnotes

.. [1] Recommended Python engine on which to run this program (it's free):
    `Anaconda <http://www.continuum.io/downloads/>`_

.. [2] What is Python?  2 min 50 secs to 4 min 10 secs of this video from
    Google describes Python: `<http://www.youtube.com/watch?v=tKTZoB2Vjuk>`_
    (An old version of Python, version 2.4, was used in this class.  As 
    concerns beginners, only two main differences exists between version 2.4
    and the newer 3.x version: 1. for division in 2.4, make sure that you use a
    decimal point in at least one of the numbers.  For example, in 2.4, 
    3/2 = 1, and 3/2.0 = 1.5.  That is, in 2.4, 3/2 is an integer division.  
    2. In version 3.x, a parenthesis is needed for the print command.  That is,
    `print('something to print')` instead of `print 'something to print'`.)