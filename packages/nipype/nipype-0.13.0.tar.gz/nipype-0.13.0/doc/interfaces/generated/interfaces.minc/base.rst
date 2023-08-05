.. AUTO-GENERATED FILE -- DO NOT EDIT!

interfaces.minc.base
====================


.. module:: nipype.interfaces.minc.base


.. _nipype.interfaces.minc.base.aggregate_filename:

:func:`aggregate_filename`
--------------------------

`Link to code <http://github.com/nipy/nipype/tree/ec86b7476/nipype/interfaces/minc/base.py#L101>`__



Try to work out a sensible name given a set of files that have
been combined in some way (e.g. averaged). If we can't work out a
sensible prefix, we use the first filename in the list.

Examples
~~~~~~~~

>>> from nipype.interfaces.minc.base import aggregate_filename
>>> f = aggregate_filename(['/tmp/foo1.mnc', '/tmp/foo2.mnc', '/tmp/foo3.mnc'], 'averaged')
>>> os.path.split(f)[1] # This has a full path, so just check the filename. # doctest: +ALLOW_UNICODE
'foo_averaged.mnc'

>>> f = aggregate_filename(['/tmp/foo1.mnc', '/tmp/blah1.mnc'], 'averaged')
>>> os.path.split(f)[1] # This has a full path, so just check the filename. # doctest: +ALLOW_UNICODE
'foo1_averaged.mnc'

