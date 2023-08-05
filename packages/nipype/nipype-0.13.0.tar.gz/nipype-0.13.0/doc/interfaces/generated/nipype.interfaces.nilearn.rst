.. AUTO-GENERATED FILE -- DO NOT EDIT!

interfaces.nilearn
==================


.. _nipype.interfaces.nilearn.SignalExtraction:


.. index:: SignalExtraction

SignalExtraction
----------------

`Link to code <http://github.com/nipy/nipype/tree/ec86b7476/nipype/interfaces/nilearn.py#L61>`__

Extracts signals over tissue classes or brain regions

>>> seinterface = SignalExtraction()
>>> seinterface.inputs.in_file = 'functional.nii'
>>> seinterface.inputs.label_files = 'segmentation0.nii.gz'
>>> seinterface.inputs.out_file = 'means.tsv'
>>> segments = ['CSF', 'GrayMatter', 'WhiteMatter']
>>> seinterface.inputs.class_labels = segments
>>> seinterface.inputs.detrend = True
>>> seinterface.inputs.include_global = True

Inputs::

        [Mandatory]
        class_labels: (a list of items which are any value)
                Human-readable labels for each segment in the label file, in order.
                The length of class_labels must be equal to the number of segments
                (background excluded). This list corresponds to the class labels in
                label_file in ascending order
        in_file: (an existing file name)
                4-D fMRI nii file
        label_files: (a list of items which are an existing file name)
                a 3-D label image, with 0 denoting background, or a list of 3-D
                probability maps (one per label) or the equivalent 4D file.

        [Optional]
        detrend: (a boolean, nipype default value: False)
                If True, perform detrending using nilearn.
        ignore_exception: (a boolean, nipype default value: False)
                Print an error message instead of throwing an exception in case the
                interface fails to run
        incl_shared_variance: (a boolean, nipype default value: True)
                By default (True), returns simple time series calculated from each
                region independently (e.g., for noise regression). If False, returns
                unique signals for each region, discarding shared variance (e.g.,
                for connectivity. Only has effect with 4D probability maps.
        include_global: (a boolean, nipype default value: False)
                If True, include an extra column labeled "GlobalSignal", with values
                calculated from the entire brain (instead of just regions).
        out_file: (a file name, nipype default value: signals.tsv)
                The name of the file to output to. signals.tsv by default

Outputs::

        out_file: (an existing file name)
                tsv file containing the computed signals, with as many columns as
                there are labels and as many rows as there are timepoints in
                in_file, plus a header row with values from class_labels
