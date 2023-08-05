.. AUTO-GENERATED FILE -- DO NOT EDIT!

interfaces.niftyreg.reg
=======================


.. _nipype.interfaces.niftyreg.reg.RegAladin:


.. index:: RegAladin

RegAladin
---------

`Link to code <http://github.com/nipy/nipype/tree/ec86b7476/nipype/interfaces/niftyreg/reg.py#L141>`__

Wraps command **reg_aladin**

Interface for executable reg_aladin from NiftyReg platform.

Block Matching algorithm for symmetric global registration.
Based on Modat et al., "Global image registration using
asymmetric block-matching approach"
J. Med. Img. 1(2) 024003, 2014, doi: 10.1117/1.JMI.1.2.024003

`Source code <https://cmiclab.cs.ucl.ac.uk/mmodat/niftyreg>`_

Examples
~~~~~~~~
>>> from nipype.interfaces import niftyreg
>>> node = niftyreg.RegAladin()
>>> node.inputs.ref_file = 'im1.nii'
>>> node.inputs.flo_file = 'im2.nii'
>>> node.inputs.rmask_file = 'mask.nii'
>>> node.inputs.omp_core_val = 4
>>> node.cmdline  # doctest: +ALLOW_UNICODE
'reg_aladin -aff im2_aff.txt -flo im2.nii -omp 4 -ref im1.nii -res im2_res.nii.gz -rmask mask.nii'

Inputs::

        [Mandatory]
        flo_file: (an existing file name)
                The input floating/source image
                flag: -flo %s
        ref_file: (an existing file name)
                The input reference/target image
                flag: -ref %s

        [Optional]
        aff_direct_flag: (a boolean)
                Directly optimise the affine parameters
                flag: -affDirect
        aff_file: (a file name)
                The output affine matrix file
                flag: -aff %s
        args: (a unicode string)
                Additional parameters to the command
                flag: %s
        cog_flag: (a boolean)
                Use the masks centre of mass to initialise the transformation
                flag: -cog
        environ: (a dictionary with keys which are a bytes or None or a value
                 of class 'str' and with values which are a bytes or None or a value
                 of class 'str', nipype default value: {})
                Environment variables
        flo_low_val: (a float)
                Lower threshold value on floating image
                flag: -floLowThr %f
        flo_up_val: (a float)
                Upper threshold value on floating image
                flag: -floUpThr %f
        fmask_file: (an existing file name)
                The input floating mask
                flag: -fmask %s
        gpuid_val: (an integer (int or long))
                Device to use id
                flag: -gpuid %i
        i_val: (a long integer >= 0)
                Percent of inlier blocks
                flag: -pi %d
        ignore_exception: (a boolean, nipype default value: False)
                Print an error message instead of throwing an exception in case the
                interface fails to run
        in_aff_file: (an existing file name)
                The input affine transformation
                flag: -inaff %s
        ln_val: (a long integer >= 0)
                Number of resolution levels to create
                flag: -ln %d
        lp_val: (a long integer >= 0)
                Number of resolution levels to perform
                flag: -lp %d
        maxit_val: (a long integer >= 0)
                Maximum number of iterations
                flag: -maxit %d
        nac_flag: (a boolean)
                Use nifti header to initialise transformation
                flag: -nac
        nosym_flag: (a boolean)
                Turn off symmetric registration
                flag: -noSym
        omp_core_val: (an integer (int or long), nipype default value: 4)
                Number of openmp thread to use
                flag: -omp %i
        platform_val: (an integer (int or long))
                Platform index
                flag: -platf %i
        ref_low_val: (a float)
                Lower threshold value on reference image
                flag: -refLowThr %f
        ref_up_val: (a float)
                Upper threshold value on reference image
                flag: -refUpThr %f
        res_file: (a file name)
                The affine transformed floating image
                flag: -res %s
        rig_only_flag: (a boolean)
                Do only a rigid registration
                flag: -rigOnly
        rmask_file: (an existing file name)
                The input reference mask
                flag: -rmask %s
        smoo_f_val: (a float)
                Amount of smoothing to apply to floating image
                flag: -smooF %f
        smoo_r_val: (a float)
                Amount of smoothing to apply to reference image
                flag: -smooR %f
        terminal_output: ('stream' or 'allatonce' or 'file' or 'none')
                Control terminal output: `stream` - displays to terminal immediately
                (default), `allatonce` - waits till command is finished to display
                output, `file` - writes output to file, `none` - output is ignored
        v_val: (a long integer >= 0)
                Percent of blocks that are active
                flag: -pv %d
        verbosity_off_flag: (a boolean)
                Turn off verbose output
                flag: -voff

Outputs::

        aff_file: (a file name)
                The output affine file
        avg_output: (a string)
                Output string in the format for reg_average
        res_file: (a file name)
                The output transformed image

.. _nipype.interfaces.niftyreg.reg.RegF3D:


.. index:: RegF3D

RegF3D
------

`Link to code <http://github.com/nipy/nipype/tree/ec86b7476/nipype/interfaces/niftyreg/reg.py#L353>`__

Wraps command **reg_f3d**

Interface for executable reg_f3d from NiftyReg platform.

Fast Free-Form Deformation (F3D) algorithm for non-rigid registration.
Initially based on Modat et al., "Fast Free-Form Deformation using
graphics processing units", CMPB, 2010

`Source code <https://cmiclab.cs.ucl.ac.uk/mmodat/niftyreg>`_

Examples
~~~~~~~~
>>> from nipype.interfaces import niftyreg
>>> node = niftyreg.RegF3D()
>>> node.inputs.ref_file = 'im1.nii'
>>> node.inputs.flo_file = 'im2.nii'
>>> node.inputs.rmask_file = 'mask.nii'
>>> node.inputs.omp_core_val = 4
>>> node.cmdline  # doctest: +ALLOW_UNICODE
'reg_f3d -cpp im2_cpp.nii.gz -flo im2.nii -omp 4 -ref im1.nii -res im2_res.nii.gz -rmask mask.nii'

Inputs::

        [Mandatory]
        flo_file: (an existing file name)
                The input floating/source image
                flag: -flo %s
        ref_file: (an existing file name)
                The input reference/target image
                flag: -ref %s

        [Optional]
        aff_file: (an existing file name)
                The input affine transformation file
                flag: -aff %s
        amc_flag: (a boolean)
                Use additive NMI
                flag: -amc
        args: (a unicode string)
                Additional parameters to the command
                flag: %s
        be_val: (a float)
                Bending energy value
                flag: -be %f
        cpp_file: (a file name)
                The output CPP file
                flag: -cpp %s
        environ: (a dictionary with keys which are a bytes or None or a value
                 of class 'str' and with values which are a bytes or None or a value
                 of class 'str', nipype default value: {})
                Environment variables
        fbn2_val: (a tuple of the form: (a long integer >= 0, a long integer
                 >= 0))
                Number of bins in the histogram for reference image for given time
                point
                flag: -fbn %d %d
        fbn_val: (a long integer >= 0)
                Number of bins in the histogram for reference image
                flag: --fbn %d
        flo_smooth_val: (a float)
                Smoothing kernel width for floating image
                flag: -smooF %f
        flwth2_thr_val: (a tuple of the form: (a long integer >= 0, a float))
                Lower threshold for floating image at the specified time point
                flag: -fLwTh %d %f
        flwth_thr_val: (a float)
                Lower threshold for floating image
                flag: --fLwTh %f
        fmask_file: (an existing file name)
                Floating image mask
                flag: -fmask %s
        fupth2_thr_val: (a tuple of the form: (a long integer >= 0, a float))
                Upper threshold for floating image at the specified time point
                flag: -fUpTh %d %f
        fupth_thr_val: (a float)
                Upper threshold for floating image
                flag: --fUpTh %f
        ignore_exception: (a boolean, nipype default value: False)
                Print an error message instead of throwing an exception in case the
                interface fails to run
        incpp_file: (an existing file name)
                The input cpp transformation file
                flag: -incpp %s
        jl_val: (a float)
                Log of jacobian of deformation penalty value
                flag: -jl %f
        kld2_flag: (a long integer >= 0)
                Use KL divergence as the similarity measure for a given time point
                flag: -kld %d
        kld_flag: (a boolean)
                Use KL divergence as the similarity measure
                flag: --kld
        le_val: (a float)
                Linear elasticity penalty term
                flag: -le %f
        ln_val: (a long integer >= 0)
                Number of resolution levels to create
                flag: -ln %d
        lncc2_val: (a tuple of the form: (a long integer >= 0, a float))
                SD of the Gaussian for computing LNCC for a given time point
                flag: -lncc %d %f
        lncc_val: (a float)
                SD of the Gaussian for computing LNCC
                flag: --lncc %f
        lp_val: (a long integer >= 0)
                Number of resolution levels to perform
                flag: -lp %d
        maxit_val: (a long integer >= 0)
                Maximum number of iterations per level
                flag: -maxit %d
        nmi_flag: (a boolean)
                use NMI even when other options are specified
                flag: --nmi
        no_app_jl_flag: (a boolean)
                Do not approximate the log of jacobian penalty at control points
                only
                flag: -noAppJL
        noconj_flag: (a boolean)
                Use simple GD optimization
                flag: -noConj
        nopy_flag: (a boolean)
                Do not use the multiresolution approach
                flag: -nopy
        nox_flag: (a boolean)
                Don't optimise in x direction
                flag: -nox
        noy_flag: (a boolean)
                Don't optimise in y direction
                flag: -noy
        noz_flag: (a boolean)
                Don't optimise in z direction
                flag: -noz
        omp_core_val: (an integer (int or long), nipype default value: 4)
                Number of openmp thread to use
                flag: -omp %i
        pad_val: (a float)
                Padding value
                flag: -pad %f
        pert_val: (a long integer >= 0)
                Add perturbation steps after each optimization step
                flag: -pert %d
        rbn2_val: (a tuple of the form: (a long integer >= 0, a long integer
                 >= 0))
                Number of bins in the histogram for reference image for given time
                point
                flag: -rbn %d %d
        rbn_val: (a long integer >= 0)
                Number of bins in the histogram for reference image
                flag: --rbn %d
        ref_smooth_val: (a float)
                Smoothing kernel width for reference image
                flag: -smooR %f
        res_file: (a file name)
                The output resampled image
                flag: -res %s
        rlwth2_thr_val: (a tuple of the form: (a long integer >= 0, a float))
                Lower threshold for reference image at the specified time point
                flag: -rLwTh %d %f
        rlwth_thr_val: (a float)
                Lower threshold for reference image
                flag: --rLwTh %f
        rmask_file: (an existing file name)
                Reference image mask
                flag: -rmask %s
        rupth2_thr_val: (a tuple of the form: (a long integer >= 0, a float))
                Upper threshold for reference image at the specified time point
                flag: -rUpTh %d %f
        rupth_thr_val: (a float)
                Upper threshold for reference image
                flag: --rUpTh %f
        smooth_grad_val: (a float)
                Kernel width for smoothing the metric gradient
                flag: -smoothGrad %f
        ssd2_flag: (a long integer >= 0)
                Use SSD as the similarity measure for a given time point
                flag: -ssd %d
        ssd_flag: (a boolean)
                Use SSD as the similarity measure
                flag: --ssd
        sx_val: (a float)
                Final grid spacing along the x axes
                flag: -sx %f
        sy_val: (a float)
                Final grid spacing along the y axes
                flag: -sy %f
        sz_val: (a float)
                Final grid spacing along the z axes
                flag: -sz %f
        terminal_output: ('stream' or 'allatonce' or 'file' or 'none')
                Control terminal output: `stream` - displays to terminal immediately
                (default), `allatonce` - waits till command is finished to display
                output, `file` - writes output to file, `none` - output is ignored
        vel_flag: (a boolean)
                Use velocity field integration
                flag: -vel
        verbosity_off_flag: (a boolean)
                Turn off verbose output
                flag: -voff

Outputs::

        avg_output: (a string)
                Output string in the format for reg_average
        cpp_file: (a file name)
                The output CPP file
        invcpp_file: (a file name)
                The output inverse CPP file
        invres_file: (a file name)
                The output inverse res file
        res_file: (a file name)
                The output resampled image
