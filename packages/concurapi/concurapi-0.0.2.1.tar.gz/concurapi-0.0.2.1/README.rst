Concur API SDK
===============
The Concur API SDK is a Python client library designed to support Concur's Developer APIs.
You can read more about the Official API by accessing its `official documentation <http://developer.concur.com>`_.

System Requirements
--------------------

Concur API SDK depends on the following Python libraries:

* requests

Installation
------------
Install using `pip`:

::

  pip install concurapi.


Configuration
--------------
You'll need to register at `Concur's Administration site <https://www.concursolutions.com/>`_.
Before you create a partner application, make sure your user account has web service administrator access.
You can create a partner application by following these steps.

* Log on to Concur's Administration using your username and password

* Follow the links *Administration* -> *Company* -> *Web Services*

* Click on the link to register a partner application in the left navigation bar.

* In the next screen click on the **New** button to create a new application

* In the modal dialog, you can choose the permissions for the actions you need to automate.

Also, please note the system generated **Key** and **Secret**. These values are used by the sdk to make a call
to Concur's API.


Usage
-----
Before you use the sdk, you'll need to register a partner application and retrieve a Key/Secret. Please see Configuration_.
You'll also need to install the client sdk using ``pip``. Please see `System Requirements`_ and Installation_.

.. code-block:: python

     from concurapi.client import ConcurAPI
     from concurapi.models import Report
     api = ConcurAPI(client_key="Kq4qIqR3K3zgOJwdI2KLtQ",
                     client_secret="Kq4qIqR3K3zgOJwdI2KLtQ",
                     username="concuruser@xyz.com",
                     password="johndoe")
     report = Report(attributes=dict(Name="First Report",
                     Description="Report for a new Expense"), api=api)
     report.create()
     get_report = Report.find(report['ID'])


If the service is not available, the sdk throws a ``ServiceNotAvailable`` exception which can be handled like so:

.. code-block:: python

     from concurapi.client import ConcurAPI
     from concurapi.exceptions import ServiceNotAvailable
     import sys
     try:
         api = ConcurAPI(client_key="Kq4qIqR3K3zgOJwdI2KLtQ",
                            client_secret="Kq4qIqR3K3zgOJwdI2KLtQ",
                            username="concuruser@xyz.com",
                            password="johndoe")
     except ServiceNotAvailable as se:
          #handle ServiceNotAvailable exception
          sys.exit(se.message)


The sdk returns ``HTTPException`` when there is a REST exception from the API.
As an example, if a report with id - ``12345-abcde`` is not available, the service returns a ``404`` HTTP Exception

.. code-block:: python

    from concurapi.client import ConcurAPI
    from concurapi.exceptions import HTTPException
    from concurapi.models import Report
    import sys
    try:
     api = ConcurAPI(client_key="Kq4qIqR3K3zgOJwdI2KLtQ",
                        client_secret="Kq4qIqR3K3zgOJwdI2KLtQ",
                        username="concuruser@xyz.com",
                        password="johndoe")
     Report.find("1234-abcde")

    except HTTPException as he:
      #handle HTTPException exception
      sys.exit(he.message)


Contributions
-------------
Contributions are welcome! Please open a pull request.