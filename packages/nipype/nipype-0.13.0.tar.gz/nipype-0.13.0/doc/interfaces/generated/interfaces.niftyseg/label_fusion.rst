.. AUTO-GENERATED FILE -- DO NOT EDIT!

interfaces.niftyseg.label_fusion
================================


.. _nipype.interfaces.niftyseg.label_fusion.CalcTopNCC:


.. index:: CalcTopNCC

CalcTopNCC
----------

`Link to code <http://github.com/nipy/nipype/tree/ec86b7476/nipype/interfaces/niftyseg/label_fusion.py#L290>`__

Wraps command **seg_CalcTopNCC**

Interface for executable seg_CalcTopNCC from NiftySeg platform.

Examples
~~~~~~~~
>>> from nipype.interfaces import niftyseg
>>> node = niftyseg.CalcTopNCC()
>>> node.inputs.in_file = 'im1.nii'
>>> node.inputs.num_templates = 2
>>> node.inputs.in_templates = ['im2.nii', 'im3.nii']
>>> node.inputs.top_templates = 1
>>> node.cmdline  # doctest: +ALLOW_UNICODE
'seg_CalcTopNCC -target im1.nii -templates 2 im2.nii im3.nii -n 1'

Inputs::

        [Mandatory]
        in_file: (an existing file name)
                Target file
                flag: -target %s, position: 1
        in_templates: (a list of items which are an existing file name)
                flag: %s, position: 3
        num_templates: (an integer (int or long))
                Number of Templates
                flag: -templates %s, position: 2
        top_templates: (an integer (int or long))
                Number of Top Templates
                flag: -n %s, position: 4

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
        mask_file: (an existing file name)
                Filename of the ROI for label fusion
                flag: -mask %s
        terminal_output: ('stream' or 'allatonce' or 'file' or 'none')
                Control terminal output: `stream` - displays to terminal immediately
                (default), `allatonce` - waits till command is finished to display
                output, `file` - writes output to file, `none` - output is ignored

Outputs::

        out_files: (any value)

.. _nipype.interfaces.niftyseg.label_fusion.LabelFusion:


.. index:: LabelFusion

LabelFusion
-----------

`Link to code <http://github.com/nipy/nipype/tree/ec86b7476/nipype/interfaces/niftyseg/label_fusion.py#L116>`__

Wraps command **seg_LabFusion**

Interface for executable seg_LabelFusion from NiftySeg platform using
type STEPS as classifier Fusion.

This executable implements 4 fusion strategies (-STEPS, -STAPLE, -MV or
- SBA), all of them using either a global (-GNCC), ROI-based (-ROINCC),
local (-LNCC) or no image similarity (-ALL). Combinations of fusion
algorithms and similarity metrics give rise to different variants of known
algorithms. As an example, using LNCC and MV as options will run a locally
weighted voting strategy with LNCC derived weights, while using STAPLE and
LNCC is equivalent to running STEPS as per its original formulation.
A few other options pertaining the use of an MRF (-MRF beta), the initial
sensitivity and specificity estimates and the use of only non-consensus
voxels (-unc) for the STAPLE and STEPS algorithm. All processing can be
masked (-mask), greatly reducing memory consumption.

As an example, the command to use STEPS should be:
seg_LabFusion -in 4D_Propragated_Labels_to_fuse.nii -out     FusedSegmentation.nii -STEPS 2 15 TargetImage.nii     4D_Propagated_Intensities.nii

`Source code <http://cmictig.cs.ucl.ac.uk/wiki/index.php/NiftySeg>`_ |
`Documentation <http://cmictig.cs.ucl.ac.uk/wiki/index.php/NiftySeg_documentation>`_

Examples
~~~~~~~~
>>> from nipype.interfaces import niftyseg
>>> node = niftyseg.LabelFusion()
>>> node.inputs.in_file = 'im1.nii'
>>> node.inputs.kernel_size = 2.0
>>> node.inputs.file_to_seg = 'im2.nii'
>>> node.inputs.template_file = 'im3.nii'
>>> node.inputs.template_num = 2
>>> node.inputs.classifier_type = 'STEPS'
>>> node.cmdline  # doctest: +ALLOW_UNICODE
'seg_LabFusion -in im1.nii -STEPS 2.000000 2 im2.nii im3.nii -out im1_steps.nii'

Inputs::

        [Mandatory]
        classifier_type: ('STEPS' or 'STAPLE' or 'MV' or 'SBA')
                Type of Classifier Fusion.
                flag: -%s, position: 2
        file_to_seg: (an existing file name)
                Original image to segment (3D Image)
        in_file: (an existing file name)
                Filename of the 4D integer label image.
                flag: -in %s, position: 1

        [Optional]
        args: (a unicode string)
                Additional parameters to the command
                flag: %s
        conv: (a float)
                Ratio for convergence (default epsilon = 10^-5).
                flag: -conv %f
        dilation_roi: (an integer (int or long))
                Dilation of the ROI ( <int> d>=1 )
        environ: (a dictionary with keys which are a bytes or None or a value
                 of class 'str' and with values which are a bytes or None or a value
                 of class 'str', nipype default value: {})
                Environment variables
        ignore_exception: (a boolean, nipype default value: False)
                Print an error message instead of throwing an exception in case the
                interface fails to run
        kernel_size: (a float)
                Gaussian kernel size in mm to compute the local similarity
        mask_file: (an existing file name)
                Filename of the ROI for label fusion
                flag: -mask %s
        max_iter: (an integer (int or long))
                Maximum number of iterations (default = 15).
                flag: -max_iter %d
        mrf_value: (a float)
                MRF prior strength (between 0 and 5)
                flag: -MRF_beta %f
        out_file: (a file name)
                Output consensus segmentation
                flag: -out %s
        prob_flag: (a boolean)
                Probabilistic/Fuzzy segmented image
                flag: -outProb
        prob_update_flag: (a boolean)
                Update label proportions at each iteration
                flag: -prop_update
        proportion: (a float)
                Proportion of the label (only for single labels).
                flag: -prop %s
        set_pq: (a tuple of the form: (a float, a float))
                Value of P and Q [ 0 < (P,Q) < 1 ] (default = 0.99 0.99)
                flag: -setPQ %f %f
        sm_ranking: ('ALL' or 'GNCC' or 'ROINCC' or 'LNCC', nipype default
                 value: ALL)
                Ranking for STAPLE and MV
                flag: -%s, position: 3
        template_file: (an existing file name)
                Registered templates (4D Image)
        template_num: (an integer (int or long))
                Number of labels to use
        terminal_output: ('stream' or 'allatonce' or 'file' or 'none')
                Control terminal output: `stream` - displays to terminal immediately
                (default), `allatonce` - waits till command is finished to display
                output, `file` - writes output to file, `none` - output is ignored
        unc: (a boolean)
                Only consider non-consensus voxels to calculate statistics
                flag: -unc
        unc_thresh: (a float)
                If <float> percent of labels agree, then area is not uncertain.
                flag: -uncthres %f
        verbose: ('0' or '1' or '2')
                Verbose level [0 = off, 1 = on, 2 = debug] (default = 0)
                flag: -v %s

Outputs::

        out_file: (an existing file name)
                image written after calculations
