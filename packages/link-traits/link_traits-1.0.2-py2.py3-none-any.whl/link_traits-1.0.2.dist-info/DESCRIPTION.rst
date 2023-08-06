link\_traits
============

|Build Status| |Codecov branch|

**link\_traits** is a fork of
`traitlets' <https://github.com/ipython/traitlets>`__ **link** and
**dlink** functions to add the ability to link
`traits <https://github.com/enthought/traits>`__ in addition to
traitlets.

Installation
------------

Make sure you have `pip
installed <https://pip.pypa.io/en/stable/installing/>`__ and run:

.. code:: bash

    pip install link_traits

**link\_traits** depends on **traits** which is not a pure Python
package. In `Anaconda <http://continuum.io/anaconda>`__ you can install
link\_traits and traits as follows:

.. code:: bash

    conda install link_traits -c conda-forge

Running the tests
-----------------

py.test is required to run the tests.

.. code:: bash

    pip install "link_traits[test]"
    py.test --pyargs traitlets

Usage
-----

.. code:: python


    import traits.api as t
    import traitlets
    from link_traits import link

    class A(t.HasTraits):
        a = t.Int()

    class B(traitlets.HasTraits):
        b = t.Int()
    a = A()
    b = B()
    l = link((a, "a"), (b, "b"))

.. code:: python

    >>> a.a = 3
    >>> b.b
    3

Development
-----------

Contributions through pull requests are welcome. The intention is to
keep the syntax and features in sync with the original traitlets'
**link** and **dlink** functions. Therefore, before contributing a new
feature here, please contribute it to
`traitlets <https://github.com/ipython/traitlets/>`__ first.

.. |Build Status| image:: https://travis-ci.org/hyperspy/link_traits.svg?branch=master
   :target: https://travis-ci.org/hyperspy/link_traits
.. |Codecov branch| image:: https://img.shields.io/codecov/c/github/hyperspy/link_traits/master.svg
   :target: https://codecov.io/gh/hyperspy/link_traits


