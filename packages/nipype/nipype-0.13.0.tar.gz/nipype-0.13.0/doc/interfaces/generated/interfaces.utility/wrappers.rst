.. AUTO-GENERATED FILE -- DO NOT EDIT!

interfaces.utility.wrappers
===========================


.. _nipype.interfaces.utility.wrappers.Function:


.. index:: Function

Function
--------

`Link to code <http://github.com/nipy/nipype/tree/ec86b7476/nipype/interfaces/utility/wrappers.py#L43>`__

Runs arbitrary function as an interface

Examples
~~~~~~~~

>>> func = 'def func(arg1, arg2=5): return arg1 + arg2'
>>> fi = Function(input_names=['arg1', 'arg2'], output_names=['out'])
>>> fi.inputs.function_str = func
>>> res = fi.run(arg1=1)
>>> res.outputs.out
~

Inputs::

        [Mandatory]
        function_str: (a unicode string)
                code for function

        [Optional]
        ignore_exception: (a boolean, nipype default value: False)
                Print an error message instead of throwing an exception in case the
                interface fails to run

Outputs::

        None
