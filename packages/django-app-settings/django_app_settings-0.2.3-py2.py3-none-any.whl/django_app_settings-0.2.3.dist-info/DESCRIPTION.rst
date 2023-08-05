==================
Django AppSettings
==================



Application settings helper for Django apps.

Why another *app settings* app?
Because none of the other suited my needs!

This one is simple to use, and works with unit tests overriding settings.

Usage
=====

With recent Django versions, it is recommended to put your settings in an
``apps.py`` module of your Django app, though you can put it wherever you want.
The following is just an example.

.. code:: python

    from django.apps import AppConfig
    import appsettings as aps

    class MyAppConfig(AppConfig):
        name = 'my_app'
        verbose_name = 'My Application'

        def ready(self):
            AppSettings.check()


    class AppSettings(aps.AppSettings):
        always_use_ice_cream = aps.BooleanSetting(default=True)
        attr_name = aps.StringSetting(name='SETTING_NAME')

        # if you have complex treatment to do on setting
        complex_setting = aps.Setting(transformer=custom_method, checker=custom_checker)

        # if you need to import a python object (module/class/method)
        imported_object = aps.ImportedObjectSetting(default='app.default.object')

        class Meta:
            setting_prefix = 'ASH'  # settings must be prefixed with ASH

Then in other modules:

.. code:: python

    from .apps import AppSettings

    # instantiation will load and transform every settings
    app_settings = AppSettings()
    app_settings.attr_name == 'something'

    # or, and in order to work with tests overriding settings
    AppSettings.get_always_use_ice_cream()  # to get ASH_ALWAYS_USE_ICE_CREAM setting dynamically
    my_python_object = AppSettings.get_imported_object()

You can access settings directly from the settings class, but also from the
settings instances:

.. code:: python

    my_setting = AppSettings.my_setting
    my_setting.get()  # get and transform
    my_setting.check()  # get and check
    my_setting.get_raw()  # just get the value in django settings

.. warning::

    After instantiating an AppSettings class, the settings won't be
    instances of Setting anymore but the result of their ``get`` method.

    .. code:: python

        appsettings = AppSettings()
        appsettings.my_setting == AppSettings.my_setting        # False
        appsettings.my_setting == AppSettings.my_setting.get()  # True
        appsettings.my_setting == AppSettings.get_my_setting()  # True

Running ``AppSettings.check()`` will raise an ``ImproperlyConfigured``
exception if at least one of the settings' ``check`` methods raised an
exception. It will also print all caught exceptions.

License
=======

Software licensed under `ISC`_ license.

.. _ISC: https://www.isc.org/downloads/software-support-policy/isc-license/

Installation
============

::

    pip install django-app-settings

Documentation
=============

`On ReadTheDocs`_

.. _`On ReadTheDocs`: http://django-appsettings.readthedocs.io/

Development
===========

To run all the tests: ``tox``

=========
Changelog
=========

0.2.3 (2917-05-02)
==================

- Add ``full_name`` property to ``Setting`` class.
- Add ``required`` parameter to ``Setting`` class (default ``False``).

0.2.2 (2017-04-17)
==================

- Import settings classes in main module to simplify imports.

0.2.1 (2017-04-17)
==================

- Add ``PositiveInt`` and ``PositiveFloat`` settings.
- Add support for Django 1.11.
- Implement basic settings classes.

0.2.0 (2017-04-17)
==================

- Implement basic Setting class.
- Pin dependencies.
- Change distribution name to ``app-settings``.

0.1.0 (2017-03-23)
==================

- Alpha release on PyPI.


