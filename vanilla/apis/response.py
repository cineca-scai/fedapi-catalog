# -*- coding: utf-8 -*-

from __future__ import absolute_import

from commons.logs import get_logger
from ..base import ExtendedApiResource
from .. import decorators as decorate

logger = get_logger(__name__)


############################################################
# # OPTION 1

# @decorate.custom_response
# def fedapp_response(
#         defined_content=None,
#         code=None,
#         errors={},
#         headers={}):

#     return ExtendedApiResource.flask_response("Hello")

# # OPTION 2

# class Response(ExtendedApiResource):
#     def fedapp_response(self, *args, **kwargs):
#         return self.flask_response("Hello")

# decorate.custom_response(Response().fedapp_response)

# # OPTION 3
## // TO BE FIXED
# decorate.custom_response(original=True)

############################################################


@decorate.custom_response
def fedapp_response(defined_content=None,
                    code=None, headers={}, errors={}):
    """
    Define my response that will be used
    from any custom endpoint inside any file
    """

    if len(errors) > 0:
        defined_content = {'errors': errors}
    else:
        pass

    return ExtendedApiResource.flask_response(
        defined_content, status=code, headers=headers)
