.. AUTO-GENERATED FILE -- DO NOT EDIT!

interfaces.diffusion_toolkit.postproc
=====================================


.. _nipype.interfaces.diffusion_toolkit.postproc.SplineFilter:


.. index:: SplineFilter

SplineFilter
------------

`Link to code <http://github.com/nipy/nipype/tree/ec86b7476/nipype/interfaces/diffusion_toolkit/postproc.py#L31>`__

Wraps command **spline_filter**

Smoothes TrackVis track files with a B-Spline filter.

Helps remove redundant track points and segments
(thus reducing the size of the track file) and also
make tracks nicely smoothed. It will NOT change the
quality of the tracks or lose any original information.

Example
~~~~~~~

>>> import nipype.interfaces.diffusion_toolkit as dtk
>>> filt = dtk.SplineFilter()
>>> filt.inputs.track_file = 'tracks.trk'
>>> filt.inputs.step_length = 0.5
>>> filt.run()                                 # doctest: +SKIP

Inputs::

        [Mandatory]
        step_length: (a float)
                in the unit of minimum voxel size
                flag: %f, position: 1
        track_file: (an existing file name)
                file containing tracks to be filtered
                flag: %s, position: 0

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
        output_file: (a file name, nipype default value: spline_tracks.trk)
                target file for smoothed tracks
                flag: %s, position: 2
        terminal_output: ('stream' or 'allatonce' or 'file' or 'none')
                Control terminal output: `stream` - displays to terminal immediately
                (default), `allatonce` - waits till command is finished to display
                output, `file` - writes output to file, `none` - output is ignored

Outputs::

        smoothed_track_file: (an existing file name)

.. _nipype.interfaces.diffusion_toolkit.postproc.TrackMerge:


.. index:: TrackMerge

TrackMerge
----------

`Link to code <http://github.com/nipy/nipype/tree/ec86b7476/nipype/interfaces/diffusion_toolkit/postproc.py#L69>`__

Wraps command **track_merge**

Merges several TrackVis track files into a single track
file.

An id type property tag is added to each track in the
newly merged file, with each unique id representing where
the track was originally from. When the merged file is
loaded in TrackVis, a property filter will show up in
Track Property panel. Users can adjust that to distinguish
and sub-group tracks by its id (origin).

Example
~~~~~~~

>>> import nipype.interfaces.diffusion_toolkit as dtk
>>> mrg = dtk.TrackMerge()
>>> mrg.inputs.track_files = ['track1.trk','track2.trk']
>>> mrg.run()                                 # doctest: +SKIP

Inputs::

        [Mandatory]
        track_files: (a list of items which are an existing file name)
                file containing tracks to be filtered
                flag: %s..., position: 0

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
        output_file: (a file name, nipype default value: merged_tracks.trk)
                target file for merged tracks
                flag: %s, position: -1
        terminal_output: ('stream' or 'allatonce' or 'file' or 'none')
                Control terminal output: `stream` - displays to terminal immediately
                (default), `allatonce` - waits till command is finished to display
                output, `file` - writes output to file, `none` - output is ignored

Outputs::

        track_file: (an existing file name)
