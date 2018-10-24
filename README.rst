Analysed Comments
=================

A simple RESTful API to create, analyse and serve text comments. 

----------------

**The Approach**

I have created a simple django app and used django-rest-framework backed with Celery and Redis to build the API.

The basic flow is:

* When a comment is created or updated the comment's status is set to 'Pending'.
* On save a signal is sent which queues a celery task `analyse_comment` for that comment.
* The celery task then calls the Watson API.
* If the API call fails or the comment cannot be analysed the comments's status is set to 'Failed'.
* If the comment is successfully analysed the status is set to 'Complete' and the `is_positive` flag is set to True/False based on the analysis reveived.

The API uses django-rest-swagger_ for documentation which can be found at http://0.0.0.0:8000/ after installing using the docs below.

The swagger docs allow you to test all API methods from withing the browser.

----------------

**The Stack**

The stack for development uses docker and docker-compose_ containers comprised of:

* Django - Runs development server
* Postgres - DB where comments are stored
* Celeryworker - celery task runner
* Redis: task queue

----------------

**The API**

The API uses 4 REST verbs across 5 endpoints and is stateless (i.e. it's RESTful!):

    GET:
        /api/ - List all comments

        /api/<sku>/ - Show details for comment with SKU <sku>

    POST:
        /api/ - Create new comment

    PUT:
        /api/<sku>/ - Update the text for the comment with SKU <sku>

    DELETE:
        /api/<sku>/ - Set the deleted flag on comment with SKU <sku>


Documentation can be found at http://0.0.0.0:8000/ once you are up and running.

.. _docker-compose: https://docs.docker.com/compose/
.. _django-rest-swagger: https://github.com/marcgibbons/django-rest-swagger/

Installation
------------

TODO


Testing
-------

TODO


Deployment
----

TODO

