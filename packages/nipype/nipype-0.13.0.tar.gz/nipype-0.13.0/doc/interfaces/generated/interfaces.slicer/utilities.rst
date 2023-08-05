.. AUTO-GENERATED FILE -- DO NOT EDIT!

interfaces.slicer.utilities
===========================


.. _nipype.interfaces.slicer.utilities.EMSegmentTransformToNewFormat:


.. index:: EMSegmentTransformToNewFormat

EMSegmentTransformToNewFormat
-----------------------------

`Link to code <http://github.com/nipy/nipype/tree/ec86b7476/nipype/interfaces/slicer/utilities.py#L20>`__

Wraps command **EMSegmentTransformToNewFormat **

title:
  Transform MRML Files to New EMSegmenter Standard


category:
  Utilities


description:
  Transform MRML Files to New EMSegmenter Standard

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
        inputMRMLFileName: (an existing file name)
                Active MRML scene that contains EMSegment algorithm parameters in
                the format before 3.6.3 - please include absolute file name in path.
                flag: --inputMRMLFileName %s
        outputMRMLFileName: (a boolean or a file name)
                Write out the MRML scene after transformation to format 3.6.3 has
                been made. - has to be in the same directory as the input MRML file
                due to Slicer Core bug - please include absolute file name in path
                flag: --outputMRMLFileName %s
        templateFlag: (a boolean)
                Set to true if the transformed mrml file should be used as template
                file
                flag: --templateFlag
        terminal_output: ('stream' or 'allatonce' or 'file' or 'none')
                Control terminal output: `stream` - displays to terminal immediately
                (default), `allatonce` - waits till command is finished to display
                output, `file` - writes output to file, `none` - output is ignored

Outputs::

        outputMRMLFileName: (an existing file name)
                Write out the MRML scene after transformation to format 3.6.3 has
                been made. - has to be in the same directory as the input MRML file
                due to Slicer Core bug - please include absolute file name in path
