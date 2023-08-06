kon
===

.. contents:: Table of contents


Overview
--------

`kon`_ is a very simple configuration file(s) management system that parses one or more configuration files in a path and provides an object tree that can be accessed directly. It also attempts to parse the data as concrete types so that you don't have to explicitly get specific types, only for `INI`_ files. This does introduce some constraints and deviations from default implementations in python, but the convenience is generally worth it. Moreover this behavior can be overridden. kon currently handles only `INI`_ and `JSON`_ files.


Installation
------------

Install the extension using ``pip``:

.. code:: bash

    $ pip install kon

or ``easy_install``:

.. code:: bash

    $ easy_install kon


Usage
-----

Basic Usage
+++++++++++

You can instantiate a ``Konfig`` object by calling its constructor:

.. code:: python

    from kon import Konfig

    cfg = Konfig('/path/to/folder/or/ini-file')
    # this can also accept options for loading by handlers
    cfg.load()

The load method will try to get an appropriate file handler based on the filename extension. If none exists, it will skip that file. The file handlers are instantiated with any default values you may want to provide the configuration. For each file handler it then calls the instance's ``load`` method. This method can accept handler specific loading options. Currently supported handlers and their behaviors are documented below.

If you want to specify default arguments, you can pass them in as keywords arguments to the constructor and they are passed through to the file handlers used to load the files.

.. code:: python

    from kon import Konfig

    cfg = Konfig('/path/to/folder/or/ini-file', a=1, b=2.2, c=False)
    cfg.load()

Load Behavior
~~~~~~~~~~~~~

The ``load`` method does a couple of things.

- It will walk the directory tree starting from the root directory you provide in the constructor call and create objects per directory as it goes along.
- Once it encounters a file, it will try to get a file handler for that type of file.
- If it cannot get a file handler, the file will be skipped.
- If it can get the file handler, it will instantiate it, pass it in the defaults it got and then call *it's* ``load`` method passing in any parameters it got.

For e.g. if you have a directory tree like the following:

::

    kon
    ├── a.ini
    ├── b
    │   ├── c.ini
    │   ├── d.json
    │   ├── e
    │   │   └── e.ini
    │   ├── g.json
    │   └── h.ini
    ├── i.ini
    ├── j.ini
    └── k.ini

The corresponding object tree created by ``load`` before calling the handlers load will be exactly like the tree above sans the filename extension.

In the event that you have a folder and a file by the same prefix, for e.g.:

::

    kon
    ├── a.ini
    └── a.ini
        └── c.ini

it will result in a single object kon.a with merged sub-children.


JSONFileHandler
+++++++++++++++

This handler parses `JSON`_ files that it finds in the path specified or an individual file if it is so specified. Internally it delegates to the default python ``json`` library.

Options
~~~~~~~

``preserve_case``
    If set to ``false`` normalizes the key names to be lower case. By default the json loads function preserves case. This is the opposite of what happens with `INIFileHandler`_.
``encoding``
    Passthrough option for `json.loads`_


INIFileHandler
++++++++++++++

This handler parses `INI`_ files that it finds in the path specified or an individual file if it is so specified. Internally it uses `SafeConfigParser`_ to load and parse the files. The individual sections, options and values are processed again.

Options
~~~~~~~

``preserve_case``
    If set to ``true`` preserves the case of the option names. Sections are still *case-insensitive*. By default ``SafeConfigParser`` normalizes all option names to lower case. This will prevent that.
``dict_type``
    Passthrough option for ``SafeConfigParser``, see below
``allow_no_value``
    Passthrough option for ``SafeConfigParser``, see below

Customizing SafeConfigParser
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If you want to customize the way the internal `SafeConfigParser`_ works you can use the arguments as specified in the `RawConfigParser`_ constructor documentation and pass them to the ``load`` method call on a ``Konfig`` instance.

.. warning::
    Do not pass in the defaults argument as that will be *ignored*. The defaults that are sent to the parser should be provided as keyword arguments to the constructor.

For example:

.. code:: python

    cfg = Konfig('/path/to/folder/or/ini-file')
    cfg.load(dict_type=OrderedDict, allow_no_value=True)


Implementation Details
~~~~~~~~~~~~~~~~~~~~~~

``Konfig`` uses `SafeConfigParser`_ to load the INI file. Consequently you get the built-in parsing and interpolation capabilities of the parser.

Because ``SafeConfigParser`` does not automatically coerce the values to an appropriate type, `kon`_ will try to do it's best to do some for you. The following cast attempts are made in order of precedence:

    * `int`_
    * `float`_
    * `boolean`_
    * list, dict or tuple (using `ast.literal_eval <https://docs.python.org/2/library/ast.html#ast.literal_eval>`_)

.. note::
    * The behavior deviates from ``SafeConfigParser``'s treatment of boolean because a type-coercion to `int`_ happens before a type-coercion to `boolean`_. So if you want a boolean set it to one of ``yes, no, on, off, true or false`` only.



.. _Kon: https://bitbucket.org/wampeter/kon
.. _INI: https://en.wikipedia.org/wiki/INI_file
.. _JSON: http://json.org
.. _ConfigParser: https://docs.python.org/2/library/configparser.html
.. _SafeConfigParser: https://docs.python.org/2/library/configparser.html#safeconfigparser-objects
.. _int: https://docs.python.org/2/library/configparser.html#ConfigParser.RawConfigParser.getint>
.. _float: https://docs.python.org/2/library/configparser.html#ConfigParser.RawConfigParser.getfloat>
.. _boolean: https://docs.python.org/2/library/configparser.html#ConfigParser.RawConfigParser.getboolean
.. _RawConfigParser: https://docs.python.org/2/library/configparser.html#ConfigParser.RawConfigParser
.. _json.loads: https://docs.python.org/2.7/library/json.html#json.loads
