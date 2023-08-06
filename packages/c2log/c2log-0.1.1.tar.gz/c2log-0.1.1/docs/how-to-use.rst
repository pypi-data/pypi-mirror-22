How to use c2log
================


The main interface to c2log is through the
:py:mod:`c2log.logbook.LogBook` object. The logbook object stores workout
and user data.

Given a directory containg PM5 log files it can be created like so:

::

    >>> from c2log.logbook import LogBook
    >>> logbook = LogBook.from_directory('/path/to/logfiles/')

The :py:mod:`c2log.logbook.LogBook` object provides a unified
interface to all workout data.
See :py:mod:`c2log.structures.base.BaseWorkout`.

::

    >>>  logbook.workouts[0].workout_name
    '5x1100m/1:30r'
    >>> logbook.workouts[0].date
    datetime.date(2016, 5, 23)
    >>> logbook.lifetime_meters
    35668


The raw data as parsed from the files can be also accessed.
The list of raw fields differs for each type of workout.

::

   >>> logbook.workouts[0].type
   3
   >>> l.workouts[0].date_struct
   ULDate (
       date=BitField(
           year=16,
           day=23,
           month=5,
        ),
    )
