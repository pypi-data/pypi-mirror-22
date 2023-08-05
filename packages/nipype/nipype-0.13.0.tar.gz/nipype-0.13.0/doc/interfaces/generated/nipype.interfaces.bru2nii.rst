.. AUTO-GENERATED FILE -- DO NOT EDIT!

interfaces.bru2nii
==================


.. _nipype.interfaces.bru2nii.Bru2:


.. index:: Bru2

Bru2
----

`Link to code <http://github.com/nipy/nipype/tree/ec86b7476/nipype/interfaces/bru2nii.py#L35>`__

Wraps command **Bru2**

Uses bru2nii's Bru2 to convert Bruker files

Examples
~~~~~~~~

>>> from nipype.interfaces.bru2nii import Bru2
>>> converter = Bru2()
>>> converter.inputs.input_dir = "brukerdir"
>>> converter.cmdline  # doctest: +ELLIPSIS +ALLOW_UNICODE
'Bru2 -o .../nipype/testing/data/brukerdir brukerdir'

Inputs::

        [Mandatory]
        input_dir: (an existing directory name)
                Input Directory
                flag: %s, position: -1

        [Optional]
        actual_size: (a boolean)
                Keep actual size - otherwise x10 scale so animals match human.
                flag: -a
        append_protocol_name: (a boolean)
                Append protocol name to output filename.
                flag: -p
        args: (a unicode string)
                Additional parameters to the command
                flag: %s
        environ: (a dictionary with keys which are a bytes or None or a value
                 of class 'str' and with values which are a bytes or None or a value
                 of class 'str', nipype default value: {})
                Environment variables
        force_conversion: (a boolean)
                Force conversion of localizers images (multiple slice orientations).
                flag: -f
        ignore_exception: (a boolean, nipype default value: False)
                Print an error message instead of throwing an exception in case the
                interface fails to run
        output_filename: (a unicode string)
                Output filename ('.nii' will be appended)
                flag: -o %s
        terminal_output: ('stream' or 'allatonce' or 'file' or 'none')
                Control terminal output: `stream` - displays to terminal immediately
                (default), `allatonce` - waits till command is finished to display
                output, `file` - writes output to file, `none` - output is ignored

Outputs::

        nii_file: (an existing file name)
