LogDataAccessTbl.bin
====================

This file contains a 32 byte entry for each workout.


Example of a single entry:

::

    f003 0000 c93e 0000 7521 bc8e 0500 157c
    0000 0001 ffff ffff d200 0100 0839 6a61


Detailed description
--------------------

+------+-----------------------------------------------------------+
|Byte  |Description                                                |
+======+===========================================================+
|1     | Each record begins with F0.                               |
|      |                                                           |
+------+-----------------------------------------------------------+
|2     |                                                           | 
|      | .. _workout-type-codes:                                   |
|      |                                                           |
|      | This byte describes the type of workout:                  |
|      |                                                           |
|      | * 01 - Free row (includes games)                          |
|      | * 03 - Single distance                                    |
|      | * 05 - Fixed time                                         |
|      | * 06 - Timed interval                                     |
|      | * 07 - Distance interval                                  |
|      |                                                           |
+------+-----------------------------------------------------------+        
|3-4   | Interval rest time in seconds. The first byte             |
|      | contains the rest time in seconds. For single             |
|      | distance workouts the value is 0000. Example:             |
|      |                                                           |
|      | A workout with a 2 minute rest time will contain the      |
|      | value 7800. 0x78 = 120.                                   |
+------+-----------------------------------------------------------+
|5-6   | This is the same value as found in LogDataStorage.bin     |
|      | bytes 27-28 except here it is little-endian. This seems   |
|      | to be used as the workout "name". In the case of a free-  |
|      | row this is the total number of meters.                   |
+------+-----------------------------------------------------------+
|7-8   | TBD                                                       |
+------+-----------------------------------------------------------+
|9-10  | This is the reverse of bytes 9-10 in LogDataStorage.bin   |
|      | It contains the day/month/year of the workout's           |
|      | timestamp.                                                |
+------+-----------------------------------------------------------+
|11-12 | TBD                                                       |
+------+-----------------------------------------------------------+
|13-14 | Number of splits in workout.                              |
+------+-----------------------------------------------------------+
|15-16 | This is the workout's duration. In the case of distance   |
|      | workouts it's measured in meters. In the case of timed    |
|      | workouts it's the duration in seconds. If it's a timed    |
|      | interval it is the total time of all intervals combined.  |
+------+-----------------------------------------------------------+
|17-18 | Offset where record starts in LogDataStorage.bin.         |
+------+-----------------------------------------------------------+
|19-20 | TBD                                                       |
+------+-----------------------------------------------------------+
|21-22 | TBD                                                       |
+------+-----------------------------------------------------------+
|23-24 | TBD                                                       |
+------+-----------------------------------------------------------+
|25-26 | This is the size of the record in bytes.                  |
+------+-----------------------------------------------------------+
|27-28 | This seems to be an index. The values increase with each  |
|      | workout. 0100, 0200, 0300, etc.                           |
+------+-----------------------------------------------------------+
|29-30 | TBD                                                       |
+------+-----------------------------------------------------------+
|31-32 | TBD                                                       |
+------+-----------------------------------------------------------+
