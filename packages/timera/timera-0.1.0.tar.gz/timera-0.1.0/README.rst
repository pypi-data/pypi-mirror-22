Timera
======

Store stats in InfluxDB.

.. figure:: docs/img/plugin-httptimer-grafana-dashboard-1.png
   :scale: 50 %
   :alt: Grafana Dashboard

   Grafana Dashboard

There's currently one plugin included with Timera, ``httptimer``.

With ``httptimer``, you can store the time it takes to get http responses. For example:

.. code-block:: ini

    [httptimer_plugin_01]
    name = www.google.com
    url = https://www.google.com/
    proxy = http://proxy.example.com:3128/
    include_direct = true

See the config file, `config.ini <https://github.com/natej/timera/blob/master/config.ini>`_, for options.

Use any InfluxDB-compatible visualization software to view your stats. For example:

- `Chronograf <https://portal.influxdata.com/downloads>`_
- `Grafana <http://docs.grafana.org/features/datasources/influxdb/>`_

Timera has a simple plugin system. So it's easy to write your own plugin to collect the stats you want.
Use `httptimer <https://github.com/natej/timera/blob/master/timera/plugins/httptimer/>`_  as an example.

Requirements
------------

- `InfluxDB <https://portal.influxdata.com/downloads>`_
- `Python <https://www.python.org/>`_ 2.7 or 3.6, pip and setuptools.

Install
-------

.. code-block:: bash

    $ pip install timera

Or if using a virtual environment:

.. code-block:: bash

    $ source env/bin/activate
    $ pip install timera

Development Install
-------------------

Use ``make install-dev`` to install in editable mode (``pip install -e .``) with pytest and tox:

.. code-block:: bash

    $ source env/bin/activate
    $ cd timera-master
    $ make install-dev
    $ make test
    $ tox

Run It
------

Create db and start collecting stats:

.. code-block:: bash

    # edit config.ini
    $ timera config.ini reset_db
    $ timera config.ini start

Optional
--------

Use `Supervisor <https://github.com/Supervisor/supervisor>`_ to run Timera. See the
`contrib dir <https://github.com/natej/timera/blob/master/contrib/>`_. Supervisor requires
Python 2 (``pip install supervisor``).

Viewing Stats with Grafana
--------------------------

Configure `InfluxDB as a datasource <http://docs.grafana.org/features/datasources/influxdb/>`_.

For the ``httptimer`` plugin, create a `graph panel <http://docs.grafana.org/features/panels/graph/>`_ and
configure the query:

.. figure:: docs/img/plugin-httptimer-grafana-metrics-tab-1.png
   :scale: 50 %
   :alt: Grafana Metrics Tab

   Grafana Metrics Tab
