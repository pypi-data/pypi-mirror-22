==================
Django AppSettings
==================



Application settings helper for Django apps.

Why another *app settings* app?
Because none of the other suited my needs!

This one is simple to use, and works with unit tests overriding settings.

Quick usage
===========

.. code:: python

    # my_package/apps.py

    from django.apps import AppConfig
    import appsettings as aps


    class AppSettings(aps.AppSettings):
        my_setting = aps.Setting(name='basic_setting', default=25)

        required_setting = aps.Setting(required=True)  # name='REQUIRED_SETTING'

        typed_setting = aps.StringSetting(prefix='string_')
        # -> typed_setting.full_name == 'STRING_TYPED_SETTING'

        custom_setting = RegexSetting()  # -> see RegexSetting class below

        class Meta:
          # default prefix for every settings
          setting_prefix = 'example_'


    class RegexSetting(Setting):
        def check():
            value = self.get_raw()  # should always be called to check required condition
            if value != self.default:  # always allow default to pass
                re_type = type(re.compile(r'^$'))
                if not isinstance(value, (re_type, str)):
                    # raise whatever exception
                    raise ValueError('%s must be a a string or a compiled regex '
                                     '(use re.compile)' % self.full_name)

        def transform(self):
            value = self.get_raw()
            # ensure it always return a compiled regex
            if isinstance(value, str):
                value = re.compile(value)
            return value


    class MyAppConfig(AppConfig):
        name = 'my_app'
        verbose_name = 'My Application'

        def ready(self):
            # check every settings at startup, raise one exception
            # with all errors in its message
            AppSettings.check()


.. code:: python

    # django_project/settings.py
    EXAMPLE_BASIC_SETTING = 26
    EXAMPLE_REQUIRED_SETTING = 'something'

.. code:: python

    # my_package/other_module.py

    from .apps import AppSettings


    regex = AppSettings.custom_setting.get()  # alias for transform()

    # instantiate the class to load each and every settings
    appsettings = AppSettings()
    appsettings.my_setting == 25  # False: 26


**Settings classes:**

- StringSetting: default = ''
- IntegerSetting: default = 0
- PositiveIntegerSetting: default = 0
- BooleanSetting: default = False
- FloatSetting: default = 0.0
- PositiveFloatSetting: default = 0.0
- ListSetting: default = []
- SetSetting: default = ()
- DictSetting: default = {}
- ImportedObjectSetting: default = None

*Are the following settings useful? Please tell me on Gitter.*

- StringListSetting: default = []
- StringSetSetting: default = ()
- IntegerListSetting: default = []
- IntegerSetSetting: default = ()
- BooleanListSetting: default = []
- BooleanSetSetting: default = ()
- FloatListSetting: default = []
- FloatSetSetting: default = ()

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

0.2.5 (2017-06-02)
==================

- Add six dependency (now required).
- Rename ``Int`` settings to ``Integer``, and ``Bool`` ones to ``Boolean``.
- Remove metaclass generated getters and checkers.

0.2.4 (2017-05-02)
==================

- Settings are not checked when they default to the provided default value.
- Settings classes received better default values corresponding to their types.

0.2.3 (2017-05-02)
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


