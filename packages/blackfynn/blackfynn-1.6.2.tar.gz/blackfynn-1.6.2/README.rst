blackfynn-py
============

Python client and command line tool for Blackfynn.

Installation
------------

Note: we currently only support *Python v2.7*.

1. Download, and unzip source.
2. In source directory, run:

.. code:: python

    pip install cython
    pip install -e .

Credentials Setup
-----------------

Connection credentials to Blackfynn can sourced from environment variables. In your ``~/.bashrc`` or
``~/.bash_profile``, set the following variables. Before using the client library or command line
tool, ensure these environment variables are set.

.. code:: bash

    export BLACKFYNN_USER=you@company.com
    export BLACKFYNN_PASS=<your-password>

Client Library
--------------

Basic Usage: examples
~~~~~~~~~~~~~~~~~~~~~

.. code:: python

    # imports
    from blackfynn import Blackfynn

    # client
    bf = Blackfynn()

    # If you belong to more than one organization, explicitly set your context, otherwise, ignore.
    bf.set_context('my organization name')

    # print your available datasets
    datasets = bf.datasets()
    print datasets

    # grab some dataset (e.g. first one)
    ds = datasets[0]

    # list items inside dataset (first level)
    print ds.items

Upload data
~~~~~~~~~~~

Upload files
^^^^^^^^^^^^

You must upload files into a ``Dataset`` or ``Collection``.

.. code:: python

    # upload a file into a dataset (ds)
    ds.upload_files('/path/to/my_data.nii.gz')

Stream timeseries data
^^^^^^^^^^^^^^^^^^^^^^

*Note:* Before streaming, ensure you have the proper AWS credentials (environment variables) set to
stream data to Kinesis. Full example of creating an empty timeseries package and streaming a
dataframe is shown below:

.. code:: python

    from blackfynn import Blackfynn, TimeSeries, TimeSeriesChannel
    from blackfynn.utils import generate_dataframe

    # generate data (4 channels)
    df = generate_dataframe(minutes=2, freq=100)

    # login
    bf = Blackfynn()
    bf.set_context('blackfynn')

    # dataset (assumes exists)
    ds = bf.get_dataset('streaming')

    # create an empty timeseries
    ts = TimeSeries('My Test TimeSeries')
    ds.add(ts) # add to dataset

    # create channels (match names to dataframe columns)
    channels = [TimeSeriesChannel(col, rate) for col in df.columns]

    # add channels to timeseries
    ts.add_channels(*channels)

    # stream the data up!
    ts.stream_data(df)

Retrieve data
~~~~~~~~~~~~~

Retrieve timeseries data
^^^^^^^^^^^^^^^^^^^^^^^^

.. code:: python

    ts = bf.get('N:package:your-timeseries-id')

    # get first minute of data in 1-second chunks
    for chunk in ts.get_data_iter(chunk_size='1s', length='1m'):
        # do something with data (pandas Dataframe)
        print "Mean values =", chunk.mean()

    # you can do the same thing for a single channel
    channel = ts.channels[0]
    for chunk in channel.get_data_iter(chunk_size='5s', length='10m'):
        # do something with data (pandas Series)
        print "Max value =", chunk.max()

Command Line Tool
-----------------

Usage
~~~~~

.. code:: bash

    >> bf --help
    Blackfynn Client

    Usage:
      bf upload [options] <destination> <file> [<file>...]
      bf append [options] <destination> <file> [<file>...]
      bf search [options] <term> [<term>...]
      bf datasets [options]
      bf dataset [options] <dataset> [<command>] [<action>] [<action-args>...]
      bf create [options] collection <destination> <name>
      bf create [options] dataset <name>
      bf delete [options] <item>
      bf show [options] <item>
      bf orgs [options]
      bf env [options]
      bf version

    Options
      -h --help       Show help.
      --user=<user>   Email/username
      --pass=<pass>   Password
      --host=<host>   Blackfynn host
      --org=<org>     Set organization context

Basic examples
~~~~~~~~~~~~~~

Show your setup

.. code:: bash

    bf env

Show your datasets

::

    >> bf datasets --org blackfynn
    Datasets:
     - Studies (id: N:dataset:12aba9af-650c-4fd5-b150-ae77a60a92a0)
     - NICU (id: N:dataset:4fb54fdf-aafb-4746-96bc-25b9f6588254)
     - Blackfynn (id: N:dataset:5a6779a4-e3d8-473f-91d0-0a99f144dc44)
     - Streaming (id: N:dataset:79627c2f-cd6c-4095-8f15-4114c80290ec)
     - Cameron's Dataset (id: N:dataset:8c02e00f-1b77-4f84-9e89-664443da13bb)
     - Patients (id: N:dataset:967ff102-d2d1-4e11-a8c8-a72c99d70b48)
     - Subjects (id: N:dataset:e4189eb0-6e66-47e6-8a23-80d81f4a0095)

Search for things

::

    >> bf search Fred
     * <TimeSeries name='Fred Tugwell' id='N:package:5385f12f-879e-4d9e-a3c2-b7ff798972d8'>
     * <TimeSeries name='Fred Heard' id='N:package:a3e6f016-f9b7-44f3-bb74-0a027935fba6'>

Show specific item

.. code:: bash

    >> bf show 'N:package:1234-1234-1234-1234'

File uploads
~~~~~~~~~~~~

Upload a file into a Dataset.

.. code:: bash

    bf upload 'N:dataset:1234-1234-1234-1234' /path/to/my_data.nii.gz

If your environment variables are not set, you can also enter credentials

.. code:: bash

    bf upload --user=<email> --pass=<pass> 'N:dataset:1234-1234-1234-1234' /path/to/data_i_want_to_upload.mef

Append data into an existing TimeSeries object (note: append process currently only supports
timeseries data)

.. code:: bash

    bf append 'N:package:1234-1234-1234-1234' /path/to/data_i_want_to_append.mef
