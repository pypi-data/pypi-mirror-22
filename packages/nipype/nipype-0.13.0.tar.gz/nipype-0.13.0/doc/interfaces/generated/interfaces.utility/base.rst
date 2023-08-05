.. AUTO-GENERATED FILE -- DO NOT EDIT!

interfaces.utility.base
=======================


.. _nipype.interfaces.utility.base.AssertEqual:


.. index:: AssertEqual

AssertEqual
-----------

`Link to code <http://github.com/nipy/nipype/tree/ec86b7476/nipype/interfaces/utility/base.py#L403>`__

Inputs::

        [Mandatory]
        volume1: (an existing file name)
        volume2: (an existing file name)

        [Optional]
        ignore_exception: (a boolean, nipype default value: False)
                Print an error message instead of throwing an exception in case the
                interface fails to run

Outputs::

        None

.. _nipype.interfaces.utility.base.IdentityInterface:


.. index:: IdentityInterface

IdentityInterface
-----------------

`Link to code <http://github.com/nipy/nipype/tree/ec86b7476/nipype/interfaces/utility/base.py#L33>`__

Basic interface class generates identity mappings

Examples
~~~~~~~~

>>> from nipype.interfaces.utility import IdentityInterface
>>> ii = IdentityInterface(fields=['a', 'b'], mandatory_inputs=False)
>>> ii.inputs.a
<undefined>

>>> ii.inputs.a = 'foo'
>>> out = ii._outputs()
>>> out.a
<undefined>

>>> out = ii.run()
>>> out.outputs.a # doctest: +ALLOW_UNICODE
'foo'

>>> ii2 = IdentityInterface(fields=['a', 'b'], mandatory_inputs=True)
>>> ii2.inputs.a = 'foo'
>>> out = ii2.run() # doctest: +SKIP
ValueError: IdentityInterface requires a value for input 'b' because it was listed in 'fields' Interface IdentityInterface failed to run.

Inputs::

        None

Outputs::

        None

.. _nipype.interfaces.utility.base.Merge:


.. index:: Merge

Merge
-----

`Link to code <http://github.com/nipy/nipype/tree/ec86b7476/nipype/interfaces/utility/base.py#L125>`__

Basic interface class to merge inputs into a single list

``Merge(1)`` will merge a list of lists

Examples
~~~~~~~~

>>> from nipype.interfaces.utility import Merge
>>> mi = Merge(3)
>>> mi.inputs.in1 = 1
>>> mi.inputs.in2 = [2, 5]
>>> mi.inputs.in3 = 3
>>> out = mi.run()
>>> out.outputs.out
[1, 2, 5, 3]

>>> merge = Merge(1)
>>> merge.inputs.in1 = [1, [2, 5], 3]
>>> out = merge.run()
>>> out.outputs.out
[1, [2, 5], 3]

>>> merge = Merge(1)
>>> merge.inputs.in1 = [1, [2, 5], 3]
>>> merge.inputs.ravel_inputs = True
>>> out = merge.run()
>>> out.outputs.out
[1, 2, 5, 3]

>>> merge = Merge(1)
>>> merge.inputs.in1 = [1, [2, 5], 3]
>>> merge.inputs.no_flatten = True
>>> out = merge.run()
>>> out.outputs.out
[[1, [2, 5], 3]]

Inputs::

        [Mandatory]

        [Optional]
        axis: ('vstack' or 'hstack', nipype default value: vstack)
                direction in which to merge, hstack requires same number of elements
                in each input
        ignore_exception: (a boolean, nipype default value: False)
                Print an error message instead of throwing an exception in case the
                interface fails to run
        no_flatten: (a boolean, nipype default value: False)
                append to outlist instead of extending in vstack mode
        ravel_inputs: (a boolean, nipype default value: False)
                ravel inputs when no_flatten is False

Outputs::

        out: (a list of items which are any value)
                Merged output

.. _nipype.interfaces.utility.base.Rename:


.. index:: Rename

Rename
------

`Link to code <http://github.com/nipy/nipype/tree/ec86b7476/nipype/interfaces/utility/base.py#L217>`__

Change the name of a file based on a mapped format string.

To use additional inputs that will be defined at run-time, the class
constructor must be called with the format template, and the fields
identified will become inputs to the interface.

Additionally, you may set the parse_string input, which will be run
over the input filename with a regular expressions search, and will
fill in additional input fields from matched groups. Fields set with
inputs have precedence over fields filled in with the regexp match.

Examples
~~~~~~~~

>>> from nipype.interfaces.utility import Rename
>>> rename1 = Rename()
>>> rename1.inputs.in_file = "zstat1.nii.gz"
>>> rename1.inputs.format_string = "Faces-Scenes.nii.gz"
>>> res = rename1.run()          # doctest: +SKIP
>>> res.outputs.out_file         # doctest: +SKIP
'Faces-Scenes.nii.gz"            # doctest: +SKIP

>>> rename2 = Rename(format_string="%(subject_id)s_func_run%(run)02d")
>>> rename2.inputs.in_file = "functional.nii"
>>> rename2.inputs.keep_ext = True
>>> rename2.inputs.subject_id = "subj_201"
>>> rename2.inputs.run = 2
>>> res = rename2.run()          # doctest: +SKIP
>>> res.outputs.out_file         # doctest: +SKIP
'subj_201_func_run02.nii'        # doctest: +SKIP

>>> rename3 = Rename(format_string="%(subject_id)s_%(seq)s_run%(run)02d.nii")
>>> rename3.inputs.in_file = "func_epi_1_1.nii"
>>> rename3.inputs.parse_string = "func_(?P<seq>\w*)_.*"
>>> rename3.inputs.subject_id = "subj_201"
>>> rename3.inputs.run = 2
>>> res = rename3.run()          # doctest: +SKIP
>>> res.outputs.out_file         # doctest: +SKIP
'subj_201_epi_run02.nii'         # doctest: +SKIP

Inputs::

        [Mandatory]
        format_string: (a unicode string)
                Python formatting string for output template
        in_file: (an existing file name)
                file to rename

        [Optional]
        keep_ext: (a boolean)
                Keep in_file extension, replace non-extension component of name
        parse_string: (a unicode string)
                Python regexp parse string to define replacement inputs
        use_fullpath: (a boolean, nipype default value: False)
                Use full path as input to regex parser

Outputs::

        out_file: (a file name)
                softlink to original file with new name

.. _nipype.interfaces.utility.base.Select:


.. index:: Select

Select
------

`Link to code <http://github.com/nipy/nipype/tree/ec86b7476/nipype/interfaces/utility/base.py#L368>`__

Basic interface class to select specific elements from a list

Examples
~~~~~~~~

>>> from nipype.interfaces.utility import Select
>>> sl = Select()
>>> _ = sl.inputs.set(inlist=[1, 2, 3, 4, 5], index=[3])
>>> out = sl.run()
>>> out.outputs.out
~

>>> _ = sl.inputs.set(inlist=[1, 2, 3, 4, 5], index=[3, 4])
>>> out = sl.run()
>>> out.outputs.out
[4, 5]

Inputs::

        [Mandatory]
        index: (a list of items which are an integer (int or long))
                0-based indices of values to choose
        inlist: (a list of items which are any value)
                list of values to choose from

        [Optional]
        ignore_exception: (a boolean, nipype default value: False)
                Print an error message instead of throwing an exception in case the
                interface fails to run

Outputs::

        out: (a list of items which are any value)
                list of selected values

.. _nipype.interfaces.utility.base.Split:


.. index:: Split

Split
-----

`Link to code <http://github.com/nipy/nipype/tree/ec86b7476/nipype/interfaces/utility/base.py#L314>`__

Basic interface class to split lists into multiple outputs

Examples
~~~~~~~~

>>> from nipype.interfaces.utility import Split
>>> sp = Split()
>>> _ = sp.inputs.set(inlist=[1, 2, 3], splits=[2, 1])
>>> out = sp.run()
>>> out.outputs.out1
[1, 2]

Inputs::

        [Mandatory]
        inlist: (a list of items which are any value)
                list of values to split
        splits: (a list of items which are an integer (int or long))
                Number of outputs in each split - should add to number of inputs

        [Optional]
        ignore_exception: (a boolean, nipype default value: False)
                Print an error message instead of throwing an exception in case the
                interface fails to run
        squeeze: (a boolean, nipype default value: False)
                unfold one-element splits removing the list

Outputs::

        None
