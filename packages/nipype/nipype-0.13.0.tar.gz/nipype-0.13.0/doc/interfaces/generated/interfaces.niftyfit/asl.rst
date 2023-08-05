.. AUTO-GENERATED FILE -- DO NOT EDIT!

interfaces.niftyfit.asl
=======================


.. _nipype.interfaces.niftyfit.asl.FitAsl:


.. index:: FitAsl

FitAsl
------

`Link to code <http://github.com/nipy/nipype/tree/ec86b7476/nipype/interfaces/niftyfit/asl.py#L135>`__

Wraps command **fit_asl**

Interface for executable fit_asl from Niftyfit platform.

Use NiftyFit to perform ASL fitting.

ASL fitting routines (following EU Cost Action White Paper recommendations)
Fits Cerebral Blood Flow maps in the first instance.

`Source code <https://cmiclab.cs.ucl.ac.uk/CMIC/NiftyFit-Release>`_

Examples
~~~~~~~~
>>> from nipype.interfaces import niftyfit
>>> node = niftyfit.FitAsl()
>>> node.inputs.source_file = 'asl.nii.gz'
>>> node.cmdline    # doctest: +ALLOW_UNICODE
'fit_asl -source asl.nii.gz -cbf asl_cbf.nii.gz -error asl_error.nii.gz -syn asl_syn.nii.gz'

Inputs::

        [Mandatory]
        source_file: (a file name)
                Filename of the 4D ASL (control/label) source image (mandatory).
                flag: -source %s, position: 1

        [Optional]
        args: (a unicode string)
                Additional parameters to the command
                flag: %s
        cbf_file: (a file name)
                Filename of the Cerebral Blood Flow map (in ml/100g/min).
                flag: -cbf %s
        dpld: (a float)
                Difference in labelling delay per slice [0.0 ms/slice.
                flag: -dPLD %f
        dt_inv2: (a float)
                Difference in inversion time per slice [0ms/slice].
                flag: -dTinv2 %f
        eff: (a float)
                Labelling efficiency [0.99 (pasl), 0.85 (pcasl)], ensure any
                background suppression pulses are included in -eff
                flag: -eff %f
        environ: (a dictionary with keys which are a bytes or None or a value
                 of class 'str' and with values which are a bytes or None or a value
                 of class 'str', nipype default value: {})
                Environment variables
        error_file: (a file name)
                Filename of the CBF error map.
                flag: -error %s
        gm_plasma: (a float)
                Plasma/GM water partition [0.95ml/g].
                flag: -gmL %f
        gm_t1: (a float)
                T1 of GM [1150ms].
                flag: -gmT1 %f
        gm_ttt: (a float)
                Time to GM [ATT+0ms].
                flag: -gmTTT %f
        ignore_exception: (a boolean, nipype default value: False)
                Print an error message instead of throwing an exception in case the
                interface fails to run
        ir_output: (a file name)
                Output of [1,2,5]s Inversion Recovery fitting.
                flag: -IRoutput %s
        ir_volume: (a file name)
                Filename of a [1,2,5]s Inversion Recovery volume (T1/M0 fitting
                carried out internally).
                flag: -IRvolume %s
        ldd: (a float)
                Labelling Duration [1800ms].
                flag: -LDD %f
        m0map: (a file name)
                Filename of the estimated input M0 map.
                flag: -m0map %s
        m0mape: (a file name)
                Filename of the estimated input M0 map error.
                flag: -m0mape %s
        mask: (a file name)
                Filename of image mask.
                flag: -mask %s, position: 2
        mul: (a float)
                Multiply CBF by this value (e.g. if CL are mislabelled use -1.0).
                flag: -mul %f
        mulgm: (a boolean)
                Multiply CBF by segmentation [Off].
                flag: -sig
        out: (a float)
                Outlier rejection for multi CL volumes (enter z-score threshold
                (e.g. 2.5)) [off].
                flag: -out %f
        pasl: (a boolean)
                Fit PASL ASL data [default]
                flag: -pasl
        pcasl: (a boolean)
                Fit PCASL ASL data
                flag: -pcasl
        plasma_coeff: (a float)
                Single plasma/tissue partition coefficient [0.9ml/g].
                flag: -L %f
        pld: (a float)
                Post Labelling Delay [2000ms].
                flag: -PLD %f
        pv0: (an integer (int or long))
                Simple PV correction (CBF=vg*CBFg + vw*CBFw, with CBFw=f*CBFg)
                [0.25].
                flag: -pv0 %d
        pv2: (an integer (int or long))
                In plane PV kernel size [3x3].
                flag: -pv2 %d
        pv3: (a tuple of the form: (an integer (int or long), an integer (int
                 or long), an integer (int or long)))
                3D kernel size [3x3x1].
                flag: -pv3 %d %d %d
        pv_threshold: (a boolean)
                Set PV threshold for switching off LSQR [O.05].
                flag: -pvthreshold
        seg: (a file name)
                Filename of the 4D segmentation (in ASL space) for L/T1 estimation
                and PV correction {WM,GM,CSF}.
                flag: -seg %s
        segstyle: (a boolean)
                Set CBF as [gm,wm] not [wm,gm].
                flag: -segstyle
        sig: (a boolean)
                Use sigmoid to estimate L from T1: L(T1|gmL,wmL) [Off].
                flag: -sig
        syn_file: (a file name)
                Filename of the synthetic ASL data.
                flag: -syn %s
        t1_art_cmp: (a float)
                T1 of arterial component [1650ms].
                flag: -T1a %f
        t1map: (a file name)
                Filename of the estimated input T1 map (in ms).
                flag: -t1map %s
        t_inv1: (a float)
                Saturation pulse time [800ms].
                flag: -Tinv1 %f
        t_inv2: (a float)
                Inversion time [2000ms].
                flag: -Tinv2 %f
        terminal_output: ('stream' or 'allatonce' or 'file' or 'none')
                Control terminal output: `stream` - displays to terminal immediately
                (default), `allatonce` - waits till command is finished to display
                output, `file` - writes output to file, `none` - output is ignored
        wm_plasma: (a float)
                Plasma/WM water partition [0.82ml/g].
                flag: -wmL %f
        wm_t1: (a float)
                T1 of WM [800ms].
                flag: -wmT1 %f
        wm_ttt: (a float)
                Time to WM [ATT+0ms].
                flag: -wmTTT %f

Outputs::

        cbf_file: (a file name)
                Filename of the Cerebral Blood Flow map (in ml/100g/min).
        error_file: (a file name)
                Filename of the CBF error map.
        syn_file: (a file name)
                Filename of the synthetic ASL data.
