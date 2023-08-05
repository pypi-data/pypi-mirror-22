.. AUTO-GENERATED FILE -- DO NOT EDIT!

interfaces.niftyseg.patchmatch
==============================


.. _nipype.interfaces.niftyseg.patchmatch.PatchMatch:


.. index:: PatchMatch

PatchMatch
----------

`Link to code <http://github.com/nipy/nipype/tree/ec86b7476/nipype/interfaces/niftyseg/patchmatch.py#L80>`__

Wraps command **seg_PatchMatch**

Interface for executable seg_PatchMatch from NiftySeg platform.

The database file is a text file and in each line we have a template
file, a mask with the search region to consider and a file with the
label to propagate.

Input image, input mask, template images from database and masks from
database must have the same 4D resolution (same number of XxYxZ voxels,
modalities and/or time-points).
Label files from database must have the same 3D resolution
(XxYxZ voxels) than input image but can have different number of
volumes than the input image allowing to propagate multiple labels
in the same execution.

`Source code <http://cmictig.cs.ucl.ac.uk/wiki/index.php/NiftySeg>`_ |
`Documentation <http://cmictig.cs.ucl.ac.uk/wiki/index.php/NiftySeg_documentation>`_

Examples
~~~~~~~~
>>> from nipype.interfaces import niftyseg
>>> node = niftyseg.PatchMatch()
>>> node.inputs.in_file = 'im1.nii'
>>> node.inputs.mask_file = 'im2.nii'
>>> node.inputs.database_file = 'db.xml'
>>> node.cmdline  # doctest: +ALLOW_UNICODE
'seg_PatchMatch -i im1.nii -m im2.nii -db db.xml -o im1_pm.nii.gz'

Inputs::

        [Mandatory]
        database_file: (an existing file name)
                Database with the segmentations
                flag: -db %s, position: 3
        in_file: (an existing file name)
                Input image to segment
                flag: -i %s, position: 1
        mask_file: (an existing file name)
                Input mask for the area where applies PatchMatch
                flag: -m %s, position: 2

        [Optional]
        args: (a unicode string)
                Additional parameters to the command
                flag: %s
        cs_size: (an integer (int or long))
                Constrained search area size, number of times bigger than the
                patchsize
                flag: -cs %i
        environ: (a dictionary with keys which are a bytes or None or a value
                 of class 'str' and with values which are a bytes or None or a value
                 of class 'str', nipype default value: {})
                Environment variables
        ignore_exception: (a boolean, nipype default value: False)
                Print an error message instead of throwing an exception in case the
                interface fails to run
        it_num: (an integer (int or long))
                Number of iterations for the patchmatch algorithm
                flag: -it %i
        match_num: (an integer (int or long))
                Number of better matching
                flag: -match %i
        out_file: (a file name)
                The output filename of the patchmatch results
                flag: -o %s, position: 4
        patch_size: (an integer (int or long))
                Patch size, #voxels
                flag: -size %i
        pm_num: (an integer (int or long))
                Number of patchmatch executions
                flag: -pm %i
        terminal_output: ('stream' or 'allatonce' or 'file' or 'none')
                Control terminal output: `stream` - displays to terminal immediately
                (default), `allatonce` - waits till command is finished to display
                output, `file` - writes output to file, `none` - output is ignored

Outputs::

        out_file: (a file name)
                Output segmentation
