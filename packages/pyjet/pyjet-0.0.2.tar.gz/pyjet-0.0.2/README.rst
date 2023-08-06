.. -*- mode: rst -*-

pyjet: The interface between FastJet and NumPy
==============================================

WORK IN PROGESS

pyjet allows you to perform jet clustering with `FastJet <http://fastjet.fr/>`_
on `NumPy <http://www.numpy.org/>`_ arrays.

By default pyjet only depends on NumPy and internally uses FastJet's standalone
fjcore release.

Installation::

   pip install --user pyjet

Get example.py and run it::

	curl -O https://raw.githubusercontent.com/ndawe/pyjet/master/example.py
	python example.py
	jet#          pT        eta        phi       mass
	0        983.280     -0.868      2.905     36.457
	1        901.745      0.221     -0.252     51.850
	2         67.994     -1.194     -0.200     11.984
	3         12.465      0.433      0.673      5.461
	4          6.568     -2.629      1.133      2.099
	5          6.498     -1.828     -2.248      3.309
