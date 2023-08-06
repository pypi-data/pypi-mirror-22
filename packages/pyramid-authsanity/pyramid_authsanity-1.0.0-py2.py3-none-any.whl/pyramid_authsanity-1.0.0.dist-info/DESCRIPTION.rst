==================
pyramid_authsanity
==================

An auth policy for the `Pyramid Web Framework
<https://trypyramid.com>`_ with sane defaults that works with `Michael
Merickel's <http://michael.merickel.org>`_ absolutely fantastic
`pyramid_services <https://github.com/mmerickel/pyramid_services>`_.
Provides an easy to use authorization policy that incorporates web security
best practices.

Installation
============

Install from `PyPI <https://pypi.python.org/pypi/pyramid_authsanity>`_ using
``pip`` or ``easy_install`` inside a virtual environment.

::

  $ $VENV/bin/pip install pyramid_authsanity

Or install directly from source.

::

  $ git clone https://github.com/usingnamespace/pyramid_authsanity.git
  $ cd pyramid_authsanity
  $ $VENV/bin/pip install -e .

Setup
=====

Activate ``pyramid_authsanity`` by including it into your pyramid application.

::

  config.include('pyramid_authsanity')



1.0.0 (2017-05-19)
==================

- Remove Python 2.6 support

- Fix a bug whereby the policy was storing a dict instead of a list in the
  source, which of course broke things subtly when actually using the policy.

- Send empty cookie when forgetting the authentication for the cookie source

0.1.0a3
=======

- Remove Python 3.2 support

- Fix failing tests using pyramid_services >= 0.4 by requiring at least
  pyramid_services 0.3 because it contains the find_service_factory function
  utilized by the test.

0.1.0a2
=======

- Bert was asleep at the keyboard, the fix below is now actually properly fixed
  by decoding to ascii, which is safe because it is base64.

0.1.0a1
=======

- Ticket value is now a string instead of binary, this way Python 3's
  json.dumps() will be able to serialize the value sent to the sources
  remember function.


0.1.0a0
=======

 - Initial release.


