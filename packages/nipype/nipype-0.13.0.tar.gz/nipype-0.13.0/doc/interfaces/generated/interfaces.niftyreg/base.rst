.. AUTO-GENERATED FILE -- DO NOT EDIT!

interfaces.niftyreg.base
========================


.. _nipype.interfaces.niftyreg.base.NiftyRegCommand:


.. index:: NiftyRegCommand

NiftyRegCommand
---------------

`Link to code <http://github.com/nipy/nipype/tree/ec86b7476/nipype/interfaces/niftyreg/base.py#L55>`__

Wraps command **None**

Base support interface for NiftyReg commands.

Inputs::

        [Mandatory]

        [Optional]
        args: (a unicode string)
                Additional parameters to the command
                flag: %s
        environ: (a dictionary with keys which are a bytes or None or a value
                 of class 'str' and with values which are a bytes or None or a value
                 of class 'str', nipype default value: {})
                Environment variables
        ignore_exception: (a boolean, nipype default value: False)
                Print an error message instead of throwing an exception in case the
                interface fails to run
        omp_core_val: (an integer (int or long), nipype default value: 4)
                Number of openmp thread to use
                flag: -omp %i
        terminal_output: ('stream' or 'allatonce' or 'file' or 'none')
                Control terminal output: `stream` - displays to terminal immediately
                (default), `allatonce` - waits till command is finished to display
                output, `file` - writes output to file, `none` - output is ignored

Outputs::

        None

.. module:: nipype.interfaces.niftyreg.base


.. _nipype.interfaces.niftyreg.base.get_custom_path:

:func:`get_custom_path`
-----------------------

`Link to code <http://github.com/nipy/nipype/tree/ec86b7476/nipype/interfaces/niftyreg/base.py#L33>`__





