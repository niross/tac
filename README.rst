Analysed Comments
=================

A simple RESTful API to create, analyse and serve text comments. 

----------------

**The Approach**

I have created a simple python3/django2 app and used django-rest-framework backed with Celery and Redis to build the API.

The basic flow is:

* When a comment is created or updated the comment's status is set to 'Pending'.
* On save a signal is sent which queues a celery task ``analyse_comment`` for that comment.
* The celery task then calls the Watson API.
* If the API call fails or the comment cannot be analysed the comments's status is set to 'Failed'.
* If the comment is successfully analysed the status is set to 'Complete' and the ``is_positive`` flag is set to True/False based on the analysis reveived.

The API uses django-rest-swagger_ for documentation which can be found at http://0.0.0.0:8000/ after installing using the docs below.

The swagger docs allow you to test all API methods from within the browser.

----------------

**The Stack**

The stack for development uses docker and docker-compose_ containers comprised of:

* Django - Runs development server
* Postgres - DB where comments are stored
* Celeryworker - celery task runner
* Redis: task queue

----------------

**The API**

The API uses 4 REST verbs across 5 endpoints and is stateless (i.e. it's RESTful):

    GET:
        /api/ - List all comments

        /api/<sku>/ - Show details for comment with SKU <sku>

    POST:
        /api/ - Create new comment

    PUT:
        /api/<sku>/ - Update the text for the comment with SKU <sku>

    DELETE:
        /api/<sku>/ - Set the deleted flag on comment with SKU <sku>


Developer documentation can be found at http://0.0.0.0:8000/ once you are up and running.

.. _docker-compose: https://docs.docker.com/compose/
.. _django-rest-swagger: https://github.com/marcgibbons/django-rest-swagger/


Installation
------------

To get up and running locally you will need docker and docker-compose::

    git clone git@github.com:niross/tac.git
    cd tac/
    docker-compose -f local.yml build
    docker-compose -f local.yml up

You can now visit http://0.0.0.0:8000/ and view the developer docs.

You can also test the API using curl

**Create a comment**::

    curl -X POST "http://0.0.0.0:8000/api/" -H "accept: application/json" -H "Content-Type: application/json" -d "{ \"text\": \"I love this comment\"}"

**List comments**::

    curl -X GET "http://0.0.0.0:8000/api/" -H "accept: application/json"

**View details of single comment**::

    curl -X GET "http://0.0.0.0:8000/api/1/" -H "accept: application/json"

**Update a comment**::

    curl -X PUT "http://0.0.0.0:8000/api/1/" -H "accept: application/json" -H "Content-Type: application/json" -d "{ \"text\": \"I hate this comment\"}"

**Delete a comment**::

    curl -X DELETE "http://0.0.0.0:8000/api/1/" -H "accept: application/json"

Testing
-------

Unit tests for models and endpoints can be found in the ``tests/`` directory.

To run the tests via docker::

    docker-compose -f local.yml run --rm django python manage.py test


Deployment
----------

If I was going to deploy this myself I would run as a virtualhost under Apache2 on my VPS using WSGI as that is the easiest option for me personally.

* Celery would be run using supervisord
* Deployment would be handled by a simple fabric script which will checkout the latest release tag and bounce apache/supervisor to refresh the changes.

Another option would be to run under docker. For me personally, as I run multiple sites on a single VPS, I would need to run a reverse proxy using nginx which would allow for running the API on port 80 (or 443 ideally).

A third option I would consider is Heroku which I have used before and makes it simple to get a project like this deployed and monitored.


Scaling
-------

* Moving the Watson API requests off to a queue will help response times when creating comments
* The standard caching built into Django will work well for GET requests. Spinning up a memcached container would work.
* If performance started getting slugginsh the first thig I would do would be split the DB out to a separate VPS (and out of docker too)

Final Notes
-----------

I would say I spent less 3-4 hours on this interspersed with phone calls/other job search activities.

Django is probably overkill for this project but it's what I'm comfortable with. Something like flask would probably be more appropriate but I went with what I know for the test scenario.

Given more time there are multiple things I would have liked to have done...

* Once a comment has failed analysis there is no way to retry it. This could potentially be logged to Sentry and picked up by a support person I guess.
* The analyse task is not really tested currently but ran out of time unfortunately.


I have included some of my initial "whiteboard" working below for reference.

