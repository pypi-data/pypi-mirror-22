**********
pytellprox
**********

This is a simple project that gives easy access to the tellprox API in Python.
The Tellprox project, which can be used in place of Telldus Live, can be found here: https://github.com/p3tecracknell/tellprox

There is not much code, but after using this for a good while it seemed good to clean up a bit and push upstream.

============
Installation
============

::
    pip install pytellprox

=====
Usage
=====
::

    from tellprox import TellProx
    tellprox_device_id=1
    tellprox_host='localhost'
    tellprox_port='8080'
    tellprox = TellProx(host=tellprox_host, port=tellprox_port)
    # if you need HTTPS you can pass protocol='https' as well
    tellprox.enable_device(tellprox_device_id)
    tellprox.toggle_device(tellprox_device_id)
