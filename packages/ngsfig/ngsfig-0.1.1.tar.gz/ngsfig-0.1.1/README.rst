
============================
NGSfig
============================


Example: Legoplot in NGSfig
----------------------------------

.. code-block:: python

  import warnings
  from pkg_resources import get_distribution, resource_stream, Requirement
  from ngsfig.graphics import trinucleotide

  with resource_stream(Requirement.parse("ngsfig"), "data/trinucleotide_demo.txt") as input:
    trinucleotide.demo(input)

Run this script or paste it into a Python console.


.. class:: no-web

  .. image:: https://raw.githubusercontent.com/xiaobeizhao/ngsfigpy/master/data/trinucleotide_demo.png
    :alt: NGSfig | Legoplot
    :width: 100%
    :align: center

.. class:: no-web no-pdf

           
Download and Install
--------------------
* `GitHub (beta) <https://github.com/xiaobeizhao/ngsfigpy>`
* `PyPI <https://pypi.python.org/pypi/ngsfig>`

  
Dependencies
------------
* `nose <https://pypi.python.org/pypi/nose>`
* `setuptools>=33.1.1 <https://pypi.python.org/pypi/setuptools/33.1.1>`
* `numpy>=1.11.3 <https://pypi.python.org/pypi/numpy/1.11.3>`
* `pandas>=0.19.2 <https://pypi.python.org/pypi/pandas/0.19.2>`
* `tabulate>=0.7.5 <https://pypi.python.org/pypi/tabulate/0.7.5>`
* `matplotlib>=2.0.0 <https://pypi.python.org/pypi/matplotlib/2.0.0>`
* `xmisc (beta) <https://github.com/xiaobeizhao/xmiscpy>`
* `xmisc <https://pypi.python.org/pypi/xmisc>`

  
License
-------
Code and documentation are available according to the GNU LGPL License.


