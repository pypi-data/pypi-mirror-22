.. AUTO-GENERATED FILE -- DO NOT EDIT!

interfaces.dipy.tracks
======================


.. _nipype.interfaces.dipy.tracks.StreamlineTractography:


.. index:: StreamlineTractography

StreamlineTractography
----------------------

`Link to code <http://github.com/nipy/nipype/tree/ec86b7476/nipype/interfaces/dipy/tracks.py#L144>`__

Streamline tractography using EuDX [Garyfallidis12]_.

.. [Garyfallidis12] Garyfallidis E., “Towards an accurate brain
  tractography”, PhD thesis, University of Cambridge, 2012

Example
~~~~~~~

>>> from nipype.interfaces import dipy as ndp
>>> track = ndp.StreamlineTractography()
>>> track.inputs.in_file = '4d_dwi.nii'
>>> track.inputs.in_model = 'model.pklz'
>>> track.inputs.tracking_mask = 'dilated_wm_mask.nii'
>>> res = track.run() # doctest: +SKIP

Inputs::

        [Mandatory]
        gfa_thresh: (a float, nipype default value: 0.2)
                GFA threshold to compute tracking mask
        in_file: (an existing file name)
                input diffusion data
        min_angle: (a float, nipype default value: 25.0)
                minimum separation angle
        multiprocess: (a boolean, nipype default value: True)
                use multiprocessing
        num_seeds: (an integer (int or long), nipype default value: 10000)
                desired number of tracks in tractography
        peak_threshold: (a float, nipype default value: 0.5)
                threshold to consider peaks from model
        save_seeds: (a boolean, nipype default value: False)
                save seeding voxels coordinates

        [Optional]
        ignore_exception: (a boolean, nipype default value: False)
                Print an error message instead of throwing an exception in case the
                interface fails to run
        in_model: (an existing file name)
                input f/d-ODF model extracted from.
        in_peaks: (an existing file name)
                peaks computed from the odf
        out_prefix: (a unicode string)
                output prefix for file names
        seed_coord: (an existing file name)
                file containing the list of seed voxel coordinates (N,3)
        seed_mask: (an existing file name)
                input mask within which perform seeding
        tracking_mask: (an existing file name)
                input mask within which perform tracking

Outputs::

        gfa: (a file name)
                The resulting GFA (generalized FA) computed using the peaks of the
                ODF
        odf_peaks: (a file name)
                peaks computed from the odf
        out_seeds: (a file name)
                file containing the (N,3) *voxel* coordinates used in seeding.
        tracks: (a file name)
                TrackVis file containing extracted streamlines

.. _nipype.interfaces.dipy.tracks.TrackDensityMap:


.. index:: TrackDensityMap

TrackDensityMap
---------------

`Link to code <http://github.com/nipy/nipype/tree/ec86b7476/nipype/interfaces/dipy/tracks.py#L43>`__

Creates a tract density image from a TrackVis track file using functions
from dipy

Example
~~~~~~~

>>> import nipype.interfaces.dipy as dipy
>>> trk2tdi = dipy.TrackDensityMap()
>>> trk2tdi.inputs.in_file = 'converted.trk'
>>> trk2tdi.run()                                   # doctest: +SKIP

Inputs::

        [Mandatory]
        in_file: (an existing file name)
                The input TrackVis track file

        [Optional]
        data_dims: (a list of from 3 to 3 items which are an integer (int or
                 long))
                The size of the image in voxels.
        ignore_exception: (a boolean, nipype default value: False)
                Print an error message instead of throwing an exception in case the
                interface fails to run
        out_filename: (a file name, nipype default value: tdi.nii)
                The output filename for the tracks in TrackVis (.trk) format
        points_space: ('rasmm' or 'voxel' or None, nipype default value:
                 rasmm)
                coordinates of trk file
        reference: (an existing file name)
                A reference file to define RAS coordinates space
        voxel_dims: (a list of from 3 to 3 items which are a float)
                The size of each voxel in mm.

Outputs::

        out_file: (an existing file name)
