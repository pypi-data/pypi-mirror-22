.. AUTO-GENERATED FILE -- DO NOT EDIT!

interfaces.petpvc
=================


.. _nipype.interfaces.petpvc.PETPVC:


.. index:: PETPVC

PETPVC
------

`Link to code <http://github.com/nipy/nipype/tree/ec86b7476/nipype/interfaces/petpvc.py#L61>`__

Wraps command **petpvc**

Use PETPVC for partial volume correction of PET images.

PETPVC is a software from the Nuclear Medicine Department
of the UCL University Hospital, London, UK.

Its source code is here: https://github.com/UCL/PETPVC

The methods that it implement are explained here:
K. Erlandsson, I. Buvat, P. H. Pretorius, B. A. Thomas, and B. F. Hutton,
"A review of partial volume correction techniques for emission tomography
and their applications in neurology, cardiology and oncology," Phys. Med.
Biol., vol. 57, no. 21, p. R119, 2012.

Its command line help shows this:

   -i --input < filename >
      = PET image file
   -o --output < filename >
      = Output file
   [ -m --mask < filename > ]
      = Mask image file
   -p --pvc < keyword >
      = Desired PVC method
   -x < X >
      = The full-width at half maximum in mm along x-axis
   -y < Y >
      = The full-width at half maximum in mm along y-axis
   -z < Z >
      = The full-width at half maximum in mm along z-axis
   [ -d --debug ]
      = Prints debug information
   [ -n --iter [ Val ] ]
      = Number of iterations
        With: Val (Default = 10)
   [ -k [ Val ] ]
      = Number of deconvolution iterations
        With: Val (Default = 10)
   [ -a --alpha [ aval ] ]
      = Alpha value
        With: aval (Default = 1.5)
   [ -s --stop [ stopval ] ]
      = Stopping criterion
        With: stopval (Default = 0.01)

Technique - keyword
~~~~~~~~~~~~~~~~~~~
- Geometric transfer matrix - "GTM"
- Labbe approach - "LABBE"
- Richardson-Lucy - "RL"
- Van-Cittert - "VC"
- Region-based voxel-wise correction - "RBV"
- RBV with Labbe - "LABBE+RBV"
- RBV with Van-Cittert - "RBV+VC"
- RBV with Richardson-Lucy - "RBV+RL"
- RBV with Labbe and Van-Cittert - "LABBE+RBV+VC"
- RBV with Labbe and Richardson-Lucy- "LABBE+RBV+RL"
- Multi-target correction - "MTC"
- MTC with Labbe - "LABBE+MTC"
- MTC with Van-Cittert - "MTC+VC"
- MTC with Richardson-Lucy - "MTC+RL"
- MTC with Labbe and Van-Cittert - "LABBE+MTC+VC"
- MTC with Labbe and Richardson-Lucy- "LABBE+MTC+RL"
- Iterative Yang - "IY"
- Iterative Yang with Van-Cittert - "IY+VC"
- Iterative Yang with Richardson-Lucy - "IY+RL"
- Muller Gartner - "MG"
- Muller Gartner with Van-Cittert - "MG+VC"
- Muller Gartner with Richardson-Lucy - "MG+RL"

Examples
~~~~~~~~
>>> from ..testing import example_data
>>> #TODO get data for PETPVC
>>> pvc = PETPVC()
>>> pvc.inputs.in_file   = 'pet.nii.gz'
>>> pvc.inputs.mask_file = 'tissues.nii.gz'
>>> pvc.inputs.out_file  = 'pet_pvc_rbv.nii.gz'
>>> pvc.inputs.pvc = 'RBV'
>>> pvc.inputs.fwhm_x = 2.0
>>> pvc.inputs.fwhm_y = 2.0
>>> pvc.inputs.fwhm_z = 2.0
>>> outs = pvc.run() #doctest: +SKIP

Inputs::

        [Mandatory]
        fwhm_x: (a float)
                The full-width at half maximum in mm along x-axis
                flag: -x %.4f
        fwhm_y: (a float)
                The full-width at half maximum in mm along y-axis
                flag: -y %.4f
        fwhm_z: (a float)
                The full-width at half maximum in mm along z-axis
                flag: -z %.4f
        in_file: (an existing file name)
                PET image file
                flag: -i %s
        mask_file: (an existing file name)
                Mask image file
                flag: -m %s
        pvc: ('GTM' or 'IY' or 'IY+RL' or 'IY+VC' or 'LABBE' or 'LABBE+MTC'
                 or 'LABBE+MTC+RL' or 'LABBE+MTC+VC' or 'LABBE+RBV' or
                 'LABBE+RBV+RL' or 'LABBE+RBV+VC' or 'MG' or 'MG+RL' or 'MG+VC' or
                 'MTC' or 'MTC+RL' or 'MTC+VC' or 'RBV' or 'RBV+RL' or 'RBV+VC' or
                 'RL' or 'VC')
                Desired PVC method
                flag: -p %s

        [Optional]
        alpha: (a float)
                Alpha value
                flag: -a %.4f
        args: (a unicode string)
                Additional parameters to the command
                flag: %s
        debug: (a boolean, nipype default value: False)
                Prints debug information
                flag: -d
        environ: (a dictionary with keys which are a bytes or None or a value
                 of class 'str' and with values which are a bytes or None or a value
                 of class 'str', nipype default value: {})
                Environment variables
        ignore_exception: (a boolean, nipype default value: False)
                Print an error message instead of throwing an exception in case the
                interface fails to run
        n_deconv: (an integer (int or long))
                Number of deconvolution iterations
                flag: -k %d
        n_iter: (an integer (int or long))
                Number of iterations
                flag: -n %d
        out_file: (a file name)
                Output file
                flag: -o %s
        stop_crit: (a float)
                Stopping criterion
                flag: -a %.4f
        terminal_output: ('stream' or 'allatonce' or 'file' or 'none')
                Control terminal output: `stream` - displays to terminal immediately
                (default), `allatonce` - waits till command is finished to display
                output, `file` - writes output to file, `none` - output is ignored

Outputs::

        out_file: (a file name)
                Output file

References::
None
