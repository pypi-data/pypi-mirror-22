.. AUTO-GENERATED FILE -- DO NOT EDIT!

interfaces.minc.minc
====================


.. _nipype.interfaces.minc.minc.Average:


.. index:: Average

Average
-------

`Link to code <http://github.com/nipy/nipype/tree/ec86b7476/nipype/interfaces/minc/minc.py#L833>`__

Wraps command **mincaverage**

Average a number of MINC files.

Examples
~~~~~~~~

>>> from nipype.interfaces.minc import Average
>>> from nipype.interfaces.minc.testdata import nonempty_minc_data

>>> files = [nonempty_minc_data(i) for i in range(3)]
>>> average = Average(input_files=files, output_file='/tmp/tmp.mnc')
>>> average.run() # doctest: +SKIP

Inputs::

        [Mandatory]
        filelist: (a file name)
                Specify the name of a file containing input file names.
                flag: -filelist %s
                mutually_exclusive: input_files, filelist
        input_files: (a list of items which are a file name)
                input file(s)
                flag: %s, position: -2
                mutually_exclusive: input_files, filelist

        [Optional]
        args: (a unicode string)
                Additional parameters to the command
                flag: %s
        avgdim: (a unicode string)
                Specify a dimension along which we wish to average.
                flag: -avgdim %s
        binarize: (a boolean)
                Binarize the volume by looking for values in a given range.
                flag: -binarize
        binrange: (a tuple of the form: (a float, a float))
                Specify a range for binarization. Default value: 1.79769e+308
                -1.79769e+308.
                flag: -binrange %s %s
        binvalue: (a float)
                Specify a target value (+/- 0.5) forbinarization. Default value:
                -1.79769e+308
                flag: -binvalue %s
        check_dimensions: (a boolean)
                Check that dimension info matches across files (default).
                flag: -check_dimensions
                mutually_exclusive: check_dimensions, no_check_dimensions
        clobber: (a boolean, nipype default value: True)
                Overwrite existing file.
                flag: -clobber
        copy_header: (a boolean)
                Copy all of the header from the first file (default for one file).
                flag: -copy_header
                mutually_exclusive: copy_header, no_copy_header
        debug: (a boolean)
                Print out debugging messages.
                flag: -debug
        environ: (a dictionary with keys which are a bytes or None or a value
                 of class 'str' and with values which are a bytes or None or a value
                 of class 'str', nipype default value: {})
                Environment variables
        format_byte: (a boolean)
                Write out byte data.
                flag: -byte
                mutually_exclusive: format_filetype, format_byte, format_short,
                 format_int, format_long, format_float, format_double,
                 format_signed, format_unsigned
        format_double: (a boolean)
                Write out double-precision floating-point data.
                flag: -double
                mutually_exclusive: format_filetype, format_byte, format_short,
                 format_int, format_long, format_float, format_double,
                 format_signed, format_unsigned
        format_filetype: (a boolean)
                Use data type of first file (default).
                flag: -filetype
                mutually_exclusive: format_filetype, format_byte, format_short,
                 format_int, format_long, format_float, format_double,
                 format_signed, format_unsigned
        format_float: (a boolean)
                Write out single-precision floating-point data.
                flag: -float
                mutually_exclusive: format_filetype, format_byte, format_short,
                 format_int, format_long, format_float, format_double,
                 format_signed, format_unsigned
        format_int: (a boolean)
                Write out 32-bit integer data.
                flag: -int
                mutually_exclusive: format_filetype, format_byte, format_short,
                 format_int, format_long, format_float, format_double,
                 format_signed, format_unsigned
        format_long: (a boolean)
                Superseded by -int.
                flag: -long
                mutually_exclusive: format_filetype, format_byte, format_short,
                 format_int, format_long, format_float, format_double,
                 format_signed, format_unsigned
        format_short: (a boolean)
                Write out short integer data.
                flag: -short
                mutually_exclusive: format_filetype, format_byte, format_short,
                 format_int, format_long, format_float, format_double,
                 format_signed, format_unsigned
        format_signed: (a boolean)
                Write signed integer data.
                flag: -signed
                mutually_exclusive: format_filetype, format_byte, format_short,
                 format_int, format_long, format_float, format_double,
                 format_signed, format_unsigned
        format_unsigned: (a boolean)
                Write unsigned integer data (default).
                flag: -unsigned
                mutually_exclusive: format_filetype, format_byte, format_short,
                 format_int, format_long, format_float, format_double,
                 format_signed, format_unsigned
        ignore_exception: (a boolean, nipype default value: False)
                Print an error message instead of throwing an exception in case the
                interface fails to run
        max_buffer_size_in_kb: (a long integer >= 0)
                Specify the maximum size of the internal buffers (in kbytes).
                flag: -max_buffer_size_in_kb %d
        no_check_dimensions: (a boolean)
                Do not check dimension info.
                flag: -nocheck_dimensions
                mutually_exclusive: check_dimensions, no_check_dimensions
        no_copy_header: (a boolean)
                Do not copy all of the header from the first file (default for many
                files)).
                flag: -nocopy_header
                mutually_exclusive: copy_header, no_copy_header
        nonormalize: (a boolean)
                Do not normalize data sets (default).
                flag: -nonormalize
                mutually_exclusive: normalize, nonormalize
        normalize: (a boolean)
                Normalize data sets for mean intensity.
                flag: -normalize
                mutually_exclusive: normalize, nonormalize
        output_file: (a file name)
                output file
                flag: %s, position: -1
        quiet: (a boolean)
                Do not print out log messages.
                flag: -quiet
                mutually_exclusive: verbose, quiet
        sdfile: (a file name)
                Specify an output sd file (default=none).
                flag: -sdfile %s
        terminal_output: ('stream' or 'allatonce' or 'file' or 'none')
                Control terminal output: `stream` - displays to terminal immediately
                (default), `allatonce` - waits till command is finished to display
                output, `file` - writes output to file, `none` - output is ignored
        two: (a boolean)
                Create a MINC 2 output file.
                flag: -2
        verbose: (a boolean)
                Print out log messages (default).
                flag: -verbose
                mutually_exclusive: verbose, quiet
        voxel_range: (a tuple of the form: (an integer (int or long), an
                 integer (int or long)))
                Valid range for output data.
                flag: -range %d %d
        weights: (a list of items which are a unicode string)
                Specify weights for averaging ("<w1>,<w2>,...").
                flag: -weights %s
        width_weighted: (a boolean)
                Weight by dimension widths when -avgdim is used.
                flag: -width_weighted
                requires: avgdim

Outputs::

        output_file: (an existing file name)
                output file

.. _nipype.interfaces.minc.minc.BBox:


.. index:: BBox

BBox
----

`Link to code <http://github.com/nipy/nipype/tree/ec86b7476/nipype/interfaces/minc/minc.py#L1184>`__

Wraps command **mincbbox**

Determine a bounding box of image.

Examples
~~~~~~~~

>>> from nipype.interfaces.minc import BBox
>>> from nipype.interfaces.minc.testdata import nonempty_minc_data

>>> file0 = nonempty_minc_data(0)
>>> bbox = BBox(input_file=file0)
>>> bbox.run() # doctest: +SKIP

Inputs::

        [Mandatory]
        input_file: (an existing file name)
                input file
                flag: %s, position: -2

        [Optional]
        args: (a unicode string)
                Additional parameters to the command
                flag: %s
        environ: (a dictionary with keys which are a bytes or None or a value
                 of class 'str' and with values which are a bytes or None or a value
                 of class 'str', nipype default value: {})
                Environment variables
        format_minccrop: (a boolean)
                Output format for minccrop: (-xlim x1 x2 -ylim y1 y2 -zlim z1 z2
                flag: -minccrop
        format_mincresample: (a boolean)
                Output format for mincresample: (-step x y z -start x y z -nelements
                x y z
                flag: -mincresample
        format_mincreshape: (a boolean)
                Output format for mincreshape: (-start x,y,z -count dx,dy,dz
                flag: -mincreshape
        ignore_exception: (a boolean, nipype default value: False)
                Print an error message instead of throwing an exception in case the
                interface fails to run
        one_line: (a boolean)
                Output on one line (default): start_x y z width_x y z
                flag: -one_line
                mutually_exclusive: one_line, two_lines
        out_file: (a file name)
                flag: > %s, position: -1
        output_file: (a file name)
                output file containing bounding box corners
        terminal_output: ('stream' or 'allatonce' or 'file' or 'none')
                Control terminal output: `stream` - displays to terminal immediately
                (default), `allatonce` - waits till command is finished to display
                output, `file` - writes output to file, `none` - output is ignored
        threshold: (an integer (int or long))
                VIO_Real value threshold for bounding box. Default value: 0.
                flag: -threshold
        two_lines: (a boolean)
                Output on two lines: start_x y z
                 width_x y z
                flag: -two_lines
                mutually_exclusive: one_line, two_lines

Outputs::

        output_file: (an existing file name)
                output file containing bounding box corners

.. _nipype.interfaces.minc.minc.Beast:


.. index:: Beast

Beast
-----

`Link to code <http://github.com/nipy/nipype/tree/ec86b7476/nipype/interfaces/minc/minc.py#L1346>`__

Wraps command **mincbeast**

Extract brain image using BEaST (Brain Extraction using
non-local Segmentation Technique).

Examples
~~~~~~~~

>>> from nipype.interfaces.minc import Beast
>>> from nipype.interfaces.minc.testdata import nonempty_minc_data

>>> file0 = nonempty_minc_data(0)
>>> beast = Beast(input_file=file0)
>>> beast .run() # doctest: +SKIP

Inputs::

        [Mandatory]
        input_file: (a file name)
                input file
                flag: %s, position: -2
        library_dir: (a directory name)
                library directory
                flag: %s, position: -3

        [Optional]
        abspath: (a boolean, nipype default value: True)
                File paths in the library are absolute (default is relative to
                library root).
                flag: -abspath
        args: (a unicode string)
                Additional parameters to the command
                flag: %s
        clobber: (a boolean, nipype default value: True)
                Overwrite existing file.
                flag: -clobber
        confidence_level_alpha: (a float)
                Specify confidence level Alpha. Default value: 0.5
                flag: -alpha %s
        configuration_file: (a file name)
                Specify configuration file.
                flag: -configuration %s
        environ: (a dictionary with keys which are a bytes or None or a value
                 of class 'str' and with values which are a bytes or None or a value
                 of class 'str', nipype default value: {})
                Environment variables
        fill_holes: (a boolean)
                Fill holes in the binary output.
                flag: -fill
        flip_images: (a boolean)
                Flip images around the mid-sagittal plane to increase patch count.
                flag: -flip
        ignore_exception: (a boolean, nipype default value: False)
                Print an error message instead of throwing an exception in case the
                interface fails to run
        load_moments: (a boolean)
                Do not calculate moments instead use precalculatedlibrary moments.
                (for optimization purposes)
                flag: -load_moments
        median_filter: (a boolean)
                Apply a median filter on the probability map.
                flag: -median
        nlm_filter: (a boolean)
                Apply an NLM filter on the probability map (experimental).
                flag: -nlm_filter
        number_selected_images: (an integer (int or long))
                Specify number of selected images. Default value: 20
                flag: -selection_num %s
        output_file: (a file name)
                output file
                flag: %s, position: -1
        patch_size: (an integer (int or long))
                Specify patch size for single scale approach. Default value: 1.
                flag: -patch_size %s
        probability_map: (a boolean)
                Output the probability map instead of crisp mask.
                flag: -probability
        same_resolution: (a boolean)
                Output final mask with the same resolution as input file.
                flag: -same_resolution
        search_area: (an integer (int or long))
                Specify size of search area for single scale approach. Default
                value: 2.
                flag: -search_area %s
        smoothness_factor_beta: (a float)
                Specify smoothness factor Beta. Default value: 0.25
                flag: -beta %s
        terminal_output: ('stream' or 'allatonce' or 'file' or 'none')
                Control terminal output: `stream` - displays to terminal immediately
                (default), `allatonce` - waits till command is finished to display
                output, `file` - writes output to file, `none` - output is ignored
        threshold_patch_selection: (a float)
                Specify threshold for patch selection. Default value: 0.95
                flag: -threshold %s
        voxel_size: (an integer (int or long))
                Specify voxel size for calculations (4, 2, or 1).Default value: 4.
                Assumes no multiscale. Use configurationfile for multiscale.
                flag: -voxel_size %s

Outputs::

        output_file: (an existing file name)
                output mask file

.. _nipype.interfaces.minc.minc.BestLinReg:


.. index:: BestLinReg

BestLinReg
----------

`Link to code <http://github.com/nipy/nipype/tree/ec86b7476/nipype/interfaces/minc/minc.py#L3100>`__

Wraps command **bestlinreg**

Hierachial linear fitting between two files.

The bestlinreg script is part of the EZminc package:

https://github.com/BIC-MNI/EZminc/blob/master/scripts/bestlinreg.pl

Examples
~~~~~~~~

>>> from nipype.interfaces.minc import BestLinReg
>>> from nipype.interfaces.minc.testdata import nonempty_minc_data

>>> input_file = nonempty_minc_data(0)
>>> target_file = nonempty_minc_data(1)
>>> linreg = BestLinReg(source=input_file, target=target_file)
>>> linreg.run() # doctest: +SKIP

Inputs::

        [Mandatory]
        source: (an existing file name)
                source Minc file
                flag: %s, position: -4
        target: (an existing file name)
                target Minc file
                flag: %s, position: -3

        [Optional]
        args: (a unicode string)
                Additional parameters to the command
                flag: %s
        clobber: (a boolean, nipype default value: True)
                Overwrite existing file.
                flag: -clobber
        environ: (a dictionary with keys which are a bytes or None or a value
                 of class 'str' and with values which are a bytes or None or a value
                 of class 'str', nipype default value: {})
                Environment variables
        ignore_exception: (a boolean, nipype default value: False)
                Print an error message instead of throwing an exception in case the
                interface fails to run
        output_mnc: (a file name)
                output mnc file
                flag: %s, position: -1
        output_xfm: (a file name)
                output xfm file
                flag: %s, position: -2
        terminal_output: ('stream' or 'allatonce' or 'file' or 'none')
                Control terminal output: `stream` - displays to terminal immediately
                (default), `allatonce` - waits till command is finished to display
                output, `file` - writes output to file, `none` - output is ignored
        verbose: (a boolean)
                Print out log messages. Default: False.
                flag: -verbose

Outputs::

        output_mnc: (an existing file name)
                output mnc file
        output_xfm: (an existing file name)
                output xfm file

.. _nipype.interfaces.minc.minc.BigAverage:


.. index:: BigAverage

BigAverage
----------

`Link to code <http://github.com/nipy/nipype/tree/ec86b7476/nipype/interfaces/minc/minc.py#L3467>`__

Wraps command **mincbigaverage**

Average 1000's of MINC files in linear time.

mincbigaverage is designed to discretise the problem of averaging either
a large number of input files or averaging a smaller number of large
files. (>1GB each). There is also some code included to perform "robust"
averaging in which only the most common features are kept via down-weighting
outliers beyond a standard deviation.

One advantage of mincbigaverage is that it avoids issues around the number
of possible open files in HDF/netCDF. In short if you have more than 100
files open at once while averaging things will slow down significantly.

mincbigaverage does this via a iterative approach to averaging files and
is a direct drop in replacement for mincaverage. That said not all the
arguments of mincaverage are supported in mincbigaverage but they should
be.

This tool is part of the minc-widgets package:

https://github.com/BIC-MNI/minc-widgets/blob/master/mincbigaverage/mincbigaverage

Examples
~~~~~~~~

>>> from nipype.interfaces.minc import BigAverage
>>> from nipype.interfaces.minc.testdata import nonempty_minc_data

>>> files = [nonempty_minc_data(i) for i in range(3)]
>>> average = BigAverage(input_files=files, output_float=True, robust=True)
>>> average.run() # doctest: +SKIP

Inputs::

        [Mandatory]
        input_files: (a list of items which are a file name)
                input file(s)
                flag: %s, position: -2

        [Optional]
        args: (a unicode string)
                Additional parameters to the command
                flag: %s
        clobber: (a boolean, nipype default value: True)
                Overwrite existing file.
                flag: --clobber
        environ: (a dictionary with keys which are a bytes or None or a value
                 of class 'str' and with values which are a bytes or None or a value
                 of class 'str', nipype default value: {})
                Environment variables
        ignore_exception: (a boolean, nipype default value: False)
                Print an error message instead of throwing an exception in case the
                interface fails to run
        output_file: (a file name)
                output file
                flag: %s, position: -1
        output_float: (a boolean)
                Output files with float precision.
                flag: --float
        robust: (a boolean)
                Perform robust averaging, features that are outside 1
                standarddeviation from the mean are downweighted. Works well for
                noisydata with artifacts. see the --tmpdir option if you have alarge
                number of input files.
                flag: -robust
        sd_file: (a file name)
                Place standard deviation image in specified file.
                flag: --sdfile %s
        terminal_output: ('stream' or 'allatonce' or 'file' or 'none')
                Control terminal output: `stream` - displays to terminal immediately
                (default), `allatonce` - waits till command is finished to display
                output, `file` - writes output to file, `none` - output is ignored
        tmpdir: (a directory name)
                temporary files directory
                flag: -tmpdir %s
        verbose: (a boolean)
                Print out log messages. Default: False.
                flag: --verbose

Outputs::

        output_file: (an existing file name)
                output file
        sd_file: (an existing file name)
                standard deviation image

.. _nipype.interfaces.minc.minc.Blob:


.. index:: Blob

Blob
----

`Link to code <http://github.com/nipy/nipype/tree/ec86b7476/nipype/interfaces/minc/minc.py#L888>`__

Wraps command **mincblob**

Calculate blobs from minc deformation grids.

Examples
~~~~~~~~

>>> from nipype.interfaces.minc import Blob
>>> from nipype.interfaces.minc.testdata import minc2Dfile

>>> blob = Blob(input_file=minc2Dfile, output_file='/tmp/tmp.mnc', trace=True)
>>> blob.run() # doctest: +SKIP

Inputs::

        [Mandatory]
        input_file: (an existing file name)
                input file to blob
                flag: %s, position: -2

        [Optional]
        args: (a unicode string)
                Additional parameters to the command
                flag: %s
        determinant: (a boolean)
                compute the determinant (exact growth and shrinkage) -- SLOW
                flag: -determinant
        environ: (a dictionary with keys which are a bytes or None or a value
                 of class 'str' and with values which are a bytes or None or a value
                 of class 'str', nipype default value: {})
                Environment variables
        ignore_exception: (a boolean, nipype default value: False)
                Print an error message instead of throwing an exception in case the
                interface fails to run
        magnitude: (a boolean)
                compute the magnitude of the displacement vector
                flag: -magnitude
        output_file: (a file name)
                output file
                flag: %s, position: -1
        terminal_output: ('stream' or 'allatonce' or 'file' or 'none')
                Control terminal output: `stream` - displays to terminal immediately
                (default), `allatonce` - waits till command is finished to display
                output, `file` - writes output to file, `none` - output is ignored
        trace: (a boolean)
                compute the trace (approximate growth and shrinkage) -- FAST
                flag: -trace
        translation: (a boolean)
                compute translation (structure displacement)
                flag: -translation

Outputs::

        output_file: (an existing file name)
                output file

.. _nipype.interfaces.minc.minc.Blur:


.. index:: Blur

Blur
----

`Link to code <http://github.com/nipy/nipype/tree/ec86b7476/nipype/interfaces/minc/minc.py#L1630>`__

Wraps command **mincblur**

Convolve an input volume with a Gaussian blurring kernel of
user-defined width.  Optionally, the first partial derivatives
and the gradient magnitude volume can be calculated.

Examples
~~~~~~~~

>>> from nipype.interfaces.minc import Blur
>>> from nipype.interfaces.minc.testdata import minc3Dfile

(1) Blur  an  input  volume with a 6mm fwhm isotropic Gaussian
blurring kernel:

>>> blur = Blur(input_file=minc3Dfile, fwhm=6, output_file_base='/tmp/out_6')
>>> blur.run() # doctest: +SKIP

mincblur will create /tmp/out_6_blur.mnc.

(2) Calculate the blurred and gradient magnitude data:

>>> blur = Blur(input_file=minc3Dfile, fwhm=6, gradient=True, output_file_base='/tmp/out_6')
>>> blur.run() # doctest: +SKIP

will create /tmp/out_6_blur.mnc and /tmp/out_6_dxyz.mnc.

(3) Calculate the blurred data, the partial derivative volumes
and  the gradient magnitude for the same data:

>>> blur = Blur(input_file=minc3Dfile, fwhm=6, partial=True, output_file_base='/tmp/out_6')
>>> blur.run() # doctest: +SKIP

will create /tmp/out_6_blur.mnc, /tmp/out_6_dx.mnc,
/tmp/out_6_dy.mnc, /tmp/out_6_dz.mnc and /tmp/out_6_dxyz.mnc.

Inputs::

        [Mandatory]
        fwhm: (a float)
                Full-width-half-maximum of gaussian kernel. Default value: 0.
                flag: -fwhm %s
                mutually_exclusive: fwhm, fwhm3d, standard_dev
        fwhm3d: (a tuple of the form: (a float, a float, a float))
                Full-width-half-maximum of gaussian kernel.Default value:
                -1.79769e+308 -1.79769e+308 -1.79769e+308.
                flag: -3dfwhm %s %s %s
                mutually_exclusive: fwhm, fwhm3d, standard_dev
        input_file: (an existing file name)
                input file
                flag: %s, position: -2
        standard_dev: (a float)
                Standard deviation of gaussian kernel. Default value: 0.
                flag: -standarddev %s
                mutually_exclusive: fwhm, fwhm3d, standard_dev

        [Optional]
        args: (a unicode string)
                Additional parameters to the command
                flag: %s
        clobber: (a boolean, nipype default value: True)
                Overwrite existing file.
                flag: -clobber
        dimensions: (1 or 2 or 3)
                Number of dimensions to blur (either 1,2 or 3). Default value: 3.
                flag: -dimensions %s
        environ: (a dictionary with keys which are a bytes or None or a value
                 of class 'str' and with values which are a bytes or None or a value
                 of class 'str', nipype default value: {})
                Environment variables
        gaussian: (a boolean)
                Use a gaussian smoothing kernel (default).
                flag: -gaussian
                mutually_exclusive: gaussian, rect
        gradient: (a boolean)
                Create the gradient magnitude volume as well.
                flag: -gradient
        ignore_exception: (a boolean, nipype default value: False)
                Print an error message instead of throwing an exception in case the
                interface fails to run
        no_apodize: (a boolean)
                Do not apodize the data before blurring.
                flag: -no_apodize
        output_file_base: (a file name)
                output file base
                flag: %s, position: -1
        partial: (a boolean)
                Create the partial derivative and gradient magnitude volumes as
                well.
                flag: -partial
        rect: (a boolean)
                Use a rect (box) smoothing kernel.
                flag: -rect
                mutually_exclusive: gaussian, rect
        terminal_output: ('stream' or 'allatonce' or 'file' or 'none')
                Control terminal output: `stream` - displays to terminal immediately
                (default), `allatonce` - waits till command is finished to display
                output, `file` - writes output to file, `none` - output is ignored

Outputs::

        gradient_dxyz: (a file name)
                Gradient dxyz.
        output_file: (an existing file name)
                Blurred output file.
        partial_dx: (a file name)
                Partial gradient dx.
        partial_dxyz: (a file name)
                Partial gradient dxyz.
        partial_dy: (a file name)
                Partial gradient dy.
        partial_dz: (a file name)
                Partial gradient dz.

.. _nipype.interfaces.minc.minc.Calc:


.. index:: Calc

Calc
----

`Link to code <http://github.com/nipy/nipype/tree/ec86b7476/nipype/interfaces/minc/minc.py#L1100>`__

Wraps command **minccalc**

Compute an expression using MINC files as input.

Examples
~~~~~~~~

>>> from nipype.interfaces.minc import Calc
>>> from nipype.interfaces.minc.testdata import nonempty_minc_data

>>> file0 = nonempty_minc_data(0)
>>> file1 = nonempty_minc_data(1)
>>> calc = Calc(input_files=[file0, file1], output_file='/tmp/calc.mnc', expression='A[0] + A[1]') # add files together
>>> calc.run() # doctest: +SKIP

Inputs::

        [Mandatory]
        expfile: (a file name)
                Name of file containing expression.
                flag: -expfile %s
                mutually_exclusive: expression, expfile
        expression: (a unicode string)
                Expression to use in calculations.
                flag: -expression '%s'
                mutually_exclusive: expression, expfile
        filelist: (a file name)
                Specify the name of a file containing input file names.
                flag: -filelist %s
                mutually_exclusive: input_files, filelist
        input_files: (a list of items which are a file name)
                input file(s) for calculation
                flag: %s, position: -2

        [Optional]
        args: (a unicode string)
                Additional parameters to the command
                flag: %s
        check_dimensions: (a boolean)
                Check that files have matching dimensions (default).
                flag: -check_dimensions
                mutually_exclusive: check_dimensions, no_check_dimensions
        clobber: (a boolean, nipype default value: True)
                Overwrite existing file.
                flag: -clobber
        copy_header: (a boolean)
                Copy all of the header from the first file.
                flag: -copy_header
                mutually_exclusive: copy_header, no_copy_header
        debug: (a boolean)
                Print out debugging messages.
                flag: -debug
        environ: (a dictionary with keys which are a bytes or None or a value
                 of class 'str' and with values which are a bytes or None or a value
                 of class 'str', nipype default value: {})
                Environment variables
        eval_width: (an integer (int or long))
                Number of voxels to evaluate simultaneously.
                flag: -eval_width %s
        format_byte: (a boolean)
                Write out byte data.
                flag: -byte
                mutually_exclusive: format_filetype, format_byte, format_short,
                 format_int, format_long, format_float, format_double,
                 format_signed, format_unsigned
        format_double: (a boolean)
                Write out double-precision floating-point data.
                flag: -double
                mutually_exclusive: format_filetype, format_byte, format_short,
                 format_int, format_long, format_float, format_double,
                 format_signed, format_unsigned
        format_filetype: (a boolean)
                Use data type of first file (default).
                flag: -filetype
                mutually_exclusive: format_filetype, format_byte, format_short,
                 format_int, format_long, format_float, format_double,
                 format_signed, format_unsigned
        format_float: (a boolean)
                Write out single-precision floating-point data.
                flag: -float
                mutually_exclusive: format_filetype, format_byte, format_short,
                 format_int, format_long, format_float, format_double,
                 format_signed, format_unsigned
        format_int: (a boolean)
                Write out 32-bit integer data.
                flag: -int
                mutually_exclusive: format_filetype, format_byte, format_short,
                 format_int, format_long, format_float, format_double,
                 format_signed, format_unsigned
        format_long: (a boolean)
                Superseded by -int.
                flag: -long
                mutually_exclusive: format_filetype, format_byte, format_short,
                 format_int, format_long, format_float, format_double,
                 format_signed, format_unsigned
        format_short: (a boolean)
                Write out short integer data.
                flag: -short
                mutually_exclusive: format_filetype, format_byte, format_short,
                 format_int, format_long, format_float, format_double,
                 format_signed, format_unsigned
        format_signed: (a boolean)
                Write signed integer data.
                flag: -signed
                mutually_exclusive: format_filetype, format_byte, format_short,
                 format_int, format_long, format_float, format_double,
                 format_signed, format_unsigned
        format_unsigned: (a boolean)
                Write unsigned integer data (default).
                flag: -unsigned
                mutually_exclusive: format_filetype, format_byte, format_short,
                 format_int, format_long, format_float, format_double,
                 format_signed, format_unsigned
        ignore_exception: (a boolean, nipype default value: False)
                Print an error message instead of throwing an exception in case the
                interface fails to run
        ignore_nan: (a boolean)
                Ignore invalid data (NaN) for accumulations.
                flag: -ignore_nan
        max_buffer_size_in_kb: (a long integer >= 0)
                Specify the maximum size of the internal buffers (in kbytes).
                flag: -max_buffer_size_in_kb %d
        no_check_dimensions: (a boolean)
                Do not check that files have matching dimensions.
                flag: -nocheck_dimensions
                mutually_exclusive: check_dimensions, no_check_dimensions
        no_copy_header: (a boolean)
                Do not copy all of the header from the first file.
                flag: -nocopy_header
                mutually_exclusive: copy_header, no_copy_header
        outfiles: (a list of items which are a tuple of the form: (a unicode
                 string, a file name))
        output_file: (a file name)
                output file
                flag: %s, position: -1
        output_illegal: (a boolean)
                Value to write out when an illegal operation is done. Default value:
                1.79769e+308
                flag: -illegal_value
                mutually_exclusive: output_nan, output_zero, output_illegal_value
        output_nan: (a boolean)
                Output NaN when an illegal operation is done (default).
                flag: -nan
                mutually_exclusive: output_nan, output_zero, output_illegal_value
        output_zero: (a boolean)
                Output zero when an illegal operation is done.
                flag: -zero
                mutually_exclusive: output_nan, output_zero, output_illegal_value
        propagate_nan: (a boolean)
                Invalid data in any file at a voxel produces a NaN (default).
                flag: -propagate_nan
        quiet: (a boolean)
                Do not print out log messages.
                flag: -quiet
                mutually_exclusive: verbose, quiet
        terminal_output: ('stream' or 'allatonce' or 'file' or 'none')
                Control terminal output: `stream` - displays to terminal immediately
                (default), `allatonce` - waits till command is finished to display
                output, `file` - writes output to file, `none` - output is ignored
        two: (a boolean)
                Create a MINC 2 output file.
                flag: -2
        verbose: (a boolean)
                Print out log messages (default).
                flag: -verbose
                mutually_exclusive: verbose, quiet
        voxel_range: (a tuple of the form: (an integer (int or long), an
                 integer (int or long)))
                Valid range for output data.
                flag: -range %d %d

Outputs::

        output_file: (an existing file name)
                output file

.. _nipype.interfaces.minc.minc.Convert:


.. index:: Convert

Convert
-------

`Link to code <http://github.com/nipy/nipype/tree/ec86b7476/nipype/interfaces/minc/minc.py#L402>`__

Wraps command **mincconvert**

convert between MINC 1 to MINC 2 format.

Examples
~~~~~~~~

>>> from nipype.interfaces.minc import Convert
>>> from nipype.interfaces.minc.testdata import minc2Dfile
>>> c = Convert(input_file=minc2Dfile, output_file='/tmp/out.mnc', two=True) # Convert to MINC2 format.
>>> c.run() # doctest: +SKIP

Inputs::

        [Mandatory]
        input_file: (an existing file name)
                input file for converting
                flag: %s, position: -2

        [Optional]
        args: (a unicode string)
                Additional parameters to the command
                flag: %s
        chunk: (a long integer >= 0)
                Set the target block size for chunking (0 default, >1 block size).
                flag: -chunk %d
        clobber: (a boolean, nipype default value: True)
                Overwrite existing file.
                flag: -clobber
        compression: (0 or 1 or 2 or 3 or 4 or 5 or 6 or 7 or 8 or 9)
                Set the compression level, from 0 (disabled) to 9 (maximum).
                flag: -compress %s
        environ: (a dictionary with keys which are a bytes or None or a value
                 of class 'str' and with values which are a bytes or None or a value
                 of class 'str', nipype default value: {})
                Environment variables
        ignore_exception: (a boolean, nipype default value: False)
                Print an error message instead of throwing an exception in case the
                interface fails to run
        output_file: (a file name)
                output file
                flag: %s, position: -1
        template: (a boolean)
                Create a template file. The dimensions, variables, andattributes of
                the input file are preserved but all data it set to zero.
                flag: -template
        terminal_output: ('stream' or 'allatonce' or 'file' or 'none')
                Control terminal output: `stream` - displays to terminal immediately
                (default), `allatonce` - waits till command is finished to display
                output, `file` - writes output to file, `none` - output is ignored
        two: (a boolean)
                Create a MINC 2 output file.
                flag: -2

Outputs::

        output_file: (an existing file name)
                output file

.. _nipype.interfaces.minc.minc.Copy:


.. index:: Copy

Copy
----

`Link to code <http://github.com/nipy/nipype/tree/ec86b7476/nipype/interfaces/minc/minc.py#L453>`__

Wraps command **minccopy**

Copy image values from one MINC file to another. Both the input
and output files must exist, and the images in both files must
have an equal number dimensions and equal dimension lengths.

NOTE: This program is intended primarily for use with scripts
such as mincedit. It does not follow the typical design rules of
most MINC command-line tools and therefore should be used only
with caution.

Inputs::

        [Mandatory]
        input_file: (an existing file name)
                input file to copy
                flag: %s, position: -2

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
        output_file: (a file name)
                output file
                flag: %s, position: -1
        pixel_values: (a boolean)
                Copy pixel values as is.
                flag: -pixel_values
                mutually_exclusive: pixel_values, real_values
        real_values: (a boolean)
                Copy real pixel intensities (default).
                flag: -real_values
                mutually_exclusive: pixel_values, real_values
        terminal_output: ('stream' or 'allatonce' or 'file' or 'none')
                Control terminal output: `stream` - displays to terminal immediately
                (default), `allatonce` - waits till command is finished to display
                output, `file` - writes output to file, `none` - output is ignored

Outputs::

        output_file: (an existing file name)
                output file

.. _nipype.interfaces.minc.minc.Dump:


.. index:: Dump

Dump
----

`Link to code <http://github.com/nipy/nipype/tree/ec86b7476/nipype/interfaces/minc/minc.py#L621>`__

Wraps command **mincdump**

Dump a MINC file. Typically used in conjunction with mincgen (see Gen).

Examples
~~~~~~~~

>>> from nipype.interfaces.minc import Dump
>>> from nipype.interfaces.minc.testdata import minc2Dfile

>>> dump = Dump(input_file=minc2Dfile)
>>> dump.run() # doctest: +SKIP

>>> dump = Dump(input_file=minc2Dfile, output_file='/tmp/out.txt', precision=(3, 4))
>>> dump.run() # doctest: +SKIP

Inputs::

        [Mandatory]
        input_file: (an existing file name)
                input file
                flag: %s, position: -2

        [Optional]
        annotations_brief: ('c' or 'f')
                Brief annotations for C or Fortran indices in data.
                flag: -b %s
                mutually_exclusive: annotations_brief, annotations_full
        annotations_full: ('c' or 'f')
                Full annotations for C or Fortran indices in data.
                flag: -f %s
                mutually_exclusive: annotations_brief, annotations_full
        args: (a unicode string)
                Additional parameters to the command
                flag: %s
        coordinate_data: (a boolean)
                Coordinate variable data and header information.
                flag: -c
                mutually_exclusive: coordinate_data, header_data
        environ: (a dictionary with keys which are a bytes or None or a value
                 of class 'str' and with values which are a bytes or None or a value
                 of class 'str', nipype default value: {})
                Environment variables
        header_data: (a boolean)
                Header information only, no data.
                flag: -h
                mutually_exclusive: coordinate_data, header_data
        ignore_exception: (a boolean, nipype default value: False)
                Print an error message instead of throwing an exception in case the
                interface fails to run
        line_length: (a long integer >= 0)
                Line length maximum in data section (default 80).
                flag: -l %d
        netcdf_name: (a unicode string)
                Name for netCDF (default derived from file name).
                flag: -n %s
        out_file: (a file name)
                flag: > %s, position: -1
        output_file: (a file name)
                output file
        precision: (an integer (int or long) or a tuple of the form: (an
                 integer (int or long), an integer (int or long)))
                Display floating-point values with less precision
                flag: %s
        terminal_output: ('stream' or 'allatonce' or 'file' or 'none')
                Control terminal output: `stream` - displays to terminal immediately
                (default), `allatonce` - waits till command is finished to display
                output, `file` - writes output to file, `none` - output is ignored
        variables: (a list of items which are a unicode string)
                Output data for specified variables only.
                flag: -v %s

Outputs::

        output_file: (an existing file name)
                output file

.. _nipype.interfaces.minc.minc.Extract:


.. index:: Extract

Extract
-------

`Link to code <http://github.com/nipy/nipype/tree/ec86b7476/nipype/interfaces/minc/minc.py#L218>`__

Wraps command **mincextract**

Dump a hyperslab of MINC file data.

Examples
~~~~~~~~

>>> from nipype.interfaces.minc import Extract
>>> from nipype.interfaces.minc.testdata import minc2Dfile

>>> extract = Extract(input_file=minc2Dfile)
>>> extract.run() # doctest: +SKIP

>>> extract = Extract(input_file=minc2Dfile, start=[3, 10, 5], count=[4, 4, 4]) # extract a 4x4x4 slab at offset [3, 10, 5]
>>> extract.run() # doctest: +SKIP

Inputs::

        [Mandatory]
        input_file: (an existing file name)
                input file
                flag: %s, position: -2

        [Optional]
        args: (a unicode string)
                Additional parameters to the command
                flag: %s
        count: (a list of items which are an integer (int or long))
                Specifies edge lengths of hyperslab to read.
                flag: -count %s
        environ: (a dictionary with keys which are a bytes or None or a value
                 of class 'str' and with values which are a bytes or None or a value
                 of class 'str', nipype default value: {})
                Environment variables
        flip_any_direction: (a boolean)
                Do not flip images (Default).
                flag: -any_direction
                mutually_exclusive: flip_positive_direction,
                 flip_negative_direction, flip_any_direction
        flip_negative_direction: (a boolean)
                Flip images to always have negative direction.
                flag: -negative_direction
                mutually_exclusive: flip_positive_direction,
                 flip_negative_direction, flip_any_direction
        flip_positive_direction: (a boolean)
                Flip images to always have positive direction.
                flag: -positive_direction
                mutually_exclusive: flip_positive_direction,
                 flip_negative_direction, flip_any_direction
        flip_x_any: (a boolean)
                Don't flip images along x-axis (default).
                flag: -xanydirection
                mutually_exclusive: flip_x_positive, flip_x_negative, flip_x_any
        flip_x_negative: (a boolean)
                Flip images to give negative xspace:step value (right-to-left).
                flag: -xdirection
                mutually_exclusive: flip_x_positive, flip_x_negative, flip_x_any
        flip_x_positive: (a boolean)
                Flip images to give positive xspace:step value (left-to-right).
                flag: +xdirection
                mutually_exclusive: flip_x_positive, flip_x_negative, flip_x_any
        flip_y_any: (a boolean)
                Don't flip images along y-axis (default).
                flag: -yanydirection
                mutually_exclusive: flip_y_positive, flip_y_negative, flip_y_any
        flip_y_negative: (a boolean)
                Flip images to give negative yspace:step value (ant-to-post).
                flag: -ydirection
                mutually_exclusive: flip_y_positive, flip_y_negative, flip_y_any
        flip_y_positive: (a boolean)
                Flip images to give positive yspace:step value (post-to-ant).
                flag: +ydirection
                mutually_exclusive: flip_y_positive, flip_y_negative, flip_y_any
        flip_z_any: (a boolean)
                Don't flip images along z-axis (default).
                flag: -zanydirection
                mutually_exclusive: flip_z_positive, flip_z_negative, flip_z_any
        flip_z_negative: (a boolean)
                Flip images to give negative zspace:step value (sup-to-inf).
                flag: -zdirection
                mutually_exclusive: flip_z_positive, flip_z_negative, flip_z_any
        flip_z_positive: (a boolean)
                Flip images to give positive zspace:step value (inf-to-sup).
                flag: +zdirection
                mutually_exclusive: flip_z_positive, flip_z_negative, flip_z_any
        ignore_exception: (a boolean, nipype default value: False)
                Print an error message instead of throwing an exception in case the
                interface fails to run
        image_maximum: (a float)
                Specify the maximum real image value for normalization.Default
                value: 1.79769e+308.
                flag: -image_maximum %s
        image_minimum: (a float)
                Specify the minimum real image value for normalization.Default
                value: 1.79769e+308.
                flag: -image_minimum %s
        image_range: (a tuple of the form: (a float, a float))
                Specify the range of real image values for normalization.
                flag: -image_range %s %s
        nonormalize: (a boolean)
                Turn off pixel normalization.
                flag: -nonormalize
                mutually_exclusive: normalize, nonormalize
        normalize: (a boolean)
                Normalize integer pixel values to file max and min.
                flag: -normalize
                mutually_exclusive: normalize, nonormalize
        out_file: (a file name)
                flag: > %s, position: -1
        output_file: (a file name)
                output file
        start: (a list of items which are an integer (int or long))
                Specifies corner of hyperslab (C conventions for indices).
                flag: -start %s
        terminal_output: ('stream' or 'allatonce' or 'file' or 'none')
                Control terminal output: `stream` - displays to terminal immediately
                (default), `allatonce` - waits till command is finished to display
                output, `file` - writes output to file, `none` - output is ignored
        write_ascii: (a boolean)
                Write out data as ascii strings (default).
                flag: -ascii
                mutually_exclusive: write_ascii, write_ascii, write_byte,
                 write_short, write_int, write_long, write_float, write_double,
                 write_signed, write_unsigned
        write_byte: (a boolean)
                Write out data as bytes.
                flag: -byte
                mutually_exclusive: write_ascii, write_ascii, write_byte,
                 write_short, write_int, write_long, write_float, write_double,
                 write_signed, write_unsigned
        write_double: (a boolean)
                Write out data as double precision floating-point values.
                flag: -double
                mutually_exclusive: write_ascii, write_ascii, write_byte,
                 write_short, write_int, write_long, write_float, write_double,
                 write_signed, write_unsigned
        write_float: (a boolean)
                Write out data as single precision floating-point values.
                flag: -float
                mutually_exclusive: write_ascii, write_ascii, write_byte,
                 write_short, write_int, write_long, write_float, write_double,
                 write_signed, write_unsigned
        write_int: (a boolean)
                Write out data as 32-bit integers.
                flag: -int
                mutually_exclusive: write_ascii, write_ascii, write_byte,
                 write_short, write_int, write_long, write_float, write_double,
                 write_signed, write_unsigned
        write_long: (a boolean)
                Superseded by write_int.
                flag: -long
                mutually_exclusive: write_ascii, write_ascii, write_byte,
                 write_short, write_int, write_long, write_float, write_double,
                 write_signed, write_unsigned
        write_range: (a tuple of the form: (a float, a float))
                Specify the range of output values
                Default value: 1.79769e+308 1.79769e+308.
                flag: -range %s %s
        write_short: (a boolean)
                Write out data as short integers.
                flag: -short
                mutually_exclusive: write_ascii, write_ascii, write_byte,
                 write_short, write_int, write_long, write_float, write_double,
                 write_signed, write_unsigned
        write_signed: (a boolean)
                Write out signed data.
                flag: -signed
                mutually_exclusive: write_signed, write_unsigned
        write_unsigned: (a boolean)
                Write out unsigned data.
                flag: -unsigned
                mutually_exclusive: write_signed, write_unsigned

Outputs::

        output_file: (an existing file name)
                output file in raw/text format

.. _nipype.interfaces.minc.minc.Gennlxfm:


.. index:: Gennlxfm

Gennlxfm
--------

`Link to code <http://github.com/nipy/nipype/tree/ec86b7476/nipype/interfaces/minc/minc.py#L2941>`__

Wraps command **gennlxfm**

Generate nonlinear xfms. Currently only identity xfms
are supported!

This tool is part of minc-widgets:

https://github.com/BIC-MNI/minc-widgets/blob/master/gennlxfm/gennlxfm

Examples
~~~~~~~~

>>> from nipype.interfaces.minc import Gennlxfm
>>> from nipype.interfaces.minc.testdata import minc2Dfile
>>> gennlxfm = Gennlxfm(step=1, like=minc2Dfile)
>>> gennlxfm.run() # doctest: +SKIP

Inputs::

        [Mandatory]

        [Optional]
        args: (a unicode string)
                Additional parameters to the command
                flag: %s
        clobber: (a boolean, nipype default value: True)
                Overwrite existing file.
                flag: -clobber
        environ: (a dictionary with keys which are a bytes or None or a value
                 of class 'str' and with values which are a bytes or None or a value
                 of class 'str', nipype default value: {})
                Environment variables
        ident: (a boolean)
                Generate an identity xfm. Default: False.
                flag: -ident
        ignore_exception: (a boolean, nipype default value: False)
                Print an error message instead of throwing an exception in case the
                interface fails to run
        like: (an existing file name)
                Generate a nlxfm like this file.
                flag: -like %s
        output_file: (a file name)
                output file
                flag: %s, position: -1
        step: (an integer (int or long))
                Output ident xfm step [default: 1].
                flag: -step %s
        terminal_output: ('stream' or 'allatonce' or 'file' or 'none')
                Control terminal output: `stream` - displays to terminal immediately
                (default), `allatonce` - waits till command is finished to display
                output, `file` - writes output to file, `none` - output is ignored
        verbose: (a boolean)
                Print out log messages. Default: False.
                flag: -verbose

Outputs::

        output_file: (an existing file name)
                output file
        output_grid: (an existing file name)
                output grid

.. _nipype.interfaces.minc.minc.Math:


.. index:: Math

Math
----

`Link to code <http://github.com/nipy/nipype/tree/ec86b7476/nipype/interfaces/minc/minc.py#L2040>`__

Wraps command **mincmath**

Various mathematical operations supplied by mincmath.

Examples
~~~~~~~~

>>> from nipype.interfaces.minc import Math
>>> from nipype.interfaces.minc.testdata import minc2Dfile

Scale: volume*3.0 + 2:

>>> scale = Math(input_files=[minc2Dfile], scale=(3.0, 2))
>>> scale.run() # doctest: +SKIP

Test if >= 1.5:

>>> gt = Math(input_files=[minc2Dfile], test_gt=1.5)
>>> gt.run() # doctest: +SKIP

Inputs::

        [Mandatory]
        filelist: (a file name)
                Specify the name of a file containing input file names.
                flag: -filelist %s
                mutually_exclusive: input_files, filelist
        input_files: (a list of items which are a file name)
                input file(s) for calculation
                flag: %s, position: -2
                mutually_exclusive: input_files, filelist

        [Optional]
        abs: (a boolean)
                Take absolute value of a volume.
                flag: -abs
        args: (a unicode string)
                Additional parameters to the command
                flag: %s
        calc_add: (a boolean or a float)
                Add N volumes or volume + constant.
                flag: -add
        calc_and: (a boolean)
                Calculate vol1 && vol2 (&& ...).
                flag: -and
        calc_div: (a boolean or a float)
                Divide 2 volumes or volume / constant.
                flag: -div
        calc_mul: (a boolean or a float)
                Multiply N volumes or volume * constant.
                flag: -mult
        calc_not: (a boolean)
                Calculate !vol1.
                flag: -not
        calc_or: (a boolean)
                Calculate vol1 || vol2 (|| ...).
                flag: -or
        calc_sub: (a boolean or a float)
                Subtract 2 volumes or volume - constant.
                flag: -sub
        check_dimensions: (a boolean)
                Check that dimension info matches across files (default).
                flag: -check_dimensions
                mutually_exclusive: check_dimensions, no_check_dimensions
        clamp: (a tuple of the form: (a float, a float))
                Clamp a volume to lie between two values.
                flag: -clamp -const2 %s %s
        clobber: (a boolean, nipype default value: True)
                Overwrite existing file.
                flag: -clobber
        copy_header: (a boolean)
                Copy all of the header from the first file (default for one file).
                flag: -copy_header
                mutually_exclusive: copy_header, no_copy_header
        count_valid: (a boolean)
                Count the number of valid values in N volumes.
                flag: -count_valid
        dimension: (a unicode string)
                Specify a dimension along which we wish to perform a calculation.
                flag: -dimension %s
        environ: (a dictionary with keys which are a bytes or None or a value
                 of class 'str' and with values which are a bytes or None or a value
                 of class 'str', nipype default value: {})
                Environment variables
        exp: (a tuple of the form: (a float, a float))
                Calculate c2*exp(c1*x). Both constants must be specified.
                flag: -exp -const2 %s %s
        format_byte: (a boolean)
                Write out byte data.
                flag: -byte
                mutually_exclusive: format_filetype, format_byte, format_short,
                 format_int, format_long, format_float, format_double,
                 format_signed, format_unsigned
        format_double: (a boolean)
                Write out double-precision floating-point data.
                flag: -double
                mutually_exclusive: format_filetype, format_byte, format_short,
                 format_int, format_long, format_float, format_double,
                 format_signed, format_unsigned
        format_filetype: (a boolean)
                Use data type of first file (default).
                flag: -filetype
                mutually_exclusive: format_filetype, format_byte, format_short,
                 format_int, format_long, format_float, format_double,
                 format_signed, format_unsigned
        format_float: (a boolean)
                Write out single-precision floating-point data.
                flag: -float
                mutually_exclusive: format_filetype, format_byte, format_short,
                 format_int, format_long, format_float, format_double,
                 format_signed, format_unsigned
        format_int: (a boolean)
                Write out 32-bit integer data.
                flag: -int
                mutually_exclusive: format_filetype, format_byte, format_short,
                 format_int, format_long, format_float, format_double,
                 format_signed, format_unsigned
        format_long: (a boolean)
                Superseded by -int.
                flag: -long
                mutually_exclusive: format_filetype, format_byte, format_short,
                 format_int, format_long, format_float, format_double,
                 format_signed, format_unsigned
        format_short: (a boolean)
                Write out short integer data.
                flag: -short
                mutually_exclusive: format_filetype, format_byte, format_short,
                 format_int, format_long, format_float, format_double,
                 format_signed, format_unsigned
        format_signed: (a boolean)
                Write signed integer data.
                flag: -signed
                mutually_exclusive: format_filetype, format_byte, format_short,
                 format_int, format_long, format_float, format_double,
                 format_signed, format_unsigned
        format_unsigned: (a boolean)
                Write unsigned integer data (default).
                flag: -unsigned
                mutually_exclusive: format_filetype, format_byte, format_short,
                 format_int, format_long, format_float, format_double,
                 format_signed, format_unsigned
        ignore_exception: (a boolean, nipype default value: False)
                Print an error message instead of throwing an exception in case the
                interface fails to run
        ignore_nan: (a boolean)
                Ignore invalid data (NaN) for accumulations.
                flag: -ignore_nan
        invert: (a float)
                Calculate 1/c.
                flag: -invert -const %s
        isnan: (a boolean)
                Test for NaN values in vol1.
                flag: -isnan
        log: (a tuple of the form: (a float, a float))
                Calculate log(x/c2)/c1. The constants c1 and c2 default to 1.
                flag: -log -const2 %s %s
        max_buffer_size_in_kb: (a long integer >= 0)
                Specify the maximum size of the internal buffers (in kbytes).
                flag: -max_buffer_size_in_kb %d
        maximum: (a boolean)
                Find maximum of N volumes.
                flag: -maximum
        minimum: (a boolean)
                Find minimum of N volumes.
                flag: -minimum
        nisnan: (a boolean)
                Negation of -isnan.
                flag: -nisnan
        no_check_dimensions: (a boolean)
                Do not check dimension info.
                flag: -nocheck_dimensions
                mutually_exclusive: check_dimensions, no_check_dimensions
        no_copy_header: (a boolean)
                Do not copy all of the header from the first file (default for many
                files)).
                flag: -nocopy_header
                mutually_exclusive: copy_header, no_copy_header
        nsegment: (a tuple of the form: (a float, a float))
                Opposite of -segment: within range = 0, outside range = 1.
                flag: -nsegment -const2 %s %s
        output_file: (a file name)
                output file
                flag: %s, position: -1
        output_illegal: (a boolean)
                Value to write out when an illegal operationis done. Default value:
                1.79769e+308
                flag: -illegal_value
                mutually_exclusive: output_nan, output_zero, output_illegal_value
        output_nan: (a boolean)
                Output NaN when an illegal operation is done (default).
                flag: -nan
                mutually_exclusive: output_nan, output_zero, output_illegal_value
        output_zero: (a boolean)
                Output zero when an illegal operation is done.
                flag: -zero
                mutually_exclusive: output_nan, output_zero, output_illegal_value
        percentdiff: (a float)
                Percent difference between 2 volumes, thresholded (const def=0.0).
                flag: -percentdiff
        propagate_nan: (a boolean)
                Invalid data in any file at a voxel produces a NaN (default).
                flag: -propagate_nan
        scale: (a tuple of the form: (a float, a float))
                Scale a volume: volume * c1 + c2.
                flag: -scale -const2 %s %s
        segment: (a tuple of the form: (a float, a float))
                Segment a volume using range of -const2: within range = 1, outside
                range = 0.
                flag: -segment -const2 %s %s
        sqrt: (a boolean)
                Take square root of a volume.
                flag: -sqrt
        square: (a boolean)
                Take square of a volume.
                flag: -square
        terminal_output: ('stream' or 'allatonce' or 'file' or 'none')
                Control terminal output: `stream` - displays to terminal immediately
                (default), `allatonce` - waits till command is finished to display
                output, `file` - writes output to file, `none` - output is ignored
        test_eq: (a boolean or a float)
                Test for integer vol1 == vol2 or vol1 == constant.
                flag: -eq
        test_ge: (a boolean or a float)
                Test for vol1 >= vol2 or vol1 >= const.
                flag: -ge
        test_gt: (a boolean or a float)
                Test for vol1 > vol2 or vol1 > constant.
                flag: -gt
        test_le: (a boolean or a float)
                Test for vol1 <= vol2 or vol1 <= const.
                flag: -le
        test_lt: (a boolean or a float)
                Test for vol1 < vol2 or vol1 < constant.
                flag: -lt
        test_ne: (a boolean or a float)
                Test for integer vol1 != vol2 or vol1 != const.
                flag: -ne
        two: (a boolean)
                Create a MINC 2 output file.
                flag: -2
        voxel_range: (a tuple of the form: (an integer (int or long), an
                 integer (int or long)))
                Valid range for output data.
                flag: -range %d %d

Outputs::

        output_file: (an existing file name)
                output file

.. _nipype.interfaces.minc.minc.NlpFit:


.. index:: NlpFit

NlpFit
------

`Link to code <http://github.com/nipy/nipype/tree/ec86b7476/nipype/interfaces/minc/minc.py#L3183>`__

Wraps command **nlpfit**

Hierarchial non-linear fitting with bluring.

This tool is part of the minc-widgets package:

https://github.com/BIC-MNI/minc-widgets/blob/master/nlpfit/nlpfit

Examples
~~~~~~~~

>>> from nipype.interfaces.minc import NlpFit
>>> from nipype.interfaces.minc.testdata import nonempty_minc_data, nlp_config
>>> from nipype.testing import example_data

>>> source = nonempty_minc_data(0)
>>> target = nonempty_minc_data(1)
>>> source_mask = nonempty_minc_data(2)
>>> config = nlp_config
>>> initial = example_data('minc_initial.xfm')
>>> nlpfit = NlpFit(config_file=config, init_xfm=initial, source_mask=source_mask, source=source, target=target)
>>> nlpfit.run() # doctest: +SKIP

Inputs::

        [Mandatory]
        config_file: (an existing file name)
                File containing the fitting configuration use.
                flag: -config_file %s
        init_xfm: (an existing file name)
                Initial transformation (default identity).
                flag: -init_xfm %s
        source: (an existing file name)
                source Minc file
                flag: %s, position: -3
        source_mask: (an existing file name)
                Source mask to use during fitting.
                flag: -source_mask %s
        target: (an existing file name)
                target Minc file
                flag: %s, position: -2

        [Optional]
        args: (a unicode string)
                Additional parameters to the command
                flag: %s
        clobber: (a boolean, nipype default value: True)
                Overwrite existing file.
                flag: -clobber
        environ: (a dictionary with keys which are a bytes or None or a value
                 of class 'str' and with values which are a bytes or None or a value
                 of class 'str', nipype default value: {})
                Environment variables
        ignore_exception: (a boolean, nipype default value: False)
                Print an error message instead of throwing an exception in case the
                interface fails to run
        input_grid_files: (a list of items which are a file name)
                input grid file(s)
        output_xfm: (a file name)
                output xfm file
                flag: %s, position: -1
        terminal_output: ('stream' or 'allatonce' or 'file' or 'none')
                Control terminal output: `stream` - displays to terminal immediately
                (default), `allatonce` - waits till command is finished to display
                output, `file` - writes output to file, `none` - output is ignored
        verbose: (a boolean)
                Print out log messages. Default: False.
                flag: -verbose

Outputs::

        output_grid: (an existing file name)
                output grid file
        output_xfm: (an existing file name)
                output xfm file

.. _nipype.interfaces.minc.minc.Norm:


.. index:: Norm

Norm
----

`Link to code <http://github.com/nipy/nipype/tree/ec86b7476/nipype/interfaces/minc/minc.py#L2637>`__

Wraps command **mincnorm**

Normalise a file between a max and minimum (possibly)
   using two histogram pct's.

Examples
~~~~~~~~

>>> from nipype.interfaces.minc import Norm
>>> from nipype.interfaces.minc.testdata import minc2Dfile
>>> n = Norm(input_file=minc2Dfile, output_file='/tmp/out.mnc') # Normalise the file.
>>> n.run() # doctest: +SKIP

Inputs::

        [Mandatory]
        input_file: (an existing file name)
                input file to normalise
                flag: %s, position: -2

        [Optional]
        args: (a unicode string)
                Additional parameters to the command
                flag: %s
        clamp: (a boolean, nipype default value: True)
                Force the ouput range between limits [default].
                flag: -clamp
        clobber: (a boolean, nipype default value: True)
                Overwrite existing file.
                flag: -clobber
        cutoff: (0.0 <= a floating point number <= 100.0)
                Cutoff value to use to calculate thresholds by a histogram PcT in %.
                [default: 0.01]
                flag: -cutoff %s
        environ: (a dictionary with keys which are a bytes or None or a value
                 of class 'str' and with values which are a bytes or None or a value
                 of class 'str', nipype default value: {})
                Environment variables
        ignore_exception: (a boolean, nipype default value: False)
                Print an error message instead of throwing an exception in case the
                interface fails to run
        lower: (a float)
                Lower real value to use.
                flag: -lower %s
        mask: (a file name)
                Calculate the image normalisation within a mask.
                flag: -mask %s
        out_ceil: (a float)
                Output files minimum [default: 100]
                flag: -out_ceil %s
        out_floor: (a float)
                Output files maximum [default: 0]
                flag: -out_floor %s
        output_file: (a file name)
                output file
                flag: %s, position: -1
        output_threshold_mask: (a file name)
                File in which to store the threshold mask.
                flag: -threshold_mask %s
        terminal_output: ('stream' or 'allatonce' or 'file' or 'none')
                Control terminal output: `stream` - displays to terminal immediately
                (default), `allatonce` - waits till command is finished to display
                output, `file` - writes output to file, `none` - output is ignored
        threshold: (a boolean)
                Threshold the image (set values below threshold_perc to -out_floor).
                flag: -threshold
        threshold_blur: (a float)
                Blur FWHM for intensity edges then thresholding [default: 2].
                flag: -threshold_blur %s
        threshold_bmt: (a boolean)
                Use the resulting image BiModalT as the threshold.
                flag: -threshold_bmt
        threshold_perc: (0.0 <= a floating point number <= 100.0)
                Threshold percentage (0.1 == lower 10% of intensity range) [default:
                0.1].
                flag: -threshold_perc %s
        upper: (a float)
                Upper real value to use.
                flag: -upper %s

Outputs::

        output_file: (an existing file name)
                output file
        output_threshold_mask: (a file name)
                threshold mask file

.. _nipype.interfaces.minc.minc.Pik:


.. index:: Pik

Pik
---

`Link to code <http://github.com/nipy/nipype/tree/ec86b7476/nipype/interfaces/minc/minc.py#L1510>`__

Wraps command **mincpik**

Generate images from minc files.

Mincpik uses Imagemagick to generate images
from Minc files.

Examples
~~~~~~~~

>>> from nipype.interfaces.minc import Pik
>>> from nipype.interfaces.minc.testdata import nonempty_minc_data

>>> file0 = nonempty_minc_data(0)
>>> pik = Pik(input_file=file0, title='foo')
>>> pik .run() # doctest: +SKIP

Inputs::

        [Mandatory]
        input_file: (an existing file name)
                input file
                flag: %s, position: -2

        [Optional]
        annotated_bar: (a boolean)
                create an annotated bar to match the image (use height of the output
                image)
                flag: --anot_bar
        args: (a unicode string)
                Additional parameters to the command
                flag: %s
        auto_range: (a boolean)
                Automatically determine image range using a 5 and 95% PcT.
                (histogram)
                flag: --auto_range
                mutually_exclusive: image_range, auto_range
        clobber: (a boolean, nipype default value: True)
                Overwrite existing file.
                flag: -clobber
        depth: (8 or 16)
                Bitdepth for resulting image 8 or 16 (MSB machines only!)
                flag: --depth %s
        environ: (a dictionary with keys which are a bytes or None or a value
                 of class 'str' and with values which are a bytes or None or a value
                 of class 'str', nipype default value: {})
                Environment variables
        horizontal_triplanar_view: (a boolean)
                Create a horizontal triplanar view.
                flag: --horizontal
                mutually_exclusive: vertical_triplanar_view,
                 horizontal_triplanar_view
        ignore_exception: (a boolean, nipype default value: False)
                Print an error message instead of throwing an exception in case the
                interface fails to run
        image_range: (a tuple of the form: (a float, a float))
                Range of image values to use for pixel intensity.
                flag: --image_range %s %s
                mutually_exclusive: image_range, auto_range
        jpg: (a boolean)
                Output a jpg file.
                mutually_exclusive: jpg, png
        lookup: (a unicode string)
                Arguments to pass to minclookup
                flag: --lookup %s
        minc_range: (a tuple of the form: (a float, a float))
                Valid range of values for MINC file.
                flag: --range %s %s
        output_file: (a file name)
                output file
                flag: %s, position: -1
        png: (a boolean)
                Output a png file (default).
                mutually_exclusive: jpg, png
        sagittal_offset: (an integer (int or long))
                Offset the sagittal slice from the centre.
                flag: --sagittal_offset %s
        sagittal_offset_perc: (0 <= a long integer <= 100)
                Offset the sagittal slice by a percentage from the centre.
                flag: --sagittal_offset_perc %d
        scale: (an integer (int or long))
                Scaling factor for resulting image. By default images areoutput at
                twice their original resolution.
                flag: --scale %s
        slice_x: (a boolean)
                Get a sagittal (x) slice.
                flag: -x
                mutually_exclusive: slice_z, slice_y, slice_x
        slice_y: (a boolean)
                Get a coronal (y) slice.
                flag: -y
                mutually_exclusive: slice_z, slice_y, slice_x
        slice_z: (a boolean)
                Get an axial/transverse (z) slice.
                flag: -z
                mutually_exclusive: slice_z, slice_y, slice_x
        start: (an integer (int or long))
                Slice number to get. (note this is in voxel co-ordinates).
                flag: --slice %s
        terminal_output: ('stream' or 'allatonce' or 'file' or 'none')
                Control terminal output: `stream` - displays to terminal immediately
                (default), `allatonce` - waits till command is finished to display
                output, `file` - writes output to file, `none` - output is ignored
        tile_size: (an integer (int or long))
                Pixel size for each image in a triplanar.
                flag: --tilesize %s
        title: (a boolean or a unicode string)
                flag: %s
        title_size: (an integer (int or long))
                Font point size for the title.
                flag: --title_size %s
                requires: title
        triplanar: (a boolean)
                Create a triplanar view of the input file.
                flag: --triplanar
        vertical_triplanar_view: (a boolean)
                Create a vertical triplanar view (Default).
                flag: --vertical
                mutually_exclusive: vertical_triplanar_view,
                 horizontal_triplanar_view
        width: (an integer (int or long))
                Autoscale the resulting image to have a fixed image width (in
                pixels).
                flag: --width %s

Outputs::

        output_file: (an existing file name)
                output image

.. _nipype.interfaces.minc.minc.Resample:


.. index:: Resample

Resample
--------

`Link to code <http://github.com/nipy/nipype/tree/ec86b7476/nipype/interfaces/minc/minc.py#L2522>`__

Wraps command **mincresample**

Resample a minc file.'

Examples
~~~~~~~~

>>> from nipype.interfaces.minc import Resample
>>> from nipype.interfaces.minc.testdata import minc2Dfile
>>> r = Resample(input_file=minc2Dfile, output_file='/tmp/out.mnc') # Resample the file.
>>> r.run() # doctest: +SKIP

Inputs::

        [Mandatory]
        input_file: (an existing file name)
                input file for resampling
                flag: %s, position: -2

        [Optional]
        args: (a unicode string)
                Additional parameters to the command
                flag: %s
        clobber: (a boolean, nipype default value: True)
                Overwrite existing file.
                flag: -clobber
        coronal_slices: (a boolean)
                Write out coronal slices
                flag: -coronal
                mutually_exclusive: transverse, sagittal, coronal
        dircos: (a tuple of the form: (a float, a float, a float))
                Direction cosines along each dimension (X, Y, Z). Default
                value:1.79769e+308 1.79769e+308 1.79769e+308 1.79769e+308 ...
                1.79769e+308 1.79769e+308 1.79769e+308 1.79769e+308 1.79769e+308.
                flag: -dircos %s %s %s
                mutually_exclusive: nelements, nelements_x_y_or_z
        environ: (a dictionary with keys which are a bytes or None or a value
                 of class 'str' and with values which are a bytes or None or a value
                 of class 'str', nipype default value: {})
                Environment variables
        fill: (a boolean)
                Use a fill value for points outside of input volume.
                flag: -fill
                mutually_exclusive: nofill, fill
        fill_value: (a float)
                Specify a fill value for points outside of input volume.Default
                value: 1.79769e+308.
                flag: -fillvalue %s
                requires: fill
        format_byte: (a boolean)
                Write out byte data.
                flag: -byte
                mutually_exclusive: format_byte, format_short, format_int,
                 format_long, format_float, format_double, format_signed,
                 format_unsigned
        format_double: (a boolean)
                Write out double-precision floating-point data.
                flag: -double
                mutually_exclusive: format_byte, format_short, format_int,
                 format_long, format_float, format_double, format_signed,
                 format_unsigned
        format_float: (a boolean)
                Write out single-precision floating-point data.
                flag: -float
                mutually_exclusive: format_byte, format_short, format_int,
                 format_long, format_float, format_double, format_signed,
                 format_unsigned
        format_int: (a boolean)
                Write out 32-bit integer data.
                flag: -int
                mutually_exclusive: format_byte, format_short, format_int,
                 format_long, format_float, format_double, format_signed,
                 format_unsigned
        format_long: (a boolean)
                Superseded by -int.
                flag: -long
                mutually_exclusive: format_byte, format_short, format_int,
                 format_long, format_float, format_double, format_signed,
                 format_unsigned
        format_short: (a boolean)
                Write out short integer data.
                flag: -short
                mutually_exclusive: format_byte, format_short, format_int,
                 format_long, format_float, format_double, format_signed,
                 format_unsigned
        format_signed: (a boolean)
                Write signed integer data.
                flag: -signed
                mutually_exclusive: format_byte, format_short, format_int,
                 format_long, format_float, format_double, format_signed,
                 format_unsigned
        format_unsigned: (a boolean)
                Write unsigned integer data (default).
                flag: -unsigned
                mutually_exclusive: format_byte, format_short, format_int,
                 format_long, format_float, format_double, format_signed,
                 format_unsigned
        half_width_sinc_window: (5 or 1 or 2 or 3 or 4 or 6 or 7 or 8 or 9 or
                 10)
                Set half-width of sinc window (1-10). Default value: 5.
                flag: -width %s
                requires: sinc_interpolation
        ignore_exception: (a boolean, nipype default value: False)
                Print an error message instead of throwing an exception in case the
                interface fails to run
        input_grid_files: (a list of items which are a file name)
                input grid file(s)
        invert_transformation: (a boolean)
                Invert the transformation before using it.
                flag: -invert_transformation
        keep_real_range: (a boolean)
                Keep the real scale of the input volume.
                flag: -keep_real_range
                mutually_exclusive: keep_real_range, nokeep_real_range
        like: (a file name)
                Specifies a model file for the resampling.
                flag: -like %s
        nearest_neighbour_interpolation: (a boolean)
                Do nearest neighbour interpolation.
                flag: -nearest_neighbour
                mutually_exclusive: trilinear_interpolation, tricubic_interpolation,
                 nearest_neighbour_interpolation, sinc_interpolation
        nelements: (a tuple of the form: (an integer (int or long), an
                 integer (int or long), an integer (int or long)))
                Number of elements along each dimension (X, Y, Z).
                flag: -nelements %s %s %s
                mutually_exclusive: nelements, nelements_x_y_or_z
        no_fill: (a boolean)
                Use value zero for points outside of input volume.
                flag: -nofill
                mutually_exclusive: nofill, fill
        no_input_sampling: (a boolean)
                Use the input sampling without transforming (old behaviour).
                flag: -use_input_sampling
                mutually_exclusive: vio_transform, no_input_sampling
        nokeep_real_range: (a boolean)
                Do not keep the real scale of the data (default).
                flag: -nokeep_real_range
                mutually_exclusive: keep_real_range, nokeep_real_range
        origin: (a tuple of the form: (a float, a float, a float))
                Origin of first pixel in 3D space.Default value: 1.79769e+308
                1.79769e+308 1.79769e+308.
                flag: -origin %s %s %s
        output_file: (a file name)
                output file
                flag: %s, position: -1
        output_range: (a tuple of the form: (a float, a float))
                Valid range for output data. Default value: -1.79769e+308
                -1.79769e+308.
                flag: -range %s %s
        sagittal_slices: (a boolean)
                Write out sagittal slices
                flag: -sagittal
                mutually_exclusive: transverse, sagittal, coronal
        sinc_interpolation: (a boolean)
                Do windowed sinc interpolation.
                flag: -sinc
                mutually_exclusive: trilinear_interpolation, tricubic_interpolation,
                 nearest_neighbour_interpolation, sinc_interpolation
        sinc_window_hamming: (a boolean)
                Set sinc window type to Hamming.
                flag: -hamming
                mutually_exclusive: sinc_window_hanning, sinc_window_hamming
                requires: sinc_interpolation
        sinc_window_hanning: (a boolean)
                Set sinc window type to Hanning.
                flag: -hanning
                mutually_exclusive: sinc_window_hanning, sinc_window_hamming
                requires: sinc_interpolation
        spacetype: (a unicode string)
                Set the spacetype attribute to a specified string.
                flag: -spacetype %s
        standard_sampling: (a boolean)
                Set the sampling to standard values (step, start and dircos).
                flag: -standard_sampling
        start: (a tuple of the form: (a float, a float, a float))
                Start point along each dimension (X, Y, Z).Default value:
                1.79769e+308 1.79769e+308 1.79769e+308.
                flag: -start %s %s %s
                mutually_exclusive: nelements, nelements_x_y_or_z
        step: (a tuple of the form: (an integer (int or long), an integer
                 (int or long), an integer (int or long)))
                Step size along each dimension (X, Y, Z). Default value: (0, 0, 0).
                flag: -step %s %s %s
                mutually_exclusive: nelements, nelements_x_y_or_z
        talairach: (a boolean)
                Output is in Talairach space.
                flag: -talairach
        terminal_output: ('stream' or 'allatonce' or 'file' or 'none')
                Control terminal output: `stream` - displays to terminal immediately
                (default), `allatonce` - waits till command is finished to display
                output, `file` - writes output to file, `none` - output is ignored
        transformation: (a file name)
                File giving world transformation. (Default = identity).
                flag: -transformation %s
        transverse_slices: (a boolean)
                Write out transverse slices.
                flag: -transverse
                mutually_exclusive: transverse, sagittal, coronal
        tricubic_interpolation: (a boolean)
                Do tricubic interpolation.
                flag: -tricubic
                mutually_exclusive: trilinear_interpolation, tricubic_interpolation,
                 nearest_neighbour_interpolation, sinc_interpolation
        trilinear_interpolation: (a boolean)
                Do trilinear interpolation.
                flag: -trilinear
                mutually_exclusive: trilinear_interpolation, tricubic_interpolation,
                 nearest_neighbour_interpolation, sinc_interpolation
        two: (a boolean)
                Create a MINC 2 output file.
                flag: -2
        units: (a unicode string)
                Specify the units of the output sampling.
                flag: -units %s
        vio_transform: (a boolean)
                VIO_Transform the input sampling with the transform (default).
                flag: -tfm_input_sampling
                mutually_exclusive: vio_transform, no_input_sampling
        xdircos: (a float)
                Direction cosines along the X dimension.Default value: 1.79769e+308
                1.79769e+308 1.79769e+308.
                flag: -xdircos %s
                mutually_exclusive: dircos, dircos_x_y_or_z
                requires: ydircos, zdircos
        xnelements: (an integer (int or long))
                Number of elements along the X dimension.
                flag: -xnelements %s
                mutually_exclusive: nelements, nelements_x_y_or_z
                requires: ynelements, znelements
        xstart: (a float)
                Start point along the X dimension. Default value: 1.79769e+308.
                flag: -xstart %s
                mutually_exclusive: start, start_x_y_or_z
                requires: ystart, zstart
        xstep: (an integer (int or long))
                Step size along the X dimension. Default value: 0.
                flag: -xstep %s
                mutually_exclusive: step, step_x_y_or_z
                requires: ystep, zstep
        ydircos: (a float)
                Direction cosines along the Y dimension.Default value: 1.79769e+308
                1.79769e+308 1.79769e+308.
                flag: -ydircos %s
                mutually_exclusive: dircos, dircos_x_y_or_z
                requires: xdircos, zdircos
        ynelements: (an integer (int or long))
                Number of elements along the Y dimension.
                flag: -ynelements %s
                mutually_exclusive: nelements, nelements_x_y_or_z
                requires: xnelements, znelements
        ystart: (a float)
                Start point along the Y dimension. Default value: 1.79769e+308.
                flag: -ystart %s
                mutually_exclusive: start, start_x_y_or_z
                requires: xstart, zstart
        ystep: (an integer (int or long))
                Step size along the Y dimension. Default value: 0.
                flag: -ystep %s
                mutually_exclusive: step, step_x_y_or_z
                requires: xstep, zstep
        zdircos: (a float)
                Direction cosines along the Z dimension.Default value: 1.79769e+308
                1.79769e+308 1.79769e+308.
                flag: -zdircos %s
                mutually_exclusive: dircos, dircos_x_y_or_z
                requires: xdircos, ydircos
        znelements: (an integer (int or long))
                Number of elements along the Z dimension.
                flag: -znelements %s
                mutually_exclusive: nelements, nelements_x_y_or_z
                requires: xnelements, ynelements
        zstart: (a float)
                Start point along the Z dimension. Default value: 1.79769e+308.
                flag: -zstart %s
                mutually_exclusive: start, start_x_y_or_z
                requires: xstart, ystart
        zstep: (an integer (int or long))
                Step size along the Z dimension. Default value: 0.
                flag: -zstep %s
                mutually_exclusive: step, step_x_y_or_z
                requires: xstep, ystep

Outputs::

        output_file: (an existing file name)
                output file

.. _nipype.interfaces.minc.minc.Reshape:


.. index:: Reshape

Reshape
-------

`Link to code <http://github.com/nipy/nipype/tree/ec86b7476/nipype/interfaces/minc/minc.py#L3542>`__

Wraps command **mincreshape**

Cut a hyperslab out of a minc file, with dimension reordering.

This is also useful for rewriting with a different format, for
example converting to short (see example below).

Examples
~~~~~~~~

>>> from nipype.interfaces.minc import Reshape
>>> from nipype.interfaces.minc.testdata import nonempty_minc_data

>>> input_file = nonempty_minc_data(0)
>>> reshape_to_short = Reshape(input_file=input_file, write_short=True)
>>> reshape_to_short.run() # doctest: +SKIP

Inputs::

        [Mandatory]
        input_file: (a file name)
                input file
                flag: %s, position: -2

        [Optional]
        args: (a unicode string)
                Additional parameters to the command
                flag: %s
        clobber: (a boolean, nipype default value: True)
                Overwrite existing file.
                flag: -clobber
        environ: (a dictionary with keys which are a bytes or None or a value
                 of class 'str' and with values which are a bytes or None or a value
                 of class 'str', nipype default value: {})
                Environment variables
        ignore_exception: (a boolean, nipype default value: False)
                Print an error message instead of throwing an exception in case the
                interface fails to run
        output_file: (a file name)
                output file
                flag: %s, position: -1
        terminal_output: ('stream' or 'allatonce' or 'file' or 'none')
                Control terminal output: `stream` - displays to terminal immediately
                (default), `allatonce` - waits till command is finished to display
                output, `file` - writes output to file, `none` - output is ignored
        verbose: (a boolean)
                Print out log messages. Default: False.
                flag: -verbose
        write_short: (a boolean)
                Convert to short integer data.
                flag: -short

Outputs::

        output_file: (an existing file name)
                output file

.. _nipype.interfaces.minc.minc.ToEcat:


.. index:: ToEcat

ToEcat
------

`Link to code <http://github.com/nipy/nipype/tree/ec86b7476/nipype/interfaces/minc/minc.py#L526>`__

Wraps command **minctoecat**

Convert a 2D image, a 3D volumes or a 4D dynamic volumes
written in MINC file format to a 2D, 3D or 4D Ecat7 file.

Examples
~~~~~~~~

>>> from nipype.interfaces.minc import ToEcat
>>> from nipype.interfaces.minc.testdata import minc2Dfile

>>> c = ToEcat(input_file=minc2Dfile)
>>> c.run() # doctest: +SKIP

>>> c = ToEcat(input_file=minc2Dfile, voxels_as_integers=True)
>>> c.run() # doctest: +SKIP

Inputs::

        [Mandatory]
        input_file: (an existing file name)
                input file to convert
                flag: %s, position: -2

        [Optional]
        args: (a unicode string)
                Additional parameters to the command
                flag: %s
        environ: (a dictionary with keys which are a bytes or None or a value
                 of class 'str' and with values which are a bytes or None or a value
                 of class 'str', nipype default value: {})
                Environment variables
        ignore_acquisition_variable: (a boolean)
                Ignore informations from the minc acquisition variable.
                flag: -ignore_acquisition_variable
        ignore_ecat_acquisition_variable: (a boolean)
                Ignore informations from the minc ecat_acquisition variable.
                flag: -ignore_ecat_acquisition_variable
        ignore_ecat_main: (a boolean)
                Ignore informations from the minc ecat-main variable.
                flag: -ignore_ecat_main
        ignore_ecat_subheader_variable: (a boolean)
                Ignore informations from the minc ecat-subhdr variable.
                flag: -ignore_ecat_subheader_variable
        ignore_exception: (a boolean, nipype default value: False)
                Print an error message instead of throwing an exception in case the
                interface fails to run
        ignore_patient_variable: (a boolean)
                Ignore informations from the minc patient variable.
                flag: -ignore_patient_variable
        ignore_study_variable: (a boolean)
                Ignore informations from the minc study variable.
                flag: -ignore_study_variable
        no_decay_corr_fctr: (a boolean)
                Do not compute the decay correction factors
                flag: -no_decay_corr_fctr
        output_file: (a file name)
                output file
                flag: %s, position: -1
        terminal_output: ('stream' or 'allatonce' or 'file' or 'none')
                Control terminal output: `stream` - displays to terminal immediately
                (default), `allatonce` - waits till command is finished to display
                output, `file` - writes output to file, `none` - output is ignored
        voxels_as_integers: (a boolean)
                Voxel values are treated as integers, scale andcalibration factors
                are set to unity
                flag: -label

Outputs::

        output_file: (an existing file name)
                output file

.. _nipype.interfaces.minc.minc.ToRaw:


.. index:: ToRaw

ToRaw
-----

`Link to code <http://github.com/nipy/nipype/tree/ec86b7476/nipype/interfaces/minc/minc.py#L322>`__

Wraps command **minctoraw**

Dump a chunk of MINC file data. This program is largely
superceded by mincextract (see Extract).

Examples
~~~~~~~~

>>> from nipype.interfaces.minc import ToRaw
>>> from nipype.interfaces.minc.testdata import minc2Dfile

>>> toraw = ToRaw(input_file=minc2Dfile)
>>> toraw.run() # doctest: +SKIP

>>> toraw = ToRaw(input_file=minc2Dfile, write_range=(0, 100))
>>> toraw.run() # doctest: +SKIP

Inputs::

        [Mandatory]
        input_file: (an existing file name)
                input file
                flag: %s, position: -2

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
        nonormalize: (a boolean)
                Turn off pixel normalization.
                flag: -nonormalize
                mutually_exclusive: normalize, nonormalize
        normalize: (a boolean)
                Normalize integer pixel values to file max and min.
                flag: -normalize
                mutually_exclusive: normalize, nonormalize
        out_file: (a file name)
                flag: > %s, position: -1
        output_file: (a file name)
                output file
        terminal_output: ('stream' or 'allatonce' or 'file' or 'none')
                Control terminal output: `stream` - displays to terminal immediately
                (default), `allatonce` - waits till command is finished to display
                output, `file` - writes output to file, `none` - output is ignored
        write_byte: (a boolean)
                Write out data as bytes.
                flag: -byte
                mutually_exclusive: write_byte, write_short, write_int, write_long,
                 write_float, write_double
        write_double: (a boolean)
                Write out data as double precision floating-point values.
                flag: -double
                mutually_exclusive: write_byte, write_short, write_int, write_long,
                 write_float, write_double
        write_float: (a boolean)
                Write out data as single precision floating-point values.
                flag: -float
                mutually_exclusive: write_byte, write_short, write_int, write_long,
                 write_float, write_double
        write_int: (a boolean)
                Write out data as 32-bit integers.
                flag: -int
                mutually_exclusive: write_byte, write_short, write_int, write_long,
                 write_float, write_double
        write_long: (a boolean)
                Superseded by write_int.
                flag: -long
                mutually_exclusive: write_byte, write_short, write_int, write_long,
                 write_float, write_double
        write_range: (a tuple of the form: (a float, a float))
                Specify the range of output values.Default value: 1.79769e+308
                1.79769e+308.
                flag: -range %s %s
        write_short: (a boolean)
                Write out data as short integers.
                flag: -short
                mutually_exclusive: write_byte, write_short, write_int, write_long,
                 write_float, write_double
        write_signed: (a boolean)
                Write out signed data.
                flag: -signed
                mutually_exclusive: write_signed, write_unsigned
        write_unsigned: (a boolean)
                Write out unsigned data.
                flag: -unsigned
                mutually_exclusive: write_signed, write_unsigned

Outputs::

        output_file: (an existing file name)
                output file in raw format

.. _nipype.interfaces.minc.minc.VolSymm:


.. index:: VolSymm

VolSymm
-------

`Link to code <http://github.com/nipy/nipype/tree/ec86b7476/nipype/interfaces/minc/minc.py#L3636>`__

Wraps command **volsymm**

Make a volume symmetric about an axis either linearly
and/or nonlinearly. This is done by registering a volume
to a flipped image of itself.

This tool is part of the minc-widgets package:

https://github.com/BIC-MNI/minc-widgets/blob/master/volsymm/volsymm

Examples
~~~~~~~~

>>> from nipype.interfaces.minc import VolSymm
>>> from nipype.interfaces.minc.testdata import nonempty_minc_data

>>> input_file = nonempty_minc_data(0)
>>> volsymm = VolSymm(input_file=input_file)
>>> volsymm.run() # doctest: +SKIP

Inputs::

        [Mandatory]
        input_file: (a file name)
                input file
                flag: %s, position: -3

        [Optional]
        args: (a unicode string)
                Additional parameters to the command
                flag: %s
        clobber: (a boolean, nipype default value: True)
                Overwrite existing file.
                flag: -clobber
        config_file: (an existing file name)
                File containing the fitting configuration (nlpfit -help for info).
                flag: -config_file %s
        environ: (a dictionary with keys which are a bytes or None or a value
                 of class 'str' and with values which are a bytes or None or a value
                 of class 'str', nipype default value: {})
                Environment variables
        fit_linear: (a boolean)
                Fit using a linear xfm.
                flag: -linear
        fit_nonlinear: (a boolean)
                Fit using a non-linear xfm.
                flag: -nonlinear
        ignore_exception: (a boolean, nipype default value: False)
                Print an error message instead of throwing an exception in case the
                interface fails to run
        input_grid_files: (a list of items which are a file name)
                input grid file(s)
        nofit: (a boolean)
                Use the input transformation instead of generating one.
                flag: -nofit
        output_file: (a file name)
                output file
                flag: %s, position: -1
        terminal_output: ('stream' or 'allatonce' or 'file' or 'none')
                Control terminal output: `stream` - displays to terminal immediately
                (default), `allatonce` - waits till command is finished to display
                output, `file` - writes output to file, `none` - output is ignored
        trans_file: (a file name)
                output xfm trans file
                flag: %s, position: -2
        verbose: (a boolean)
                Print out log messages. Default: False.
                flag: -verbose
        x: (a boolean)
                Flip volume in x-plane (default).
                flag: -x
        y: (a boolean)
                Flip volume in y-plane.
                flag: -y
        z: (a boolean)
                Flip volume in z-plane.
                flag: -z

Outputs::

        output_file: (an existing file name)
                output file
        output_grid: (an existing file name)
                output grid file
        trans_file: (an existing file name)
                xfm trans file

.. _nipype.interfaces.minc.minc.Volcentre:


.. index:: Volcentre

Volcentre
---------

`Link to code <http://github.com/nipy/nipype/tree/ec86b7476/nipype/interfaces/minc/minc.py#L2735>`__

Wraps command **volcentre**

Centre a MINC image's sampling about a point, typically (0,0,0).

Example
~~~~~~~~

>>> from nipype.interfaces.minc import Volcentre
>>> from nipype.interfaces.minc.testdata import minc2Dfile
>>> vc = Volcentre(input_file=minc2Dfile)
>>> vc.run() # doctest: +SKIP

Inputs::

        [Mandatory]
        input_file: (an existing file name)
                input file to centre
                flag: %s, position: -2

        [Optional]
        args: (a unicode string)
                Additional parameters to the command
                flag: %s
        centre: (a tuple of the form: (a float, a float, a float))
                Centre to use (x,y,z) [default: 0 0 0].
                flag: -centre %s %s %s
        clobber: (a boolean, nipype default value: True)
                Overwrite existing file.
                flag: -clobber
        com: (a boolean)
                Use the CoM of the volume for the new centre (via mincstats).
                Default: False
                flag: -com
        environ: (a dictionary with keys which are a bytes or None or a value
                 of class 'str' and with values which are a bytes or None or a value
                 of class 'str', nipype default value: {})
                Environment variables
        ignore_exception: (a boolean, nipype default value: False)
                Print an error message instead of throwing an exception in case the
                interface fails to run
        output_file: (a file name)
                output file
                flag: %s, position: -1
        terminal_output: ('stream' or 'allatonce' or 'file' or 'none')
                Control terminal output: `stream` - displays to terminal immediately
                (default), `allatonce` - waits till command is finished to display
                output, `file` - writes output to file, `none` - output is ignored
        verbose: (a boolean)
                Print out log messages. Default: False.
                flag: -verbose
        zero_dircos: (a boolean)
                Set the direction cosines to identity [default].
                flag: -zero_dircos

Outputs::

        output_file: (an existing file name)
                output file

.. _nipype.interfaces.minc.minc.Voliso:


.. index:: Voliso

Voliso
------

`Link to code <http://github.com/nipy/nipype/tree/ec86b7476/nipype/interfaces/minc/minc.py#L2887>`__

Wraps command **voliso**

Changes the steps and starts in order that the output volume
has isotropic sampling.

Examples
~~~~~~~~

>>> from nipype.interfaces.minc import Voliso
>>> from nipype.interfaces.minc.testdata import minc2Dfile
>>> viso = Voliso(input_file=minc2Dfile, minstep=0.1, avgstep=True)
>>> viso.run() # doctest: +SKIP

Inputs::

        [Mandatory]
        input_file: (an existing file name)
                input file to convert to isotropic sampling
                flag: %s, position: -2

        [Optional]
        args: (a unicode string)
                Additional parameters to the command
                flag: %s
        avgstep: (a boolean)
                Calculate the maximum step from the average steps of the input
                volume.
                flag: --avgstep
        clobber: (a boolean, nipype default value: True)
                Overwrite existing file.
                flag: --clobber
        environ: (a dictionary with keys which are a bytes or None or a value
                 of class 'str' and with values which are a bytes or None or a value
                 of class 'str', nipype default value: {})
                Environment variables
        ignore_exception: (a boolean, nipype default value: False)
                Print an error message instead of throwing an exception in case the
                interface fails to run
        maxstep: (a float)
                The target maximum step desired in the output volume.
                flag: --maxstep %s
        minstep: (a float)
                The target minimum step desired in the output volume.
                flag: --minstep %s
        output_file: (a file name)
                output file
                flag: %s, position: -1
        terminal_output: ('stream' or 'allatonce' or 'file' or 'none')
                Control terminal output: `stream` - displays to terminal immediately
                (default), `allatonce` - waits till command is finished to display
                output, `file` - writes output to file, `none` - output is ignored
        verbose: (a boolean)
                Print out log messages. Default: False.
                flag: --verbose

Outputs::

        output_file: (an existing file name)
                output file

.. _nipype.interfaces.minc.minc.Volpad:


.. index:: Volpad

Volpad
------

`Link to code <http://github.com/nipy/nipype/tree/ec86b7476/nipype/interfaces/minc/minc.py#L2826>`__

Wraps command **volpad**

Centre a MINC image's sampling about a point, typically (0,0,0).

Examples
~~~~~~~~

>>> from nipype.interfaces.minc import Volpad
>>> from nipype.interfaces.minc.testdata import minc2Dfile
>>> vp = Volpad(input_file=minc2Dfile, smooth=True, smooth_distance=4)
>>> vp.run() # doctest: +SKIP

Inputs::

        [Mandatory]
        input_file: (an existing file name)
                input file to centre
                flag: %s, position: -2

        [Optional]
        args: (a unicode string)
                Additional parameters to the command
                flag: %s
        auto: (a boolean)
                Automatically determine padding distances (uses -distance as max).
                Default: False.
                flag: -auto
        auto_freq: (a float)
                Frequency of voxels over bimodalt threshold to stop at [default:
                500].
                flag: -auto_freq %s
        clobber: (a boolean, nipype default value: True)
                Overwrite existing file.
                flag: -clobber
        distance: (an integer (int or long))
                Padding distance (in voxels) [default: 4].
                flag: -distance %s
        environ: (a dictionary with keys which are a bytes or None or a value
                 of class 'str' and with values which are a bytes or None or a value
                 of class 'str', nipype default value: {})
                Environment variables
        ignore_exception: (a boolean, nipype default value: False)
                Print an error message instead of throwing an exception in case the
                interface fails to run
        output_file: (a file name)
                output file
                flag: %s, position: -1
        smooth: (a boolean)
                Smooth (blur) edges before padding. Default: False.
                flag: -smooth
        smooth_distance: (an integer (int or long))
                Smoothing distance (in voxels) [default: 4].
                flag: -smooth_distance %s
        terminal_output: ('stream' or 'allatonce' or 'file' or 'none')
                Control terminal output: `stream` - displays to terminal immediately
                (default), `allatonce` - waits till command is finished to display
                output, `file` - writes output to file, `none` - output is ignored
        verbose: (a boolean)
                Print out log messages. Default: False.
                flag: -verbose

Outputs::

        output_file: (an existing file name)
                output file

.. _nipype.interfaces.minc.minc.XfmAvg:


.. index:: XfmAvg

XfmAvg
------

`Link to code <http://github.com/nipy/nipype/tree/ec86b7476/nipype/interfaces/minc/minc.py#L3286>`__

Wraps command **xfmavg**

Average a number of xfm transforms using matrix logs and exponents.
The program xfmavg calls Octave for numerical work.

This tool is part of the minc-widgets package:

https://github.com/BIC-MNI/minc-widgets/tree/master/xfmavg

Examples
~~~~~~~~

>>> from nipype.interfaces.minc import XfmAvg
>>> from nipype.interfaces.minc.testdata import nonempty_minc_data, nlp_config
>>> from nipype.testing import example_data

>>> xfm1 = example_data('minc_initial.xfm')
>>> xfm2 = example_data('minc_initial.xfm')  # cheating for doctest
>>> xfmavg = XfmAvg(input_files=[xfm1, xfm2])
>>> xfmavg.run() # doctest: +SKIP

Inputs::

        [Mandatory]
        input_files: (a list of items which are a file name)
                input file(s)
                flag: %s, position: -2

        [Optional]
        args: (a unicode string)
                Additional parameters to the command
                flag: %s
        avg_linear: (a boolean)
                average the linear part [default].
                flag: -avg_linear
        avg_nonlinear: (a boolean)
                average the non-linear part [default].
                flag: -avg_nonlinear
        clobber: (a boolean, nipype default value: True)
                Overwrite existing file.
                flag: -clobber
        environ: (a dictionary with keys which are a bytes or None or a value
                 of class 'str' and with values which are a bytes or None or a value
                 of class 'str', nipype default value: {})
                Environment variables
        ignore_exception: (a boolean, nipype default value: False)
                Print an error message instead of throwing an exception in case the
                interface fails to run
        ignore_linear: (a boolean)
                opposite of -avg_linear.
                flag: -ignore_linear
        ignore_nonlinear: (a boolean)
                opposite of -avg_nonlinear.
                flag: -ignore_nonline
        input_grid_files: (a list of items which are a file name)
                input grid file(s)
        output_file: (a file name)
                output file
                flag: %s, position: -1
        terminal_output: ('stream' or 'allatonce' or 'file' or 'none')
                Control terminal output: `stream` - displays to terminal immediately
                (default), `allatonce` - waits till command is finished to display
                output, `file` - writes output to file, `none` - output is ignored
        verbose: (a boolean)
                Print out log messages. Default: False.
                flag: -verbose

Outputs::

        output_file: (an existing file name)
                output file
        output_grid: (an existing file name)
                output grid file

.. _nipype.interfaces.minc.minc.XfmConcat:


.. index:: XfmConcat

XfmConcat
---------

`Link to code <http://github.com/nipy/nipype/tree/ec86b7476/nipype/interfaces/minc/minc.py#L3008>`__

Wraps command **xfmconcat**

Concatenate transforms together. The output transformation
is equivalent to applying input1.xfm, then input2.xfm, ..., in
that order.

Examples
~~~~~~~~

>>> from nipype.interfaces.minc import XfmConcat
>>> from nipype.interfaces.minc.testdata import minc2Dfile
>>> conc = XfmConcat(input_files=['input1.xfm', 'input1.xfm'])
>>> conc.run() # doctest: +SKIP

Inputs::

        [Mandatory]
        input_files: (a list of items which are a file name)
                input file(s)
                flag: %s, position: -2

        [Optional]
        args: (a unicode string)
                Additional parameters to the command
                flag: %s
        clobber: (a boolean, nipype default value: True)
                Overwrite existing file.
                flag: -clobber
        environ: (a dictionary with keys which are a bytes or None or a value
                 of class 'str' and with values which are a bytes or None or a value
                 of class 'str', nipype default value: {})
                Environment variables
        ignore_exception: (a boolean, nipype default value: False)
                Print an error message instead of throwing an exception in case the
                interface fails to run
        input_grid_files: (a list of items which are a file name)
                input grid file(s)
        output_file: (a file name)
                output file
                flag: %s, position: -1
        terminal_output: ('stream' or 'allatonce' or 'file' or 'none')
                Control terminal output: `stream` - displays to terminal immediately
                (default), `allatonce` - waits till command is finished to display
                output, `file` - writes output to file, `none` - output is ignored
        verbose: (a boolean)
                Print out log messages. Default: False.
                flag: -verbose

Outputs::

        output_file: (an existing file name)
                output file
        output_grids: (a list of items which are an existing file name)
                output grids

.. _nipype.interfaces.minc.minc.XfmInvert:


.. index:: XfmInvert

XfmInvert
---------

`Link to code <http://github.com/nipy/nipype/tree/ec86b7476/nipype/interfaces/minc/minc.py#L3367>`__

Wraps command **xfminvert**

Invert an xfm transform file.

Examples
~~~~~~~~

>>> from nipype.interfaces.minc import XfmAvg
>>> from nipype.testing import example_data

>>> xfm = example_data('minc_initial.xfm')
>>> invert = XfmInvert(input_file=xfm)
>>> invert.run() # doctest: +SKIP

Inputs::

        [Mandatory]
        input_file: (a file name)
                input file
                flag: %s, position: -2

        [Optional]
        args: (a unicode string)
                Additional parameters to the command
                flag: %s
        clobber: (a boolean, nipype default value: True)
                Overwrite existing file.
                flag: -clobber
        environ: (a dictionary with keys which are a bytes or None or a value
                 of class 'str' and with values which are a bytes or None or a value
                 of class 'str', nipype default value: {})
                Environment variables
        ignore_exception: (a boolean, nipype default value: False)
                Print an error message instead of throwing an exception in case the
                interface fails to run
        output_file: (a file name)
                output file
                flag: %s, position: -1
        terminal_output: ('stream' or 'allatonce' or 'file' or 'none')
                Control terminal output: `stream` - displays to terminal immediately
                (default), `allatonce` - waits till command is finished to display
                output, `file` - writes output to file, `none` - output is ignored
        verbose: (a boolean)
                Print out log messages. Default: False.
                flag: -verbose

Outputs::

        output_file: (an existing file name)
                output file
        output_grid: (an existing file name)
                output grid file
