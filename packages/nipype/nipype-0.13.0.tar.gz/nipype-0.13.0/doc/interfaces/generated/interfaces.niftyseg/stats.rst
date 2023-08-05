.. AUTO-GENERATED FILE -- DO NOT EDIT!

interfaces.niftyseg.stats
=========================


.. _nipype.interfaces.niftyseg.stats.BinaryStats:


.. index:: BinaryStats

BinaryStats
-----------

`Link to code <http://github.com/nipy/nipype/tree/ec86b7476/nipype/interfaces/niftyseg/stats.py#L202>`__

Wraps command **seg_stats**

Interface for executable seg_stats from NiftySeg platform.

Interface to use any binary statistical operations that can be performed

with the seg_stats command-line program.

See below for those operations::

p - <float> - The <float>th percentile of all voxels intensity (float=[0,100])

sa - <ax> - Average of all voxels

ss - <ax> - Standard deviation of all voxels

svp - <ax> - Volume of all probabilsitic voxels (sum(<in>) * <volume per voxel>)

al - <in2> - Average value in <in> for each label in <in2>

d - <in2> - Calculate the Dice score between all classes in <in>and <in2>

ncc - <in2> - Normalized cross correlation between <in> and <in2>

nmi - <in2> - Normalized Mutual Information between <in> and <in2>

Vl - <csv> - Volume of each integer label <in>. Save to <csv>file.

Nl - <csv> - Count of each label <in>. Save to <csv> file.

`Source code <http://cmictig.cs.ucl.ac.uk/wiki/index.php/NiftySeg>`_ |
`Documentation <http://cmictig.cs.ucl.ac.uk/wiki/index.php/NiftySeg_documentation>`_

Examples
~~~~~~~~
>>> import copy
>>> from nipype.interfaces import niftyseg
>>> binary = niftyseg.BinaryStats()
>>> binary.inputs.in_file = 'im1.nii'
>>> # Test sa operation
>>> binary_sa = copy.deepcopy(binary)
>>> binary_sa.inputs.operation = 'sa'
>>> binary_sa.inputs.operand_value = 2.0
>>> binary_sa.cmdline  # doctest: +ALLOW_UNICODE
'seg_stats im1.nii -sa 2.00000000'
>>> binary_sa.run()  # doctest: +SKIP
>>> # Test ncc operation
>>> binary_ncc = copy.deepcopy(binary)
>>> binary_ncc.inputs.operation = 'ncc'
>>> binary_ncc.inputs.operand_file = 'im2.nii'
>>> binary_ncc.cmdline  # doctest: +ALLOW_UNICODE
'seg_stats im1.nii -ncc im2.nii'
>>> binary_ncc.run()  # doctest: +SKIP
>>> # Test Nl operation
>>> binary_nl = copy.deepcopy(binary)
>>> binary_nl.inputs.operation = 'Nl'
>>> binary_nl.inputs.operand_file = 'output.csv'
>>> binary_nl.cmdline  # doctest: +ALLOW_UNICODE
'seg_stats im1.nii -Nl output.csv'
>>> binary_nl.run()  # doctest: +SKIP

Inputs::

        [Mandatory]
        in_file: (an existing file name)
                image to operate on
                flag: %s, position: 2
        operand_file: (an existing file name)
                second image to perform operation with
                flag: %s, position: 5
                mutually_exclusive: operand_value
        operand_value: (a float)
                value to perform operation with
                flag: %.8f, position: 5
                mutually_exclusive: operand_file
        operation: ('p' or 'sa' or 'ss' or 'svp' or 'al' or 'd' or 'ncc' or
                 'nmi' or 'Vl' or 'Nl')
                operation to perform
                flag: -%s, position: 4

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
        larger_voxel: (a float)
                Only estimate statistics if voxel is larger than <float>
                flag: -t %f, position: -3
        mask_file: (an existing file name)
                statistics within the masked area
                flag: -m %s, position: -2
        terminal_output: ('stream' or 'allatonce' or 'file' or 'none')
                Control terminal output: `stream` - displays to terminal immediately
                (default), `allatonce` - waits till command is finished to display
                output, `file` - writes output to file, `none` - output is ignored

Outputs::

        output: (an array)
                Output array from seg_stats

.. _nipype.interfaces.niftyseg.stats.StatsCommand:


.. index:: StatsCommand

StatsCommand
------------

`Link to code <http://github.com/nipy/nipype/tree/ec86b7476/nipype/interfaces/niftyseg/stats.py#L48>`__

Wraps command **seg_stats**

Base Command Interface for seg_stats interfaces.

The executable seg_stats enables the estimation of image statistics on
continuous voxel intensities (average, standard deviation, min/max, robust
range, percentiles, sum, probabilistic volume, entropy, etc) either over
the full image or on a per slice basis (slice axis can be specified),
statistics over voxel coordinates (location of max, min and centre of
mass, bounding box, etc) and statistics over categorical images (e.g. per
region volume, count, average, Dice scores, etc). These statistics are
robust to the presence of NaNs, and can be constrained by a mask and/or
thresholded at a certain level.

Inputs::

        [Mandatory]
        in_file: (an existing file name)
                image to operate on
                flag: %s, position: 2

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
        larger_voxel: (a float)
                Only estimate statistics if voxel is larger than <float>
                flag: -t %f, position: -3
        mask_file: (an existing file name)
                statistics within the masked area
                flag: -m %s, position: -2
        terminal_output: ('stream' or 'allatonce' or 'file' or 'none')
                Control terminal output: `stream` - displays to terminal immediately
                (default), `allatonce` - waits till command is finished to display
                output, `file` - writes output to file, `none` - output is ignored

Outputs::

        output: (an array)
                Output array from seg_stats

.. _nipype.interfaces.niftyseg.stats.UnaryStats:


.. index:: UnaryStats

UnaryStats
----------

`Link to code <http://github.com/nipy/nipype/tree/ec86b7476/nipype/interfaces/niftyseg/stats.py#L100>`__

Wraps command **seg_stats**

Interface for executable seg_stats from NiftySeg platform.

Interface to use any unary statistical operations that can be performed

with the seg_stats command-line program.

See below for those operations::

r - The range <min max> of all voxels.

R - The robust range (assuming 2% outliers on both sides) of all voxels

a - Average of all voxels

s - Standard deviation of all voxels

v - Volume of all voxels above 0 (<# voxels> * <volume per voxel>)

vl - Volume of each integer label (<# voxels per label> * <volume per voxel>)

vp - Volume of all probabilsitic voxels (sum(<in>) * <volume per voxel>)

n - Count of all voxels above 0 (<# voxels>)

np - Sum of all fuzzy voxels (sum(<in>))

e - Entropy of all voxels

ne - Normalized entropy of all voxels

x - Location (i j k x y z) of the smallest value in the image

X - Location (i j k x y z) of the largest value in the image

c - Location (i j k x y z) of the centre of mass of the object

B - Bounding box of all nonzero voxels [ xmin xsize ymin ysize zmin zsize ]

xvox - Output the number of voxels in the x direction. Replace x with y/z for other directions.

xdim - Output the voxel dimention in the x direction. Replace x with y/z for other directions.

`Source code <http://cmictig.cs.ucl.ac.uk/wiki/index.php/NiftySeg>`_ |
`Documentation <http://cmictig.cs.ucl.ac.uk/wiki/index.php/NiftySeg_documentation>`_

Examples
~~~~~~~~
>>> import copy
>>> from nipype.interfaces import niftyseg
>>> unary = niftyseg.UnaryStats()
>>> unary.inputs.in_file = 'im1.nii'
>>> # Test v operation
>>> unary_v = copy.deepcopy(unary)
>>> unary_v.inputs.operation = 'v'
>>> unary_v.cmdline  # doctest: +ALLOW_UNICODE
'seg_stats im1.nii -v'
>>> unary_v.run()  # doctest: +SKIP
>>> # Test vl operation
>>> unary_vl = copy.deepcopy(unary)
>>> unary_vl.inputs.operation = 'vl'
>>> unary_vl.cmdline  # doctest: +ALLOW_UNICODE
'seg_stats im1.nii -vl'
>>> unary_vl.run()  # doctest: +SKIP
>>> # Test x operation
>>> unary_x = copy.deepcopy(unary)
>>> unary_x.inputs.operation = 'x'
>>> unary_x.cmdline  # doctest: +ALLOW_UNICODE
'seg_stats im1.nii -x'
>>> unary_x.run()  # doctest: +SKIP

Inputs::

        [Mandatory]
        in_file: (an existing file name)
                image to operate on
                flag: %s, position: 2
        operation: ('r' or 'R' or 'a' or 's' or 'v' or 'vl' or 'vp' or 'n' or
                 'np' or 'e' or 'ne' or 'x' or 'X' or 'c' or 'B' or 'xvox' or
                 'xdim')
                operation to perform
                flag: -%s, position: 4

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
        larger_voxel: (a float)
                Only estimate statistics if voxel is larger than <float>
                flag: -t %f, position: -3
        mask_file: (an existing file name)
                statistics within the masked area
                flag: -m %s, position: -2
        terminal_output: ('stream' or 'allatonce' or 'file' or 'none')
                Control terminal output: `stream` - displays to terminal immediately
                (default), `allatonce` - waits till command is finished to display
                output, `file` - writes output to file, `none` - output is ignored

Outputs::

        output: (an array)
                Output array from seg_stats
