Introduction
============

This is a "just for fun" project, created to show my django_ projects guts. It allows to browse source code of all ``INSTALLED_APPS``.

Dependencies
------------

If you want to highlight sources then install Pygments_.

Installation
------------

* Run ``pip install django-guts Pygments``.
* Add application ``django_guts`` to the ``INSTALLED_APPS`` list.
* Add this to your ``urls.py``::

        url(r'^guts/', include('django_guts.urls')),

* Add these optional variables to the settings.py::

        GUTS_IGNORE = (r'^\..*\.swp$', r'^.*\.pyc$', r'^.*\.pyo$')
        GUTS_HL_EXTENSIONS = ('py', 'html', 'htm')

* Restart server and point your browser to ``http://yourproject.com/guts/``.

.. _django: http://djangoproject.org
.. _Pygments: http://pygments.org
