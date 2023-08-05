.. AUTO-GENERATED FILE -- DO NOT EDIT!

workflows.smri.niftyreg.groupwise
=================================


.. module:: nipype.workflows.smri.niftyreg.groupwise


.. _nipype.workflows.smri.niftyreg.groupwise.create_groupwise_average:

:func:`create_groupwise_average`
--------------------------------

`Link to code <http://github.com/nipy/nipype/tree/ec86b7476/nipype/workflows/smri/niftyreg/groupwise.py#L237>`__



Create the overall workflow that embeds all the rigid, affine and
non-linear components.

Inputs::

    inputspec.in_files - The input files to be registered
    inputspec.ref_file - The initial reference image that the input files
                          are registered to
    inputspec.rmask_file - Mask of the reference image
    inputspec.in_trans_files - Initial transformation files (affine or
                                cpps)

Outputs::

    outputspec.average_image - The average image
    outputspec.cpp_files - The bspline transformation files


Example
~~~~~~~

>>> from nipype.workflows.smri.niftyreg import create_groupwise_average
>>> node = create_groupwise_average('groupwise_av')  # doctest: +SKIP
>>> node.inputs.inputspec.in_files = [
...     'file1.nii.gz', 'file2.nii.gz']  # doctest: +SKIP
>>> node.inputs.inputspec.ref_file = ['ref.nii.gz']  # doctest: +SKIP
>>> node.inputs.inputspec.rmask_file = ['mask.nii.gz']  # doctest: +SKIP
>>> node.run()  # doctest: +SKIP


Graph
~~~~~

.. graphviz::

	digraph atlas_creation{

	  label="atlas_creation";

	  atlas_creation_inputspec[label="inputspec (utility)"];

	  atlas_creation_outputspec[label="outputspec (utility)"];

	  subgraph cluster_atlas_creation_lin_reg0 {

	      label="lin_reg0";

	    atlas_creation_lin_reg0_inputspec[label="inputspec (utility)"];

	    atlas_creation_lin_reg0_lin_reg[label="lin_reg (niftyreg)"];

	    atlas_creation_lin_reg0_ave_ims[label="ave_ims (niftyreg)"];

	    atlas_creation_lin_reg0_outputspec[label="outputspec (utility)"];

	    atlas_creation_lin_reg0_inputspec -> atlas_creation_lin_reg0_lin_reg;

	    atlas_creation_lin_reg0_inputspec -> atlas_creation_lin_reg0_lin_reg;

	    atlas_creation_lin_reg0_lin_reg -> atlas_creation_lin_reg0_ave_ims;

	    atlas_creation_lin_reg0_lin_reg -> atlas_creation_lin_reg0_outputspec;

	    atlas_creation_lin_reg0_ave_ims -> atlas_creation_lin_reg0_outputspec;

	  }

	  subgraph cluster_atlas_creation_lin_reg1 {

	      label="lin_reg1";

	    atlas_creation_lin_reg1_inputspec[label="inputspec (utility)"];

	    atlas_creation_lin_reg1_lin_reg[label="lin_reg (niftyreg)"];

	    atlas_creation_lin_reg1_ave_ims[label="ave_ims (niftyreg)"];

	    atlas_creation_lin_reg1_outputspec[label="outputspec (utility)"];

	    atlas_creation_lin_reg1_inputspec -> atlas_creation_lin_reg1_lin_reg;

	    atlas_creation_lin_reg1_inputspec -> atlas_creation_lin_reg1_lin_reg;

	    atlas_creation_lin_reg1_lin_reg -> atlas_creation_lin_reg1_ave_ims;

	    atlas_creation_lin_reg1_lin_reg -> atlas_creation_lin_reg1_outputspec;

	    atlas_creation_lin_reg1_ave_ims -> atlas_creation_lin_reg1_outputspec;

	  }

	  subgraph cluster_atlas_creation_lin_reg2 {

	      label="lin_reg2";

	    atlas_creation_lin_reg2_inputspec[label="inputspec (utility)"];

	    atlas_creation_lin_reg2_lin_reg[label="lin_reg (niftyreg)"];

	    atlas_creation_lin_reg2_ave_ims[label="ave_ims (niftyreg)"];

	    atlas_creation_lin_reg2_outputspec[label="outputspec (utility)"];

	    atlas_creation_lin_reg2_inputspec -> atlas_creation_lin_reg2_lin_reg;

	    atlas_creation_lin_reg2_inputspec -> atlas_creation_lin_reg2_lin_reg;

	    atlas_creation_lin_reg2_lin_reg -> atlas_creation_lin_reg2_ave_ims;

	    atlas_creation_lin_reg2_lin_reg -> atlas_creation_lin_reg2_outputspec;

	    atlas_creation_lin_reg2_ave_ims -> atlas_creation_lin_reg2_outputspec;

	  }

	  subgraph cluster_atlas_creation_lin_reg3 {

	      label="lin_reg3";

	    atlas_creation_lin_reg3_inputspec[label="inputspec (utility)"];

	    atlas_creation_lin_reg3_lin_reg[label="lin_reg (niftyreg)"];

	    atlas_creation_lin_reg3_ave_ims[label="ave_ims (niftyreg)"];

	    atlas_creation_lin_reg3_outputspec[label="outputspec (utility)"];

	    atlas_creation_lin_reg3_inputspec -> atlas_creation_lin_reg3_lin_reg;

	    atlas_creation_lin_reg3_inputspec -> atlas_creation_lin_reg3_lin_reg;

	    atlas_creation_lin_reg3_inputspec -> atlas_creation_lin_reg3_ave_ims;

	    atlas_creation_lin_reg3_lin_reg -> atlas_creation_lin_reg3_ave_ims;

	    atlas_creation_lin_reg3_lin_reg -> atlas_creation_lin_reg3_outputspec;

	    atlas_creation_lin_reg3_ave_ims -> atlas_creation_lin_reg3_outputspec;

	  }

	  subgraph cluster_atlas_creation_lin_reg4 {

	      label="lin_reg4";

	    atlas_creation_lin_reg4_inputspec[label="inputspec (utility)"];

	    atlas_creation_lin_reg4_lin_reg[label="lin_reg (niftyreg)"];

	    atlas_creation_lin_reg4_ave_ims[label="ave_ims (niftyreg)"];

	    atlas_creation_lin_reg4_outputspec[label="outputspec (utility)"];

	    atlas_creation_lin_reg4_inputspec -> atlas_creation_lin_reg4_lin_reg;

	    atlas_creation_lin_reg4_inputspec -> atlas_creation_lin_reg4_lin_reg;

	    atlas_creation_lin_reg4_inputspec -> atlas_creation_lin_reg4_ave_ims;

	    atlas_creation_lin_reg4_lin_reg -> atlas_creation_lin_reg4_ave_ims;

	    atlas_creation_lin_reg4_lin_reg -> atlas_creation_lin_reg4_outputspec;

	    atlas_creation_lin_reg4_ave_ims -> atlas_creation_lin_reg4_outputspec;

	  }

	  subgraph cluster_atlas_creation_lin_reg5 {

	      label="lin_reg5";

	    atlas_creation_lin_reg5_inputspec[label="inputspec (utility)"];

	    atlas_creation_lin_reg5_lin_reg[label="lin_reg (niftyreg)"];

	    atlas_creation_lin_reg5_ave_ims[label="ave_ims (niftyreg)"];

	    atlas_creation_lin_reg5_outputspec[label="outputspec (utility)"];

	    atlas_creation_lin_reg5_inputspec -> atlas_creation_lin_reg5_lin_reg;

	    atlas_creation_lin_reg5_inputspec -> atlas_creation_lin_reg5_lin_reg;

	    atlas_creation_lin_reg5_lin_reg -> atlas_creation_lin_reg5_ave_ims;

	    atlas_creation_lin_reg5_lin_reg -> atlas_creation_lin_reg5_outputspec;

	    atlas_creation_lin_reg5_ave_ims -> atlas_creation_lin_reg5_outputspec;

	  }

	  subgraph cluster_atlas_creation_nonlin0 {

	      label="nonlin0";

	    atlas_creation_nonlin0_inputspec[label="inputspec (utility)"];

	    atlas_creation_nonlin0_nonlin_reg[label="nonlin_reg (niftyreg)"];

	    atlas_creation_nonlin0_ave_ims[label="ave_ims (niftyreg)"];

	    atlas_creation_nonlin0_outputspec[label="outputspec (utility)"];

	    atlas_creation_nonlin0_inputspec -> atlas_creation_nonlin0_nonlin_reg;

	    atlas_creation_nonlin0_inputspec -> atlas_creation_nonlin0_nonlin_reg;

	    atlas_creation_nonlin0_inputspec -> atlas_creation_nonlin0_nonlin_reg;

	    atlas_creation_nonlin0_inputspec -> atlas_creation_nonlin0_ave_ims;

	    atlas_creation_nonlin0_nonlin_reg -> atlas_creation_nonlin0_ave_ims;

	    atlas_creation_nonlin0_nonlin_reg -> atlas_creation_nonlin0_outputspec;

	    atlas_creation_nonlin0_ave_ims -> atlas_creation_nonlin0_outputspec;

	  }

	  subgraph cluster_atlas_creation_nonlin1 {

	      label="nonlin1";

	    atlas_creation_nonlin1_inputspec[label="inputspec (utility)"];

	    atlas_creation_nonlin1_nonlin_reg[label="nonlin_reg (niftyreg)"];

	    atlas_creation_nonlin1_ave_ims[label="ave_ims (niftyreg)"];

	    atlas_creation_nonlin1_outputspec[label="outputspec (utility)"];

	    atlas_creation_nonlin1_inputspec -> atlas_creation_nonlin1_nonlin_reg;

	    atlas_creation_nonlin1_inputspec -> atlas_creation_nonlin1_nonlin_reg;

	    atlas_creation_nonlin1_inputspec -> atlas_creation_nonlin1_nonlin_reg;

	    atlas_creation_nonlin1_inputspec -> atlas_creation_nonlin1_ave_ims;

	    atlas_creation_nonlin1_nonlin_reg -> atlas_creation_nonlin1_ave_ims;

	    atlas_creation_nonlin1_nonlin_reg -> atlas_creation_nonlin1_outputspec;

	    atlas_creation_nonlin1_ave_ims -> atlas_creation_nonlin1_outputspec;

	  }

	  subgraph cluster_atlas_creation_nonlin2 {

	      label="nonlin2";

	    atlas_creation_nonlin2_inputspec[label="inputspec (utility)"];

	    atlas_creation_nonlin2_nonlin_reg[label="nonlin_reg (niftyreg)"];

	    atlas_creation_nonlin2_ave_ims[label="ave_ims (niftyreg)"];

	    atlas_creation_nonlin2_outputspec[label="outputspec (utility)"];

	    atlas_creation_nonlin2_inputspec -> atlas_creation_nonlin2_nonlin_reg;

	    atlas_creation_nonlin2_inputspec -> atlas_creation_nonlin2_nonlin_reg;

	    atlas_creation_nonlin2_inputspec -> atlas_creation_nonlin2_nonlin_reg;

	    atlas_creation_nonlin2_inputspec -> atlas_creation_nonlin2_ave_ims;

	    atlas_creation_nonlin2_nonlin_reg -> atlas_creation_nonlin2_ave_ims;

	    atlas_creation_nonlin2_nonlin_reg -> atlas_creation_nonlin2_outputspec;

	    atlas_creation_nonlin2_ave_ims -> atlas_creation_nonlin2_outputspec;

	  }

	  subgraph cluster_atlas_creation_nonlin3 {

	      label="nonlin3";

	    atlas_creation_nonlin3_inputspec[label="inputspec (utility)"];

	    atlas_creation_nonlin3_nonlin_reg[label="nonlin_reg (niftyreg)"];

	    atlas_creation_nonlin3_ave_ims[label="ave_ims (niftyreg)"];

	    atlas_creation_nonlin3_outputspec[label="outputspec (utility)"];

	    atlas_creation_nonlin3_inputspec -> atlas_creation_nonlin3_nonlin_reg;

	    atlas_creation_nonlin3_inputspec -> atlas_creation_nonlin3_nonlin_reg;

	    atlas_creation_nonlin3_inputspec -> atlas_creation_nonlin3_nonlin_reg;

	    atlas_creation_nonlin3_inputspec -> atlas_creation_nonlin3_ave_ims;

	    atlas_creation_nonlin3_nonlin_reg -> atlas_creation_nonlin3_ave_ims;

	    atlas_creation_nonlin3_nonlin_reg -> atlas_creation_nonlin3_outputspec;

	    atlas_creation_nonlin3_ave_ims -> atlas_creation_nonlin3_outputspec;

	  }

	  subgraph cluster_atlas_creation_nonlin4 {

	      label="nonlin4";

	    atlas_creation_nonlin4_inputspec[label="inputspec (utility)"];

	    atlas_creation_nonlin4_nonlin_reg[label="nonlin_reg (niftyreg)"];

	    atlas_creation_nonlin4_ave_ims[label="ave_ims (niftyreg)"];

	    atlas_creation_nonlin4_outputspec[label="outputspec (utility)"];

	    atlas_creation_nonlin4_inputspec -> atlas_creation_nonlin4_nonlin_reg;

	    atlas_creation_nonlin4_inputspec -> atlas_creation_nonlin4_nonlin_reg;

	    atlas_creation_nonlin4_inputspec -> atlas_creation_nonlin4_nonlin_reg;

	    atlas_creation_nonlin4_nonlin_reg -> atlas_creation_nonlin4_ave_ims;

	    atlas_creation_nonlin4_nonlin_reg -> atlas_creation_nonlin4_outputspec;

	    atlas_creation_nonlin4_ave_ims -> atlas_creation_nonlin4_outputspec;

	  }

	  atlas_creation_inputspec -> atlas_creation_lin_reg0_inputspec;

	  atlas_creation_inputspec -> atlas_creation_lin_reg0_inputspec;

	  atlas_creation_inputspec -> atlas_creation_lin_reg1_inputspec;

	  atlas_creation_inputspec -> atlas_creation_lin_reg2_inputspec;

	  atlas_creation_inputspec -> atlas_creation_lin_reg3_inputspec;

	  atlas_creation_inputspec -> atlas_creation_lin_reg4_inputspec;

	  atlas_creation_inputspec -> atlas_creation_lin_reg5_inputspec;

	  atlas_creation_inputspec -> atlas_creation_nonlin0_inputspec;

	  atlas_creation_inputspec -> atlas_creation_nonlin1_inputspec;

	  atlas_creation_inputspec -> atlas_creation_nonlin2_inputspec;

	  atlas_creation_inputspec -> atlas_creation_nonlin3_inputspec;

	  atlas_creation_inputspec -> atlas_creation_nonlin4_inputspec;

	  atlas_creation_lin_reg0_outputspec -> atlas_creation_lin_reg1_inputspec;

	  atlas_creation_lin_reg1_outputspec -> atlas_creation_lin_reg2_inputspec;

	  atlas_creation_lin_reg2_outputspec -> atlas_creation_lin_reg3_inputspec;

	  atlas_creation_lin_reg3_outputspec -> atlas_creation_lin_reg4_inputspec;

	  atlas_creation_lin_reg4_outputspec -> atlas_creation_lin_reg5_inputspec;

	  atlas_creation_lin_reg5_outputspec -> atlas_creation_nonlin0_inputspec;

	  atlas_creation_lin_reg5_outputspec -> atlas_creation_nonlin0_inputspec;

	  atlas_creation_lin_reg5_outputspec -> atlas_creation_nonlin1_inputspec;

	  atlas_creation_lin_reg5_outputspec -> atlas_creation_nonlin2_inputspec;

	  atlas_creation_lin_reg5_outputspec -> atlas_creation_nonlin3_inputspec;

	  atlas_creation_lin_reg5_outputspec -> atlas_creation_nonlin4_inputspec;

	  atlas_creation_nonlin0_outputspec -> atlas_creation_nonlin1_inputspec;

	  atlas_creation_nonlin1_outputspec -> atlas_creation_nonlin2_inputspec;

	  atlas_creation_nonlin2_outputspec -> atlas_creation_nonlin3_inputspec;

	  atlas_creation_nonlin3_outputspec -> atlas_creation_nonlin4_inputspec;

	  atlas_creation_nonlin4_outputspec -> atlas_creation_outputspec;

	  atlas_creation_nonlin4_outputspec -> atlas_creation_outputspec;

	}


.. _nipype.workflows.smri.niftyreg.groupwise.create_linear_gw_step:

:func:`create_linear_gw_step`
-----------------------------

`Link to code <http://github.com/nipy/nipype/tree/ec86b7476/nipype/workflows/smri/niftyreg/groupwise.py#L15>`__



Creates a workflow that performs linear co-registration of a set of images
using RegAladin, producing an average image and a set of affine
transformation matrices linking each of the floating images to the average.

Inputs::

    inputspec.in_files - The input files to be registered
    inputspec.ref_file - The initial reference image that the input files
                          are registered to
    inputspec.rmask_file - Mask of the reference image
    inputspec.in_aff_files - Initial affine transformation files

Outputs::

    outputspec.average_image - The average image
    outputspec.aff_files - The affine transformation files

Optional arguments::

    linear_options_hash - An options dictionary containing a list of
                          parameters for RegAladin that take
    the same form as given in the interface (default None)
    demean - Selects whether to demean the transformation matrices when
             performing the averaging (default True)
    initial_affines - Selects whether to iterate over initial affine
                      images, which we generally won't have (default False)

Example
~~~~~~~

>>> from nipype.workflows.smri.niftyreg import create_linear_gw_step
>>> lgw = create_linear_gw_step('my_linear_coreg')  # doctest: +SKIP
>>> lgw.inputs.inputspec.in_files = [
...     'file1.nii.gz', 'file2.nii.gz']  # doctest: +SKIP
>>> lgw.inputs.inputspec.ref_file = ['ref.nii.gz']  # doctest: +SKIP
>>> lgw.run()  # doctest: +SKIP


Graph
~~~~~

.. graphviz::

	digraph linear_gw_niftyreg{

	  label="linear_gw_niftyreg";

	  linear_gw_niftyreg_inputspec[label="inputspec (utility)"];

	  linear_gw_niftyreg_lin_reg[label="lin_reg (niftyreg)"];

	  linear_gw_niftyreg_ave_ims[label="ave_ims (niftyreg)"];

	  linear_gw_niftyreg_outputspec[label="outputspec (utility)"];

	  linear_gw_niftyreg_inputspec -> linear_gw_niftyreg_lin_reg;

	  linear_gw_niftyreg_inputspec -> linear_gw_niftyreg_lin_reg;

	  linear_gw_niftyreg_inputspec -> linear_gw_niftyreg_ave_ims;

	  linear_gw_niftyreg_lin_reg -> linear_gw_niftyreg_ave_ims;

	  linear_gw_niftyreg_lin_reg -> linear_gw_niftyreg_outputspec;

	  linear_gw_niftyreg_ave_ims -> linear_gw_niftyreg_outputspec;

	}


.. _nipype.workflows.smri.niftyreg.groupwise.create_nonlinear_gw_step:

:func:`create_nonlinear_gw_step`
--------------------------------

`Link to code <http://github.com/nipy/nipype/tree/ec86b7476/nipype/workflows/smri/niftyreg/groupwise.py#L111>`__



Creates a workflow that perform non-linear co-registrations of a set of
images using RegF3d, producing an non-linear average image and a set of
cpp transformation linking each of the floating images to the average.

Inputs::

    inputspec.in_files - The input files to be registered
    inputspec.ref_file - The initial reference image that the input files
                          are registered to
    inputspec.rmask_file - Mask of the reference image
    inputspec.in_trans_files - Initial transformation files (affine or
                                cpps)

Outputs::

    outputspec.average_image - The average image
    outputspec.cpp_files - The bspline transformation files

Optional arguments::

    nonlinear_options_hash - An options dictionary containing a list of
                             parameters for RegAladin that take the
    same form as given in the interface (default None)
    initial_affines - Selects whether to iterate over initial affine
                      images, which we generally won't have (default False)

Example
~~~~~~~
>>> from nipype.workflows.smri.niftyreg import create_nonlinear_gw_step
>>> nlc = create_nonlinear_gw_step('nonlinear_coreg')  # doctest: +SKIP
>>> nlc.inputs.inputspec.in_files = [
...     'file1.nii.gz', 'file2.nii.gz']  # doctest: +SKIP
>>> nlc.inputs.inputspec.ref_file = ['ref.nii.gz']  # doctest: +SKIP
>>> nlc.run()  # doctest: +SKIP


Graph
~~~~~

.. graphviz::

	digraph nonlinear_gw_niftyreg{

	  label="nonlinear_gw_niftyreg";

	  nonlinear_gw_niftyreg_inputspec[label="inputspec (utility)"];

	  nonlinear_gw_niftyreg_nonlin_reg[label="nonlin_reg (niftyreg)"];

	  nonlinear_gw_niftyreg_ave_ims[label="ave_ims (niftyreg)"];

	  nonlinear_gw_niftyreg_outputspec[label="outputspec (utility)"];

	  nonlinear_gw_niftyreg_inputspec -> nonlinear_gw_niftyreg_nonlin_reg;

	  nonlinear_gw_niftyreg_inputspec -> nonlinear_gw_niftyreg_nonlin_reg;

	  nonlinear_gw_niftyreg_inputspec -> nonlinear_gw_niftyreg_ave_ims;

	  nonlinear_gw_niftyreg_nonlin_reg -> nonlinear_gw_niftyreg_ave_ims;

	  nonlinear_gw_niftyreg_nonlin_reg -> nonlinear_gw_niftyreg_outputspec;

	  nonlinear_gw_niftyreg_ave_ims -> nonlinear_gw_niftyreg_outputspec;

	}

