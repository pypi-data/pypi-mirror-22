====================
CRX Unpack in Python
====================

|pkg_version| |docs| |python_versions| |license_type|

.. main_intro

This module contains several utilities for working with Google Chrome extension files (CRXs), which have the ``*.crx``
file extension. The goal of this project is to mimic as closely as possible the functionality of Google Chrome when
these extensions are unpacked and installed.

.. end_main_intro

Documentation
-------------

Please view the full documentation for this project on `Read the Docs`_.

.. begin_import

Installation
------------

Since ``crx_unpack`` is available on `PyPI`_, you can install it using `pip`_:

::

    $ pip install crx_unpack


Structure of CRX Package Format
-------------------------------

The information in this section introduces the structure and contents of CRX files.

*As explained at* `<https://developer.chrome.com/extensions/crx>`_

Package Header
^^^^^^^^^^^^^^

The header contains the author's public key and the extension's signature. The signature is generated from the ZIP file
using SHA-1 with the author's private key. The header requires a little-endian byte ordering with 4-byte alignment. The
following table describes the fields of the ``.crx`` header in order:

===================  ============  ===============  =================  ===========
Field                Type          Length           Value              Description
===================  ============  ===============  =================  ===========
*magic number*       char[]        32 bits          Cr24               Chrome requires this constant at the beginning of every ``.crx`` package.
*version*            unsigned int  32 bits          2                  The version of the ``*.crx`` file format used (currently 2).
*public key length*  unsigned int  32 bits          *pubkey.length*    The length of the RSA public key in *bytes*.
*signature length*   unsigned int  32 bits          *sig.length*       The length of the signature in *bytes*.
*public key*         byte[]        *pubkey.length*  *pubkey.contents*  The contents of the author's RSA public key formatted as an X509 SubjectPublicKeyInfo block.
*signature*          byte[]        *sig.length*     *sig.contents*     The signature of the ZIP content using the author's private key. The signature is created using the RSA algorithm with the SHA-1 hash function.
===================  ============  ===============  =================  ===========

Extension Contents
^^^^^^^^^^^^^^^^^^

The extension's ZIP file is appended to the ``*.crx`` package after the header. This should be the same ZIP file that
the signature in the header was generated from.


.. |pkg_version| image:: https://img.shields.io/pypi/v/crx_unpack.svg
    :alt: Package version
    :target: `PyPI`_

.. |docs| image:: https://readthedocs.org/projects/crx-unpack/badge/
    :alt: Documentation Status
    :target: `Read the Docs`_

.. |python_versions| image:: https://img.shields.io/pypi/pyversions/crx_unpack.svg
    :alt: Python versions supported
    :target: `PyPI`_

.. |license_type| image:: https://img.shields.io/pypi/l/crx_unpack.svg
    :alt: License: MIT
    :target: `PyPI`_

.. _PyPI: https://pypi.python.org/pypi/crx_unpack

.. _Read the Docs: http://crx-unpack.readthedocs.io/

.. _pip: https://pip.pypa.io/en/stable/installing/
