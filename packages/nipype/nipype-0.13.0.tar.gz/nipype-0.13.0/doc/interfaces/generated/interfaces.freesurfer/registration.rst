.. AUTO-GENERATED FILE -- DO NOT EDIT!

interfaces.freesurfer.registration
==================================


.. _nipype.interfaces.freesurfer.registration.EMRegister:


.. index:: EMRegister

EMRegister
----------

`Link to code <http://github.com/nipy/nipype/tree/ec86b7476/nipype/interfaces/freesurfer/registration.py#L195>`__

Wraps command **mri_em_register**

This program creates a tranform in lta format

Examples
~~~~~~~~
>>> from nipype.interfaces.freesurfer import EMRegister
>>> register = EMRegister()
>>> register.inputs.in_file = 'norm.mgz'
>>> register.inputs.template = 'aseg.mgz'
>>> register.inputs.out_file = 'norm_transform.lta'
>>> register.inputs.skull = True
>>> register.inputs.nbrspacing = 9
>>> register.cmdline # doctest: +ALLOW_UNICODE
'mri_em_register -uns 9 -skull norm.mgz aseg.mgz norm_transform.lta'

Inputs::

        [Mandatory]
        in_file: (an existing file name)
                in brain volume
                flag: %s, position: -3
        template: (an existing file name)
                template gca
                flag: %s, position: -2

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
        mask: (an existing file name)
                use volume as a mask
                flag: -mask %s
        nbrspacing: (an integer (int or long))
                align to atlas containing skull setting unknown_nbr_spacing =
                nbrspacing
                flag: -uns %d
        num_threads: (an integer (int or long))
                allows for specifying more threads
        out_file: (a file name)
                output transform
                flag: %s, position: -1
        skull: (a boolean)
                align to atlas containing skull (uns=5)
                flag: -skull
        subjects_dir: (an existing directory name)
                subjects directory
        terminal_output: ('stream' or 'allatonce' or 'file' or 'none')
                Control terminal output: `stream` - displays to terminal immediately
                (default), `allatonce` - waits till command is finished to display
                output, `file` - writes output to file, `none` - output is ignored
        transform: (an existing file name)
                Previously computed transform
                flag: -t %s

Outputs::

        out_file: (a file name)
                output transform

.. _nipype.interfaces.freesurfer.registration.MPRtoMNI305:


.. index:: MPRtoMNI305

MPRtoMNI305
-----------

`Link to code <http://github.com/nipy/nipype/tree/ec86b7476/nipype/interfaces/freesurfer/registration.py#L50>`__

Wraps command **mpr2mni305**

For complete details, see FreeSurfer documentation

Examples
~~~~~~~~

>>> from nipype.interfaces.freesurfer import MPRtoMNI305, Info
>>> mprtomni305 = MPRtoMNI305()
>>> mprtomni305.inputs.target = 'structural.nii'
>>> mprtomni305.inputs.reference_dir = '.' # doctest: +SKIP
>>> mprtomni305.cmdline # doctest: +SKIP
'mpr2mni305 output'
>>> mprtomni305.inputs.out_file = 'struct_out' # doctest: +SKIP
>>> mprtomni305.cmdline # doctest: +SKIP
'mpr2mni305 struct_out' # doctest: +SKIP
>>> mprtomni305.inputs.environ['REFDIR'] == os.path.join(Info.home(), 'average') # doctest: +SKIP
True
>>> mprtomni305.inputs.environ['MPR2MNI305_TARGET'] # doctest: +SKIP
'structural'
>>> mprtomni305.run() # doctest: +SKIP

Inputs::

        [Mandatory]
        reference_dir: (an existing directory name, nipype default value: )
                TODO
        target: (a string, nipype default value: )
                input atlas file

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
        in_file: (a file name, nipype default value: )
                the input file prefix for MPRtoMNI305
                flag: %s
        subjects_dir: (an existing directory name)
                subjects directory
        terminal_output: ('stream' or 'allatonce' or 'file' or 'none')
                Control terminal output: `stream` - displays to terminal immediately
                (default), `allatonce` - waits till command is finished to display
                output, `file` - writes output to file, `none` - output is ignored

Outputs::

        log_file: (an existing file name, nipype default value:
                 stdout.nipype)
                The output log
        out_file: (a file name)
                The output file '<in_file>_to_<target>_t4_vox2vox.txt'

.. _nipype.interfaces.freesurfer.registration.Paint:


.. index:: Paint

Paint
-----

`Link to code <http://github.com/nipy/nipype/tree/ec86b7476/nipype/interfaces/freesurfer/registration.py#L307>`__

Wraps command **mrisp_paint**

This program is useful for extracting one of the arrays ("a variable")
from a surface-registration template file. The output is a file
containing a surface-worth of per-vertex values, saved in "curvature"
format. Because the template data is sampled to a particular surface
mesh, this conjures the idea of "painting to a surface".

Examples
~~~~~~~~
>>> from nipype.interfaces.freesurfer import Paint
>>> paint = Paint()
>>> paint.inputs.in_surf = 'lh.pial'
>>> paint.inputs.template = 'aseg.mgz'
>>> paint.inputs.averages = 5
>>> paint.inputs.out_file = 'lh.avg_curv'
>>> paint.cmdline # doctest: +ALLOW_UNICODE
'mrisp_paint -a 5 aseg.mgz lh.pial lh.avg_curv'

Inputs::

        [Mandatory]
        in_surf: (an existing file name)
                Surface file with grid (vertices) onto which the template data is to
                be sampled or 'painted'
                flag: %s, position: -2
        template: (an existing file name)
                Template file
                flag: %s, position: -3

        [Optional]
        args: (a unicode string)
                Additional parameters to the command
                flag: %s
        averages: (an integer (int or long))
                Average curvature patterns
                flag: -a %d
        environ: (a dictionary with keys which are a bytes or None or a value
                 of class 'str' and with values which are a bytes or None or a value
                 of class 'str', nipype default value: {})
                Environment variables
        ignore_exception: (a boolean, nipype default value: False)
                Print an error message instead of throwing an exception in case the
                interface fails to run
        out_file: (a file name)
                File containing a surface-worth of per-vertex values, saved in
                'curvature' format.
                flag: %s, position: -1
        subjects_dir: (an existing directory name)
                subjects directory
        template_param: (an integer (int or long))
                Frame number of the input template
        terminal_output: ('stream' or 'allatonce' or 'file' or 'none')
                Control terminal output: `stream` - displays to terminal immediately
                (default), `allatonce` - waits till command is finished to display
                output, `file` - writes output to file, `none` - output is ignored

Outputs::

        out_file: (a file name)
                File containing a surface-worth of per-vertex values, saved in
                'curvature' format.

.. _nipype.interfaces.freesurfer.registration.Register:


.. index:: Register

Register
--------

`Link to code <http://github.com/nipy/nipype/tree/ec86b7476/nipype/interfaces/freesurfer/registration.py#L244>`__

Wraps command **mris_register**

This program registers a surface to an average surface template.

Examples
~~~~~~~~
>>> from nipype.interfaces.freesurfer import Register
>>> register = Register()
>>> register.inputs.in_surf = 'lh.pial'
>>> register.inputs.in_smoothwm = 'lh.pial'
>>> register.inputs.in_sulc = 'lh.pial'
>>> register.inputs.target = 'aseg.mgz'
>>> register.inputs.out_file = 'lh.pial.reg'
>>> register.inputs.curv = True
>>> register.cmdline # doctest: +ALLOW_UNICODE
'mris_register -curv lh.pial aseg.mgz lh.pial.reg'

Inputs::

        [Mandatory]
        in_sulc: (an existing file name)
                Undocumented mandatory input file
                ${SUBJECTS_DIR}/surf/{hemisphere}.sulc
        in_surf: (an existing file name)
                Surface to register, often {hemi}.sphere
                flag: %s, position: -3
        target: (an existing file name)
                The data to register to. In normal recon-all usage, this is a
                template file for average surface.
                flag: %s, position: -2

        [Optional]
        args: (a unicode string)
                Additional parameters to the command
                flag: %s
        curv: (a boolean)
                Use smoothwm curvature for final alignment
                flag: -curv
                requires: in_smoothwm
        environ: (a dictionary with keys which are a bytes or None or a value
                 of class 'str' and with values which are a bytes or None or a value
                 of class 'str', nipype default value: {})
                Environment variables
        ignore_exception: (a boolean, nipype default value: False)
                Print an error message instead of throwing an exception in case the
                interface fails to run
        in_smoothwm: (an existing file name)
                Undocumented input file ${SUBJECTS_DIR}/surf/{hemisphere}.smoothwm
        out_file: (a file name)
                Output surface file to capture registration
                flag: %s, position: -1
        subjects_dir: (an existing directory name)
                subjects directory
        terminal_output: ('stream' or 'allatonce' or 'file' or 'none')
                Control terminal output: `stream` - displays to terminal immediately
                (default), `allatonce` - waits till command is finished to display
                output, `file` - writes output to file, `none` - output is ignored

Outputs::

        out_file: (a file name)
                Output surface file to capture registration

.. _nipype.interfaces.freesurfer.registration.RegisterAVItoTalairach:


.. index:: RegisterAVItoTalairach

RegisterAVItoTalairach
----------------------

`Link to code <http://github.com/nipy/nipype/tree/ec86b7476/nipype/interfaces/freesurfer/registration.py#L128>`__

Wraps command **avi2talxfm**

converts the vox2vox from talairach_avi to a talairach.xfm file

This is a script that converts the vox2vox from talairach_avi to a
talairach.xfm file. It is meant to replace the following cmd line:

tkregister2_cmdl         --mov $InVol         --targ $FREESURFER_HOME/average/mni305.cor.mgz         --xfmout ${XFM}         --vox2vox talsrcimg_to_${target}_t4_vox2vox.txt         --noedit         --reg talsrcimg.reg.tmp.dat
set targ = $FREESURFER_HOME/average/mni305.cor.mgz
set subject = mgh-02407836-v2
set InVol = $SUBJECTS_DIR/$subject/mri/orig.mgz
set vox2vox = $SUBJECTS_DIR/$subject/mri/transforms/talsrcimg_to_711-2C_as_mni_average_305_t4_vox2vox.txt

Examples
~~~~~~~~

>>> from nipype.interfaces.freesurfer import RegisterAVItoTalairach
>>> register = RegisterAVItoTalairach()
>>> register.inputs.in_file = 'structural.mgz'                         # doctest: +SKIP
>>> register.inputs.target = 'mni305.cor.mgz'                          # doctest: +SKIP
>>> register.inputs.vox2vox = 'talsrcimg_to_structural_t4_vox2vox.txt' # doctest: +SKIP
>>> register.cmdline                                                   # doctest: +SKIP
'avi2talxfm structural.mgz mni305.cor.mgz talsrcimg_to_structural_t4_vox2vox.txt talairach.auto.xfm'

>>> register.run() # doctest: +SKIP

Inputs::

        [Mandatory]
        in_file: (an existing file name)
                The input file
                flag: %s, position: 0
        target: (an existing file name)
                The target file
                flag: %s, position: 1
        vox2vox: (an existing file name)
                The vox2vox file
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
        out_file: (a file name, nipype default value: talairach.auto.xfm)
                The transform output
                flag: %s, position: 3
        subjects_dir: (an existing directory name)
                subjects directory
        terminal_output: ('stream' or 'allatonce' or 'file' or 'none')
                Control terminal output: `stream` - displays to terminal immediately
                (default), `allatonce` - waits till command is finished to display
                output, `file` - writes output to file, `none` - output is ignored

Outputs::

        log_file: (an existing file name, nipype default value:
                 stdout.nipype)
                The output log
        out_file: (a file name)
                The output file for RegisterAVItoTalairach
