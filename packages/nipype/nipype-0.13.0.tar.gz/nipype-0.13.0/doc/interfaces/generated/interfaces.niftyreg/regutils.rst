.. AUTO-GENERATED FILE -- DO NOT EDIT!

interfaces.niftyreg.regutils
============================


.. _nipype.interfaces.niftyreg.regutils.RegAverage:


.. index:: RegAverage

RegAverage
----------

`Link to code <http://github.com/nipy/nipype/tree/ec86b7476/nipype/interfaces/niftyreg/regutils.py#L379>`__

Wraps command **reg_average**

Interface for executable reg_average from NiftyReg platform.

Compute average matrix or image from a list of matrices or image.
The tool can be use to resample images given input transformation
parametrisation as well as to demean transformations in Euclidean or
log-Euclidean space.

This interface is different than the others in the way that the options
will be written in a command file that is given as a parameter.

`Source code <https://cmiclab.cs.ucl.ac.uk/mmodat/niftyreg>`_

Examples
~~~~~~~~
>>> from nipype.interfaces import niftyreg
>>> node = niftyreg.RegAverage()
>>> one_file = 'im1.nii'
>>> two_file = 'im2.nii'
>>> three_file = 'im3.nii'
>>> node.inputs.avg_files = [one_file, two_file, three_file]
>>> node.cmdline  # doctest: +ELLIPSIS +ALLOW_UNICODE
'reg_average --cmd_file .../reg_average_cmd'

Inputs::

        [Mandatory]

        [Optional]
        args: (a unicode string)
                Additional parameters to the command
                flag: %s
        avg_files: (a list of items which are a file name)
                Averaging of images/affine transformations
                flag: -avg %s, position: 1
                mutually_exclusive: avg_lts_files, avg_ref_file, demean1_ref_file,
                 demean2_ref_file, demean3_ref_file, warp_files
        avg_lts_files: (a list of items which are a file name)
                Robust average of affine transformations
                flag: -avg_lts %s, position: 1
                mutually_exclusive: avg_files, avg_ref_file, demean1_ref_file,
                 demean2_ref_file, demean3_ref_file, warp_files
        avg_ref_file: (a file name)
                All input images are resampled into the space of <reference image>
                and averaged. A cubic spline interpolation scheme is used for
                resampling
                flag: -avg_tran %s, position: 1
                mutually_exclusive: avg_files, avg_lts_files, demean1_ref_file,
                 demean2_ref_file, demean3_ref_file
                requires: warp_files
        demean1_ref_file: (a file name)
                Average images and demean average image that have affine
                transformations to a common space
                flag: -demean1 %s, position: 1
                mutually_exclusive: avg_files, avg_lts_files, avg_ref_file,
                 demean2_ref_file, demean3_ref_file
                requires: warp_files
        demean2_ref_file: (a file name)
                Average images and demean average image that have non-rigid
                transformations to a common space
                flag: -demean2 %s, position: 1
                mutually_exclusive: avg_files, avg_lts_files, avg_ref_file,
                 demean1_ref_file, demean3_ref_file
                requires: warp_files
        demean3_ref_file: (a file name)
                Average images and demean average image that have linear and non-
                rigid transformations to a common space
                flag: -demean3 %s, position: 1
                mutually_exclusive: avg_files, avg_lts_files, avg_ref_file,
                 demean1_ref_file, demean2_ref_file
                requires: warp_files
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
        out_file: (a file name)
                Output file name
                flag: %s, position: 0
        terminal_output: ('stream' or 'allatonce' or 'file' or 'none')
                Control terminal output: `stream` - displays to terminal immediately
                (default), `allatonce` - waits till command is finished to display
                output, `file` - writes output to file, `none` - output is ignored
        warp_files: (a list of items which are a file name)
                transformation files and floating image pairs/triplets to the
                reference space
                flag: %s, position: -1
                mutually_exclusive: avg_files, avg_lts_files

Outputs::

        out_file: (a file name)
                Output file name

.. _nipype.interfaces.niftyreg.regutils.RegJacobian:


.. index:: RegJacobian

RegJacobian
-----------

`Link to code <http://github.com/nipy/nipype/tree/ec86b7476/nipype/interfaces/niftyreg/regutils.py#L161>`__

Wraps command **reg_jacobian**

Interface for executable reg_resample from NiftyReg platform.

Tool to generate Jacobian determinant maps from transformation
parametrisation generated by reg_f3d

`Source code <https://cmiclab.cs.ucl.ac.uk/mmodat/niftyreg>`_

Examples
~~~~~~~~
>>> from nipype.interfaces import niftyreg
>>> node = niftyreg.RegJacobian()
>>> node.inputs.ref_file = 'im1.nii'
>>> node.inputs.trans_file = 'warpfield.nii'
>>> node.inputs.omp_core_val = 4
>>> node.cmdline  # doctest: +ALLOW_UNICODE
'reg_jacobian -omp 4 -ref im1.nii -trans warpfield.nii -jac warpfield_jac.nii.gz'

Inputs::

        [Mandatory]
        trans_file: (an existing file name)
                The input non-rigid transformation
                flag: -trans %s

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
        out_file: (a file name)
                The output jacobian determinant file name
                flag: %s, position: -1
        ref_file: (an existing file name)
                Reference/target file (required if specifying CPP transformations.
                flag: -ref %s
        terminal_output: ('stream' or 'allatonce' or 'file' or 'none')
                Control terminal output: `stream` - displays to terminal immediately
                (default), `allatonce` - waits till command is finished to display
                output, `file` - writes output to file, `none` - output is ignored
        type: ('jac' or 'jacL' or 'jacM', nipype default value: jac)
                Type of jacobian outcome
                flag: -%s, position: -2

Outputs::

        out_file: (a file name)
                The output file

.. _nipype.interfaces.niftyreg.regutils.RegMeasure:


.. index:: RegMeasure

RegMeasure
----------

`Link to code <http://github.com/nipy/nipype/tree/ec86b7476/nipype/interfaces/niftyreg/regutils.py#L692>`__

Wraps command **reg_measure**

Interface for executable reg_measure from NiftyReg platform.

Given two input images, compute the specified measure(s) of similarity

`Source code <https://cmiclab.cs.ucl.ac.uk/mmodat/niftyreg>`_

Examples
~~~~~~~~
>>> from nipype.interfaces import niftyreg
>>> node = niftyreg.RegMeasure()
>>> node.inputs.ref_file = 'im1.nii'
>>> node.inputs.flo_file = 'im2.nii'
>>> node.inputs.measure_type = 'lncc'
>>> node.inputs.omp_core_val = 4
>>> node.cmdline  # doctest: +ALLOW_UNICODE
'reg_measure -flo im2.nii -lncc -omp 4 -out im2_lncc.txt -ref im1.nii'

Inputs::

        [Mandatory]
        flo_file: (an existing file name)
                The input floating/source image
                flag: -flo %s
        measure_type: ('ncc' or 'lncc' or 'nmi' or 'ssd')
                Measure of similarity to compute
                flag: -%s
        ref_file: (an existing file name)
                The input reference/target image
                flag: -ref %s

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
        out_file: (a file name)
                The output text file containing the measure
                flag: -out %s
        terminal_output: ('stream' or 'allatonce' or 'file' or 'none')
                Control terminal output: `stream` - displays to terminal immediately
                (default), `allatonce` - waits till command is finished to display
                output, `file` - writes output to file, `none` - output is ignored

Outputs::

        out_file: (a file name)
                The output text file containing the measure

.. _nipype.interfaces.niftyreg.regutils.RegResample:


.. index:: RegResample

RegResample
-----------

`Link to code <http://github.com/nipy/nipype/tree/ec86b7476/nipype/interfaces/niftyreg/regutils.py#L91>`__

Wraps command **reg_resample**

Interface for executable reg_resample from NiftyReg platform.

Tool to resample floating image in the space of a defined reference image
given a transformation parametrisation generated by reg_aladin, reg_f3d or
reg_transform

`Source code <https://cmiclab.cs.ucl.ac.uk/mmodat/niftyreg>`_

Examples
~~~~~~~~
>>> from nipype.interfaces import niftyreg
>>> node = niftyreg.RegResample()
>>> node.inputs.ref_file = 'im1.nii'
>>> node.inputs.flo_file = 'im2.nii'
>>> node.inputs.trans_file = 'warpfield.nii'
>>> node.inputs.inter_val = 'LIN'
>>> node.inputs.omp_core_val = 4
>>> node.cmdline  # doctest: +ALLOW_UNICODE
'reg_resample -flo im2.nii -inter 1 -omp 4 -ref im1.nii -trans warpfield.nii -res im2_res.nii.gz'

Inputs::

        [Mandatory]
        flo_file: (an existing file name)
                The input floating/source image
                flag: -flo %s
        ref_file: (an existing file name)
                The input reference/target image
                flag: -ref %s

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
        inter_val: ('NN' or 'LIN' or 'CUB' or 'SINC')
                Interpolation type
                flag: -inter %d
        omp_core_val: (an integer (int or long), nipype default value: 4)
                Number of openmp thread to use
                flag: -omp %i
        out_file: (a file name)
                The output filename of the transformed image
                flag: %s, position: -1
        pad_val: (a float)
                Padding value
                flag: -pad %f
        psf_alg: (0 or 1)
                Minimise the matrix metric (0) or the determinant (1) when
                estimating the PSF [0]
                flag: -psf_alg %d
        psf_flag: (a boolean)
                Perform the resampling in two steps to resample an image to a lower
                resolution
                flag: -psf
        tensor_flag: (a boolean)
                Resample Tensor Map
                flag: -tensor
        terminal_output: ('stream' or 'allatonce' or 'file' or 'none')
                Control terminal output: `stream` - displays to terminal immediately
                (default), `allatonce` - waits till command is finished to display
                output, `file` - writes output to file, `none` - output is ignored
        trans_file: (an existing file name)
                The input transformation file
                flag: -trans %s
        type: ('res' or 'blank', nipype default value: res)
                Type of output
                flag: -%s, position: -2
        verbosity_off_flag: (a boolean)
                Turn off verbose output
                flag: -voff

Outputs::

        out_file: (a file name)
                The output filename of the transformed image

.. _nipype.interfaces.niftyreg.regutils.RegTools:


.. index:: RegTools

RegTools
--------

`Link to code <http://github.com/nipy/nipype/tree/ec86b7476/nipype/interfaces/niftyreg/regutils.py#L276>`__

Wraps command **reg_tools**

Interface for executable reg_tools from NiftyReg platform.

Tool delivering various actions related to registration such as
resampling the input image to a chosen resolution or remove the nan and
inf in the input image by a specified value.

`Source code <https://cmiclab.cs.ucl.ac.uk/mmodat/niftyreg>`_

Examples
~~~~~~~~
>>> from nipype.interfaces import niftyreg
>>> node = niftyreg.RegTools()
>>> node.inputs.in_file = 'im1.nii'
>>> node.inputs.mul_val = 4
>>> node.inputs.omp_core_val = 4
>>> node.cmdline  # doctest: +ALLOW_UNICODE
'reg_tools -in im1.nii -mul 4.0 -omp 4 -out im1_tools.nii.gz'

Inputs::

        [Mandatory]
        in_file: (an existing file name)
                The input image file path
                flag: -in %s

        [Optional]
        add_val: (a float or an existing file name)
                Add to the input image or value
                flag: -add %s
        args: (a unicode string)
                Additional parameters to the command
                flag: %s
        bin_flag: (a boolean)
                Binarise the input image
                flag: -bin
        chg_res_val: (a tuple of the form: (a float, a float, a float))
                Change the resolution of the input image
                flag: -chgres %f %f %f
        div_val: (a float or an existing file name)
                Divide the input by image or value
                flag: -div %s
        down_flag: (a boolean)
                Downsample the image by a factor of 2
                flag: -down
        environ: (a dictionary with keys which are a bytes or None or a value
                 of class 'str' and with values which are a bytes or None or a value
                 of class 'str', nipype default value: {})
                Environment variables
        ignore_exception: (a boolean, nipype default value: False)
                Print an error message instead of throwing an exception in case the
                interface fails to run
        iso_flag: (a boolean)
                Make output image isotropic
                flag: -iso
        mask_file: (an existing file name)
                Values outside the mask are set to NaN
                flag: -nan %s
        mul_val: (a float or an existing file name)
                Multiply the input by image or value
                flag: -mul %s
        noscl_flag: (a boolean)
                Set scale, slope to 0 and 1
                flag: -noscl
        omp_core_val: (an integer (int or long), nipype default value: 4)
                Number of openmp thread to use
                flag: -omp %i
        out_file: (a file name)
                The output file name
                flag: -out %s
        rms_val: (an existing file name)
                Compute the mean RMS between the images
                flag: -rms %s
        smo_g_val: (a tuple of the form: (a float, a float, a float))
                Smooth the input image using a Gaussian kernel
                flag: -smoG %f %f %f
        smo_s_val: (a tuple of the form: (a float, a float, a float))
                Smooth the input image using a cubic spline kernel
                flag: -smoS %f %f %f
        sub_val: (a float or an existing file name)
                Add to the input image or value
                flag: -sub %s
        terminal_output: ('stream' or 'allatonce' or 'file' or 'none')
                Control terminal output: `stream` - displays to terminal immediately
                (default), `allatonce` - waits till command is finished to display
                output, `file` - writes output to file, `none` - output is ignored
        thr_val: (a float)
                Binarise the input image with the given threshold
                flag: -thr %f

Outputs::

        out_file: (an existing file name)
                The output file

.. _nipype.interfaces.niftyreg.regutils.RegTransform:


.. index:: RegTransform

RegTransform
------------

`Link to code <http://github.com/nipy/nipype/tree/ec86b7476/nipype/interfaces/niftyreg/regutils.py#L581>`__

Wraps command **reg_transform**

Interface for executable reg_transform from NiftyReg platform.

Tools to convert transformation parametrisation from one type to another
as well as to compose, inverse or half transformations.

`Source code <https://cmiclab.cs.ucl.ac.uk/mmodat/niftyreg>`_

Examples
~~~~~~~~
>>> from nipype.interfaces import niftyreg
>>> node = niftyreg.RegTransform()
>>> node.inputs.def_input = 'warpfield.nii'
>>> node.inputs.omp_core_val = 4
>>> node.cmdline  # doctest: +ELLIPSIS +ALLOW_UNICODE
'reg_transform -omp 4 -def warpfield.nii .../warpfield_trans.nii.gz'

Inputs::

        [Mandatory]

        [Optional]
        aff_2_rig_input: (an existing file name)
                Extract the rigid component from affine transformation
                flag: -aff2rig %s, position: -2
                mutually_exclusive: def_input, disp_input, flow_input, comp_input,
                 upd_s_form_input, inv_aff_input, inv_nrr_input, half_input,
                 make_aff_input, flirt_2_nr_input
        args: (a unicode string)
                Additional parameters to the command
                flag: %s
        comp_input: (an existing file name)
                compose two transformations
                flag: -comp %s, position: -3
                mutually_exclusive: def_input, disp_input, flow_input,
                 upd_s_form_input, inv_aff_input, inv_nrr_input, half_input,
                 make_aff_input, aff_2_rig_input, flirt_2_nr_input
                requires: comp_input2
        comp_input2: (an existing file name)
                compose two transformations
                flag: %s, position: -2
        def_input: (an existing file name)
                Compute deformation field from transformation
                flag: -def %s, position: -2
                mutually_exclusive: disp_input, flow_input, comp_input,
                 upd_s_form_input, inv_aff_input, inv_nrr_input, half_input,
                 make_aff_input, aff_2_rig_input, flirt_2_nr_input
        disp_input: (an existing file name)
                Compute displacement field from transformation
                flag: -disp %s, position: -2
                mutually_exclusive: def_input, flow_input, comp_input,
                 upd_s_form_input, inv_aff_input, inv_nrr_input, half_input,
                 make_aff_input, aff_2_rig_input, flirt_2_nr_input
        environ: (a dictionary with keys which are a bytes or None or a value
                 of class 'str' and with values which are a bytes or None or a value
                 of class 'str', nipype default value: {})
                Environment variables
        flirt_2_nr_input: (a tuple of the form: (an existing file name, an
                 existing file name, an existing file name))
                Convert a FLIRT affine transformation to niftyreg affine
                transformation
                flag: -flirtAff2NR %s %s %s, position: -2
                mutually_exclusive: def_input, disp_input, flow_input, comp_input,
                 upd_s_form_input, inv_aff_input, inv_nrr_input, half_input,
                 make_aff_input, aff_2_rig_input
        flow_input: (an existing file name)
                Compute flow field from spline SVF
                flag: -flow %s, position: -2
                mutually_exclusive: def_input, disp_input, comp_input,
                 upd_s_form_input, inv_aff_input, inv_nrr_input, half_input,
                 make_aff_input, aff_2_rig_input, flirt_2_nr_input
        half_input: (an existing file name)
                Half way to the input transformation
                flag: -half %s, position: -2
                mutually_exclusive: def_input, disp_input, flow_input, comp_input,
                 upd_s_form_input, inv_aff_input, inv_nrr_input, make_aff_input,
                 aff_2_rig_input, flirt_2_nr_input
        ignore_exception: (a boolean, nipype default value: False)
                Print an error message instead of throwing an exception in case the
                interface fails to run
        inv_aff_input: (an existing file name)
                Invert an affine transformation
                flag: -invAff %s, position: -2
                mutually_exclusive: def_input, disp_input, flow_input, comp_input,
                 upd_s_form_input, inv_nrr_input, half_input, make_aff_input,
                 aff_2_rig_input, flirt_2_nr_input
        inv_nrr_input: (a tuple of the form: (an existing file name, an
                 existing file name))
                Invert a non-linear transformation
                flag: -invNrr %s %s, position: -2
                mutually_exclusive: def_input, disp_input, flow_input, comp_input,
                 upd_s_form_input, inv_aff_input, half_input, make_aff_input,
                 aff_2_rig_input, flirt_2_nr_input
        make_aff_input: (a tuple of the form: (a float, a float, a float, a
                 float, a float, a float, a float, a float, a float, a float, a
                 float, a float))
                Make an affine transformation matrix
                flag: -makeAff %f %f %f %f %f %f %f %f %f %f %f %f, position: -2
                mutually_exclusive: def_input, disp_input, flow_input, comp_input,
                 upd_s_form_input, inv_aff_input, inv_nrr_input, half_input,
                 aff_2_rig_input, flirt_2_nr_input
        omp_core_val: (an integer (int or long), nipype default value: 4)
                Number of openmp thread to use
                flag: -omp %i
        out_file: (a file name)
                transformation file to write
                flag: %s, position: -1
        ref1_file: (an existing file name)
                The input reference/target image
                flag: -ref %s, position: 0
        ref2_file: (an existing file name)
                The input second reference/target image
                flag: -ref2 %s, position: 1
                requires: ref1_file
        terminal_output: ('stream' or 'allatonce' or 'file' or 'none')
                Control terminal output: `stream` - displays to terminal immediately
                (default), `allatonce` - waits till command is finished to display
                output, `file` - writes output to file, `none` - output is ignored
        upd_s_form_input: (an existing file name)
                Update s-form using the affine transformation
                flag: -updSform %s, position: -3
                mutually_exclusive: def_input, disp_input, flow_input, comp_input,
                 inv_aff_input, inv_nrr_input, half_input, make_aff_input,
                 aff_2_rig_input, flirt_2_nr_input
                requires: upd_s_form_input2
        upd_s_form_input2: (an existing file name)
                Update s-form using the affine transformation
                flag: %s, position: -2
                requires: upd_s_form_input

Outputs::

        out_file: (a file name)
                Output File (transformation in any format)
