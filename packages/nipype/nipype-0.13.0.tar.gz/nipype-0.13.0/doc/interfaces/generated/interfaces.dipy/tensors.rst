.. AUTO-GENERATED FILE -- DO NOT EDIT!

interfaces.dipy.tensors
=======================


.. _nipype.interfaces.dipy.tensors.DTI:


.. index:: DTI

DTI
---

`Link to code <http://github.com/nipy/nipype/tree/ec86b7476/nipype/interfaces/dipy/tensors.py#L32>`__

Calculates the diffusion tensor model parameters

Example
~~~~~~~

>>> import nipype.interfaces.dipy as dipy
>>> dti = dipy.DTI()
>>> dti.inputs.in_file = 'diffusion.nii'
>>> dti.inputs.in_bvec = 'bvecs'
>>> dti.inputs.in_bval = 'bvals'
>>> dti.run()                                   # doctest: +SKIP

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
        mask_file: (an existing file name)
                An optional white matter mask
        out_prefix: (a unicode string)
                output prefix for file names

Outputs::

        ad_file: (an existing file name)
        fa_file: (an existing file name)
        md_file: (an existing file name)
        out_file: (an existing file name)
        rd_file: (an existing file name)

.. _nipype.interfaces.dipy.tensors.TensorMode:


.. index:: TensorMode

TensorMode
----------

`Link to code <http://github.com/nipy/nipype/tree/ec86b7476/nipype/interfaces/dipy/tensors.py#L98>`__

Creates a map of the mode of the diffusion tensors given a set of
diffusion-weighted images, as well as their associated b-values and
b-vectors. Fits the diffusion tensors and calculates tensor mode
with Dipy.

.. [1] Daniel B. Ennis and G. Kindlmann, "Orthogonal Tensor
    Invariants and the Analysis of Diffusion Tensor Magnetic Resonance
    Images", Magnetic Resonance in Medicine, vol. 55, no. 1, pp. 136-146,
    2006.

Example
~~~~~~~

>>> import nipype.interfaces.dipy as dipy
>>> mode = dipy.TensorMode()
>>> mode.inputs.in_file = 'diffusion.nii'
>>> mode.inputs.in_bvec = 'bvecs'
>>> mode.inputs.in_bval = 'bvals'
>>> mode.run()                                   # doctest: +SKIP

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
        mask_file: (an existing file name)
                An optional white matter mask
        out_prefix: (a unicode string)
                output prefix for file names

Outputs::

        out_file: (an existing file name)
