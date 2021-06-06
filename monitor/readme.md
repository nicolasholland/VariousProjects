Monitor 监控
===========

monitor.py
----------

Reads in csv files configured in a monitor.yml and creates a monitor.html
showing their basetimes and indicating if the csv files age is appropriate
for a real time service.

monitor.yml
-----------

In order to monitor timestamps add plants to the plants list.
Ever plant can have an arbitrary number of csv files attached to it.
For every csv file there will be an entry in the monitor showing how old
its basetime is.
Make sure to add a limit for every kind of csv file to the limits list.
If a basetime is older than utc now with respect to its limit, the monitor
will indicate so.

![](https://raw.githubusercontent.com/nicolasholland/VariousProjects/master/monitor/images/example.png)
