.. AUTO-GENERATED FILE -- DO NOT EDIT!

interfaces.niftyfit.dwi
=======================


.. _nipype.interfaces.niftyfit.dwi.DwiTool:


.. index:: DwiTool

DwiTool
-------

`Link to code <http://github.com/nipy/nipype/tree/ec86b7476/nipype/interfaces/niftyfit/dwi.py#L408>`__

Wraps command **dwi_tool**

Interface for executable dwi_tool from Niftyfit platform.

Use DwiTool.

Diffusion-Weighted MR Prediction.
Predicts DWI from previously fitted models and calculates model derived
maps.

`Source code <https://cmiclab.cs.ucl.ac.uk/CMIC/NiftyFit-Release>`_

Examples
~~~~~~~~

>>> from nipype.interfaces import niftyfit
>>> dwi_tool = niftyfit.DwiTool(dti_flag=True)
>>> dwi_tool.inputs.source_file = 'dwi.nii.gz'
>>> dwi_tool.inputs.bvec_file = 'bvecs'
>>> dwi_tool.inputs.bval_file = 'bvals'
>>> dwi_tool.inputs.mask_file = 'mask.nii.gz'
>>> dwi_tool.inputs.b0_file = 'b0.nii.gz'
>>> dwi_tool.inputs.rgbmap_file = 'rgb_map.nii.gz'
>>> dwi_tool.cmdline  # doctest: +ALLOW_UNICODE
'dwi_tool -source dwi.nii.gz -bval bvals -bvec bvecs -b0 b0.nii.gz -mask mask.nii.gz -dti -famap dwi_famap.nii.gz -logdti2 dwi_logdti2.nii.gz -mcmap dwi_mcmap.nii.gz -mdmap dwi_mdmap.nii.gz -rgbmap rgb_map.nii.gz -syn dwi_syn.nii.gz -v1map dwi_v1map.nii.gz'

Inputs::

        [Mandatory]
        bval_file: (a file name)
                The file containing the bvalues of the source DWI.
                flag: -bval %s, position: 2
        source_file: (a file name)
                The source image containing the fitted model.
                flag: -source %s, position: 1

        [Optional]
        args: (a unicode string)
                Additional parameters to the command
                flag: %s
        b0_file: (a file name)
                The B0 image corresponding to the source DWI
                flag: -b0 %s, position: 4
        ball_flag: (a boolean)
                Input is a ball and stick model.
                flag: -ball, position: 6
                mutually_exclusive: mono_flag, ivim_flag, dti_flag, dti_flag2,
                 ballv_flag, nod_flag, nodv_flag
        ballv_flag: (a boolean)
                Input is a ball and stick model with optimised PDD.
                flag: -ballv, position: 6
                mutually_exclusive: mono_flag, ivim_flag, dti_flag, dti_flag2,
                 ball_flag, nod_flag, nodv_flag
        bvec_file: (a file name)
                The file containing the bvectors of the source DWI.
                flag: -bvec %s, position: 3
        diso_val: (a float)
                Isotropic diffusivity for -nod [3e-3]
                flag: -diso %f
        dpr_val: (a float)
                Parallel diffusivity for -nod [1.7e-3].
                flag: -dpr %f
        dti_flag: (a boolean)
                Input is a tensor model diag/off-diag.
                flag: -dti, position: 6
                mutually_exclusive: mono_flag, ivim_flag, dti_flag2, ball_flag,
                 ballv_flag, nod_flag, nodv_flag
        dti_flag2: (a boolean)
                Input is a tensor model lower triangular
                flag: -dti2, position: 6
                mutually_exclusive: mono_flag, ivim_flag, dti_flag, ball_flag,
                 ballv_flag, nod_flag, nodv_flag
        environ: (a dictionary with keys which are a bytes or None or a value
                 of class 'str' and with values which are a bytes or None or a value
                 of class 'str', nipype default value: {})
                Environment variables
        famap_file: (a file name)
                Filename of FA map
                flag: -famap %s
        ignore_exception: (a boolean, nipype default value: False)
                Print an error message instead of throwing an exception in case the
                interface fails to run
        ivim_flag: (a boolean)
                Inputs is an IVIM model to non-directional data.
                flag: -ivim, position: 6
                mutually_exclusive: mono_flag, dti_flag, dti_flag2, ball_flag,
                 ballv_flag, nod_flag, nodv_flag
        logdti_file: (a file name)
                Filename of output logdti map.
                flag: -logdti2 %s
        mask_file: (a file name)
                The image mask
                flag: -mask %s, position: 5
        mcmap_file: (a file name)
                Filename of multi-compartment model parameter map (-ivim,-ball,-nod)
                flag: -mcmap %s
        mdmap_file: (a file name)
                Filename of MD map/ADC
                flag: -mdmap %s
        mono_flag: (a boolean)
                Input is a single exponential to non-directional data [default with
                no b-vectors]
                flag: -mono, position: 6
                mutually_exclusive: ivim_flag, dti_flag, dti_flag2, ball_flag,
                 ballv_flag, nod_flag, nodv_flag
        nod_flag: (a boolean)
                Input is a NODDI model
                flag: -nod, position: 6
                mutually_exclusive: mono_flag, ivim_flag, dti_flag, dti_flag2,
                 ball_flag, ballv_flag, nodv_flag
        nodv_flag: (a boolean)
                Input is a NODDI model with optimised PDD
                flag: -nodv, position: 6
                mutually_exclusive: mono_flag, ivim_flag, dti_flag, dti_flag2,
                 ball_flag, ballv_flag, nod_flag
        rgbmap_file: (a file name)
                Filename of colour FA map.
                flag: -rgbmap %s
        syn_file: (a file name)
                Filename of synthetic image. Requires: bvec_file/b0_file.
                flag: -syn %s
                requires: bvec_file, b0_file
        terminal_output: ('stream' or 'allatonce' or 'file' or 'none')
                Control terminal output: `stream` - displays to terminal immediately
                (default), `allatonce` - waits till command is finished to display
                output, `file` - writes output to file, `none` - output is ignored
        v1map_file: (a file name)
                Filename of PDD map [x,y,z]
                flag: -v1map %s

Outputs::

        famap_file: (a file name)
                Filename of FA map
        logdti_file: (a file name)
                Filename of output logdti map
        mcmap_file: (a file name)
                Filename of multi-compartment model parameter map (-ivim,-ball,-nod)
        mdmap_file: (a file name)
                Filename of MD map/ADC
        rgbmap_file: (a file name)
                Filename of colour FA map
        syn_file: (a file name)
                Filename of synthetic image
        v1map_file: (a file name)
                Filename of PDD map [x,y,z]

.. _nipype.interfaces.niftyfit.dwi.FitDwi:


.. index:: FitDwi

FitDwi
------

`Link to code <http://github.com/nipy/nipype/tree/ec86b7476/nipype/interfaces/niftyfit/dwi.py#L232>`__

Wraps command **fit_dwi**

Interface for executable fit_dwi from Niftyfit platform.

Use NiftyFit to perform diffusion model fitting.

Diffusion-weighted MR Fitting.
Fits DWI parameter maps to multi-shell, multi-directional data.

`Source code <https://cmiclab.cs.ucl.ac.uk/CMIC/NiftyFit-Release>`_

Examples
~~~~~~~~

>>> from nipype.interfaces import niftyfit
>>> fit_dwi = niftyfit.FitDwi(dti_flag=True)
>>> fit_dwi.inputs.source_file = 'dwi.nii.gz'
>>> fit_dwi.inputs.bvec_file = 'bvecs'
>>> fit_dwi.inputs.bval_file = 'bvals'
>>> fit_dwi.inputs.rgbmap_file = 'rgb.nii.gz'
>>> fit_dwi.cmdline  # doctest: +ALLOW_UNICODE
'fit_dwi -source dwi.nii.gz -bval bvals -bvec bvecs -dti -error dwi_error.nii.gz -famap dwi_famap.nii.gz -mcmap dwi_mcmap.nii.gz -mcout dwi_mcout.txt -mdmap dwi_mdmap.nii.gz -nodiff dwi_no_diff.nii.gz -res dwi_resmap.nii.gz -rgbmap rgb.nii.gz -syn dwi_syn.nii.gz -tenmap2 dwi_tenmap2.nii.gz  -v1map dwi_v1map.nii.gz'

Inputs::

        [Mandatory]
        bval_file: (a file name)
                The file containing the bvalues of the source DWI.
                flag: -bval %s, position: 2
        bvec_file: (a file name)
                The file containing the bvectors of the source DWI.
                flag: -bvec %s, position: 3
        source_file: (a file name)
                The source image containing the dwi data.
                flag: -source %s, position: 1

        [Optional]
        acceptance: (a float)
                Fraction of iterations to accept [0.23].
                flag: -accpetance %f
        args: (a unicode string)
                Additional parameters to the command
                flag: %s
        ball_flag: (a boolean)
                Fit the ball and stick model.
                flag: -ball, position: 4
                mutually_exclusive: mono_flag, ivim_flag, dti_flag, ballv_flag,
                 nod_flag, nodv_flag
        ballv_flag: (a boolean)
                Fit the ball and stick model with optimised PDD.
                flag: -ballv, position: 4
                mutually_exclusive: mono_flag, ivim_flag, dti_flag, ball_flag,
                 nod_flag, nodv_flag
        cov_file: (a file name)
                Filename of ithe nc*nc covariance matrix [I]
                flag: -cov %s
        csf_t2_val: (a float)
                CSF T2 value [400ms].
                flag: -csfT2 %f
        diso_val: (a float)
                Isotropic diffusivity for -nod [3e-3]
                flag: -diso %f
        dpr_val: (a float)
                Parallel diffusivity for -nod [1.7e-3].
                flag: -dpr %f
        dti_flag: (a boolean)
                Fit the tensor model [default with b-vectors].
                flag: -dti, position: 4
                mutually_exclusive: mono_flag, ivim_flag, ball_flag, ballv_flag,
                 nod_flag, nodv_flag
        environ: (a dictionary with keys which are a bytes or None or a value
                 of class 'str' and with values which are a bytes or None or a value
                 of class 'str', nipype default value: {})
                Environment variables
        error_file: (a file name)
                Filename of parameter error maps.
                flag: -error %s
        famap_file: (a file name)
                Filename of FA map
                flag: -famap %s
        gn_flag: (a boolean)
                Use Gauss-Newton algorithm [Levenberg-Marquardt].
                flag: -gn
                mutually_exclusive: wls_flag
        ignore_exception: (a boolean, nipype default value: False)
                Print an error message instead of throwing an exception in case the
                interface fails to run
        ivim_flag: (a boolean)
                Fit IVIM model to non-directional data.
                flag: -ivim, position: 4
                mutually_exclusive: mono_flag, dti_flag, ball_flag, ballv_flag,
                 nod_flag, nodv_flag
        lm_vals: (a tuple of the form: (a float, a float))
                LM parameters (initial value, decrease rate) [100,1.2].
                flag: -lm %f %f
                requires: gn_flag
        mask_file: (a file name)
                The image mask
                flag: -mask %s
        maxit_val: (an integer (int or long))
                Maximum number of non-linear LSQR iterations [100x2 passes])
                flag: -maxit %d
                requires: gn_flag
        mcmap_file: (a file name)
                Filename of multi-compartment model parameter map (-ivim,-ball,-nod)
                flag: -mcmap %s
                requires: nodv_flag
        mcmaxit: (an integer (int or long))
                Number of iterations to run [10,000].
                flag: -mcmaxit %d
        mcout: (a file name)
                Filename of mc samples (ascii text file)
                flag: -mcout %s
        mcsamples: (an integer (int or long))
                Number of samples to keep [100].
                flag: -mcsamples %d
        mdmap_file: (a file name)
                Filename of MD map/ADC
                flag: -mdmap %s
        mono_flag: (a boolean)
                Fit single exponential to non-directional data [default with no
                b-vectors]
                flag: -mono, position: 4
                mutually_exclusive: ivim_flag, dti_flag, ball_flag, ballv_flag,
                 nod_flag, nodv_flag
        nod_flag: (a boolean)
                Fit the NODDI model
                flag: -nod, position: 4
                mutually_exclusive: mono_flag, ivim_flag, dti_flag, ball_flag,
                 ballv_flag, nodv_flag
        nodiff_file: (a file name)
                Filename of average no diffusion image.
                flag: -nodiff %s
        nodv_flag: (a boolean)
                Fit the NODDI model with optimised PDD
                flag: -nodv, position: 4
                mutually_exclusive: mono_flag, ivim_flag, dti_flag, ball_flag,
                 ballv_flag, nod_flag
        perf_thr: (a float)
                Threshold for perfusion/diffsuion effects [100].
                flag: -perfthreshold %f
        prior_file: (a file name)
                Filename of parameter priors for -ball and -nod.
                flag: -prior %s
        res_file: (a file name)
                Filename of model residual map.
                flag: -res %s
        rgbmap_file: (a file name)
                Filename of colour-coded FA map
                flag: -rgbmap %s
                requires: dti_flag
        rot_sform_flag: (an integer (int or long))
                Rotate the output tensors according to the q/s form of the image
                (resulting tensors will be in mm coordinates, default: 0).
                flag: -rotsform %d
        slice_no: (an integer (int or long))
                Fit to single slice number.
                flag: -slice %d
        swls_val: (a float)
                Use location-weighted least squares for DTI fitting [3x3 Gaussian]
                flag: -swls %f
        syn_file: (a file name)
                Filename of synthetic image.
                flag: -syn %s
        te_file: (a file name)
                Filename of TEs (ms).
                flag: -TE %s
                mutually_exclusive: te_file
        te_value: (a file name)
                Value of TEs (ms).
                flag: -TE %s
                mutually_exclusive: te_file
        ten_type: ('lower-tri' or 'diag-off-diag', nipype default value:
                 lower-tri)
                Use lower triangular (tenmap2) or diagonal, off-diagonal tensor
                format
        tenmap2_file: (a file name)
                Filename of tensor map [lower tri]
                flag: -tenmap2 %s
                requires: dti_flag
        tenmap_file: (a file name)
                Filename of tensor map [diag,offdiag].
                flag: -tenmap %s
                requires: dti_flag
        terminal_output: ('stream' or 'allatonce' or 'file' or 'none')
                Control terminal output: `stream` - displays to terminal immediately
                (default), `allatonce` - waits till command is finished to display
                output, `file` - writes output to file, `none` - output is ignored
        v1map_file: (a file name)
                Filename of PDD map [x,y,z]
                flag: -v1map %s
        vb_flag: (a boolean)
                Use Variational Bayes fitting with known prior (currently identity
                covariance...).
                flag: -vb
        voxel: (a tuple of the form: (an integer (int or long), an integer
                 (int or long), an integer (int or long)))
                Fit to single voxel only.
                flag: -voxel %d %d %d
        wls_flag: (a boolean)
                Use Variational Bayes fitting with known prior (currently identity
                covariance...).
                flag: -wls
                mutually_exclusive: gn_flag
        wm_t2_val: (a float)
                White matter T2 value [80ms].
                flag: -wmT2 %f

Outputs::

        error_file: (a file name)
                Filename of parameter error maps
        famap_file: (a file name)
                Filename of FA map
        mcmap_file: (a file name)
                Filename of multi-compartment model parameter map
                (-ivim,-ball,-nod).
        mcout: (a file name)
                Filename of mc samples (ascii text file)
        mdmap_file: (a file name)
                Filename of MD map/ADC
        nodiff_file: (a file name)
                Filename of average no diffusion image.
        res_file: (a file name)
                Filename of model residual map
        rgbmap_file: (a file name)
                Filename of colour FA map
        syn_file: (a file name)
                Filename of synthetic image
        tenmap2_file: (a file name)
                Filename of tensor map [lower tri]
        tenmap_file: (a file name)
                Filename of tensor map
        v1map_file: (a file name)
                Filename of PDD map [x,y,z]
