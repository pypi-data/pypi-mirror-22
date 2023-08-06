confutil
========

Configuration utility to ease navigation of local and system configurations

Installation
------------

From the project root directory::

    $ python setup.py install

Or install with pip::

    $ pip install confutil

Usage
-----

Example::

    from confutil import Config
    conf = Config('spam')
    password = conf['password']

That will pull the first password value from a search through this sequence:

    - ./.spam.conf
    - ./.spam.cfg
    - ~/.spam.conf
    - ~/.spam.cfg
    - ~/.config/.spam.conf
    - ~/.config/.spam.cfg
    - ~/.config/spam/config.conf
    - ~/.config/spam/config.cfg
    - ~/.config/spam/config
    - /etc/.spam.conf
    - /etc/.spam.cfg
    - /etc/spam/config.conf
    - /etc/spam/config.cfg
    - /etc/spam/config

To write out a loaded configuration::
    
    from confutil import Config
    c = Config('myapp')
    c.write('output_path.cfg')

To print a derived configuration from the current directory, run::

    $ confutil $PROJECT_NAME

To output it to a new file, run::
    
    $ confutil $PROJECT_NAME -o output_path.cfg

Release Notes
-------------

:0.1.3:
    Add ``get_in(key)`` and ``get_as(key, type=str)``
:0.0.1:
    Project created
