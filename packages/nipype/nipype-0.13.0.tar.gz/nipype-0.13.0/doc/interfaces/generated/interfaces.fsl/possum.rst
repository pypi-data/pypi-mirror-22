.. AUTO-GENERATED FILE -- DO NOT EDIT!

interfaces.fsl.possum
=====================


.. _nipype.interfaces.fsl.possum.B0Calc:


.. index:: B0Calc

B0Calc
------

`Link to code <http://github.com/nipy/nipype/tree/ec86b7476/nipype/interfaces/fsl/possum.py#L67>`__

Wraps command **b0calc**

B0 inhomogeneities occur at interfaces of materials with different magnetic susceptibilities,
such as tissue-air interfaces. These differences lead to distortion in the local magnetic field,
as Maxwell’s equations need to be satisfied. An example of B0 inhomogneity is the first volume
of the 4D volume ```$FSLDIR/data/possum/b0_ppm.nii.gz```.

Examples
~~~~~~~~

>>> from nipype.interfaces.fsl import B0Calc
>>> b0calc = B0Calc()
>>> b0calc.inputs.in_file = 'tissue+air_map.nii'
>>> b0calc.inputs.z_b0 = 3.0
>>> b0calc.inputs.output_type = "NIFTI_GZ"
>>> b0calc.cmdline  # doctest: +ALLOW_UNICODE
'b0calc -i tissue+air_map.nii -o tissue+air_map_b0field.nii.gz --b0=3.00'

Inputs::

        [Mandatory]
        in_file: (an existing file name)
                filename of input image (usually a tissue/air segmentation)
                flag: -i %s, position: 0

        [Optional]
        args: (a unicode string)
                Additional parameters to the command
                flag: %s
        chi_air: (a float)
                susceptibility of air
                flag: --chi0=%e
        compute_xyz: (a boolean)
                calculate and save all 3 field components (i.e. x,y,z)
                flag: --xyz
        delta: (a float)
                Delta value (chi_tissue - chi_air)
                flag: -d %e
        directconv: (a boolean)
                use direct (image space) convolution, not FFT
                flag: --directconv
        environ: (a dictionary with keys which are a bytes or None or a value
                 of class 'str' and with values which are a bytes or None or a value
                 of class 'str', nipype default value: {})
                Environment variables
        extendboundary: (a float)
                Relative proportion to extend voxels at boundary
                flag: --extendboundary=%0.2f
        ignore_exception: (a boolean, nipype default value: False)
                Print an error message instead of throwing an exception in case the
                interface fails to run
        out_file: (a file name)
                filename of B0 output volume
                flag: -o %s, position: 1
        output_type: ('NIFTI' or 'NIFTI_PAIR' or 'NIFTI_GZ' or
                 'NIFTI_PAIR_GZ')
                FSL output type
        terminal_output: ('stream' or 'allatonce' or 'file' or 'none')
                Control terminal output: `stream` - displays to terminal immediately
                (default), `allatonce` - waits till command is finished to display
                output, `file` - writes output to file, `none` - output is ignored
        x_b0: (a float)
                Value for zeroth-order b0 field (x-component), in Tesla
                flag: --b0x=%0.2f
                mutually_exclusive: xyz_b0
        x_grad: (a float)
                Value for zeroth-order x-gradient field (per mm)
                flag: --gx=%0.4f
        xyz_b0: (a tuple of the form: (a float, a float, a float))
                Zeroth-order B0 field in Tesla
                flag: --b0x=%0.2f --b0y=%0.2f --b0=%0.2f
                mutually_exclusive: x_b0, y_b0, z_b0
        y_b0: (a float)
                Value for zeroth-order b0 field (y-component), in Tesla
                flag: --b0y=%0.2f
                mutually_exclusive: xyz_b0
        y_grad: (a float)
                Value for zeroth-order y-gradient field (per mm)
                flag: --gy=%0.4f
        z_b0: (a float)
                Value for zeroth-order b0 field (z-component), in Tesla
                flag: --b0=%0.2f
                mutually_exclusive: xyz_b0
        z_grad: (a float)
                Value for zeroth-order z-gradient field (per mm)
                flag: --gz=%0.4f

Outputs::

        out_file: (an existing file name)
                filename of B0 output volume

References::
None
