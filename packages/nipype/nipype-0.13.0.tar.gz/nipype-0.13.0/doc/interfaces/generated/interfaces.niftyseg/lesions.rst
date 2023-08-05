.. AUTO-GENERATED FILE -- DO NOT EDIT!

interfaces.niftyseg.lesions
===========================


.. _nipype.interfaces.niftyseg.lesions.FillLesions:


.. index:: FillLesions

FillLesions
-----------

`Link to code <http://github.com/nipy/nipype/tree/ec86b7476/nipype/interfaces/niftyseg/lesions.py#L98>`__

Wraps command **seg_FillLesions**

Interface for executable seg_FillLesions from NiftySeg platform.

Fill all the masked lesions with WM intensity average.

`Source code <http://cmictig.cs.ucl.ac.uk/wiki/index.php/NiftySeg>`_ |
`Documentation <http://cmictig.cs.ucl.ac.uk/wiki/index.php/NiftySeg_documentation>`_

Examples
~~~~~~~~
>>> from nipype.interfaces import niftyseg
>>> node = niftyseg.FillLesions()
>>> node.inputs.in_file = 'im1.nii'
>>> node.inputs.lesion_mask = 'im2.nii'
>>> node.cmdline  # doctest: +ALLOW_UNICODE
'seg_FillLesions -i im1.nii -l im2.nii -o im1_lesions_filled.nii.gz'

Inputs::

        [Mandatory]
        in_file: (an existing file name)
                Input image to fill lesions
                flag: -i %s, position: 1
        lesion_mask: (an existing file name)
                Lesion mask
                flag: -l %s, position: 2

        [Optional]
        args: (a unicode string)
                Additional parameters to the command
                flag: %s
        bin_mask: (a file name)
                Give a binary mask with the valid search areas.
                flag: -mask %s
        cwf: (a float)
                Patch cardinality weighting factor (by default 2).
                flag: -cwf %f
        debug: (a boolean)
                Save all intermidium files (by default OFF).
                flag: -debug
        environ: (a dictionary with keys which are a bytes or None or a value
                 of class 'str' and with values which are a bytes or None or a value
                 of class 'str', nipype default value: {})
                Environment variables
        ignore_exception: (a boolean, nipype default value: False)
                Print an error message instead of throwing an exception in case the
                interface fails to run
        in_dilation: (an integer (int or long))
                Dilate the mask <int> times (in voxels, by default 0)
                flag: -dil %d
        match: (a float)
                Percentage of minimum number of voxels between patches <float> (by
                default 0.5).
                flag: -match %f
        other: (a boolean)
                Guizard et al. (FIN 2015) method, it doesn't include the
                multiresolution/hierarchical inpainting part, this part needs to be
                done with some external software such as reg_tools and reg_resample
                from NiftyReg. By default it uses the method presented in Prados et
                al. (Neuroimage 2016).
                flag: -other
        out_datatype: (a string)
                Set output <datatype> (char, short, int, uchar, ushort, uint, float,
                double).
                flag: -odt %s
        out_file: (a file name)
                The output filename of the fill lesions results
                flag: -o %s, position: 3
        search: (a float)
                Minimum percentage of valid voxels in target patch <float> (by
                default 0).
                flag: -search %f
        size: (an integer (int or long))
                Search regions size respect biggest patch size (by default 4).
                flag: -size %d
        smooth: (a float)
                Smoothing by <float> (in minimal 6-neighbourhood voxels (by default
                0.1)).
                flag: -smo %f
        terminal_output: ('stream' or 'allatonce' or 'file' or 'none')
                Control terminal output: `stream` - displays to terminal immediately
                (default), `allatonce` - waits till command is finished to display
                output, `file` - writes output to file, `none` - output is ignored
        use_2d: (a boolean)
                Uses 2D patches in the Z axis, by default 3D.
                flag: -2D
        verbose: (a boolean)
                Verbose (by default OFF).
                flag: -v

Outputs::

        out_file: (a file name)
                Output segmentation
