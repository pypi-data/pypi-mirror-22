.. AUTO-GENERATED FILE -- DO NOT EDIT!

workflows.smri.freesurfer.autorecon1
====================================


.. module:: nipype.workflows.smri.freesurfer.autorecon1


.. _nipype.workflows.smri.freesurfer.autorecon1.checkT1s:

:func:`checkT1s`
----------------

`Link to code <http://github.com/nipy/nipype/tree/ec86b7476/nipype/workflows/smri/freesurfer/autorecon1.py#L10>`__



Verifying size of inputs and setting workflow parameters


.. _nipype.workflows.smri.freesurfer.autorecon1.create_AutoRecon1:

:func:`create_AutoRecon1`
-------------------------

`Link to code <http://github.com/nipy/nipype/tree/ec86b7476/nipype/workflows/smri/freesurfer/autorecon1.py#L38>`__



Creates the AutoRecon1 workflow in nipype.

Inputs::
       inputspec.T1_files : T1 files (mandatory)
       inputspec.T2_file : T2 file (optional)
       inputspec.FLAIR_file : FLAIR file (optional)
       inputspec.cw256 : Conform inputs to 256 FOV (optional)
       inputspec.num_threads: Number of threads to use with EM Register (default=1)
Outpus::

