django-thema
============

A `Django <https://www.djangoproject.com/>`__ application that provides
`EDItEUR Thema categories <http://www.editeur.org/151/Thema/>`__. It
supplies translation to all languages EDItEUR supports, so if you are
using Django's internationalization in your project you will also get
translation.

Requirements
------------

This application requires:

::

    django,
    mock,
    polib,
    xlrd,

Installation
------------

Install the application from Pypi:

``$ pip install django-thema``

Add the application to your Django project:

::


    INSTALLED_APPS = [
        ...
        'thema',
        ...
    ]

Migrate the application

::

    $ ./manage.py thema

You should populate the model with the data in EDItEUR database, for
this use the command ``populate_thema_categories``

::

    $ ./manage.py populate_thema_categories

Also, please make sure the tests passed smoothly

::

    $ ./manage.py test thema

If any test fails, then you could end up with missing data in your
database or malfunction of the application.

How it works
------------

``django-thema`` offers a model ``ThemaCategory``, each instance is a
Thema category. The model looks like:

::

    class ThemaCategory(models.Model):
        """Model that represents the Thema categories.

        The field `header` contains the heading in English.
        """
        ...
        code: The code of the Thema category,
        header: The heading of the Thema category (description),
        parent: A ForeignKey to the parent category.
        ...
        
        @property
        def local_header(self):
            """Return the header translated to the activated language."""
            return _(self.header)

The content of ``header`` is in English, but you can get its translation
to your local language using the property
``ThemaCategory.local_header``. To see all supported languages check
Supported Languages section.

::

    ...
    >>> from thema.models import ThemaCategory
    >>> thema_aba = ThemaCategory.objects.get(code='ABA')
    >>> thema_aba.header
    'Theory of art'
    ...

Getting translation:

::

    ...
    >>> from django.utils.translation import activate
    >>> activate('es')
    >>> thema_aba.local_header
    'Teoría del arte'
    >>> activate('da')
    >>> thema_aba.local_header
    'Kunstteori'
    ...

*Note: the translation will work only if you have enabled `Django's
internationalization <https://docs.djangoproject.com/en/1.10/topics/i18n/>`__
in your project.*

Getting the parent category:

::

    ...
    >>> thema_aba.parent
    <ThemaCategory: AB>
    ...

Supported language
==================

The application supports the languages covered by EDItEUR:

-  Arabic
-  Danish
-  English
-  Spanish
-  French
-  German
-  Hungarian
-  Italian
-  Japanese
-  Lithuanian
-  Norwegian
-  Polish
-  Portuguese
-  Swedish
-  Turkish

We don't do any translation, we just use the data provided by EDItEUR,
so if you find a missing translation or a translation error, please
`contact EDItEUR directly <http://www.editeur.org/42/Contact/>`__.

Authors
=======

- Dannier Trinchet
- Mikkel Munch
- Vladir Parrado
- Søren Howe
- Tobias Ley

Maintenance
===========

To submit bugs, feature requests, submit patches, please use `the
official repository <https://saxo.githost.io/publish/django-thema/>`__.

Copyright and licensing information
===================================

BSD License 2.0, 3-clause license.
