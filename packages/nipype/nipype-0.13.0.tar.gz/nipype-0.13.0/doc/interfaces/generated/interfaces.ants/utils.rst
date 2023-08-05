.. AUTO-GENERATED FILE -- DO NOT EDIT!

interfaces.ants.utils
=====================


.. _nipype.interfaces.ants.utils.AffineInitializer:


.. index:: AffineInitializer

AffineInitializer
-----------------

`Link to code <http://github.com/nipy/nipype/tree/ec86b7476/nipype/interfaces/ants/utils.py#L210>`__

Wraps command **antsAffineInitializer**

Initialize an affine transform (as in antsBrainExtraction.sh)

>>> from nipype.interfaces.ants import AffineInitializer
>>> init = AffineInitializer()
>>> init.inputs.fixed_image = 'fixed1.nii'
>>> init.inputs.moving_image = 'moving1.nii'
>>> init.cmdline # doctest: +ALLOW_UNICODE
'antsAffineInitializer 3 fixed1.nii moving1.nii transform.mat 15.000000 0.100000 0 10'

Inputs::

        [Mandatory]
        fixed_image: (an existing file name)
                reference image
                flag: %s, position: 1
        moving_image: (an existing file name)
                moving image
                flag: %s, position: 2

        [Optional]
        args: (a unicode string)
                Additional parameters to the command
                flag: %s
        dimension: (3 or 2, nipype default value: 3)
                dimension
                flag: %s, position: 0
        environ: (a dictionary with keys which are a bytes or None or a value
                 of class 'str' and with values which are a bytes or None or a value
                 of class 'str', nipype default value: {})
                Environment variables
        ignore_exception: (a boolean, nipype default value: False)
                Print an error message instead of throwing an exception in case the
                interface fails to run
        local_search: (an integer (int or long), nipype default value: 10)
                 determines if a local optimization is run at each search point for
                the set number of iterations
                flag: %d, position: 7
        out_file: (a file name, nipype default value: transform.mat)
                output transform file
                flag: %s, position: 3
        principal_axes: (a boolean, nipype default value: False)
                whether the rotation is searched around an initial principal axis
                alignment.
                flag: %d, position: 6
        radian_fraction: (0.0 <= a floating point number <= 1.0, nipype
                 default value: 0.1)
                search this arc +/- principal axes
                flag: %f, position: 5
        search_factor: (a float, nipype default value: 15.0)
                increments (degrees) for affine search
                flag: %f, position: 4
        terminal_output: ('stream' or 'allatonce' or 'file' or 'none')
                Control terminal output: `stream` - displays to terminal immediately
                (default), `allatonce` - waits till command is finished to display
                output, `file` - writes output to file, `none` - output is ignored

Outputs::

        out_file: (a file name)
                output transform file

.. _nipype.interfaces.ants.utils.AverageAffineTransform:


.. index:: AverageAffineTransform

AverageAffineTransform
----------------------

`Link to code <http://github.com/nipy/nipype/tree/ec86b7476/nipype/interfaces/ants/utils.py#L33>`__

Wraps command **AverageAffineTransform**

Examples
~~~~~~~~
>>> from nipype.interfaces.ants import AverageAffineTransform
>>> avg = AverageAffineTransform()
>>> avg.inputs.dimension = 3
>>> avg.inputs.transforms = ['trans.mat', 'func_to_struct.mat']
>>> avg.inputs.output_affine_transform = 'MYtemplatewarp.mat'
>>> avg.cmdline # doctest: +ALLOW_UNICODE
'AverageAffineTransform 3 MYtemplatewarp.mat trans.mat func_to_struct.mat'

Inputs::

        [Mandatory]
        dimension: (3 or 2)
                image dimension (2 or 3)
                flag: %d, position: 0
        output_affine_transform: (a file name)
                Outputfname.txt: the name of the resulting transform.
                flag: %s, position: 1
        transforms: (a list of items which are an existing file name)
                transforms to average
                flag: %s, position: 3

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
        num_threads: (an integer (int or long), nipype default value: 1)
                Number of ITK threads to use
        terminal_output: ('stream' or 'allatonce' or 'file' or 'none')
                Control terminal output: `stream` - displays to terminal immediately
                (default), `allatonce` - waits till command is finished to display
                output, `file` - writes output to file, `none` - output is ignored

Outputs::

        affine_transform: (an existing file name)
                average transform file

.. _nipype.interfaces.ants.utils.AverageImages:


.. index:: AverageImages

AverageImages
-------------

`Link to code <http://github.com/nipy/nipype/tree/ec86b7476/nipype/interfaces/ants/utils.py#L74>`__

Wraps command **AverageImages**

Examples
~~~~~~~~
>>> from nipype.interfaces.ants import AverageImages
>>> avg = AverageImages()
>>> avg.inputs.dimension = 3
>>> avg.inputs.output_average_image = "average.nii.gz"
>>> avg.inputs.normalize = True
>>> avg.inputs.images = ['rc1s1.nii', 'rc1s1.nii']
>>> avg.cmdline # doctest: +ALLOW_UNICODE
'AverageImages 3 average.nii.gz 1 rc1s1.nii rc1s1.nii'

Inputs::

        [Mandatory]
        dimension: (3 or 2)
                image dimension (2 or 3)
                flag: %d, position: 0
        images: (a list of items which are an existing file name)
                image to apply transformation to (generally a coregistered
                functional)
                flag: %s, position: 3
        normalize: (a boolean)
                Normalize: if true, the 2nd imageis divided by its mean. This will
                select the largest image to average into.
                flag: %d, position: 2

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
        num_threads: (an integer (int or long), nipype default value: 1)
                Number of ITK threads to use
        output_average_image: (a file name, nipype default value:
                 average.nii)
                the name of the resulting image.
                flag: %s, position: 1
        terminal_output: ('stream' or 'allatonce' or 'file' or 'none')
                Control terminal output: `stream` - displays to terminal immediately
                (default), `allatonce` - waits till command is finished to display
                output, `file` - writes output to file, `none` - output is ignored

Outputs::

        output_average_image: (an existing file name)
                average image file

.. _nipype.interfaces.ants.utils.CreateJacobianDeterminantImage:


.. index:: CreateJacobianDeterminantImage

CreateJacobianDeterminantImage
------------------------------

`Link to code <http://github.com/nipy/nipype/tree/ec86b7476/nipype/interfaces/ants/utils.py#L157>`__

Wraps command **CreateJacobianDeterminantImage**

Examples
~~~~~~~~
>>> from nipype.interfaces.ants import CreateJacobianDeterminantImage
>>> jacobian = CreateJacobianDeterminantImage()
>>> jacobian.inputs.imageDimension = 3
>>> jacobian.inputs.deformationField = 'ants_Warp.nii.gz'
>>> jacobian.inputs.outputImage = 'out_name.nii.gz'
>>> jacobian.cmdline # doctest: +ALLOW_UNICODE
'CreateJacobianDeterminantImage 3 ants_Warp.nii.gz out_name.nii.gz'

Inputs::

        [Mandatory]
        deformationField: (an existing file name)
                deformation transformation file
                flag: %s, position: 1
        imageDimension: (3 or 2)
                image dimension (2 or 3)
                flag: %d, position: 0
        outputImage: (a file name)
                output filename
                flag: %s, position: 2

        [Optional]
        args: (a unicode string)
                Additional parameters to the command
                flag: %s
        doLogJacobian: (0 or 1)
                return the log jacobian
                flag: %d, position: 3
        environ: (a dictionary with keys which are a bytes or None or a value
                 of class 'str' and with values which are a bytes or None or a value
                 of class 'str', nipype default value: {})
                Environment variables
        ignore_exception: (a boolean, nipype default value: False)
                Print an error message instead of throwing an exception in case the
                interface fails to run
        num_threads: (an integer (int or long), nipype default value: 1)
                Number of ITK threads to use
        terminal_output: ('stream' or 'allatonce' or 'file' or 'none')
                Control terminal output: `stream` - displays to terminal immediately
                (default), `allatonce` - waits till command is finished to display
                output, `file` - writes output to file, `none` - output is ignored
        useGeometric: (0 or 1)
                return the geometric jacobian
                flag: %d, position: 4

Outputs::

        jacobian_image: (an existing file name)
                jacobian image

.. _nipype.interfaces.ants.utils.MultiplyImages:


.. index:: MultiplyImages

MultiplyImages
--------------

`Link to code <http://github.com/nipy/nipype/tree/ec86b7476/nipype/interfaces/ants/utils.py#L115>`__

Wraps command **MultiplyImages**

Examples
~~~~~~~~
>>> from nipype.interfaces.ants import MultiplyImages
>>> test = MultiplyImages()
>>> test.inputs.dimension = 3
>>> test.inputs.first_input = 'moving2.nii'
>>> test.inputs.second_input = 0.25
>>> test.inputs.output_product_image = "out.nii"
>>> test.cmdline # doctest: +ALLOW_UNICODE
'MultiplyImages 3 moving2.nii 0.25 out.nii'

Inputs::

        [Mandatory]
        dimension: (3 or 2)
                image dimension (2 or 3)
                flag: %d, position: 0
        first_input: (an existing file name)
                image 1
                flag: %s, position: 1
        output_product_image: (a file name)
                Outputfname.nii.gz: the name of the resulting image.
                flag: %s, position: 3
        second_input: (an existing file name or a float)
                image 2 or multiplication weight
                flag: %s, position: 2

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
        num_threads: (an integer (int or long), nipype default value: 1)
                Number of ITK threads to use
        terminal_output: ('stream' or 'allatonce' or 'file' or 'none')
                Control terminal output: `stream` - displays to terminal immediately
                (default), `allatonce` - waits till command is finished to display
                output, `file` - writes output to file, `none` - output is ignored

Outputs::

        output_product_image: (an existing file name)
                average image file
