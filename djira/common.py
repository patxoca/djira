# -*- coding: utf-8 -*-

# $Id:$

from __future__ import print_function
from __future__ import unicode_literals

from django.apps import apps
from django.core.serializers.json import DjangoJSONEncoder

import pluggy


# Project name, required by pluggy. Used as the name of the app too.
PROJECT_NAME = "djira"


class EndPoint(object):
    """Class describing an endpoint.

    :param callable function: the function that will be called for the
      endpoint. Will receive the arguments from the GET request
      payload. No ``request`` will be passed, it's not a view. Return
      an object that can be serialized to json.

    :param str name: name of the endpoint, used for the URL. If
      omitted ``function.__name__`` will be used.

    :param Schema request_schema: ``Schema`` describing the parameters
      accepted by ``function``. Leave blank if ``function`` takes no
      arguments. Is used both for sanitizing the input and for
      documentation purposes.

    :param Schema response_schema: ``Schema`` describin the value
      returned by ``function``. Used for documentation purposes.

    :param str doc: documentation for of the endpoint. If omitted
      ``function.__doc__`` will be used.

    :param object encode: json encode used to convert the value
      returned by ``function`` to json. Specify a value in case
      ``function`` returns some non *standard* value.

    """
    def __init__(self, function, name=None, request_schema=None,
                 response_schema=None, doc=None, encoder=DjangoJSONEncoder):
        if not callable(function):
            raise TypeError("'function' argument must be callable.")
        if name is None:
            name = function.__name__
        if doc is None:
            doc = function.__doc__
        self.function = function
        self.name = name
        self.request_schema = request_schema
        self.response_schema = response_schema
        self.doc = doc
        self.encoder = encoder


def get_plugin_manager():
    """Return the plugin manager.

    """
    app = apps.get_app_config(PROJECT_NAME)
    return app.plugin_manager


# decorator required by pluggy in order to mark plugin implementation
# functions.
hookimpl = pluggy.HookimplMarker(PROJECT_NAME)