.. AUTO-GENERATED FILE -- DO NOT EDIT!

interfaces.ants.segmentation
============================


.. _nipype.interfaces.ants.segmentation.AntsJointFusion:


.. index:: AntsJointFusion

AntsJointFusion
---------------

`Link to code <http://github.com/nipy/nipype/tree/ec86b7476/nipype/interfaces/ants/segmentation.py#L1071>`__

Wraps command **antsJointFusion**

Examples
~~~~~~~~

>>> from nipype.interfaces.ants import AntsJointFusion
>>> antsjointfusion = AntsJointFusion()
>>> antsjointfusion.inputs.out_label_fusion = 'ants_fusion_label_output.nii'
>>> antsjointfusion.inputs.atlas_image = [ ['rc1s1.nii','rc1s2.nii'] ]
>>> antsjointfusion.inputs.atlas_segmentation_image = ['segmentation0.nii.gz']
>>> antsjointfusion.inputs.target_image = ['im1.nii']
>>> antsjointfusion.cmdline # doctest: +ALLOW_UNICODE
"antsJointFusion -a 0.1 -g ['rc1s1.nii', 'rc1s2.nii'] -l segmentation0.nii.gz -b 2.0 -o ants_fusion_label_output.nii -s 3x3x3 -t ['im1.nii']"

>>> antsjointfusion.inputs.target_image = [ ['im1.nii', 'im2.nii'] ]
>>> antsjointfusion.cmdline # doctest: +ALLOW_UNICODE
"antsJointFusion -a 0.1 -g ['rc1s1.nii', 'rc1s2.nii'] -l segmentation0.nii.gz -b 2.0 -o ants_fusion_label_output.nii -s 3x3x3 -t ['im1.nii', 'im2.nii']"

>>> antsjointfusion.inputs.atlas_image = [ ['rc1s1.nii','rc1s2.nii'],
...                                        ['rc2s1.nii','rc2s2.nii'] ]
>>> antsjointfusion.inputs.atlas_segmentation_image = ['segmentation0.nii.gz',
...                                                    'segmentation1.nii.gz']
>>> antsjointfusion.cmdline # doctest: +ALLOW_UNICODE
"antsJointFusion -a 0.1 -g ['rc1s1.nii', 'rc1s2.nii'] -g ['rc2s1.nii', 'rc2s2.nii'] -l segmentation0.nii.gz -l segmentation1.nii.gz -b 2.0 -o ants_fusion_label_output.nii -s 3x3x3 -t ['im1.nii', 'im2.nii']"

>>> antsjointfusion.inputs.dimension = 3
>>> antsjointfusion.inputs.alpha = 0.5
>>> antsjointfusion.inputs.beta = 1.0
>>> antsjointfusion.inputs.patch_radius = [3,2,1]
>>> antsjointfusion.inputs.search_radius = [3]
>>> antsjointfusion.cmdline # doctest: +ALLOW_UNICODE
"antsJointFusion -a 0.5 -g ['rc1s1.nii', 'rc1s2.nii'] -g ['rc2s1.nii', 'rc2s2.nii'] -l segmentation0.nii.gz -l segmentation1.nii.gz -b 1.0 -d 3 -o ants_fusion_label_output.nii -p 3x2x1 -s 3 -t ['im1.nii', 'im2.nii']"

>>> antsjointfusion.inputs.search_radius = ['mask.nii']
>>> antsjointfusion.inputs.verbose = True
>>> antsjointfusion.inputs.exclusion_image = ['roi01.nii', 'roi02.nii']
>>> antsjointfusion.inputs.exclusion_image_label = ['1','2']
>>> antsjointfusion.cmdline # doctest: +ALLOW_UNICODE
"antsJointFusion -a 0.5 -g ['rc1s1.nii', 'rc1s2.nii'] -g ['rc2s1.nii', 'rc2s2.nii'] -l segmentation0.nii.gz -l segmentation1.nii.gz -b 1.0 -d 3 -e 1[roi01.nii] -e 2[roi02.nii] -o ants_fusion_label_output.nii -p 3x2x1 -s mask.nii -t ['im1.nii', 'im2.nii'] -v"

>>> antsjointfusion.inputs.out_label_fusion = 'ants_fusion_label_output.nii'
>>> antsjointfusion.inputs.out_intensity_fusion_name_format = 'ants_joint_fusion_intensity_%d.nii.gz'
>>> antsjointfusion.inputs.out_label_post_prob_name_format = 'ants_joint_fusion_posterior_%d.nii.gz'
>>> antsjointfusion.inputs.out_atlas_voting_weight_name_format = 'ants_joint_fusion_voting_weight_%d.nii.gz'
>>> antsjointfusion.cmdline # doctest: +ALLOW_UNICODE
"antsJointFusion -a 0.5 -g ['rc1s1.nii', 'rc1s2.nii'] -g ['rc2s1.nii', 'rc2s2.nii'] -l segmentation0.nii.gz -l segmentation1.nii.gz -b 1.0 -d 3 -e 1[roi01.nii] -e 2[roi02.nii]  -o [ants_fusion_label_output.nii, ants_joint_fusion_intensity_%d.nii.gz, ants_joint_fusion_posterior_%d.nii.gz, ants_joint_fusion_voting_weight_%d.nii.gz] -p 3x2x1 -s mask.nii -t ['im1.nii', 'im2.nii'] -v"

Inputs::

        [Mandatory]
        atlas_image: (a list of items which are a list of items which are an
                 existing file name)
                The atlas image (or multimodal atlas images) assumed to be aligned
                to a common image domain.
                flag: -g %s...
        atlas_segmentation_image: (a list of items which are an existing file
                 name)
                The atlas segmentation images. For performing label fusion the
                number of specified segmentations should be identical to the number
                of atlas image sets.
                flag: -l %s...
        target_image: (a list of items which are a list of items which are an
                 existing file name)
                The target image (or multimodal target images) assumed to be aligned
                to a common image domain.
                flag: -t %s

        [Optional]
        alpha: (a float, nipype default value: 0.1)
                Regularization term added to matrix Mx for calculating the inverse.
                Default = 0.1
                flag: -a %s
        args: (a unicode string)
                Additional parameters to the command
                flag: %s
        beta: (a float, nipype default value: 2.0)
                Exponent for mapping intensity difference to the joint error.
                Default = 2.0
                flag: -b %s
        constrain_nonnegative: (a boolean, nipype default value: False)
                Constrain solution to non-negative weights.
                flag: -c
        dimension: (3 or 2 or 4)
                This option forces the image to be treated as a specified-
                dimensional image. If not specified, the program tries to infer the
                dimensionality from the input image.
                flag: -d %d
        environ: (a dictionary with keys which are a bytes or None or a value
                 of class 'str' and with values which are a bytes or None or a value
                 of class 'str', nipype default value: {})
                Environment variables
        exclusion_image: (a list of items which are an existing file name)
                Specify an exclusion region for the given label.
        exclusion_image_label: (a list of items which are a unicode string)
                Specify a label for the exclusion region.
                flag: -e %s
                requires: exclusion_image
        ignore_exception: (a boolean, nipype default value: False)
                Print an error message instead of throwing an exception in case the
                interface fails to run
        mask_image: (an existing file name)
                If a mask image is specified, fusion is only performed in the mask
                region.
                flag: -x %s
        num_threads: (an integer (int or long), nipype default value: 1)
                Number of ITK threads to use
        out_atlas_voting_weight_name_format: (a unicode string)
                Optional atlas voting weight image file name format.
                requires: out_label_fusion, out_intensity_fusion_name_format,
                 out_label_post_prob_name_format
        out_intensity_fusion_name_format: (a unicode string)
                Optional intensity fusion image file name format.
        out_label_fusion: (a file name)
                The output label fusion image.
                flag: %s
        out_label_post_prob_name_format: (a unicode string)
                Optional label posterior probability image file name format.
                requires: out_label_fusion, out_intensity_fusion_name_format
        patch_metric: ('PC' or 'MSQ')
                Metric to be used in determining the most similar neighborhood
                patch. Options include Pearson's correlation (PC) and mean squares
                (MSQ). Default = PC (Pearson correlation).
                flag: -m %s
        patch_radius: (a list of items which are a value of class 'int')
                Patch radius for similarity measures.Default: 2x2x2
                flag: -p %s
        retain_atlas_voting_images: (a boolean, nipype default value: False)
                Retain atlas voting images. Default = false
                flag: -f
        retain_label_posterior_images: (a boolean, nipype default value:
                 False)
                Retain label posterior probability images. Requires atlas
                segmentations to be specified. Default = false
                flag: -r
                requires: atlas_segmentation_image
        search_radius: (a list of from 1 to 3 items which are any value,
                 nipype default value: [3, 3, 3])
                Search radius for similarity measures. Default = 3x3x3. One can also
                specify an image where the value at the voxel specifies the
                isotropic search radius at that voxel.
                flag: -s %s
        terminal_output: ('stream' or 'allatonce' or 'file' or 'none')
                Control terminal output: `stream` - displays to terminal immediately
                (default), `allatonce` - waits till command is finished to display
                output, `file` - writes output to file, `none` - output is ignored
        verbose: (a boolean)
                Verbose output.
                flag: -v

Outputs::

        out_atlas_voting_weight_name_format: (a unicode string)
        out_intensity_fusion_name_format: (a unicode string)
        out_label_fusion: (an existing file name)
        out_label_post_prob_name_format: (a unicode string)

.. _nipype.interfaces.ants.segmentation.Atropos:


.. index:: Atropos

Atropos
-------

`Link to code <http://github.com/nipy/nipype/tree/ec86b7476/nipype/interfaces/ants/segmentation.py#L64>`__

Wraps command **Atropos**

A finite mixture modeling (FMM) segmentation approach with possibilities for
specifying prior constraints. These prior constraints include the specification
of a prior label image, prior probability images (one for each class), and/or an
MRF prior to enforce spatial smoothing of the labels. Similar algorithms include
FAST and SPM.

Examples
~~~~~~~~

>>> from nipype.interfaces.ants import Atropos
>>> at = Atropos()
>>> at.inputs.dimension = 3
>>> at.inputs.intensity_images = 'structural.nii'
>>> at.inputs.mask_image = 'mask.nii'
>>> at.inputs.initialization = 'PriorProbabilityImages'
>>> at.inputs.prior_probability_images = ['rc1s1.nii', 'rc1s2.nii']
>>> at.inputs.number_of_tissue_classes = 2
>>> at.inputs.prior_weighting = 0.8
>>> at.inputs.prior_probability_threshold = 0.0000001
>>> at.inputs.likelihood_model = 'Gaussian'
>>> at.inputs.mrf_smoothing_factor = 0.2
>>> at.inputs.mrf_radius = [1, 1, 1]
>>> at.inputs.icm_use_synchronous_update = True
>>> at.inputs.maximum_number_of_icm_terations = 1
>>> at.inputs.n_iterations = 5
>>> at.inputs.convergence_threshold = 0.000001
>>> at.inputs.posterior_formulation = 'Socrates'
>>> at.inputs.use_mixture_model_proportions = True
>>> at.inputs.save_posteriors = True
>>> at.cmdline # doctest: +ALLOW_UNICODE
'Atropos --image-dimensionality 3 --icm [1,1] --initialization PriorProbabilityImages[2,priors/priorProbImages%02d.nii,0.8,1e-07] --intensity-image structural.nii --likelihood-model Gaussian --mask-image mask.nii --mrf [0.2,1x1x1] --convergence [5,1e-06] --output [structural_labeled.nii,POSTERIOR_%02d.nii.gz] --posterior-formulation Socrates[1] --use-random-seed 1'

Inputs::

        [Mandatory]
        initialization: ('Random' or 'Otsu' or 'KMeans' or
                 'PriorProbabilityImages' or 'PriorLabelImage')
                flag: %s
                requires: number_of_tissue_classes
        intensity_images: (a list of items which are an existing file name)
                flag: --intensity-image %s...
        mask_image: (an existing file name)
                flag: --mask-image %s
        number_of_tissue_classes: (an integer (int or long))

        [Optional]
        args: (a unicode string)
                Additional parameters to the command
                flag: %s
        convergence_threshold: (a float)
                requires: n_iterations
        dimension: (3 or 2 or 4, nipype default value: 3)
                image dimension (2, 3, or 4)
                flag: --image-dimensionality %d
        environ: (a dictionary with keys which are a bytes or None or a value
                 of class 'str' and with values which are a bytes or None or a value
                 of class 'str', nipype default value: {})
                Environment variables
        icm_use_synchronous_update: (a boolean)
                flag: %s
        ignore_exception: (a boolean, nipype default value: False)
                Print an error message instead of throwing an exception in case the
                interface fails to run
        likelihood_model: (a unicode string)
                flag: --likelihood-model %s
        maximum_number_of_icm_terations: (an integer (int or long))
                requires: icm_use_synchronous_update
        mrf_radius: (a list of items which are an integer (int or long))
                requires: mrf_smoothing_factor
        mrf_smoothing_factor: (a float)
                flag: %s
        n_iterations: (an integer (int or long))
                flag: %s
        num_threads: (an integer (int or long), nipype default value: 1)
                Number of ITK threads to use
        out_classified_image_name: (a file name)
                flag: %s
        output_posteriors_name_template: (a unicode string, nipype default
                 value: POSTERIOR_%02d.nii.gz)
        posterior_formulation: (a unicode string)
                flag: %s
        prior_probability_images: (a list of items which are an existing file
                 name)
        prior_probability_threshold: (a float)
                requires: prior_weighting
        prior_weighting: (a float)
        save_posteriors: (a boolean)
        terminal_output: ('stream' or 'allatonce' or 'file' or 'none')
                Control terminal output: `stream` - displays to terminal immediately
                (default), `allatonce` - waits till command is finished to display
                output, `file` - writes output to file, `none` - output is ignored
        use_mixture_model_proportions: (a boolean)
                requires: posterior_formulation
        use_random_seed: (a boolean, nipype default value: True)
                use random seed value over constant
                flag: --use-random-seed %d

Outputs::

        classified_image: (an existing file name)
        posteriors: (a list of items which are a file name)

.. _nipype.interfaces.ants.segmentation.BrainExtraction:


.. index:: BrainExtraction

BrainExtraction
---------------

`Link to code <http://github.com/nipy/nipype/tree/ec86b7476/nipype/interfaces/ants/segmentation.py#L678>`__

Wraps command **antsBrainExtraction.sh**

Examples
~~~~~~~~
>>> from nipype.interfaces.ants.segmentation import BrainExtraction
>>> brainextraction = BrainExtraction()
>>> brainextraction.inputs.dimension = 3
>>> brainextraction.inputs.anatomical_image ='T1.nii.gz'
>>> brainextraction.inputs.brain_template = 'study_template.nii.gz'
>>> brainextraction.inputs.brain_probability_mask ='ProbabilityMaskOfStudyTemplate.nii.gz'
>>> brainextraction.cmdline # doctest: +ALLOW_UNICODE
'antsBrainExtraction.sh -a T1.nii.gz -m ProbabilityMaskOfStudyTemplate.nii.gz -e study_template.nii.gz -d 3 -s nii.gz -o highres001_'

Inputs::

        [Mandatory]
        anatomical_image: (an existing file name)
                Structural image, typically T1. If more than oneanatomical image is
                specified, subsequently specifiedimages are used during the
                segmentation process. However,only the first image is used in the
                registration of priors.Our suggestion would be to specify the T1 as
                the first image.Anatomical template created using e.g. LPBA40 data
                set withbuildtemplateparallel.sh in ANTs.
                flag: -a %s
        brain_probability_mask: (an existing file name)
                Brain probability mask created using e.g. LPBA40 data set whichhave
                brain masks defined, and warped to anatomical template andaveraged
                resulting in a probability image.
                flag: -m %s
        brain_template: (an existing file name)
                Anatomical template created using e.g. LPBA40 data set
                withbuildtemplateparallel.sh in ANTs.
                flag: -e %s

        [Optional]
        args: (a unicode string)
                Additional parameters to the command
                flag: %s
        debug: (a boolean)
                If > 0, runs a faster version of the script.Only for testing.
                Implies -u 0.Requires single thread computation for complete
                reproducibility.
                flag: -z 1
        dimension: (3 or 2, nipype default value: 3)
                image dimension (2 or 3)
                flag: -d %d
        environ: (a dictionary with keys which are a bytes or None or a value
                 of class 'str' and with values which are a bytes or None or a value
                 of class 'str', nipype default value: {})
                Environment variables
        extraction_registration_mask: (an existing file name)
                Mask (defined in the template space) used during registration for
                brain extraction.To limit the metric computation to a specific
                region.
                flag: -f %s
        ignore_exception: (a boolean, nipype default value: False)
                Print an error message instead of throwing an exception in case the
                interface fails to run
        image_suffix: (a unicode string, nipype default value: nii.gz)
                any of standard ITK formats, nii.gz is default
                flag: -s %s
        keep_temporary_files: (an integer (int or long))
                Keep brain extraction/segmentation warps, etc (default = 0).
                flag: -k %d
        num_threads: (an integer (int or long), nipype default value: 1)
                Number of ITK threads to use
        out_prefix: (a unicode string, nipype default value: highres001_)
                Prefix that is prepended to all output files (default =
                highress001_)
                flag: -o %s
        terminal_output: ('stream' or 'allatonce' or 'file' or 'none')
                Control terminal output: `stream` - displays to terminal immediately
                (default), `allatonce` - waits till command is finished to display
                output, `file` - writes output to file, `none` - output is ignored
        use_floatingpoint_precision: (0 or 1)
                Use floating point precision in registrations (default = 0)
                flag: -q %d
        use_random_seeding: (0 or 1)
                Use random number generated from system clock in Atropos(default =
                1)
                flag: -u %d

Outputs::

        BrainExtractionBrain: (an existing file name)
                brain extraction image
        BrainExtractionCSF: (an existing file name)
                segmentation mask with only CSF
        BrainExtractionGM: (an existing file name)
                segmentation mask with only grey matter
        BrainExtractionInitialAffine: (an existing file name)
        BrainExtractionInitialAffineFixed: (an existing file name)
        BrainExtractionInitialAffineMoving: (an existing file name)
        BrainExtractionLaplacian: (an existing file name)
        BrainExtractionMask: (an existing file name)
                brain extraction mask
        BrainExtractionPrior0GenericAffine: (an existing file name)
        BrainExtractionPrior1InverseWarp: (an existing file name)
        BrainExtractionPrior1Warp: (an existing file name)
        BrainExtractionPriorWarped: (an existing file name)
        BrainExtractionSegmentation: (an existing file name)
                segmentation mask with CSF, GM, and WM
        BrainExtractionTemplateLaplacian: (an existing file name)
        BrainExtractionTmp: (an existing file name)
        BrainExtractionWM: (an existing file name)
                segmenration mask with only white matter
        N4Corrected0: (an existing file name)
                N4 bias field corrected image
        N4Truncated0: (an existing file name)

.. _nipype.interfaces.ants.segmentation.CorticalThickness:


.. index:: CorticalThickness

CorticalThickness
-----------------

`Link to code <http://github.com/nipy/nipype/tree/ec86b7476/nipype/interfaces/ants/segmentation.py#L494>`__

Wraps command **antsCorticalThickness.sh**

Examples
~~~~~~~~
>>> from nipype.interfaces.ants.segmentation import CorticalThickness
>>> corticalthickness = CorticalThickness()
>>> corticalthickness.inputs.dimension = 3
>>> corticalthickness.inputs.anatomical_image ='T1.nii.gz'
>>> corticalthickness.inputs.brain_template = 'study_template.nii.gz'
>>> corticalthickness.inputs.brain_probability_mask ='ProbabilityMaskOfStudyTemplate.nii.gz'
>>> corticalthickness.inputs.segmentation_priors = ['BrainSegmentationPrior01.nii.gz',
...                                                 'BrainSegmentationPrior02.nii.gz',
...                                                 'BrainSegmentationPrior03.nii.gz',
...                                                 'BrainSegmentationPrior04.nii.gz']
>>> corticalthickness.inputs.t1_registration_template = 'brain_study_template.nii.gz'
>>> corticalthickness.cmdline # doctest: +ALLOW_UNICODE
'antsCorticalThickness.sh -a T1.nii.gz -m ProbabilityMaskOfStudyTemplate.nii.gz -e study_template.nii.gz -d 3 -s nii.gz -o antsCT_ -p nipype_priors/BrainSegmentationPrior%02d.nii.gz -t brain_study_template.nii.gz'

Inputs::

        [Mandatory]
        anatomical_image: (an existing file name)
                Structural *intensity* image, typically T1.If more than one
                anatomical image is specified,subsequently specified images are used
                during thesegmentation process. However, only the firstimage is used
                in the registration of priors.Our suggestion would be to specify the
                T1as the first image.
                flag: -a %s
        brain_probability_mask: (an existing file name)
                brain probability mask in template space
                flag: -m %s
        brain_template: (an existing file name)
                Anatomical *intensity* template (possibly created using apopulation
                data set with buildtemplateparallel.sh in ANTs).This template is
                *not* skull-stripped.
                flag: -e %s
        segmentation_priors: (a list of items which are an existing file
                 name)
                flag: -p %s
        t1_registration_template: (an existing file name)
                Anatomical *intensity* template(assumed to be skull-stripped). A
                commoncase would be where this would be the sametemplate as
                specified in the -e option whichis not skull stripped.
                flag: -t %s

        [Optional]
        args: (a unicode string)
                Additional parameters to the command
                flag: %s
        b_spline_smoothing: (a boolean)
                Use B-spline SyN for registrations and B-splineexponential mapping
                in DiReCT.
                flag: -v
        cortical_label_image: (an existing file name)
                Cortical ROI labels to use as a prior for ATITH.
        debug: (a boolean)
                If > 0, runs a faster version of the script.Only for testing.
                Implies -u 0.Requires single thread computation for complete
                reproducibility.
                flag: -z 1
        dimension: (3 or 2, nipype default value: 3)
                image dimension (2 or 3)
                flag: -d %d
        environ: (a dictionary with keys which are a bytes or None or a value
                 of class 'str' and with values which are a bytes or None or a value
                 of class 'str', nipype default value: {})
                Environment variables
        extraction_registration_mask: (an existing file name)
                Mask (defined in the template space) used during registration for
                brain extraction.
                flag: -f %s
        ignore_exception: (a boolean, nipype default value: False)
                Print an error message instead of throwing an exception in case the
                interface fails to run
        image_suffix: (a unicode string, nipype default value: nii.gz)
                any of standard ITK formats, nii.gz is default
                flag: -s %s
        keep_temporary_files: (an integer (int or long))
                Keep brain extraction/segmentation warps, etc (default = 0).
                flag: -k %d
        label_propagation: (a unicode string)
                Incorporate a distance prior one the posterior formulation. Should
                beof the form 'label[lambda,boundaryProbability]' where labelis a
                value of 1,2,3,... denoting label ID. The labelprobability for
                anything outside the current label = boundaryProbability * exp(
                -lambda * distanceFromBoundary )Intuitively, smaller lambda values
                will increase the spatial capturerange of the distance prior. To
                apply to all label values, simply omitspecifying the label, i.e. -l
                [lambda,boundaryProbability].
                flag: -l %s
        max_iterations: (an integer (int or long))
                ANTS registration max iterations(default = 100x100x70x20)
                flag: -i %d
        num_threads: (an integer (int or long), nipype default value: 1)
                Number of ITK threads to use
        out_prefix: (a unicode string, nipype default value: antsCT_)
                Prefix that is prepended to all output files (default = antsCT_)
                flag: -o %s
        posterior_formulation: (a unicode string)
                Atropos posterior formulation and whether or notto use mixture model
                proportions.e.g 'Socrates[1]' (default) or 'Aristotle[1]'.Choose the
                latter if youwant use the distance priors (see also the -l optionfor
                label propagation control).
                flag: -b %s
        prior_segmentation_weight: (a float)
                Atropos spatial prior *probability* weight forthe segmentation
                flag: -w %f
        quick_registration: (a boolean)
                If = 1, use antsRegistrationSyNQuick.sh as the basis for
                registrationduring brain extraction, brain segmentation,
                and(optional) normalization to a template.Otherwise use
                antsRegistrationSyN.sh (default = 0).
                flag: -q 1
        segmentation_iterations: (an integer (int or long))
                N4 -> Atropos -> N4 iterations during segmentation(default = 3)
                flag: -n %d
        terminal_output: ('stream' or 'allatonce' or 'file' or 'none')
                Control terminal output: `stream` - displays to terminal immediately
                (default), `allatonce` - waits till command is finished to display
                output, `file` - writes output to file, `none` - output is ignored
        use_floatingpoint_precision: (0 or 1)
                Use floating point precision in registrations (default = 0)
                flag: -j %d
        use_random_seeding: (0 or 1)
                Use random number generated from system clock in Atropos(default =
                1)
                flag: -u %d

Outputs::

        BrainExtractionMask: (an existing file name)
                brain extraction mask
        BrainSegmentation: (an existing file name)
                brain segmentaion image
        BrainSegmentationN4: (an existing file name)
                N4 corrected image
        BrainSegmentationPosteriors: (a list of items which are an existing
                 file name)
                Posterior probability images
        BrainVolumes: (an existing file name)
                Brain volumes as text
        CorticalThickness: (an existing file name)
                cortical thickness file
        CorticalThicknessNormedToTemplate: (an existing file name)
                Normalized cortical thickness
        SubjectToTemplate0GenericAffine: (an existing file name)
                Template to subject inverse affine
        SubjectToTemplate1Warp: (an existing file name)
                Template to subject inverse warp
        SubjectToTemplateLogJacobian: (an existing file name)
                Template to subject log jacobian
        TemplateToSubject0Warp: (an existing file name)
                Template to subject warp
        TemplateToSubject1GenericAffine: (an existing file name)
                Template to subject affine

.. _nipype.interfaces.ants.segmentation.DenoiseImage:


.. index:: DenoiseImage

DenoiseImage
------------

`Link to code <http://github.com/nipy/nipype/tree/ec86b7476/nipype/interfaces/ants/segmentation.py#L956>`__

Wraps command **DenoiseImage**

Examples
~~~~~~~~
>>> import copy
>>> from nipype.interfaces.ants import DenoiseImage
>>> denoise = DenoiseImage()
>>> denoise.inputs.dimension = 3
>>> denoise.inputs.input_image = 'im1.nii'
>>> denoise.cmdline # doctest: +ALLOW_UNICODE
'DenoiseImage -d 3 -i im1.nii -n Gaussian -o im1_noise_corrected.nii -s 1'

>>> denoise_2 = copy.deepcopy(denoise)
>>> denoise_2.inputs.output_image = 'output_corrected_image.nii.gz'
>>> denoise_2.inputs.noise_model = 'Rician'
>>> denoise_2.inputs.shrink_factor = 2
>>> denoise_2.cmdline # doctest: +ALLOW_UNICODE
'DenoiseImage -d 3 -i im1.nii -n Rician -o output_corrected_image.nii.gz -s 2'

>>> denoise_3 = DenoiseImage()
>>> denoise_3.inputs.input_image = 'im1.nii'
>>> denoise_3.inputs.save_noise = True
>>> denoise_3.cmdline # doctest: +ALLOW_UNICODE
'DenoiseImage -i im1.nii -n Gaussian -o [ im1_noise_corrected.nii, im1_noise.nii ] -s 1'

Inputs::

        [Mandatory]
        input_image: (an existing file name)
                A scalar image is expected as input for noise correction.
                flag: -i %s
        save_noise: (a boolean, nipype default value: False)
                True if the estimated noise should be saved to file.
                mutually_exclusive: noise_image

        [Optional]
        args: (a unicode string)
                Additional parameters to the command
                flag: %s
        dimension: (2 or 3 or 4)
                This option forces the image to be treated as a specified-
                dimensional image. If not specified, the program tries to infer the
                dimensionality from the input image.
                flag: -d %d
        environ: (a dictionary with keys which are a bytes or None or a value
                 of class 'str' and with values which are a bytes or None or a value
                 of class 'str', nipype default value: {})
                Environment variables
        ignore_exception: (a boolean, nipype default value: False)
                Print an error message instead of throwing an exception in case the
                interface fails to run
        noise_image: (a file name)
                Filename for the estimated noise.
        noise_model: ('Gaussian' or 'Rician', nipype default value: Gaussian)
                Employ a Rician or Gaussian noise model.
                flag: -n %s
        num_threads: (an integer (int or long), nipype default value: 1)
                Number of ITK threads to use
        output_image: (a file name)
                The output consists of the noise corrected version of the input
                image.
                flag: -o %s
        shrink_factor: (an integer (int or long), nipype default value: 1)
                Running noise correction on large images can be time consuming. To
                lessen computation time, the input image can be resampled. The
                shrink factor, specified as a single integer, describes this
                resampling. Shrink factor = 1 is the default.
                flag: -s %s
        terminal_output: ('stream' or 'allatonce' or 'file' or 'none')
                Control terminal output: `stream` - displays to terminal immediately
                (default), `allatonce` - waits till command is finished to display
                output, `file` - writes output to file, `none` - output is ignored
        verbose: (a boolean)
                Verbose output.
                flag: -v

Outputs::

        noise_image: (a file name)
        output_image: (an existing file name)

.. _nipype.interfaces.ants.segmentation.JointFusion:


.. index:: JointFusion

JointFusion
-----------

`Link to code <http://github.com/nipy/nipype/tree/ec86b7476/nipype/interfaces/ants/segmentation.py#L861>`__

Wraps command **jointfusion**

Examples
~~~~~~~~

>>> from nipype.interfaces.ants import JointFusion
>>> at = JointFusion()
>>> at.inputs.dimension = 3
>>> at.inputs.modalities = 1
>>> at.inputs.method = 'Joint[0.1,2]'
>>> at.inputs.output_label_image ='fusion_labelimage_output.nii'
>>> at.inputs.warped_intensity_images = ['im1.nii',
...                                      'im2.nii',
...                                      'im3.nii']
>>> at.inputs.warped_label_images = ['segmentation0.nii.gz',
...                                  'segmentation1.nii.gz',
...                                  'segmentation1.nii.gz']
>>> at.inputs.target_image = 'T1.nii'
>>> at.cmdline # doctest: +ALLOW_UNICODE
'jointfusion 3 1 -m Joint[0.1,2] -tg T1.nii -g im1.nii -g im2.nii -g im3.nii -l segmentation0.nii.gz -l segmentation1.nii.gz -l segmentation1.nii.gz fusion_labelimage_output.nii'

>>> at.inputs.method = 'Joint'
>>> at.inputs.alpha = 0.5
>>> at.inputs.beta = 1
>>> at.inputs.patch_radius = [3,2,1]
>>> at.inputs.search_radius = [1,2,3]
>>> at.cmdline # doctest: +ALLOW_UNICODE
'jointfusion 3 1 -m Joint[0.5,1] -rp 3x2x1 -rs 1x2x3 -tg T1.nii -g im1.nii -g im2.nii -g im3.nii -l segmentation0.nii.gz -l segmentation1.nii.gz -l segmentation1.nii.gz fusion_labelimage_output.nii'

Inputs::

        [Mandatory]
        dimension: (3 or 2 or 4, nipype default value: 3)
                image dimension (2, 3, or 4)
                flag: %d, position: 0
        modalities: (an integer (int or long))
                Number of modalities or features
                flag: %d, position: 1
        output_label_image: (a file name)
                Output fusion label map image
                flag: %s, position: -1
        target_image: (a list of items which are an existing file name)
                Target image(s)
                flag: -tg %s...
        warped_intensity_images: (a list of items which are an existing file
                 name)
                Warped atlas images
                flag: -g %s...
        warped_label_images: (a list of items which are an existing file
                 name)
                Warped atlas segmentations
                flag: -l %s...

        [Optional]
        alpha: (a float, nipype default value: 0.0)
                Regularization term added to matrix Mx for inverse
                requires: method
        args: (a unicode string)
                Additional parameters to the command
                flag: %s
        atlas_group_id: (a list of items which are a value of class 'int')
                Assign a group ID for each atlas
                flag: -gp %d...
        atlas_group_weights: (a list of items which are a value of class
                 'int')
                Assign the voting weights to each atlas group
                flag: -gpw %d...
        beta: (an integer (int or long), nipype default value: 0)
                Exponent for mapping intensity difference to joint error
                requires: method
        environ: (a dictionary with keys which are a bytes or None or a value
                 of class 'str' and with values which are a bytes or None or a value
                 of class 'str', nipype default value: {})
                Environment variables
        exclusion_region: (an existing file name)
                Specify an exclusion region for the given label.
                flag: -x %s
        ignore_exception: (a boolean, nipype default value: False)
                Print an error message instead of throwing an exception in case the
                interface fails to run
        method: (a unicode string, nipype default value: )
                Select voting method. Options: Joint (Joint Label Fusion). May be
                followed by optional parameters in brackets, e.g., -m Joint[0.1,2]
                flag: -m %s
        num_threads: (an integer (int or long), nipype default value: 1)
                Number of ITK threads to use
        patch_radius: (a list of items which are a value of class 'int')
                Patch radius for similarity measures, scalar or vector. Default:
                2x2x2
                flag: -rp %s
        search_radius: (a list of items which are a value of class 'int')
                Local search radius. Default: 3x3x3
                flag: -rs %s
        terminal_output: ('stream' or 'allatonce' or 'file' or 'none')
                Control terminal output: `stream` - displays to terminal immediately
                (default), `allatonce` - waits till command is finished to display
                output, `file` - writes output to file, `none` - output is ignored

Outputs::

        output_label_image: (an existing file name)

.. _nipype.interfaces.ants.segmentation.KellyKapowski:


.. index:: KellyKapowski

KellyKapowski
-------------

`Link to code <http://github.com/nipy/nipype/tree/ec86b7476/nipype/interfaces/ants/segmentation.py#L1282>`__

Wraps command **KellyKapowski**

Nipype Interface to ANTs' KellyKapowski, also known as DiReCT.

DiReCT is a registration based estimate of cortical thickness. It was published
in S. R. Das, B. B. Avants, M. Grossman, and J. C. Gee, Registration based
cortical thickness measurement, Neuroimage 2009, 45:867--879.

Examples
~~~~~~~~
>>> from nipype.interfaces.ants.segmentation import KellyKapowski
>>> kk = KellyKapowski()
>>> kk.inputs.dimension = 3
>>> kk.inputs.segmentation_image = "segmentation0.nii.gz"
>>> kk.inputs.convergence = "[45,0.0,10]"
>>> kk.inputs.gradient_step = 0.025
>>> kk.inputs.smoothing_variance = 1.0
>>> kk.inputs.smoothing_velocity_field = 1.5
>>> #kk.inputs.use_bspline_smoothing = False
>>> kk.inputs.number_integration_points = 10
>>> kk.inputs.thickness_prior_estimate = 10
>>> kk.cmdline # doctest: +ALLOW_UNICODE
u'KellyKapowski --convergence "[45,0.0,10]" --output "[segmentation0_cortical_thickness.nii.gz,segmentation0_warped_white_matter.nii.gz]" --image-dimensionality 3 --gradient-step 0.025000 --number-of-integration-points 10 --segmentation-image "[segmentation0.nii.gz,2,3]" --smoothing-variance 1.000000 --smoothing-velocity-field-parameter 1.500000 --thickness-prior-estimate 10.000000'

Inputs::

        [Mandatory]
        segmentation_image: (an existing file name)
                A segmentation image must be supplied labeling the gray and white
                matters.
                Default values = 2 and 3, respectively.
                flag: --segmentation-image "%s"

        [Optional]
        args: (a unicode string)
                Additional parameters to the command
                flag: %s
        convergence: (a unicode string, nipype default value: )
                Convergence is determined by fitting a line to the normalized energy
                profile of
                the last N iterations (where N is specified by the window size) and
                determining
                the slope which is then compared with the convergence threshold.
                flag: --convergence "%s"
        cortical_thickness: (a file name)
                Filename for the cortical thickness.
                flag: --output "%s"
        dimension: (3 or 2, nipype default value: 3)
                image dimension (2 or 3)
                flag: --image-dimensionality %d
        environ: (a dictionary with keys which are a bytes or None or a value
                 of class 'str' and with values which are a bytes or None or a value
                 of class 'str', nipype default value: {})
                Environment variables
        gradient_step: (a float, nipype default value: 0.025)
                Gradient step size for the optimization.
                flag: --gradient-step %f
        gray_matter_label: (an integer (int or long), nipype default value:
                 2)
                The label value for the gray matter label in the segmentation_image.
        gray_matter_prob_image: (an existing file name)
                In addition to the segmentation image, a gray matter probability
                image can be
                used. If no such image is supplied, one is created using the
                segmentation image
                and a variance of 1.0 mm.
                flag: --gray-matter-probability-image "%s"
        ignore_exception: (a boolean, nipype default value: False)
                Print an error message instead of throwing an exception in case the
                interface fails to run
        max_invert_displacement_field_iters: (an integer (int or long))
                Maximum number of iterations for estimating the invert
                displacement field.
                flag: --maximum-number-of-invert-displacement-field-iterations %d
        num_threads: (an integer (int or long), nipype default value: 1)
                Number of ITK threads to use
        number_integration_points: (an integer (int or long))
                Number of compositions of the diffeomorphism per iteration.
                flag: --number-of-integration-points %d
        smoothing_variance: (a float)
                Defines the Gaussian smoothing of the hit and total images.
                flag: --smoothing-variance %f
        smoothing_velocity_field: (a float)
                Defines the Gaussian smoothing of the velocity field (default =
                1.5).
                If the b-spline smoothing option is chosen, then this defines the
                isotropic mesh spacing for the smoothing spline (default = 15).
                flag: --smoothing-velocity-field-parameter %f
        terminal_output: ('stream' or 'allatonce' or 'file' or 'none')
                Control terminal output: `stream` - displays to terminal immediately
                (default), `allatonce` - waits till command is finished to display
                output, `file` - writes output to file, `none` - output is ignored
        thickness_prior_estimate: (a float, nipype default value: 10)
                Provides a prior constraint on the final thickness measurement in
                mm.
                flag: --thickness-prior-estimate %f
        thickness_prior_image: (an existing file name)
                An image containing spatially varying prior thickness values.
                flag: --thickness-prior-image "%s"
        use_bspline_smoothing: (a boolean)
                Sets the option for B-spline smoothing of the velocity field.
                flag: --use-bspline-smoothing 1
        warped_white_matter: (a file name)
                Filename for the warped white matter file.
        white_matter_label: (an integer (int or long), nipype default value:
                 3)
                The label value for the white matter label in the
                segmentation_image.
        white_matter_prob_image: (an existing file name)
                In addition to the segmentation image, a white matter probability
                image can be
                used. If no such image is supplied, one is created using the
                segmentation image
                and a variance of 1.0 mm.
                flag: --white-matter-probability-image "%s"

Outputs::

        cortical_thickness: (a file name)
                A thickness map defined in the segmented gray matter.
        warped_white_matter: (a file name)
                A warped white matter image.

References::
None

.. _nipype.interfaces.ants.segmentation.LaplacianThickness:


.. index:: LaplacianThickness

LaplacianThickness
------------------

`Link to code <http://github.com/nipy/nipype/tree/ec86b7476/nipype/interfaces/ants/segmentation.py#L201>`__

Wraps command **LaplacianThickness**

Calculates the cortical thickness from an anatomical image

Examples
~~~~~~~~

>>> from nipype.interfaces.ants import LaplacianThickness
>>> cort_thick = LaplacianThickness()
>>> cort_thick.inputs.input_wm = 'white_matter.nii.gz'
>>> cort_thick.inputs.input_gm = 'gray_matter.nii.gz'
>>> cort_thick.inputs.output_image = 'output_thickness.nii.gz'
>>> cort_thick.cmdline # doctest: +ALLOW_UNICODE
'LaplacianThickness white_matter.nii.gz gray_matter.nii.gz output_thickness.nii.gz'

Inputs::

        [Mandatory]
        input_gm: (a file name)
                gray matter segmentation image
                flag: %s, position: 2
        input_wm: (a file name)
                white matter segmentation image
                flag: %s, position: 1

        [Optional]
        args: (a unicode string)
                Additional parameters to the command
                flag: %s
        dT: (a float)
                flag: dT=%d, position: 6
        environ: (a dictionary with keys which are a bytes or None or a value
                 of class 'str' and with values which are a bytes or None or a value
                 of class 'str', nipype default value: {})
                Environment variables
        ignore_exception: (a boolean, nipype default value: False)
                Print an error message instead of throwing an exception in case the
                interface fails to run
        num_threads: (an integer (int or long), nipype default value: 1)
                Number of ITK threads to use
        opt_tolerance: (a float)
                flag: optional-laplacian-tolerance=%d, position: 8
        output_image: (a file name)
                name of output file
                flag: %s, position: 3
        prior_thickness: (a float)
                flag: priorthickval=%d, position: 5
        smooth_param: (a float)
                flag: smoothparam=%d, position: 4
        sulcus_prior: (a boolean)
                flag: use-sulcus-prior, position: 7
        terminal_output: ('stream' or 'allatonce' or 'file' or 'none')
                Control terminal output: `stream` - displays to terminal immediately
                (default), `allatonce` - waits till command is finished to display
                output, `file` - writes output to file, `none` - output is ignored

Outputs::

        output_image: (an existing file name)
                Cortical thickness

.. _nipype.interfaces.ants.segmentation.N4BiasFieldCorrection:


.. index:: N4BiasFieldCorrection

N4BiasFieldCorrection
---------------------

`Link to code <http://github.com/nipy/nipype/tree/ec86b7476/nipype/interfaces/ants/segmentation.py#L269>`__

Wraps command **N4BiasFieldCorrection**

N4 is a variant of the popular N3 (nonparameteric nonuniform normalization)
retrospective bias correction algorithm. Based on the assumption that the
corruption of the low frequency bias field can be modeled as a convolution of
the intensity histogram by a Gaussian, the basic algorithmic protocol is to
iterate between deconvolving the intensity histogram by a Gaussian, remapping
the intensities, and then spatially smoothing this result by a B-spline modeling
of the bias field itself. The modifications from and improvements obtained over
the original N3 algorithm are described in [Tustison2010]_.

.. [Tustison2010] N. Tustison et al.,
  N4ITK: Improved N3 Bias Correction, IEEE Transactions on Medical Imaging,
  29(6):1310-1320, June 2010.

Examples
~~~~~~~~

>>> import copy
>>> from nipype.interfaces.ants import N4BiasFieldCorrection
>>> n4 = N4BiasFieldCorrection()
>>> n4.inputs.dimension = 3
>>> n4.inputs.input_image = 'structural.nii'
>>> n4.inputs.bspline_fitting_distance = 300
>>> n4.inputs.shrink_factor = 3
>>> n4.inputs.n_iterations = [50,50,30,20]
>>> n4.cmdline # doctest: +ALLOW_UNICODE
'N4BiasFieldCorrection --bspline-fitting [ 300 ] -d 3 --input-image structural.nii --convergence [ 50x50x30x20 ] --output structural_corrected.nii --shrink-factor 3'

>>> n4_2 = copy.deepcopy(n4)
>>> n4_2.inputs.convergence_threshold = 1e-6
>>> n4_2.cmdline # doctest: +ALLOW_UNICODE
'N4BiasFieldCorrection --bspline-fitting [ 300 ] -d 3 --input-image structural.nii --convergence [ 50x50x30x20, 1e-06 ] --output structural_corrected.nii --shrink-factor 3'

>>> n4_3 = copy.deepcopy(n4_2)
>>> n4_3.inputs.bspline_order = 5
>>> n4_3.cmdline # doctest: +ALLOW_UNICODE
'N4BiasFieldCorrection --bspline-fitting [ 300, 5 ] -d 3 --input-image structural.nii --convergence [ 50x50x30x20, 1e-06 ] --output structural_corrected.nii --shrink-factor 3'

>>> n4_4 = N4BiasFieldCorrection()
>>> n4_4.inputs.input_image = 'structural.nii'
>>> n4_4.inputs.save_bias = True
>>> n4_4.inputs.dimension = 3
>>> n4_4.cmdline # doctest: +ALLOW_UNICODE
'N4BiasFieldCorrection -d 3 --input-image structural.nii --output [ structural_corrected.nii, structural_bias.nii ]'

Inputs::

        [Mandatory]
        input_image: (a file name)
                image to apply transformation to (generally a coregistered
                functional)
                flag: --input-image %s
        save_bias: (a boolean, nipype default value: False)
                True if the estimated bias should be saved to file.
                mutually_exclusive: bias_image

        [Optional]
        args: (a unicode string)
                Additional parameters to the command
                flag: %s
        bias_image: (a file name)
                Filename for the estimated bias.
        bspline_fitting_distance: (a float)
                flag: --bspline-fitting %s
        bspline_order: (an integer (int or long))
                requires: bspline_fitting_distance
        convergence_threshold: (a float)
                requires: n_iterations
        dimension: (3 or 2, nipype default value: 3)
                image dimension (2 or 3)
                flag: -d %d
        environ: (a dictionary with keys which are a bytes or None or a value
                 of class 'str' and with values which are a bytes or None or a value
                 of class 'str', nipype default value: {})
                Environment variables
        ignore_exception: (a boolean, nipype default value: False)
                Print an error message instead of throwing an exception in case the
                interface fails to run
        mask_image: (a file name)
                flag: --mask-image %s
        n_iterations: (a list of items which are an integer (int or long))
                flag: --convergence %s
        num_threads: (an integer (int or long), nipype default value: 1)
                Number of ITK threads to use
        output_image: (a unicode string)
                output file name
                flag: --output %s
        shrink_factor: (an integer (int or long))
                flag: --shrink-factor %d
        terminal_output: ('stream' or 'allatonce' or 'file' or 'none')
                Control terminal output: `stream` - displays to terminal immediately
                (default), `allatonce` - waits till command is finished to display
                output, `file` - writes output to file, `none` - output is ignored
        weight_image: (a file name)
                flag: --weight-image %s

Outputs::

        bias_image: (an existing file name)
                Estimated bias
        output_image: (an existing file name)
                Warped image

.. _nipype.interfaces.ants.segmentation.antsBrainExtraction:


.. index:: antsBrainExtraction

antsBrainExtraction
-------------------

`Link to code <http://github.com/nipy/nipype/tree/ec86b7476/nipype/interfaces/ants/segmentation.py#L809>`__

Wraps command **antsBrainExtraction.sh**


Inputs::

        [Mandatory]
        anatomical_image: (an existing file name)
                Structural image, typically T1. If more than oneanatomical image is
                specified, subsequently specifiedimages are used during the
                segmentation process. However,only the first image is used in the
                registration of priors.Our suggestion would be to specify the T1 as
                the first image.Anatomical template created using e.g. LPBA40 data
                set withbuildtemplateparallel.sh in ANTs.
                flag: -a %s
        brain_probability_mask: (an existing file name)
                Brain probability mask created using e.g. LPBA40 data set whichhave
                brain masks defined, and warped to anatomical template andaveraged
                resulting in a probability image.
                flag: -m %s
        brain_template: (an existing file name)
                Anatomical template created using e.g. LPBA40 data set
                withbuildtemplateparallel.sh in ANTs.
                flag: -e %s

        [Optional]
        args: (a unicode string)
                Additional parameters to the command
                flag: %s
        debug: (a boolean)
                If > 0, runs a faster version of the script.Only for testing.
                Implies -u 0.Requires single thread computation for complete
                reproducibility.
                flag: -z 1
        dimension: (3 or 2, nipype default value: 3)
                image dimension (2 or 3)
                flag: -d %d
        environ: (a dictionary with keys which are a bytes or None or a value
                 of class 'str' and with values which are a bytes or None or a value
                 of class 'str', nipype default value: {})
                Environment variables
        extraction_registration_mask: (an existing file name)
                Mask (defined in the template space) used during registration for
                brain extraction.To limit the metric computation to a specific
                region.
                flag: -f %s
        ignore_exception: (a boolean, nipype default value: False)
                Print an error message instead of throwing an exception in case the
                interface fails to run
        image_suffix: (a unicode string, nipype default value: nii.gz)
                any of standard ITK formats, nii.gz is default
                flag: -s %s
        keep_temporary_files: (an integer (int or long))
                Keep brain extraction/segmentation warps, etc (default = 0).
                flag: -k %d
        num_threads: (an integer (int or long), nipype default value: 1)
                Number of ITK threads to use
        out_prefix: (a unicode string, nipype default value: highres001_)
                Prefix that is prepended to all output files (default =
                highress001_)
                flag: -o %s
        terminal_output: ('stream' or 'allatonce' or 'file' or 'none')
                Control terminal output: `stream` - displays to terminal immediately
                (default), `allatonce` - waits till command is finished to display
                output, `file` - writes output to file, `none` - output is ignored
        use_floatingpoint_precision: (0 or 1)
                Use floating point precision in registrations (default = 0)
                flag: -q %d
        use_random_seeding: (0 or 1)
                Use random number generated from system clock in Atropos(default =
                1)
                flag: -u %d

Outputs::

        BrainExtractionBrain: (an existing file name)
                brain extraction image
        BrainExtractionCSF: (an existing file name)
                segmentation mask with only CSF
        BrainExtractionGM: (an existing file name)
                segmentation mask with only grey matter
        BrainExtractionInitialAffine: (an existing file name)
        BrainExtractionInitialAffineFixed: (an existing file name)
        BrainExtractionInitialAffineMoving: (an existing file name)
        BrainExtractionLaplacian: (an existing file name)
        BrainExtractionMask: (an existing file name)
                brain extraction mask
        BrainExtractionPrior0GenericAffine: (an existing file name)
        BrainExtractionPrior1InverseWarp: (an existing file name)
        BrainExtractionPrior1Warp: (an existing file name)
        BrainExtractionPriorWarped: (an existing file name)
        BrainExtractionSegmentation: (an existing file name)
                segmentation mask with CSF, GM, and WM
        BrainExtractionTemplateLaplacian: (an existing file name)
        BrainExtractionTmp: (an existing file name)
        BrainExtractionWM: (an existing file name)
                segmenration mask with only white matter
        N4Corrected0: (an existing file name)
                N4 bias field corrected image
        N4Truncated0: (an existing file name)

.. _nipype.interfaces.ants.segmentation.antsCorticalThickness:


.. index:: antsCorticalThickness

antsCorticalThickness
---------------------

`Link to code <http://github.com/nipy/nipype/tree/ec86b7476/nipype/interfaces/ants/segmentation.py#L607>`__

Wraps command **antsCorticalThickness.sh**


Inputs::

        [Mandatory]
        anatomical_image: (an existing file name)
                Structural *intensity* image, typically T1.If more than one
                anatomical image is specified,subsequently specified images are used
                during thesegmentation process. However, only the firstimage is used
                in the registration of priors.Our suggestion would be to specify the
                T1as the first image.
                flag: -a %s
        brain_probability_mask: (an existing file name)
                brain probability mask in template space
                flag: -m %s
        brain_template: (an existing file name)
                Anatomical *intensity* template (possibly created using apopulation
                data set with buildtemplateparallel.sh in ANTs).This template is
                *not* skull-stripped.
                flag: -e %s
        segmentation_priors: (a list of items which are an existing file
                 name)
                flag: -p %s
        t1_registration_template: (an existing file name)
                Anatomical *intensity* template(assumed to be skull-stripped). A
                commoncase would be where this would be the sametemplate as
                specified in the -e option whichis not skull stripped.
                flag: -t %s

        [Optional]
        args: (a unicode string)
                Additional parameters to the command
                flag: %s
        b_spline_smoothing: (a boolean)
                Use B-spline SyN for registrations and B-splineexponential mapping
                in DiReCT.
                flag: -v
        cortical_label_image: (an existing file name)
                Cortical ROI labels to use as a prior for ATITH.
        debug: (a boolean)
                If > 0, runs a faster version of the script.Only for testing.
                Implies -u 0.Requires single thread computation for complete
                reproducibility.
                flag: -z 1
        dimension: (3 or 2, nipype default value: 3)
                image dimension (2 or 3)
                flag: -d %d
        environ: (a dictionary with keys which are a bytes or None or a value
                 of class 'str' and with values which are a bytes or None or a value
                 of class 'str', nipype default value: {})
                Environment variables
        extraction_registration_mask: (an existing file name)
                Mask (defined in the template space) used during registration for
                brain extraction.
                flag: -f %s
        ignore_exception: (a boolean, nipype default value: False)
                Print an error message instead of throwing an exception in case the
                interface fails to run
        image_suffix: (a unicode string, nipype default value: nii.gz)
                any of standard ITK formats, nii.gz is default
                flag: -s %s
        keep_temporary_files: (an integer (int or long))
                Keep brain extraction/segmentation warps, etc (default = 0).
                flag: -k %d
        label_propagation: (a unicode string)
                Incorporate a distance prior one the posterior formulation. Should
                beof the form 'label[lambda,boundaryProbability]' where labelis a
                value of 1,2,3,... denoting label ID. The labelprobability for
                anything outside the current label = boundaryProbability * exp(
                -lambda * distanceFromBoundary )Intuitively, smaller lambda values
                will increase the spatial capturerange of the distance prior. To
                apply to all label values, simply omitspecifying the label, i.e. -l
                [lambda,boundaryProbability].
                flag: -l %s
        max_iterations: (an integer (int or long))
                ANTS registration max iterations(default = 100x100x70x20)
                flag: -i %d
        num_threads: (an integer (int or long), nipype default value: 1)
                Number of ITK threads to use
        out_prefix: (a unicode string, nipype default value: antsCT_)
                Prefix that is prepended to all output files (default = antsCT_)
                flag: -o %s
        posterior_formulation: (a unicode string)
                Atropos posterior formulation and whether or notto use mixture model
                proportions.e.g 'Socrates[1]' (default) or 'Aristotle[1]'.Choose the
                latter if youwant use the distance priors (see also the -l optionfor
                label propagation control).
                flag: -b %s
        prior_segmentation_weight: (a float)
                Atropos spatial prior *probability* weight forthe segmentation
                flag: -w %f
        quick_registration: (a boolean)
                If = 1, use antsRegistrationSyNQuick.sh as the basis for
                registrationduring brain extraction, brain segmentation,
                and(optional) normalization to a template.Otherwise use
                antsRegistrationSyN.sh (default = 0).
                flag: -q 1
        segmentation_iterations: (an integer (int or long))
                N4 -> Atropos -> N4 iterations during segmentation(default = 3)
                flag: -n %d
        terminal_output: ('stream' or 'allatonce' or 'file' or 'none')
                Control terminal output: `stream` - displays to terminal immediately
                (default), `allatonce` - waits till command is finished to display
                output, `file` - writes output to file, `none` - output is ignored
        use_floatingpoint_precision: (0 or 1)
                Use floating point precision in registrations (default = 0)
                flag: -j %d
        use_random_seeding: (0 or 1)
                Use random number generated from system clock in Atropos(default =
                1)
                flag: -u %d

Outputs::

        BrainExtractionMask: (an existing file name)
                brain extraction mask
        BrainSegmentation: (an existing file name)
                brain segmentaion image
        BrainSegmentationN4: (an existing file name)
                N4 corrected image
        BrainSegmentationPosteriors: (a list of items which are an existing
                 file name)
                Posterior probability images
        BrainVolumes: (an existing file name)
                Brain volumes as text
        CorticalThickness: (an existing file name)
                cortical thickness file
        CorticalThicknessNormedToTemplate: (an existing file name)
                Normalized cortical thickness
        SubjectToTemplate0GenericAffine: (an existing file name)
                Template to subject inverse affine
        SubjectToTemplate1Warp: (an existing file name)
                Template to subject inverse warp
        SubjectToTemplateLogJacobian: (an existing file name)
                Template to subject log jacobian
        TemplateToSubject0Warp: (an existing file name)
                Template to subject warp
        TemplateToSubject1GenericAffine: (an existing file name)
                Template to subject affine
