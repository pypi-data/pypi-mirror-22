#############
rst2db-opf.py
#############

A reST to DocBook converter (``rst2db-opf``) with an included Sphinx builder
  (openpowerfoundation.spinx_ext.docbook_builder).

These tools were forked and derived from the rst2db project by Abystrys hosted
at Abstrys_GitHub_.  The OpenPOWER Foundation project is now hosted at
OpenPOWER_Foundation_GitHub_.

.. _Abstrys_GitHub: https://github.com/Abstrys/rst2db
.. _OpenPOWER_Foundation_GitHub: https://github.com/OpenPOWERFoundation/rst2db-opf

Prerequisites
=============

Before installing rst2db-opf, you'll need the following prerequisites:

* libxml2 and headers (**libxml2** and **libxml2-dev**)
* Python bindings for libxml2 (**python-lxml** or **python3-lxml**)
* libxslt1 headers (**libxslt1-dev**)
* Python headers (**python-dev** or **python3-dev**)

**You can install these on Ubuntu / Debian** by running::

 sudo apt-get install libxml2 libxml2-dev libxslt1-dev

and *one* of the following, depending on your Python version::

 sudo apt-get install python3-lxml python3-dev

 sudo apt-get install python-lxml python-dev


Using the sphinx extension for OpenPOWER Projects
=================================================
[TODO: more information here]

Additional tooling documentation
================================

The following sections are provided for general tooling use but are not required for OpenPOWER
Foundation documentation support.

Using the command-line utilities
--------------------------------

::

 rst2db-opf <filename> [-e root_element] [-o output_file] [-t template_file]

Only the *filename* to process is required. All other settings are optional.

**Settings:**

.. list-table::
   :widths: 1 3

   * - -e root_element
     - set the root element of the resulting docbook file. If this is not specified, then 'section'
       will be used.

   * - -o output_file
     - set the output filename to write. If this is not specified, then output will be sent to
       stdout.

   * - -t template_file
     - set a template file to use to dress the output. You must have Jinja2 installed to use this
       feature.


DocBook template files
----------------------

When using a DocBook template file, use {{data.root_element}} and {{data.contents}} to represent the
root element (chapter, section, etc.) and {{data.contents}} to represent the transformed contents of
your ``.rst`` source.

For example, you could use a template that looks like this:

.. code-block:: xml

   <?xml version="1.0" encoding="utf-8"?>
   <!DOCTYPE {{data.root_element}} PUBLIC "-//OASIS//DTD DocBook XML V4.1.2//EN"
             "http://www.oasis-open.org/docbook/xml/4.1.2/docbookx.dtd">
   <{{data.root_element}}>
       {{data.contents}}
   </{{data.root_element}}>

A template is only necessary if you want to customize the output. A standard DocBook XML header will
be included in each output file by default.


Using the Sphinx builders
-------------------------

To build DocBook output with Sphinx, add `openpowerfoundation.sphinx_ext.docbook_builder` to the *extensions*
list in ``conf.py``::

 extensions = [
    ... other extensions here ...
    openpowerfoundation.sphinx_ext.docbook_builder
    ]

There are 3 configurable parameters for ``conf.py`` that correspond to
``rst2db-opf.py`` parameters:


.. list-table::
   :widths: 1 3

   * - *docbook_template_file*
     - template file that will be used to position the document parts. This should be a valid
       DocBook .xml file that contains  Requires Jinja2 to be
       installed if specified.

   * - *docbook_default_root_element*
     - default root element for a file-level document.  Default is 'section'.
     
   * - *docbook_standalone*
     - Boolean flag ('True' or 'False') to indicate if the individual XML files 
       should be marked as "standalone='yes'" The default value if not set is 'True'.
       **Note:** if the *docbook_template_file* parameter is used, the XML files will
       always be marked as "standalone='yes'".

For example:

.. code:: python

   docbook_template_file = 'dbtemplate.xml'
   docbook_default_root_element = chapter

Then, build your project using ``sphinx-build`` with the ``-b docbook`` option::

 sphinx-build source output -b docbook


License
=======

This software is provided under the `BSD 3-Clause`__ license. See the
`LICENSE`__ file for more details.

.. __: http://opensource.org/licenses/BSD-3-Clause
.. __: https://github.com/OpenPOWERFoundation/rst2db-opf/blob/master/LICENSE

For more information
====================

Contact: OpenPOWER System Software Work Group Chair <syssw-chair@openpowerfoundation.org>

