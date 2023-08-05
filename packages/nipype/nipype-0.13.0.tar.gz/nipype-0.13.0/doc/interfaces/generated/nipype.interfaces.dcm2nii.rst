.. AUTO-GENERATED FILE -- DO NOT EDIT!

interfaces.dcm2nii
==================


.. _nipype.interfaces.dcm2nii.Dcm2nii:


.. index:: Dcm2nii

Dcm2nii
-------

`Link to code <http://github.com/nipy/nipype/tree/ec86b7476/nipype/interfaces/dcm2nii.py#L67>`__

Wraps command **dcm2nii**

Uses MRIcron's dcm2nii to convert dicom files

Examples
~~~~~~~~

>>> from nipype.interfaces.dcm2nii import Dcm2nii
>>> converter = Dcm2nii()
>>> converter.inputs.source_names = ['functional_1.dcm', 'functional_2.dcm']
>>> converter.inputs.gzip_output = True
>>> converter.inputs.output_dir = '.'
>>> converter.cmdline # doctest: +ALLOW_UNICODE
'dcm2nii -a y -c y -b config.ini -v y -d y -e y -g y -i n -n y -o . -p y -x n -f n functional_1.dcm'

Inputs::

        [Mandatory]
        source_dir: (an existing directory name)
                flag: %s, position: -1
                mutually_exclusive: source_names
        source_names: (a list of items which are an existing file name)
                flag: %s, position: -1
                mutually_exclusive: source_dir

        [Optional]
        anonymize: (a boolean, nipype default value: True)
                Remove identifying information
                flag: -a
        args: (a unicode string)
                Additional parameters to the command
                flag: %s
        collapse_folders: (a boolean, nipype default value: True)
                Collapse input folders
                flag: -c
        config_file: (an existing file name)
                Load settings from specified inifile
                flag: -b %s
        convert_all_pars: (a boolean, nipype default value: True)
                Convert every image in directory
                flag: -v
        date_in_filename: (a boolean, nipype default value: True)
                Date in filename
                flag: -d
        environ: (a dictionary with keys which are a bytes or None or a value
                 of class 'str' and with values which are a bytes or None or a value
                 of class 'str', nipype default value: {})
                Environment variables
        events_in_filename: (a boolean, nipype default value: True)
                Events (series/acq) in filename
                flag: -e
        gzip_output: (a boolean, nipype default value: False)
                Gzip output (.gz)
                flag: -g
        id_in_filename: (a boolean, nipype default value: False)
                ID in filename
                flag: -i
        ignore_exception: (a boolean, nipype default value: False)
                Print an error message instead of throwing an exception in case the
                interface fails to run
        nii_output: (a boolean, nipype default value: True)
                Save as .nii - if no, create .hdr/.img pair
                flag: -n
        output_dir: (an existing directory name)
                Output dir - if unspecified, source directory is used
                flag: -o %s
        protocol_in_filename: (a boolean, nipype default value: True)
                Protocol in filename
                flag: -p
        reorient: (a boolean)
                Reorient image to nearest orthogonal
                flag: -r
        reorient_and_crop: (a boolean, nipype default value: False)
                Reorient and crop 3D images
                flag: -x
        source_in_filename: (a boolean, nipype default value: False)
                Source filename
                flag: -f
        spm_analyze: (a boolean)
                SPM2/Analyze not SPM5/NIfTI
                flag: -s
                mutually_exclusive: nii_output
        terminal_output: ('stream' or 'allatonce' or 'file' or 'none')
                Control terminal output: `stream` - displays to terminal immediately
                (default), `allatonce` - waits till command is finished to display
                output, `file` - writes output to file, `none` - output is ignored

Outputs::

        bvals: (a list of items which are an existing file name)
        bvecs: (a list of items which are an existing file name)
        converted_files: (a list of items which are an existing file name)
        reoriented_and_cropped_files: (a list of items which are an existing
                 file name)
        reoriented_files: (a list of items which are an existing file name)

.. _nipype.interfaces.dcm2nii.Dcm2niix:


.. index:: Dcm2niix

Dcm2niix
--------

`Link to code <http://github.com/nipy/nipype/tree/ec86b7476/nipype/interfaces/dcm2nii.py#L237>`__

Wraps command **dcm2niix**

Uses Chris Rorden's dcm2niix to convert dicom files

Examples
~~~~~~~~

>>> from nipype.interfaces.dcm2nii import Dcm2niix
>>> converter = Dcm2niix()
>>> converter.inputs.source_names = ['functional_1.dcm', 'functional_2.dcm']
>>> converter.inputs.compress = 'i'
>>> converter.inputs.single_file = True
>>> converter.inputs.output_dir = '.'
>>> converter.cmdline # doctest: +SKIP
'dcm2niix -b y -z i -x n -t n -m n -f %t%p -o . -s y -v n functional_1.dcm'

>>> flags = '-'.join([val.strip() + ' ' for val in sorted(' '.join(converter.cmdline.split()[1:-1]).split('-'))])
>>> flags # doctest: +ALLOW_UNICODE
' -b y -f %t%p -m n -o . -s y -t n -v n -x n -z i '

Inputs::

        [Mandatory]
        source_dir: (an existing directory name)
                flag: %s, position: -1
                mutually_exclusive: source_names
        source_names: (a list of items which are an existing file name)
                flag: %s, position: -1
                mutually_exclusive: source_dir

        [Optional]
        args: (a unicode string)
                Additional parameters to the command
                flag: %s
        bids_format: (a boolean, nipype default value: True)
                Create a BIDS sidecar file
                flag: -b
        compress: ('y' or 'i' or 'n', nipype default value: i)
                Gzip compress images - [y=pigz, i=internal, n=no]
                flag: -z %s
        crop: (a boolean, nipype default value: False)
                Crop 3D T1 acquisitions
                flag: -x
        environ: (a dictionary with keys which are a bytes or None or a value
                 of class 'str' and with values which are a bytes or None or a value
                 of class 'str', nipype default value: {})
                Environment variables
        has_private: (a boolean, nipype default value: False)
                Flag if text notes includes private patient details
                flag: -t
        ignore_exception: (a boolean, nipype default value: False)
                Print an error message instead of throwing an exception in case the
                interface fails to run
        merge_imgs: (a boolean, nipype default value: False)
                merge 2D slices from same series
                flag: -m
        out_filename: (a unicode string, nipype default value: %t%p)
                Output filename
                flag: -f %s
        output_dir: (an existing directory name)
                Output directory
                flag: -o %s
        single_file: (a boolean, nipype default value: False)
                Convert only one image (filename as last input
                flag: -s
        terminal_output: ('stream' or 'allatonce' or 'file' or 'none')
                Control terminal output: `stream` - displays to terminal immediately
                (default), `allatonce` - waits till command is finished to display
                output, `file` - writes output to file, `none` - output is ignored
        verbose: (a boolean, nipype default value: False)
                Verbose output
                flag: -v

Outputs::

        bids: (a list of items which are an existing file name)
        bvals: (a list of items which are an existing file name)
        bvecs: (a list of items which are an existing file name)
        converted_files: (a list of items which are an existing file name)
