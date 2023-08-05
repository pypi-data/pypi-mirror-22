.. AUTO-GENERATED FILE -- DO NOT EDIT!

interfaces.niftyfit.qt1
=======================


.. _nipype.interfaces.niftyfit.qt1.FitQt1:


.. index:: FitQt1

FitQt1
------

`Link to code <http://github.com/nipy/nipype/tree/ec86b7476/nipype/interfaces/niftyfit/qt1.py#L152>`__

Wraps command **fit_qt1**

Interface for executable fit_qt1 from Niftyfit platform.

Use NiftyFit to perform Qt1 fitting.

T1 Fitting Routine (To inversion recovery or spgr data).
Fits single component T1 maps in the first instance.

`Source code <https://cmiclab.cs.ucl.ac.uk/CMIC/NiftyFit-Release>`_

Examples
~~~~~~~~

>>> from nipype.interfaces.niftyfit import FitQt1
>>> fit_qt1 = FitQt1()
>>> fit_qt1.inputs.source_file = 'TI4D.nii.gz'
>>> fit_qt1.cmdline  # doctest: +ALLOW_UNICODE
'fit_qt1 -source TI4D.nii.gz -comp TI4D_comp.nii.gz -error TI4D_error.nii.gz -m0map TI4D_m0map.nii.gz -mcmap TI4D_mcmap.nii.gz -res TI4D_res.nii.gz -syn TI4D_syn.nii.gz -t1map TI4D_t1map.nii.gz'

Inputs::

        [Mandatory]
        source_file: (an existing file name)
                Filename of the 4D Multi-Echo T1 source image.
                flag: -source %s, position: 1

        [Optional]
        acceptance: (a float)
                Fraction of iterations to accept [0.23].
                flag: -acceptance %f
        args: (a unicode string)
                Additional parameters to the command
                flag: %s
        b1map: (a file name)
                Filename of B1 estimate for fitting (or include in prior).
                flag: -b1map %s
        comp_file: (a file name)
                Filename of the estimated multi-component T1 map.
                flag: -comp %s
        environ: (a dictionary with keys which are a bytes or None or a value
                 of class 'str' and with values which are a bytes or None or a value
                 of class 'str', nipype default value: {})
                Environment variables
        error_file: (a file name)
                Filename of the error map (symmetric matrix, [Diag,OffDiag]).
                flag: -error %s
        flips: (a list of items which are a float)
                Flip angles
                flag: -flips %s
        flips_list: (a file name)
                Filename of list of pre-defined flip angles (deg).
                flag: -fliplist %s
        gn_flag: (a boolean)
                Use Gauss-Newton algorithm [Levenberg-Marquardt].
                flag: -gn, position: 8
        ignore_exception: (a boolean, nipype default value: False)
                Print an error message instead of throwing an exception in case the
                interface fails to run
        ir_flag: (a boolean)
                Inversion Recovery fitting [default].
                flag: -IR, position: 13
        lm_val: (a tuple of the form: (a float, a float))
                Set LM parameters (initial value, decrease rate) [100,1.2].
                flag: -lm %f %f, position: 7
        m0map_file: (a file name)
                Filename of the estimated input M0 map.
                flag: -m0map %s
        mask: (an existing file name)
                Filename of image mask.
                flag: -mask %s, position: 2
        maxit: (an integer (int or long))
                NLSQR iterations [100].
                flag: -maxit %d, position: 11
        mcmap_file: (a file name)
                Filename of the estimated output multi-parameter map.
                flag: -mcmap %s
        mcmaxit: (an integer (int or long))
                Number of iterations to run [10,000].
                flag: -mcmaxit %d
        mcout: (a file name)
                Filename of mc samples (ascii text file)
                flag: -mcout %s
        mcsamples: (an integer (int or long))
                Number of samples to keep [100].
                flag: -mcsamples %d
        nb_comp: (an integer (int or long))
                Number of components to fit [1] (currently IR/SR only)
                flag: -nc %d, position: 6
        prior: (an existing file name)
                Filename of parameter prior.
                flag: -prior %s, position: 3
        res_file: (a file name)
                Filename of the model fit residuals
                flag: -res %s
        slice_no: (an integer (int or long))
                Fit to single slice number.
                flag: -slice %d, position: 9
        spgr: (a boolean)
                Spoiled Gradient Echo fitting
                flag: -SPGR
        sr_flag: (a boolean)
                Saturation Recovery fitting [default].
                flag: -SR, position: 12
        syn_file: (a file name)
                Filename of the synthetic ASL data.
                flag: -syn %s
        t1_list: (a file name)
                Filename of list of pre-defined T1s
                flag: -T1list %s
        t1map_file: (a file name)
                Filename of the estimated output T1 map (in ms).
                flag: -t1map %s
        t1max: (a float)
                Maximum tissue T1 value [4000ms].
                flag: -T1max %f
        t1min: (a float)
                Minimum tissue T1 value [400ms].
                flag: -T1min %f
        te_value: (a float)
                TE Echo Time [0ms!].
                flag: -TE %f, position: 4
        terminal_output: ('stream' or 'allatonce' or 'file' or 'none')
                Control terminal output: `stream` - displays to terminal immediately
                (default), `allatonce` - waits till command is finished to display
                output, `file` - writes output to file, `none` - output is ignored
        tis: (a list of items which are a float)
                Inversion times for T1 data [1s,2s,5s].
                flag: -TIs %s, position: 14
        tis_list: (a file name)
                Filename of list of pre-defined TIs.
                flag: -TIlist %s
        tr_value: (a float)
                TR Repetition Time [10s!].
                flag: -TR %f, position: 5
        voxel: (a tuple of the form: (an integer (int or long), an integer
                 (int or long), an integer (int or long)))
                Fit to single voxel only.
                flag: -voxel %d %d %d, position: 10

Outputs::

        comp_file: (a file name)
                Filename of the estimated multi-component T1 map.
        error_file: (a file name)
                Filename of the error map (symmetric matrix, [Diag,OffDiag])
        m0map_file: (a file name)
                Filename of the m0 map
        mcmap_file: (a file name)
                Filename of the estimated output multi-parameter map
        res_file: (a file name)
                Filename of the model fit residuals
        syn_file: (a file name)
                Filename of the synthetic ASL data
        t1map_file: (a file name)
                Filename of the estimated output T1 map (in ms)
