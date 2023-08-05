.. AUTO-GENERATED FILE -- DO NOT EDIT!

interfaces.freesurfer.longitudinal
==================================


.. _nipype.interfaces.freesurfer.longitudinal.FuseSegmentations:


.. index:: FuseSegmentations

FuseSegmentations
-----------------

`Link to code <http://github.com/nipy/nipype/tree/ec86b7476/nipype/interfaces/freesurfer/longitudinal.py#L157>`__

Wraps command **mri_fuse_segmentations**

fuse segmentations together from multiple timepoints

Examples
~~~~~~~~
>>> from nipype.interfaces.freesurfer import FuseSegmentations
>>> fuse = FuseSegmentations()
>>> fuse.inputs.subject_id = 'tp.long.A.template'
>>> fuse.inputs.timepoints = ['tp1', 'tp2']
>>> fuse.inputs.out_file = 'aseg.fused.mgz'
>>> fuse.inputs.in_segmentations = ['aseg.mgz', 'aseg.mgz']
>>> fuse.inputs.in_segmentations_noCC = ['aseg.mgz', 'aseg.mgz']
>>> fuse.inputs.in_norms = ['norm.mgz', 'norm.mgz', 'norm.mgz']
>>> fuse.cmdline # doctest: +ALLOW_UNICODE
'mri_fuse_segmentations -n norm.mgz -a aseg.mgz -c aseg.mgz tp.long.A.template tp1 tp2'

Inputs::

        [Mandatory]
        in_norms: (a list of items which are an existing file name)
                -n <filename> - name of norm file to use (default: norm.mgs) must
                include the corresponding norm file for all given timepoints as well
                as for the current subject
                flag: -n %s
        in_segmentations: (a list of items which are an existing file name)
                name of aseg file to use (default: aseg.mgz) must include the aseg
                files for all the given timepoints
                flag: -a %s
        in_segmentations_noCC: (a list of items which are an existing file
                 name)
                name of aseg file w/o CC labels (default: aseg.auto_noCCseg.mgz)
                must include the corresponding file for all the given timepoints
                flag: -c %s
        out_file: (a file name)
                output fused segmentation file
        timepoints: (a list of items which are a string)
                subject_ids or timepoints to be processed
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
        subject_id: (a string)
                subject_id being processed
                flag: %s, position: -3
        subjects_dir: (an existing directory name)
                subjects directory
        terminal_output: ('stream' or 'allatonce' or 'file' or 'none')
                Control terminal output: `stream` - displays to terminal immediately
                (default), `allatonce` - waits till command is finished to display
                output, `file` - writes output to file, `none` - output is ignored

Outputs::

        out_file: (a file name)
                output fused segmentation file

.. _nipype.interfaces.freesurfer.longitudinal.RobustTemplate:


.. index:: RobustTemplate

RobustTemplate
--------------

`Link to code <http://github.com/nipy/nipype/tree/ec86b7476/nipype/interfaces/freesurfer/longitudinal.py#L75>`__

Wraps command **mri_robust_template**

construct an unbiased robust template for longitudinal volumes

Examples
~~~~~~~~
>>> from nipype.interfaces.freesurfer import RobustTemplate
>>> template = RobustTemplate()
>>> template.inputs.in_files = ['structural.nii', 'functional.nii']
>>> template.inputs.auto_detect_sensitivity = True
>>> template.inputs.average_metric = 'mean'
>>> template.inputs.initial_timepoint = 1
>>> template.inputs.fixed_timepoint = True
>>> template.inputs.no_iteration = True
>>> template.inputs.subsample_threshold = 200
>>> template.cmdline  #doctest: +NORMALIZE_WHITESPACE +ALLOW_UNICODE
'mri_robust_template --satit --average 0 --fixtp --mov structural.nii functional.nii --inittp 1 --noit --template mri_robust_template_out.mgz --subsample 200'
>>> template.inputs.out_file = 'T1.nii'
>>> template.cmdline  #doctest: +NORMALIZE_WHITESPACE +ALLOW_UNICODE
'mri_robust_template --satit --average 0 --fixtp --mov structural.nii functional.nii --inittp 1 --noit --template T1.nii --subsample 200'

>>> template.inputs.transform_outputs = ['structural.lta', 'functional.lta']
>>> template.inputs.scaled_intensity_outputs = ['structural-iscale.txt', 'functional-iscale.txt']
>>> template.cmdline    #doctest: +NORMALIZE_WHITESPACE +ALLOW_UNICODE
'mri_robust_template --satit --average 0 --fixtp --mov structural.nii functional.nii --inittp 1 --noit --template T1.nii --iscaleout structural-iscale.txt functional-iscale.txt --subsample 200 --lta structural.lta functional.lta'

>>> template.run()  #doctest: +SKIP

References
~~~~~~~~~~
[https://surfer.nmr.mgh.harvard.edu/fswiki/mri_robust_template]

Inputs::

        [Mandatory]
        auto_detect_sensitivity: (a boolean)
                auto-detect good sensitivity (recommended for head or full brain
                scans)
                flag: --satit
                mutually_exclusive: outlier_sensitivity
        in_files: (a list of items which are an existing file name)
                input movable volumes to be aligned to common mean/median template
                flag: --mov %s
        out_file: (a file name, nipype default value:
                 mri_robust_template_out.mgz)
                output template volume (final mean/median image)
                flag: --template %s
        outlier_sensitivity: (a float)
                set outlier sensitivity manually (e.g. "--sat 4.685" ). Higher
                values mean less sensitivity.
                flag: --sat %.4f
                mutually_exclusive: auto_detect_sensitivity

        [Optional]
        args: (a unicode string)
                Additional parameters to the command
                flag: %s
        average_metric: ('median' or 'mean')
                construct template from: 0 Mean, 1 Median (default)
                flag: --average %d
        environ: (a dictionary with keys which are a bytes or None or a value
                 of class 'str' and with values which are a bytes or None or a value
                 of class 'str', nipype default value: {})
                Environment variables
        fixed_timepoint: (a boolean)
                map everthing to init TP# (init TP is not resampled)
                flag: --fixtp
        ignore_exception: (a boolean, nipype default value: False)
                Print an error message instead of throwing an exception in case the
                interface fails to run
        in_intensity_scales: (a list of items which are an existing file
                 name)
                use initial intensity scales
                flag: --iscalein %s
        initial_timepoint: (an integer (int or long))
                use TP# for spacial init (default random), 0: no init
                flag: --inittp %d
        initial_transforms: (a list of items which are an existing file name)
                use initial transforms (lta) on source
                flag: --ixforms %s
        intensity_scaling: (a boolean)
                allow also intensity scaling (default off)
                flag: --iscale
        no_iteration: (a boolean)
                do not iterate, just create first template
                flag: --noit
        scaled_intensity_outputs: (a list of items which are a file name)
                final intensity scales (will activate --iscale)
                flag: --iscaleout %s
        subjects_dir: (an existing directory name)
                subjects directory
        subsample_threshold: (an integer (int or long))
                subsample if dim > # on all axes (default no subs.)
                flag: --subsample %d
        terminal_output: ('stream' or 'allatonce' or 'file' or 'none')
                Control terminal output: `stream` - displays to terminal immediately
                (default), `allatonce` - waits till command is finished to display
                output, `file` - writes output to file, `none` - output is ignored
        transform_outputs: (a list of items which are a file name)
                output xforms to template (for each input)
                flag: --lta %s

Outputs::

        out_file: (an existing file name)
                output template volume (final mean/median image)
        scaled_intensity_outputs: (a list of items which are an existing file
                 name)
                output final intensity scales
        transform_outputs: (a list of items which are an existing file name)
                output xform files from moving to template
