|Build Status| |Coverage Status| |PyPI| |PyPI| |Docker Pulls| |Image
Layers|

blobxfer
========

``blobxfer`` is an advanced data movement tool and library for Azure
Storage Blob and Files. With ``blobxfer`` you can copy your files into
or out of Azure Storage with the CLI or integrate the ``blobxfer`` data
movement library into your own Python scripts.

Major Features
--------------

-  Command-line interface (CLI) providing data movement capability to
   and from Azure Blob and File Storage
-  Standalone library for integration with scripts or other Python
   packages
-  High-performance design with asynchronous transfers and disk I/O
-  YAML configuration driven execution support
-  Resume support
-  Vectored IO support
-  ``stripe`` mode allows striping a single file across multiple blobs
   (even to multiple storage accounts) to break through single blob or
   fileshare throughput limits
-  ``replica`` mode allows replication of a file across multiple
   destinations including to multiple storage accounts
-  Synchronous copy with replication support (including block-level
   copies for Block blobs)
-  Client-side encryption support
-  Support all Azure Blob types and Azure Files for both upload and
   download
-  Advanced skip options for rsync-like operations
-  Store/restore POSIX filemode and uid/gid
-  Support reading/pipe from ``stdin``
-  Support reading from blob snapshots for downloading and synchronous
   copy
-  Configurable one-shot block upload support
-  Configurable chunk size for both upload and download
-  Automatic block size selection for block blob uploading
-  Automatic uploading of VHD/VHDX files as page blobs
-  Include and exclude filtering support
-  Rsync-like delete support
-  No clobber support in either direction
-  File logging support

Installation
------------

``blobxfer`` is on `PyPI <https://pypi.python.org/pypi/blobxfer>`__ and
on `Docker Hub <https://hub.docker.com/r/alfpark/blobxfer/>`__. Please
refer to the `installation
guide <https://github.com/Azure/blobxfer/blob/master/docs/01-installation.md>`__
on how to install ``blobxfer``.

Documentation
-------------

Please refer to the ```blobxfer``
documentation <https://github.com/Azure/blobxfer/blob/master/docs>`__
for more details and usage information.

Change Log
----------

For recent changes, please refer to the
`CHANGELOG.md <https://github.com/Azure/blobxfer/blob/master/CHANGELOG.md>`__
file.

--------------

This project has adopted the `Microsoft Open Source Code of
Conduct <https://opensource.microsoft.com/codeofconduct/>`__. For more
information see the `Code of Conduct
FAQ <https://opensource.microsoft.com/codeofconduct/faq/>`__ or contact
` <mailto:opencode@microsoft.com>`__ with any additional questions or
comments.

.. |Build Status| image:: https://travis-ci.org/Azure/blobxfer.svg?branch=master
   :target: https://travis-ci.org/Azure/blobxfer
.. |Coverage Status| image:: https://coveralls.io/repos/github/Azure/blobxfer/badge.svg?branch=master
   :target: https://coveralls.io/github/Azure/blobxfer?branch=master
.. |PyPI| image:: https://img.shields.io/pypi/v/blobxfer.svg
   :target: https://pypi.python.org/pypi/blobxfer
.. |PyPI| image:: https://img.shields.io/pypi/pyversions/blobxfer.svg
   :target: https://pypi.python.org/pypi/blobxfer
.. |Docker Pulls| image:: https://img.shields.io/docker/pulls/alfpark/blobxfer.svg
   :target: https://hub.docker.com/r/alfpark/blobxfer
.. |Image Layers| image:: https://images.microbadger.com/badges/image/alfpark/blobxfer:latest.svg
   :target: http://microbadger.com/images/alfpark/blobxfer


