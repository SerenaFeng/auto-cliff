Cliff Generator
=================

This tool is developed to generate a cli project leveraging cliff_

Config File
-------------

The items and syntax in config file would be:

.. code-block:: YAML

    # must be provided
    project: grafana-client

    # if not provided, empty
    summary: a tool used to generate Grafana Dashboard

    # if not provided, empty
    author: SerenaFeng

    # if not provided, empty
    author-email: serena.feng.711@gmail.com

    # if not provided, leverage https://github.com/{author}/{project}
    home-page: https://github.com/SerenaFeng/Grafana-client

    # if not provide, substitute - with _ in {project}
    package: grafana_client

    # if not provide, leverage {project} directly
    #cli: grafana-client

    subs:
      dashboard: [create, update, show, list, delete]
      folder: [create, update, show, list, delete]
      datasource: [create, update, show, list, delete]

Usage
--------

.. code-block:: Shell

    cliffg -rm -o ~/ <conf_file>

``-rm``: whether to remove existed project directory or not

``-o``: the output directory, './' by default

``conf_file``: config file path, the config file must be a yaml file,
               such as *./conf.yaml*

References
--------------

.. [cliff] https://docs.openstack.org/cliff/latest/