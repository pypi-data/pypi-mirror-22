Microsoft Azure SDK for Python
==============================

This is the Microsoft Azure Resource Management Client Library.

Azure Resource Manager (ARM) is the next generation of management APIs that
replace the old Azure Service Management (ASM).

This package has been tested with Python 2.7, 3.3, 3.4 and 3.5.

For the older Azure Service Management (ASM) libraries, see
`azure-servicemanagement-legacy <https://pypi.python.org/pypi/azure-servicemanagement-legacy>`__ library.

For a more complete set of Azure libraries, see the `azure <https://pypi.python.org/pypi/azure>`__ bundle package.


Compatibility
=============

**IMPORTANT**: If you have an earlier version of the azure package
(version < 1.0), you should uninstall it before installing this package.

You can check the version using pip:

.. code:: shell

    pip freeze

If you see azure==0.11.0 (or any version below 1.0), uninstall it first:

.. code:: shell

    pip uninstall azure


Usage
=====

For code examples, see `Resource Management 
<https://azure-sdk-for-python.readthedocs.org/en/latest/resourcemanagement.html>`__
on readthedocs.org.


Provide Feedback
================

If you encounter any bugs or have suggestions, please file an issue in the
`Issues <https://github.com/Azure/azure-sdk-for-python/issues>`__
section of the project.


.. :changelog:

Release History
===============

1.0.0rc2 (2017-05-02)
+++++++++++++++++++++

- Add Managed Applications client

1.0.0rc1 (2017-04-11)
+++++++++++++++++++++

**Bug fixes**

- tag_count is now correctly an int and not a string
- deployment_properties is now required for all deployments operations as expected

**Breaking Changes**

- Locks moves to a new ApiVersion and brings several consistent naming refactoring and new methods

**Features**

To help customers with sovereign clouds (not general Azure),
this version has official multi ApiVersion support for the following resource type:

- Locks: 2015-01-01 and 2016-09-01
- Policy: 2016-04-01 and 2016-12-01
- Resources: 2016-02-01 and 2016-09-01

The following resource types support one ApiVersion:

- Features: 2015-12-01
- Links: 2016-09-01
- Subscriptions: 2016-06-01

0.31.0 (2016-11-10)
+++++++++++++++++++

**Breaking change**

- Resource.Links 'create_or_update' method has simpler parameters

0.30.2 (2016-10-20)
+++++++++++++++++++

**Features**

- Add Resource.Links client


0.30.1 (2016-10-17)
+++++++++++++++++++

**Bugfixes**

- Location is now correctly declared optional and not required.

0.30.0 (2016-10-04)
+++++++++++++++++++

* Preview release. Based on API version 2016-09-01.

0.20.0 (2015-08-31)
+++++++++++++++++++

* Initial preview release. Based on API version 2014-04-01-preview


