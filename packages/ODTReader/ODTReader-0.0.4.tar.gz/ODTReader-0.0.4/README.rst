##################
ODTReader
##################

Lightweight python module for extracting raw text from OpenDocument (odt) files.

Linux, macOS and Windows platforms supported.

Just point at the file with the ``.odt`` extension and let it print it out for you.

Installation
============
::

    $ pip install odtreader

Usage
=====

You can simply use it by calling the ``odtToText()`` function. The file is parsed and the text returned to you as a ``unicode`` object.


**Example:**

.. sourcecode:: python

   from ODTReader.odtreader import odtToText
   
   text = odtToText("path/to/file.odt")




It can also be used as a command line utility.


**Example:**
::

    $ python odtreader.py path/to/file.odt
    This is the contents of the odt file!
    
    $ python odtreader.py path/to/file.odt -o outfile.txt
    Contents written to 'outfile.txt' 


Version Support
===============

This module only supports Python 2.7 as of now.


License
=======

`GNU GPL v3.0 License <https://github.com/KaneGalba/ODTReader/blob/master/LICENSE>`_, see LICENSE file.

