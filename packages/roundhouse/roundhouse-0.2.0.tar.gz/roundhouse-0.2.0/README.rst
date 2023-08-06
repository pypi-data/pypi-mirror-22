==========
Roundhouse
==========


.. image:: https://img.shields.io/pypi/v/roundhouse.svg
    :target: https://pypi.python.org/pypi/roundhouse

.. image:: https://img.shields.io/travis/nick-allen/python-roundhouse.svg
    :target: https://travis-ci.org/nick-allen/python-roundhouse

.. image:: https://readthedocs.org/projects/roundhouse/badge/?version=latest
    :target: https://roundhouse.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status

Convert many serialization formats to many formats

----------


Installation
------------

Install CLI bundled with base package

Comes with just JSON and Pickle serializers by default, no external dependencies

.. code-block:: bash

    pip install roundhouse

Install one or more additional serializers and their dependencies

See :mod:`roundhouse.contrib.serializers` for list of available bundled serializers

.. code-block:: bash

    pip install roundhouse[yaml] roundhouse[msgpack] ...

Or install all builtin serializers and dependencies bundled with core package

.. code-block:: bash

    pip install roundhouse[all]

Additional serializer plugins can be published and installed via pypi/pip using the `roundhouse` setuptools entrypoint
pointing to module/package containing additional serializer classes


Usage
-----

CLI
^^^

The `rh` CLI command is installed automatically, and defaults to reading from stdin and writing stdout

Run `rh --help` for full usage instructions

.. code-block:: bash

    echo '{"root": {"nested": {"key": "value"}}}' | rh -i json -o xml

    <?xml version="1.0" encoding="utf-8"?>
    <root><nested><key>value</key></nested></root>

Python
^^^^^^

Data is serialized/deserialized to and from :class:`dict` instances

Other data types may be supported depending on the serializer

Use the :meth:`roundhouse.serialize` and :meth:`roundhouse.deserialize` functions with target format

.. code-block:: python

    from roundhouse import serialize, deserialize

    data = deserialize('{"root": {"nested": {"key": "value"}}}', 'json')
    print(serialize(data, 'xml'))
