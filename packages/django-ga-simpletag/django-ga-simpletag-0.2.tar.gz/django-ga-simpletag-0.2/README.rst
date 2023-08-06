=====
Google Analytics simple tag
=====

Polls is a simple Django app to conduct Web-based polls. For each
question, visitors can choose between a fixed number of answers.

Detailed documentation is in the "docs" directory.

Quick start
-----------

1. Add "polls" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'gasimpletag',
    ]
2. Load templatetags {% load google_analytics %}

3. Load Tag set id track {% ga_js 'UA-77777777-1' %}