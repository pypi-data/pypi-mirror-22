=====
Jobs
=====

Jobs is an add-on for ServiceM8. Allow customers to easily schedule jobs from a "customer portal".

Detailed documentation is in the "docs" directory.

Quick start
-----------

1. Add "jobs" and "bootstrap3" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'jobs',
        'bootstrap3',
    ]

2. Include the polls URLconf in your project urls.py like this::

    url(r'^jobs/', include('jobs.urls')),

3. Run `python manage.py migrate` to create the polls models.

4. Start the development server and visit http://127.0.0.1:8000/admin/
   to create a poll (you'll need the Admin app enabled).

5. Visit http://127.0.0.1:8000/polls/ to participate in the poll.
