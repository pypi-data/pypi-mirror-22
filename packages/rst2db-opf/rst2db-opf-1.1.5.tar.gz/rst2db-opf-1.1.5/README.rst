#############
rst2db-opf.py
#############

A reST to DocBook converter (``rst2db-opf``) with an included Sphinx builder
  (openpowerfoundation.spinx_ext.docbook_builder).

These tools were forked and derived from the rst2db project by Abystrys hosted
at Abstrys_GitHub_.  The OpenPOWER Foundation (OPF) project is now hosted at
OpenPOWER_Foundation_GitHub_.  The python distribution package is available at
Python_Package_Index_rst2db-opf_Project_.

.. _Abstrys_GitHub: https://github.com/Abstrys/rst2db/
.. _OpenPOWER_Foundation_GitHub: https://github.com/OpenPOWERFoundation/rst2db-opf/
.. _Python_Package_Index_rst2db-opf_Project: https://pypi.python.org/pypi/rst2db-opf/

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

This package is used to assist OpenPOWER Foundation projects with RST-based documentation
(such as SkiBoot_) convert their documents to the OpenPOWER Foundation look-and-feel.  This
is accomplished by extending the sphinx-build environment commonly used, to build OPF-type
PDF and html products.  This is accomplished during the build by converting the the RST 
files to XML (DocBook) and programmatically merging them with OpenPOWER Foundation 
maven-based document builds.

The steps to accomplish this are as follows:

1. Install this package from PyPI by running::

     sudo -H pip install rst2db-opf

2. Update the ``sphinx-build`` extensions in the ``conf.py`` file to include
   this one with the following line::

     extensions = [
        ... other extensions here ... ,
        openpowerfoundation.sphinx_ext.docbook_builder
        ]

3. Also add the following lines to ``conf.py`` file to enhance the 
   ``sphinx-build`` environment::

     # -- Options for Docbook output -------------------------------------------
     docbook_default_root_element = 'section'
     docbook_standalone = 'False'

     # -- Settings for OpenPOWER Foundation Docbook output ---------------------
     # The following structure defines which files and tags in the OpenPOWER
     # Foundation Docs-Template/rst_template directory get updated.  The
     # opf_docbook.py file imports conf.py (this file) and uses the
     # opf_docbook_settings structure to replace tags in the respected files.
     #
     # The structure of the following hash is:
     #
     #   { file_name : { tag_name : tag_value, ... }, ... }
     #
     # The GitHub project containing the template and the tool can be
     # located at https://github.com/OpenPOWERFoundation/Docs-Template
     #
     opf_docbook_settings = {
         u'pom.xml' :    { u'artifactId' : u'<TBD>',
                           u'name' : u'<TBD>',
                           u'disqusShortname' : u'<TBD>',
                           u'webhelpDirname' : u'<TBD>',
                           u'pdfFilenameBase' : u'<TBD>',
                           u'workProduct' : u'<TBD: workgroupNotes, workgroupSpecification, candidateStandard, or openpowerStandard>',
                           u'security' : u'<TBD: public, workgroupConfidential, or foundationConfidential>',
                           u'documentStatus' : u'<TBD: draft, review, or published>' },
                            
         u'bk_main.xml': { u'title' : u'<TBD>',
                           u'subtitle' : u'<TBD>',
                           u'personname' : u'<TBD>',
                           u'email' : u'<TBD>',
                           u'year' : u'<TBD>',
                           u'holder' : u'<TBD>',
                           u'releaseinfo' : u'<TBD>',
                           u'abstract' : u'<TBD>' }
         }

   Please replace the values in ``opf_docbook_settings`` marked "<TBD...>" 
   with appropriate values for the project.  A sample solution can be found in the 
   SkiBoot_doc_conf.py_ file in GitHub.  More details about each field can
   be found in the OpenPOWER_Foundation_Document_Development_Guide_.
   
4. Enhance the ``sphinx-build`` ``Makefile`` with the following updates

   * General environment settings needed near the top of the file::

       # Variables for OPF Docbook conversion
       RMDIR         = rm -rf
       DBEXT         = rst2db-opf
       GIT           = git
       CP            = cp
       MAVEN         = mvn
       OPFMASTER     = https://github.com/OpenPOWERFoundation/Docs-Master.git
       OPFTEMPLATE   = https://github.com/OpenPOWERFoundation/Docs-Template.git
       DBDIR         = $(BUILDDIR)/docbook
       MASTERDIR     = $(BUILDDIR)/Docs-Master
       TEMPLATEDIR   = $(BUILDDIR)/Docs-Template
       OPFBLDDIR     = $(TEMPLATEDIR)/rst_template
       OPFDOCDIR     = $(OPFBLDDIR)/target/docbkx/webhelp
       OPFDBDIR      = $(DBDIR)/opf_docbook
       PROCXML       = opf_docbook.py

   
   * A set of commands to build the new make target, ``docbook``.  Copy the following
     lines unchanged into the bottom of the ``Makefile``::

       docbook:
         # User-friendly check for docbook extension (opf_rst2db)
         ifeq ($(shell which $(DBEXT) >/dev/null 2>&1; echo $$?), 1)
         $(error The '$(DBEXT)' command was not found. Make sure you have Sphinx extension rst2db-opf installed. Grab it from https://pypi.python.org/pypi/rst2db-opf or pip install rst2db-opf.)
         endif

         # User-friend check for git
         ifeq ($(shell which $(GIT) >/dev/null 2>&1; echo $$?), 1)
         $(error The '$(GIT)' command was not found. Make sure you have git installed.
         endif

       	 $(RMDIR) $(DBDIR)/doctrees/
       	 $(SPHINXBUILD) -v -b docbook $(ALLSPHINXOPTS) $(DBDIR)
       	 $(RMDIR) $(DBDIR)/doctrees/
       	 @echo
       	 @echo "Build finished. The XML files are in $(DBDIR)."
       	 @echo "Cloning OpenPOWER Docbook template information"
       	 if [ -d $(MASTERDIR) ]; then $(RMDIR) $(MASTERDIR);	fi;
       	 $(GIT) clone $(OPFMASTER) $(MASTERDIR)
         if [ -d $(TEMPLATEDIR) ];  then $(RMDIR) $(TEMPLATEDIR); fi;
         $(GIT) clone $(OPFTEMPLATE) $(TEMPLATEDIR)
         @echo "Retrieving conversion program from $(OPFBLDDIR)"
       	 $(CP) $(OPFBLDDIR)/$(PROCXML) .
       	 @echo "Starting conversion code"
       	 python $(PROCXML) -b $(BUILDDIR) -d $(DBDIR) -m $(MASTERDIR) -t $(TEMPLATEDIR)
       	 @echo
       	 @echo "Conversion done, building OPF documents"
       	 cd $(OPFBLDDIR); \
       	 $(MAVEN) generate-sources
       	 if [ -d $(OPFDOCDIR) ]; then cp -a $(OPFDOCDIR)/ $(OPFDBDIR); fi;
       	 @echo
       	 @echo "If build was successful, PDF and HTML will be found in $(OPFDBDIR)

   Other updates such as command help text in the (``help:`` target) may be necessary.
   For a working ``Makefile`` example, see the SkiBoot_doc_Makefile_ in GitHub.
       	
For more information about the above setting or the conversion process
in general, consult the OpenPOWER_Foundation_Document_Development_Guide_.
  
.. _SkiBoot: https://github.com/open-power/skiboot/
.. _SkiBoot_doc_conf.py: https://github.com/open-power/skiboot/blob/master/doc/conf.py
.. _SkiBoot_doc_Makefile: https://github.com/open-power/skiboot/blob/master/doc/Makefile
.. _OpenPOWER_Foundation_Document_Development_Guide: https://openpowerfoundation.org/?resource_lib=openpower-foundation-documentation-development-guide

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
    ... other extensions here ... ,
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

