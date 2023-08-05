.. AUTO-GENERATED FILE -- DO NOT EDIT!

sphinxext.plot_workflow
=======================


.. module:: nipype.sphinxext.plot_workflow


.. _nipype.sphinxext.plot_workflow.contains_doctest:

:func:`contains_doctest`
------------------------

`Link to code <http://github.com/nipy/nipype/tree/ec86b7476/nipype/sphinxext/plot_workflow.py#L273>`__






.. _nipype.sphinxext.plot_workflow.get_wf_formats:

:func:`get_wf_formats`
----------------------

`Link to code <http://github.com/nipy/nipype/tree/ec86b7476/nipype/sphinxext/plot_workflow.py#L476>`__






.. _nipype.sphinxext.plot_workflow.mark_wf_labels:

:func:`mark_wf_labels`
----------------------

`Link to code <http://github.com/nipy/nipype/tree/ec86b7476/nipype/sphinxext/plot_workflow.py#L198>`__



To make graphs referenceable, we need to move the reference from
the "htmlonly" (or "latexonly") node to the actual figure node
itself.


.. _nipype.sphinxext.plot_workflow.out_of_date:

:func:`out_of_date`
-------------------

`Link to code <http://github.com/nipy/nipype/tree/ec86b7476/nipype/sphinxext/plot_workflow.py#L392>`__



Returns True if derivative is out-of-date wrt original,
both of which are full file paths.


.. _nipype.sphinxext.plot_workflow.remove_coding:

:func:`remove_coding`
---------------------

`Link to code <http://github.com/nipy/nipype/tree/ec86b7476/nipype/sphinxext/plot_workflow.py#L305>`__



Remove the coding comment, which exec doesn't like.


.. _nipype.sphinxext.plot_workflow.render_figures:

:func:`render_figures`
----------------------

`Link to code <http://github.com/nipy/nipype/tree/ec86b7476/nipype/sphinxext/plot_workflow.py#L499>`__



Run a nipype workflow creation script and save the graph in *output_dir*.
Save the images under *output_dir* with file names derived from
*output_base*


.. _nipype.sphinxext.plot_workflow.run:

:func:`run`
-----------

`Link to code <http://github.com/nipy/nipype/tree/ec86b7476/nipype/sphinxext/plot_workflow.py#L532>`__






.. _nipype.sphinxext.plot_workflow.run_code:

:func:`run_code`
----------------

`Link to code <http://github.com/nipy/nipype/tree/ec86b7476/nipype/sphinxext/plot_workflow.py#L406>`__



Import a Python module from a path, and run the function given by
name, if function_name is not None.


.. _nipype.sphinxext.plot_workflow.setup:

:func:`setup`
-------------

`Link to code <http://github.com/nipy/nipype/tree/ec86b7476/nipype/sphinxext/plot_workflow.py#L229>`__






.. _nipype.sphinxext.plot_workflow.unescape_doctest:

:func:`unescape_doctest`
------------------------

`Link to code <http://github.com/nipy/nipype/tree/ec86b7476/nipype/sphinxext/plot_workflow.py#L285>`__



Extract code from a piece of text, which contains either Python code
or doctests.


.. _nipype.sphinxext.plot_workflow.wf_directive:

:func:`wf_directive`
--------------------

`Link to code <http://github.com/nipy/nipype/tree/ec86b7476/nipype/sphinxext/plot_workflow.py#L161>`__



:mod:`nipype.sphinxext.plot_workflow` -- Workflow plotting extension
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


A directive for including a nipype workflow graph in a Sphinx document.

This code is forked from the plot_figure sphinx extension of matplotlib.

By default, in HTML output, `workflow` will include a .png file with a
link to a high-res .png.  In LaTeX output, it will include a
.pdf.
The source code for the workflow may be included as **inline content** to
the directive `workflow`::

  .. workflow ::
      :graph2use: flat
      :simple_form: no

      from nipype.workflows.dmri.camino.connectivity_mapping import create_connectivity_pipeline
      wf = create_connectivity_pipeline()


For example, the following graph has been generated inserting the previous
code block in this documentation:

.. workflow ::
  :graph2use: flat
  :simple_form: no

  from nipype.workflows.dmri.camino.connectivity_mapping import create_connectivity_pipeline
  wf = create_connectivity_pipeline()


Options
~~~~~~~

The ``workflow`` directive supports the following options:
    graph2use : {'hierarchical', 'colored', 'flat', 'orig', 'exec'}
        Specify the type of graph to be generated.
    simple_form: bool
        Whether the graph will be in detailed or simple form.
    format : {'python', 'doctest'}
        Specify the format of the input
    include-source : bool
        Whether to display the source code. The default can be changed
        using the `workflow_include_source` variable in conf.py
    encoding : str
        If this source file is in a non-UTF8 or non-ASCII encoding,
        the encoding must be specified using the `:encoding:` option.
        The encoding will not be inferred using the ``-*- coding -*-``
        metacomment.

Additionally, this directive supports all of the options of the
`image` directive, except for `target` (since workflow will add its own
target).  These include `alt`, `height`, `width`, `scale`, `align` and
`class`.

Configuration options
~~~~~~~~~~~~~~~~~~~~~

The workflow directive has the following configuration options:
    graph2use
        Select a graph type to use
    simple_form
        determines if the node name shown in the visualization is either of the form nodename
        (package) when set to True or nodename.Class.package when set to False.
    wf_include_source
        Default value for the include-source option
    wf_html_show_source_link
        Whether to show a link to the source in HTML.
    wf_pre_code
        Code that should be executed before each workflow.
    wf_basedir
        Base directory, to which ``workflow::`` file names are relative
        to.  (If None or empty, file names are relative to the
        directory where the file containing the directive is.)
    wf_formats
        File formats to generate. List of tuples or strings::
            [(suffix, dpi), suffix, ...]
        that determine the file format and the DPI. For entries whose
        DPI was omitted, sensible defaults are chosen. When passing from
        the command line through sphinx_build the list should be passed as
        suffix:dpi,suffix:dpi, ....
    wf_html_show_formats
        Whether to show links to the files in HTML.
    wf_rcparams
        A dictionary containing any non-standard rcParams that should
        be applied before each workflow.
    wf_apply_rcparams
        By default, rcParams are applied when `context` option is not used in
        a workflow directive.  This configuration option overrides this behavior
        and applies rcParams before each workflow.
    wf_working_directory
        By default, the working directory will be changed to the directory of
        the example, so the code can get at its data files, if any.  Also its
        path will be added to `sys.path` so it can import any helper modules
        sitting beside it.  This configuration option can be used to specify
        a central directory (also added to `sys.path`) where data files and
        helper modules for all code are located.
    wf_template
        Provide a customized template for preparing restructured text.

