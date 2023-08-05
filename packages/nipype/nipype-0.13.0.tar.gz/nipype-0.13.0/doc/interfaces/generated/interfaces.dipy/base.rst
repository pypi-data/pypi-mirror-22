.. AUTO-GENERATED FILE -- DO NOT EDIT!

interfaces.dipy.base
====================


.. _nipype.interfaces.dipy.base.DipyBaseInterface:


.. index:: DipyBaseInterface

DipyBaseInterface
-----------------

`Link to code <http://github.com/nipy/nipype/tree/ec86b7476/nipype/interfaces/dipy/base.py#L34>`__

A base interface for py:mod:`dipy` computations

Inputs::

        [Mandatory]

        [Optional]
        ignore_exception: (a boolean, nipype default value: False)
                Print an error message instead of throwing an exception in case the
                interface fails to run

Outputs::

        None

.. _nipype.interfaces.dipy.base.DipyDiffusionInterface:


.. index:: DipyDiffusionInterface

DipyDiffusionInterface
----------------------

`Link to code <http://github.com/nipy/nipype/tree/ec86b7476/nipype/interfaces/dipy/base.py#L54>`__

A base interface for py:mod:`dipy` computations

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
        out_prefix: (a unicode string)
                output prefix for file names

Outputs::

        None
