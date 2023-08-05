.. AUTO-GENERATED FILE -- DO NOT EDIT!

interfaces.camino.utils
=======================


.. _nipype.interfaces.camino.utils.ImageStats:


.. index:: ImageStats

ImageStats
----------

`Link to code <http://github.com/nipy/nipype/tree/ec86b7476/nipype/interfaces/camino/utils.py#L40>`__

Wraps command **imagestats**

This program computes voxelwise statistics on a series of 3D images. The images
must be in the same space; the operation is performed voxelwise and one output
is produced per voxel.

Examples
~~~~~~~~

>>> import nipype.interfaces.camino as cam
>>> imstats = cam.ImageStats()
>>> imstats.inputs.in_files = ['im1.nii','im2.nii','im3.nii']
>>> imstats.inputs.stat = 'max'
>>> imstats.run()                  # doctest: +SKIP

Inputs::

        [Mandatory]
        in_files: (a list of items which are an existing file name)
                List of images to process. They must be in the same space and have
                the same dimensions.
                flag: -images %s, position: -1
        output_root: (a file name)
                Filename root prepended onto the names of the output files. The
                extension will be determined from the input.
                flag: -outputroot %s
        stat: ('min' or 'max' or 'mean' or 'median' or 'sum' or 'std' or
                 'var')
                The statistic to compute.
                flag: -stat %s

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
        out_type: ('float' or 'char' or 'short' or 'int' or 'long' or
                 'double', nipype default value: float)
                A Camino data type string, default is "float". Type must be signed.
                flag: -outputdatatype %s
        terminal_output: ('stream' or 'allatonce' or 'file' or 'none')
                Control terminal output: `stream` - displays to terminal immediately
                (default), `allatonce` - waits till command is finished to display
                output, `file` - writes output to file, `none` - output is ignored

Outputs::

        out_file: (an existing file name)
                Path of the file computed with the statistic chosen
