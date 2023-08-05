.. AUTO-GENERATED FILE -- DO NOT EDIT!

interfaces.niftyfit.base
========================


.. _nipype.interfaces.niftyfit.base.NiftyFitCommand:


.. index:: NiftyFitCommand

NiftyFitCommand
---------------

`Link to code <http://github.com/nipy/nipype/tree/ec86b7476/nipype/interfaces/niftyfit/base.py#L32>`__

Wraps command **None**

Base support interface for NiftyFit commands.

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
        terminal_output: ('stream' or 'allatonce' or 'file' or 'none')
                Control terminal output: `stream` - displays to terminal immediately
                (default), `allatonce` - waits till command is finished to display
                output, `file` - writes output to file, `none` - output is ignored

Outputs::

        None
