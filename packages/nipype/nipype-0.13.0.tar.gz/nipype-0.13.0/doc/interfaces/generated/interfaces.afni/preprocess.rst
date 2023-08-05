.. AUTO-GENERATED FILE -- DO NOT EDIT!

interfaces.afni.preprocess
==========================


.. _nipype.interfaces.afni.preprocess.Allineate:


.. index:: Allineate

Allineate
---------

`Link to code <http://github.com/nipy/nipype/tree/ec86b7476/nipype/interfaces/afni/preprocess.py#L257>`__

Wraps command **3dAllineate**

Program to align one dataset (the 'source') to a base dataset

For complete details, see the `3dAllineate Documentation.
<https://afni.nimh.nih.gov/pub/dist/doc/program_help/3dAllineate.html>`_

Examples
~~~~~~~~

>>> from nipype.interfaces import afni
>>> allineate = afni.Allineate()
>>> allineate.inputs.in_file = 'functional.nii'
>>> allineate.inputs.out_file = 'functional_allineate.nii'
>>> allineate.inputs.in_matrix = 'cmatrix.mat'
>>> allineate.cmdline  # doctest: +ALLOW_UNICODE
'3dAllineate -1Dmatrix_apply cmatrix.mat -prefix functional_allineate.nii -source functional.nii'
>>> res = allineate.run()  # doctest: +SKIP

Inputs::

        [Mandatory]
        in_file: (an existing file name)
                input file to 3dAllineate
                flag: -source %s, position: -1

        [Optional]
        args: (a unicode string)
                Additional parameters to the command
                flag: %s
        autobox: (a boolean)
                Expand the -automask function to enclose a rectangular box that
                holds the irregular mask.
                flag: -autobox
        automask: (an integer (int or long))
                Compute a mask function, set a value for dilation or 0.
                flag: -automask+%d
        autoweight: (a unicode string)
                Compute a weight function using the 3dAutomask algorithm plus some
                blurring of the base image.
                flag: -autoweight%s
        center_of_mass: (a unicode string)
                Use the center-of-mass calculation to bracket the shifts.
                flag: -cmass%s
        check: (a list of items which are 'leastsq' or 'ls' or 'mutualinfo'
                 or 'mi' or 'corratio_mul' or 'crM' or 'norm_mutualinfo' or 'nmi' or
                 'hellinger' or 'hel' or 'corratio_add' or 'crA' or 'corratio_uns'
                 or 'crU')
                After cost functional optimization is done, start at the final
                parameters and RE-optimize using this new cost functions. If the
                results are too different, a warning message will be printed.
                However, the final parameters from the original optimization will be
                used to create the output dataset.
                flag: -check %s
        convergence: (a float)
                Convergence test in millimeters (default 0.05mm).
                flag: -conv %f
        cost: ('leastsq' or 'ls' or 'mutualinfo' or 'mi' or 'corratio_mul' or
                 'crM' or 'norm_mutualinfo' or 'nmi' or 'hellinger' or 'hel' or
                 'corratio_add' or 'crA' or 'corratio_uns' or 'crU')
                Defines the 'cost' function that defines the matching between the
                source and the base
                flag: -cost %s
        environ: (a dictionary with keys which are a bytes or None or a value
                 of class 'str' and with values which are a bytes or None or a value
                 of class 'str', nipype default value: {})
                Environment variables
        epi: (a boolean)
                Treat the source dataset as being composed of warped EPI slices, and
                the base as comprising anatomically 'true' images. Only phase-
                encoding direction image shearing and scaling will be allowed with
                this option.
                flag: -EPI
        final_interpolation: ('nearestneighbour' or 'linear' or 'cubic' or
                 'quintic' or 'wsinc5')
                Defines interpolation method used to create the output dataset
                flag: -final %s
        fine_blur: (a float)
                Set the blurring radius to use in the fine resolution pass to 'x'
                mm. A small amount (1-2 mm?) of blurring at the fine step may help
                with convergence, if there is some problem, especially if the base
                volume is very noisy. [Default == 0 mm = no blurring at the final
                alignment pass]
                flag: -fineblur %f
        ignore_exception: (a boolean, nipype default value: False)
                Print an error message instead of throwing an exception in case the
                interface fails to run
        in_matrix: (a file name)
                matrix to align input file
                flag: -1Dmatrix_apply %s, position: -3
        in_param_file: (an existing file name)
                Read warp parameters from file and apply them to the source dataset,
                and produce a new dataset
                flag: -1Dparam_apply %s
        interpolation: ('nearestneighbour' or 'linear' or 'cubic' or
                 'quintic')
                Defines interpolation method to use during matching
                flag: -interp %s
        master: (an existing file name)
                Write the output dataset on the same grid as this file.
                flag: -master %s
        newgrid: (a float)
                Write the output dataset using isotropic grid spacing in mm.
                flag: -newgrid %f
        nmatch: (an integer (int or long))
                Use at most n scattered points to match the datasets.
                flag: -nmatch %d
        no_pad: (a boolean)
                Do not use zero-padding on the base image.
                flag: -nopad
        nomask: (a boolean)
                Don't compute the autoweight/mask; if -weight is not also used, then
                every voxel will be counted equally.
                flag: -nomask
        nwarp: ('bilinear' or 'cubic' or 'quintic' or 'heptic' or 'nonic' or
                 'poly3' or 'poly5' or 'poly7' or 'poly9')
                Experimental nonlinear warping: bilinear or legendre poly.
                flag: -nwarp %s
        nwarp_fixdep: (a list of items which are 'X' or 'Y' or 'Z' or 'I' or
                 'J' or 'K')
                To fix non-linear warp dependency along directions.
                flag: -nwarp_fixdep%s
        nwarp_fixmot: (a list of items which are 'X' or 'Y' or 'Z' or 'I' or
                 'J' or 'K')
                To fix motion along directions.
                flag: -nwarp_fixmot%s
        one_pass: (a boolean)
                Use only the refining pass -- do not try a coarse resolution pass
                first. Useful if you know that only small amounts of image alignment
                are needed.
                flag: -onepass
        out_file: (a file name)
                output file from 3dAllineate
                flag: -prefix %s, position: -2
        out_matrix: (a file name)
                Save the transformation matrix for each volume.
                flag: -1Dmatrix_save %s
        out_param_file: (a file name)
                Save the warp parameters in ASCII (.1D) format.
                flag: -1Dparam_save %s
        out_weight_file: (a file name)
                Write the weight volume to disk as a dataset
                flag: -wtprefix %s
        outputtype: ('NIFTI' or 'AFNI' or 'NIFTI_GZ')
                AFNI output filetype
        reference: (an existing file name)
                file to be used as reference, the first volume will be used if not
                given the reference will be the first volume of in_file.
                flag: -base %s
        replacebase: (a boolean)
                If the source has more than one volume, then after the first volume
                is aligned to the base.
                flag: -replacebase
        replacemeth: ('leastsq' or 'ls' or 'mutualinfo' or 'mi' or
                 'corratio_mul' or 'crM' or 'norm_mutualinfo' or 'nmi' or
                 'hellinger' or 'hel' or 'corratio_add' or 'crA' or 'corratio_uns'
                 or 'crU')
                After first volume is aligned, switch method for later volumes. For
                use with '-replacebase'.
                flag: -replacemeth %s
        source_automask: (an integer (int or long))
                Automatically mask the source dataset with dilation or 0.
                flag: -source_automask+%d
        source_mask: (an existing file name)
                mask the input dataset
                flag: -source_mask %s
        terminal_output: ('stream' or 'allatonce' or 'file' or 'none')
                Control terminal output: `stream` - displays to terminal immediately
                (default), `allatonce` - waits till command is finished to display
                output, `file` - writes output to file, `none` - output is ignored
        two_best: (an integer (int or long))
                In the coarse pass, use the best 'bb' set of initialpoints to search
                for the starting point for the finepass. If bb==0, then no search is
                made for the beststarting point, and the identity transformation
                isused as the starting point. [Default=5; min=0 max=11]
                flag: -twobest %d
        two_blur: (a float)
                Set the blurring radius for the first pass in mm.
                flag: -twoblur
        two_first: (a boolean)
                Use -twopass on the first image to be registered, and then on all
                subsequent images from the source dataset, use results from the
                first image's coarse pass to start the fine pass.
                flag: -twofirst
        two_pass: (a boolean)
                Use a two pass alignment strategy for all volumes, searching for a
                large rotation+shift and then refining the alignment.
                flag: -twopass
        usetemp: (a boolean)
                temporary file use
                flag: -usetemp
        warp_type: ('shift_only' or 'shift_rotate' or 'shift_rotate_scale' or
                 'affine_general')
                Set the warp type.
                flag: -warp %s
        warpfreeze: (a boolean)
                Freeze the non-rigid body parameters after first volume.
                flag: -warpfreeze
        weight_file: (an existing file name)
                Set the weighting for each voxel in the base dataset; larger weights
                mean that voxel count more in the cost function. Must be defined on
                the same grid as the base dataset
                flag: -weight %s
        zclip: (a boolean)
                Replace negative values in the input datasets (source & base) with
                zero.
                flag: -zclip

Outputs::

        matrix: (a file name)
                matrix to align input file
        out_file: (a file name)
                output image file name

References::
None
None

.. _nipype.interfaces.afni.preprocess.AutoTcorrelate:


.. index:: AutoTcorrelate

AutoTcorrelate
--------------

`Link to code <http://github.com/nipy/nipype/tree/ec86b7476/nipype/interfaces/afni/preprocess.py#L339>`__

Wraps command **3dAutoTcorrelate**

Computes the correlation coefficient between the time series of each
pair of voxels in the input dataset, and stores the output into a
new anatomical bucket dataset [scaled to shorts to save memory space].

For complete details, see the `3dAutoTcorrelate Documentation.
<https://afni.nimh.nih.gov/pub/dist/doc/program_help/3dAutoTcorrelate.html>`_

Examples
~~~~~~~~

>>> from nipype.interfaces import afni
>>> corr = afni.AutoTcorrelate()
>>> corr.inputs.in_file = 'functional.nii'
>>> corr.inputs.polort = -1
>>> corr.inputs.eta2 = True
>>> corr.inputs.mask = 'mask.nii'
>>> corr.inputs.mask_only_targets = True
>>> corr.cmdline  # doctest: +ELLIPSIS +NORMALIZE_WHITESPACE +ALLOW_UNICODE
'3dAutoTcorrelate -eta2 -mask mask.nii -mask_only_targets -prefix functional_similarity_matrix.1D -polort -1 functional.nii'
>>> res = corr.run()  # doctest: +SKIP

Inputs::

        [Mandatory]
        in_file: (an existing file name)
                timeseries x space (volume or surface) file
                flag: %s, position: -1

        [Optional]
        args: (a unicode string)
                Additional parameters to the command
                flag: %s
        environ: (a dictionary with keys which are a bytes or None or a value
                 of class 'str' and with values which are a bytes or None or a value
                 of class 'str', nipype default value: {})
                Environment variables
        eta2: (a boolean)
                eta^2 similarity
                flag: -eta2
        ignore_exception: (a boolean, nipype default value: False)
                Print an error message instead of throwing an exception in case the
                interface fails to run
        mask: (an existing file name)
                mask of voxels
                flag: -mask %s
        mask_only_targets: (a boolean)
                use mask only on targets voxels
                flag: -mask_only_targets
                mutually_exclusive: mask_source
        mask_source: (an existing file name)
                mask for source voxels
                flag: -mask_source %s
                mutually_exclusive: mask_only_targets
        out_file: (a file name)
                output image file name
                flag: -prefix %s
        outputtype: ('NIFTI' or 'AFNI' or 'NIFTI_GZ')
                AFNI output filetype
        polort: (an integer (int or long))
                Remove polynomical trend of order m or -1 for no detrending
                flag: -polort %d
        terminal_output: ('stream' or 'allatonce' or 'file' or 'none')
                Control terminal output: `stream` - displays to terminal immediately
                (default), `allatonce` - waits till command is finished to display
                output, `file` - writes output to file, `none` - output is ignored

Outputs::

        out_file: (an existing file name)
                output file

References::
None
None

.. _nipype.interfaces.afni.preprocess.Automask:


.. index:: Automask

Automask
--------

`Link to code <http://github.com/nipy/nipype/tree/ec86b7476/nipype/interfaces/afni/preprocess.py#L411>`__

Wraps command **3dAutomask**

Create a brain-only mask of the image using AFNI 3dAutomask command

For complete details, see the `3dAutomask Documentation.
<https://afni.nimh.nih.gov/pub/dist/doc/program_help/3dAutomask.html>`_

Examples
~~~~~~~~

>>> from nipype.interfaces import afni
>>> automask = afni.Automask()
>>> automask.inputs.in_file = 'functional.nii'
>>> automask.inputs.dilate = 1
>>> automask.inputs.outputtype = 'NIFTI'
>>> automask.cmdline  # doctest: +ELLIPSIS +ALLOW_UNICODE
'3dAutomask -apply_prefix functional_masked.nii -dilate 1 -prefix functional_mask.nii functional.nii'
>>> res = automask.run()  # doctest: +SKIP

Inputs::

        [Mandatory]
        in_file: (an existing file name)
                input file to 3dAutomask
                flag: %s, position: -1

        [Optional]
        args: (a unicode string)
                Additional parameters to the command
                flag: %s
        brain_file: (a file name)
                output file from 3dAutomask
                flag: -apply_prefix %s
        clfrac: (a float)
                sets the clip level fraction (must be 0.1-0.9). A small value will
                tend to make the mask larger [default = 0.5].
                flag: -clfrac %s
        dilate: (an integer (int or long))
                dilate the mask outwards
                flag: -dilate %s
        environ: (a dictionary with keys which are a bytes or None or a value
                 of class 'str' and with values which are a bytes or None or a value
                 of class 'str', nipype default value: {})
                Environment variables
        erode: (an integer (int or long))
                erode the mask inwards
                flag: -erode %s
        ignore_exception: (a boolean, nipype default value: False)
                Print an error message instead of throwing an exception in case the
                interface fails to run
        out_file: (a file name)
                output image file name
                flag: -prefix %s
        outputtype: ('NIFTI' or 'AFNI' or 'NIFTI_GZ')
                AFNI output filetype
        terminal_output: ('stream' or 'allatonce' or 'file' or 'none')
                Control terminal output: `stream` - displays to terminal immediately
                (default), `allatonce` - waits till command is finished to display
                output, `file` - writes output to file, `none` - output is ignored

Outputs::

        brain_file: (an existing file name)
                brain file (skull stripped)
        out_file: (an existing file name)
                mask file

References::
None
None

.. _nipype.interfaces.afni.preprocess.Bandpass:


.. index:: Bandpass

Bandpass
--------

`Link to code <http://github.com/nipy/nipype/tree/ec86b7476/nipype/interfaces/afni/preprocess.py#L518>`__

Wraps command **3dBandpass**

Program to lowpass and/or highpass each voxel time series in a
dataset, offering more/different options than Fourier

For complete details, see the `3dBandpass Documentation.
<https://afni.nimh.nih.gov/pub/dist/doc/program_help/3dBandpass.html>`_

Examples
~~~~~~~~

>>> from nipype.interfaces import afni
>>> from nipype.testing import  example_data
>>> bandpass = afni.Bandpass()
>>> bandpass.inputs.in_file = 'functional.nii'
>>> bandpass.inputs.highpass = 0.005
>>> bandpass.inputs.lowpass = 0.1
>>> bandpass.cmdline  # doctest: +ALLOW_UNICODE
'3dBandpass -prefix functional_bp 0.005000 0.100000 functional.nii'
>>> res = bandpass.run()  # doctest: +SKIP

Inputs::

        [Mandatory]
        highpass: (a float)
                highpass
                flag: %f, position: -3
        in_file: (an existing file name)
                input file to 3dBandpass
                flag: %s, position: -1
        lowpass: (a float)
                lowpass
                flag: %f, position: -2

        [Optional]
        args: (a unicode string)
                Additional parameters to the command
                flag: %s
        automask: (a boolean)
                Create a mask from the input dataset.
                flag: -automask
        blur: (a float)
                Blur (inside the mask only) with a filter width (FWHM) of 'fff'
                millimeters.
                flag: -blur %f
        despike: (a boolean)
                Despike each time series before other processing. Hopefully, you
                don't actually need to do this, which is why it is optional.
                flag: -despike
        environ: (a dictionary with keys which are a bytes or None or a value
                 of class 'str' and with values which are a bytes or None or a value
                 of class 'str', nipype default value: {})
                Environment variables
        ignore_exception: (a boolean, nipype default value: False)
                Print an error message instead of throwing an exception in case the
                interface fails to run
        localPV: (a float)
                Replace each vector by the local Principal Vector (AKA first
                singular vector) from a neighborhood of radius 'rrr' millimeters.
                Note that the PV time series is L2 normalized. This option is mostly
                for Bob Cox to have fun with.
                flag: -localPV %f
        mask: (an existing file name)
                mask file
                flag: -mask %s, position: 2
        nfft: (an integer (int or long))
                Set the FFT length [must be a legal value].
                flag: -nfft %d
        no_detrend: (a boolean)
                Skip the quadratic detrending of the input that occurs before the
                FFT-based bandpassing. You would only want to do this if the dataset
                had been detrended already in some other program.
                flag: -nodetrend
        normalize: (a boolean)
                Make all output time series have L2 norm = 1 (i.e., sum of squares =
                1).
                flag: -norm
        notrans: (a boolean)
                Don't check for initial positive transients in the data. The test is
                a little slow, so skipping it is OK, if you KNOW the data time
                series are transient-free.
                flag: -notrans
        orthogonalize_dset: (an existing file name)
                Orthogonalize each voxel to the corresponding voxel time series in
                dataset 'fset', which must have the same spatial and temporal grid
                structure as the main input dataset. At present, only one '-dsort'
                option is allowed.
                flag: -dsort %s
        orthogonalize_file: (a list of items which are an existing file name)
                Also orthogonalize input to columns in f.1D. Multiple '-ort' options
                are allowed.
                flag: -ort %s
        out_file: (a file name)
                output file from 3dBandpass
                flag: -prefix %s, position: 1
        outputtype: ('NIFTI' or 'AFNI' or 'NIFTI_GZ')
                AFNI output filetype
        terminal_output: ('stream' or 'allatonce' or 'file' or 'none')
                Control terminal output: `stream` - displays to terminal immediately
                (default), `allatonce` - waits till command is finished to display
                output, `file` - writes output to file, `none` - output is ignored
        tr: (a float)
                Set time step (TR) in sec [default=from dataset header].
                flag: -dt %f

Outputs::

        out_file: (an existing file name)
                output file

References::
None
None

.. _nipype.interfaces.afni.preprocess.BlurInMask:


.. index:: BlurInMask

BlurInMask
----------

`Link to code <http://github.com/nipy/nipype/tree/ec86b7476/nipype/interfaces/afni/preprocess.py#L588>`__

Wraps command **3dBlurInMask**

Blurs a dataset spatially inside a mask.  That's all.  Experimental.

For complete details, see the `3dBlurInMask Documentation.
<https://afni.nimh.nih.gov/pub/dist/doc/program_help/3dBlurInMask.html>`_

Examples
~~~~~~~~

>>> from nipype.interfaces import afni
>>> bim = afni.BlurInMask()
>>> bim.inputs.in_file = 'functional.nii'
>>> bim.inputs.mask = 'mask.nii'
>>> bim.inputs.fwhm = 5.0
>>> bim.cmdline  # doctest: +ELLIPSIS +ALLOW_UNICODE
'3dBlurInMask -input functional.nii -FWHM 5.000000 -mask mask.nii -prefix functional_blur'
>>> res = bim.run()  # doctest: +SKIP

Inputs::

        [Mandatory]
        fwhm: (a float)
                fwhm kernel size
                flag: -FWHM %f
        in_file: (an existing file name)
                input file to 3dSkullStrip
                flag: -input %s, position: 1

        [Optional]
        args: (a unicode string)
                Additional parameters to the command
                flag: %s
        automask: (a boolean)
                Create an automask from the input dataset.
                flag: -automask
        environ: (a dictionary with keys which are a bytes or None or a value
                 of class 'str' and with values which are a bytes or None or a value
                 of class 'str', nipype default value: {})
                Environment variables
        float_out: (a boolean)
                Save dataset as floats, no matter what the input data type is.
                flag: -float
        ignore_exception: (a boolean, nipype default value: False)
                Print an error message instead of throwing an exception in case the
                interface fails to run
        mask: (a file name)
                Mask dataset, if desired. Blurring will occur only within the mask.
                Voxels NOT in the mask will be set to zero in the output.
                flag: -mask %s
        multimask: (a file name)
                Multi-mask dataset -- each distinct nonzero value in dataset will be
                treated as a separate mask for blurring purposes.
                flag: -Mmask %s
        options: (a unicode string)
                options
                flag: %s, position: 2
        out_file: (a file name)
                output to the file
                flag: -prefix %s, position: -1
        outputtype: ('NIFTI' or 'AFNI' or 'NIFTI_GZ')
                AFNI output filetype
        preserve: (a boolean)
                Normally, voxels not in the mask will be set to zero in the output.
                If you want the original values in the dataset to be preserved in
                the output, use this option.
                flag: -preserve
        terminal_output: ('stream' or 'allatonce' or 'file' or 'none')
                Control terminal output: `stream` - displays to terminal immediately
                (default), `allatonce` - waits till command is finished to display
                output, `file` - writes output to file, `none` - output is ignored

Outputs::

        out_file: (an existing file name)
                output file

References::
None
None

.. _nipype.interfaces.afni.preprocess.BlurToFWHM:


.. index:: BlurToFWHM

BlurToFWHM
----------

`Link to code <http://github.com/nipy/nipype/tree/ec86b7476/nipype/interfaces/afni/preprocess.py#L639>`__

Wraps command **3dBlurToFWHM**

Blurs a 'master' dataset until it reaches a specified FWHM smoothness
(approximately).

For complete details, see the `3dBlurToFWHM Documentation
<https://afni.nimh.nih.gov/pub/dist/doc/program_help/3dBlurToFWHM.html>`_

Examples
~~~~~~~~

>>> from nipype.interfaces import afni
>>> blur = afni.preprocess.BlurToFWHM()
>>> blur.inputs.in_file = 'epi.nii'
>>> blur.inputs.fwhm = 2.5
>>> blur.cmdline  # doctest: +ELLIPSIS +ALLOW_UNICODE
'3dBlurToFWHM -FWHM 2.500000 -input epi.nii -prefix epi_afni'
>>> res = blur.run()  # doctest: +SKIP

Inputs::

        [Mandatory]
        in_file: (an existing file name)
                The dataset that will be smoothed
                flag: -input %s

        [Optional]
        args: (a unicode string)
                Additional parameters to the command
                flag: %s
        automask: (a boolean)
                Create an automask from the input dataset.
                flag: -automask
        blurmaster: (an existing file name)
                The dataset whose smoothness controls the process.
                flag: -blurmaster %s
        environ: (a dictionary with keys which are a bytes or None or a value
                 of class 'str' and with values which are a bytes or None or a value
                 of class 'str', nipype default value: {})
                Environment variables
        fwhm: (a float)
                Blur until the 3D FWHM reaches this value (in mm)
                flag: -FWHM %f
        fwhmxy: (a float)
                Blur until the 2D (x,y)-plane FWHM reaches this value (in mm)
                flag: -FWHMxy %f
        ignore_exception: (a boolean, nipype default value: False)
                Print an error message instead of throwing an exception in case the
                interface fails to run
        mask: (an existing file name)
                Mask dataset, if desired. Voxels NOT in mask will be set to zero in
                output.
                flag: -blurmaster %s
        out_file: (a file name)
                output image file name
                flag: -prefix %s
        outputtype: ('NIFTI' or 'AFNI' or 'NIFTI_GZ')
                AFNI output filetype
        terminal_output: ('stream' or 'allatonce' or 'file' or 'none')
                Control terminal output: `stream` - displays to terminal immediately
                (default), `allatonce` - waits till command is finished to display
                output, `file` - writes output to file, `none` - output is ignored

Outputs::

        out_file: (an existing file name)
                output file

References::
None
None

.. _nipype.interfaces.afni.preprocess.ClipLevel:


.. index:: ClipLevel

ClipLevel
---------

`Link to code <http://github.com/nipy/nipype/tree/ec86b7476/nipype/interfaces/afni/preprocess.py#L691>`__

Wraps command **3dClipLevel**

Estimates the value at which to clip the anatomical dataset so
   that background regions are set to zero.

For complete details, see the `3dClipLevel Documentation.
<https://afni.nimh.nih.gov/pub/dist/doc/program_help/3dClipLevel.html>`_

Examples
~~~~~~~~

>>> from nipype.interfaces.afni import preprocess
>>> cliplevel = preprocess.ClipLevel()
>>> cliplevel.inputs.in_file = 'anatomical.nii'
>>> cliplevel.cmdline  # doctest: +ALLOW_UNICODE
'3dClipLevel anatomical.nii'
>>> res = cliplevel.run()  # doctest: +SKIP

Inputs::

        [Mandatory]
        in_file: (an existing file name)
                input file to 3dClipLevel
                flag: %s, position: -1

        [Optional]
        args: (a unicode string)
                Additional parameters to the command
                flag: %s
        doall: (a boolean)
                Apply the algorithm to each sub-brick separately.
                flag: -doall, position: 3
                mutually_exclusive: g, r, a, d
        environ: (a dictionary with keys which are a bytes or None or a value
                 of class 'str' and with values which are a bytes or None or a value
                 of class 'str', nipype default value: {})
                Environment variables
        grad: (a file name)
                Also compute a 'gradual' clip level as a function of voxel position,
                and output that to a dataset.
                flag: -grad %s, position: 3
                mutually_exclusive: d, o, a, l, l
        ignore_exception: (a boolean, nipype default value: False)
                Print an error message instead of throwing an exception in case the
                interface fails to run
        mfrac: (a float)
                Use the number ff instead of 0.50 in the algorithm
                flag: -mfrac %s, position: 2
        terminal_output: ('stream' or 'allatonce' or 'file' or 'none')
                Control terminal output: `stream` - displays to terminal immediately
                (default), `allatonce` - waits till command is finished to display
                output, `file` - writes output to file, `none` - output is ignored

Outputs::

        clip_val: (a float)
                output

.. _nipype.interfaces.afni.preprocess.DegreeCentrality:


.. index:: DegreeCentrality

DegreeCentrality
----------------

`Link to code <http://github.com/nipy/nipype/tree/ec86b7476/nipype/interfaces/afni/preprocess.py#L771>`__

Wraps command **3dDegreeCentrality**

Performs degree centrality on a dataset using a given maskfile
via 3dDegreeCentrality

For complete details, see the `3dDegreeCentrality Documentation.
<https://afni.nimh.nih.gov/pub/dist/doc/program_help/3dDegreeCentrality.html>`_

Examples
~~~~~~~~

>>> from nipype.interfaces import afni
>>> degree = afni.DegreeCentrality()
>>> degree.inputs.in_file = 'functional.nii'
>>> degree.inputs.mask = 'mask.nii'
>>> degree.inputs.sparsity = 1 # keep the top one percent of connections
>>> degree.inputs.out_file = 'out.nii'
>>> degree.cmdline  # doctest: +ALLOW_UNICODE
'3dDegreeCentrality -mask mask.nii -prefix out.nii -sparsity 1.000000 functional.nii'
>>> res = degree.run()  # doctest: +SKIP

Inputs::

        [Mandatory]
        in_file: (an existing file name)
                input file to 3dDegreeCentrality
                flag: %s, position: -1

        [Optional]
        args: (a unicode string)
                Additional parameters to the command
                flag: %s
        autoclip: (a boolean)
                Clip off low-intensity regions in the dataset
                flag: -autoclip
        automask: (a boolean)
                Mask the dataset to target brain-only voxels
                flag: -automask
        environ: (a dictionary with keys which are a bytes or None or a value
                 of class 'str' and with values which are a bytes or None or a value
                 of class 'str', nipype default value: {})
                Environment variables
        ignore_exception: (a boolean, nipype default value: False)
                Print an error message instead of throwing an exception in case the
                interface fails to run
        mask: (an existing file name)
                mask file to mask input data
                flag: -mask %s
        oned_file: (a unicode string)
                output filepath to text dump of correlation matrix
                flag: -out1D %s
        out_file: (a file name)
                output image file name
                flag: -prefix %s
        outputtype: ('NIFTI' or 'AFNI' or 'NIFTI_GZ')
                AFNI output filetype
        polort: (an integer (int or long))
                flag: -polort %d
        sparsity: (a float)
                only take the top percent of connections
                flag: -sparsity %f
        terminal_output: ('stream' or 'allatonce' or 'file' or 'none')
                Control terminal output: `stream` - displays to terminal immediately
                (default), `allatonce` - waits till command is finished to display
                output, `file` - writes output to file, `none` - output is ignored
        thresh: (a float)
                threshold to exclude connections where corr <= thresh
                flag: -thresh %f

Outputs::

        oned_file: (a file name)
                The text output of the similarity matrix computed after thresholding
                with one-dimensional and ijk voxel indices, correlations, image
                extents, and affine matrix.
        out_file: (an existing file name)
                output file

References::
None
None

.. _nipype.interfaces.afni.preprocess.Despike:


.. index:: Despike

Despike
-------

`Link to code <http://github.com/nipy/nipype/tree/ec86b7476/nipype/interfaces/afni/preprocess.py#L825>`__

Wraps command **3dDespike**

Removes 'spikes' from the 3D+time input dataset

For complete details, see the `3dDespike Documentation.
<https://afni.nimh.nih.gov/pub/dist/doc/program_help/3dDespike.html>`_

Examples
~~~~~~~~

>>> from nipype.interfaces import afni
>>> despike = afni.Despike()
>>> despike.inputs.in_file = 'functional.nii'
>>> despike.cmdline  # doctest: +ALLOW_UNICODE
'3dDespike -prefix functional_despike functional.nii'
>>> res = despike.run()  # doctest: +SKIP

Inputs::

        [Mandatory]
        in_file: (an existing file name)
                input file to 3dDespike
                flag: %s, position: -1

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
                output image file name
                flag: -prefix %s
        outputtype: ('NIFTI' or 'AFNI' or 'NIFTI_GZ')
                AFNI output filetype
        terminal_output: ('stream' or 'allatonce' or 'file' or 'none')
                Control terminal output: `stream` - displays to terminal immediately
                (default), `allatonce` - waits till command is finished to display
                output, `file` - writes output to file, `none` - output is ignored

Outputs::

        out_file: (an existing file name)
                output file

References::
None
None

.. _nipype.interfaces.afni.preprocess.Detrend:


.. index:: Detrend

Detrend
-------

`Link to code <http://github.com/nipy/nipype/tree/ec86b7476/nipype/interfaces/afni/preprocess.py#L863>`__

Wraps command **3dDetrend**

This program removes components from voxel time series using
linear least squares

For complete details, see the `3dDetrend Documentation.
<https://afni.nimh.nih.gov/pub/dist/doc/program_help/3dDetrend.html>`_

Examples
~~~~~~~~

>>> from nipype.interfaces import afni
>>> detrend = afni.Detrend()
>>> detrend.inputs.in_file = 'functional.nii'
>>> detrend.inputs.args = '-polort 2'
>>> detrend.inputs.outputtype = 'AFNI'
>>> detrend.cmdline  # doctest: +ALLOW_UNICODE
'3dDetrend -polort 2 -prefix functional_detrend functional.nii'
>>> res = detrend.run()  # doctest: +SKIP

Inputs::

        [Mandatory]
        in_file: (an existing file name)
                input file to 3dDetrend
                flag: %s, position: -1

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
                output image file name
                flag: -prefix %s
        outputtype: ('NIFTI' or 'AFNI' or 'NIFTI_GZ')
                AFNI output filetype
        terminal_output: ('stream' or 'allatonce' or 'file' or 'none')
                Control terminal output: `stream` - displays to terminal immediately
                (default), `allatonce` - waits till command is finished to display
                output, `file` - writes output to file, `none` - output is ignored

Outputs::

        out_file: (an existing file name)
                output file

References::
None
None

.. _nipype.interfaces.afni.preprocess.ECM:


.. index:: ECM

ECM
---

`Link to code <http://github.com/nipy/nipype/tree/ec86b7476/nipype/interfaces/afni/preprocess.py#L934>`__

Wraps command **3dECM**

Performs degree centrality on a dataset using a given maskfile
via the 3dECM command

For complete details, see the `3dECM Documentation.
<https://afni.nimh.nih.gov/pub/dist/doc/program_help/3dECM.html>`_

Examples
~~~~~~~~

>>> from nipype.interfaces import afni
>>> ecm = afni.ECM()
>>> ecm.inputs.in_file = 'functional.nii'
>>> ecm.inputs.mask = 'mask.nii'
>>> ecm.inputs.sparsity = 0.1 # keep top 0.1% of connections
>>> ecm.inputs.out_file = 'out.nii'
>>> ecm.cmdline  # doctest: +ALLOW_UNICODE
'3dECM -mask mask.nii -prefix out.nii -sparsity 0.100000 functional.nii'
>>> res = ecm.run()  # doctest: +SKIP

Inputs::

        [Mandatory]
        in_file: (an existing file name)
                input file to 3dECM
                flag: %s, position: -1

        [Optional]
        args: (a unicode string)
                Additional parameters to the command
                flag: %s
        autoclip: (a boolean)
                Clip off low-intensity regions in the dataset
                flag: -autoclip
        automask: (a boolean)
                Mask the dataset to target brain-only voxels
                flag: -automask
        environ: (a dictionary with keys which are a bytes or None or a value
                 of class 'str' and with values which are a bytes or None or a value
                 of class 'str', nipype default value: {})
                Environment variables
        eps: (a float)
                sets the stopping criterion for the power iteration; l2|v_old -
                v_new| < eps*|v_old|; default = 0.001
                flag: -eps %f
        fecm: (a boolean)
                Fast centrality method; substantial speed increase but cannot
                accomodate thresholding; automatically selected if -thresh or
                -sparsity are not set
                flag: -fecm
        full: (a boolean)
                Full power method; enables thresholding; automatically selected if
                -thresh or -sparsity are set
                flag: -full
        ignore_exception: (a boolean, nipype default value: False)
                Print an error message instead of throwing an exception in case the
                interface fails to run
        mask: (an existing file name)
                mask file to mask input data
                flag: -mask %s
        max_iter: (an integer (int or long))
                sets the maximum number of iterations to use in the power iteration;
                default = 1000
                flag: -max_iter %d
        memory: (a float)
                Limit memory consumption on system by setting the amount of GB to
                limit the algorithm to; default = 2GB
                flag: -memory %f
        out_file: (a file name)
                output image file name
                flag: -prefix %s
        outputtype: ('NIFTI' or 'AFNI' or 'NIFTI_GZ')
                AFNI output filetype
        polort: (an integer (int or long))
                flag: -polort %d
        scale: (a float)
                scale correlation coefficients in similarity matrix to after
                shifting, x >= 0.0; default = 1.0 for -full, 0.5 for -fecm
                flag: -scale %f
        shift: (a float)
                shift correlation coefficients in similarity matrix to enforce non-
                negativity, s >= 0.0; default = 0.0 for -full, 1.0 for -fecm
                flag: -shift %f
        sparsity: (a float)
                only take the top percent of connections
                flag: -sparsity %f
        terminal_output: ('stream' or 'allatonce' or 'file' or 'none')
                Control terminal output: `stream` - displays to terminal immediately
                (default), `allatonce` - waits till command is finished to display
                output, `file` - writes output to file, `none` - output is ignored
        thresh: (a float)
                threshold to exclude connections where corr <= thresh
                flag: -thresh %f

Outputs::

        out_file: (an existing file name)
                output file

References::
None
None

.. _nipype.interfaces.afni.preprocess.Fim:


.. index:: Fim

Fim
---

`Link to code <http://github.com/nipy/nipype/tree/ec86b7476/nipype/interfaces/afni/preprocess.py#L990>`__

Wraps command **3dfim+**

Program to calculate the cross-correlation of an ideal reference
waveform with the measured FMRI time series for each voxel.

For complete details, see the `3dfim+ Documentation.
<https://afni.nimh.nih.gov/pub/dist/doc/program_help/3dfim+.html>`_

Examples
~~~~~~~~

>>> from nipype.interfaces import afni
>>> fim = afni.Fim()
>>> fim.inputs.in_file = 'functional.nii'
>>> fim.inputs.ideal_file= 'seed.1D'
>>> fim.inputs.out_file = 'functional_corr.nii'
>>> fim.inputs.out = 'Correlation'
>>> fim.inputs.fim_thr = 0.0009
>>> fim.cmdline  # doctest: +ALLOW_UNICODE
'3dfim+ -input functional.nii -ideal_file seed.1D -fim_thr 0.000900 -out Correlation -bucket functional_corr.nii'
>>> res = fim.run()  # doctest: +SKIP

Inputs::

        [Mandatory]
        ideal_file: (an existing file name)
                ideal time series file name
                flag: -ideal_file %s, position: 2
        in_file: (an existing file name)
                input file to 3dfim+
                flag: -input %s, position: 1

        [Optional]
        args: (a unicode string)
                Additional parameters to the command
                flag: %s
        environ: (a dictionary with keys which are a bytes or None or a value
                 of class 'str' and with values which are a bytes or None or a value
                 of class 'str', nipype default value: {})
                Environment variables
        fim_thr: (a float)
                fim internal mask threshold value
                flag: -fim_thr %f, position: 3
        ignore_exception: (a boolean, nipype default value: False)
                Print an error message instead of throwing an exception in case the
                interface fails to run
        out: (a unicode string)
                Flag to output the specified parameter
                flag: -out %s, position: 4
        out_file: (a file name)
                output image file name
                flag: -bucket %s
        outputtype: ('NIFTI' or 'AFNI' or 'NIFTI_GZ')
                AFNI output filetype
        terminal_output: ('stream' or 'allatonce' or 'file' or 'none')
                Control terminal output: `stream` - displays to terminal immediately
                (default), `allatonce` - waits till command is finished to display
                output, `file` - writes output to file, `none` - output is ignored

Outputs::

        out_file: (an existing file name)
                output file

References::
None
None

.. _nipype.interfaces.afni.preprocess.Fourier:


.. index:: Fourier

Fourier
-------

`Link to code <http://github.com/nipy/nipype/tree/ec86b7476/nipype/interfaces/afni/preprocess.py#L1045>`__

Wraps command **3dFourier**

Program to lowpass and/or highpass each voxel time series in a
dataset, via the FFT

For complete details, see the `3dFourier Documentation.
<https://afni.nimh.nih.gov/pub/dist/doc/program_help/3dFourier.html>`_

Examples
~~~~~~~~

>>> from nipype.interfaces import afni
>>> fourier = afni.Fourier()
>>> fourier.inputs.in_file = 'functional.nii'
>>> fourier.inputs.retrend = True
>>> fourier.inputs.highpass = 0.005
>>> fourier.inputs.lowpass = 0.1
>>> fourier.cmdline  # doctest: +ALLOW_UNICODE
'3dFourier -highpass 0.005000 -lowpass 0.100000 -prefix functional_fourier -retrend functional.nii'
>>> res = fourier.run()  # doctest: +SKIP

Inputs::

        [Mandatory]
        highpass: (a float)
                highpass
                flag: -highpass %f
        in_file: (an existing file name)
                input file to 3dFourier
                flag: %s, position: -1
        lowpass: (a float)
                lowpass
                flag: -lowpass %f

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
                output image file name
                flag: -prefix %s
        outputtype: ('NIFTI' or 'AFNI' or 'NIFTI_GZ')
                AFNI output filetype
        retrend: (a boolean)
                Any mean and linear trend are removed before filtering. This will
                restore the trend after filtering.
                flag: -retrend
        terminal_output: ('stream' or 'allatonce' or 'file' or 'none')
                Control terminal output: `stream` - displays to terminal immediately
                (default), `allatonce` - waits till command is finished to display
                output, `file` - writes output to file, `none` - output is ignored

Outputs::

        out_file: (an existing file name)
                output file

References::
None
None

.. _nipype.interfaces.afni.preprocess.Hist:


.. index:: Hist

Hist
----

`Link to code <http://github.com/nipy/nipype/tree/ec86b7476/nipype/interfaces/afni/preprocess.py#L1121>`__

Wraps command **3dHist**

Computes average of all voxels in the input dataset
which satisfy the criterion in the options list

For complete details, see the `3dHist Documentation.
<https://afni.nimh.nih.gov/pub/dist/doc/program_help/3dHist.html>`_

Examples
~~~~~~~~

>>> from nipype.interfaces import afni
>>> hist = afni.Hist()
>>> hist.inputs.in_file = 'functional.nii'
>>> hist.cmdline  # doctest: +ALLOW_UNICODE
'3dHist -input functional.nii -prefix functional_hist'
>>> res = hist.run()  # doctest: +SKIP

Inputs::

        [Mandatory]
        in_file: (an existing file name)
                input file to 3dHist
                flag: -input %s, position: 1

        [Optional]
        args: (a unicode string)
                Additional parameters to the command
                flag: %s
        bin_width: (a float)
                bin width
                flag: -binwidth %f
        environ: (a dictionary with keys which are a bytes or None or a value
                 of class 'str' and with values which are a bytes or None or a value
                 of class 'str', nipype default value: {})
                Environment variables
        ignore_exception: (a boolean, nipype default value: False)
                Print an error message instead of throwing an exception in case the
                interface fails to run
        mask: (an existing file name)
                matrix to align input file
                flag: -mask %s
        max_value: (a float)
                maximum intensity value
                flag: -max %f
        min_value: (a float)
                minimum intensity value
                flag: -min %f
        nbin: (an integer (int or long))
                number of bins
                flag: -nbin %d
        out_file: (a file name)
                Write histogram to niml file with this prefix
                flag: -prefix %s
        out_show: (a file name)
                output image file name
                flag: > %s, position: -1
        showhist: (a boolean, nipype default value: False)
                write a text visual histogram
                flag: -showhist
        terminal_output: ('stream' or 'allatonce' or 'file' or 'none')
                Control terminal output: `stream` - displays to terminal immediately
                (default), `allatonce` - waits till command is finished to display
                output, `file` - writes output to file, `none` - output is ignored

Outputs::

        out_file: (an existing file name)
                output file
        out_show: (a file name)
                output visual histogram

.. _nipype.interfaces.afni.preprocess.LFCD:


.. index:: LFCD

LFCD
----

`Link to code <http://github.com/nipy/nipype/tree/ec86b7476/nipype/interfaces/afni/preprocess.py#L1182>`__

Wraps command **3dLFCD**

Performs degree centrality on a dataset using a given maskfile
via the 3dLFCD command

For complete details, see the `3dLFCD Documentation.
<https://afni.nimh.nih.gov/pub/dist/doc/program_help/3dLFCD.html>`_

Examples
~~~~~~~~

>>> from nipype.interfaces import afni
>>> lfcd = afni.LFCD()
>>> lfcd.inputs.in_file = 'functional.nii'
>>> lfcd.inputs.mask = 'mask.nii'
>>> lfcd.inputs.thresh = 0.8 # keep all connections with corr >= 0.8
>>> lfcd.inputs.out_file = 'out.nii'
>>> lfcd.cmdline  # doctest: +ALLOW_UNICODE
'3dLFCD -mask mask.nii -prefix out.nii -thresh 0.800000 functional.nii'
>>> res = lfcd.run()  # doctest: +SKIP

Inputs::

        [Mandatory]
        in_file: (an existing file name)
                input file to 3dLFCD
                flag: %s, position: -1

        [Optional]
        args: (a unicode string)
                Additional parameters to the command
                flag: %s
        autoclip: (a boolean)
                Clip off low-intensity regions in the dataset
                flag: -autoclip
        automask: (a boolean)
                Mask the dataset to target brain-only voxels
                flag: -automask
        environ: (a dictionary with keys which are a bytes or None or a value
                 of class 'str' and with values which are a bytes or None or a value
                 of class 'str', nipype default value: {})
                Environment variables
        ignore_exception: (a boolean, nipype default value: False)
                Print an error message instead of throwing an exception in case the
                interface fails to run
        mask: (an existing file name)
                mask file to mask input data
                flag: -mask %s
        out_file: (a file name)
                output image file name
                flag: -prefix %s
        outputtype: ('NIFTI' or 'AFNI' or 'NIFTI_GZ')
                AFNI output filetype
        polort: (an integer (int or long))
                flag: -polort %d
        terminal_output: ('stream' or 'allatonce' or 'file' or 'none')
                Control terminal output: `stream` - displays to terminal immediately
                (default), `allatonce` - waits till command is finished to display
                output, `file` - writes output to file, `none` - output is ignored
        thresh: (a float)
                threshold to exclude connections where corr <= thresh
                flag: -thresh %f

Outputs::

        out_file: (an existing file name)
                output file

References::
None
None

.. _nipype.interfaces.afni.preprocess.Maskave:


.. index:: Maskave

Maskave
-------

`Link to code <http://github.com/nipy/nipype/tree/ec86b7476/nipype/interfaces/afni/preprocess.py#L1234>`__

Wraps command **3dmaskave**

Computes average of all voxels in the input dataset
which satisfy the criterion in the options list

For complete details, see the `3dmaskave Documentation.
<https://afni.nimh.nih.gov/pub/dist/doc/program_help/3dmaskave.html>`_

Examples
~~~~~~~~

>>> from nipype.interfaces import afni
>>> maskave = afni.Maskave()
>>> maskave.inputs.in_file = 'functional.nii'
>>> maskave.inputs.mask= 'seed_mask.nii'
>>> maskave.inputs.quiet= True
>>> maskave.cmdline  # doctest: +ELLIPSIS +ALLOW_UNICODE
'3dmaskave -mask seed_mask.nii -quiet functional.nii > functional_maskave.1D'
>>> res = maskave.run()  # doctest: +SKIP

Inputs::

        [Mandatory]
        in_file: (an existing file name)
                input file to 3dmaskave
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
        mask: (an existing file name)
                matrix to align input file
                flag: -mask %s, position: 1
        out_file: (a file name)
                output image file name
                flag: > %s, position: -1
        outputtype: ('NIFTI' or 'AFNI' or 'NIFTI_GZ')
                AFNI output filetype
        quiet: (a boolean)
                matrix to align input file
                flag: -quiet, position: 2
        terminal_output: ('stream' or 'allatonce' or 'file' or 'none')
                Control terminal output: `stream` - displays to terminal immediately
                (default), `allatonce` - waits till command is finished to display
                output, `file` - writes output to file, `none` - output is ignored

Outputs::

        out_file: (an existing file name)
                output file

References::
None
None

.. _nipype.interfaces.afni.preprocess.Means:


.. index:: Means

Means
-----

`Link to code <http://github.com/nipy/nipype/tree/ec86b7476/nipype/interfaces/afni/preprocess.py#L1303>`__

Wraps command **3dMean**

Takes the voxel-by-voxel mean of all input datasets using 3dMean

For complete details, see the `3dMean Documentation.
<https://afni.nimh.nih.gov/pub/dist/doc/program_help/3dMean.html>`_

Examples
~~~~~~~~

>>> from nipype.interfaces import afni
>>> means = afni.Means()
>>> means.inputs.in_file_a = 'im1.nii'
>>> means.inputs.in_file_b = 'im2.nii'
>>> means.inputs.out_file =  'output.nii'
>>> means.cmdline  # doctest: +ALLOW_UNICODE
'3dMean im1.nii im2.nii -prefix output.nii'
>>> res = means.run()  # doctest: +SKIP

Inputs::

        [Mandatory]
        in_file_a: (an existing file name)
                input file to 3dMean
                flag: %s, position: 0

        [Optional]
        args: (a unicode string)
                Additional parameters to the command
                flag: %s
        count: (a boolean)
                compute count of non-zero voxels
                flag: -count
        environ: (a dictionary with keys which are a bytes or None or a value
                 of class 'str' and with values which are a bytes or None or a value
                 of class 'str', nipype default value: {})
                Environment variables
        ignore_exception: (a boolean, nipype default value: False)
                Print an error message instead of throwing an exception in case the
                interface fails to run
        in_file_b: (an existing file name)
                another input file to 3dMean
                flag: %s, position: 1
        mask_inter: (a boolean)
                create intersection mask
                flag: -mask_inter
        mask_union: (a boolean)
                create union mask
                flag: -mask_union
        non_zero: (a boolean)
                use only non-zero values
                flag: -non_zero
        out_file: (a file name)
                output image file name
                flag: -prefix %s
        outputtype: ('NIFTI' or 'AFNI' or 'NIFTI_GZ')
                AFNI output filetype
        scale: (a unicode string)
                scaling of output
                flag: -%sscale
        sqr: (a boolean)
                mean square instead of value
                flag: -sqr
        std_dev: (a boolean)
                calculate std dev
                flag: -stdev
        summ: (a boolean)
                take sum, (not average)
                flag: -sum
        terminal_output: ('stream' or 'allatonce' or 'file' or 'none')
                Control terminal output: `stream` - displays to terminal immediately
                (default), `allatonce` - waits till command is finished to display
                output, `file` - writes output to file, `none` - output is ignored

Outputs::

        out_file: (an existing file name)
                output file

References::
None
None

.. _nipype.interfaces.afni.preprocess.OutlierCount:


.. index:: OutlierCount

OutlierCount
------------

`Link to code <http://github.com/nipy/nipype/tree/ec86b7476/nipype/interfaces/afni/preprocess.py#L1411>`__

Wraps command **3dToutcount**

Calculates number of 'outliers' a 3D+time dataset, at each
time point, and writes the results to stdout.

For complete details, see the `3dToutcount Documentation
<https://afni.nimh.nih.gov/pub/dist/doc/program_help/3dToutcount.html>`_

Examples
~~~~~~~~

>>> from nipype.interfaces import afni
>>> toutcount = afni.OutlierCount()
>>> toutcount.inputs.in_file = 'functional.nii'
>>> toutcount.cmdline  # doctest: +ELLIPSIS +ALLOW_UNICODE
'3dToutcount functional.nii > functional_outliers'
>>> res = toutcount.run()  # doctest: +SKIP

Inputs::

        [Mandatory]
        in_file: (an existing file name)
                input dataset
                flag: %s, position: -2

        [Optional]
        args: (a unicode string)
                Additional parameters to the command
                flag: %s
        autoclip: (a boolean, nipype default value: False)
                clip off small voxels
                flag: -autoclip
                mutually_exclusive: in_file
        automask: (a boolean, nipype default value: False)
                clip off small voxels
                flag: -automask
                mutually_exclusive: in_file
        environ: (a dictionary with keys which are a bytes or None or a value
                 of class 'str' and with values which are a bytes or None or a value
                 of class 'str', nipype default value: {})
                Environment variables
        fraction: (a boolean, nipype default value: False)
                write out the fraction of masked voxels which are outliers at each
                timepoint
                flag: -fraction
        ignore_exception: (a boolean, nipype default value: False)
                Print an error message instead of throwing an exception in case the
                interface fails to run
        interval: (a boolean, nipype default value: False)
                write out the median + 3.5 MAD of outlier count with each timepoint
                flag: -range
        legendre: (a boolean, nipype default value: False)
                use Legendre polynomials
                flag: -legendre
        mask: (an existing file name)
                only count voxels within the given mask
                flag: -mask %s
                mutually_exclusive: autoclip, automask
        out_file: (a file name)
                capture standard output
                flag: > %s, position: -1
        outliers_file: (a file name)
                output image file name
                flag: -save %s
        polort: (an integer (int or long))
                detrend each voxel timeseries with polynomials
                flag: -polort %d
        qthr: (0.0 <= a floating point number <= 1.0)
                indicate a value for q to compute alpha
                flag: -qthr %.5f
        save_outliers: (a boolean, nipype default value: False)
                enables out_file option
        terminal_output: ('stream' or 'allatonce' or 'file' or 'none')
                Control terminal output: `stream` - displays to terminal immediately
                (default), `allatonce` - waits till command is finished to display
                output, `file` - writes output to file, `none` - output is ignored

Outputs::

        out_file: (a file name)
                capture standard output
                flag: > %s, position: -1
        out_outliers: (an existing file name)
                output image file name

.. _nipype.interfaces.afni.preprocess.QualityIndex:


.. index:: QualityIndex

QualityIndex
------------

`Link to code <http://github.com/nipy/nipype/tree/ec86b7476/nipype/interfaces/afni/preprocess.py#L1509>`__

Wraps command **3dTqual**

Computes a `quality index' for each sub-brick in a 3D+time dataset.
The output is a 1D time series with the index for each sub-brick.
The results are written to stdout.

For complete details, see the `3dTqual Documentation
<https://afni.nimh.nih.gov/pub/dist/doc/program_help/3dTqual.html>`_

Examples
~~~~~~~~

>>> from nipype.interfaces import afni
>>> tqual = afni.QualityIndex()
>>> tqual.inputs.in_file = 'functional.nii'
>>> tqual.cmdline  # doctest: +ELLIPSIS +ALLOW_UNICODE
'3dTqual functional.nii > functional_tqual'
>>> res = tqual.run()  # doctest: +SKIP

Inputs::

        [Mandatory]
        in_file: (an existing file name)
                input dataset
                flag: %s, position: -2

        [Optional]
        args: (a unicode string)
                Additional parameters to the command
                flag: %s
        autoclip: (a boolean, nipype default value: False)
                clip off small voxels
                flag: -autoclip
                mutually_exclusive: mask
        automask: (a boolean, nipype default value: False)
                clip off small voxels
                flag: -automask
                mutually_exclusive: mask
        clip: (a float)
                clip off values below
                flag: -clip %f
        environ: (a dictionary with keys which are a bytes or None or a value
                 of class 'str' and with values which are a bytes or None or a value
                 of class 'str', nipype default value: {})
                Environment variables
        ignore_exception: (a boolean, nipype default value: False)
                Print an error message instead of throwing an exception in case the
                interface fails to run
        interval: (a boolean, nipype default value: False)
                write out the median + 3.5 MAD of outlier count with each timepoint
                flag: -range
        mask: (an existing file name)
                compute correlation only across masked voxels
                flag: -mask %s
                mutually_exclusive: autoclip, automask
        out_file: (a file name)
                capture standard output
                flag: > %s, position: -1
        quadrant: (a boolean, nipype default value: False)
                Similar to -spearman, but using 1 minus the quadrant correlation
                coefficient as the quality index.
                flag: -quadrant
        spearman: (a boolean, nipype default value: False)
                Quality index is 1 minus the Spearman (rank) correlation coefficient
                of each sub-brick with the median sub-brick. (default).
                flag: -spearman
        terminal_output: ('stream' or 'allatonce' or 'file' or 'none')
                Control terminal output: `stream` - displays to terminal immediately
                (default), `allatonce` - waits till command is finished to display
                output, `file` - writes output to file, `none` - output is ignored

Outputs::

        out_file: (a file name)
                file containing the captured standard output

.. _nipype.interfaces.afni.preprocess.QwarpPlusMinus:


.. index:: QwarpPlusMinus

QwarpPlusMinus
--------------

`Link to code <http://github.com/nipy/nipype/tree/ec86b7476/nipype/interfaces/afni/preprocess.py#L2419>`__

Wraps command **3dQwarp -prefix Qwarp.nii.gz -plusminus**

A version of 3dQwarp for performing field susceptibility correction
using two images with opposing phase encoding directions.

For complete details, see the `3dQwarp Documentation.
<https://afni.nimh.nih.gov/pub/dist/doc/program_help/3dQwarp.html>`_

Examples
~~~~~~~~

>>> from nipype.interfaces import afni
>>> qwarp = afni.QwarpPlusMinus()
>>> qwarp.inputs.source_file = 'sub-01_dir-LR_epi.nii.gz'
>>> qwarp.inputs.nopadWARP = True
>>> qwarp.inputs.base_file = 'sub-01_dir-RL_epi.nii.gz'
>>> qwarp.cmdline  # doctest: +ALLOW_UNICODE
'3dQwarp -prefix Qwarp.nii.gz -plusminus -base sub-01_dir-RL_epi.nii.gz -nopadWARP -source sub-01_dir-LR_epi.nii.gz'
>>> res = warp.run()  # doctest: +SKIP

Inputs::

        [Mandatory]
        base_file: (an existing file name)
                Base image (opposite phase encoding direction than source image).
                flag: -base %s
        source_file: (an existing file name)
                Source image (opposite phase encoding direction than base image).
                flag: -source %s

        [Optional]
        args: (a unicode string)
                Additional parameters to the command
                flag: %s
        blur: (a list of from 1 to 2 items which are a float)
                Gaussian blur the input images by (FWHM) voxels before doing the
                alignment (the output dataset will not be blurred). The default is
                2.345 (for no good reason). Optionally, you can provide 2 values,
                and then the first one is applied to the base volume, the second to
                the source volume. A negative blur radius means to use 3D median
                filtering, rather than Gaussian blurring. This type of filtering
                will better preserve edges, which can be important in alignment.
                flag: -blur %s
        environ: (a dictionary with keys which are a bytes or None or a value
                 of class 'str' and with values which are a bytes or None or a value
                 of class 'str', nipype default value: {})
                Environment variables
        ignore_exception: (a boolean, nipype default value: False)
                Print an error message instead of throwing an exception in case the
                interface fails to run
        minpatch: (an integer (int or long))
                Set the minimum patch size for warp searching to 'mm' voxels.
                flag: -minpatch %d
        nopadWARP: (a boolean)
                If for some reason you require the warp volume tomatch the base
                volume, then use this option to have the outputWARP dataset(s)
                truncated.
                flag: -nopadWARP
        noweight: (a boolean)
                If you want a binary weight (the old default), use this option.That
                is, each voxel in the base volume automask will beweighted the same
                in the computation of the cost functional.
                flag: -noweight
        pblur: (a list of from 1 to 2 items which are a float)
                The fraction of the patch size thatis used for the progressive blur
                by providing a value between 0 and 0.25. If you provide TWO values,
                the first fraction is used for progressively blurring the base image
                and the second for the source image.
                flag: -pblur %s
        terminal_output: ('stream' or 'allatonce' or 'file' or 'none')
                Control terminal output: `stream` - displays to terminal immediately
                (default), `allatonce` - waits till command is finished to display
                output, `file` - writes output to file, `none` - output is ignored

Outputs::

        base_warp: (an existing file name)
                Field suceptibility correction warp (in 'mm') for base image.
        source_warp: (an existing file name)
                Field suceptibility correction warp (in 'mm') for source image.
        warped_base: (an existing file name)
                Undistorted base file.
        warped_source: (an existing file name)
                Undistorted source file.

.. _nipype.interfaces.afni.preprocess.ROIStats:


.. index:: ROIStats

ROIStats
--------

`Link to code <http://github.com/nipy/nipype/tree/ec86b7476/nipype/interfaces/afni/preprocess.py#L1569>`__

Wraps command **3dROIstats**

Display statistics over masked regions

For complete details, see the `3dROIstats Documentation.
<https://afni.nimh.nih.gov/pub/dist/doc/program_help/3dROIstats.html>`_

Examples
~~~~~~~~

>>> from nipype.interfaces import afni
>>> roistats = afni.ROIStats()
>>> roistats.inputs.in_file = 'functional.nii'
>>> roistats.inputs.mask = 'skeleton_mask.nii.gz'
>>> roistats.inputs.quiet = True
>>> roistats.cmdline  # doctest: +ALLOW_UNICODE
'3dROIstats -quiet -mask skeleton_mask.nii.gz functional.nii'
>>> res = roistats.run()  # doctest: +SKIP

Inputs::

        [Mandatory]
        in_file: (an existing file name)
                input file to 3dROIstats
                flag: %s, position: -1
        terminal_output: ('allatonce', nipype default value: allatonce)
                Control terminal output:`allatonce` - waits till command is finished
                to display output

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
        mask: (an existing file name)
                input mask
                flag: -mask %s, position: 3
        mask_f2short: (a boolean)
                Tells the program to convert a float mask to short integers, by
                simple rounding.
                flag: -mask_f2short, position: 2
        quiet: (a boolean)
                execute quietly
                flag: -quiet, position: 1

Outputs::

        stats: (an existing file name)
                output tab separated values file

.. _nipype.interfaces.afni.preprocess.Retroicor:


.. index:: Retroicor

Retroicor
---------

`Link to code <http://github.com/nipy/nipype/tree/ec86b7476/nipype/interfaces/afni/preprocess.py#L1648>`__

Wraps command **3dretroicor**

Performs Retrospective Image Correction for physiological
motion effects, using a slightly modified version of the
RETROICOR algorithm

The durations of the physiological inputs are assumed to equal
the duration of the dataset. Any constant sampling rate may be
used, but 40 Hz seems to be acceptable. This program's cardiac
peak detection algorithm is rather simplistic, so you might try
using the scanner's cardiac gating output (transform it to a
spike wave if necessary).

This program uses slice timing information embedded in the
dataset to estimate the proper cardiac/respiratory phase for
each slice. It makes sense to run this program before any
program that may destroy the slice timings (e.g. 3dvolreg for
motion correction).

For complete details, see the `3dretroicor Documentation.
<https://afni.nimh.nih.gov/pub/dist/doc/program_help/3dretroicor.html>`_

Examples
~~~~~~~~
>>> from nipype.interfaces import afni
>>> ret = afni.Retroicor()
>>> ret.inputs.in_file = 'functional.nii'
>>> ret.inputs.card = 'mask.1D'
>>> ret.inputs.resp = 'resp.1D'
>>> ret.inputs.outputtype = 'NIFTI'
>>> ret.cmdline  # doctest: +ALLOW_UNICODE
'3dretroicor -prefix functional_retroicor.nii -resp resp.1D -card mask.1D functional.nii'
>>> res = ret.run()  # doctest: +SKIP

Inputs::

        [Mandatory]
        in_file: (an existing file name)
                input file to 3dretroicor
                flag: %s, position: -1

        [Optional]
        args: (a unicode string)
                Additional parameters to the command
                flag: %s
        card: (an existing file name)
                1D cardiac data file for cardiac correction
                flag: -card %s, position: -2
        cardphase: (a file name)
                Filename for 1D cardiac phase output
                flag: -cardphase %s, position: -6
        environ: (a dictionary with keys which are a bytes or None or a value
                 of class 'str' and with values which are a bytes or None or a value
                 of class 'str', nipype default value: {})
                Environment variables
        ignore_exception: (a boolean, nipype default value: False)
                Print an error message instead of throwing an exception in case the
                interface fails to run
        order: (an integer (int or long))
                The order of the correction (2 is typical)
                flag: -order %s, position: -5
        out_file: (a file name)
                output image file name
                flag: -prefix %s, position: 1
        outputtype: ('NIFTI' or 'AFNI' or 'NIFTI_GZ')
                AFNI output filetype
        resp: (an existing file name)
                1D respiratory waveform data for correction
                flag: -resp %s, position: -3
        respphase: (a file name)
                Filename for 1D resp phase output
                flag: -respphase %s, position: -7
        terminal_output: ('stream' or 'allatonce' or 'file' or 'none')
                Control terminal output: `stream` - displays to terminal immediately
                (default), `allatonce` - waits till command is finished to display
                output, `file` - writes output to file, `none` - output is ignored
        threshold: (an integer (int or long))
                Threshold for detection of R-wave peaks in input (Make sure it is
                above the background noise level, Try 3/4 or 4/5 times range plus
                minimum)
                flag: -threshold %d, position: -4

Outputs::

        out_file: (an existing file name)
                output file

References::
None
None

.. _nipype.interfaces.afni.preprocess.Seg:


.. index:: Seg

Seg
---

`Link to code <http://github.com/nipy/nipype/tree/ec86b7476/nipype/interfaces/afni/preprocess.py#L1745>`__

Wraps command **3dSeg**

3dSeg segments brain volumes into tissue classes. The program allows
for adding a variety of global and voxelwise priors. However for the
moment, only mixing fractions and MRF are documented.

For complete details, see the `3dSeg Documentation.
<https://afni.nimh.nih.gov/pub/dist/doc/program_help/3dSeg.html>`_

Examples
~~~~~~~~

>>> from nipype.interfaces.afni import preprocess
>>> seg = preprocess.Seg()
>>> seg.inputs.in_file = 'structural.nii'
>>> seg.inputs.mask = 'AUTO'
>>> seg.cmdline  # doctest: +ALLOW_UNICODE
'3dSeg -mask AUTO -anat structural.nii'
>>> res = seg.run()  # doctest: +SKIP

Inputs::

        [Mandatory]
        in_file: (an existing file name)
                ANAT is the volume to segment
                flag: -anat %s, position: -1
        mask: ('AUTO' or an existing file name)
                only non-zero voxels in mask are analyzed. mask can either be a
                dataset or the string "AUTO" which would use AFNI's automask
                function to create the mask.
                flag: -mask %s, position: -2

        [Optional]
        args: (a unicode string)
                Additional parameters to the command
                flag: %s
        bias_classes: (a unicode string)
                A semicolon delimited string of classes that contribute to the
                estimation of the bias field
                flag: -bias_classes %s
        bias_fwhm: (a float)
                The amount of blurring used when estimating the field bias with the
                Wells method
                flag: -bias_fwhm %f
        blur_meth: ('BFT' or 'BIM')
                set the blurring method for bias field estimation
                flag: -blur_meth %s
        bmrf: (a float)
                Weighting factor controlling spatial homogeneity of the
                classifications
                flag: -bmrf %f
        classes: (a unicode string)
                CLASS_STRING is a semicolon delimited string of class labels
                flag: -classes %s
        environ: (a dictionary with keys which are a bytes or None or a value
                 of class 'str' and with values which are a bytes or None or a value
                 of class 'str', nipype default value: {})
                Environment variables
        ignore_exception: (a boolean, nipype default value: False)
                Print an error message instead of throwing an exception in case the
                interface fails to run
        main_N: (an integer (int or long))
                Number of iterations to perform.
                flag: -main_N %d
        mixfloor: (a float)
                Set the minimum value for any class's mixing fraction
                flag: -mixfloor %f
        mixfrac: (a unicode string)
                MIXFRAC sets up the volume-wide (within mask) tissue fractions while
                initializing the segmentation (see IGNORE for exception)
                flag: -mixfrac %s
        prefix: (a unicode string)
                the prefix for the output folder containing all output volumes
                flag: -prefix %s
        terminal_output: ('stream' or 'allatonce' or 'file' or 'none')
                Control terminal output: `stream` - displays to terminal immediately
                (default), `allatonce` - waits till command is finished to display
                output, `file` - writes output to file, `none` - output is ignored

Outputs::

        out_file: (an existing file name)
                output file

.. _nipype.interfaces.afni.preprocess.SkullStrip:


.. index:: SkullStrip

SkullStrip
----------

`Link to code <http://github.com/nipy/nipype/tree/ec86b7476/nipype/interfaces/afni/preprocess.py#L1801>`__

Wraps command **3dSkullStrip**

A program to extract the brain from surrounding tissue from MRI
T1-weighted images.
TODO Add optional arguments.

For complete details, see the `3dSkullStrip Documentation.
<https://afni.nimh.nih.gov/pub/dist/doc/program_help/3dSkullStrip.html>`_

Examples
~~~~~~~~

>>> from nipype.interfaces import afni
>>> skullstrip = afni.SkullStrip()
>>> skullstrip.inputs.in_file = 'functional.nii'
>>> skullstrip.inputs.args = '-o_ply'
>>> skullstrip.cmdline  # doctest: +ALLOW_UNICODE
'3dSkullStrip -input functional.nii -o_ply -prefix functional_skullstrip'
>>> res = skullstrip.run()  # doctest: +SKIP

Inputs::

        [Mandatory]
        in_file: (an existing file name)
                input file to 3dSkullStrip
                flag: -input %s, position: 1

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
                output image file name
                flag: -prefix %s
        outputtype: ('NIFTI' or 'AFNI' or 'NIFTI_GZ')
                AFNI output filetype
        terminal_output: ('stream' or 'allatonce' or 'file' or 'none')
                Control terminal output: `stream` - displays to terminal immediately
                (default), `allatonce` - waits till command is finished to display
                output, `file` - writes output to file, `none` - output is ignored

Outputs::

        out_file: (an existing file name)
                output file

References::
None
None

.. _nipype.interfaces.afni.preprocess.TCorr1D:


.. index:: TCorr1D

TCorr1D
-------

`Link to code <http://github.com/nipy/nipype/tree/ec86b7476/nipype/interfaces/afni/preprocess.py#L1883>`__

Wraps command **3dTcorr1D**

Computes the correlation coefficient between each voxel time series
in the input 3D+time dataset.

For complete details, see the `3dTcorr1D Documentation.
<https://afni.nimh.nih.gov/pub/dist/doc/program_help/3dTcorr1D.html>`_

>>> from nipype.interfaces import afni
>>> tcorr1D = afni.TCorr1D()
>>> tcorr1D.inputs.xset= 'u_rc1s1_Template.nii'
>>> tcorr1D.inputs.y_1d = 'seed.1D'
>>> tcorr1D.cmdline  # doctest: +ALLOW_UNICODE
'3dTcorr1D -prefix u_rc1s1_Template_correlation.nii.gz  u_rc1s1_Template.nii  seed.1D'
>>> res = tcorr1D.run()  # doctest: +SKIP

Inputs::

        [Mandatory]
        xset: (an existing file name)
                3d+time dataset input
                flag:  %s, position: -2
        y_1d: (an existing file name)
                1D time series file input
                flag:  %s, position: -1

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
        ktaub: (a boolean)
                Correlation is the Kendall's tau_b correlation coefficient
                flag:  -ktaub, position: 1
                mutually_exclusive: pearson, spearman, quadrant
        out_file: (a file name)
                output filename prefix
                flag: -prefix %s
        outputtype: ('NIFTI' or 'AFNI' or 'NIFTI_GZ')
                AFNI output filetype
        pearson: (a boolean)
                Correlation is the normal Pearson correlation coefficient
                flag:  -pearson, position: 1
                mutually_exclusive: spearman, quadrant, ktaub
        quadrant: (a boolean)
                Correlation is the quadrant correlation coefficient
                flag:  -quadrant, position: 1
                mutually_exclusive: pearson, spearman, ktaub
        spearman: (a boolean)
                Correlation is the Spearman (rank) correlation coefficient
                flag:  -spearman, position: 1
                mutually_exclusive: pearson, quadrant, ktaub
        terminal_output: ('stream' or 'allatonce' or 'file' or 'none')
                Control terminal output: `stream` - displays to terminal immediately
                (default), `allatonce` - waits till command is finished to display
                output, `file` - writes output to file, `none` - output is ignored

Outputs::

        out_file: (an existing file name)
                output file containing correlations

References::
None
None

.. _nipype.interfaces.afni.preprocess.TCorrMap:


.. index:: TCorrMap

TCorrMap
--------

`Link to code <http://github.com/nipy/nipype/tree/ec86b7476/nipype/interfaces/afni/preprocess.py#L2020>`__

Wraps command **3dTcorrMap**

For each voxel time series, computes the correlation between it
and all other voxels, and combines this set of values into the
output dataset(s) in some way.

For complete details, see the `3dTcorrMap Documentation.
<https://afni.nimh.nih.gov/pub/dist/doc/program_help/3dTcorrMap.html>`_

Examples
~~~~~~~~

>>> from nipype.interfaces import afni
>>> tcm = afni.TCorrMap()
>>> tcm.inputs.in_file = 'functional.nii'
>>> tcm.inputs.mask = 'mask.nii'
>>> tcm.mean_file = 'functional_meancorr.nii'
>>> tcm.cmdline  # doctest: +ALLOW_UNICODE +SKIP
'3dTcorrMap -input functional.nii -mask mask.nii -Mean functional_meancorr.nii'
>>> res = tcm.run()  # doctest: +SKIP

Inputs::

        [Mandatory]
        in_file: (an existing file name)
                flag: -input %s

        [Optional]
        absolute_threshold: (a file name)
                flag: -Thresh %f %s
                mutually_exclusive: absolute_threshold, var_absolute_threshold,
                 var_absolute_threshold_normalize
        args: (a unicode string)
                Additional parameters to the command
                flag: %s
        automask: (a boolean)
                flag: -automask
        average_expr: (a file name)
                flag: -Aexpr %s %s
                mutually_exclusive: average_expr, average_expr_nonzero, sum_expr
        average_expr_nonzero: (a file name)
                flag: -Cexpr %s %s
                mutually_exclusive: average_expr, average_expr_nonzero, sum_expr
        bandpass: (a tuple of the form: (a float, a float))
                flag: -bpass %f %f
        blur_fwhm: (a float)
                flag: -Gblur %f
        correlation_maps: (a file name)
                flag: -CorrMap %s
        correlation_maps_masked: (a file name)
                flag: -CorrMask %s
        environ: (a dictionary with keys which are a bytes or None or a value
                 of class 'str' and with values which are a bytes or None or a value
                 of class 'str', nipype default value: {})
                Environment variables
        expr: (a unicode string)
        histogram: (a file name)
                flag: -Hist %d %s
        histogram_bin_numbers: (an integer (int or long))
        ignore_exception: (a boolean, nipype default value: False)
                Print an error message instead of throwing an exception in case the
                interface fails to run
        mask: (an existing file name)
                flag: -mask %s
        mean_file: (a file name)
                flag: -Mean %s
        out_file: (a file name)
                output image file name
                flag: -prefix %s
        outputtype: ('NIFTI' or 'AFNI' or 'NIFTI_GZ')
                AFNI output filetype
        pmean: (a file name)
                flag: -Pmean %s
        polort: (an integer (int or long))
                flag: -polort %d
        qmean: (a file name)
                flag: -Qmean %s
        regress_out_timeseries: (a file name)
                flag: -ort %s
        seeds: (an existing file name)
                flag: -seed %s
                mutually_exclusive: s, e, e, d, s, _, w, i, d, t, h
        seeds_width: (a float)
                flag: -Mseed %f
                mutually_exclusive: s, e, e, d, s
        sum_expr: (a file name)
                flag: -Sexpr %s %s
                mutually_exclusive: average_expr, average_expr_nonzero, sum_expr
        terminal_output: ('stream' or 'allatonce' or 'file' or 'none')
                Control terminal output: `stream` - displays to terminal immediately
                (default), `allatonce` - waits till command is finished to display
                output, `file` - writes output to file, `none` - output is ignored
        thresholds: (a list of items which are an integer (int or long))
        var_absolute_threshold: (a file name)
                flag: -VarThresh %f %f %f %s
                mutually_exclusive: absolute_threshold, var_absolute_threshold,
                 var_absolute_threshold_normalize
        var_absolute_threshold_normalize: (a file name)
                flag: -VarThreshN %f %f %f %s
                mutually_exclusive: absolute_threshold, var_absolute_threshold,
                 var_absolute_threshold_normalize
        zmean: (a file name)
                flag: -Zmean %s

Outputs::

        absolute_threshold: (a file name)
        average_expr: (a file name)
        average_expr_nonzero: (a file name)
        correlation_maps: (a file name)
        correlation_maps_masked: (a file name)
        histogram: (a file name)
        mean_file: (a file name)
        pmean: (a file name)
        qmean: (a file name)
        sum_expr: (a file name)
        var_absolute_threshold: (a file name)
        var_absolute_threshold_normalize: (a file name)
        zmean: (a file name)

References::
None
None

.. _nipype.interfaces.afni.preprocess.TCorrelate:


.. index:: TCorrelate

TCorrelate
----------

`Link to code <http://github.com/nipy/nipype/tree/ec86b7476/nipype/interfaces/afni/preprocess.py#L2087>`__

Wraps command **3dTcorrelate**

Computes the correlation coefficient between corresponding voxel
time series in two input 3D+time datasets 'xset' and 'yset'

For complete details, see the `3dTcorrelate Documentation.
<https://afni.nimh.nih.gov/pub/dist/doc/program_help/3dTcorrelate.html>`_

Examples
~~~~~~~~

>>> from nipype.interfaces import afni
>>> tcorrelate = afni.TCorrelate()
>>> tcorrelate.inputs.xset= 'u_rc1s1_Template.nii'
>>> tcorrelate.inputs.yset = 'u_rc1s2_Template.nii'
>>> tcorrelate.inputs.out_file = 'functional_tcorrelate.nii.gz'
>>> tcorrelate.inputs.polort = -1
>>> tcorrelate.inputs.pearson = True
>>> tcorrelate.cmdline  # doctest: +ALLOW_UNICODE
'3dTcorrelate -prefix functional_tcorrelate.nii.gz -pearson -polort -1 u_rc1s1_Template.nii u_rc1s2_Template.nii'
>>> res = tcarrelate.run()  # doctest: +SKIP

Inputs::

        [Mandatory]
        xset: (an existing file name)
                input xset
                flag: %s, position: -2
        yset: (an existing file name)
                input yset
                flag: %s, position: -1

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
                output image file name
                flag: -prefix %s
        outputtype: ('NIFTI' or 'AFNI' or 'NIFTI_GZ')
                AFNI output filetype
        pearson: (a boolean)
                Correlation is the normal Pearson correlation coefficient
                flag: -pearson
        polort: (an integer (int or long))
                Remove polynomical trend of order m
                flag: -polort %d
        terminal_output: ('stream' or 'allatonce' or 'file' or 'none')
                Control terminal output: `stream` - displays to terminal immediately
                (default), `allatonce` - waits till command is finished to display
                output, `file` - writes output to file, `none` - output is ignored

Outputs::

        out_file: (an existing file name)
                output file

References::
None
None

.. _nipype.interfaces.afni.preprocess.TShift:


.. index:: TShift

TShift
------

`Link to code <http://github.com/nipy/nipype/tree/ec86b7476/nipype/interfaces/afni/preprocess.py#L2160>`__

Wraps command **3dTshift**

Shifts voxel time series from input so that seperate slices are aligned
to the same temporal origin.

For complete details, see the `3dTshift Documentation.
<https://afni.nimh.nih.gov/pub/dist/doc/program_help/3dTshift.html>`_

Examples
~~~~~~~~

>>> from nipype.interfaces import afni
>>> tshift = afni.TShift()
>>> tshift.inputs.in_file = 'functional.nii'
>>> tshift.inputs.tpattern = 'alt+z'
>>> tshift.inputs.tzero = 0.0
>>> tshift.cmdline  # doctest: +ALLOW_UNICODE
'3dTshift -prefix functional_tshift -tpattern alt+z -tzero 0.0 functional.nii'
>>> res = tshift.run()  # doctest: +SKIP

Inputs::

        [Mandatory]
        in_file: (an existing file name)
                input file to 3dTShift
                flag: %s, position: -1

        [Optional]
        args: (a unicode string)
                Additional parameters to the command
                flag: %s
        environ: (a dictionary with keys which are a bytes or None or a value
                 of class 'str' and with values which are a bytes or None or a value
                 of class 'str', nipype default value: {})
                Environment variables
        ignore: (an integer (int or long))
                ignore the first set of points specified
                flag: -ignore %s
        ignore_exception: (a boolean, nipype default value: False)
                Print an error message instead of throwing an exception in case the
                interface fails to run
        interp: ('Fourier' or 'linear' or 'cubic' or 'quintic' or 'heptic')
                different interpolation methods (see 3dTShift for details) default =
                Fourier
                flag: -%s
        out_file: (a file name)
                output image file name
                flag: -prefix %s
        outputtype: ('NIFTI' or 'AFNI' or 'NIFTI_GZ')
                AFNI output filetype
        rlt: (a boolean)
                Before shifting, remove the mean and linear trend
                flag: -rlt
        rltplus: (a boolean)
                Before shifting, remove the mean and linear trend and later put back
                the mean
                flag: -rlt+
        terminal_output: ('stream' or 'allatonce' or 'file' or 'none')
                Control terminal output: `stream` - displays to terminal immediately
                (default), `allatonce` - waits till command is finished to display
                output, `file` - writes output to file, `none` - output is ignored
        tpattern: (a unicode string)
                use specified slice time pattern rather than one in header
                flag: -tpattern %s
        tr: (a unicode string)
                manually set the TR. You can attach suffix "s" for seconds or "ms"
                for milliseconds.
                flag: -TR %s
        tslice: (an integer (int or long))
                align each slice to time offset of given slice
                flag: -slice %s
                mutually_exclusive: tzero
        tzero: (a float)
                align each slice to given time offset
                flag: -tzero %s
                mutually_exclusive: tslice

Outputs::

        out_file: (an existing file name)
                output file

References::
None
None

.. _nipype.interfaces.afni.preprocess.Volreg:


.. index:: Volreg

Volreg
------

`Link to code <http://github.com/nipy/nipype/tree/ec86b7476/nipype/interfaces/afni/preprocess.py#L2252>`__

Wraps command **3dvolreg**

Register input volumes to a base volume using AFNI 3dvolreg command

For complete details, see the `3dvolreg Documentation.
<https://afni.nimh.nih.gov/pub/dist/doc/program_help/3dvolreg.html>`_

Examples
~~~~~~~~

>>> from nipype.interfaces import afni
>>> volreg = afni.Volreg()
>>> volreg.inputs.in_file = 'functional.nii'
>>> volreg.inputs.args = '-Fourier -twopass'
>>> volreg.inputs.zpad = 4
>>> volreg.inputs.outputtype = 'NIFTI'
>>> volreg.cmdline  # doctest: +ELLIPSIS +ALLOW_UNICODE
'3dvolreg -Fourier -twopass -1Dfile functional.1D -1Dmatrix_save functional.aff12.1D -prefix functional_volreg.nii -zpad 4 -maxdisp1D functional_md.1D functional.nii'
>>> res = volreg.run()  # doctest: +SKIP

Inputs::

        [Mandatory]
        in_file: (an existing file name)
                input file to 3dvolreg
                flag: %s, position: -1

        [Optional]
        args: (a unicode string)
                Additional parameters to the command
                flag: %s
        basefile: (an existing file name)
                base file for registration
                flag: -base %s, position: -6
        copyorigin: (a boolean)
                copy base file origin coords to output
                flag: -twodup
        environ: (a dictionary with keys which are a bytes or None or a value
                 of class 'str' and with values which are a bytes or None or a value
                 of class 'str', nipype default value: {})
                Environment variables
        ignore_exception: (a boolean, nipype default value: False)
                Print an error message instead of throwing an exception in case the
                interface fails to run
        md1d_file: (a file name)
                max displacement output file
                flag: -maxdisp1D %s, position: -4
        oned_file: (a file name)
                1D movement parameters output file
                flag: -1Dfile %s
        oned_matrix_save: (a file name)
                Save the matrix transformation
                flag: -1Dmatrix_save %s
        out_file: (a file name)
                output image file name
                flag: -prefix %s
        outputtype: ('NIFTI' or 'AFNI' or 'NIFTI_GZ')
                AFNI output filetype
        terminal_output: ('stream' or 'allatonce' or 'file' or 'none')
                Control terminal output: `stream` - displays to terminal immediately
                (default), `allatonce` - waits till command is finished to display
                output, `file` - writes output to file, `none` - output is ignored
        timeshift: (a boolean)
                time shift to mean slice time offset
                flag: -tshift 0
        verbose: (a boolean)
                more detailed description of the process
                flag: -verbose
        zpad: (an integer (int or long))
                Zeropad around the edges by 'n' voxels during rotations
                flag: -zpad %d, position: -5

Outputs::

        md1d_file: (an existing file name)
                max displacement info file
        oned_file: (an existing file name)
                movement parameters info file
        oned_matrix_save: (an existing file name)
                matrix transformation from base to input
        out_file: (an existing file name)
                registered file

References::
None
None

.. _nipype.interfaces.afni.preprocess.Warp:


.. index:: Warp

Warp
----

`Link to code <http://github.com/nipy/nipype/tree/ec86b7476/nipype/interfaces/afni/preprocess.py#L2320>`__

Wraps command **3dWarp**

Use 3dWarp for spatially transforming a dataset

For complete details, see the `3dWarp Documentation.
<https://afni.nimh.nih.gov/pub/dist/doc/program_help/3dWarp.html>`_

Examples
~~~~~~~~

>>> from nipype.interfaces import afni
>>> warp = afni.Warp()
>>> warp.inputs.in_file = 'structural.nii'
>>> warp.inputs.deoblique = True
>>> warp.inputs.out_file = 'trans.nii.gz'
>>> warp.cmdline  # doctest: +ALLOW_UNICODE
'3dWarp -deoblique -prefix trans.nii.gz structural.nii'
>>> res = warp.run()  # doctest: +SKIP

>>> warp_2 = afni.Warp()
>>> warp_2.inputs.in_file = 'structural.nii'
>>> warp_2.inputs.newgrid = 1.0
>>> warp_2.inputs.out_file = 'trans.nii.gz'
>>> warp_2.cmdline  # doctest: +ALLOW_UNICODE
'3dWarp -newgrid 1.000000 -prefix trans.nii.gz structural.nii'
>>> res = warp_2.run()  # doctest: +SKIP

Inputs::

        [Mandatory]
        in_file: (an existing file name)
                input file to 3dWarp
                flag: %s, position: -1

        [Optional]
        args: (a unicode string)
                Additional parameters to the command
                flag: %s
        deoblique: (a boolean)
                transform dataset from oblique to cardinal
                flag: -deoblique
        environ: (a dictionary with keys which are a bytes or None or a value
                 of class 'str' and with values which are a bytes or None or a value
                 of class 'str', nipype default value: {})
                Environment variables
        gridset: (an existing file name)
                copy grid of specified dataset
                flag: -gridset %s
        ignore_exception: (a boolean, nipype default value: False)
                Print an error message instead of throwing an exception in case the
                interface fails to run
        interp: ('linear' or 'cubic' or 'NN' or 'quintic')
                spatial interpolation methods [default = linear]
                flag: -%s
        matparent: (an existing file name)
                apply transformation from 3dWarpDrive
                flag: -matparent %s
        mni2tta: (a boolean)
                transform dataset from MNI152 to Talaraich
                flag: -mni2tta
        newgrid: (a float)
                specify grid of this size (mm)
                flag: -newgrid %f
        out_file: (a file name)
                output image file name
                flag: -prefix %s
        outputtype: ('NIFTI' or 'AFNI' or 'NIFTI_GZ')
                AFNI output filetype
        terminal_output: ('stream' or 'allatonce' or 'file' or 'none')
                Control terminal output: `stream` - displays to terminal immediately
                (default), `allatonce` - waits till command is finished to display
                output, `file` - writes output to file, `none` - output is ignored
        tta2mni: (a boolean)
                transform dataset from Talairach to MNI152
                flag: -tta2mni
        zpad: (an integer (int or long))
                pad input dataset with N planes of zero on all sides.
                flag: -zpad %d

Outputs::

        out_file: (an existing file name)
                output file

References::
None
None
