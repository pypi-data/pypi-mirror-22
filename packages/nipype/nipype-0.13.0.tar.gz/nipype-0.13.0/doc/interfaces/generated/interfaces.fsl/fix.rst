.. AUTO-GENERATED FILE -- DO NOT EDIT!

interfaces.fsl.fix
==================


.. _nipype.interfaces.fsl.fix.Classifier:


.. index:: Classifier

Classifier
----------

`Link to code <http://github.com/nipy/nipype/tree/ec86b7476/nipype/interfaces/fsl/fix.py#L225>`__

Wraps command **None**

Classify ICA components using a specific training dataset (<thresh> is in the range 0-100, typically 5-20).

Inputs::

        [Mandatory]
        thresh: (an integer (int or long))
                Threshold for cleanup.
                flag: %d, position: -1
        trained_wts_file: (an existing file name)
                trained-weights file
                flag: %s, position: 2

        [Optional]
        args: (a unicode string)
                Additional parameters to the command
                flag: %s
        artifacts_list_file: (a file name)
                Text file listing which ICs are artifacts; can be the output from
                classification or can be created manually
        environ: (a dictionary with keys which are a bytes or None or a value
                 of class 'str' and with values which are a bytes or None or a value
                 of class 'str', nipype default value: {})
                Environment variables
        ignore_exception: (a boolean, nipype default value: False)
                Print an error message instead of throwing an exception in case the
                interface fails to run
        mel_ica: (an existing directory name)
                Melodic output directory or directories
                flag: %s, position: 1
        terminal_output: ('stream' or 'allatonce' or 'file' or 'none')
                Control terminal output: `stream` - displays to terminal immediately
                (default), `allatonce` - waits till command is finished to display
                output, `file` - writes output to file, `none` - output is ignored

Outputs::

        artifacts_list_file: (a file name)
                Text file listing which ICs are artifacts; can be the output from
                classification or can be created manually

.. _nipype.interfaces.fsl.fix.Cleaner:


.. index:: Cleaner

Cleaner
-------

`Link to code <http://github.com/nipy/nipype/tree/ec86b7476/nipype/interfaces/fsl/fix.py#L278>`__

Wraps command **None**

Extract features (for later training and/or classifying)

Inputs::

        [Mandatory]
        artifacts_list_file: (an existing file name)
                Text file listing which ICs are artifacts; can be the output from
                classification or can be created manually
                flag: %s, position: 1

        [Optional]
        aggressive: (a boolean)
                Apply aggressive (full variance) cleanup, instead of the default
                less-aggressive (unique variance) cleanup.
                flag: -A, position: 3
        args: (a unicode string)
                Additional parameters to the command
                flag: %s
        cleanup_motion: (a boolean)
                cleanup motion confounds, looks for design.fsf for highpass filter
                cut-off
                flag: -m, position: 2
        confound_file: (a file name)
                Include additional confound file.
                flag: -x %s, position: 4
        confound_file_1: (a file name)
                Include additional confound file.
                flag: -x %s, position: 5
        confound_file_2: (a file name)
                Include additional confound file.
                flag: -x %s, position: 6
        environ: (a dictionary with keys which are a bytes or None or a value
                 of class 'str' and with values which are a bytes or None or a value
                 of class 'str', nipype default value: {})
                Environment variables
        highpass: (a float, nipype default value: 100)
                cleanup motion confounds
                flag: -m -h %f, position: 2
        ignore_exception: (a boolean, nipype default value: False)
                Print an error message instead of throwing an exception in case the
                interface fails to run
        terminal_output: ('stream' or 'allatonce' or 'file' or 'none')
                Control terminal output: `stream` - displays to terminal immediately
                (default), `allatonce` - waits till command is finished to display
                output, `file` - writes output to file, `none` - output is ignored

Outputs::

        cleaned_functional_file: (an existing file name)
                Cleaned session data

.. _nipype.interfaces.fsl.fix.FeatureExtractor:


.. index:: FeatureExtractor

FeatureExtractor
----------------

`Link to code <http://github.com/nipy/nipype/tree/ec86b7476/nipype/interfaces/fsl/fix.py#L131>`__

Wraps command **None**

Extract features (for later training and/or classifying)

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
        mel_ica: (an existing directory name)
                Melodic output directory or directories
                flag: %s, position: -1
        terminal_output: ('stream' or 'allatonce' or 'file' or 'none')
                Control terminal output: `stream` - displays to terminal immediately
                (default), `allatonce` - waits till command is finished to display
                output, `file` - writes output to file, `none` - output is ignored

Outputs::

        mel_ica: (an existing directory name)
                Melodic output directory or directories
                flag: %s, position: -1

.. _nipype.interfaces.fsl.fix.Training:


.. index:: Training

Training
--------

`Link to code <http://github.com/nipy/nipype/tree/ec86b7476/nipype/interfaces/fsl/fix.py#L159>`__

Wraps command **None**

Train the classifier based on your own FEAT/MELODIC output directory.

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
        loo: (a boolean)
                full leave-one-out test with classifier training
                flag: -l, position: 2
        mel_icas: (a list of items which are an existing directory name)
                Melodic output directories
                flag: %s, position: -1
        terminal_output: ('stream' or 'allatonce' or 'file' or 'none')
                Control terminal output: `stream` - displays to terminal immediately
                (default), `allatonce` - waits till command is finished to display
                output, `file` - writes output to file, `none` - output is ignored
        trained_wts_filestem: (a unicode string)
                trained-weights filestem, used for trained_wts_file and output
                directories
                flag: %s, position: 1

Outputs::

        trained_wts_file: (an existing file name)
                Trained-weights file

.. _nipype.interfaces.fsl.fix.TrainingSetCreator:


.. index:: TrainingSetCreator

TrainingSetCreator
------------------

`Link to code <http://github.com/nipy/nipype/tree/ec86b7476/nipype/interfaces/fsl/fix.py#L85>`__

Goes through set of provided melodic output directories, to find all
the ones that have a hand_labels_noise.txt file in them.

This is outsourced as a separate class, so that the pipeline is
rerun everytime a handlabeled file has been changed, or a new one
created.

Inputs::

        [Mandatory]

        [Optional]
        ignore_exception: (a boolean, nipype default value: False)
                Print an error message instead of throwing an exception in case the
                interface fails to run
        mel_icas_in: (a list of items which are an existing directory name)
                Melodic output directories
                flag: %s, position: -1

Outputs::

        mel_icas_out: (a list of items which are an existing directory name)
                Hand labels for noise vs signal
                flag: %s, position: -1
