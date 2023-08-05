.. AUTO-GENERATED FILE -- DO NOT EDIT!

interfaces.niftyseg.em
======================


.. _nipype.interfaces.niftyseg.em.EM:


.. index:: EM

EM
--

`Link to code <http://github.com/nipy/nipype/tree/ec86b7476/nipype/interfaces/niftyseg/em.py#L114>`__

Wraps command **seg_EM**

Interface for executable seg_EM from NiftySeg platform.

seg_EM is a general purpose intensity based image segmentation tool. In
it's simplest form, it takes in one 2D or 3D image and segments it in n
classes.

`Source code <http://cmictig.cs.ucl.ac.uk/wiki/index.php/NiftySeg>`_ |
`Documentation <http://cmictig.cs.ucl.ac.uk/wiki/index.php/NiftySeg_documentation>`_

Examples
~~~~~~~~
>>> from nipype.interfaces import niftyseg
>>> node = niftyseg.EM()
>>> node.inputs.in_file = 'im1.nii'
>>> node.inputs.no_prior = 4
>>> node.cmdline  # doctest: +ALLOW_UNICODE
'seg_EM -in im1.nii -nopriors 4 -bc_out im1_bc_em.nii.gz -out im1_em.nii.gz -out_outlier im1_outlier_em.nii.gz'

Inputs::

        [Mandatory]
        in_file: (an existing file name)
                Input image to segment
                flag: -in %s, position: 4
        no_prior: (an integer (int or long))
                Number of classes to use without prior
                flag: -nopriors %s
                mutually_exclusive: prior_4D, priors
        prior_4D: (an existing file name)
                4D file containing the priors
                flag: -prior4D %s
                mutually_exclusive: no_prior, priors
        priors: (a list of items which are any value)
                List of priors filepaths.
                flag: %s
                mutually_exclusive: no_prior, prior_4D

        [Optional]
        args: (a unicode string)
                Additional parameters to the command
                flag: %s
        bc_order_val: (an integer (int or long))
                Polynomial order for the bias field
                flag: -bc_order %s
        bc_thresh_val: (a float)
                Bias field correction will run only if the ratio of improvement is
                below bc_thresh. (default=0 [OFF])
                flag: -bc_thresh %s
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
        max_iter: (an integer (int or long))
                Maximum number of iterations
                flag: -max_iter %s
        min_iter: (an integer (int or long))
                Minimun number of iterations
                flag: -min_iter %s
        mrf_beta_val: (a float)
                Weight of the Markov Random Field
                flag: -mrf_beta %s
        out_bc_file: (a file name)
                Output bias corrected image
                flag: -bc_out %s
        out_file: (a file name)
                Output segmentation
                flag: -out %s
        out_outlier_file: (a file name)
                Output outlierness image
                flag: -out_outlier %s
        outlier_val: (a tuple of the form: (a float, a float))
                Outlier detection as in (Van Leemput TMI 2003). <fl1> is the
                Mahalanobis threshold [recommended between 3 and 7] <fl2> is a
                convergence ratio below which the outlier detection is going to be
                done [recommended 0.01]
                flag: -outlier %s %s
        reg_val: (a float)
                Amount of regularization over the diagonal of the covariance matrix
                [above 1]
                flag: -reg %s
        relax_priors: (a tuple of the form: (a float, a float))
                Relax Priors [relaxation factor: 0<rf<1 (recommended=0.5), gaussian
                regularization: gstd>0 (recommended=2.0)] /only 3D/
                flag: -rf %s %s
        terminal_output: ('stream' or 'allatonce' or 'file' or 'none')
                Control terminal output: `stream` - displays to terminal immediately
                (default), `allatonce` - waits till command is finished to display
                output, `file` - writes output to file, `none` - output is ignored

Outputs::

        out_bc_file: (a file name)
                Output bias corrected image
        out_file: (a file name)
                Output segmentation
        out_outlier_file: (a file name)
                Output outlierness image
