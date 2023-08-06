Install
=======

This package must be installed in a virtualenv

::

    export VENV='myEnv'
    virtualenv $VENV
    source $VENV/bin/activate
    pip install modoco

Because of the way pip resolves dependencies this can sometimes fail because
MoinMoin is not installed early enough - in that case install it manually
in your virtualenv with ``pip install 'moin>=1.9,<2.0'`` and then repeat
``pip install modoco``.

You can safely ignore errors referring to failure to build the wheel.

Start server
============

If you have pip installed mod_wsgi, you can then run modoco straight away
using mod\_wsgi-express:

::

    mod_wsgi-express start-server $VENV/share/moin/moin.wsgi &

Start using modoco
==================

-  Navigate to ``localhost:8000/`` and login using the superuser credentials
   found in ``$VENV/share/moin/wikiconfig.py``.
-  Read the HelpOnModoco page
