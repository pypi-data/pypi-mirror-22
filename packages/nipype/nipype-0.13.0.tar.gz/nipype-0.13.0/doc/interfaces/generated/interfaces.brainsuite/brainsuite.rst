.. AUTO-GENERATED FILE -- DO NOT EDIT!

interfaces.brainsuite.brainsuite
================================


.. _nipype.interfaces.brainsuite.brainsuite.BDP:


.. index:: BDP

BDP
---

`Link to code <http://github.com/nipy/nipype/tree/ec86b7476/nipype/interfaces/brainsuite/brainsuite.py#L1532>`__

Wraps command **bdp.sh**

BrainSuite Diffusion Pipeline (BDP) enables fusion of diffusion and
structural MRI information for advanced image and connectivity analysis.
It provides various methods for distortion correction, co-registration,
diffusion modeling (DTI and ODF) and basic ROI-wise statistic. BDP is a
flexible and diverse tool which supports wide variety of diffusion
datasets.
For more information, please see:

http://brainsuite.org/processing/diffusion/

Examples
~~~~~~~~

>>> from nipype.interfaces import brainsuite
>>> bdp = brainsuite.BDP()
>>> bdp.inputs.bfcFile = '/directory/subdir/prefix.bfc.nii.gz'
>>> bdp.inputs.inputDiffusionData = '/directory/subdir/prefix.dwi.nii.gz'
>>> bdp.inputs.BVecBValPair = ['/directory/subdir/prefix.dwi.bvec', '/directory/subdir/prefix.dwi.bval']
>>> results = bdp.run() #doctest: +SKIP

Inputs::

        [Mandatory]
        BVecBValPair: (a list of from 2 to 2 items which are a value of class
                 'str')
                Must input a list containing first the BVector file, then the BValue
                file (both must be absolute paths)
                Example: bdp.inputs.BVecBValPair =
                ['/directory/subdir/prefix.dwi.bvec',
                '/directory/subdir/prefix.dwi.bval'] The first item in the list
                specifies the filename of the file containing b-values for the
                diffusion scan. The b-value file must be a plain-text file and
                usually has an extension of .bval
                The second item in the list specifies the filename of the file
                containing the diffusion gradient directions (specified in the voxel
                coordinates of the input diffusion-weighted image)The b-vectors file
                must be a plain text file and usually has an extension of .bvec
                flag: --bvec %s --bval %s, position: -1
                mutually_exclusive: bMatrixFile
        bMatrixFile: (a file name)
                Specifies the absolute path and filename of the file containing
                b-matrices for diffusion-weighted scans. The flag must be followed
                by the filename. This file must be a plain text file containing 3x3
                matrices for each diffusion encoding direction. It should contain
                zero matrices corresponding to b=0 images. This file usually has
                ".bmat" as its extension, and can be used to provide BDP with the
                more-accurate b-matrices as saved by some proprietary scanners. The
                b-matrices specified by the file must be in the voxel coordinates of
                the input diffusion weighted image (NIfTI file). In case b-matrices
                are not known/calculated, bvec and .bval files can be used instead
                (see diffusionGradientFile and bValueFile).
                flag: --bmat %s, position: -1
                mutually_exclusive: BVecBValPair
        bfcFile: (a file name)
                Specify absolute path to file produced by bfc. By default, bfc
                produces the file in the format: prefix.bfc.nii.gz
                flag: %s, position: 0
                mutually_exclusive: noStructuralRegistration
        inputDiffusionData: (a file name)
                Specifies the absolute path and filename of the input diffusion data
                in 4D NIfTI-1 format. The flag must be followed by the filename.
                Only NIfTI-1 files with extension .nii or .nii.gz are supported.
                Furthermore, either bMatrixFile, or a combination of both bValueFile
                and diffusionGradientFile must be used to provide the necessary
                b-matrices/b-values and gradient vectors.
                flag: --nii %s, position: -2
        noStructuralRegistration: (a boolean)
                Allows BDP to work without any structural input. This can useful
                when one is only interested in diffusion modelling part of BDP. With
                this flag only fieldmap-based distortion correction is supported.
                outPrefix can be used to specify fileprefix of the output filenames.
                Change dwiMask to define region of interest for diffusion modelling.
                flag: --no-structural-registration, position: 0
                mutually_exclusive: bfcFile

        [Optional]
        args: (a unicode string)
                Additional parameters to the command
                flag: %s
        bValRatioThreshold: (a float)
                Sets a threshold which is used to determine b=0 images. When there
                are no diffusion weighted image with b-value of zero, then BDP tries
                to use diffusion weighted images with a low b-value in place of b=0
                image. The diffusion images with minimum b-value is used as b=0
                image only if the ratio of the maximum and minimum b-value is more
                than the specified threshold. A lower value of threshold will allow
                diffusion images with higher b-value to be used as b=0 image. The
                default value of this threshold is set to 45, if this trait is not
                set.
                flag: --bval-ratio-threshold %f
        customDiffusionLabel: (a file name)
                BDP supports custom ROIs in addition to those generated by
                BrainSuite SVReg) for ROI-wise statistics calculation. The flag must
                be followed by the name of either a file (custom ROI file) or of a
                folder that contains one or more ROI files. All of the files must be
                in diffusion coordinate, i.e. the label files should overlay
                correctly with the diffusion scan in BrainSuite. These input label
                files are also transferred (and saved) to T1 coordinate for
                statistics in T1 coordinate. BDP uses nearest-neighborhood
                interpolation for this transformation. Only NIfTI files, with an
                extension of .nii or .nii.gz are supported. In order to avoid
                confusion with other ROI IDs in the statistic files, a 5-digit ROI
                ID is generated for each custom label found and the mapping of ID to
                label file is saved in the file fileprefix>.BDP_ROI_MAP.xml. Custom
                label files can also be generated by using the label painter tool in
                BrainSuite. See also customLabelXML
                flag: --custom-diffusion-label %s
        customLabelXML: (a file name)
                BrainSuite saves a descriptions of the SVReg labels (ROI name, ID,
                color, and description) in an .xml file
                brainsuite_labeldescription.xml). BDP uses the ROI ID"s from this
                xml file to report statistics. This flag allows for the use of a
                custom label description xml file. The flag must be followed by an
                xml filename. This can be useful when you want to limit the ROIs for
                which you compute statistics. You can also use custom xml files to
                name your own ROIs (assign ID"s) for custom labels. BrainSuite can
                save a label description in .xml format after using the label
                painter tool to create a ROI label. The xml file MUST be in the same
                format as BrainSuite"s label description file (see
                brainsuite_labeldescription.xml for an example). When this flag is
                used, NO 5-digit ROI ID is generated for custom label files and NO
                Statistics will be calculated for ROIs not identified in the custom
                xml file. See also customDiffusionLabel and customT1Label.
                flag: --custom-label-xml %s
        customT1Label: (a file name)
                Same as customDiffusionLabelexcept that the label files specified
                must be in T1 coordinate, i.e. the label files should overlay
                correctly with the T1-weighted scan in BrainSuite. If the trait
                outputDiffusionCoordinates is also used then these input label files
                are also transferred (and saved) to diffusion coordinate for
                statistics in diffusion coordinate. BDP uses nearest-neighborhood
                interpolation for this transformation. See also customLabelXML.
                flag: --custom-t1-label %s
        dataSinkDelay: (a list of items which are a value of class 'str')
                For use in parallel processing workflows including Brainsuite
                Cortical Surface Extraction sequence. Connect datasink out_file to
                dataSinkDelay to delay execution of BDP until dataSink has finished
                sinking outputs. In particular, BDP may be run after BFC has
                finished. For more information see
                http://brainsuite.org/processing/diffusion/pipeline/
                flag: %s
        dcorrRegMeasure: ('MI' or 'INVERSION-EPI' or 'INVERSION-T1' or
                 'INVERSION-BOTH' or 'BDP')
                Defines the method for registration-based distortion correction.
                Possible methods are "MI", "INVERSION-EPI", "INVERSION-T1",
                INVERSION-BOTH", and "BDP". MI method uses normalized mutual
                information based cost-function while estimating the distortion
                field. INVERSION-based method uses simpler cost function based on
                sum of squared difference by exploiting the known approximate
                contrast relationship in T1- and T2-weighted images. T2-weighted EPI
                is inverted when INVERSION-EPI is used; T1-image is inverted when
                INVERSION-T1 is used; and both are inverted when INVERSION-BOTH is
                used. BDP method add the MI-based refinement after the correction
                using INVERSION-BOTH method. BDP is the default method when this
                trait is not set.
                flag: --dcorr-reg-method %s
        dcorrWeight: (a float)
                Sets the (scalar) weighting parameter for regularization penalty in
                registration-based distortion correction. Set this trait to a
                single, non-negative number which specifies the weight. A large
                regularization weight encourages smoother distortion field at the
                cost of low measure of image similarity after distortion correction.
                On the other hand, a smaller regularization weight can result into
                higher measure of image similarity but with unrealistic and unsmooth
                distortion field. A weight of 0.5 would reduce the penalty to half
                of the default regularization penalty (By default, this weight is
                set to 1.0). Similarly, a weight of 2.0 would increase the penalty
                to twice of the default penalty.
                flag: --dcorr-regularization-wt %f
        dwiMask: (a file name)
                Specifies the filename of the brain-mask file for diffusion data.
                This mask is used only for co-registration purposes and can affect
                overall quality of co-registration (see t1Mask for definition of
                brain mask for statistics computation). The mask must be a 3D volume
                and should be in the same coordinates as input Diffusion file/data
                (i.e. should overlay correctly with input diffusion data in
                BrainSuite). For best results, the mask should include only brain
                voxels (CSF voxels around brain is also acceptable). When this flag
                is not used, BDP will generate a pseudo mask using first b=0 image
                volume and would save it as fileprefix>.dwi.RSA.mask.nii.gz. In case
                co-registration is not accurate with automatically generated pseudo
                mask, BDP should be re-run with a refined diffusion mask. The mask
                can be generated and/or edited in BrainSuite.
                flag: --dwi-mask %s
        echoSpacing: (a float)
                Sets the echo spacing to t seconds, which is used for fieldmap-based
                distortion correction. This flag is required when using
                fieldmapCorrection
                flag: --echo-spacing=%f
        environ: (a dictionary with keys which are a bytes or None or a value
                 of class 'str' and with values which are a bytes or None or a value
                 of class 'str', nipype default value: {})
                Environment variables
        estimateODF_3DShore: (a float)
                Estimates ODFs using 3Dshore. Pass in diffusion time, in ms
                flag: --3dshore --diffusion_time_ms %f
        estimateODF_FRACT: (a boolean)
                Estimates ODFs using the Funk-Radon and Cosine Transformation
                (FRACT). The outputs are saved in a separate directory with name
                "FRACT" and the ODFs can be visualized by loading the saved ".odf"
                file in BrainSuite.
                flag: --FRACT
        estimateODF_FRT: (a boolean)
                Estimates ODFs using Funk-Radon Transformation (FRT). The
                coefficient maps for ODFs are saved in a separate directory with
                name "FRT" and the ODFs can be visualized by loading the saved
                ".odf" file in BrainSuite. The derived generalized-FA (GFA) maps are
                also saved in the output directory.
                flag: --FRT
        estimateTensors: (a boolean)
                Estimates diffusion tensors using a weighted log-linear estimation
                and saves derived diffusion tensor parameters (FA, MD, axial,
                radial, L2, L3). This is the default behavior if no diffusion
                modeling flags are specified. The estimated diffusion tensors can be
                visualized by loading the saved *.eig.nii.gz file in BrainSuite. BDP
                reports diffusivity (MD, axial, radial, L2 and L3) in a unit which
                is reciprocal inverse of the unit of input b-value.
                flag: --tensors
        fieldmapCorrection: (a file name)
                Use an acquired fieldmap for distortion correction. The fieldmap
                must have units of radians/second. Specify the filename of the
                fieldmap file. The field of view (FOV) of the fieldmap scan must
                cover the FOV of the diffusion scan. BDP will try to check the
                overlap of the FOV of the two scans and will issue a warning/error
                if the diffusion scan"s FOV is not fully covered by the fieldmap"s
                FOV. BDP uses all of the information saved in the NIfTI header to
                compute the FOV. If you get this error and think that it is
                incorrect, then it can be suppressed using the flag ignore-fieldmap-
                FOV. Neither the image matrix size nor the imaging grid resolution
                of the fieldmap needs to be the same as that of the diffusion scan,
                but the fieldmap must be pre-registred to the diffusion scan. BDP
                does NOT align the fieldmap to the diffusion scan, nor does it check
                the alignment of the fieldmap and diffusion scans. Only NIfTI files
                with extension of .nii or .nii.gz are supported. Fieldmap-based
                distortion correction also requires the echoSpacing. Also
                fieldmapCorrectionMethod allows you to define method for distortion
                correction. least squares is the default method.
                flag: --fieldmap-correction %s
                requires: echoSpacing
        fieldmapCorrectionMethod: ('pixelshift' or 'leastsq')
                Defines the distortion correction method while using fieldmap.
                Possible methods are "pixelshift" and "leastsq". leastsq is the
                default method when this flag is not used. Pixel-shift (pixelshift)
                method uses image interpolation to un-distort the distorted
                diffusion images. Least squares (leastsq) method uses a physical
                model of distortion which is more accurate (and more computationally
                expensive) than pixel-shift method.
                flag: --fieldmap-correction-method %s
                mutually_exclusive: skipIntensityCorr
        fieldmapSmooth: (a float)
                Applies 3D Gaussian smoothing with a standard deviation of S
                millimeters (mm) to the input fieldmap before applying distortion
                correction. This trait is only useful with fieldmapCorrection. Skip
                this trait for no smoothing.
                flag: --fieldmap-smooth3=%f
        flagConfigFile: (a file name)
                Uses the defined file to specify BDP flags which can be useful for
                batch processing. A flag configuration file is a plain text file
                which can contain any number of BDP"s optional flags (and their
                parameters) separated by whitespace. Everything coming after # until
                end-of-line is treated as comment and is ignored. If a flag is
                defined in configuration file and is also specified in the command
                used to run BDP, then the later get preference and overrides the
                definition in configuration file.
                flag: --flag-conf-file %s
        forcePartialROIStats: (a boolean)
                The field of view (FOV) of the diffusion and T1-weighted scans may
                differ significantly in some situations. This may result in partial
                acquisitions of some ROIs in the diffusion scan. By default, BDP
                does not compute statistics for partially acquired ROIs and shows
                warnings. This flag forces computation of statistics for all ROIs,
                including those which are partially acquired. When this flag is
                used, number of missing voxels are also reported for each ROI in
                statistics files. Number of missing voxels are reported in the same
                coordinate system as the statistics file.
                flag: --force-partial-roi-stats
        generateStats: (a boolean)
                Generate ROI-wise statistics of estimated diffusion tensor
                parameters. Units of the reported statistics are same as that of the
                estimated tensor parameters (see estimateTensors). Mean, variance,
                and voxel counts of white matter(WM), grey matter(GM), and both WM
                and GM combined are written for each estimated parameter in a
                separate comma-seperated value csv) file. BDP uses the ROI labels
                generated by Surface-Volume Registration (SVReg) in the BrainSuite
                extraction sequence. Specifically, it looks for labels saved in
                either fileprefix>.svreg.corr.label.nii.gz or
                <fileprefix>.svreg.label.nii.gz. In case both files are present,
                only the first file is used. Also see customDiffusionLabel and
                customT1Label for specifying your own ROIs. It is also possible to
                forgo computing the SVReg ROI-wise statistics and only compute stats
                with custom labels if SVReg label is missing. BDP also transfers
                (and saves) the label/mask files to appropriate coordinates before
                computing statistics. Also see outputDiffusionCoordinates for
                outputs in diffusion coordinate and forcePartialROIStats for an
                important note about field of view of diffusion and T1-weighted
                scans.
                flag: --generate-stats
        ignoreFieldmapFOV: (a boolean)
                Supresses the error generated by an insufficient field of view of
                the input fieldmap and continues with the processing. It is useful
                only when used with fieldmap-based distortion correction. See
                fieldmap-correction for a detailed explanation.
                flag: --ignore-fieldmap-fov
        ignoreMemory: (a boolean)
                Deactivates the inbuilt memory checks and forces BDP to run
                registration-based distortion correction at its default resolution
                even on machines with a low amount of memory. This may result in an
                out-of-memory error when BDP cannot allocate sufficient memory.
                flag: --ignore-memory
        ignore_exception: (a boolean, nipype default value: False)
                Print an error message instead of throwing an exception in case the
                interface fails to run
        lowMemory: (a boolean)
                Activates low-memory mode. This will run the registration-based
                distortion correction at a lower resolution, which could result in a
                less-accurate correction. This should only be used when no other
                alternative is available.
                flag: --low-memory
        odfLambta: (a boolean)
                Sets the regularization parameter, lambda, of the Laplace-Beltrami
                operator while estimating ODFs. The default value is set to 0.006 .
                This can be used to set the appropriate regularization for the input
                diffusion data.
                flag: --odf-lambda <L>
        onlyStats: (a boolean)
                Skip all of the processing (co-registration, distortion correction
                and tensor/ODF estimation) and directly start computation of
                statistics. This flag is useful when BDP was previously run on a
                subject (or fileprefix>) and statistics need to be (re-)computed
                later. This assumes that all the necessary files were generated
                earlier. All of the other flags MUST be used in the same way as they
                were in the initial BDP run that processed the data.
                flag: --generate-only-stats
        outPrefix: (a unicode string)
                Specifies output fileprefix when noStructuralRegistration is used.
                The fileprefix can not start with a dash (-) and should be a simple
                string reflecting the absolute path to desired location, along with
                outPrefix. When this flag is not specified (and
                noStructuralRegistration is used) then the output files have same
                file-base as the input diffusion file. This trait is ignored when
                noStructuralRegistration is not used.
                flag: --output-fileprefix %s
        outputDiffusionCoordinates: (a boolean)
                Enables estimation of diffusion tensors and/or ODFs (and statistics
                if applicable) in the native diffusion coordinate in addition to the
                default T1-coordinate. All native diffusion coordinate files are
                saved in a seperate folder named "diffusion_coord_outputs". In case
                statistics computation is required, it will also transform/save all
                label/mask files required to diffusion coordinate (see generateStats
                for details).
                flag: --output-diffusion-coordinate
        outputSubdir: (a unicode string)
                By default, BDP writes out all the output (and intermediate) files
                in the same directory (or folder) as the BFC file. This flag allows
                to specify a sub-directory name in which output (and intermediate)
                files would be written. BDP will create the sub-directory in the
                same directory as BFC file. <directory_name> should be the name of
                the sub-directory without any path. This can be useful to organize
                all outputs generated by BDP in a separate sub-directory.
                flag: --output-subdir %s
        phaseEncodingDirection: ('x' or 'x-' or 'y' or 'y-' or 'z' or 'z-')
                Specifies the phase-encoding direction of the EPI (diffusion)
                images. It is same as the dominant direction of distortion in the
                images. This information is used to constrain the distortion
                correction along the specified direction. Directions are represented
                by any one of x, x-, y, y-, z or z-. "x" direction increases towards
                the right side of the subject, while "x-" increases towards the left
                side of the subject. Similarly, "y" and "y-" are along the anterior-
                posterior direction of the subject, and "z" & "z-" are along the
                inferior-superior direction. When this flag is not used, BDP uses
                "y" as the default phase-encoding direction.
                flag: --dir=%s
        rigidRegMeasure: ('MI' or 'INVERSION' or 'BDP')
                Defines the similarity measure to be used for rigid registration.
                Possible measures are "MI", "INVERSION" and "BDP". MI measure uses
                normalized mutual information based cost function. INVERSION measure
                uses simpler cost function based on sum of squared difference by
                exploiting the approximate inverse-contrast relationship in T1- and
                T2-weighted images. BDP measure combines MI and INVERSION. It starts
                with INVERSION measure and refines the result with MI measure. BDP
                is the default measure when this trait is not set.
                flag: --rigid-reg-measure %s
        skipDistortionCorr: (a boolean)
                Skips distortion correction completely and performs only a rigid
                registration of diffusion and T1-weighted image. This can be useful
                when the input diffusion images do not have any distortion or they
                have been corrected for distortion.
                flag: --no-distortion-correction
        skipIntensityCorr: (a boolean)
                Disables intensity correction when performing distortion correction.
                Intensity correction can change the noise distribution in the
                corrected image, but it does not affect estimated diffusion
                parameters like FA, etc.
                flag: --no-intensity-correction
                mutually_exclusive: fieldmapCorrectionMethod
        skipNonuniformityCorr: (a boolean)
                Skips intensity non-uniformity correction in b=0 image for
                registration-based distortion correction. The intensity non-
                uniformity correction does not affect any diffusion modeling.
                flag: --no-nonuniformity-correction
        t1Mask: (a file name)
                Specifies the filename of the brain-mask file for input T1-weighted
                image. This mask can be same as the brain mask generated during
                BrainSuite extraction sequence. For best results, the mask should
                not include any extra-meningial tissues from T1-weighted image. The
                mask must be in the same coordinates as input T1-weighted image
                (i.e. should overlay correctly with input <fileprefix>.bfc.nii.gz
                file in BrainSuite). This mask is used for co-registration and
                defining brain boundary for statistics computation. The mask can be
                generated and/or edited in BrainSuite. In case
                outputDiffusionCoordinates is also used, this mask is first
                transformed to diffusion coordinate and the transformed mask is used
                for defining brain boundary in diffusion coordinates. When t1Mask is
                not set, BDP will try to use fileprefix>.mask.nii.gz as brain-mask.
                If <fileprefix>.mask.nii.gz is not found, then BDP will use the
                input <fileprefix>.bfc.nii.gz itself as mask (i.e. all non-zero
                voxels in <fileprefix>.bfc.nii.gz is assumed to constitute brain
                mask).
                flag: --t1-mask %s
        terminal_output: ('stream' or 'allatonce' or 'file' or 'none')
                Control terminal output: `stream` - displays to terminal immediately
                (default), `allatonce` - waits till command is finished to display
                output, `file` - writes output to file, `none` - output is ignored
        threads: (an integer (int or long))
                Sets the number of parallel process threads which can be used for
                computations to N, where N must be an integer. Default value of N is
                flag: --threads=%d
        transformDataOnly: (a boolean)
                Skip all of the processing (co-registration, distortion correction
                and tensor/ODF estimation) and directly start transformation of
                defined custom volumes, mask and labels (using transformT1Volume,
                transformDiffusionVolume, transformT1Surface,
                transformDiffusionSurface, customDiffusionLabel, customT1Label).
                This flag is useful when BDP was previously run on a subject (or
                <fileprefix>) and some more data (volumes, mask or labels) need to
                be transformed across the T1-diffusion coordinate spaces. This
                assumes that all the necessary files were generated earlier and all
                of the other flags MUST be used in the same way as they were in the
                initial BDP run that processed the data.
                flag: --transform-data-only
        transformDiffusionSurface: (a file name)
                Same as transformT1Volume, except that the .dfs files specified must
                be in diffusion coordinate, i.e. the surface files should overlay
                correctly with the diffusion scan in BrainSuite. The transformed
                files are written to the output directory with suffix ".T1_coord" in
                the filename. See also transformT1Volume.
                flag: --transform-diffusion-surface %s
        transformDiffusionVolume: (a file name)
                This flag allows to define custom volumes in diffusion coordinate
                which would be transformed into T1 coordinate in a rigid fashion.
                The flag must be followed by the name of either a NIfTI file or of a
                folder that contains one or more NIfTI files. All of the files must
                be in diffusion coordinate, i.e. the files should overlay correctly
                with the diffusion scan in BrainSuite. Only NIfTI files with an
                extension of .nii or .nii.gz are supported. The transformed files
                are written to the output directory with suffix ".T1_coord" in the
                filename and will not be corrected for distortion, if any. The trait
                transformInterpolation can be used to define the type of
                interpolation that would be used (default is set to linear). If you
                are attempting to transform a label file or mask file, use "nearest"
                interpolation method with transformInterpolation. See also
                transformT1Volume and transformInterpolation
                flag: --transform-diffusion-volume %s
        transformInterpolation: ('linear' or 'nearest' or 'cubic' or
                 'spline')
                Defines the type of interpolation method which would be used while
                transforming volumes defined by transformT1Volume and
                transformDiffusionVolume. Possible methods are "linear", "nearest",
                "cubic" and "spline". By default, "linear" interpolation is used.
                flag: --transform-interpolation %s
        transformT1Surface: (a file name)
                Similar to transformT1Volume, except that this flag allows
                transforming surfaces (instead of volumes) in T1 coordinate into
                diffusion coordinate in a rigid fashion. The flag must be followed
                by the name of either a .dfs file or of a folder that contains one
                or more dfs files. All of the files must be in T1 coordinate, i.e.
                the files should overlay correctly with the T1-weighted scan in
                BrainSuite. The transformed files are written to the output
                directory with suffix D_coord" in the filename.
                flag: --transform-t1-surface %s
        transformT1Volume: (a file name)
                Same as transformDiffusionVolume except that files specified must be
                in T1 coordinate, i.e. the files should overlay correctly with the
                input <fileprefix>.bfc.nii.gz files in BrainSuite. BDP transforms
                these data/images from T1 coordinate to diffusion coordinate. The
                transformed files are written to the output directory with suffix
                ".D_coord" in the filename. See also transformDiffusionVolume and
                transformInterpolation.
                flag: --transform-t1-volume %s

Outputs::

        None

.. _nipype.interfaces.brainsuite.brainsuite.Bfc:


.. index:: Bfc

Bfc
---

`Link to code <http://github.com/nipy/nipype/tree/ec86b7476/nipype/interfaces/brainsuite/brainsuite.py#L172>`__

Wraps command **bfc**

bias field corrector (BFC)
This program corrects gain variation in T1-weighted MRI.

http://brainsuite.org/processing/surfaceextraction/bfc/

Examples
~~~~~~~~

>>> from nipype.interfaces import brainsuite
>>> from nipype.testing import example_data
>>> bfc = brainsuite.Bfc()
>>> bfc.inputs.inputMRIFile = example_data('structural.nii')
>>> bfc.inputs.inputMaskFile = example_data('mask.nii')
>>> results = bfc.run() #doctest: +SKIP

Inputs::

        [Mandatory]
        inputMRIFile: (a file name)
                input skull-stripped MRI volume
                flag: -i %s

        [Optional]
        args: (a unicode string)
                Additional parameters to the command
                flag: %s
        biasEstimateConvergenceThreshold: (a float)
                bias estimate convergence threshold (values > 0.1 disable)
                flag: --beps %f
        biasEstimateSpacing: (an integer (int or long))
                bias sample spacing (voxels)
                flag: -s %d
        biasFieldEstimatesOutputPrefix: (a unicode string)
                save iterative bias field estimates as <prefix>.n.field.nii.gz
                flag: --biasprefix %s
        biasRange: ('low' or 'medium' or 'high')
                Preset options for bias_model
                 low: small bias model [0.95,1.05]
                medium: medium bias model [0.90,1.10]
                 high: high bias model [0.80,1.20]
                flag: %s
        controlPointSpacing: (an integer (int or long))
                control point spacing (voxels)
                flag: -c %d
        convergenceThreshold: (a float)
                convergence threshold
                flag: --eps %f
        correctWholeVolume: (a boolean)
                apply correction field to entire volume
                flag: --extrapolate
        correctedImagesOutputPrefix: (a unicode string)
                save iterative corrected images as <prefix>.n.bfc.nii.gz
                flag: --prefix %s
        correctionScheduleFile: (a file name)
                list of parameters
                flag: --schedule %s
        environ: (a dictionary with keys which are a bytes or None or a value
                 of class 'str' and with values which are a bytes or None or a value
                 of class 'str', nipype default value: {})
                Environment variables
        histogramRadius: (an integer (int or long))
                histogram radius (voxels)
                flag: -r %d
        histogramType: ('ellipse' or 'block')
                Options for type of histogram
                ellipse: use ellipsoid for ROI histogram
                block :use block for ROI histogram
                flag: %s
        ignore_exception: (a boolean, nipype default value: False)
                Print an error message instead of throwing an exception in case the
                interface fails to run
        inputMaskFile: (a file name)
                mask file
                flag: -m %s
        intermediate_file_type: ('analyze' or 'nifti' or 'gzippedAnalyze' or
                 'gzippedNifti')
                Options for the format in which intermediate files are generated
                flag: %s
        iterativeMode: (a boolean)
                iterative mode (overrides -r, -s, -c, -w settings)
                flag: --iterate
        maxBias: (a float, nipype default value: 1.5)
                maximum allowed bias value
                flag: -U %f
        minBias: (a float, nipype default value: 0.5)
                minimum allowed bias value
                flag: -L %f
        outputBiasField: (a file name)
                save bias field estimate
                flag: --bias %s
        outputMRIVolume: (a file name)
                output bias-corrected MRI volume.If unspecified, output file name
                will be auto generated.
                flag: -o %s
        outputMaskedBiasField: (a file name)
                save bias field estimate (masked)
                flag: --maskedbias %s
        splineLambda: (a float)
                spline stiffness weighting parameter
                flag: -w %f
        terminal_output: ('stream' or 'allatonce' or 'file' or 'none')
                Control terminal output: `stream` - displays to terminal immediately
                (default), `allatonce` - waits till command is finished to display
                output, `file` - writes output to file, `none` - output is ignored
        timer: (a boolean)
                display timing information
                flag: --timer
        verbosityLevel: (an integer (int or long))
                verbosity level (0=silent)
                flag: -v %d

Outputs::

        correctionScheduleFile: (a file name)
                path/name of schedule file
        outputBiasField: (a file name)
                path/name of bias field output file
        outputMRIVolume: (a file name)
                path/name of output file
        outputMaskedBiasField: (a file name)
                path/name of masked bias field output

.. _nipype.interfaces.brainsuite.brainsuite.Bse:


.. index:: Bse

Bse
---

`Link to code <http://github.com/nipy/nipype/tree/ec86b7476/nipype/interfaces/brainsuite/brainsuite.py#L63>`__

Wraps command **bse**

brain surface extractor (BSE)
This program performs automated skull and scalp removal on T1-weighted MRI volumes.

http://brainsuite.org/processing/surfaceextraction/bse/

Examples
~~~~~~~~

>>> from nipype.interfaces import brainsuite
>>> from nipype.testing import example_data
>>> bse = brainsuite.Bse()
>>> bse.inputs.inputMRIFile = example_data('structural.nii')
>>> results = bse.run() #doctest: +SKIP

Inputs::

        [Mandatory]
        inputMRIFile: (a file name)
                input MRI volume
                flag: -i %s

        [Optional]
        args: (a unicode string)
                Additional parameters to the command
                flag: %s
        diffusionConstant: (a float, nipype default value: 25)
                diffusion constant
                flag: -d %f
        diffusionIterations: (an integer (int or long), nipype default value:
                 3)
                diffusion iterations
                flag: -n %d
        dilateFinalMask: (a boolean, nipype default value: True)
                dilate final mask
                flag: -p
        edgeDetectionConstant: (a float, nipype default value: 0.64)
                edge detection constant
                flag: -s %f
        environ: (a dictionary with keys which are a bytes or None or a value
                 of class 'str' and with values which are a bytes or None or a value
                 of class 'str', nipype default value: {})
                Environment variables
        ignore_exception: (a boolean, nipype default value: False)
                Print an error message instead of throwing an exception in case the
                interface fails to run
        noRotate: (a boolean)
                retain original orientation(default behavior will auto-rotate input
                NII files to LPI orientation)
                flag: --norotate
        outputCortexFile: (a file name)
                cortex file
                flag: --cortex %s
        outputDetailedBrainMask: (a file name)
                save detailed brain mask
                flag: --hires %s
        outputDiffusionFilter: (a file name)
                diffusion filter output
                flag: --adf %s
        outputEdgeMap: (a file name)
                edge map output
                flag: --edge %s
        outputMRIVolume: (a file name)
                output brain-masked MRI volume. If unspecified, output file name
                will be auto generated.
                flag: -o %s
        outputMaskFile: (a file name)
                save smooth brain mask. If unspecified, output file name will be
                auto generated.
                flag: --mask %s
        radius: (a float, nipype default value: 1)
                radius of erosion/dilation filter
                flag: -r %f
        terminal_output: ('stream' or 'allatonce' or 'file' or 'none')
                Control terminal output: `stream` - displays to terminal immediately
                (default), `allatonce` - waits till command is finished to display
                output, `file` - writes output to file, `none` - output is ignored
        timer: (a boolean)
                show timing
                flag: --timer
        trim: (a boolean, nipype default value: True)
                trim brainstem
                flag: --trim
        verbosityLevel: (a float, nipype default value: 1)
                 verbosity level (0=silent)
                flag: -v %f

Outputs::

        outputCortexFile: (a file name)
                path/name of cortex file
        outputDetailedBrainMask: (a file name)
                path/name of detailed brain mask
        outputDiffusionFilter: (a file name)
                path/name of diffusion filter output
        outputEdgeMap: (a file name)
                path/name of edge map output
        outputMRIVolume: (a file name)
                path/name of brain-masked MRI volume
        outputMaskFile: (a file name)
                path/name of smooth brain mask

.. _nipype.interfaces.brainsuite.brainsuite.Cerebro:


.. index:: Cerebro

Cerebro
-------

`Link to code <http://github.com/nipy/nipype/tree/ec86b7476/nipype/interfaces/brainsuite/brainsuite.py#L327>`__

Wraps command **cerebro**

Cerebrum/cerebellum labeling tool
This program performs automated labeling of cerebellum and cerebrum in T1 MRI.
Input MRI should be skull-stripped or a brain-only mask should be provided.


http://brainsuite.org/processing/surfaceextraction/cerebrum/

Examples
~~~~~~~~

>>> from nipype.interfaces import brainsuite
>>> from nipype.testing import example_data
>>> cerebro = brainsuite.Cerebro()
>>> cerebro.inputs.inputMRIFile = example_data('structural.nii')
>>> cerebro.inputs.inputAtlasMRIFile = 'atlasMRIVolume.img'
>>> cerebro.inputs.inputAtlasLabelFile = 'atlasLabels.img'
>>> cerebro.inputs.inputBrainMaskFile = example_data('mask.nii')
>>> results = cerebro.run() #doctest: +SKIP

Inputs::

        [Mandatory]
        inputAtlasLabelFile: (a file name)
                atlas labeling
                flag: --atlaslabels %s
        inputAtlasMRIFile: (a file name)
                atlas MRI volume
                flag: --atlas %s
        inputMRIFile: (a file name)
                input 3D MRI volume
                flag: -i %s

        [Optional]
        args: (a unicode string)
                Additional parameters to the command
                flag: %s
        costFunction: (an integer (int or long), nipype default value: 2)
                0,1,2
                flag: -c %d
        environ: (a dictionary with keys which are a bytes or None or a value
                 of class 'str' and with values which are a bytes or None or a value
                 of class 'str', nipype default value: {})
                Environment variables
        ignore_exception: (a boolean, nipype default value: False)
                Print an error message instead of throwing an exception in case the
                interface fails to run
        inputBrainMaskFile: (a file name)
                brain mask file
                flag: -m %s
        keepTempFiles: (a boolean)
                don't remove temporary files
                flag: --keep
        linearConvergence: (a float)
                linear convergence
                flag: --linconv %f
        outputAffineTransformFile: (a file name)
                save affine transform to file.
                flag: --air %s
        outputCerebrumMaskFile: (a file name)
                output cerebrum mask volume. If unspecified, output file name will
                be auto generated.
                flag: -o %s
        outputLabelVolumeFile: (a file name)
                output labeled hemisphere/cerebrum volume. If unspecified, output
                file name will be auto generated.
                flag: -l %s
        outputWarpTransformFile: (a file name)
                save warp transform to file.
                flag: --warp %s
        tempDirectory: (a unicode string)
                specify directory to use for temporary files
                flag: --tempdir %s
        tempDirectoryBase: (a unicode string)
                create a temporary directory within this directory
                flag: --tempdirbase %s
        terminal_output: ('stream' or 'allatonce' or 'file' or 'none')
                Control terminal output: `stream` - displays to terminal immediately
                (default), `allatonce` - waits till command is finished to display
                output, `file` - writes output to file, `none` - output is ignored
        useCentroids: (a boolean)
                use centroids of data to initialize position
                flag: --centroids
        verbosity: (an integer (int or long))
                verbosity level (0=silent)
                flag: -v %d
        warpConvergence: (a float)
                warp convergence
                flag: --warpconv %f
        warpLabel: (an integer (int or long))
                warp order (2,3,4,5,6,7,8)
                flag: --warplevel %d

Outputs::

        outputAffineTransformFile: (a file name)
                path/name of affine transform file
        outputCerebrumMaskFile: (a file name)
                path/name of cerebrum mask file
        outputLabelVolumeFile: (a file name)
                path/name of label mask file
        outputWarpTransformFile: (a file name)
                path/name of warp transform file

.. _nipype.interfaces.brainsuite.brainsuite.Cortex:


.. index:: Cortex

Cortex
------

`Link to code <http://github.com/nipy/nipype/tree/ec86b7476/nipype/interfaces/brainsuite/brainsuite.py#L398>`__

Wraps command **cortex**

cortex extractor
This program produces a cortical mask using tissue fraction estimates
and a co-registered cerebellum/hemisphere mask.

http://brainsuite.org/processing/surfaceextraction/cortex/

Examples
~~~~~~~~

>>> from nipype.interfaces import brainsuite
>>> from nipype.testing import example_data
>>> cortex = brainsuite.Cortex()
>>> cortex.inputs.inputHemisphereLabelFile = example_data('mask.nii')
>>> cortex.inputs.inputTissueFractionFile = example_data('tissues.nii.gz')
>>> results = cortex.run() #doctest: +SKIP

Inputs::

        [Mandatory]
        inputHemisphereLabelFile: (a file name)
                hemisphere / lobe label volume
                flag: -h %s
        inputTissueFractionFile: (a file name)
                tissue fraction file (32-bit float)
                flag: -f %s

        [Optional]
        args: (a unicode string)
                Additional parameters to the command
                flag: %s
        computeGCBoundary: (a boolean)
                compute GM/CSF boundary
                flag: -g
        computeWGBoundary: (a boolean, nipype default value: True)
                compute WM/GM boundary
                flag: -w
        environ: (a dictionary with keys which are a bytes or None or a value
                 of class 'str' and with values which are a bytes or None or a value
                 of class 'str', nipype default value: {})
                Environment variables
        ignore_exception: (a boolean, nipype default value: False)
                Print an error message instead of throwing an exception in case the
                interface fails to run
        includeAllSubcorticalAreas: (a boolean, nipype default value: True)
                include all subcortical areas in WM mask
                flag: -a
        outputCerebrumMask: (a file name)
                output structure mask. If unspecified, output file name will be auto
                generated.
                flag: -o %s
        terminal_output: ('stream' or 'allatonce' or 'file' or 'none')
                Control terminal output: `stream` - displays to terminal immediately
                (default), `allatonce` - waits till command is finished to display
                output, `file` - writes output to file, `none` - output is ignored
        timer: (a boolean)
                timing function
                flag: --timer
        tissueFractionThreshold: (a float, nipype default value: 50.0)
                tissue fraction threshold (percentage)
                flag: -p %f
        verbosity: (an integer (int or long))
                verbosity level
                flag: -v %d

Outputs::

        outputCerebrumMask: (a file name)
                path/name of cerebrum mask

.. _nipype.interfaces.brainsuite.brainsuite.Dewisp:


.. index:: Dewisp

Dewisp
------

`Link to code <http://github.com/nipy/nipype/tree/ec86b7476/nipype/interfaces/brainsuite/brainsuite.py#L560>`__

Wraps command **dewisp**

dewisp
removes wispy tendril structures from cortex model binary masks.
It does so based on graph theoretic analysis of connected components,
similar to TCA. Each branch of the structure graph is analyzed to determine
pinch points that indicate a likely error in segmentation that attaches noise
to the image. The pinch threshold determines how many voxels the cross-section
can be before it is considered part of the image.

http://brainsuite.org/processing/surfaceextraction/dewisp/

Examples
~~~~~~~~

>>> from nipype.interfaces import brainsuite
>>> from nipype.testing import example_data
>>> dewisp = brainsuite.Dewisp()
>>> dewisp.inputs.inputMaskFile = example_data('mask.nii')
>>> results = dewisp.run() #doctest: +SKIP

Inputs::

        [Mandatory]
        inputMaskFile: (a file name)
                input file
                flag: -i %s

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
        maximumIterations: (an integer (int or long))
                maximum number of iterations
                flag: -n %d
        outputMaskFile: (a file name)
                output file. If unspecified, output file name will be auto
                generated.
                flag: -o %s
        sizeThreshold: (an integer (int or long))
                size threshold
                flag: -t %d
        terminal_output: ('stream' or 'allatonce' or 'file' or 'none')
                Control terminal output: `stream` - displays to terminal immediately
                (default), `allatonce` - waits till command is finished to display
                output, `file` - writes output to file, `none` - output is ignored
        timer: (a boolean)
                time processing
                flag: --timer
        verbosity: (an integer (int or long))
                verbosity
                flag: -v %d

Outputs::

        outputMaskFile: (a file name)
                path/name of mask file

.. _nipype.interfaces.brainsuite.brainsuite.Dfs:


.. index:: Dfs

Dfs
---

`Link to code <http://github.com/nipy/nipype/tree/ec86b7476/nipype/interfaces/brainsuite/brainsuite.py#L636>`__

Wraps command **dfs**

Surface Generator
Generates mesh surfaces using an isosurface algorithm.

http://brainsuite.org/processing/surfaceextraction/inner-cortical-surface/

Examples
~~~~~~~~

>>> from nipype.interfaces import brainsuite
>>> from nipype.testing import example_data
>>> dfs = brainsuite.Dfs()
>>> dfs.inputs.inputVolumeFile = example_data('structural.nii')
>>> results = dfs.run() #doctest: +SKIP

Inputs::

        [Mandatory]
        inputVolumeFile: (a file name)
                input 3D volume
                flag: -i %s

        [Optional]
        args: (a unicode string)
                Additional parameters to the command
                flag: %s
        curvatureWeighting: (a float, nipype default value: 5.0)
                curvature weighting
                flag: -w %f
        environ: (a dictionary with keys which are a bytes or None or a value
                 of class 'str' and with values which are a bytes or None or a value
                 of class 'str', nipype default value: {})
                Environment variables
        ignore_exception: (a boolean, nipype default value: False)
                Print an error message instead of throwing an exception in case the
                interface fails to run
        inputShadingVolume: (a file name)
                shade surface model with data from image volume
                flag: -c %s
        noNormalsFlag: (a boolean)
                do not compute vertex normals
                flag: --nonormals
        nonZeroTessellation: (a boolean)
                tessellate non-zero voxels
                flag: -nz
                mutually_exclusive: nonZeroTessellation, specialTessellation
        outputSurfaceFile: (a file name)
                output surface mesh file. If unspecified, output file name will be
                auto generated.
                flag: -o %s
        postSmoothFlag: (a boolean)
                smooth vertices after coloring
                flag: --postsmooth
        scalingPercentile: (a float)
                scaling percentile
                flag: -f %f
        smoothingConstant: (a float, nipype default value: 0.5)
                smoothing constant
                flag: -a %f
        smoothingIterations: (an integer (int or long), nipype default value:
                 10)
                number of smoothing iterations
                flag: -n %d
        specialTessellation: ('greater_than' or 'less_than' or 'equal_to')
                To avoid throwing a UserWarning, set tessellationThreshold first.
                Then set this attribute.
                Usage: tessellate voxels greater_than, less_than, or equal_to
                <tessellationThreshold>
                flag: %s, position: -1
                mutually_exclusive: nonZeroTessellation, specialTessellation
                requires: tessellationThreshold
        terminal_output: ('stream' or 'allatonce' or 'file' or 'none')
                Control terminal output: `stream` - displays to terminal immediately
                (default), `allatonce` - waits till command is finished to display
                output, `file` - writes output to file, `none` - output is ignored
        tessellationThreshold: (a float)
                To be used with specialTessellation. Set this value first, then set
                specialTessellation value.
                Usage: tessellate voxels greater_than, less_than, or equal_to
                <tessellationThreshold>
                flag: %f
        timer: (a boolean)
                timing function
                flag: --timer
        verbosity: (an integer (int or long))
                verbosity (0 = quiet)
                flag: -v %d
        zeroPadFlag: (a boolean)
                zero-pad volume (avoids clipping at edges)
                flag: -z

Outputs::

        outputSurfaceFile: (a file name)
                path/name of surface file

.. _nipype.interfaces.brainsuite.brainsuite.Hemisplit:


.. index:: Hemisplit

Hemisplit
---------

`Link to code <http://github.com/nipy/nipype/tree/ec86b7476/nipype/interfaces/brainsuite/brainsuite.py#L786>`__

Wraps command **hemisplit**

Hemisphere splitter
Splits a surface object into two separate surfaces given an input label volume.
Each vertex is labeled left or right based on the labels being odd (left) or even (right).
The largest contour on the split surface is then found and used as the separation between left and right.

Examples
~~~~~~~~

>>> from nipype.interfaces import brainsuite
>>> from nipype.testing import example_data
>>> hemisplit = brainsuite.Hemisplit()
>>> hemisplit.inputs.inputSurfaceFile = 'input_surf.dfs'
>>> hemisplit.inputs.inputHemisphereLabelFile = 'label.nii'
>>> hemisplit.inputs.pialSurfaceFile = 'pial.dfs'
>>> results = hemisplit.run() #doctest: +SKIP

Inputs::

        [Mandatory]
        inputHemisphereLabelFile: (a file name)
                input hemisphere label volume
                flag: -l %s
        inputSurfaceFile: (a file name)
                input surface
                flag: -i %s

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
        outputLeftHemisphere: (a file name)
                output surface file, left hemisphere. If unspecified, output file
                name will be auto generated.
                flag: --left %s
        outputLeftPialHemisphere: (a file name)
                output pial surface file, left hemisphere. If unspecified, output
                file name will be auto generated.
                flag: -pl %s
        outputRightHemisphere: (a file name)
                output surface file, right hemisphere. If unspecified, output file
                name will be auto generated.
                flag: --right %s
        outputRightPialHemisphere: (a file name)
                output pial surface file, right hemisphere. If unspecified, output
                file name will be auto generated.
                flag: -pr %s
        pialSurfaceFile: (a file name)
                pial surface file -- must have same geometry as input surface
                flag: -p %s
        terminal_output: ('stream' or 'allatonce' or 'file' or 'none')
                Control terminal output: `stream` - displays to terminal immediately
                (default), `allatonce` - waits till command is finished to display
                output, `file` - writes output to file, `none` - output is ignored
        timer: (a boolean)
                timing function
                flag: --timer
        verbosity: (an integer (int or long))
                verbosity (0 = silent)
                flag: -v %d

Outputs::

        outputLeftHemisphere: (a file name)
                path/name of left hemisphere
        outputLeftPialHemisphere: (a file name)
                path/name of left pial hemisphere
        outputRightHemisphere: (a file name)
                path/name of right hemisphere
        outputRightPialHemisphere: (a file name)
                path/name of right pial hemisphere

.. _nipype.interfaces.brainsuite.brainsuite.Pialmesh:


.. index:: Pialmesh

Pialmesh
--------

`Link to code <http://github.com/nipy/nipype/tree/ec86b7476/nipype/interfaces/brainsuite/brainsuite.py#L721>`__

Wraps command **pialmesh**

pialmesh
computes a pial surface model using an inner WM/GM mesh and a tissue fraction map.

http://brainsuite.org/processing/surfaceextraction/pial/

Examples
~~~~~~~~

>>> from nipype.interfaces import brainsuite
>>> from nipype.testing import example_data
>>> pialmesh = brainsuite.Pialmesh()
>>> pialmesh.inputs.inputSurfaceFile = 'input_mesh.dfs'
>>> pialmesh.inputs.inputTissueFractionFile = 'frac_file.nii.gz'
>>> pialmesh.inputs.inputMaskFile = example_data('mask.nii')
>>> results = pialmesh.run() #doctest: +SKIP

Inputs::

        [Mandatory]
        inputMaskFile: (a file name)
                restrict growth to mask file region
                flag: -m %s
        inputSurfaceFile: (a file name)
                input file
                flag: -i %s
        inputTissueFractionFile: (a file name)
                floating point (32) tissue fraction image
                flag: -f %s

        [Optional]
        args: (a unicode string)
                Additional parameters to the command
                flag: %s
        environ: (a dictionary with keys which are a bytes or None or a value
                 of class 'str' and with values which are a bytes or None or a value
                 of class 'str', nipype default value: {})
                Environment variables
        exportPrefix: (a unicode string)
                prefix for exporting surfaces if interval is set
                flag: --prefix %s
        ignore_exception: (a boolean, nipype default value: False)
                Print an error message instead of throwing an exception in case the
                interface fails to run
        laplacianSmoothing: (a float, nipype default value: 0.025)
                apply Laplacian smoothing
                flag: --smooth %f
        maxThickness: (a float, nipype default value: 20)
                maximum allowed tissue thickness
                flag: --max %f
        normalSmoother: (a float, nipype default value: 0.2)
                strength of normal smoother.
                flag: --nc %f
        numIterations: (an integer (int or long), nipype default value: 100)
                number of iterations
                flag: -n %d
        outputInterval: (an integer (int or long), nipype default value: 10)
                output interval
                flag: --interval %d
        outputSurfaceFile: (a file name)
                output file. If unspecified, output file name will be auto
                generated.
                flag: -o %s
        recomputeNormals: (a boolean)
                recompute normals at each iteration
                flag: --norm
        searchRadius: (a float, nipype default value: 1)
                search radius
                flag: -r %f
        stepSize: (a float, nipype default value: 0.4)
                step size
                flag: -s %f
        tangentSmoother: (a float)
                strength of tangential smoother.
                flag: --tc %f
        terminal_output: ('stream' or 'allatonce' or 'file' or 'none')
                Control terminal output: `stream` - displays to terminal immediately
                (default), `allatonce` - waits till command is finished to display
                output, `file` - writes output to file, `none` - output is ignored
        timer: (a boolean)
                show timing
                flag: --timer
        tissueThreshold: (a float, nipype default value: 1.05)
                tissue threshold
                flag: -t %f
        verbosity: (an integer (int or long))
                verbosity
                flag: -v %d

Outputs::

        outputSurfaceFile: (a file name)
                path/name of surface file

.. _nipype.interfaces.brainsuite.brainsuite.Pvc:


.. index:: Pvc

Pvc
---

`Link to code <http://github.com/nipy/nipype/tree/ec86b7476/nipype/interfaces/brainsuite/brainsuite.py#L242>`__

Wraps command **pvc**

partial volume classifier (PVC) tool.
This program performs voxel-wise tissue classification T1-weighted MRI.
Image should be skull-stripped and bias-corrected before tissue classification.

http://brainsuite.org/processing/surfaceextraction/pvc/

Examples
~~~~~~~~

>>> from nipype.interfaces import brainsuite
>>> from nipype.testing import example_data
>>> pvc = brainsuite.Pvc()
>>> pvc.inputs.inputMRIFile = example_data('structural.nii')
>>> pvc.inputs.inputMaskFile = example_data('mask.nii')
>>> results = pvc.run() #doctest: +SKIP

Inputs::

        [Mandatory]
        inputMRIFile: (a file name)
                MRI file
                flag: -i %s

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
        inputMaskFile: (a file name)
                brain mask file
                flag: -m %s
        outputLabelFile: (a file name)
                output label file. If unspecified, output file name will be auto
                generated.
                flag: -o %s
        outputTissueFractionFile: (a file name)
                output tissue fraction file
                flag: -f %s
        spatialPrior: (a float)
                spatial prior strength
                flag: -l %f
        terminal_output: ('stream' or 'allatonce' or 'file' or 'none')
                Control terminal output: `stream` - displays to terminal immediately
                (default), `allatonce` - waits till command is finished to display
                output, `file` - writes output to file, `none` - output is ignored
        threeClassFlag: (a boolean)
                use a three-class (CSF=0,GM=1,WM=2) labeling
                flag: -3
        timer: (a boolean)
                time processing
                flag: --timer
        verbosity: (an integer (int or long))
                verbosity level (0 = silent)
                flag: -v %d

Outputs::

        outputLabelFile: (a file name)
                path/name of label file
        outputTissueFractionFile: (a file name)
                path/name of tissue fraction file

.. _nipype.interfaces.brainsuite.brainsuite.SVReg:


.. index:: SVReg

SVReg
-----

`Link to code <http://github.com/nipy/nipype/tree/ec86b7476/nipype/interfaces/brainsuite/brainsuite.py#L1015>`__

Wraps command **svreg.sh**

surface and volume registration (svreg)
This program registers a subject's BrainSuite-processed volume and surfaces
to an atlas, allowing for automatic labelling of volume and surface ROIs.

For more information, please see:
http://brainsuite.org/processing/svreg/usage/

Examples
~~~~~~~~

>>> from nipype.interfaces import brainsuite
>>> svreg = brainsuite.SVReg()
>>> svreg.inputs.subjectFilePrefix = 'home/user/btestsubject/testsubject'
>>> svreg.inputs.refineOutputs = True
>>> svreg.inputs.skipToVolumeReg = False
>>> svreg.inputs. keepIntermediates = True
>>> svreg.inputs.verbosity2 = True
>>> svreg.inputs.displayTimestamps = True
>>> svreg.inputs.useSingleThreading = True
>>> results = svreg.run() #doctest: +SKIP

Inputs::

        [Mandatory]
        subjectFilePrefix: (a unicode string)
                Absolute path and filename prefix of the subjects output from
                BrainSuite Cortical Surface Extraction Sequence
                flag: '%s', position: 0

        [Optional]
        args: (a unicode string)
                Additional parameters to the command
                flag: %s
        atlasFilePrefix: (a unicode string)
                Optional: Absolute Path and filename prefix of atlas files and
                labels to which the subject will be registered. If unspecified,
                SVRegwill use its own included atlas files
                flag: '%s', position: 1
        curveMatchingInstructions: (a unicode string)
                Used to take control of the curve matching process between the atlas
                and subject. One can specify the name of the .dfc file <sulname.dfc>
                and the sulcal numbers <#sul> to be used as constraints. example:
                curveMatchingInstructions = "subbasename.right.dfc 1 2 20"
                flag: '-cur %s'
        dataSinkDelay: (a list of items which are a value of class 'str')
                Connect datasink out_file to dataSinkDelay to delay execution of
                SVReg until dataSink has finished sinking CSE outputs.For use with
                parallel processing workflows including Brainsuites Cortical Surface
                Extraction sequence (SVReg requires certain files from Brainsuite
                CSE, which must all be in the pathway specified by
                subjectFilePrefix. see http://brainsuite.org/processing/svreg/usage/
                for list of required inputs
                flag: %s
        displayModuleName: (a boolean)
                Module name will be displayed in the messages
                flag: '-m'
        displayTimestamps: (a boolean)
                Timestamps will be displayed in the messages
                flag: '-t'
        environ: (a dictionary with keys which are a bytes or None or a value
                 of class 'str' and with values which are a bytes or None or a value
                 of class 'str', nipype default value: {})
                Environment variables
        ignore_exception: (a boolean, nipype default value: False)
                Print an error message instead of throwing an exception in case the
                interface fails to run
        iterations: (an integer (int or long))
                Assigns a number of iterations in the intensity registration step.if
                unspecified, performs 100 iterations
                flag: '-H %d'
        keepIntermediates: (a boolean)
                Keep the intermediate files after the svreg sequence is complete.
                flag: '-k'
        pialSurfaceMaskDilation: (an integer (int or long))
                Cortical volume labels found in file output
                subbasename.svreg.label.nii.gz find its boundaries by using the pial
                surface then dilating by 1 voxel. Use this flag in order to control
                the number of pial surface mask dilation. (ie. -D 0 will assign no
                voxel dilation)
                flag: '-D %d'
        refineOutputs: (a boolean)
                Refine outputs at the expense of more processing time.
                flag: '-r'
        shortMessages: (a boolean)
                Short messages instead of detailed messages
                flag: '-gui'
        skipToIntensityReg: (a boolean)
                If the p-harmonic volumetric registration was already performed at
                an earlier time and the user would not like to redo this step, then
                this flag may be used to skip ahead to the intensity registration
                and label transfer step.
                flag: '-p'
        skipToVolumeReg: (a boolean)
                If surface registration was already performed at an earlier time and
                the user would not like to redo this step, then this flag may be
                used to skip ahead to the volumetric registration. Necessary input
                files will need to be present in the input directory called by the
                command.
                flag: '-s'
        skipVolumetricProcessing: (a boolean)
                Only surface registration and labeling will be performed. Volumetric
                processing will be skipped.
                flag: '-S'
        terminal_output: ('stream' or 'allatonce' or 'file' or 'none')
                Control terminal output: `stream` - displays to terminal immediately
                (default), `allatonce` - waits till command is finished to display
                output, `file` - writes output to file, `none` - output is ignored
        useCerebrumMask: (a boolean)
                The cerebrum mask <subbasename.cerebrum.mask.nii.gz> will be used
                for masking the final labels instead of the default pial surface
                mask. Every voxel will be labeled within the cerebrum mask
                regardless of the boundaries of the pial surface.
                flag: '-C'
        useManualMaskFile: (a boolean)
                Can call a manually edited cerebrum mask to limit boundaries. Will
                use file: subbasename.cerebrum.mask.nii.gz Make sure to correctly
                replace your manually edited mask file in your input folder with the
                correct subbasename.
                flag: '-cbm'
        useMultiThreading: (a boolean)
                If multiple CPUs are present on the system, the code will try to use
                multithreading to make the execution fast.
                flag: '-P'
        useSingleThreading: (a boolean)
                Use single threaded mode.
                flag: '-U'
        verbosity0: (a boolean)
                no messages will be reported
                flag: '-v0'
                mutually_exclusive: verbosity0, verbosity1, verbosity2
        verbosity1: (a boolean)
                messages will be reported but not the iteration-wise detailed
                messages
                flag: '-v1'
                mutually_exclusive: verbosity0, verbosity1, verbosity2
        verbosity2: (a boolean)
                all the messages, including per-iteration, will be displayed
                flag: 'v2'
                mutually_exclusive: verbosity0, verbosity1, verbosity2

Outputs::

        None

.. _nipype.interfaces.brainsuite.brainsuite.Scrubmask:


.. index:: Scrubmask

Scrubmask
---------

`Link to code <http://github.com/nipy/nipype/tree/ec86b7476/nipype/interfaces/brainsuite/brainsuite.py#L454>`__

Wraps command **scrubmask**

ScrubMask tool
scrubmask filters binary masks to trim loosely connected voxels that may
result from segmentation errors and produce bumps on tessellated surfaces.

http://brainsuite.org/processing/surfaceextraction/scrubmask/

Examples
~~~~~~~~

>>> from nipype.interfaces import brainsuite
>>> from nipype.testing import example_data
>>> scrubmask = brainsuite.Scrubmask()
>>> scrubmask.inputs.inputMaskFile = example_data('mask.nii')
>>> results = scrubmask.run() #doctest: +SKIP

Inputs::

        [Mandatory]
        inputMaskFile: (a file name)
                input structure mask file
                flag: -i %s

        [Optional]
        args: (a unicode string)
                Additional parameters to the command
                flag: %s
        backgroundFillThreshold: (an integer (int or long), nipype default
                 value: 2)
                background fill threshold
                flag: -b %d
        environ: (a dictionary with keys which are a bytes or None or a value
                 of class 'str' and with values which are a bytes or None or a value
                 of class 'str', nipype default value: {})
                Environment variables
        foregroundTrimThreshold: (an integer (int or long), nipype default
                 value: 0)
                foreground trim threshold
                flag: -f %d
        ignore_exception: (a boolean, nipype default value: False)
                Print an error message instead of throwing an exception in case the
                interface fails to run
        numberIterations: (an integer (int or long))
                number of iterations
                flag: -n %d
        outputMaskFile: (a file name)
                output structure mask file. If unspecified, output file name will be
                auto generated.
                flag: -o %s
        terminal_output: ('stream' or 'allatonce' or 'file' or 'none')
                Control terminal output: `stream` - displays to terminal immediately
                (default), `allatonce` - waits till command is finished to display
                output, `file` - writes output to file, `none` - output is ignored
        timer: (a boolean)
                timing function
                flag: --timer
        verbosity: (an integer (int or long))
                verbosity (0=silent)
                flag: -v %d

Outputs::

        outputMaskFile: (a file name)
                path/name of mask file

.. _nipype.interfaces.brainsuite.brainsuite.Skullfinder:


.. index:: Skullfinder

Skullfinder
-----------

`Link to code <http://github.com/nipy/nipype/tree/ec86b7476/nipype/interfaces/brainsuite/brainsuite.py#L864>`__

Wraps command **skullfinder**

Skull and scalp segmentation algorithm.

Examples
~~~~~~~~

>>> from nipype.interfaces import brainsuite
>>> from nipype.testing import example_data
>>> skullfinder = brainsuite.Skullfinder()
>>> skullfinder.inputs.inputMRIFile = example_data('structural.nii')
>>> skullfinder.inputs.inputMaskFile = example_data('mask.nii')
>>> results = skullfinder.run() #doctest: +SKIP

Inputs::

        [Mandatory]
        inputMRIFile: (a file name)
                input file
                flag: -i %s
        inputMaskFile: (a file name)
                A brain mask file, 8-bit image (0=non-brain, 255=brain)
                flag: -m %s

        [Optional]
        args: (a unicode string)
                Additional parameters to the command
                flag: %s
        bgLabelValue: (an integer (int or long))
                background label value (0-255)
                flag: --bglabel %d
        brainLabelValue: (an integer (int or long))
                brain label value (0-255)
                flag: --brainlabel %d
        environ: (a dictionary with keys which are a bytes or None or a value
                 of class 'str' and with values which are a bytes or None or a value
                 of class 'str', nipype default value: {})
                Environment variables
        ignore_exception: (a boolean, nipype default value: False)
                Print an error message instead of throwing an exception in case the
                interface fails to run
        lowerThreshold: (an integer (int or long))
                Lower threshold for segmentation
                flag: -l %d
        outputLabelFile: (a file name)
                output multi-colored label volume segmenting brain, scalp, inner
                skull & outer skull If unspecified, output file name will be auto
                generated.
                flag: -o %s
        performFinalOpening: (a boolean)
                perform a final opening operation on the scalp mask
                flag: --finalOpening
        scalpLabelValue: (an integer (int or long))
                scalp label value (0-255)
                flag: --scalplabel %d
        skullLabelValue: (an integer (int or long))
                skull label value (0-255)
                flag: --skulllabel %d
        spaceLabelValue: (an integer (int or long))
                space label value (0-255)
                flag: --spacelabel %d
        surfaceFilePrefix: (a unicode string)
                if specified, generate surface files for brain, skull, and scalp
                flag: -s %s
        terminal_output: ('stream' or 'allatonce' or 'file' or 'none')
                Control terminal output: `stream` - displays to terminal immediately
                (default), `allatonce` - waits till command is finished to display
                output, `file` - writes output to file, `none` - output is ignored
        upperThreshold: (an integer (int or long))
                Upper threshold for segmentation
                flag: -u %d
        verbosity: (an integer (int or long))
                verbosity
                flag: -v %d

Outputs::

        outputLabelFile: (a file name)
                path/name of label file

.. _nipype.interfaces.brainsuite.brainsuite.Tca:


.. index:: Tca

Tca
---

`Link to code <http://github.com/nipy/nipype/tree/ec86b7476/nipype/interfaces/brainsuite/brainsuite.py#L510>`__

Wraps command **tca**

topological correction algorithm (TCA)
This program removes topological handles from a binary object.

http://brainsuite.org/processing/surfaceextraction/tca/

Examples
~~~~~~~~
>>> from nipype.interfaces import brainsuite
>>> from nipype.testing import example_data
>>> tca = brainsuite.Tca()
>>> tca.inputs.inputMaskFile = example_data('mask.nii')
>>> results = tca.run() #doctest: +SKIP

Inputs::

        [Mandatory]
        inputMaskFile: (a file name)
                input mask volume
                flag: -i %s

        [Optional]
        args: (a unicode string)
                Additional parameters to the command
                flag: %s
        environ: (a dictionary with keys which are a bytes or None or a value
                 of class 'str' and with values which are a bytes or None or a value
                 of class 'str', nipype default value: {})
                Environment variables
        foregroundDelta: (an integer (int or long), nipype default value: 20)
                foreground delta
                flag: --delta %d
        ignore_exception: (a boolean, nipype default value: False)
                Print an error message instead of throwing an exception in case the
                interface fails to run
        maxCorrectionSize: (an integer (int or long))
                minimum correction size
                flag: -n %d
        minCorrectionSize: (an integer (int or long), nipype default value:
                 2500)
                maximum correction size
                flag: -m %d
        outputMaskFile: (a file name)
                output mask volume. If unspecified, output file name will be auto
                generated.
                flag: -o %s
        terminal_output: ('stream' or 'allatonce' or 'file' or 'none')
                Control terminal output: `stream` - displays to terminal immediately
                (default), `allatonce` - waits till command is finished to display
                output, `file` - writes output to file, `none` - output is ignored
        timer: (a boolean)
                timing function
                flag: --timer
        verbosity: (an integer (int or long))
                verbosity (0 = quiet)
                flag: -v %d

Outputs::

        outputMaskFile: (a file name)
                path/name of mask file

.. _nipype.interfaces.brainsuite.brainsuite.ThicknessPVC:


.. index:: ThicknessPVC

ThicknessPVC
------------

`Link to code <http://github.com/nipy/nipype/tree/ec86b7476/nipype/interfaces/brainsuite/brainsuite.py#L1576>`__

Wraps command **thicknessPVC.sh**

ThicknessPVC computes cortical thickness using partial tissue fractions.
This thickness measure is then transferred to the atlas surface to
facilitate population studies. It also stores the computed thickness into
separate hemisphere files and subject thickness mapped to the atlas
hemisphere surfaces. ThicknessPVC is not run through the main SVReg
sequence, and should be used after executing the BrainSuite and SVReg
sequence.
For more informaction, please see:

http://brainsuite.org/processing/svreg/svreg_modules/

Examples
~~~~~~~~

>>> from nipype.interfaces import brainsuite
>>> thicknessPVC = brainsuite.ThicknessPVC()
>>> thicknessPVC.inputs.subjectFilePrefix = 'home/user/btestsubject/testsubject'
>>> results = thicknessPVC.run() #doctest: +SKIP

Inputs::

        [Mandatory]
        subjectFilePrefix: (a unicode string)
                Absolute path and filename prefix of the subject data
                flag: %s

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
        terminal_output: ('stream' or 'allatonce' or 'file' or 'none')
                Control terminal output: `stream` - displays to terminal immediately
                (default), `allatonce` - waits till command is finished to display
                output, `file` - writes output to file, `none` - output is ignored

Outputs::

        None

.. module:: nipype.interfaces.brainsuite.brainsuite


.. _nipype.interfaces.brainsuite.brainsuite.getFileName:

:func:`getFileName`
-------------------

`Link to code <http://github.com/nipy/nipype/tree/ec86b7476/nipype/interfaces/brainsuite/brainsuite.py#L1607>`__






.. _nipype.interfaces.brainsuite.brainsuite.l_outputs:

:func:`l_outputs`
-----------------

`Link to code <http://github.com/nipy/nipype/tree/ec86b7476/nipype/interfaces/brainsuite/brainsuite.py#L1616>`__





