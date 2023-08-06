LogDataStorage.bin
==================

This file contains more data about each workout and is referenced from
:doc:`logdataaccesstbl.bin`.

The data structurce changes depending on the type of workout being
stored. Each top-level record starts with 95XX where XX is the type code
as described :ref:`here <workout-type-codes>`.

The following table describes the data that appears to be common amongst
all workout entries.

Example from a single distance workout:

::

    9503 0001 19a4 982a 2175 1412 00af 00ff
    ffff 9600 0000 3ec9 0000 157c 1585 044c
    0000 0000 0000 0130 0000 2f41 1d48 0e36
    1def


Detailed description
--------------------

+------+-----------------------------------------------------------+
|Byte  |Description                                                |
+======+===========================================================+
|1     | Each record begin with 95.                                |
+------+-----------------------------------------------------------+
|2     | Type of workout as described above                        |
+------+-----------------------------------------------------------+
|3-4   | TBD                                                       |
+------+-----------------------------------------------------------+
|5-8   | Serial number.                                            |
+------+-----------------------------------------------------------+
|9-12  | These four bytes describe the workout date and time in    |
|      | the following format:                                     |
|      |                                                           |
|      | =======   ===================================             |
|      | Bits      Description                                     |
|      | -------   -----------------------------------             |
|      | 1-8       Minute component of time                        |
|      | 9-16      Hour component of time                          |
|      | 17-20     Month                                           |
|      | 21-25     Day                                             |
|      | 26-32     Year, as number of years since 2000             |
|      | =======   ===================================             |
|      |                                                           |
|      | Byte 9 starts with bit 32 and byte 12 ends on bit 1.      |
|      |                                                           |
+------+-----------------------------------------------------------+
|13-14 | Possibly a user ID. This value appears in UserStatic.bin  |
+------+-----------------------------------------------------------+
|15-16 | TBD                                                       |
+------+-----------------------------------------------------------+
|17-18 | TBD                                                       |
+------+-----------------------------------------------------------+
|19    | Record identifier.                                        |
+------+-----------------------------------------------------------+
|20    | In the case of workout types 6 and 7 this value holds the |
|      | number of intervals.                                      |
+------+-----------------------------------------------------------+
|21-22 | Interval distance. Only applies to interval workouts.     |
|      | For single-distance this field is 0000.                   |
+------+-----------------------------------------------------------+
|23-24 | Interval rest period. In the case of single-distance      |
|      | workouts this value is the total workout time.            |
+------+-----------------------------------------------------------+
|25-26 | TBD                                                       |
+------+-----------------------------------------------------------+
|27-28 | For single distance workouts this is the workout in       |
|      | meters. For timed intervals this is the total time        |
|      | excluding rest periods.                                   |
+------+-----------------------------------------------------------+
|29-30 | Interval overage in meters. For single-distance workouts  |
|      | this is the total distance including the overage. E.g in  |
|      | a 5500m workout with 9m of overage this field will be     |
|      | 0x1585 which is 5509.                                     |
+------+-----------------------------------------------------------+
|31-32 | For single distance workouts this is the interval         |
|      | distance in meters.                                       |
+------+-----------------------------------------------------------+
|33-34 | TBD                                                       |
+------+-----------------------------------------------------------+
|35-36 | TBD                                                       |
+------+-----------------------------------------------------------+
|37-38 | TBD                                                       |
+------+-----------------------------------------------------------+
|39-40 | TBD                                                       |
+------+-----------------------------------------------------------+
|41-48 | These are at the end of each top-level record and inteval |
|      | record and are the same across all workout types.         |
+------+-----------------------------------------------------------+
|49-50 | In the case of non-single-distance workouts there are two |
|      | bytes here. These two bytes vary across devices but seem  |
|      | to be the same for all records from a particular device.  |
+------+-----------------------------------------------------------+
