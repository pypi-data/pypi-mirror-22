.. AUTO-GENERATED FILE -- DO NOT EDIT!

algorithms.confounds
====================


.. _nipype.algorithms.confounds.ACompCor:


.. index:: ACompCor

ACompCor
--------

`Link to code <http://github.com/nipy/nipype/tree/ec86b7476/nipype/algorithms/confounds.py#L432>`__

Anatomical compcor: for inputs and outputs, see CompCor.
When the mask provided is an anatomical mask, then CompCor
is equivalent to ACompCor.

Inputs::

        [Mandatory]
        realigned_file: (an existing file name)
                already realigned brain image (4D)

        [Optional]
        components_file: (a unicode string, nipype default value:
                 components_file.txt)
                Filename to store physiological components
        header_prefix: (a unicode string)
                the desired header for the output tsv file (one column). If
                undefined, will default to "CompCor"
        ignore_exception: (a boolean, nipype default value: False)
                Print an error message instead of throwing an exception in case the
                interface fails to run
        mask_files: (a list of items which are an existing file name)
                One or more mask files that determines ROI (3D). When more that one
                file is provided `merge_method` or `merge_index` must be provided
        mask_index: (a long integer >= 0)
                Position of mask in `mask_files` to use - first is the default.
                mutually_exclusive: merge_method
                requires: mask_files
        merge_method: ('union' or 'intersect' or 'none')
                Merge method if multiple masks are present - `union` uses voxels
                included in at least one input mask, `intersect` uses only voxels
                present in all input masks, `none` performs CompCor on each mask
                individually
                mutually_exclusive: mask_index
                requires: mask_files
        num_components: (an integer (int or long), nipype default value: 6)
        regress_poly_degree: (a long integer >= 1, nipype default value: 1)
                the degree polynomial to use
        use_regress_poly: (a boolean, nipype default value: True)
                use polynomial regression pre-component extraction

Outputs::

        components_file: (an existing file name)
                text file containing the noise components

References::
None

.. _nipype.algorithms.confounds.CompCor:


.. index:: CompCor

CompCor
-------

`Link to code <http://github.com/nipy/nipype/tree/ec86b7476/nipype/algorithms/confounds.py#L343>`__

Interface with core CompCor computation, used in aCompCor and tCompCor

Example
~~~~~~~

>>> ccinterface = CompCor()
>>> ccinterface.inputs.realigned_file = 'functional.nii'
>>> ccinterface.inputs.mask_files = 'mask.nii'
>>> ccinterface.inputs.num_components = 1
>>> ccinterface.inputs.use_regress_poly = True
>>> ccinterface.inputs.regress_poly_degree = 2

Inputs::

        [Mandatory]
        realigned_file: (an existing file name)
                already realigned brain image (4D)

        [Optional]
        components_file: (a unicode string, nipype default value:
                 components_file.txt)
                Filename to store physiological components
        header_prefix: (a unicode string)
                the desired header for the output tsv file (one column). If
                undefined, will default to "CompCor"
        ignore_exception: (a boolean, nipype default value: False)
                Print an error message instead of throwing an exception in case the
                interface fails to run
        mask_files: (a list of items which are an existing file name)
                One or more mask files that determines ROI (3D). When more that one
                file is provided `merge_method` or `merge_index` must be provided
        mask_index: (a long integer >= 0)
                Position of mask in `mask_files` to use - first is the default.
                mutually_exclusive: merge_method
                requires: mask_files
        merge_method: ('union' or 'intersect' or 'none')
                Merge method if multiple masks are present - `union` uses voxels
                included in at least one input mask, `intersect` uses only voxels
                present in all input masks, `none` performs CompCor on each mask
                individually
                mutually_exclusive: mask_index
                requires: mask_files
        num_components: (an integer (int or long), nipype default value: 6)
        regress_poly_degree: (a long integer >= 1, nipype default value: 1)
                the degree polynomial to use
        use_regress_poly: (a boolean, nipype default value: True)
                use polynomial regression pre-component extraction

Outputs::

        components_file: (an existing file name)
                text file containing the noise components

References::
None

.. _nipype.algorithms.confounds.ComputeDVARS:


.. index:: ComputeDVARS

ComputeDVARS
------------

`Link to code <http://github.com/nipy/nipype/tree/ec86b7476/nipype/algorithms/confounds.py#L82>`__

Computes the DVARS.

Inputs::

        [Mandatory]
        in_file: (an existing file name)
                functional data, after HMC
        in_mask: (an existing file name)
                a brain mask

        [Optional]
        figdpi: (an integer (int or long), nipype default value: 100)
                output dpi for the plot
        figformat: ('png' or 'pdf' or 'svg', nipype default value: png)
                output format for figures
        figsize: (a tuple of the form: (a float, a float), nipype default
                 value: (11.7, 2.3))
                output figure size
        ignore_exception: (a boolean, nipype default value: False)
                Print an error message instead of throwing an exception in case the
                interface fails to run
        intensity_normalization: (a float, nipype default value: 1000.0)
                Divide value in each voxel at each timepoint by the median
                calculated across all voxelsand timepoints within the mask (if
                specified)and then multiply by the value specified bythis parameter.
                By using the default (1000)output DVARS will be expressed in x10 %
                BOLD units compatible with Power et al.2012. Set this to 0 to
                disable intensitynormalization altogether.
        remove_zerovariance: (a boolean, nipype default value: True)
                remove voxels with zero variance
        save_all: (a boolean, nipype default value: False)
                output all DVARS
        save_nstd: (a boolean, nipype default value: False)
                save non-standardized DVARS
        save_plot: (a boolean, nipype default value: False)
                write DVARS plot
        save_std: (a boolean, nipype default value: True)
                save standardized DVARS
        save_vxstd: (a boolean, nipype default value: False)
                save voxel-wise standardized DVARS
        series_tr: (a float)
                repetition time in sec.

Outputs::

        avg_nstd: (a float)
        avg_std: (a float)
        avg_vxstd: (a float)
        fig_nstd: (an existing file name)
                output DVARS plot
        fig_std: (an existing file name)
                output DVARS plot
        fig_vxstd: (an existing file name)
                output DVARS plot
        out_all: (an existing file name)
                output text file
        out_nstd: (an existing file name)
                output text file
        out_std: (an existing file name)
                output text file
        out_vxstd: (an existing file name)
                output text file

References::
None
None

.. _nipype.algorithms.confounds.FramewiseDisplacement:


.. index:: FramewiseDisplacement

FramewiseDisplacement
---------------------

`Link to code <http://github.com/nipy/nipype/tree/ec86b7476/nipype/algorithms/confounds.py#L233>`__

Calculate the :abbr:`FD (framewise displacement)` as in [Power2012]_.
This implementation reproduces the calculation in fsl_motion_outliers

.. [Power2012] Power et al., Spurious but systematic correlations in functional
     connectivity MRI networks arise from subject motion, NeuroImage 59(3),
     2012. doi:`10.1016/j.neuroimage.2011.10.018
     <http://dx.doi.org/10.1016/j.neuroimage.2011.10.018>`_.

Inputs::

        [Mandatory]
        in_file: (an existing file name)
                motion parameters
        parameter_source: ('FSL' or 'AFNI' or 'SPM' or 'FSFAST' or 'NIPY')
                Source of movement parameters

        [Optional]
        figdpi: (an integer (int or long), nipype default value: 100)
                output dpi for the FD plot
        figsize: (a tuple of the form: (a float, a float), nipype default
                 value: (11.7, 2.3))
                output figure size
        ignore_exception: (a boolean, nipype default value: False)
                Print an error message instead of throwing an exception in case the
                interface fails to run
        normalize: (a boolean, nipype default value: False)
                calculate FD in mm/s
        out_figure: (a file name, nipype default value: fd_power_2012.pdf)
                output figure name
        out_file: (a file name, nipype default value: fd_power_2012.txt)
                output file name
        radius: (a float, nipype default value: 50)
                radius in mm to calculate angular FDs, 50mm is the default since it
                is used in Power et al. 2012
        save_plot: (a boolean, nipype default value: False)
                write FD plot
        series_tr: (a float)
                repetition time in sec.

Outputs::

        fd_average: (a float)
                average FD
        out_figure: (a file name)
                output image file
        out_file: (a file name)
                calculated FD per timestep

References::
None

.. _nipype.algorithms.confounds.NonSteadyStateDetector:


.. index:: NonSteadyStateDetector

NonSteadyStateDetector
----------------------

`Link to code <http://github.com/nipy/nipype/tree/ec86b7476/nipype/algorithms/confounds.py#L607>`__

Returns the number of non-steady state volumes detected at the beginning
of the scan.

Inputs::

        [Mandatory]
        in_file: (an existing file name)
                4D NIFTI EPI file

        [Optional]
        ignore_exception: (a boolean, nipype default value: False)
                Print an error message instead of throwing an exception in case the
                interface fails to run

Outputs::

        n_volumes_to_discard: (an integer (int or long))
                Number of non-steady state volumesdetected in the beginning of the
                scan.

.. _nipype.algorithms.confounds.TCompCor:


.. index:: TCompCor

TCompCor
--------

`Link to code <http://github.com/nipy/nipype/tree/ec86b7476/nipype/algorithms/confounds.py#L465>`__

Interface for tCompCor. Computes a ROI mask based on variance of voxels.

Example
~~~~~~~

>>> ccinterface = TCompCor()
>>> ccinterface.inputs.realigned_file = 'functional.nii'
>>> ccinterface.inputs.mask_files = 'mask.nii'
>>> ccinterface.inputs.num_components = 1
>>> ccinterface.inputs.use_regress_poly = True
>>> ccinterface.inputs.regress_poly_degree = 2
>>> ccinterface.inputs.percentile_threshold = .03

Inputs::

        [Mandatory]
        realigned_file: (an existing file name)
                already realigned brain image (4D)

        [Optional]
        components_file: (a unicode string, nipype default value:
                 components_file.txt)
                Filename to store physiological components
        header_prefix: (a unicode string)
                the desired header for the output tsv file (one column). If
                undefined, will default to "CompCor"
        ignore_exception: (a boolean, nipype default value: False)
                Print an error message instead of throwing an exception in case the
                interface fails to run
        mask_files: (a list of items which are an existing file name)
                One or more mask files that determines ROI (3D). When more that one
                file is provided `merge_method` or `merge_index` must be provided
        mask_index: (a long integer >= 0)
                Position of mask in `mask_files` to use - first is the default.
                mutually_exclusive: merge_method
                requires: mask_files
        merge_method: ('union' or 'intersect' or 'none')
                Merge method if multiple masks are present - `union` uses voxels
                included in at least one input mask, `intersect` uses only voxels
                present in all input masks, `none` performs CompCor on each mask
                individually
                mutually_exclusive: mask_index
                requires: mask_files
        num_components: (an integer (int or long), nipype default value: 6)
        percentile_threshold: (0.0 < a floating point number < 1.0, nipype
                 default value: 0.02)
                the percentile used to select highest-variance voxels, represented
                by a number between 0 and 1, exclusive. By default, this value is
                set to .02. That is, the 2% of voxels with the highest variance are
                used.
        regress_poly_degree: (a long integer >= 1, nipype default value: 1)
                the degree polynomial to use
        use_regress_poly: (a boolean, nipype default value: True)
                use polynomial regression pre-component extraction

Outputs::

        components_file: (an existing file name)
                text file containing the noise components
        high_variance_masks: (a list of items which are an existing file
                 name)
                voxels exceeding the variance threshold

References::
None

.. _nipype.algorithms.confounds.TSNR:


.. index:: TSNR

TSNR
----

`Link to code <http://github.com/nipy/nipype/tree/ec86b7476/nipype/algorithms/confounds.py#L542>`__

Computes the time-course SNR for a time series

Typically you want to run this on a realigned time-series.

Example
~~~~~~~

>>> tsnr = TSNR()
>>> tsnr.inputs.in_file = 'functional.nii'
>>> res = tsnr.run() # doctest: +SKIP

Inputs::

        [Mandatory]
        in_file: (a list of items which are an existing file name)
                realigned 4D file or a list of 3D files

        [Optional]
        detrended_file: (a file name, nipype default value: detrend.nii.gz)
                input file after detrending
        ignore_exception: (a boolean, nipype default value: False)
                Print an error message instead of throwing an exception in case the
                interface fails to run
        mean_file: (a file name, nipype default value: mean.nii.gz)
                output mean file
        regress_poly: (a long integer >= 1)
                Remove polynomials
        stddev_file: (a file name, nipype default value: stdev.nii.gz)
                output tSNR file
        tsnr_file: (a file name, nipype default value: tsnr.nii.gz)
                output tSNR file

Outputs::

        detrended_file: (a file name)
                detrended input file
        mean_file: (an existing file name)
                mean image file
        stddev_file: (an existing file name)
                std dev image file
        tsnr_file: (an existing file name)
                tsnr image file

.. module:: nipype.algorithms.confounds


.. _nipype.algorithms.confounds.combine_mask_files:

:func:`combine_mask_files`
--------------------------

`Link to code <http://github.com/nipy/nipype/tree/ec86b7476/nipype/algorithms/confounds.py#L834>`__



Combines input mask files into a single nibabel image

A helper function for CompCor

mask_files: a list
    one or more binary mask files
mask_method: enum ('union', 'intersect', 'none')
    determines how to combine masks
mask_index: an integer
    determines which file to return (mutually exclusive with mask_method)

returns: a list of nibabel images


.. _nipype.algorithms.confounds.compute_dvars:

:func:`compute_dvars`
---------------------

`Link to code <http://github.com/nipy/nipype/tree/ec86b7476/nipype/algorithms/confounds.py#L630>`__



Compute the :abbr:`DVARS (D referring to temporal
derivative of timecourses, VARS referring to RMS variance over voxels)`
[Power2012]_.

Particularly, the *standardized* :abbr:`DVARS (D referring to temporal
derivative of timecourses, VARS referring to RMS variance over voxels)`
[Nichols2013]_ are computed.

.. [Nichols2013] Nichols T, `Notes on creating a standardized version of
     DVARS <http://www2.warwick.ac.uk/fac/sci/statistics/staff/academic-research/nichols/scripts/fsl/standardizeddvars.pdf>`_, 2013.

.. note:: Implementation details

  Uses the implementation of the `Yule-Walker equations
  from nitime
  <http://nipy.org/nitime/api/generated/nitime.algorithms.autoregressive.html#nitime.algorithms.autoregressive.AR_est_YW>`_
  for the :abbr:`AR (auto-regressive)` filtering of the fMRI signal.

:param numpy.ndarray func: functional data, after head-motion-correction.
:param numpy.ndarray mask: a 3D mask of the brain
:param bool output_all: write out all dvars
:param str out_file: a path to which the standardized dvars should be saved.
:return: the standardized DVARS


.. _nipype.algorithms.confounds.compute_noise_components:

:func:`compute_noise_components`
--------------------------------

`Link to code <http://github.com/nipy/nipype/tree/ec86b7476/nipype/algorithms/confounds.py#L889>`__



Compute the noise components from the imgseries for each mask

imgseries: a nibabel img
mask_images: a list of nibabel images
degree: order of polynomial used to remove trends from the timeseries
num_components: number of noise components to return

returns:

components: a numpy array


.. _nipype.algorithms.confounds.is_outlier:

:func:`is_outlier`
------------------

`Link to code <http://github.com/nipy/nipype/tree/ec86b7476/nipype/algorithms/confounds.py#L759>`__



Returns a boolean array with True if points are outliers and False
otherwise.

:param nparray points: an numobservations by numdimensions numpy array of observations
:param float thresh: the modified z-score to use as a threshold. Observations with
    a modified z-score (based on the median absolute deviation) greater
    than this value will be classified as outliers.

:return: A bolean mask, of size numobservations-length array.

.. note:: References

    Boris Iglewicz and David Hoaglin (1993), "Volume 16: How to Detect and
    Handle Outliers", The ASQC Basic References in Quality Control:
    Statistical Techniques, Edward F. Mykytka, Ph.D., Editor.


.. _nipype.algorithms.confounds.plot_confound:

:func:`plot_confound`
---------------------

`Link to code <http://github.com/nipy/nipype/tree/ec86b7476/nipype/algorithms/confounds.py#L716>`__



A helper function to plot :abbr:`fMRI (functional MRI)` confounds.


.. _nipype.algorithms.confounds.regress_poly:

:func:`regress_poly`
--------------------

`Link to code <http://github.com/nipy/nipype/tree/ec86b7476/nipype/algorithms/confounds.py#L797>`__



Returns data with degree polynomial regressed out.

:param bool remove_mean: whether or not demean data (i.e. degree 0),
:param int axis: numpy array axes along which regression is performed

