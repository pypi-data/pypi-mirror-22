terminal_banner
===============

A text banner for use in terminal applications.

Example
-------

.. code-block:: python

    import terminal_banner
    banner_text = "This is my banner text.\n\nThis is a second line of text."
    my_banner = terminal_banner.Banner(banner_text)
    print(my_banner)

Output:
~~~~~~~

::

    ******************************************...****
    * This is my banner text.                       *
    *                                               *
    * This is a second line of text.                *
    ******************************************...****

Installation
------------

To install the python package with pip::
    pip install terminal_banner

For source::
    git clone https://github.com/martincyoung/terminal_banner

License
-------

::

    MIT License

    Copyright (c) 2016 Martin Craig Young

    Permission is hereby granted, free of charge, to any person obtaining a copy
    of this software and associated documentation files (the "Software"), to deal
    in the Software without restriction, including without limitation the rights
    to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
    copies of the Software, and to permit persons to whom the Software is
    furnished to do so, subject to the following conditions:

    The above copyright notice and this permission notice shall be included in all
    copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
    OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
    SOFTWARE.
