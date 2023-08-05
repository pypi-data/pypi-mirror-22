.. AUTO-GENERATED FILE -- DO NOT EDIT!

interfaces.cmtk.convert
=======================


.. _nipype.interfaces.cmtk.convert.CFFConverter:


.. index:: CFFConverter

CFFConverter
------------

`Link to code <http://github.com/nipy/nipype/tree/ec86b7476/nipype/interfaces/cmtk/convert.py#L63>`__

Creates a Connectome File Format (CFF) file from input networks, surfaces, volumes, tracts, etcetera....

Example
~~~~~~~

>>> import nipype.interfaces.cmtk as cmtk
>>> cvt = cmtk.CFFConverter()
>>> cvt.inputs.title = 'subject 1'
>>> cvt.inputs.gifti_surfaces = ['lh.pial_converted.gii', 'rh.pial_converted.gii']
>>> cvt.inputs.tract_files = ['streamlines.trk']
>>> cvt.inputs.gpickled_networks = ['network0.gpickle']
>>> cvt.run()                 # doctest: +SKIP

Inputs::

        [Mandatory]

        [Optional]
        creator: (a unicode string)
                Creator
        data_files: (a list of items which are an existing file name)
                list of external data files (i.e. Numpy, HD5, XML)
        description: (a unicode string, nipype default value: Created with
                 the Nipype CFF converter)
                Description
        email: (a unicode string)
                Email address
        gifti_labels: (a list of items which are an existing file name)
                list of GIFTI labels
        gifti_surfaces: (a list of items which are an existing file name)
                list of GIFTI surfaces
        gpickled_networks: (a list of items which are an existing file name)
                list of gpickled Networkx graphs
        graphml_networks: (a list of items which are an existing file name)
                list of graphML networks
        ignore_exception: (a boolean, nipype default value: False)
                Print an error message instead of throwing an exception in case the
                interface fails to run
        license: (a unicode string)
                License
        nifti_volumes: (a list of items which are an existing file name)
                list of NIFTI volumes
        out_file: (a file name, nipype default value: connectome.cff)
                Output connectome file
        publisher: (a unicode string)
                Publisher
        references: (a unicode string)
                References
        relation: (a unicode string)
                Relation
        rights: (a unicode string)
                Rights
        script_files: (a list of items which are an existing file name)
                list of script files to include
        species: (a unicode string, nipype default value: Homo sapiens)
                Species
        timeseries_files: (a list of items which are an existing file name)
                list of HDF5 timeseries files
        title: (a unicode string)
                Connectome Title
        tract_files: (a list of items which are an existing file name)
                list of Trackvis fiber files

Outputs::

        connectome_file: (an existing file name)
                Output connectome file

.. _nipype.interfaces.cmtk.convert.MergeCNetworks:


.. index:: MergeCNetworks

MergeCNetworks
--------------

`Link to code <http://github.com/nipy/nipype/tree/ec86b7476/nipype/interfaces/cmtk/convert.py#L219>`__

Merges networks from multiple CFF files into one new CFF file.

Example
~~~~~~~

>>> import nipype.interfaces.cmtk as cmtk
>>> mrg = cmtk.MergeCNetworks()
>>> mrg.inputs.in_files = ['subj1.cff','subj2.cff']
>>> mrg.run()                  # doctest: +SKIP

Inputs::

        [Mandatory]
        in_files: (a list of items which are an existing file name)
                List of CFF files to extract networks from

        [Optional]
        ignore_exception: (a boolean, nipype default value: False)
                Print an error message instead of throwing an exception in case the
                interface fails to run
        out_file: (a file name, nipype default value:
                 merged_network_connectome.cff)
                Output CFF file with all the networks added

Outputs::

        connectome_file: (an existing file name)
                Output CFF file with all the networks added
