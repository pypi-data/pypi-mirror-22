
ModConf
=======

Pattern for using python modules as configuration files

Install
-------

::

    pip3 install modconf

Example
-------

::

    from modconf import import_conf

    conf = import_conf('module_name', 'optional module search path')

``conf`` is simply the module loaded using ``__import__``


