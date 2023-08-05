pyads - Python package
======================

|Code Issues|

This is a python wrapper for TwinCATs ADS library. It provides python
functions for communicating with TwinCAT devices. *pyads* uses the C API
*AdsDLL.dll*. The documentation for the ADS API is available on
`infosys.beckhoff.com <http://infosys.beckhoff.com/english.php?content=../content/1033/tcadsdll2/html/tcadsdll_api_overview.htm&id=20557>`__.

Changelog
---------

Version 2.0.0
~~~~~~~~~~~~~

I wanted to make the Wrapper more pythonic so I created a new module
named pyads.ads that contains all the functions from pyads.pyads but in
a more pythonic way. You can still access the old functions by using the
pyads.pyads module.

Improvements:

-  more pythonic function names (e.g. 'write' instead of 'adsSyncWrite')
-  easier handling of reading and writing Strings
-  no error codes, if errors occur an Exception with the error code will
   be raised

Examples
--------

Open port and create a AmsAddr object for remote machine.

.. code:: python

    >>> import pyads
    >>> pyads.open_port()
    32828
    >>> pyads.get_local_address()
    <AmsAddress 192.168.0.109.1.1:32828>
    >>> adr = pyads.AmsAddr('5.33.160.54.1.1', 851)

You can read and write a variable by name from a remote machine.

.. code:: python

    >>> pyads.read_by_name(adr, 'global.bool_value', pyads.PLCTYPE_BOOL)
    True
    >>> pyads.write_by_name(adr, 'global.bool_value', False, pyads.PLCTYPE_BOOL)
    >>> pyads.read_by_name(adr, 'global.bool_value', pyads.PLCTYPE_BOOL)
    False

If the name could not be found an Exception containing the error message
and ADS Error number is raised.

.. code:: python

    >>> pyads.read_by_name(adr, 'global.wrong_name', pyads.PLCTYPE_BOOL)
    ADSError: ADSError: symbol not found (1808)

Reading and writing Strings is now easier as you don' t have to supply
the length of a string anymore. For reading strings the maximum buffer
length is 1024.

.. code:: python

    >>> pyads.read_by_name(adr, 'global.sample_string', pyads.PLCTYPE_STRING)
    'Hello World'
    >>> pyads.write_by_name(adr, 'global.sample_string', 'abc', pyads.PLCTYPE_STRING)
    >>> pyads.read_by_name(adr, 'global.sample_string', pyads.PLCTYPE_STRING)
    'abc'

Setting the ADS state and machine state.

::

    >>> pyads.write_control(adr, pyads.ADSSTATE_STOP, 0, 0)

Toggle bitsize variables by address.

.. code:: python

    >>> data = pyads.read(adr, INDEXGROUP_MEMORYBIT, 100*8 + 0, PLCTYPE_BOOL)
    >>> pyads.write(adr, INDEXGROUP_MEMORYBIT, 100*8 + 0, not data)

Read and write udint variable by address.

.. code:: python

    >>> pyads.write(adr, INDEXGROUP_MEMORYBYTE, 0, 65536, PLCTYPE_UDINT)
    >>> pyads.read(adr, INDEXGROUP_MEMORYBYTE, 0, PLCTYPE_UDINT)
    65536

Finally close the ADS port.

.. code:: python

    >>> pyads.close_port()

.. |Code Issues| image:: http://www.quantifiedcode.com/api/v1/project/3e884877fac4408ea0d33ec4a788a212/badge.svg
   :target: http://www.quantifiedcode.com/app/project/3e884877fac4408ea0d33ec4a788a212
