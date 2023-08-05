pyfpdf: FPDF for Python
=======================

PyFPDF is a library for PDF document generation under Python, ported
from PHP (see `FPDF <http://www.fpdf.org/>`__: "Free"-PDF, a well-known
PDFlib-extension replacement with many examples, scripts and
derivatives).

Compared with other PDF libraries, PyFPDF is simple, small and
versatile, with advanced capabilities, and is easy to learn, extend and
maintain.

THIS VERSION IS AN UPDATED VERSION OF THE PYPI 'fpdf' PACKAGE.

Features:
---------

-  Python 2.5 to 3.4 support
-  Unicode (UTF-8) TrueType font subset embedding
-  Internal/External Links
-  PNG, GIF and JPG support (including transparency and alpha channel)
-  Shape, Line Drawing
-  Cell/Multi-cell/Plaintext writing, Automatic page breaks
-  Basic html2pdf (Templates with a visual designer in the works)
-  Exceptions support, other minor fixes, improvements and PEP8 code
   cleanups

Installation Instructions:
--------------------------

To get the latest development version you can download the source code
running:

::

      git clone https://github.com/alexanderankin/pyfpdf.git
      cd pyfpdf
      python setup.py install

You can also install PyFPDF from PyPI, with easyinstall or from Windows
installers. For example, using pip:

::

      pip install fpdf

**Note:** the `Python Imaging
Library <http://www.pythonware.com/products/pil/>`__ (PIL) is needed for
GIF support. PNG and JPG support is built-in and doesn't require any
external dependency. For Python 3, `Pillow - The friendly PIL
fork <https://github.com/python-pillow/Pillow>`__ is supported.

Documentation:
--------------

|Documentation Status|

-  `Read the Docs <http://pyfpdf.readthedocs.org/en/latest/>`__
-  `FAQ <docs/FAQ.md>`__
-  `Tutorial <docs/Tutorial.md>`__ (Spanish translation available)
-  `Reference Manual <docs/ReferenceManual.md>`__

For further information, see the project site:
https://github.com/reingart/pyfpdf or the old Google Code project page
https://code.google.com/p/pyfpdf/.

.. |Documentation Status| image:: https://readthedocs.org/projects/pyfpdf/badge/?version=latest
   :target: http://pyfpdf.rtfd.org


