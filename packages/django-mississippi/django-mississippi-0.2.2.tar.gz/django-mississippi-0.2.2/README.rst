===========
Mississippi
===========

Mississippi goes one step beyond Django's URL dispatcher to:

* Promote resources (pages) and resource types to first class citizens
* Allow for /<slug> URLs without any prefix, regardless of the resource type
* Easily and automatically generate sitemaps

Right now Mississippi is in its early development stage; there is more to come.

Quick Start
-----------

1. Add 'mississippi' to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'mississippi',
    ]

2. Make the mississippi URLconf the last one in your project urls.py like this::

    url(r'', include('mississippi.urls')),

3. Run `python manage.py migrate` to create the mississippi models.

TODO: Describe how to associate models with mississippi models.

TODO: Describe how to test to ensure mississippi is installed correctly.

