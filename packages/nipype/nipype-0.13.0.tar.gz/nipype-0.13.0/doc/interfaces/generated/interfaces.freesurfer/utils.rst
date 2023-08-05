.. AUTO-GENERATED FILE -- DO NOT EDIT!

interfaces.freesurfer.utils
===========================


.. _nipype.interfaces.freesurfer.utils.AddXFormToHeader:


.. index:: AddXFormToHeader

AddXFormToHeader
----------------

`Link to code <http://github.com/nipy/nipype/tree/ec86b7476/nipype/interfaces/freesurfer/utils.py#L1452>`__

Wraps command **mri_add_xform_to_header**

Just adds specified xform to the volume header

(!) WARNING: transform input **MUST** be an absolute path to a DataSink'ed transform or
the output will reference a transform in the workflow cache directory!

>>> from nipype.interfaces.freesurfer import AddXFormToHeader
>>> adder = AddXFormToHeader()
>>> adder.inputs.in_file = 'norm.mgz'
>>> adder.inputs.transform = 'trans.mat'
>>> adder.cmdline # doctest: +ALLOW_UNICODE
'mri_add_xform_to_header trans.mat norm.mgz output.mgz'

>>> adder.inputs.copy_name = True
>>> adder.cmdline # doctest: +ALLOW_UNICODE
'mri_add_xform_to_header -c trans.mat norm.mgz output.mgz'

>>> adder.run()   # doctest: +SKIP

References:
~~~~~~~~~~
[https://surfer.nmr.mgh.harvard.edu/fswiki/mri_add_xform_to_header]

Inputs::

        [Mandatory]
        in_file: (an existing file name)
                input volume
                flag: %s, position: -2
        transform: (a file name)
                xfm file
                flag: %s, position: -3

        [Optional]
        args: (a unicode string)
                Additional parameters to the command
                flag: %s
        copy_name: (a boolean)
                do not try to load the xfmfile, just copy name
                flag: -c
        environ: (a dictionary with keys which are a bytes or None or a value
                 of class 'str' and with values which are a bytes or None or a value
                 of class 'str', nipype default value: {})
                Environment variables
        ignore_exception: (a boolean, nipype default value: False)
                Print an error message instead of throwing an exception in case the
                interface fails to run
        out_file: (a file name, nipype default value: output.mgz)
                output volume
                flag: %s, position: -1
        subjects_dir: (an existing directory name)
                subjects directory
        terminal_output: ('stream' or 'allatonce' or 'file' or 'none')
                Control terminal output: `stream` - displays to terminal immediately
                (default), `allatonce` - waits till command is finished to display
                output, `file` - writes output to file, `none` - output is ignored
        verbose: (a boolean)
                be verbose
                flag: -v

Outputs::

        out_file: (an existing file name)
                output volume

.. _nipype.interfaces.freesurfer.utils.Aparc2Aseg:


.. index:: Aparc2Aseg

Aparc2Aseg
----------

`Link to code <http://github.com/nipy/nipype/tree/ec86b7476/nipype/interfaces/freesurfer/utils.py#L2865>`__

Wraps command **mri_aparc2aseg**

Maps the cortical labels from the automatic cortical parcellation
(aparc) to the automatic segmentation volume (aseg). The result can be
used as the aseg would. The algorithm is to find each aseg voxel
labeled as cortex (3 and 42) and assign it the label of the closest
cortical vertex. If the voxel is not in the ribbon (as defined by mri/
lh.ribbon and rh.ribbon), then the voxel is marked as unknown (0).
This can be turned off with --noribbon. The cortical parcellation is
obtained from subject/label/hemi.aparc.annot which should be based on
the curvature.buckner40.filled.desikan_killiany.gcs atlas. The aseg is
obtained from subject/mri/aseg.mgz and should be based on the
RB40_talairach_2005-07-20.gca atlas. If these atlases are used, then the
segmentations can be viewed with tkmedit and the
FreeSurferColorLUT.txt color table found in $FREESURFER_HOME. These
are the default atlases used by recon-all.

Examples
~~~~~~~~
>>> from nipype.interfaces.freesurfer import Aparc2Aseg
>>> aparc2aseg = Aparc2Aseg()
>>> aparc2aseg.inputs.lh_white = 'lh.pial'
>>> aparc2aseg.inputs.rh_white = 'lh.pial'
>>> aparc2aseg.inputs.lh_pial = 'lh.pial'
>>> aparc2aseg.inputs.rh_pial = 'lh.pial'
>>> aparc2aseg.inputs.lh_ribbon = 'label.mgz'
>>> aparc2aseg.inputs.rh_ribbon = 'label.mgz'
>>> aparc2aseg.inputs.ribbon = 'label.mgz'
>>> aparc2aseg.inputs.lh_annotation = 'lh.pial'
>>> aparc2aseg.inputs.rh_annotation = 'lh.pial'
>>> aparc2aseg.inputs.out_file = 'aparc+aseg.mgz'
>>> aparc2aseg.inputs.label_wm = True
>>> aparc2aseg.inputs.rip_unknown = True
>>> aparc2aseg.cmdline # doctest: +SKIP
'mri_aparc2aseg --labelwm  --o aparc+aseg.mgz --rip-unknown --s subject_id'

Inputs::

        [Mandatory]
        lh_annotation: (an existing file name)
                Input file must be <subject_id>/label/lh.aparc.annot
        lh_pial: (an existing file name)
                Input file must be <subject_id>/surf/lh.pial
        lh_ribbon: (an existing file name)
                Input file must be <subject_id>/mri/lh.ribbon.mgz
        lh_white: (an existing file name)
                Input file must be <subject_id>/surf/lh.white
        out_file: (a file name)
                Full path of file to save the output segmentation in
                flag: --o %s
        rh_annotation: (an existing file name)
                Input file must be <subject_id>/label/rh.aparc.annot
        rh_pial: (an existing file name)
                Input file must be <subject_id>/surf/rh.pial
        rh_ribbon: (an existing file name)
                Input file must be <subject_id>/mri/rh.ribbon.mgz
        rh_white: (an existing file name)
                Input file must be <subject_id>/surf/rh.white
        ribbon: (an existing file name)
                Input file must be <subject_id>/mri/ribbon.mgz
        subject_id: (a string, nipype default value: subject_id)
                Subject being processed
                flag: --s %s

        [Optional]
        a2009s: (a boolean)
                Using the a2009s atlas
                flag: --a2009s
        args: (a unicode string)
                Additional parameters to the command
                flag: %s
        aseg: (an existing file name)
                Input aseg file
                flag: --aseg %s
        copy_inputs: (a boolean)
                If running as a node, set this to True.This will copy the input
                files to the node directory.
        ctxseg: (an existing file name)
                flag: --ctxseg %s
        environ: (a dictionary with keys which are a bytes or None or a value
                 of class 'str' and with values which are a bytes or None or a value
                 of class 'str', nipype default value: {})
                Environment variables
        filled: (an existing file name)
                Implicit input filled file. Only required with FS v5.3.
        hypo_wm: (a boolean)
                Label hypointensities as WM
                flag: --hypo-as-wm
        ignore_exception: (a boolean, nipype default value: False)
                Print an error message instead of throwing an exception in case the
                interface fails to run
        label_wm: (a boolean)
                 For each voxel labeled as white matter in the aseg, re-assign
                 its label to be that of the closest cortical point if its
                 distance is less than dmaxctx
                flag: --labelwm
        rip_unknown: (a boolean)
                Do not label WM based on 'unknown' corical label
                flag: --rip-unknown
        subjects_dir: (an existing directory name)
                subjects directory
        terminal_output: ('stream' or 'allatonce' or 'file' or 'none')
                Control terminal output: `stream` - displays to terminal immediately
                (default), `allatonce` - waits till command is finished to display
                output, `file` - writes output to file, `none` - output is ignored
        volmask: (a boolean)
                Volume mask flag
                flag: --volmask

Outputs::

        out_file: (a file name)
                Output aseg file
                flag: %s

.. _nipype.interfaces.freesurfer.utils.Apas2Aseg:


.. index:: Apas2Aseg

Apas2Aseg
---------

`Link to code <http://github.com/nipy/nipype/tree/ec86b7476/nipype/interfaces/freesurfer/utils.py#L2954>`__

Wraps command **apas2aseg**

Converts aparc+aseg.mgz into something like aseg.mgz by replacing the
cortical segmentations 1000-1035 with 3 and 2000-2035 with 42. The
advantage of this output is that the cortical label conforms to the
actual surface (this is not the case with aseg.mgz).

Examples
~~~~~~~~
>>> from nipype.interfaces.freesurfer import Apas2Aseg
>>> apas2aseg = Apas2Aseg()
>>> apas2aseg.inputs.in_file = 'aseg.mgz'
>>> apas2aseg.inputs.out_file = 'output.mgz'
>>> apas2aseg.cmdline # doctest: +ALLOW_UNICODE
'apas2aseg --i aseg.mgz --o output.mgz'

Inputs::

        [Mandatory]
        in_file: (an existing file name)
                Input aparc+aseg.mgz
                flag: --i %s
        out_file: (a file name)
                Output aseg file
                flag: --o %s

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
        subjects_dir: (an existing directory name)
                subjects directory
        terminal_output: ('stream' or 'allatonce' or 'file' or 'none')
                Control terminal output: `stream` - displays to terminal immediately
                (default), `allatonce` - waits till command is finished to display
                output, `file` - writes output to file, `none` - output is ignored

Outputs::

        out_file: (a file name)
                Output aseg file
                flag: %s

.. _nipype.interfaces.freesurfer.utils.ApplyMask:


.. index:: ApplyMask

ApplyMask
---------

`Link to code <http://github.com/nipy/nipype/tree/ec86b7476/nipype/interfaces/freesurfer/utils.py#L561>`__

Wraps command **mri_mask**

Use Freesurfer's mri_mask to apply a mask to an image.

The mask file need not be binarized; it can be thresholded above a given
value before application. It can also optionally be transformed into input
space with an LTA matrix.

Inputs::

        [Mandatory]
        in_file: (an existing file name)
                input image (will be masked)
                flag: %s, position: -3
        mask_file: (an existing file name)
                image defining mask space
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
        invert_xfm: (a boolean)
                invert transformation
                flag: -invert
        keep_mask_deletion_edits: (a boolean)
                transfer voxel-deletion edits (voxels=1) from mask to out vol
                flag: -keep_mask_deletion_edits
        mask_thresh: (a float)
                threshold mask before applying
                flag: -T %.4f
        out_file: (a file name)
                final image to write
                flag: %s, position: -1
        subjects_dir: (an existing directory name)
                subjects directory
        terminal_output: ('stream' or 'allatonce' or 'file' or 'none')
                Control terminal output: `stream` - displays to terminal immediately
                (default), `allatonce` - waits till command is finished to display
                output, `file` - writes output to file, `none` - output is ignored
        transfer: (an integer (int or long))
                transfer only voxel value # from mask to out
                flag: -transfer %d
        use_abs: (a boolean)
                take absolute value of mask before applying
                flag: -abs
        xfm_file: (an existing file name)
                LTA-format transformation matrix to align mask with input
                flag: -xform %s
        xfm_source: (an existing file name)
                image defining transform source space
                flag: -lta_src %s
        xfm_target: (an existing file name)
                image defining transform target space
                flag: -lta_dst %s

Outputs::

        out_file: (an existing file name)
                masked image

.. _nipype.interfaces.freesurfer.utils.CheckTalairachAlignment:


.. index:: CheckTalairachAlignment

CheckTalairachAlignment
-----------------------

`Link to code <http://github.com/nipy/nipype/tree/ec86b7476/nipype/interfaces/freesurfer/utils.py#L1508>`__

Wraps command **talairach_afd**

This program detects Talairach alignment failures

Examples
~~~~~~~~

>>> from nipype.interfaces.freesurfer import CheckTalairachAlignment
>>> checker = CheckTalairachAlignment()

>>> checker.inputs.in_file = 'trans.mat'
>>> checker.inputs.threshold = 0.005
>>> checker.cmdline # doctest: +ALLOW_UNICODE
'talairach_afd -T 0.005 -xfm trans.mat'

>>> checker.run() # doctest: +SKIP

Inputs::

        [Mandatory]
        in_file: (an existing file name)
                specify the talairach.xfm file to check
                flag: -xfm %s, position: -1
                mutually_exclusive: subject
        subject: (a string)
                specify subject's name
                flag: -subj %s, position: -1
                mutually_exclusive: in_file

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
        subjects_dir: (an existing directory name)
                subjects directory
        terminal_output: ('stream' or 'allatonce' or 'file' or 'none')
                Control terminal output: `stream` - displays to terminal immediately
                (default), `allatonce` - waits till command is finished to display
                output, `file` - writes output to file, `none` - output is ignored
        threshold: (a float)
                Talairach transforms for subjects with p-values <= T are considered
                as very unlikely default=0.010
                flag: -T %.3f

Outputs::

        out_file: (a file name)
                The input file for CheckTalairachAlignment

.. _nipype.interfaces.freesurfer.utils.Contrast:


.. index:: Contrast

Contrast
--------

`Link to code <http://github.com/nipy/nipype/tree/ec86b7476/nipype/interfaces/freesurfer/utils.py#L2705>`__

Wraps command **pctsurfcon**

Compute surface-wise gray/white contrast

Examples
~~~~~~~~
>>> from nipype.interfaces.freesurfer import Contrast
>>> contrast = Contrast()
>>> contrast.inputs.subject_id = '10335'
>>> contrast.inputs.hemisphere = 'lh'
>>> contrast.inputs.white = 'lh.white' # doctest: +SKIP
>>> contrast.inputs.thickness = 'lh.thickness' # doctest: +SKIP
>>> contrast.inputs.annotation = '../label/lh.aparc.annot' # doctest: +SKIP
>>> contrast.inputs.cortex = '../label/lh.cortex.label' # doctest: +SKIP
>>> contrast.inputs.rawavg = '../mri/rawavg.mgz' # doctest: +SKIP
>>> contrast.inputs.orig = '../mri/orig.mgz' # doctest: +SKIP
>>> contrast.cmdline # doctest: +SKIP
'pctsurfcon --lh-only --s 10335'

Inputs::

        [Mandatory]
        annotation: (a file name)
                Input annotation file must be
                <subject_id>/label/<hemisphere>.aparc.annot
        cortex: (a file name)
                Input cortex label must be
                <subject_id>/label/<hemisphere>.cortex.label
        hemisphere: ('lh' or 'rh')
                Hemisphere being processed
                flag: --%s-only
        orig: (an existing file name)
                Implicit input file mri/orig.mgz
        rawavg: (an existing file name)
                Implicit input file mri/rawavg.mgz
        subject_id: (a string, nipype default value: subject_id)
                Subject being processed
                flag: --s %s
        thickness: (an existing file name)
                Input file must be <subject_id>/surf/?h.thickness
        white: (an existing file name)
                Input file must be <subject_id>/surf/<hemisphere>.white

        [Optional]
        args: (a unicode string)
                Additional parameters to the command
                flag: %s
        copy_inputs: (a boolean)
                If running as a node, set this to True.This will copy the input
                files to the node directory.
        environ: (a dictionary with keys which are a bytes or None or a value
                 of class 'str' and with values which are a bytes or None or a value
                 of class 'str', nipype default value: {})
                Environment variables
        ignore_exception: (a boolean, nipype default value: False)
                Print an error message instead of throwing an exception in case the
                interface fails to run
        subjects_dir: (an existing directory name)
                subjects directory
        terminal_output: ('stream' or 'allatonce' or 'file' or 'none')
                Control terminal output: `stream` - displays to terminal immediately
                (default), `allatonce` - waits till command is finished to display
                output, `file` - writes output to file, `none` - output is ignored

Outputs::

        out_contrast: (a file name)
                Output contrast file from Contrast
        out_log: (an existing file name)
                Output log from Contrast
        out_stats: (a file name)
                Output stats file from Contrast

.. _nipype.interfaces.freesurfer.utils.Curvature:


.. index:: Curvature

Curvature
---------

`Link to code <http://github.com/nipy/nipype/tree/ec86b7476/nipype/interfaces/freesurfer/utils.py#L2156>`__

Wraps command **mris_curvature**

This program will compute the second fundamental form of a cortical
surface. It will create two new files <hemi>.<surface>.H and
<hemi>.<surface>.K with the mean and Gaussian curvature respectively.

Examples
~~~~~~~~
>>> from nipype.interfaces.freesurfer import Curvature
>>> curv = Curvature()
>>> curv.inputs.in_file = 'lh.pial'
>>> curv.inputs.save = True
>>> curv.cmdline # doctest: +ALLOW_UNICODE
'mris_curvature -w lh.pial'

Inputs::

        [Mandatory]
        in_file: (an existing file name)
                Input file for Curvature
                flag: %s, position: -2

        [Optional]
        args: (a unicode string)
                Additional parameters to the command
                flag: %s
        averages: (an integer (int or long))
                Perform this number iterative averages of curvature measure before
                saving
                flag: -a %d
        copy_input: (a boolean)
                Copy input file to current directory
        distances: (a tuple of the form: (an integer (int or long), an
                 integer (int or long)))
                Undocumented input integer distances
                flag: -distances %d %d
        environ: (a dictionary with keys which are a bytes or None or a value
                 of class 'str' and with values which are a bytes or None or a value
                 of class 'str', nipype default value: {})
                Environment variables
        ignore_exception: (a boolean, nipype default value: False)
                Print an error message instead of throwing an exception in case the
                interface fails to run
        n: (a boolean)
                Undocumented boolean flag
                flag: -n
        save: (a boolean)
                Save curvature files (will only generate screen output without this
                option)
                flag: -w
        subjects_dir: (an existing directory name)
                subjects directory
        terminal_output: ('stream' or 'allatonce' or 'file' or 'none')
                Control terminal output: `stream` - displays to terminal immediately
                (default), `allatonce` - waits till command is finished to display
                output, `file` - writes output to file, `none` - output is ignored
        threshold: (a float)
                Undocumented input threshold
                flag: -thresh %.3f

Outputs::

        out_gauss: (a file name)
                Gaussian curvature output file
        out_mean: (a file name)
                Mean curvature output file

.. _nipype.interfaces.freesurfer.utils.CurvatureStats:


.. index:: CurvatureStats

CurvatureStats
--------------

`Link to code <http://github.com/nipy/nipype/tree/ec86b7476/nipype/interfaces/freesurfer/utils.py#L2227>`__

Wraps command **mris_curvature_stats**

In its simplest usage, 'mris_curvature_stats' will compute a set
of statistics on its input <curvFile>. These statistics are the
mean and standard deviation of the particular curvature on the
surface, as well as the results from several surface-based
integrals.

Additionally, 'mris_curvature_stats' can report the max/min
curvature values, and compute a simple histogram based on
all curvature values.

Curvatures can also be normalised and constrained to a given
range before computation.

Principal curvature (K, H, k1 and k2) calculations on a surface
structure can also be performed, as well as several functions
derived from k1 and k2.

Finally, all output to the console, as well as any new
curvatures that result from the above calculations can be
saved to a series of text and binary-curvature files.

Examples
~~~~~~~~
>>> from nipype.interfaces.freesurfer import CurvatureStats
>>> curvstats = CurvatureStats()
>>> curvstats.inputs.hemisphere = 'lh'
>>> curvstats.inputs.curvfile1 = 'lh.pial'
>>> curvstats.inputs.curvfile2 = 'lh.pial'
>>> curvstats.inputs.surface = 'lh.pial'
>>> curvstats.inputs.out_file = 'lh.curv.stats'
>>> curvstats.inputs.values = True
>>> curvstats.inputs.min_max = True
>>> curvstats.inputs.write = True
>>> curvstats.cmdline # doctest: +ALLOW_UNICODE
'mris_curvature_stats -m -o lh.curv.stats -F pial -G --writeCurvatureFiles subject_id lh pial pial'

Inputs::

        [Mandatory]
        curvfile1: (an existing file name)
                Input file for CurvatureStats
                flag: %s, position: -2
        curvfile2: (an existing file name)
                Input file for CurvatureStats
                flag: %s, position: -1
        hemisphere: ('lh' or 'rh')
                Hemisphere being processed
                flag: %s, position: -3
        subject_id: (a string, nipype default value: subject_id)
                Subject being processed
                flag: %s, position: -4

        [Optional]
        args: (a unicode string)
                Additional parameters to the command
                flag: %s
        copy_inputs: (a boolean)
                If running as a node, set this to True.This will copy the input
                files to the node directory.
        environ: (a dictionary with keys which are a bytes or None or a value
                 of class 'str' and with values which are a bytes or None or a value
                 of class 'str', nipype default value: {})
                Environment variables
        ignore_exception: (a boolean, nipype default value: False)
                Print an error message instead of throwing an exception in case the
                interface fails to run
        min_max: (a boolean)
                Output min / max information for the processed curvature.
                flag: -m
        out_file: (a file name)
                Output curvature stats file
                flag: -o %s
        subjects_dir: (an existing directory name)
                subjects directory
        surface: (an existing file name)
                Specify surface file for CurvatureStats
                flag: -F %s
        terminal_output: ('stream' or 'allatonce' or 'file' or 'none')
                Control terminal output: `stream` - displays to terminal immediately
                (default), `allatonce` - waits till command is finished to display
                output, `file` - writes output to file, `none` - output is ignored
        values: (a boolean)
                Triggers a series of derived curvature values
                flag: -G
        write: (a boolean)
                Write curvature files
                flag: --writeCurvatureFiles

Outputs::

        out_file: (a file name)
                Output curvature stats file

.. _nipype.interfaces.freesurfer.utils.EulerNumber:


.. index:: EulerNumber

EulerNumber
-----------

`Link to code <http://github.com/nipy/nipype/tree/ec86b7476/nipype/interfaces/freesurfer/utils.py#L1894>`__

Wraps command **mris_euler_number**

This program computes EulerNumber for a cortical surface

Examples
~~~~~~~~
>>> from nipype.interfaces.freesurfer import EulerNumber
>>> ft = EulerNumber()
>>> ft.inputs.in_file = 'lh.pial'
>>> ft.cmdline # doctest: +ALLOW_UNICODE
'mris_euler_number lh.pial'

Inputs::

        [Mandatory]
        in_file: (an existing file name)
                Input file for EulerNumber
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
        subjects_dir: (an existing directory name)
                subjects directory
        terminal_output: ('stream' or 'allatonce' or 'file' or 'none')
                Control terminal output: `stream` - displays to terminal immediately
                (default), `allatonce` - waits till command is finished to display
                output, `file` - writes output to file, `none` - output is ignored

Outputs::

        out_file: (a file name)
                Output file for EulerNumber

.. _nipype.interfaces.freesurfer.utils.ExtractMainComponent:


.. index:: ExtractMainComponent

ExtractMainComponent
--------------------

`Link to code <http://github.com/nipy/nipype/tree/ec86b7476/nipype/interfaces/freesurfer/utils.py#L1324>`__

Wraps command **mris_extract_main_component**

Extract the main component of a tesselated surface

Examples
~~~~~~~~

>>> from nipype.interfaces.freesurfer import ExtractMainComponent
>>> mcmp = ExtractMainComponent(in_file='lh.pial')
>>> mcmp.cmdline # doctest: +ALLOW_UNICODE
'mris_extract_main_component lh.pial lh.maincmp'

Inputs::

        [Mandatory]
        in_file: (an existing file name)
                input surface file
                flag: %s, position: 1

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
                surface containing main component
                flag: %s, position: 2
        terminal_output: ('stream' or 'allatonce' or 'file' or 'none')
                Control terminal output: `stream` - displays to terminal immediately
                (default), `allatonce` - waits till command is finished to display
                output, `file` - writes output to file, `none` - output is ignored

Outputs::

        out_file: (an existing file name)
                surface containing main component

.. _nipype.interfaces.freesurfer.utils.FixTopology:


.. index:: FixTopology

FixTopology
-----------

`Link to code <http://github.com/nipy/nipype/tree/ec86b7476/nipype/interfaces/freesurfer/utils.py#L1826>`__

Wraps command **mris_fix_topology**

This program computes a mapping from the unit sphere onto the surface
of the cortex from a previously generated approximation of the
cortical surface, thus guaranteeing a topologically correct surface.

Examples
~~~~~~~~
>>> from nipype.interfaces.freesurfer import FixTopology
>>> ft = FixTopology()
>>> ft.inputs.in_orig = 'lh.orig' # doctest: +SKIP
>>> ft.inputs.in_inflated = 'lh.inflated' # doctest: +SKIP
>>> ft.inputs.sphere = 'lh.qsphere.nofix' # doctest: +SKIP
>>> ft.inputs.hemisphere = 'lh'
>>> ft.inputs.subject_id = '10335'
>>> ft.inputs.mgz = True
>>> ft.inputs.ga = True
>>> ft.cmdline # doctest: +SKIP
'mris_fix_topology -ga -mgz -sphere qsphere.nofix 10335 lh'

Inputs::

        [Mandatory]
        copy_inputs: (a boolean)
                If running as a node, set this to True otherwise, the topology
                fixing will be done in place.
        hemisphere: (a string)
                Hemisphere being processed
                flag: %s, position: -1
        in_brain: (an existing file name)
                Implicit input brain.mgz
        in_inflated: (an existing file name)
                Undocumented input file <hemisphere>.inflated
        in_orig: (an existing file name)
                Undocumented input file <hemisphere>.orig
        in_wm: (an existing file name)
                Implicit input wm.mgz
        subject_id: (a string, nipype default value: subject_id)
                Subject being processed
                flag: %s, position: -2

        [Optional]
        args: (a unicode string)
                Additional parameters to the command
                flag: %s
        environ: (a dictionary with keys which are a bytes or None or a value
                 of class 'str' and with values which are a bytes or None or a value
                 of class 'str', nipype default value: {})
                Environment variables
        ga: (a boolean)
                No documentation. Direct questions to analysis-
                bugs@nmr.mgh.harvard.edu
                flag: -ga
        ignore_exception: (a boolean, nipype default value: False)
                Print an error message instead of throwing an exception in case the
                interface fails to run
        mgz: (a boolean)
                No documentation. Direct questions to analysis-
                bugs@nmr.mgh.harvard.edu
                flag: -mgz
        seed: (an integer (int or long))
                Seed for setting random number generator
                flag: -seed %d
        sphere: (a file name)
                Sphere input file
                flag: -sphere %s
        subjects_dir: (an existing directory name)
                subjects directory
        terminal_output: ('stream' or 'allatonce' or 'file' or 'none')
                Control terminal output: `stream` - displays to terminal immediately
                (default), `allatonce` - waits till command is finished to display
                output, `file` - writes output to file, `none` - output is ignored

Outputs::

        out_file: (a file name)
                Output file for FixTopology

.. _nipype.interfaces.freesurfer.utils.Jacobian:


.. index:: Jacobian

Jacobian
--------

`Link to code <http://github.com/nipy/nipype/tree/ec86b7476/nipype/interfaces/freesurfer/utils.py#L2309>`__

Wraps command **mris_jacobian**

This program computes the Jacobian of a surface mapping.

Examples
~~~~~~~~
>>> from nipype.interfaces.freesurfer import Jacobian
>>> jacobian = Jacobian()
>>> jacobian.inputs.in_origsurf = 'lh.pial'
>>> jacobian.inputs.in_mappedsurf = 'lh.pial'
>>> jacobian.cmdline # doctest: +ALLOW_UNICODE
'mris_jacobian lh.pial lh.pial lh.jacobian'

Inputs::

        [Mandatory]
        in_mappedsurf: (an existing file name)
                Mapped surface
                flag: %s, position: -2
        in_origsurf: (an existing file name)
                Original surface
                flag: %s, position: -3

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
                Output Jacobian of the surface mapping
                flag: %s, position: -1
        subjects_dir: (an existing directory name)
                subjects directory
        terminal_output: ('stream' or 'allatonce' or 'file' or 'none')
                Control terminal output: `stream` - displays to terminal immediately
                (default), `allatonce` - waits till command is finished to display
                output, `file` - writes output to file, `none` - output is ignored

Outputs::

        out_file: (a file name)
                Output Jacobian of the surface mapping

.. _nipype.interfaces.freesurfer.utils.MRIFill:


.. index:: MRIFill

MRIFill
-------

`Link to code <http://github.com/nipy/nipype/tree/ec86b7476/nipype/interfaces/freesurfer/utils.py#L1674>`__

Wraps command **mri_fill**

This program creates hemispheric cutting planes and fills white matter
with specific values for subsequent surface tesselation.

Examples
~~~~~~~~
>>> from nipype.interfaces.freesurfer import MRIFill
>>> fill = MRIFill()
>>> fill.inputs.in_file = 'wm.mgz' # doctest: +SKIP
>>> fill.inputs.out_file = 'filled.mgz' # doctest: +SKIP
>>> fill.cmdline # doctest: +SKIP
'mri_fill wm.mgz filled.mgz'

Inputs::

        [Mandatory]
        in_file: (an existing file name)
                Input white matter file
                flag: %s, position: -2
        out_file: (a file name)
                Output filled volume file name for MRIFill
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
        log_file: (a file name)
                Output log file for MRIFill
                flag: -a %s
        segmentation: (an existing file name)
                Input segmentation file for MRIFill
                flag: -segmentation %s
        subjects_dir: (an existing directory name)
                subjects directory
        terminal_output: ('stream' or 'allatonce' or 'file' or 'none')
                Control terminal output: `stream` - displays to terminal immediately
                (default), `allatonce` - waits till command is finished to display
                output, `file` - writes output to file, `none` - output is ignored
        transform: (an existing file name)
                Input transform file for MRIFill
                flag: -xform %s

Outputs::

        log_file: (a file name)
                Output log file from MRIFill
        out_file: (a file name)
                Output file from MRIFill

.. _nipype.interfaces.freesurfer.utils.MRIMarchingCubes:


.. index:: MRIMarchingCubes

MRIMarchingCubes
----------------

`Link to code <http://github.com/nipy/nipype/tree/ec86b7476/nipype/interfaces/freesurfer/utils.py#L1157>`__

Wraps command **mri_mc**

Uses Freesurfer's mri_mc to create surfaces by tessellating a given input volume

Example
~~~~~~~

>>> import nipype.interfaces.freesurfer as fs
>>> mc = fs.MRIMarchingCubes()
>>> mc.inputs.in_file = 'aseg.mgz'
>>> mc.inputs.label_value = 17
>>> mc.inputs.out_file = 'lh.hippocampus'
>>> mc.run() # doctest: +SKIP

Inputs::

        [Mandatory]
        in_file: (an existing file name)
                Input volume to tesselate voxels from.
                flag: %s, position: 1
        label_value: (an integer (int or long))
                Label value which to tesselate from the input volume. (integer, if
                input is "filled.mgz" volume, 127 is rh, 255 is lh)
                flag: %d, position: 2

        [Optional]
        args: (a unicode string)
                Additional parameters to the command
                flag: %s
        connectivity_value: (an integer (int or long), nipype default value:
                 1)
                Alter the marching cubes connectivity: 1=6+,2=18,3=6,4=26
                (default=1)
                flag: %d, position: -1
        environ: (a dictionary with keys which are a bytes or None or a value
                 of class 'str' and with values which are a bytes or None or a value
                 of class 'str', nipype default value: {})
                Environment variables
        ignore_exception: (a boolean, nipype default value: False)
                Print an error message instead of throwing an exception in case the
                interface fails to run
        out_file: (a file name)
                output filename or True to generate one
                flag: ./%s, position: -2
        subjects_dir: (an existing directory name)
                subjects directory
        terminal_output: ('stream' or 'allatonce' or 'file' or 'none')
                Control terminal output: `stream` - displays to terminal immediately
                (default), `allatonce` - waits till command is finished to display
                output, `file` - writes output to file, `none` - output is ignored

Outputs::

        surface: (an existing file name)
                binary surface of the tessellation

.. _nipype.interfaces.freesurfer.utils.MRIPretess:


.. index:: MRIPretess

MRIPretess
----------

`Link to code <http://github.com/nipy/nipype/tree/ec86b7476/nipype/interfaces/freesurfer/utils.py#L1108>`__

Wraps command **mri_pretess**

Uses Freesurfer's mri_pretess to prepare volumes to be tessellated.

Description
~~~~~~~~~~~

Changes white matter (WM) segmentation so that the neighbors of all
voxels labeled as WM have a face in common - no edges or corners
allowed.

Example
~~~~~~~

>>> import nipype.interfaces.freesurfer as fs
>>> pretess = fs.MRIPretess()
>>> pretess.inputs.in_filled = 'wm.mgz'
>>> pretess.inputs.in_norm = 'norm.mgz'
>>> pretess.inputs.nocorners = True
>>> pretess.cmdline # doctest: +ALLOW_UNICODE
'mri_pretess -nocorners wm.mgz wm norm.mgz wm_pretesswm.mgz'
>>> pretess.run() # doctest: +SKIP

Inputs::

        [Mandatory]
        in_filled: (an existing file name)
                filled volume, usually wm.mgz
                flag: %s, position: -4
        in_norm: (an existing file name)
                the normalized, brain-extracted T1w image. Usually norm.mgz
                flag: %s, position: -2
        label: (a unicode string or an integer (int or long), nipype default
                 value: wm)
                label to be picked up, can be a Freesurfer's string like 'wm' or a
                label value (e.g. 127 for rh or 255 for lh)
                flag: %s, position: -3

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
        keep: (a boolean)
                keep WM edits
                flag: -keep
        nocorners: (a boolean)
                do not remove corner configurations in addition to edge ones.
                flag: -nocorners
        out_file: (a file name)
                the output file after mri_pretess.
                flag: %s, position: -1
        subjects_dir: (an existing directory name)
                subjects directory
        terminal_output: ('stream' or 'allatonce' or 'file' or 'none')
                Control terminal output: `stream` - displays to terminal immediately
                (default), `allatonce` - waits till command is finished to display
                output, `file` - writes output to file, `none` - output is ignored
        test: (a boolean)
                adds a voxel that should be removed by mri_pretess. The value of the
                voxel is set to that of an ON-edited WM, so it should be kept with
                -keep. The output will NOT be saved.
                flag: -test

Outputs::

        out_file: (an existing file name)
                output file after mri_pretess

.. _nipype.interfaces.freesurfer.utils.MRITessellate:


.. index:: MRITessellate

MRITessellate
-------------

`Link to code <http://github.com/nipy/nipype/tree/ec86b7476/nipype/interfaces/freesurfer/utils.py#L1047>`__

Wraps command **mri_tessellate**

Uses Freesurfer's mri_tessellate to create surfaces by tessellating a given input volume

Example
~~~~~~~

>>> import nipype.interfaces.freesurfer as fs
>>> tess = fs.MRITessellate()
>>> tess.inputs.in_file = 'aseg.mgz'
>>> tess.inputs.label_value = 17
>>> tess.inputs.out_file = 'lh.hippocampus'
>>> tess.run() # doctest: +SKIP

Inputs::

        [Mandatory]
        in_file: (an existing file name)
                Input volume to tesselate voxels from.
                flag: %s, position: -3
        label_value: (an integer (int or long))
                Label value which to tesselate from the input volume. (integer, if
                input is "filled.mgz" volume, 127 is rh, 255 is lh)
                flag: %d, position: -2

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
                output filename or True to generate one
                flag: %s, position: -1
        subjects_dir: (an existing directory name)
                subjects directory
        terminal_output: ('stream' or 'allatonce' or 'file' or 'none')
                Control terminal output: `stream` - displays to terminal immediately
                (default), `allatonce` - waits till command is finished to display
                output, `file` - writes output to file, `none` - output is ignored
        tesselate_all_voxels: (a boolean)
                Tessellate the surface of all voxels with different labels
                flag: -a
        use_real_RAS_coordinates: (a boolean)
                Saves surface with real RAS coordinates where c_(r,a,s) != 0
                flag: -n

Outputs::

        surface: (an existing file name)
                binary surface of the tessellation

.. _nipype.interfaces.freesurfer.utils.MRIsCalc:


.. index:: MRIsCalc

MRIsCalc
--------

`Link to code <http://github.com/nipy/nipype/tree/ec86b7476/nipype/interfaces/freesurfer/utils.py#L2355>`__

Wraps command **mris_calc**

'mris_calc' is a simple calculator that operates on FreeSurfer
curvatures and volumes. In most cases, the calculator functions with
three arguments: two inputs and an <ACTION> linking them. Some
actions, however, operate with only one input <file1>. In all cases,
the first input <file1> is the name of a FreeSurfer curvature overlay
(e.g. rh.curv) or volume file (e.g. orig.mgz). For two inputs, the
calculator first assumes that the second input is a file. If, however,
this second input file doesn't exist, the calculator assumes it refers
to a float number, which is then processed according to <ACTION>.Note:
<file1> and <file2> should typically be generated on the same subject.

Examples
~~~~~~~~
>>> from nipype.interfaces.freesurfer import MRIsCalc
>>> example = MRIsCalc()
>>> example.inputs.in_file1 = 'lh.area' # doctest: +SKIP
>>> example.inputs.in_file2 = 'lh.area.pial' # doctest: +SKIP
>>> example.inputs.action = 'add'
>>> example.inputs.out_file = 'area.mid'
>>> example.cmdline # doctest: +SKIP
'mris_calc -o lh.area.mid lh.area add lh.area.pial'

Inputs::

        [Mandatory]
        action: (a string)
                Action to perform on input file(s)
                flag: %s, position: -2
        in_file1: (an existing file name)
                Input file 1
                flag: %s, position: -3
        out_file: (a file name)
                Output file after calculation
                flag: -o %s

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
        in_file2: (an existing file name)
                Input file 2
                flag: %s, position: -1
                mutually_exclusive: in_float, in_int
        in_float: (a float)
                Input float
                flag: %f, position: -1
                mutually_exclusive: in_file2, in_int
        in_int: (an integer (int or long))
                Input integer
                flag: %d, position: -1
                mutually_exclusive: in_file2, in_float
        subjects_dir: (an existing directory name)
                subjects directory
        terminal_output: ('stream' or 'allatonce' or 'file' or 'none')
                Control terminal output: `stream` - displays to terminal immediately
                (default), `allatonce` - waits till command is finished to display
                output, `file` - writes output to file, `none` - output is ignored

Outputs::

        out_file: (a file name)
                Output file after calculation

.. _nipype.interfaces.freesurfer.utils.MRIsCombine:


.. index:: MRIsCombine

MRIsCombine
-----------

`Link to code <http://github.com/nipy/nipype/tree/ec86b7476/nipype/interfaces/freesurfer/utils.py#L977>`__

Wraps command **mris_convert**

Uses Freesurfer's ``mris_convert`` to combine two surface files into one.

For complete details, see the `mris_convert Documentation.
<https://surfer.nmr.mgh.harvard.edu/fswiki/mris_convert>`_

If given an ``out_file`` that does not begin with ``'lh.'`` or ``'rh.'``,
``mris_convert`` will prepend ``'lh.'`` to the file name.
To avoid this behavior, consider setting ``out_file = './<filename>'``, or
leaving out_file blank.

In a Node/Workflow, ``out_file`` is interpreted literally.

Example
~~~~~~~

>>> import nipype.interfaces.freesurfer as fs
>>> mris = fs.MRIsCombine()
>>> mris.inputs.in_files = ['lh.pial', 'rh.pial']
>>> mris.inputs.out_file = 'bh.pial'
>>> mris.cmdline  # doctest: +ALLOW_UNICODE
'mris_convert --combinesurfs lh.pial rh.pial bh.pial'
>>> mris.run()  # doctest: +SKIP

Inputs::

        [Mandatory]
        in_files: (a list of from 2 to 2 items which are a file name)
                Two surfaces to be combined.
                flag: --combinesurfs %s, position: 1
        out_file: (a file name)
                Output filename. Combined surfaces from in_files.
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
        subjects_dir: (an existing directory name)
                subjects directory
        terminal_output: ('stream' or 'allatonce' or 'file' or 'none')
                Control terminal output: `stream` - displays to terminal immediately
                (default), `allatonce` - waits till command is finished to display
                output, `file` - writes output to file, `none` - output is ignored

Outputs::

        out_file: (an existing file name)
                Output filename. Combined surfaces from in_files.

.. _nipype.interfaces.freesurfer.utils.MRIsConvert:


.. index:: MRIsConvert

MRIsConvert
-----------

`Link to code <http://github.com/nipy/nipype/tree/ec86b7476/nipype/interfaces/freesurfer/utils.py#L905>`__

Wraps command **mris_convert**

Uses Freesurfer's mris_convert to convert surface files to various formats

Example
~~~~~~~

>>> import nipype.interfaces.freesurfer as fs
>>> mris = fs.MRIsConvert()
>>> mris.inputs.in_file = 'lh.pial'
>>> mris.inputs.out_datatype = 'gii'
>>> mris.run() # doctest: +SKIP

Inputs::

        [Mandatory]
        in_file: (an existing file name)
                File to read/convert
                flag: %s, position: -2
        out_datatype: ('asc' or 'ico' or 'tri' or 'stl' or 'vtk' or 'gii' or
                 'mgh' or 'mgz')
                These file formats are supported: ASCII: .ascICO: .ico, .tri GEO:
                .geo STL: .stl VTK: .vtk GIFTI: .gii MGH surface-encoded 'volume':
                .mgh, .mgz
                mutually_exclusive: out_file
        out_file: (a file name)
                output filename or True to generate one
                flag: %s, position: -1
                mutually_exclusive: out_datatype

        [Optional]
        annot_file: (an existing file name)
                input is annotation or gifti label data
                flag: --annot %s
        args: (a unicode string)
                Additional parameters to the command
                flag: %s
        dataarray_num: (an integer (int or long))
                if input is gifti, 'num' specifies which data array to use
                flag: --da_num %d
        environ: (a dictionary with keys which are a bytes or None or a value
                 of class 'str' and with values which are a bytes or None or a value
                 of class 'str', nipype default value: {})
                Environment variables
        functional_file: (an existing file name)
                input is functional time-series or other multi-frame data (must
                specify surface)
                flag: -f %s
        ignore_exception: (a boolean, nipype default value: False)
                Print an error message instead of throwing an exception in case the
                interface fails to run
        label_file: (an existing file name)
                infile is .label file, label is name of this label
                flag: --label %s
        labelstats_outfile: (a file name)
                outfile is name of gifti file to which label stats will be written
                flag: --labelstats %s
        normal: (a boolean)
                output is an ascii file where vertex data
                flag: -n
        origname: (a string)
                read orig positions
                flag: -o %s
        parcstats_file: (an existing file name)
                infile is name of text file containing label/val pairs
                flag: --parcstats %s
        patch: (a boolean)
                input is a patch, not a full surface
                flag: -p
        rescale: (a boolean)
                rescale vertex xyz so total area is same as group average
                flag: -r
        scalarcurv_file: (an existing file name)
                input is scalar curv overlay file (must still specify surface)
                flag: -c %s
        scale: (a float)
                scale vertex xyz by scale
                flag: -s %.3f
        subjects_dir: (an existing directory name)
                subjects directory
        talairachxfm_subjid: (a string)
                apply talairach xfm of subject to vertex xyz
                flag: -t %s
        terminal_output: ('stream' or 'allatonce' or 'file' or 'none')
                Control terminal output: `stream` - displays to terminal immediately
                (default), `allatonce` - waits till command is finished to display
                output, `file` - writes output to file, `none` - output is ignored
        to_scanner: (a boolean)
                convert coordinates from native FS (tkr) coords to scanner coords
                flag: --to-scanner
        to_tkr: (a boolean)
                convert coordinates from scanner coords to native FS (tkr) coords
                flag: --to-tkr
        vertex: (a boolean)
                Writes out neighbors of a vertex in each row
                flag: -v
        xyz_ascii: (a boolean)
                Print only surface xyz to ascii file
                flag: -a

Outputs::

        converted: (an existing file name)
                converted output surface

.. _nipype.interfaces.freesurfer.utils.MRIsExpand:


.. index:: MRIsExpand

MRIsExpand
----------

`Link to code <http://github.com/nipy/nipype/tree/ec86b7476/nipype/interfaces/freesurfer/utils.py#L3039>`__

Wraps command **mris_expand**

Expands a surface (typically ?h.white) outwards while maintaining
smoothness and self-intersection constraints.

Examples
~~~~~~~~
>>> from nipype.interfaces.freesurfer import MRIsExpand
>>> mris_expand = MRIsExpand(thickness=True, distance=0.5)
>>> mris_expand.inputs.in_file = 'lh.white'
>>> mris_expand.cmdline # doctest: +ALLOW_UNICODE
'mris_expand -thickness lh.white 0.5 expanded'
>>> mris_expand.inputs.out_name = 'graymid'
>>> mris_expand.cmdline # doctest: +ALLOW_UNICODE
'mris_expand -thickness lh.white 0.5 graymid'

Inputs::

        [Mandatory]
        distance: (a float)
                Distance in mm or fraction of cortical thickness
                flag: %g, position: -2
        in_file: (an existing file name)
                Surface to expand
                flag: %s, position: -3

        [Optional]
        args: (a unicode string)
                Additional parameters to the command
                flag: %s
        dt: (a float)
                dt (implicit: 0.25)
                flag: -T %g
        environ: (a dictionary with keys which are a bytes or None or a value
                 of class 'str' and with values which are a bytes or None or a value
                 of class 'str', nipype default value: {})
                Environment variables
        ignore_exception: (a boolean, nipype default value: False)
                Print an error message instead of throwing an exception in case the
                interface fails to run
        nsurfaces: (an integer (int or long))
                Number of surfacces to write during expansion
                flag: -N %d
        out_name: (a unicode string, nipype default value: expanded)
                Output surface file
                If no path, uses directory of `in_file`
                If no path AND missing "lh." or "rh.", derive from `in_file`
                flag: %s, position: -1
        pial: (a unicode string)
                Name of pial file (implicit: "pial")
                If no path, uses directory of `in_file`
                If no path AND missing "lh." or "rh.", derive from `in_file`
                flag: -pial %s
        smooth_averages: (an integer (int or long))
                Smooth surface with N iterations after expansion
                flag: -A %d
        sphere: (a unicode string, nipype default value: sphere)
                WARNING: Do not change this trait
        spring: (a float)
                Spring term (implicit: 0.05)
                flag: -S %g
        subjects_dir: (an existing directory name)
                subjects directory
        terminal_output: ('stream' or 'allatonce' or 'file' or 'none')
                Control terminal output: `stream` - displays to terminal immediately
                (default), `allatonce` - waits till command is finished to display
                output, `file` - writes output to file, `none` - output is ignored
        thickness: (a boolean)
                Expand by fraction of cortical thickness, not mm
                flag: -thickness
        thickness_name: (a unicode string)
                Name of thickness file (implicit: "thickness")
                If no path, uses directory of `in_file`
                If no path AND missing "lh." or "rh.", derive from `in_file`
                flag: -thickness_name %s
        write_iterations: (an integer (int or long))
                Write snapshots of expansion every N iterations
                flag: -W %d

Outputs::

        out_file: (a file name)
                Output surface file

.. _nipype.interfaces.freesurfer.utils.MRIsInflate:


.. index:: MRIsInflate

MRIsInflate
-----------

`Link to code <http://github.com/nipy/nipype/tree/ec86b7476/nipype/interfaces/freesurfer/utils.py#L1723>`__

Wraps command **mris_inflate**

This program will inflate a cortical surface.

Examples
~~~~~~~~
>>> from nipype.interfaces.freesurfer import MRIsInflate
>>> inflate = MRIsInflate()
>>> inflate.inputs.in_file = 'lh.pial'
>>> inflate.inputs.no_save_sulc = True
>>> inflate.cmdline # doctest: +SKIP
'mris_inflate -no-save-sulc lh.pial lh.inflated'

Inputs::

        [Mandatory]
        in_file: (an existing file name)
                Input file for MRIsInflate
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
        no_save_sulc: (a boolean)
                Do not save sulc file as output
                flag: -no-save-sulc
                mutually_exclusive: out_sulc
        out_file: (a file name)
                Output file for MRIsInflate
                flag: %s, position: -1
        out_sulc: (a file name)
                Output sulc file
                mutually_exclusive: no_save_sulc
        subjects_dir: (an existing directory name)
                subjects directory
        terminal_output: ('stream' or 'allatonce' or 'file' or 'none')
                Control terminal output: `stream` - displays to terminal immediately
                (default), `allatonce` - waits till command is finished to display
                output, `file` - writes output to file, `none` - output is ignored

Outputs::

        out_file: (a file name)
                Output file for MRIsInflate
        out_sulc: (a file name)
                Output sulc file

.. _nipype.interfaces.freesurfer.utils.MakeAverageSubject:


.. index:: MakeAverageSubject

MakeAverageSubject
------------------

`Link to code <http://github.com/nipy/nipype/tree/ec86b7476/nipype/interfaces/freesurfer/utils.py#L1289>`__

Wraps command **make_average_subject**

Make an average freesurfer subject

Examples
~~~~~~~~

>>> from nipype.interfaces.freesurfer import MakeAverageSubject
>>> avg = MakeAverageSubject(subjects_ids=['s1', 's2'])
>>> avg.cmdline # doctest: +ALLOW_UNICODE
'make_average_subject --out average --subjects s1 s2'

Inputs::

        [Mandatory]
        subjects_ids: (a list of items which are a unicode string)
                freesurfer subjects ids to average
                flag: --subjects %s

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
        out_name: (a file name, nipype default value: average)
                name for the average subject
                flag: --out %s
        subjects_dir: (an existing directory name)
                subjects directory
        terminal_output: ('stream' or 'allatonce' or 'file' or 'none')
                Control terminal output: `stream` - displays to terminal immediately
                (default), `allatonce` - waits till command is finished to display
                output, `file` - writes output to file, `none` - output is ignored

Outputs::

        average_subject_name: (a unicode string)
                Output registration file

.. _nipype.interfaces.freesurfer.utils.MakeSurfaces:


.. index:: MakeSurfaces

MakeSurfaces
------------

`Link to code <http://github.com/nipy/nipype/tree/ec86b7476/nipype/interfaces/freesurfer/utils.py#L2015>`__

Wraps command **mris_make_surfaces**

This program positions the tessellation of the cortical surface at the
white matter surface, then the gray matter surface and generate
surface files for these surfaces as well as a 'curvature' file for the
cortical thickness, and a surface file which approximates layer IV of
the cortical sheet.

Examples
~~~~~~~~
>>> from nipype.interfaces.freesurfer import MakeSurfaces
>>> makesurfaces = MakeSurfaces()
>>> makesurfaces.inputs.hemisphere = 'lh'
>>> makesurfaces.inputs.subject_id = '10335'
>>> makesurfaces.inputs.in_orig = 'lh.pial'
>>> makesurfaces.inputs.in_wm = 'wm.mgz'
>>> makesurfaces.inputs.in_filled = 'norm.mgz'
>>> makesurfaces.inputs.in_label = 'aparc+aseg.nii'
>>> makesurfaces.inputs.in_T1 = 'T1.mgz'
>>> makesurfaces.inputs.orig_pial = 'lh.pial'
>>> makesurfaces.cmdline # doctest: +ALLOW_UNICODE
'mris_make_surfaces -T1 T1.mgz -orig pial -orig_pial pial 10335 lh'

Inputs::

        [Mandatory]
        hemisphere: ('lh' or 'rh')
                Hemisphere being processed
                flag: %s, position: -1
        in_filled: (an existing file name)
                Implicit input file filled.mgz
        in_orig: (an existing file name)
                Implicit input file <hemisphere>.orig
                flag: -orig %s
        in_wm: (an existing file name)
                Implicit input file wm.mgz
        subject_id: (a string, nipype default value: subject_id)
                Subject being processed
                flag: %s, position: -2

        [Optional]
        args: (a unicode string)
                Additional parameters to the command
                flag: %s
        copy_inputs: (a boolean)
                If running as a node, set this to True.This will copy the input
                files to the node directory.
        environ: (a dictionary with keys which are a bytes or None or a value
                 of class 'str' and with values which are a bytes or None or a value
                 of class 'str', nipype default value: {})
                Environment variables
        fix_mtl: (a boolean)
                Undocumented flag
                flag: -fix_mtl
        ignore_exception: (a boolean, nipype default value: False)
                Print an error message instead of throwing an exception in case the
                interface fails to run
        in_T1: (an existing file name)
                Input brain or T1 file
                flag: -T1 %s
        in_aseg: (an existing file name)
                Input segmentation file
                flag: -aseg %s
        in_label: (an existing file name)
                Implicit input label/<hemisphere>.aparc.annot
                mutually_exclusive: noaparc
        in_white: (an existing file name)
                Implicit input that is sometimes used
        longitudinal: (a boolean)
                No documentation (used for longitudinal processing)
                flag: -long
        maximum: (a float)
                No documentation (used for longitudinal processing)
                flag: -max %.1f
        mgz: (a boolean)
                No documentation. Direct questions to analysis-
                bugs@nmr.mgh.harvard.edu
                flag: -mgz
        no_white: (a boolean)
                Undocumented flag
                flag: -nowhite
        noaparc: (a boolean)
                No documentation. Direct questions to analysis-
                bugs@nmr.mgh.harvard.edu
                flag: -noaparc
                mutually_exclusive: in_label
        orig_pial: (an existing file name)
                Specify a pial surface to start with
                flag: -orig_pial %s
                requires: in_label
        orig_white: (an existing file name)
                Specify a white surface to start with
                flag: -orig_white %s
        subjects_dir: (an existing directory name)
                subjects directory
        terminal_output: ('stream' or 'allatonce' or 'file' or 'none')
                Control terminal output: `stream` - displays to terminal immediately
                (default), `allatonce` - waits till command is finished to display
                output, `file` - writes output to file, `none` - output is ignored
        white: (a string)
                White surface name
                flag: -white %s
        white_only: (a boolean)
                Undocumented flage
                flag: -whiteonly

Outputs::

        out_area: (a file name)
                Output area file for MakeSurfaces
        out_cortex: (a file name)
                Output cortex file for MakeSurfaces
        out_curv: (a file name)
                Output curv file for MakeSurfaces
        out_pial: (a file name)
                Output pial surface for MakeSurfaces
        out_thickness: (a file name)
                Output thickness file for MakeSurfaces
        out_white: (a file name)
                Output white matter hemisphere surface

.. _nipype.interfaces.freesurfer.utils.ParcellationStats:


.. index:: ParcellationStats

ParcellationStats
-----------------

`Link to code <http://github.com/nipy/nipype/tree/ec86b7476/nipype/interfaces/freesurfer/utils.py#L2555>`__

Wraps command **mris_anatomical_stats**

This program computes a number of anatomical properties.

Examples
~~~~~~~~
>>> from nipype.interfaces.freesurfer import ParcellationStats
>>> import os
>>> parcstats = ParcellationStats()
>>> parcstats.inputs.subject_id = '10335'
>>> parcstats.inputs.hemisphere = 'lh'
>>> parcstats.inputs.wm = './../mri/wm.mgz' # doctest: +SKIP
>>> parcstats.inputs.transform = './../mri/transforms/talairach.xfm' # doctest: +SKIP
>>> parcstats.inputs.brainmask = './../mri/brainmask.mgz' # doctest: +SKIP
>>> parcstats.inputs.aseg = './../mri/aseg.presurf.mgz' # doctest: +SKIP
>>> parcstats.inputs.ribbon = './../mri/ribbon.mgz' # doctest: +SKIP
>>> parcstats.inputs.lh_pial = 'lh.pial' # doctest: +SKIP
>>> parcstats.inputs.rh_pial = 'lh.pial' # doctest: +SKIP
>>> parcstats.inputs.lh_white = 'lh.white' # doctest: +SKIP
>>> parcstats.inputs.rh_white = 'rh.white' # doctest: +SKIP
>>> parcstats.inputs.thickness = 'lh.thickness' # doctest: +SKIP
>>> parcstats.inputs.surface = 'white'
>>> parcstats.inputs.out_table = 'lh.test.stats'
>>> parcstats.inputs.out_color = 'test.ctab'
>>> parcstats.cmdline # doctest: +SKIP
'mris_anatomical_stats -c test.ctab -f lh.test.stats 10335 lh white'

Inputs::

        [Mandatory]
        aseg: (an existing file name)
                Input file must be <subject_id>/mri/aseg.presurf.mgz
        brainmask: (an existing file name)
                Input file must be <subject_id>/mri/brainmask.mgz
        hemisphere: ('lh' or 'rh')
                Hemisphere being processed
                flag: %s, position: -2
        lh_pial: (an existing file name)
                Input file must be <subject_id>/surf/lh.pial
        lh_white: (an existing file name)
                Input file must be <subject_id>/surf/lh.white
        rh_pial: (an existing file name)
                Input file must be <subject_id>/surf/rh.pial
        rh_white: (an existing file name)
                Input file must be <subject_id>/surf/rh.white
        ribbon: (an existing file name)
                Input file must be <subject_id>/mri/ribbon.mgz
        subject_id: (a string, nipype default value: subject_id)
                Subject being processed
                flag: %s, position: -3
        thickness: (an existing file name)
                Input file must be <subject_id>/surf/?h.thickness
        transform: (an existing file name)
                Input file must be <subject_id>/mri/transforms/talairach.xfm
        wm: (an existing file name)
                Input file must be <subject_id>/mri/wm.mgz

        [Optional]
        args: (a unicode string)
                Additional parameters to the command
                flag: %s
        copy_inputs: (a boolean)
                If running as a node, set this to True.This will copy the input
                files to the node directory.
        cortex_label: (an existing file name)
                implicit input file {hemi}.cortex.label
        environ: (a dictionary with keys which are a bytes or None or a value
                 of class 'str' and with values which are a bytes or None or a value
                 of class 'str', nipype default value: {})
                Environment variables
        ignore_exception: (a boolean, nipype default value: False)
                Print an error message instead of throwing an exception in case the
                interface fails to run
        in_annotation: (a file name)
                compute properties for each label in the annotation file separately
                flag: -a %s
                mutually_exclusive: in_label
        in_cortex: (a file name)
                Input cortex label
                flag: -cortex %s
        in_label: (a file name)
                limit calculations to specified label
                flag: -l %s
                mutually_exclusive: in_annotatoin, out_color
        mgz: (a boolean)
                Look for mgz files
                flag: -mgz
        out_color: (a file name)
                Output annotation files's colortable to text file
                flag: -c %s
                mutually_exclusive: in_label
        out_table: (a file name)
                Table output to tablefile
                flag: -f %s
                requires: tabular_output
        subjects_dir: (an existing directory name)
                subjects directory
        surface: (a string)
                Input surface (e.g. 'white')
                flag: %s, position: -1
        tabular_output: (a boolean)
                Tabular output
                flag: -b
        terminal_output: ('stream' or 'allatonce' or 'file' or 'none')
                Control terminal output: `stream` - displays to terminal immediately
                (default), `allatonce` - waits till command is finished to display
                output, `file` - writes output to file, `none` - output is ignored
        th3: (a boolean)
                turns on new vertex-wise volume calc for mris_anat_stats
                flag: -th3
                requires: cortex_label

Outputs::

        out_color: (a file name)
                Output annotation files's colortable to text file
        out_table: (a file name)
                Table output to tablefile

.. _nipype.interfaces.freesurfer.utils.RelabelHypointensities:


.. index:: RelabelHypointensities

RelabelHypointensities
----------------------

`Link to code <http://github.com/nipy/nipype/tree/ec86b7476/nipype/interfaces/freesurfer/utils.py#L2784>`__

Wraps command **mri_relabel_hypointensities**

Relabel Hypointensities

Examples
~~~~~~~~
>>> from nipype.interfaces.freesurfer import RelabelHypointensities
>>> relabelhypos = RelabelHypointensities()
>>> relabelhypos.inputs.lh_white = 'lh.pial'
>>> relabelhypos.inputs.rh_white = 'lh.pial'
>>> relabelhypos.inputs.surf_directory = '.'
>>> relabelhypos.inputs.aseg = 'aseg.mgz'
>>> relabelhypos.cmdline # doctest: +ALLOW_UNICODE
'mri_relabel_hypointensities aseg.mgz . aseg.hypos.mgz'

Inputs::

        [Mandatory]
        aseg: (an existing file name)
                Input aseg file
                flag: %s, position: -3
        lh_white: (an existing file name)
                Implicit input file must be lh.white
        rh_white: (an existing file name)
                Implicit input file must be rh.white

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
                Output aseg file
                flag: %s, position: -1
        subjects_dir: (an existing directory name)
                subjects directory
        surf_directory: (a directory name, nipype default value: .)
                Directory containing lh.white and rh.white
                flag: %s, position: -2
        terminal_output: ('stream' or 'allatonce' or 'file' or 'none')
                Control terminal output: `stream` - displays to terminal immediately
                (default), `allatonce` - waits till command is finished to display
                output, `file` - writes output to file, `none` - output is ignored

Outputs::

        out_file: (a file name)
                Output aseg file
                flag: %s

.. _nipype.interfaces.freesurfer.utils.RemoveIntersection:


.. index:: RemoveIntersection

RemoveIntersection
------------------

`Link to code <http://github.com/nipy/nipype/tree/ec86b7476/nipype/interfaces/freesurfer/utils.py#L1930>`__

Wraps command **mris_remove_intersection**

This program removes the intersection of the given MRI

Examples
~~~~~~~~
>>> from nipype.interfaces.freesurfer import RemoveIntersection
>>> ri = RemoveIntersection()
>>> ri.inputs.in_file = 'lh.pial'
>>> ri.cmdline # doctest: +ALLOW_UNICODE
'mris_remove_intersection lh.pial lh.pial'

Inputs::

        [Mandatory]
        in_file: (an existing file name)
                Input file for RemoveIntersection
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
        out_file: (a file name)
                Output file for RemoveIntersection
                flag: %s, position: -1
        subjects_dir: (an existing directory name)
                subjects directory
        terminal_output: ('stream' or 'allatonce' or 'file' or 'none')
                Control terminal output: `stream` - displays to terminal immediately
                (default), `allatonce` - waits till command is finished to display
                output, `file` - writes output to file, `none` - output is ignored

Outputs::

        out_file: (a file name)
                Output file for RemoveIntersection

.. _nipype.interfaces.freesurfer.utils.RemoveNeck:


.. index:: RemoveNeck

RemoveNeck
----------

`Link to code <http://github.com/nipy/nipype/tree/ec86b7476/nipype/interfaces/freesurfer/utils.py#L1627>`__

Wraps command **mri_remove_neck**

Crops the neck out of the mri image

Examples
~~~~~~~~

>>> from nipype.interfaces.freesurfer import TalairachQC
>>> remove_neck = RemoveNeck()
>>> remove_neck.inputs.in_file = 'norm.mgz'
>>> remove_neck.inputs.transform = 'trans.mat'
>>> remove_neck.inputs.template = 'trans.mat'
>>> remove_neck.cmdline # doctest: +ALLOW_UNICODE
'mri_remove_neck norm.mgz trans.mat trans.mat norm_noneck.mgz'

Inputs::

        [Mandatory]
        in_file: (an existing file name)
                Input file for RemoveNeck
                flag: %s, position: -4
        template: (an existing file name)
                Input template file for RemoveNeck
                flag: %s, position: -2
        transform: (an existing file name)
                Input transform file for RemoveNeck
                flag: %s, position: -3

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
                Output file for RemoveNeck
                flag: %s, position: -1
        radius: (an integer (int or long))
                Radius
                flag: -radius %d
        subjects_dir: (an existing directory name)
                subjects directory
        terminal_output: ('stream' or 'allatonce' or 'file' or 'none')
                Control terminal output: `stream` - displays to terminal immediately
                (default), `allatonce` - waits till command is finished to display
                output, `file` - writes output to file, `none` - output is ignored

Outputs::

        out_file: (a file name)
                Output file with neck removed

.. _nipype.interfaces.freesurfer.utils.SampleToSurface:


.. index:: SampleToSurface

SampleToSurface
---------------

`Link to code <http://github.com/nipy/nipype/tree/ec86b7476/nipype/interfaces/freesurfer/utils.py#L174>`__

Wraps command **mri_vol2surf**

Sample a volume to the cortical surface using Freesurfer's mri_vol2surf.

You must supply a sampling method, range, and units.  You can project
either a given distance (in mm) or a given fraction of the cortical
thickness at that vertex along the surface normal from the target surface,
and then set the value of that vertex to be either the value at that point
or the average or maximum value found along the projection vector.

By default, the surface will be saved as a vector with a length equal to the
number of vertices on the target surface.  This is not a problem for Freesurfer
programs, but if you intend to use the file with interfaces to another package,
you must set the ``reshape`` input to True, which will factor the surface vector
into a matrix with dimensions compatible with proper Nifti files.

Examples
~~~~~~~~

>>> import nipype.interfaces.freesurfer as fs
>>> sampler = fs.SampleToSurface(hemi="lh")
>>> sampler.inputs.source_file = "cope1.nii.gz"
>>> sampler.inputs.reg_file = "register.dat"
>>> sampler.inputs.sampling_method = "average"
>>> sampler.inputs.sampling_range = 1
>>> sampler.inputs.sampling_units = "frac"
>>> sampler.cmdline  # doctest: +ELLIPSIS +ALLOW_UNICODE
'mri_vol2surf --hemi lh --o ...lh.cope1.mgz --reg register.dat --projfrac-avg 1.000 --mov cope1.nii.gz'
>>> res = sampler.run() # doctest: +SKIP

Inputs::

        [Mandatory]
        hemi: ('lh' or 'rh')
                target hemisphere
                flag: --hemi %s
        mni152reg: (a boolean)
                source volume is in MNI152 space
                flag: --mni152reg
                mutually_exclusive: reg_file, reg_header, mni152reg
        projection_stem: (a string)
                stem for precomputed linear estimates and volume fractions
                mutually_exclusive: sampling_method
        reg_file: (an existing file name)
                source-to-reference registration file
                flag: --reg %s
                mutually_exclusive: reg_file, reg_header, mni152reg
        reg_header: (a boolean)
                register based on header geometry
                flag: --regheader %s
                mutually_exclusive: reg_file, reg_header, mni152reg
                requires: subject_id
        sampling_method: ('point' or 'max' or 'average')
                how to sample -- at a point or at the max or average over a range
                flag: %s
                mutually_exclusive: projection_stem
                requires: sampling_range, sampling_units
        source_file: (an existing file name)
                volume to sample values from
                flag: --mov %s

        [Optional]
        apply_rot: (a tuple of the form: (a float, a float, a float))
                rotation angles (in degrees) to apply to reg matrix
                flag: --rot %.3f %.3f %.3f
        apply_trans: (a tuple of the form: (a float, a float, a float))
                translation (in mm) to apply to reg matrix
                flag: --trans %.3f %.3f %.3f
        args: (a unicode string)
                Additional parameters to the command
                flag: %s
        cortex_mask: (a boolean)
                mask the target surface with hemi.cortex.label
                flag: --cortex
                mutually_exclusive: mask_label
        environ: (a dictionary with keys which are a bytes or None or a value
                 of class 'str' and with values which are a bytes or None or a value
                 of class 'str', nipype default value: {})
                Environment variables
        fix_tk_reg: (a boolean)
                make reg matrix round-compatible
                flag: --fixtkreg
        float2int_method: ('round' or 'tkregister')
                method to convert reg matrix values (default is round)
                flag: --float2int %s
        frame: (an integer (int or long))
                save only one frame (0-based)
                flag: --frame %d
        hits_file: (a boolean or an existing file name)
                save image with number of hits at each voxel
                flag: --srchit %s
        hits_type: ('cor' or 'mgh' or 'mgz' or 'minc' or 'analyze' or
                 'analyze4d' or 'spm' or 'afni' or 'brik' or 'bshort' or 'bfloat' or
                 'sdt' or 'outline' or 'otl' or 'gdf' or 'nifti1' or 'nii' or
                 'niigz')
                hits file type
                flag: --srchit_type
        ico_order: (an integer (int or long))
                icosahedron order when target_subject is 'ico'
                flag: --icoorder %d
                requires: target_subject
        ignore_exception: (a boolean, nipype default value: False)
                Print an error message instead of throwing an exception in case the
                interface fails to run
        interp_method: ('nearest' or 'trilinear')
                interpolation method
                flag: --interp %s
        mask_label: (an existing file name)
                label file to mask output with
                flag: --mask %s
                mutually_exclusive: cortex_mask
        no_reshape: (a boolean)
                do not reshape surface vector (default)
                flag: --noreshape
                mutually_exclusive: reshape
        out_file: (a file name)
                surface file to write
                flag: --o %s
        out_type: ('cor' or 'mgh' or 'mgz' or 'minc' or 'analyze' or
                 'analyze4d' or 'spm' or 'afni' or 'brik' or 'bshort' or 'bfloat' or
                 'sdt' or 'outline' or 'otl' or 'gdf' or 'nifti1' or 'nii' or
                 'niigz' or 'gii')
                output file type
                flag: --out_type %s
        override_reg_subj: (a boolean)
                override the subject in the reg file header
                flag: --srcsubject %s
                requires: subject_id
        reference_file: (an existing file name)
                reference volume (default is orig.mgz)
                flag: --ref %s
        reshape: (a boolean)
                reshape surface vector to fit in non-mgh format
                flag: --reshape
                mutually_exclusive: no_reshape
        reshape_slices: (an integer (int or long))
                number of 'slices' for reshaping
                flag: --rf %d
        sampling_range: (a float or a tuple of the form: (a float, a float, a
                 float))
                sampling range - a point or a tuple of (min, max, step)
        sampling_units: ('mm' or 'frac')
                sampling range type -- either 'mm' or 'frac'
        scale_input: (a float)
                multiple all intensities by scale factor
                flag: --scale %.3f
        smooth_surf: (a float)
                smooth output surface (mm fwhm)
                flag: --surf-fwhm %.3f
        smooth_vol: (a float)
                smooth input volume (mm fwhm)
                flag: --fwhm %.3f
        subject_id: (a string)
                subject id
        subjects_dir: (an existing directory name)
                subjects directory
        surf_reg: (a boolean)
                use surface registration to target subject
                flag: --surfreg
                requires: target_subject
        surface: (a string)
                target surface (default is white)
                flag: --surf %s
        target_subject: (a string)
                sample to surface of different subject than source
                flag: --trgsubject %s
        terminal_output: ('stream' or 'allatonce' or 'file' or 'none')
                Control terminal output: `stream` - displays to terminal immediately
                (default), `allatonce` - waits till command is finished to display
                output, `file` - writes output to file, `none` - output is ignored
        vox_file: (a boolean or a file name)
                text file with the number of voxels intersecting the surface
                flag: --nvox %s

Outputs::

        hits_file: (an existing file name)
                image with number of hits at each voxel
        out_file: (an existing file name)
                surface file
        vox_file: (an existing file name)
                text file with the number of voxels intersecting the surface

.. _nipype.interfaces.freesurfer.utils.SmoothTessellation:


.. index:: SmoothTessellation

SmoothTessellation
------------------

`Link to code <http://github.com/nipy/nipype/tree/ec86b7476/nipype/interfaces/freesurfer/utils.py#L1228>`__

Wraps command **mris_smooth**

This program smooths the tessellation of a surface using 'mris_smooth'

.. seealso::

    SurfaceSmooth() Interface
        For smoothing a scalar field along a surface manifold

Example
~~~~~~~

>>> import nipype.interfaces.freesurfer as fs
>>> smooth = fs.SmoothTessellation()
>>> smooth.inputs.in_file = 'lh.hippocampus.stl'
>>> smooth.run() # doctest: +SKIP

Inputs::

        [Mandatory]
        in_file: (an existing file name)
                Input volume to tesselate voxels from.
                flag: %s, position: -2

        [Optional]
        args: (a unicode string)
                Additional parameters to the command
                flag: %s
        curvature_averaging_iterations: (an integer (int or long))
                Number of curvature averaging iterations (default=10)
                flag: -a %d
        disable_estimates: (a boolean)
                Disables the writing of curvature and area estimates
                flag: -nw
        environ: (a dictionary with keys which are a bytes or None or a value
                 of class 'str' and with values which are a bytes or None or a value
                 of class 'str', nipype default value: {})
                Environment variables
        gaussian_curvature_norm_steps: (an integer (int or long))
                Use Gaussian curvature smoothing
                flag: %d
        gaussian_curvature_smoothing_steps: (an integer (int or long))
                Use Gaussian curvature smoothing
                flag: %d
        ignore_exception: (a boolean, nipype default value: False)
                Print an error message instead of throwing an exception in case the
                interface fails to run
        normalize_area: (a boolean)
                Normalizes the area after smoothing
                flag: -area
        out_area_file: (a file name)
                Write area to ?h.areaname (default "area")
                flag: -b %s
        out_curvature_file: (a file name)
                Write curvature to ?h.curvname (default "curv")
                flag: -c %s
        out_file: (a file name)
                output filename or True to generate one
                flag: %s, position: -1
        seed: (an integer (int or long))
                Seed for setting random number generator
                flag: -seed %d
        smoothing_iterations: (an integer (int or long))
                Number of smoothing iterations (default=10)
                flag: -n %d
        snapshot_writing_iterations: (an integer (int or long))
                Write snapshot every "n" iterations
                flag: -w %d
        subjects_dir: (an existing directory name)
                subjects directory
        terminal_output: ('stream' or 'allatonce' or 'file' or 'none')
                Control terminal output: `stream` - displays to terminal immediately
                (default), `allatonce` - waits till command is finished to display
                output, `file` - writes output to file, `none` - output is ignored
        use_gaussian_curvature_smoothing: (a boolean)
                Use Gaussian curvature smoothing
                flag: -g
        use_momentum: (a boolean)
                Uses momentum
                flag: -m

Outputs::

        surface: (an existing file name)
                Smoothed surface file

.. _nipype.interfaces.freesurfer.utils.Sphere:


.. index:: Sphere

Sphere
------

`Link to code <http://github.com/nipy/nipype/tree/ec86b7476/nipype/interfaces/freesurfer/utils.py#L1770>`__

Wraps command **mris_sphere**

This program will add a template into an average surface

Examples
~~~~~~~~
>>> from nipype.interfaces.freesurfer import Sphere
>>> sphere = Sphere()
>>> sphere.inputs.in_file = 'lh.pial'
>>> sphere.cmdline # doctest: +ALLOW_UNICODE
'mris_sphere lh.pial lh.sphere'

Inputs::

        [Mandatory]
        in_file: (an existing file name)
                Input file for Sphere
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
        in_smoothwm: (an existing file name)
                Input surface required when -q flag is not selected
        magic: (a boolean)
                No documentation. Direct questions to analysis-
                bugs@nmr.mgh.harvard.edu
                flag: -q
        num_threads: (an integer (int or long))
                allows for specifying more threads
        out_file: (a file name)
                Output file for Sphere
                flag: %s, position: -1
        seed: (an integer (int or long))
                Seed for setting random number generator
                flag: -seed %d
        subjects_dir: (an existing directory name)
                subjects directory
        terminal_output: ('stream' or 'allatonce' or 'file' or 'none')
                Control terminal output: `stream` - displays to terminal immediately
                (default), `allatonce` - waits till command is finished to display
                output, `file` - writes output to file, `none` - output is ignored

Outputs::

        out_file: (a file name)
                Output file for Sphere

.. _nipype.interfaces.freesurfer.utils.Surface2VolTransform:


.. index:: Surface2VolTransform

Surface2VolTransform
--------------------

`Link to code <http://github.com/nipy/nipype/tree/ec86b7476/nipype/interfaces/freesurfer/utils.py#L508>`__

Wraps command **mri_surf2vol**

Use FreeSurfer mri_surf2vol to apply a transform.

Examples
~~~~~~~~

>>> from nipype.interfaces.freesurfer import Surface2VolTransform
>>> xfm2vol = Surface2VolTransform()
>>> xfm2vol.inputs.source_file = 'lh.cope1.mgz'
>>> xfm2vol.inputs.reg_file = 'register.mat'
>>> xfm2vol.inputs.hemi = 'lh'
>>> xfm2vol.inputs.template_file = 'cope1.nii.gz'
>>> xfm2vol.inputs.subjects_dir = '.'
>>> xfm2vol.cmdline # doctest: +ALLOW_UNICODE
'mri_surf2vol --hemi lh --volreg register.mat --surfval lh.cope1.mgz --sd . --template cope1.nii.gz --outvol lh.cope1_asVol.nii --vtxvol lh.cope1_asVol_vertex.nii'
>>> res = xfm2vol.run()# doctest: +SKIP

Inputs::

        [Mandatory]
        hemi: (a unicode string)
                hemisphere of data
                flag: --hemi %s
        reg_file: (an existing file name)
                tkRAS-to-tkRAS matrix (tkregister2 format)
                flag: --volreg %s
                mutually_exclusive: subject_id
        source_file: (an existing file name)
                This is the source of the surface values
                flag: --surfval %s
                mutually_exclusive: mkmask

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
        mkmask: (a boolean)
                make a mask instead of loading surface values
                flag: --mkmask
                mutually_exclusive: source_file
        projfrac: (a float)
                thickness fraction
                flag: --projfrac %s
        subject_id: (a unicode string)
                subject id
                flag: --identity %s
                mutually_exclusive: reg_file
        subjects_dir: (a unicode string)
                freesurfer subjects directory defaults to $SUBJECTS_DIR
                flag: --sd %s
        surf_name: (a unicode string)
                surfname (default is white)
                flag: --surf %s
        template_file: (an existing file name)
                Output template volume
                flag: --template %s
        terminal_output: ('stream' or 'allatonce' or 'file' or 'none')
                Control terminal output: `stream` - displays to terminal immediately
                (default), `allatonce` - waits till command is finished to display
                output, `file` - writes output to file, `none` - output is ignored
        transformed_file: (a file name)
                Output volume
                flag: --outvol %s
        vertexvol_file: (a file name)
                Path name of the vertex output volume, which is the same as output
                volume except that the value of each voxel is the vertex-id that is
                mapped to that voxel.
                flag: --vtxvol %s

Outputs::

        transformed_file: (an existing file name)
                Path to output file if used normally
        vertexvol_file: (a file name)
                vertex map volume path id. Optional

.. _nipype.interfaces.freesurfer.utils.SurfaceSmooth:


.. index:: SurfaceSmooth

SurfaceSmooth
-------------

`Link to code <http://github.com/nipy/nipype/tree/ec86b7476/nipype/interfaces/freesurfer/utils.py#L306>`__

Wraps command **mri_surf2surf**

Smooth a surface image with mri_surf2surf.

The surface is smoothed by an interative process of averaging the
value at each vertex with those of its adjacent neighbors. You may supply
either the number of iterations to run or a desired effective FWHM of the
smoothing process.  If the latter, the underlying program will calculate
the correct number of iterations internally.

.. seealso::

    SmoothTessellation() Interface
        For smoothing a tessellated surface (e.g. in gifti or .stl)

Examples
~~~~~~~~

>>> import nipype.interfaces.freesurfer as fs
>>> smoother = fs.SurfaceSmooth()
>>> smoother.inputs.in_file = "lh.cope1.mgz"
>>> smoother.inputs.subject_id = "subj_1"
>>> smoother.inputs.hemi = "lh"
>>> smoother.inputs.fwhm = 5
>>> smoother.cmdline # doctest: +ELLIPSIS +ALLOW_UNICODE
'mri_surf2surf --cortex --fwhm 5.0000 --hemi lh --sval lh.cope1.mgz --tval ...lh.cope1_smooth5.mgz --s subj_1'
>>> smoother.run() # doctest: +SKIP

Inputs::

        [Mandatory]
        hemi: ('lh' or 'rh')
                hemisphere to operate on
                flag: --hemi %s
        in_file: (a file name)
                source surface file
                flag: --sval %s
        subject_id: (a string)
                subject id of surface file
                flag: --s %s

        [Optional]
        args: (a unicode string)
                Additional parameters to the command
                flag: %s
        cortex: (a boolean, nipype default value: True)
                only smooth within $hemi.cortex.label
                flag: --cortex
        environ: (a dictionary with keys which are a bytes or None or a value
                 of class 'str' and with values which are a bytes or None or a value
                 of class 'str', nipype default value: {})
                Environment variables
        fwhm: (a float)
                effective FWHM of the smoothing process
                flag: --fwhm %.4f
                mutually_exclusive: smooth_iters
        ignore_exception: (a boolean, nipype default value: False)
                Print an error message instead of throwing an exception in case the
                interface fails to run
        out_file: (a file name)
                surface file to write
                flag: --tval %s
        reshape: (a boolean)
                reshape surface vector to fit in non-mgh format
                flag: --reshape
        smooth_iters: (an integer (int or long))
                iterations of the smoothing process
                flag: --smooth %d
                mutually_exclusive: fwhm
        subjects_dir: (an existing directory name)
                subjects directory
        terminal_output: ('stream' or 'allatonce' or 'file' or 'none')
                Control terminal output: `stream` - displays to terminal immediately
                (default), `allatonce` - waits till command is finished to display
                output, `file` - writes output to file, `none` - output is ignored

Outputs::

        out_file: (an existing file name)
                smoothed surface file

.. _nipype.interfaces.freesurfer.utils.SurfaceSnapshots:


.. index:: SurfaceSnapshots

SurfaceSnapshots
----------------

`Link to code <http://github.com/nipy/nipype/tree/ec86b7476/nipype/interfaces/freesurfer/utils.py#L650>`__

Wraps command **tksurfer**

Use Tksurfer to save pictures of the cortical surface.

By default, this takes snapshots of the lateral, medial, ventral,
and dorsal surfaces.  See the ``six_images`` option to add the
anterior and posterior surfaces.

You may also supply your own tcl script (see the Freesurfer wiki for
information on scripting tksurfer). The screenshot stem is set as the
environment variable "_SNAPSHOT_STEM", which you can use in your
own scripts.

Node that this interface will not run if you do not have graphics
enabled on your system.

Examples
~~~~~~~~

>>> import nipype.interfaces.freesurfer as fs
>>> shots = fs.SurfaceSnapshots(subject_id="fsaverage", hemi="lh", surface="pial")
>>> shots.inputs.overlay = "zstat1.nii.gz"
>>> shots.inputs.overlay_range = (2.3, 6)
>>> shots.inputs.overlay_reg = "register.dat"
>>> res = shots.run() # doctest: +SKIP

Inputs::

        [Mandatory]
        hemi: ('lh' or 'rh')
                hemisphere to visualize
                flag: %s, position: 2
        subject_id: (a string)
                subject to visualize
                flag: %s, position: 1
        surface: (a string)
                surface to visualize
                flag: %s, position: 3

        [Optional]
        annot_file: (an existing file name)
                path to annotation file to display
                flag: -annotation %s
                mutually_exclusive: annot_name
        annot_name: (a string)
                name of annotation to display (must be in $subject/label directory
                flag: -annotation %s
                mutually_exclusive: annot_file
        args: (a unicode string)
                Additional parameters to the command
                flag: %s
        colortable: (an existing file name)
                load colortable file
                flag: -colortable %s
        demean_overlay: (a boolean)
                remove mean from overlay
                flag: -zm
        environ: (a dictionary with keys which are a bytes or None or a value
                 of class 'str' and with values which are a bytes or None or a value
                 of class 'str', nipype default value: {})
                Environment variables
        identity_reg: (a boolean)
                use the identity matrix to register the overlay to the surface
                flag: -overlay-reg-identity
                mutually_exclusive: overlay_reg, identity_reg, mni152_reg
        ignore_exception: (a boolean, nipype default value: False)
                Print an error message instead of throwing an exception in case the
                interface fails to run
        invert_overlay: (a boolean)
                invert the overlay display
                flag: -invphaseflag 1
        label_file: (an existing file name)
                path to label file to display
                flag: -label %s
                mutually_exclusive: label_name
        label_name: (a string)
                name of label to display (must be in $subject/label directory
                flag: -label %s
                mutually_exclusive: label_file
        label_outline: (a boolean)
                draw label/annotation as outline
                flag: -label-outline
        label_under: (a boolean)
                draw label/annotation under overlay
                flag: -labels-under
        mni152_reg: (a boolean)
                use to display a volume in MNI152 space on the average subject
                flag: -mni152reg
                mutually_exclusive: overlay_reg, identity_reg, mni152_reg
        orig_suffix: (a string)
                set the orig surface suffix string
                flag: -orig %s
        overlay: (an existing file name)
                load an overlay volume/surface
                flag: -overlay %s
                requires: overlay_range
        overlay_range: (a float or a tuple of the form: (a float, a float) or
                 a tuple of the form: (a float, a float, a float))
                overlay range--either min, (min, max) or (min, mid, max)
                flag: %s
        overlay_range_offset: (a float)
                overlay range will be symettric around offset value
                flag: -foffset %.3f
        overlay_reg: (a file name)
                registration matrix file to register overlay to surface
                flag: -overlay-reg %s
                mutually_exclusive: overlay_reg, identity_reg, mni152_reg
        patch_file: (an existing file name)
                load a patch
                flag: -patch %s
        reverse_overlay: (a boolean)
                reverse the overlay display
                flag: -revphaseflag 1
        screenshot_stem: (a string)
                stem to use for screenshot file names
        show_color_scale: (a boolean)
                display the color scale bar
                flag: -colscalebarflag 1
        show_color_text: (a boolean)
                display text in the color scale bar
                flag: -colscaletext 1
        show_curv: (a boolean)
                show curvature
                flag: -curv
                mutually_exclusive: show_gray_curv
        show_gray_curv: (a boolean)
                show curvature in gray
                flag: -gray
                mutually_exclusive: show_curv
        six_images: (a boolean)
                also take anterior and posterior snapshots
        sphere_suffix: (a string)
                set the sphere.reg suffix string
                flag: -sphere %s
        stem_template_args: (a list of items which are a string)
                input names to use as arguments for a string-formated stem template
                requires: screenshot_stem
        subjects_dir: (an existing directory name)
                subjects directory
        tcl_script: (an existing file name)
                override default screenshot script
                flag: %s
        terminal_output: ('stream' or 'allatonce' or 'file' or 'none')
                Control terminal output: `stream` - displays to terminal immediately
                (default), `allatonce` - waits till command is finished to display
                output, `file` - writes output to file, `none` - output is ignored
        truncate_overlay: (a boolean)
                truncate the overlay display
                flag: -truncphaseflag 1

Outputs::

        snapshots: (a list of items which are an existing file name)
                tiff images of the surface from different perspectives

.. _nipype.interfaces.freesurfer.utils.SurfaceTransform:


.. index:: SurfaceTransform

SurfaceTransform
----------------

`Link to code <http://github.com/nipy/nipype/tree/ec86b7476/nipype/interfaces/freesurfer/utils.py#L393>`__

Wraps command **mri_surf2surf**

Transform a surface file from one subject to another via a spherical registration.

Both the source and target subject must reside in your Subjects Directory,
and they must have been processed with recon-all, unless you are transforming
to one of the icosahedron meshes.

Examples
~~~~~~~~

>>> from nipype.interfaces.freesurfer import SurfaceTransform
>>> sxfm = SurfaceTransform()
>>> sxfm.inputs.source_file = "lh.cope1.nii.gz"
>>> sxfm.inputs.source_subject = "my_subject"
>>> sxfm.inputs.target_subject = "fsaverage"
>>> sxfm.inputs.hemi = "lh"
>>> sxfm.run() # doctest: +SKIP

Inputs::

        [Mandatory]
        hemi: ('lh' or 'rh')
                hemisphere to transform
                flag: --hemi %s
        source_annot_file: (an existing file name)
                surface annotation file
                flag: --sval-annot %s
                mutually_exclusive: source_file
        source_file: (an existing file name)
                surface file with source values
                flag: --sval %s
                mutually_exclusive: source_annot_file
        source_subject: (a string)
                subject id for source surface
                flag: --srcsubject %s
        target_subject: (a string)
                subject id of target surface
                flag: --trgsubject %s

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
                surface file to write
                flag: --tval %s
        reshape: (a boolean)
                reshape output surface to conform with Nifti
                flag: --reshape
        reshape_factor: (an integer (int or long))
                number of slices in reshaped image
                flag: --reshape-factor
        source_type: ('cor' or 'mgh' or 'mgz' or 'minc' or 'analyze' or
                 'analyze4d' or 'spm' or 'afni' or 'brik' or 'bshort' or 'bfloat' or
                 'sdt' or 'outline' or 'otl' or 'gdf' or 'nifti1' or 'nii' or
                 'niigz')
                source file format
                flag: --sfmt %s
                requires: source_file
        subjects_dir: (an existing directory name)
                subjects directory
        target_ico_order: (1 or 2 or 3 or 4 or 5 or 6 or 7)
                order of the icosahedron if target_subject is 'ico'
                flag: --trgicoorder %d
        target_type: ('cor' or 'mgh' or 'mgz' or 'minc' or 'analyze' or
                 'analyze4d' or 'spm' or 'afni' or 'brik' or 'bshort' or 'bfloat' or
                 'sdt' or 'outline' or 'otl' or 'gdf' or 'nifti1' or 'nii' or
                 'niigz' or 'gii')
                output format
                flag: --tfmt %s
        terminal_output: ('stream' or 'allatonce' or 'file' or 'none')
                Control terminal output: `stream` - displays to terminal immediately
                (default), `allatonce` - waits till command is finished to display
                output, `file` - writes output to file, `none` - output is ignored

Outputs::

        out_file: (an existing file name)
                transformed surface file

.. _nipype.interfaces.freesurfer.utils.TalairachAVI:


.. index:: TalairachAVI

TalairachAVI
------------

`Link to code <http://github.com/nipy/nipype/tree/ec86b7476/nipype/interfaces/freesurfer/utils.py#L1554>`__

Wraps command **talairach_avi**

Front-end for Avi Snyders image registration tool. Computes the
talairach transform that maps the input volume to the MNI average_305.
This does not add the xfm to the header of the input file. When called
by recon-all, the xfm is added to the header after the transform is
computed.

Examples
~~~~~~~~

>>> from nipype.interfaces.freesurfer import TalairachAVI
>>> example = TalairachAVI()
>>> example.inputs.in_file = 'norm.mgz'
>>> example.inputs.out_file = 'trans.mat'
>>> example.cmdline # doctest: +ALLOW_UNICODE
'talairach_avi --i norm.mgz --xfm trans.mat'

>>> example.run() # doctest: +SKIP

Inputs::

        [Mandatory]
        in_file: (an existing file name)
                input volume
                flag: --i %s
        out_file: (a file name)
                output xfm file
                flag: --xfm %s

        [Optional]
        args: (a unicode string)
                Additional parameters to the command
                flag: %s
        atlas: (a string)
                alternate target atlas (in freesurfer/average dir)
                flag: --atlas %s
        environ: (a dictionary with keys which are a bytes or None or a value
                 of class 'str' and with values which are a bytes or None or a value
                 of class 'str', nipype default value: {})
                Environment variables
        ignore_exception: (a boolean, nipype default value: False)
                Print an error message instead of throwing an exception in case the
                interface fails to run
        subjects_dir: (an existing directory name)
                subjects directory
        terminal_output: ('stream' or 'allatonce' or 'file' or 'none')
                Control terminal output: `stream` - displays to terminal immediately
                (default), `allatonce` - waits till command is finished to display
                output, `file` - writes output to file, `none` - output is ignored

Outputs::

        out_file: (a file name)
                The output transform for TalairachAVI
        out_log: (a file name)
                The output log file for TalairachAVI
        out_txt: (a file name)
                The output text file for TaliarachAVI

.. _nipype.interfaces.freesurfer.utils.TalairachQC:


.. index:: TalairachQC

TalairachQC
-----------

`Link to code <http://github.com/nipy/nipype/tree/ec86b7476/nipype/interfaces/freesurfer/utils.py#L1592>`__

Wraps command **tal_QC_AZS**

Examples
~~~~~~~~

>>> from nipype.interfaces.freesurfer import TalairachQC
>>> qc = TalairachQC()
>>> qc.inputs.log_file = 'dirs.txt'
>>> qc.cmdline # doctest: +ALLOW_UNICODE
'tal_QC_AZS dirs.txt'

Inputs::

        [Mandatory]
        log_file: (an existing file name)
                The log file for TalairachQC
                flag: %s, position: 0

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
        subjects_dir: (an existing directory name)
                subjects directory
        terminal_output: ('stream' or 'allatonce' or 'file' or 'none')
                Control terminal output: `stream` - displays to terminal immediately
                (default), `allatonce` - waits till command is finished to display
                output, `file` - writes output to file, `none` - output is ignored

Outputs::

        log_file: (an existing file name, nipype default value:
                 stdout.nipype)
                The output log

.. _nipype.interfaces.freesurfer.utils.Tkregister2:


.. index:: Tkregister2

Tkregister2
-----------

`Link to code <http://github.com/nipy/nipype/tree/ec86b7476/nipype/interfaces/freesurfer/utils.py#L1379>`__

Wraps command **tkregister2**

Examples
~~~~~~~~

Get transform matrix between orig (*tkRAS*) and native (*scannerRAS*)
coordinates in Freesurfer. Implements the first step of mapping surfaces
to native space in `this guide
<http://surfer.nmr.mgh.harvard.edu/fswiki/FsAnat-to-NativeAnat>`_.

>>> from nipype.interfaces.freesurfer import Tkregister2
>>> tk2 = Tkregister2(reg_file='T1_to_native.dat')
>>> tk2.inputs.moving_image = 'T1.mgz'
>>> tk2.inputs.target_image = 'structural.nii'
>>> tk2.inputs.reg_header = True
>>> tk2.cmdline # doctest: +ALLOW_UNICODE
'tkregister2 --mov T1.mgz --noedit --reg T1_to_native.dat --regheader --targ structural.nii'
>>> tk2.run() # doctest: +SKIP

The example below uses tkregister2 without the manual editing
stage to convert FSL-style registration matrix (.mat) to
FreeSurfer-style registration matrix (.dat)

>>> from nipype.interfaces.freesurfer import Tkregister2
>>> tk2 = Tkregister2()
>>> tk2.inputs.moving_image = 'epi.nii'
>>> tk2.inputs.fsl_in_matrix = 'flirt.mat'
>>> tk2.cmdline # doctest: +ALLOW_UNICODE
'tkregister2 --fsl flirt.mat --mov epi.nii --noedit --reg register.dat'
>>> tk2.run() # doctest: +SKIP

Inputs::

        [Mandatory]
        moving_image: (an existing file name)
                moving volume
                flag: --mov %s
        reg_file: (a file name, nipype default value: register.dat)
                freesurfer-style registration file
                flag: --reg %s

        [Optional]
        args: (a unicode string)
                Additional parameters to the command
                flag: %s
        environ: (a dictionary with keys which are a bytes or None or a value
                 of class 'str' and with values which are a bytes or None or a value
                 of class 'str', nipype default value: {})
                Environment variables
        fsl_in_matrix: (an existing file name)
                fsl-style registration input matrix
                flag: --fsl %s
        fsl_out: (a file name)
                compute an FSL-compatible resgitration matrix
                flag: --fslregout %s
        fstal: (a boolean)
                set mov to be tal and reg to be tal xfm
                flag: --fstal
                mutually_exclusive: target_image, moving_image
        fstarg: (a boolean)
                use subject's T1 as reference
                flag: --fstarg
                mutually_exclusive: target_image
        ignore_exception: (a boolean, nipype default value: False)
                Print an error message instead of throwing an exception in case the
                interface fails to run
        movscale: (a float)
                adjust registration matrix to scale mov
                flag: --movscale %f
        noedit: (a boolean, nipype default value: True)
                do not open edit window (exit)
                flag: --noedit
        reg_header: (a boolean)
                compute regstration from headers
                flag: --regheader
        subject_id: (a string)
                freesurfer subject ID
                flag: --s %s
        subjects_dir: (an existing directory name)
                subjects directory
        target_image: (an existing file name)
                target volume
                flag: --targ %s
                mutually_exclusive: fstarg
        terminal_output: ('stream' or 'allatonce' or 'file' or 'none')
                Control terminal output: `stream` - displays to terminal immediately
                (default), `allatonce` - waits till command is finished to display
                output, `file` - writes output to file, `none` - output is ignored
        xfm: (an existing file name)
                use a matrix in MNI coordinates as initial registration
                flag: --xfm %s

Outputs::

        fsl_file: (a file name)
                FSL-style registration file
        reg_file: (an existing file name)
                freesurfer-style registration file

.. _nipype.interfaces.freesurfer.utils.VolumeMask:


.. index:: VolumeMask

VolumeMask
----------

`Link to code <http://github.com/nipy/nipype/tree/ec86b7476/nipype/interfaces/freesurfer/utils.py#L2432>`__

Wraps command **mris_volmask**

Computes a volume mask, at the same resolution as the
<subject>/mri/brain.mgz.  The volume mask contains 4 values: LH_WM
(default 10), LH_GM (default 100), RH_WM (default 20), RH_GM (default
200).
The algorithm uses the 4 surfaces situated in <subject>/surf/
[lh|rh].[white|pial] and labels voxels based on the
signed-distance function from the surface.

Examples
~~~~~~~~
>>> from nipype.interfaces.freesurfer import VolumeMask
>>> volmask = VolumeMask()
>>> volmask.inputs.left_whitelabel = 2
>>> volmask.inputs.left_ribbonlabel = 3
>>> volmask.inputs.right_whitelabel = 41
>>> volmask.inputs.right_ribbonlabel = 42
>>> volmask.inputs.lh_pial = 'lh.pial'
>>> volmask.inputs.rh_pial = 'lh.pial'
>>> volmask.inputs.lh_white = 'lh.pial'
>>> volmask.inputs.rh_white = 'lh.pial'
>>> volmask.inputs.subject_id = '10335'
>>> volmask.inputs.save_ribbon = True
>>> volmask.cmdline # doctest: +ALLOW_UNICODE
'mris_volmask --label_left_ribbon 3 --label_left_white 2 --label_right_ribbon 42 --label_right_white 41 --save_ribbon 10335'

Inputs::

        [Mandatory]
        left_ribbonlabel: (an integer (int or long))
                Left cortical ribbon label
                flag: --label_left_ribbon %d
        left_whitelabel: (an integer (int or long))
                Left white matter label
                flag: --label_left_white %d
        lh_pial: (an existing file name)
                Implicit input left pial surface
        lh_white: (an existing file name)
                Implicit input left white matter surface
        rh_pial: (an existing file name)
                Implicit input right pial surface
        rh_white: (an existing file name)
                Implicit input right white matter surface
        right_ribbonlabel: (an integer (int or long))
                Right cortical ribbon label
                flag: --label_right_ribbon %d
        right_whitelabel: (an integer (int or long))
                Right white matter label
                flag: --label_right_white %d
        subject_id: (a string, nipype default value: subject_id)
                Subject being processed
                flag: %s, position: -1

        [Optional]
        args: (a unicode string)
                Additional parameters to the command
                flag: %s
        aseg: (an existing file name)
                Implicit aseg.mgz segmentation. Specify a different aseg by using
                the 'in_aseg' input.
                mutually_exclusive: in_aseg
        copy_inputs: (a boolean)
                If running as a node, set this to True.This will copy the implicit
                input files to the node directory.
        environ: (a dictionary with keys which are a bytes or None or a value
                 of class 'str' and with values which are a bytes or None or a value
                 of class 'str', nipype default value: {})
                Environment variables
        ignore_exception: (a boolean, nipype default value: False)
                Print an error message instead of throwing an exception in case the
                interface fails to run
        in_aseg: (an existing file name)
                Input aseg file for VolumeMask
                flag: --aseg_name %s
                mutually_exclusive: aseg
        save_ribbon: (a boolean)
                option to save just the ribbon for the hemispheres in the format
                ?h.ribbon.mgz
                flag: --save_ribbon
        subjects_dir: (an existing directory name)
                subjects directory
        terminal_output: ('stream' or 'allatonce' or 'file' or 'none')
                Control terminal output: `stream` - displays to terminal immediately
                (default), `allatonce` - waits till command is finished to display
                output, `file` - writes output to file, `none` - output is ignored

Outputs::

        lh_ribbon: (a file name)
                Output left cortical ribbon mask
        out_ribbon: (a file name)
                Output cortical ribbon mask
        rh_ribbon: (a file name)
                Output right cortical ribbon mask

.. module:: nipype.interfaces.freesurfer.utils


.. _nipype.interfaces.freesurfer.utils.copy2subjdir:

:func:`copy2subjdir`
--------------------

`Link to code <http://github.com/nipy/nipype/tree/ec86b7476/nipype/interfaces/freesurfer/utils.py#L43>`__



Method to copy an input to the subjects directory


.. _nipype.interfaces.freesurfer.utils.createoutputdirs:

:func:`createoutputdirs`
------------------------

`Link to code <http://github.com/nipy/nipype/tree/ec86b7476/nipype/interfaces/freesurfer/utils.py#L75>`__



create all output directories. If not created, some freesurfer interfaces fail

