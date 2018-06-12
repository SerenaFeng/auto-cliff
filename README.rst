Cliff Generator
=================

This tool is developed to generate a cli project leveraging cliff_

Config File
-------------

The items and syntax in config file would be:

.. code-block:: YAML

    # must be provided
    project: cliffg-example

    # if not provided, empty
    summary: A project to test cliff-generator

    # if not provided, empty
    author: SerenaFeng

    # if not provided, empty
    author-email: serena.feng.711@gmail.com

    # if not provided, leverage https://github.com/{author}/{project}
    home-page: https://github.com/SerenaFeng/cliffg-example

    # if not provide, substitute - with _ in {project}
    #package: cliffg_example

    # if not provide, leverage {project} directly
    #cli: cliffg-example

    subs:
      sub1: [create, show, list, delete]
      sub2: [create, update, show]

    # support communicating with other components using RESTful API
    use_rest: False

Usage
--------

.. code-block:: Shell

    cliffg -rm -o ~/ <conf_file>

``-rm``: whether to remove existed project directory or not

``-o``: the output directory, './' by default

``conf_file``: config file path, the config file must be a yaml file,
such as *./conf.yaml*

An example please reference cliffg-example_

References
--------------

.. _cliff: https://docs.openstack.org/cliff/latest/
.. _cliffg-example: https://github.com/SerenaFeng/cliffg-example