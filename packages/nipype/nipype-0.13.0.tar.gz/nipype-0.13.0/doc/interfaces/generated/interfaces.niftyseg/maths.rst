.. AUTO-GENERATED FILE -- DO NOT EDIT!

interfaces.niftyseg.maths
=========================


.. _nipype.interfaces.niftyseg.maths.BinaryMaths:


.. index:: BinaryMaths

BinaryMaths
-----------

`Link to code <http://github.com/nipy/nipype/tree/ec86b7476/nipype/interfaces/niftyseg/maths.py#L237>`__

Wraps command **seg_maths**

Interface for executable seg_maths from NiftySeg platform.

Interface to use any binary mathematical operations that can be performed

with the seg_maths command-line program.

See below for those operations::

mul - <float/file> - Multiply image <float> value or by other image.

div - <float/file> - Divide image by <float> or by other image.

add - <float/file> - Add image by <float> or by other image.

sub - <float/file> - Subtract image by <float> or by other image.

pow - <float> - Image to the power of <float>.

thr - <float> - Threshold the image below <float>.

uthr - <float> - Threshold image above <float>.

smo - <float> - Gaussian smoothing by std <float> (in voxels and up to 4-D).

edge - <float> - Calculate the edges of the image using a threshold <float>.

sobel3 - <float> - Calculate the edges of all timepoints using a Sobel filter with a 3x3x3 kernel and applying <float> gaussian smoothing.

sobel5 - <float> - Calculate the edges of all timepoints using a Sobel filter with a 5x5x5 kernel and applying <float> gaussian smoothing.

min - <file> - Get the min per voxel between <current> and <file>.

smol - <float> - Gaussian smoothing of a 3D label image.

geo - <float/file> - Geodesic distance according to the speed function <float/file>

llsnorm  <file_norm> - Linear LS normalisation between current and <file_norm>

masknan <file_norm> - Assign everything outside the mask (mask==0) with NaNs

hdr_copy <file> - Copy header from working image to <file> and save in <output>.

splitinter <x/y/z> - Split interleaved slices in direction <x/y/z> into separate time points

`Source code <http://cmictig.cs.ucl.ac.uk/wiki/index.php/NiftySeg>`_ |
`Documentation <http://cmictig.cs.ucl.ac.uk/wiki/index.php/NiftySeg_documentation>`_

Examples
~~~~~~~~
>>> import copy
>>> from nipype.interfaces import niftyseg
>>> binary = niftyseg.BinaryMaths()
>>> binary.inputs.in_file = 'im1.nii'
>>> binary.inputs.output_datatype = 'float'
>>> # Test sub operation
>>> binary_sub = copy.deepcopy(binary)
>>> binary_sub.inputs.operation = 'sub'
>>> binary_sub.inputs.operand_file = 'im2.nii'
>>> binary_sub.cmdline  # doctest: +ALLOW_UNICODE
'seg_maths im1.nii -sub im2.nii -odt float im1_sub.nii'
>>> binary_sub.run()  # doctest: +SKIP
>>> # Test mul operation
>>> binary_mul = copy.deepcopy(binary)
>>> binary_mul.inputs.operation = 'mul'
>>> binary_mul.inputs.operand_value = 2.0
>>> binary_mul.cmdline  # doctest: +ALLOW_UNICODE
'seg_maths im1.nii -mul 2.00000000 -odt float im1_mul.nii'
>>> binary_mul.run()  # doctest: +SKIP
>>> # Test llsnorm operation
>>> binary_llsnorm = copy.deepcopy(binary)
>>> binary_llsnorm.inputs.operation = 'llsnorm'
>>> binary_llsnorm.inputs.operand_file = 'im2.nii'
>>> binary_llsnorm.cmdline  # doctest: +ALLOW_UNICODE
'seg_maths im1.nii -llsnorm im2.nii -odt float im1_llsnorm.nii'
>>> binary_llsnorm.run()  # doctest: +SKIP
>>> # Test splitinter operation
>>> binary_splitinter = copy.deepcopy(binary)
>>> binary_splitinter.inputs.operation = 'splitinter'
>>> binary_splitinter.inputs.operand_str = 'z'
>>> binary_splitinter.cmdline  # doctest: +ALLOW_UNICODE
'seg_maths im1.nii -splitinter z -odt float im1_splitinter.nii'
>>> binary_splitinter.run()  # doctest: +SKIP

Inputs::

        [Mandatory]
        in_file: (an existing file name)
                image to operate on
                flag: %s, position: 2
        operand_file: (an existing file name)
                second image to perform operation with
                flag: %s, position: 5
                mutually_exclusive: operand_value, operand_str
        operand_str: ('x' or 'y' or 'z')
                string value to perform operation splitinter
                flag: %s, position: 5
                mutually_exclusive: operand_value, operand_file
        operand_value: (a float)
                float value to perform operation with
                flag: %.8f, position: 5
                mutually_exclusive: operand_file, operand_str
        operation: ('mul' or 'div' or 'add' or 'sub' or 'pow' or 'thr' or
                 'uthr' or 'smo' or 'edge' or 'sobel3' or 'sobel5' or 'min' or
                 'smol' or 'geo' or 'llsnorm' or 'masknan' or 'hdr_copy' or
                 'splitinter')
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
        out_file: (a file name)
                image to write
                flag: %s, position: -2
        output_datatype: ('float' or 'char' or 'int' or 'short' or 'double'
                 or 'input')
                datatype to use for output (default uses input type)
                flag: -odt %s, position: -3
        terminal_output: ('stream' or 'allatonce' or 'file' or 'none')
                Control terminal output: `stream` - displays to terminal immediately
                (default), `allatonce` - waits till command is finished to display
                output, `file` - writes output to file, `none` - output is ignored

Outputs::

        out_file: (a file name)
                image written after calculations

.. _nipype.interfaces.niftyseg.maths.BinaryMathsInteger:


.. index:: BinaryMathsInteger

BinaryMathsInteger
------------------

`Link to code <http://github.com/nipy/nipype/tree/ec86b7476/nipype/interfaces/niftyseg/maths.py#L386>`__

Wraps command **seg_maths**

Interface for executable seg_maths from NiftySeg platform.

Interface to use any integer mathematical operations that can be performed

with the seg_maths command-line program.

See below for those operations:: (requiring integer values)

equal - <int> - Get voxels equal to <int>

dil - <int>  - Dilate the image <int> times (in voxels).

ero - <int> - Erode the image <int> times (in voxels).

tp - <int> - Extract time point <int>

crop - <int> - Crop <int> voxels around each 3D volume.

pad - <int> -  Pad <int> voxels with NaN value around each 3D volume.

`Source code <http://cmictig.cs.ucl.ac.uk/wiki/index.php/NiftySeg>`_ |
`Documentation <http://cmictig.cs.ucl.ac.uk/wiki/index.php/NiftySeg_documentation>`_

Examples
~~~~~~~~
>>> import copy
>>> from nipype.interfaces.niftyseg import BinaryMathsInteger
>>> binaryi = BinaryMathsInteger()
>>> binaryi.inputs.in_file = 'im1.nii'
>>> binaryi.inputs.output_datatype = 'float'
>>> # Test dil operation
>>> binaryi_dil = copy.deepcopy(binaryi)
>>> binaryi_dil.inputs.operation = 'dil'
>>> binaryi_dil.inputs.operand_value = 2
>>> binaryi_dil.cmdline  # doctest: +ALLOW_UNICODE
'seg_maths im1.nii -dil 2 -odt float im1_dil.nii'
>>> binaryi_dil.run()  # doctest: +SKIP
>>> # Test dil operation
>>> binaryi_ero = copy.deepcopy(binaryi)
>>> binaryi_ero.inputs.operation = 'ero'
>>> binaryi_ero.inputs.operand_value = 1
>>> binaryi_ero.cmdline  # doctest: +ALLOW_UNICODE
'seg_maths im1.nii -ero 1 -odt float im1_ero.nii'
>>> binaryi_ero.run()  # doctest: +SKIP
>>> # Test pad operation
>>> binaryi_pad = copy.deepcopy(binaryi)
>>> binaryi_pad.inputs.operation = 'pad'
>>> binaryi_pad.inputs.operand_value = 4
>>> binaryi_pad.cmdline  # doctest: +ALLOW_UNICODE
'seg_maths im1.nii -pad 4 -odt float im1_pad.nii'
>>> binaryi_pad.run()  # doctest: +SKIP

Inputs::

        [Mandatory]
        in_file: (an existing file name)
                image to operate on
                flag: %s, position: 2
        operand_value: (an integer (int or long))
                int value to perform operation with
                flag: %d, position: 5
        operation: ('dil' or 'ero' or 'tp' or 'equal' or 'pad' or 'crop')
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
        out_file: (a file name)
                image to write
                flag: %s, position: -2
        output_datatype: ('float' or 'char' or 'int' or 'short' or 'double'
                 or 'input')
                datatype to use for output (default uses input type)
                flag: -odt %s, position: -3
        terminal_output: ('stream' or 'allatonce' or 'file' or 'none')
                Control terminal output: `stream` - displays to terminal immediately
                (default), `allatonce` - waits till command is finished to display
                output, `file` - writes output to file, `none` - output is ignored

Outputs::

        out_file: (a file name)
                image written after calculations

.. _nipype.interfaces.niftyseg.maths.MathsCommand:


.. index:: MathsCommand

MathsCommand
------------

`Link to code <http://github.com/nipy/nipype/tree/ec86b7476/nipype/interfaces/niftyseg/maths.py#L58>`__

Wraps command **seg_maths**

Base Command Interface for seg_maths interfaces.

The executable seg_maths enables the sequential execution of arithmetic
operations, like multiplication (-mul), division (-div) or addition
(-add), binarisation (-bin) or thresholding (-thr) operations and
convolution by a Gaussian kernel (-smo). It also alows mathematical
morphology based operations like dilation (-dil), erosion (-ero),
connected components (-lconcomp) and hole filling (-fill), Euclidean
(- euc) and geodesic (-geo) distance transforms, local image similarity
metric calculation (-lncc and -lssd). Finally, it allows multiple
operations over the dimensionality of the image, from merging 3D images
together as a 4D image (-merge) or splitting (-split or -tp) 4D images
into several 3D images, to estimating the maximum, minimum and average
over all time-points, etc.

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
        out_file: (a file name)
                image to write
                flag: %s, position: -2
        output_datatype: ('float' or 'char' or 'int' or 'short' or 'double'
                 or 'input')
                datatype to use for output (default uses input type)
                flag: -odt %s, position: -3
        terminal_output: ('stream' or 'allatonce' or 'file' or 'none')
                Control terminal output: `stream` - displays to terminal immediately
                (default), `allatonce` - waits till command is finished to display
                output, `file` - writes output to file, `none` - output is ignored

Outputs::

        out_file: (a file name)
                image written after calculations

.. _nipype.interfaces.niftyseg.maths.Merge:


.. index:: Merge

Merge
-----

`Link to code <http://github.com/nipy/nipype/tree/ec86b7476/nipype/interfaces/niftyseg/maths.py#L553>`__

Wraps command **seg_maths**

Interface for executable seg_maths from NiftySeg platform.

Interface to use the merge operation that can be performed

with the seg_maths command-line program.

See below for this option::

merge  <i> <d> <files>  Merge <i> images and the working image in the <d> dimension

`Source code <http://cmictig.cs.ucl.ac.uk/wiki/index.php/NiftySeg>`_ |
`Documentation <http://cmictig.cs.ucl.ac.uk/wiki/index.php/NiftySeg_documentation>`_

Examples
~~~~~~~~
>>> from nipype.interfaces import niftyseg
>>> node = niftyseg.Merge()
>>> node.inputs.in_file = 'im1.nii'
>>> files = ['im2.nii', 'im3.nii']
>>> node.inputs.merge_files = files
>>> node.inputs.dimension = 2
>>> node.inputs.output_datatype = 'float'
>>> node.cmdline  # doctest: +ALLOW_UNICODE
'seg_maths im1.nii -merge 2 2 im2.nii im3.nii -odt float im1_merged.nii'

Inputs::

        [Mandatory]
        dimension: (an integer (int or long))
                Dimension to merge the images.
        in_file: (an existing file name)
                image to operate on
                flag: %s, position: 2
        merge_files: (a list of items which are an existing file name)
                List of images to merge to the working image <input>.
                flag: %s, position: 4

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
        out_file: (a file name)
                image to write
                flag: %s, position: -2
        output_datatype: ('float' or 'char' or 'int' or 'short' or 'double'
                 or 'input')
                datatype to use for output (default uses input type)
                flag: -odt %s, position: -3
        terminal_output: ('stream' or 'allatonce' or 'file' or 'none')
                Control terminal output: `stream` - displays to terminal immediately
                (default), `allatonce` - waits till command is finished to display
                output, `file` - writes output to file, `none` - output is ignored

Outputs::

        out_file: (a file name)
                image written after calculations

.. _nipype.interfaces.niftyseg.maths.TupleMaths:


.. index:: TupleMaths

TupleMaths
----------

`Link to code <http://github.com/nipy/nipype/tree/ec86b7476/nipype/interfaces/niftyseg/maths.py#L480>`__

Wraps command **seg_maths**

Interface for executable seg_maths from NiftySeg platform.

Interface to use any tuple mathematical operations that can be performed

with the seg_maths command-line program.

See below for those operations::

lncc <file> <std> Local CC between current img and <file> on a kernel with <std>

lssd <file> <std> Local SSD between current img and <file> on a kernel with <std>

lltsnorm <file_norm> <float>  Linear LTS normalisation assuming <float> percent outliers

`Source code <http://cmictig.cs.ucl.ac.uk/wiki/index.php/NiftySeg>`_ |
`Documentation <http://cmictig.cs.ucl.ac.uk/wiki/index.php/NiftySeg_documentation>`_

Examples
~~~~~~~~
>>> import copy
>>> from nipype.interfaces import niftyseg
>>> tuple = niftyseg.TupleMaths()
>>> tuple.inputs.in_file = 'im1.nii'
>>> tuple.inputs.output_datatype = 'float'

>>> # Test lncc operation
>>> tuple_lncc = copy.deepcopy(tuple)
>>> tuple_lncc.inputs.operation = 'lncc'
>>> tuple_lncc.inputs.operand_file1 = 'im2.nii'
>>> tuple_lncc.inputs.operand_value2 = 2.0
>>> tuple_lncc.cmdline  # doctest: +ALLOW_UNICODE
'seg_maths im1.nii -lncc im2.nii 2.00000000 -odt float im1_lncc.nii'
>>> tuple_lncc.run()  # doctest: +SKIP

>>> # Test lssd operation
>>> tuple_lssd = copy.deepcopy(tuple)
>>> tuple_lssd.inputs.operation = 'lssd'
>>> tuple_lssd.inputs.operand_file1 = 'im2.nii'
>>> tuple_lssd.inputs.operand_value2 = 1.0
>>> tuple_lssd.cmdline  # doctest: +ALLOW_UNICODE
'seg_maths im1.nii -lssd im2.nii 1.00000000 -odt float im1_lssd.nii'
>>> tuple_lssd.run()  # doctest: +SKIP

>>> # Test lltsnorm operation
>>> tuple_lltsnorm = copy.deepcopy(tuple)
>>> tuple_lltsnorm.inputs.operation = 'lltsnorm'
>>> tuple_lltsnorm.inputs.operand_file1 = 'im2.nii'
>>> tuple_lltsnorm.inputs.operand_value2 = 0.01
>>> tuple_lltsnorm.cmdline  # doctest: +ALLOW_UNICODE
'seg_maths im1.nii -lltsnorm im2.nii 0.01000000 -odt float im1_lltsnorm.nii'
>>> tuple_lltsnorm.run()  # doctest: +SKIP

Inputs::

        [Mandatory]
        in_file: (an existing file name)
                image to operate on
                flag: %s, position: 2
        operand_file1: (an existing file name)
                image to perform operation 1 with
                flag: %s, position: 5
                mutually_exclusive: operand_value1
        operand_file2: (an existing file name)
                image to perform operation 2 with
                flag: %s, position: 6
                mutually_exclusive: operand_value2
        operand_value1: (a float)
                float value to perform operation 1 with
                flag: %.8f, position: 5
                mutually_exclusive: operand_file1
        operand_value2: (a float)
                float value to perform operation 2 with
                flag: %.8f, position: 6
                mutually_exclusive: operand_file2
        operation: ('lncc' or 'lssd' or 'lltsnorm')
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
        out_file: (a file name)
                image to write
                flag: %s, position: -2
        output_datatype: ('float' or 'char' or 'int' or 'short' or 'double'
                 or 'input')
                datatype to use for output (default uses input type)
                flag: -odt %s, position: -3
        terminal_output: ('stream' or 'allatonce' or 'file' or 'none')
                Control terminal output: `stream` - displays to terminal immediately
                (default), `allatonce` - waits till command is finished to display
                output, `file` - writes output to file, `none` - output is ignored

Outputs::

        out_file: (a file name)
                image written after calculations

.. _nipype.interfaces.niftyseg.maths.UnaryMaths:


.. index:: UnaryMaths

UnaryMaths
----------

`Link to code <http://github.com/nipy/nipype/tree/ec86b7476/nipype/interfaces/niftyseg/maths.py#L102>`__

Wraps command **seg_maths**

Interface for executable seg_maths from NiftySeg platform.

Interface to use any unary mathematical operations that can be performed

with the seg_maths command-line program.

See below for those operations::

sqrt - Square root of the image).

exp - Exponential root of the image.

log - Log of the image.

recip - Reciprocal (1/I) of the image.

abs - Absolute value of the image.

bin - Binarise the image.

otsu - Otsu thresholding of the current image.

lconcomp - Take the largest connected component

concomp6 - Label the different connected components with a 6NN kernel

concomp26 - Label the different connected components with a 26NN kernel

fill - Fill holes in binary object (e.g. fill ventricle in brain mask).

euc - Euclidean distance trasnform

tpmax - Get the time point with the highest value (binarise 4D probabilities)

tmean - Mean value of all time points.

tmax - Max value of all time points.

tmin - Mean value of all time points.

splitlab - Split the integer labels into multiple timepoints

removenan - Remove all NaNs and replace then with 0

isnan - Binary image equal to 1 if the value is NaN and 0 otherwise

subsamp2 - Subsample the image by 2 using NN sampling (qform and sform scaled)

scl  - Reset scale and slope info.

4to5 - Flip the 4th and 5th dimension.

range - Reset the image range to the min max.

`Source code <http://cmictig.cs.ucl.ac.uk/wiki/index.php/NiftySeg>`_ |
`Documentation <http://cmictig.cs.ucl.ac.uk/wiki/index.php/NiftySeg_documentation>`_

Examples
~~~~~~~~
>>> import copy
>>> from nipype.interfaces import niftyseg
>>> unary = niftyseg.UnaryMaths()
>>> unary.inputs.output_datatype = 'float'
>>> unary.inputs.in_file = 'im1.nii'
>>> # Test sqrt operation
>>> unary_sqrt = copy.deepcopy(unary)
>>> unary_sqrt.inputs.operation = 'sqrt'
>>> unary_sqrt.cmdline  # doctest: +ALLOW_UNICODE
'seg_maths im1.nii -sqrt -odt float im1_sqrt.nii'
>>> unary_sqrt.run()  # doctest: +SKIP
>>> # Test sqrt operation
>>> unary_abs = copy.deepcopy(unary)
>>> unary_abs.inputs.operation = 'abs'
>>> unary_abs.cmdline  # doctest: +ALLOW_UNICODE
'seg_maths im1.nii -abs -odt float im1_abs.nii'
>>> unary_abs.run()  # doctest: +SKIP
>>> # Test bin operation
>>> unary_bin = copy.deepcopy(unary)
>>> unary_bin.inputs.operation = 'bin'
>>> unary_bin.cmdline  # doctest: +ALLOW_UNICODE
'seg_maths im1.nii -bin -odt float im1_bin.nii'
>>> unary_bin.run()  # doctest: +SKIP
>>> # Test otsu operation
>>> unary_otsu = copy.deepcopy(unary)
>>> unary_otsu.inputs.operation = 'otsu'
>>> unary_otsu.cmdline  # doctest: +ALLOW_UNICODE
'seg_maths im1.nii -otsu -odt float im1_otsu.nii'
>>> unary_otsu.run()  # doctest: +SKIP
>>> # Test isnan operation
>>> unary_isnan = copy.deepcopy(unary)
>>> unary_isnan.inputs.operation = 'isnan'
>>> unary_isnan.cmdline  # doctest: +ALLOW_UNICODE
'seg_maths im1.nii -isnan -odt float im1_isnan.nii'
>>> unary_isnan.run()  # doctest: +SKIP

Inputs::

        [Mandatory]
        in_file: (an existing file name)
                image to operate on
                flag: %s, position: 2
        operation: ('sqrt' or 'exp' or 'log' or 'recip' or 'abs' or 'bin' or
                 'otsu' or 'lconcomp' or 'concomp6' or 'concomp26' or 'fill' or
                 'euc' or 'tpmax' or 'tmean' or 'tmax' or 'tmin' or 'splitlab' or
                 'removenan' or 'isnan' or 'subsamp2' or 'scl' or '4to5' or 'range')
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
        out_file: (a file name)
                image to write
                flag: %s, position: -2
        output_datatype: ('float' or 'char' or 'int' or 'short' or 'double'
                 or 'input')
                datatype to use for output (default uses input type)
                flag: -odt %s, position: -3
        terminal_output: ('stream' or 'allatonce' or 'file' or 'none')
                Control terminal output: `stream` - displays to terminal immediately
                (default), `allatonce` - waits till command is finished to display
                output, `file` - writes output to file, `none` - output is ignored

Outputs::

        out_file: (a file name)
                image written after calculations
