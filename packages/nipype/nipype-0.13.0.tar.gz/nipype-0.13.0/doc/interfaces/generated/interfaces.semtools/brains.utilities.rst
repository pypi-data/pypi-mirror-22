.. AUTO-GENERATED FILE -- DO NOT EDIT!

interfaces.semtools.brains.utilities
====================================


.. _nipype.interfaces.semtools.brains.utilities.GenerateEdgeMapImage:


.. index:: GenerateEdgeMapImage

GenerateEdgeMapImage
--------------------

`Link to code <http://github.com/nipy/nipype/tree/ec86b7476/nipype/interfaces/semtools/brains/utilities.py#L66>`__

Wraps command ** GenerateEdgeMapImage **

title: GenerateEdgeMapImage

category: BRAINS.Utilities

description: Automatic edgemap generation for edge-guided super-resolution reconstruction

version: 1.0

contributor: Ali Ghayoor

Inputs::

        [Mandatory]

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
        inputMRVolumes: (a list of items which are an existing file name)
                List of input structural MR volumes to create the maximum edgemap
                flag: --inputMRVolumes %s...
        inputMask: (an existing file name)
                Input mask file name. If set, image histogram percentiles will be
                calculated within the mask
                flag: --inputMask %s
        lowerPercentileMatching: (a float)
                Map lower quantile and below to minOutputRange. It should be a value
                between zero and one
                flag: --lowerPercentileMatching %f
        maximumOutputRange: (an integer (int or long))
                Map upper quantile and above to maximum output range. Default is 255
                that is the maximum range of unsigned char
                flag: --maximumOutputRange %d
        minimumOutputRange: (an integer (int or long))
                Map lower quantile and below to minimum output range. It should be a
                small number greater than zero. Default is 1
                flag: --minimumOutputRange %d
        numberOfThreads: (an integer (int or long))
                Explicitly specify the maximum number of threads to use.
                flag: --numberOfThreads %d
        outputEdgeMap: (a boolean or a file name)
                output edgemap file name
                flag: --outputEdgeMap %s
        outputMaximumGradientImage: (a boolean or a file name)
                output gradient image file name
                flag: --outputMaximumGradientImage %s
        terminal_output: ('stream' or 'allatonce' or 'file' or 'none')
                Control terminal output: `stream` - displays to terminal immediately
                (default), `allatonce` - waits till command is finished to display
                output, `file` - writes output to file, `none` - output is ignored
        upperPercentileMatching: (a float)
                Map upper quantile and above to maxOutputRange. It should be a value
                between zero and one
                flag: --upperPercentileMatching %f

Outputs::

        outputEdgeMap: (an existing file name)
                (required) output file name
        outputMaximumGradientImage: (an existing file name)
                output gradient image file name

.. _nipype.interfaces.semtools.brains.utilities.GeneratePurePlugMask:


.. index:: GeneratePurePlugMask

GeneratePurePlugMask
--------------------

`Link to code <http://github.com/nipy/nipype/tree/ec86b7476/nipype/interfaces/semtools/brains/utilities.py#L96>`__

Wraps command ** GeneratePurePlugMask **

title: GeneratePurePlugMask

category: BRAINS.Utilities

description: This program gets several modality image files and returns a binary mask that defines the pure plugs

version: 1.0

contributor: Ali Ghayoor

Inputs::

        [Mandatory]

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
        inputImageModalities: (a list of items which are an existing file
                 name)
                List of input image file names to create pure plugs mask
                flag: --inputImageModalities %s...
        numberOfSubSamples: (a list of items which are an integer (int or
                 long))
                Number of continous index samples taken at each direction of lattice
                space for each plug volume
                flag: --numberOfSubSamples %s
        outputMaskFile: (a boolean or a file name)
                Output binary mask file name
                flag: --outputMaskFile %s
        terminal_output: ('stream' or 'allatonce' or 'file' or 'none')
                Control terminal output: `stream` - displays to terminal immediately
                (default), `allatonce` - waits till command is finished to display
                output, `file` - writes output to file, `none` - output is ignored
        threshold: (a float)
                threshold value to define class membership
                flag: --threshold %f

Outputs::

        outputMaskFile: (an existing file name)
                (required) Output binary mask file name

.. _nipype.interfaces.semtools.brains.utilities.HistogramMatchingFilter:


.. index:: HistogramMatchingFilter

HistogramMatchingFilter
-----------------------

`Link to code <http://github.com/nipy/nipype/tree/ec86b7476/nipype/interfaces/semtools/brains/utilities.py#L30>`__

Wraps command ** HistogramMatchingFilter **

title: Write Out Image Intensities

category: BRAINS.Utilities

description: For Analysis

version: 0.1

contributor: University of Iowa Department of Psychiatry, http:://www.psychiatry.uiowa.edu

Inputs::

        [Mandatory]

        [Optional]
        args: (a unicode string)
                Additional parameters to the command
                flag: %s
        environ: (a dictionary with keys which are a bytes or None or a value
                 of class 'str' and with values which are a bytes or None or a value
                 of class 'str', nipype default value: {})
                Environment variables
        histogramAlgorithm: ('OtsuHistogramMatching')
                 histogram algrithm selection
                flag: --histogramAlgorithm %s
        ignore_exception: (a boolean, nipype default value: False)
                Print an error message instead of throwing an exception in case the
                interface fails to run
        inputBinaryVolume: (an existing file name)
                inputBinaryVolume
                flag: --inputBinaryVolume %s
        inputVolume: (an existing file name)
                The Input image to be computed for statistics
                flag: --inputVolume %s
        numberOfHistogramBins: (an integer (int or long))
                 number of histogram bin
                flag: --numberOfHistogramBins %d
        numberOfMatchPoints: (an integer (int or long))
                 number of histogram matching points
                flag: --numberOfMatchPoints %d
        outputVolume: (a boolean or a file name)
                Output Image File Name
                flag: --outputVolume %s
        referenceBinaryVolume: (an existing file name)
                referenceBinaryVolume
                flag: --referenceBinaryVolume %s
        referenceVolume: (an existing file name)
                The Input image to be computed for statistics
                flag: --referenceVolume %s
        terminal_output: ('stream' or 'allatonce' or 'file' or 'none')
                Control terminal output: `stream` - displays to terminal immediately
                (default), `allatonce` - waits till command is finished to display
                output, `file` - writes output to file, `none` - output is ignored
        verbose: (a boolean)
                 verbose mode running for debbuging
                flag: --verbose
        writeHistogram: (a unicode string)
                 decide if histogram data would be written with prefixe of the file
                name
                flag: --writeHistogram %s

Outputs::

        outputVolume: (an existing file name)
                Output Image File Name
