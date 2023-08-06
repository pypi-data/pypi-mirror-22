HCP Upload Daemon
=================

**hcpupd** is a daemon that automatically uploads files to HCP.

It's using the Linux
`inotify kernel subsystem <https://en.wikipedia.org/wiki/Inotify>`_ to monitor
a folder (aka *watchdir*), sending every file that is moved or written to it to
HCP, immediately.

Features:

*   Two different upload modes:

    1.  Transfer the folder structure created in *watchdir* to HCP as it is

        *   human-readable
        *   performance-wise not the best possible solution
        *   not tolerant against filename duplicates (except if the Namespace
            has Versioning enabled)

    **or**

    2.  Obfuscate the folder structure on HCP by creating an UUID per file, used
        as filename as well as to construct a path to it

        *   best possible ingest performance
        *   64k folders created at max. (*to be precise: 256**2 + 256*)
        *   an unlimited number of **hcpupd**\ 's can write into the same Namespace
            without the risk of filename conflicts
        *   supports search for the original filename by adding an annotation to
            each file, which can be used by *HCP's Metadata Query Engine*,
            *Hitachi Content Intelligence* or any other indexer that is able to
            crawl a HCP Namespace

*   Optionally, auto-delete files from *watchdir* after successful upload
*   Optionally, auto-delete folders after the last file has been uploaded
*   Made to run as a Linux daemon (but can run in an interactive session as
    well)
*   Extended logging available, incl. log rotation

Dependencies
------------

A binary is provided (`here <https://gitlab.com/simont3/hcpupd/blob/master/src/dist/hcpupd>`_)
which *should* run on most up-to-date Linux derivates. No specific dependencies
exist for it.

If you want to build the binary yourself (or just run the Python script
directly), you need to have at least Python 3.4.3 installed. See the
documentation for details.

Documentation
-------------

To be found at `readthedocs.org <http://hcpupd.readthedocs.io>`_

Installation
------------

Install **hcpupd** by running::

    $ pip install hcpupd


-or-

get the source from `gitlab.com <https://gitlab.com/simont3/hcpupd>`_,
unzip and run::

    $ python setup.py install


-or-

Fork at `gitlab.com <https://gitlab.com/simont3/hcpupd>`_

Contribute
----------

- Source Code: `<https://gitlab.com/simont3/hcpupd>`_
- Issue tracker: `<https://gitlab.com/simont3/hcpupd/issues>`_

Support
-------

If you've found any bugs, please let me know via the Issue Tracker;
if you have comments or suggestions, send an email to `<sw@snomis.de>`_

License
-------

The MIT License (MIT)

Copyright (c) 2017 Thorsten Simons (sw@snomis.de)

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
