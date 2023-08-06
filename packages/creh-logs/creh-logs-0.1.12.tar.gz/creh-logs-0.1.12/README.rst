=====
Creh Logs
=====

Creh-logs is a simple Django app to conduct Web-based polls. For each
question, visitors can choose between a fixed number of answers.

Detailed documentation is in the "docs" directory.

Quick start
-----------

1. creh-logs can be obtained directly from PyPI, and can be installed with pip:

    pip install creh-logs

1. Add "polls" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'logs',
    ]

2. Run "python manage.py migrate" to create the log models.

3. Use

    from creh-logs.actions import register
    from creh-logs.utils import get_location

    register.create_by_exception(exception=exception, message='message', location=get_location(), tag='Tag')

