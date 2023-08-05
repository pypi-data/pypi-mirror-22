.. AUTO-GENERATED FILE -- DO NOT EDIT!

interfaces.utility.csv
======================


.. _nipype.interfaces.utility.csv.CSVReader:


.. index:: CSVReader

CSVReader
---------

`Link to code <http://github.com/nipy/nipype/tree/ec86b7476/nipype/interfaces/utility/csv.py#L29>`__

Examples
~~~~~~~~

>>> reader = CSVReader()  # doctest: +SKIP
>>> reader.inputs.in_file = 'noHeader.csv'  # doctest: +SKIP
>>> out = reader.run()  # doctest: +SKIP
>>> out.outputs.column_0 == ['foo', 'bar', 'baz']  # doctest: +SKIP
True
>>> out.outputs.column_1 == ['hello', 'world', 'goodbye']  # doctest: +SKIP
True
>>> out.outputs.column_2 == ['300.1', '5', '0.3']  # doctest: +SKIP
True

>>> reader = CSVReader()  # doctest: +SKIP
>>> reader.inputs.in_file = 'header.csv'  # doctest: +SKIP
>>> reader.inputs.header = True  # doctest: +SKIP
>>> out = reader.run()  # doctest: +SKIP
>>> out.outputs.files == ['foo', 'bar', 'baz']  # doctest: +SKIP
True
>>> out.outputs.labels == ['hello', 'world', 'goodbye']  # doctest: +SKIP
True
>>> out.outputs.erosion == ['300.1', '5', '0.3']  # doctest: +SKIP
True

Inputs::

        [Mandatory]
        in_file: (an existing file name)
                Input comma-seperated value (CSV) file

        [Optional]
        header: (a boolean, nipype default value: False)
                True if the first line is a column header

Outputs::

        None
