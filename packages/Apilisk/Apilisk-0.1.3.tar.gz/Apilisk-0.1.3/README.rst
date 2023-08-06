Apilisk
================================

Standalone rest client for Apiwatcher platform.

It can run testcases defined in Apiwatcher locally on you machine or on
CI server.

Installation
=================================

Currently Apilisk is distributed using Pypi, more options for download
are comming soon.

Linux
********************************

The best way is to create a virtual environment and then use *pip*.

.. code-block:: shell

  virtualenv env
  . env/bin/activate

  pip install Apilisk

You must have libcurl installed.

OS X
*********************************

On Mac we suggest to use *easy_install*, although *pip* should work as well.

.. code-block:: shell

  sudo easy_install Apilisk

Run
==================================
At first you need to have a team in Apiwatcher, so sign/log in.

You need to create a project and some testcases, otherwise there is nothing to
run. :) And finally you need to have a credentials (Client ID and
Client secret). This you can find under team settings - create a new pair and
download the configuration file for Apilisk.

Example file:

.. code-block::

  {
    "host": "https://api2.apiwatcher.com",
    "port": 443,
    "client_id": "YOUR_CLIENT_ID",
    "client_secret": "YOUR_CLIENT_SECRET",
    "agent_id": "My local agent"
  }

And now just run it :)

.. code-block:: shell

  apilisk -c apilisk.json -u -v 1 -d YOUR_DATASET_ID YOUR_PROJECT_HASH
