.. ***************************************************************************
.. Copyright (c) 2013 SAP AG or an SAP affiliate company. All rights reserved.
.. ***************************************************************************

sqlalchemy-sqlany
=================
This project provides a SQLAlchemy dialect for communicating with a SQL Anywhere
database server. It is built upon the Python SQL Anywhere Database Interface.

Requirements
------------
The following software is required to use the SQL Anywhere dialect for SQLAlchemy:

* SQL Anywhere 11.0.1 or higher
* Python 2.4, 2.5, 2.6, 2.7, or 3.4
* The Python SQL Anywhere Database Interface version 1.0.6 or later
* SQLAlchemy version 0.8.0 or higher

Installing the required software
--------------------------------

The dialect uses the SQL Anywhere Python driver, which must also be installed.
If you are using pip to install the sqlalchemy-sqlany dialect, you can skip
this step since the SQL Anywhere Python driver will be installed as part of
that step.

The SQL Anywhere Database Interface for Python provides a Database API v2
compliant driver (see Python PEP 249) for accessing SQL Anywhere
databases from Python. The SQL Anywhere backend for Django is built on
top of this interface so installing it is required.
    
You can use pip to make this easy::

    $ pip install sqlanydb

Alternatively, you can obtain the Python SQL Anywhere Database Interface 
from https://github.com/sqlanywhere/sqlanydb. Install the driver by
downloading the source and running the following command::
    
    $ python setup.py install

Installing the sqlalchemy-sqlany dialect
----------------------------------------

Again, use pip to install this easily::

    $ pip install sqlalchemy-sqlany

This will install the SQL Anywhere python driver if it was not already installed.

Or you can obtain the dialect from 
https://github.com/sqlanywhere/sqlalchemy-sqlany/. Install the dialect by
downloading the source and running the following command::
    
    $ python setup.py install


Testing the dialect
-------------------

Once the Python SQL Anywhere Database Interface driver and the sqlalchemy-sqlany
dialect are installed, you can run the standard SQLAlchemy tests by following the
following instructions:

1. Create an empty database.
2. Start a SQL Anywhere server on that database. Make sure the server is
   listening for TCP/IP connections on the default port (2638) using 
   -x "tcpip(port=2638)".
3. Execute

::

     $ python run_tests.py

License
-------
This package is licensed under the terms of the Apache License, Version 2.0. See
the LICENSE file for details.

Feedback and Questions
----------------------
For feedback on this project, or for general questions about using SQL Anywhere
please use the SQL Anywhere Forum at http://sqlanywhere-forum.sap.com/
