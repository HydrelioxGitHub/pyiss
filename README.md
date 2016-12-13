PyIss 
===================

[![Coverage Status](https://coveralls.io/repos/github/HydrelioxGitHub/pyiss/badge.svg)](https://coveralls.io/github/HydrelioxGitHub/pyiss)
[![Build Status](https://travis-ci.org/HydrelioxGitHub/pyiss.svg?branch=master)](https://travis-ci.org/HydrelioxGitHub/pyiss)
[![PyPI version](https://badge.fury.io/py/pyiss.svg)](https://badge.fury.io/py/pyiss)

![ISS](https://upload.wikimedia.org/wikipedia/commons/8/88/ISS_after_STS-118_%28computer_rendering_of_August_2006%29.png)

### <i class="icon-book"></i> Library

**PyIss** is a Python3 library to access to International Space Station location and data

  - This library has been developed using this [API](http://open-notify.org/)
  - This library is for Python3 version 3.3 and upper.

### <i class="icon-check"></i>Installation


There are many ways to install ``pyiss``:

* With pip (preferred), do ``pip install pyiss``.
* To install from source, download it from
  https://github.com/HydrelioxGitHub/pyiss/ and do
  ``python setup.py install``.


### <i class="icon-check"></i>Usage

To use ``pyiss``, just import it in your project like so::

    >>> import pyiss

Afterwards, you can have access to ISS location::

    >>> station = pyiss.ISS()
    >>> print (station.current_location())
    {'longitude': '133.6864', 'latitude': '51.4806'}


That's it!

Documentation is coming !


### <i class="icon-check"></i>License

``pyiss`` is distributed under the MIT license.
 



