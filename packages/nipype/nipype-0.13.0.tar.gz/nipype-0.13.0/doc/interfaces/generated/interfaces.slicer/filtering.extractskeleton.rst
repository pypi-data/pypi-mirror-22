.. AUTO-GENERATED FILE -- DO NOT EDIT!

interfaces.slicer.filtering.extractskeleton
===========================================


.. _nipype.interfaces.slicer.filtering.extractskeleton.ExtractSkeleton:


.. index:: ExtractSkeleton

ExtractSkeleton
---------------

`Link to code <http://github.com/nipy/nipype/tree/ec86b7476/nipype/interfaces/slicer/filtering/extractskeleton.py#L23>`__

Wraps command **ExtractSkeleton **

title: Extract Skeleton

category: Filtering

description: Extract the skeleton of a binary object.  The skeleton can be limited to being a 1D curve or allowed to be a full 2D manifold.  The branches of the skeleton can be pruned so that only the maximal center skeleton is returned.

version: 0.1.0.$Revision: 2104 $(alpha)

documentation-url: http://wiki.slicer.org/slicerWiki/index.php/Documentation/4.1/Modules/ExtractSkeleton

contributor: Pierre Seroul (UNC), Martin Styner (UNC), Guido Gerig (UNC), Stephen Aylward (Kitware)

acknowledgements: The original implementation of this method was provided by ETH Zurich, Image Analysis Laboratory of Profs Olaf Kuebler, Gabor Szekely and Guido Gerig.  Martin Styner at UNC, Chapel Hill made enhancements.  Wrapping for Slicer was provided by Pierre Seroul and Stephen Aylward at Kitware, Inc.

Inputs::

        [Mandatory]

        [Optional]
        InputImageFileName: (an existing file name)
                Input image
                flag: %s, position: -2
        OutputImageFileName: (a boolean or a file name)
                Skeleton of the input image
                flag: %s, position: -1
        args: (a unicode string)
                Additional parameters to the command
                flag: %s
        dontPrune: (a boolean)
                Return the full skeleton, not just the maximal skeleton
                flag: --dontPrune
        environ: (a dictionary with keys which are a bytes or None or a value
                 of class 'str' and with values which are a bytes or None or a value
                 of class 'str', nipype default value: {})
                Environment variables
        ignore_exception: (a boolean, nipype default value: False)
                Print an error message instead of throwing an exception in case the
                interface fails to run
        numPoints: (an integer (int or long))
                Number of points used to represent the skeleton
                flag: --numPoints %d
        pointsFile: (a unicode string)
                Name of the file to store the coordinates of the central (1D)
                skeleton points
                flag: --pointsFile %s
        terminal_output: ('stream' or 'allatonce' or 'file' or 'none')
                Control terminal output: `stream` - displays to terminal immediately
                (default), `allatonce` - waits till command is finished to display
                output, `file` - writes output to file, `none` - output is ignored
        type: ('1D' or '2D')
                Type of skeleton to create
                flag: --type %s

Outputs::

        OutputImageFileName: (an existing file name)
                Skeleton of the input image
