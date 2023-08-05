.. AUTO-GENERATED FILE -- DO NOT EDIT!

interfaces.dipy.reconstruction
==============================


.. _nipype.interfaces.dipy.reconstruction.CSD:


.. index:: CSD

CSD
---

`Link to code <http://github.com/nipy/nipype/tree/ec86b7476/nipype/interfaces/dipy/reconstruction.py#L295>`__

Uses CSD [Tournier2007]_ to generate the fODF of DWIs. The interface uses
:py:mod:`dipy`, as explained in `dipy's CSD example
<http://nipy.org/dipy/examples_built/reconst_csd.html>`_.

.. [Tournier2007] Tournier, J.D., et al. NeuroImage 2007.
  Robust determination of the fibre orientation distribution in diffusion
  MRI: Non-negativity constrained super-resolved spherical deconvolution


Example
~~~~~~~

>>> from nipype.interfaces import dipy as ndp
>>> csd = ndp.CSD()
>>> csd.inputs.in_file = '4d_dwi.nii'
>>> csd.inputs.in_bval = 'bvals'
>>> csd.inputs.in_bvec = 'bvecs'
>>> res = csd.run() # doctest: +SKIP

Inputs::

        [Mandatory]
        in_bval: (an existing file name)
                input b-values table
        in_bvec: (an existing file name)
                input b-vectors table
        in_file: (an existing file name)
                input diffusion data

        [Optional]
        b0_thres: (an integer (int or long), nipype default value: 700)
                b0 threshold
        ignore_exception: (a boolean, nipype default value: False)
                Print an error message instead of throwing an exception in case the
                interface fails to run
        in_mask: (an existing file name)
                input mask in which compute tensors
        out_fods: (a file name)
                fODFs output file name
        out_prefix: (a unicode string)
                output prefix for file names
        response: (an existing file name)
                single fiber estimated response
        save_fods: (a boolean, nipype default value: True)
                save fODFs in file
        sh_order: (an integer (int or long), nipype default value: 8)
                maximal shperical harmonics order

Outputs::

        model: (a file name)
                Python pickled object of the CSD model fitted.
        out_fods: (a file name)
                fODFs output file name

.. _nipype.interfaces.dipy.reconstruction.EstimateResponseSH:


.. index:: EstimateResponseSH

EstimateResponseSH
------------------

`Link to code <http://github.com/nipy/nipype/tree/ec86b7476/nipype/interfaces/dipy/reconstruction.py#L182>`__

Uses dipy to compute the single fiber response to be used in spherical
deconvolution methods, in a similar way to MRTrix's command
``estimate_response``.


Example
~~~~~~~

>>> from nipype.interfaces import dipy as ndp
>>> dti = ndp.EstimateResponseSH()
>>> dti.inputs.in_file = '4d_dwi.nii'
>>> dti.inputs.in_bval = 'bvals'
>>> dti.inputs.in_bvec = 'bvecs'
>>> dti.inputs.in_evals = 'dwi_evals.nii'
>>> res = dti.run() # doctest: +SKIP

Inputs::

        [Mandatory]
        in_bval: (an existing file name)
                input b-values table
        in_bvec: (an existing file name)
                input b-vectors table
        in_evals: (an existing file name)
                input eigenvalues file
        in_file: (an existing file name)
                input diffusion data

        [Optional]
        auto: (a boolean)
                use the auto_response estimator from dipy
                mutually_exclusive: recursive
        b0_thres: (an integer (int or long), nipype default value: 700)
                b0 threshold
        fa_thresh: (a float, nipype default value: 0.7)
                FA threshold
        ignore_exception: (a boolean, nipype default value: False)
                Print an error message instead of throwing an exception in case the
                interface fails to run
        in_mask: (an existing file name)
                input mask in which we find single fibers
        out_mask: (a file name, nipype default value: wm_mask.nii.gz)
                computed wm mask
        out_prefix: (a unicode string)
                output prefix for file names
        recursive: (a boolean)
                use the recursive response estimator from dipy
                mutually_exclusive: auto
        response: (a file name, nipype default value: response.txt)
                the output response file
        roi_radius: (an integer (int or long), nipype default value: 10)
                ROI radius to be used in auto_response

Outputs::

        out_mask: (an existing file name)
                output wm mask
        response: (an existing file name)
                the response file

.. _nipype.interfaces.dipy.reconstruction.RESTORE:


.. index:: RESTORE

RESTORE
-------

`Link to code <http://github.com/nipy/nipype/tree/ec86b7476/nipype/interfaces/dipy/reconstruction.py#L43>`__

Uses RESTORE [Chang2005]_ to perform DTI fitting with outlier detection.
The interface uses :py:mod:`dipy`, as explained in `dipy's documentation`_.

.. [Chang2005] Chang, LC, Jones, DK and Pierpaoli, C. RESTORE: robust     estimation of tensors by outlier rejection. MRM, 53:1088-95, (2005).

.. _dipy's documentation:     http://nipy.org/dipy/examples_built/restore_dti.html


Example
~~~~~~~

>>> from nipype.interfaces import dipy as ndp
>>> dti = ndp.RESTORE()
>>> dti.inputs.in_file = '4d_dwi.nii'
>>> dti.inputs.in_bval = 'bvals'
>>> dti.inputs.in_bvec = 'bvecs'
>>> res = dti.run() # doctest: +SKIP

Inputs::

        [Mandatory]
        in_bval: (an existing file name)
                input b-values table
        in_bvec: (an existing file name)
                input b-vectors table
        in_file: (an existing file name)
                input diffusion data

        [Optional]
        b0_thres: (an integer (int or long), nipype default value: 700)
                b0 threshold
        ignore_exception: (a boolean, nipype default value: False)
                Print an error message instead of throwing an exception in case the
                interface fails to run
        in_mask: (an existing file name)
                input mask in which compute tensors
        noise_mask: (an existing file name)
                input mask in which compute noise variance
        out_prefix: (a unicode string)
                output prefix for file names

Outputs::

        evals: (a file name)
                output the eigenvalues of the fitted DTI
        evecs: (a file name)
                output the eigenvectors of the fitted DTI
        fa: (a file name)
                output fractional anisotropy (FA) map computed from the fitted DTI
        md: (a file name)
                output mean diffusivity (MD) map computed from the fitted DTI
        mode: (a file name)
                output mode (MO) map computed from the fitted DTI
        rd: (a file name)
                output radial diffusivity (RD) map computed from the fitted DTI
        trace: (a file name)
                output the tensor trace map computed from the fitted DTI
