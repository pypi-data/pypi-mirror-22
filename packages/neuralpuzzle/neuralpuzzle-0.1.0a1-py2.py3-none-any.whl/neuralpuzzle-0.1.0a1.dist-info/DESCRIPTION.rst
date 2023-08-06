===============================
NeuralPuzzle
===============================


.. image:: https://img.shields.io/pypi/v/neuralpuzzle.svg
    :target: https://pypi.python.org/pypi/neuralpuzzle

.. image:: https://travis-ci.org/cxmaro-s/NeuralPuzzle.svg?branch=master
    :target: https://travis-ci.org/cxmaro-s/NeuralPuzzle
    :alt: Build status on Travis CI

.. image:: https://readthedocs.org/projects/neuralpuzzle/badge/?version=latest
    :target: https://neuralpuzzle.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status

.. image:: https://pyup.io/repos/github/cxmaro-s/NeuralPuzzle/shield.svg
    :target: https://pyup.io/account/repos/github/cxmaro-s/NeuralPuzzle/
    :alt: Updates

.. image:: http://ci.appveyor.com/api/projects/status/github/cxmaro-s/neuralpuzzle?branch=master
    :target: https://ci.appveyor.com/project/cxmaro-s/neuralpuzzle/branch/master
    :alt: Windows build status on Appveyor

.. image:: https://img.shields.io/badge/License-GPL%20v3-blue.svg
    :target: https://github.com/cxmaro-s/NeuralPuzzle/blob/master/LICENSE


A simple Python package that helps anyone on building and running a deep neural network
in second.


* Free software: GNU General Public License v3
* Documentation: https://neuralpuzzle.readthedocs.io.

Quickstart
----------

To install NeuralPuzzle, run the following command in your terminal::

    pip install neuralpuzzle

Quickly train a simple one hidden layer feed forward nueral network with ReLU activation fucntion, and initialize paramters (weights and bias) using Xavier method::

    from neuralpuzzle import *

    train_network = NeuralPuzzle('mnist.pkl', [784, 50, 10], ['relu'], 'xavier')

Features
--------

* Easy install and use
* One-line code to train


Credits
---------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage



=======
History
=======

0.1.0 (2017-04-18)
------------------

* First release on PyPI.


