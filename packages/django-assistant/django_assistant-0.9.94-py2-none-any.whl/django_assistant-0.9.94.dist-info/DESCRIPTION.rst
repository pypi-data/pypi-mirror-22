=================
django_assistant
=================

django_assistant is a simple Django app to aid developers. 
Detailed documentation is in the "docs" directory.

Some highlights
1. find the location of a view, model, task
2. api documentation tool


Quick start
-----------

1. Add "django_assistant" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'django_assistant',
    ]

2. Include the polls URLconf in your project urls.py like this::

    url(r'^django_assistant/', include('django_assistant.urls')),

3. Run `python manage.py migrate` to create the polls models.

4. Start the development server and visit http://127.0.0.1:8000/django_assistant/
   and start wondering how you lived without it :) 



