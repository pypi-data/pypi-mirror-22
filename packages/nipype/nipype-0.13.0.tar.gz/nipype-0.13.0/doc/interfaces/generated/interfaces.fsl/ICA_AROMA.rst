.. AUTO-GENERATED FILE -- DO NOT EDIT!

interfaces.fsl.ICA_AROMA
========================


.. _nipype.interfaces.fsl.ICA_AROMA.ICA_AROMA:


.. index:: ICA_AROMA

ICA_AROMA
---------

`Link to code <http://github.com/nipy/nipype/tree/ec86b7476/nipype/interfaces/fsl/ICA_AROMA.py#L77>`__

Wraps command **ICA_AROMA.py**

Interface for the ICA_AROMA.py script.

ICA-AROMA (i.e. 'ICA-based Automatic Removal Of Motion Artifacts') concerns
a data-driven method to identify and remove motion-related independent
components from fMRI data. To that end it exploits a small, but robust
set of theoretically motivated features, preventing the need for classifier
re-training and therefore providing direct and easy applicability.

See link for further documentation: https://github.com/rhr-pruim/ICA-AROMA

Example
~~~~~~~

>>> from nipype.interfaces.fsl import ICA_AROMA
>>> from nipype.testing import example_data
>>> AROMA_obj = ICA_AROMA.ICA_AROMA()
>>> AROMA_obj.inputs.in_file = 'functional.nii'
>>> AROMA_obj.inputs.mat_file = 'func_to_struct.mat'
>>> AROMA_obj.inputs.fnirt_warp_file = 'warpfield.nii'
>>> AROMA_obj.inputs.motion_parameters = 'fsl_mcflirt_movpar.txt'
>>> AROMA_obj.inputs.mask = 'mask.nii.gz'
>>> AROMA_obj.inputs.denoise_type = 'both'
>>> AROMA_obj.inputs.out_dir = 'ICA_testout'
>>> AROMA_obj.cmdline # doctest: +ALLOW_UNICODE
'ICA_AROMA.py -den both -warp warpfield.nii -i functional.nii -m mask.nii.gz -affmat func_to_struct.mat -mc fsl_mcflirt_movpar.txt -o ICA_testout'

Inputs::

        [Mandatory]
        denoise_type: ('nonaggr' or 'aggr' or 'both' or 'no', nipype default
                 value: nonaggr)
                Type of denoising strategy:
                -none: only classification, no denoising
                -nonaggr (default): non-aggresssive denoising, i.e. partial
                component regression
                -aggr: aggressive denoising, i.e. full component regression
                -both: both aggressive and non-aggressive denoising (two outputs)
                flag: -den %s
        feat_dir: (an existing directory name)
                If a feat directory exists and temporal filtering has not been run
                yet, ICA_AROMA can use the files in this directory.
                flag: -feat %s
                mutually_exclusive: in_file, mat_file, fnirt_warp_file,
                 motion_parameters
        in_file: (an existing file name)
                volume to be denoised
                flag: -i %s
                mutually_exclusive: feat_dir
        motion_parameters: (an existing file name)
                motion parameters file
                flag: -mc %s
                mutually_exclusive: feat_dir
        out_dir: (a directory name)
                output directory
                flag: -o %s

        [Optional]
        TR: (a float)
                TR in seconds. If this is not specified the TR will be extracted
                from the header of the fMRI nifti file.
                flag: -tr %.3f
        args: (a unicode string)
                Additional parameters to the command
                flag: %s
        dim: (an integer (int or long))
                Dimensionality reduction when running MELODIC (defualt is automatic
                estimation)
                flag: -dim %d
        environ: (a dictionary with keys which are a bytes or None or a value
                 of class 'str' and with values which are a bytes or None or a value
                 of class 'str', nipype default value: {})
                Environment variables
        fnirt_warp_file: (an existing file name)
                File name of the warp-file describing the non-linear registration
                (e.g. FSL FNIRT) of the structural data to MNI152 space (.nii.gz)
                flag: -warp %s
                mutually_exclusive: feat_dir
        ignore_exception: (a boolean, nipype default value: False)
                Print an error message instead of throwing an exception in case the
                interface fails to run
        mask: (an existing file name)
                path/name volume mask
                flag: -m %s
                mutually_exclusive: feat_dir
        mat_file: (an existing file name)
                path/name of the mat-file describing the affine registration (e.g.
                FSL FLIRT) of the functional data to structural space (.mat file)
                flag: -affmat %s
                mutually_exclusive: feat_dir
        melodic_dir: (an existing directory name)
                path to MELODIC directory if MELODIC has already been run
                flag: -meldir %s
        terminal_output: ('stream' or 'allatonce' or 'file' or 'none')
                Control terminal output: `stream` - displays to terminal immediately
                (default), `allatonce` - waits till command is finished to display
                output, `file` - writes output to file, `none` - output is ignored

Outputs::

        aggr_denoised_file: (an existing file name)
                if generated: aggressively denoised volume
        nonaggr_denoised_file: (an existing file name)
                if generated: non aggressively denoised volume
        out_dir: (an existing directory name)
                directory contains (in addition to the denoised files): melodic.ica
                + classified_motion_components + classification_overview +
                feature_scores + melodic_ic_mni)
