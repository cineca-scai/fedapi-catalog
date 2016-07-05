# -*- coding: utf-8 -*-

from __future__ import absolute_import
from commons.logs import get_logger
from ..base import ExtendedApiResource
from .. import decorators as decorate

# # AUTH
# from ...auth import auth

logger = get_logger(__name__)


#####################################
# Make a custom response

## OPTION 1

# @decorate.custom_response
# def fedapp_response(
#         defined_content=None,
#         code=None,
#         errors={},
#         headers={}):

#     return ExtendedApiResource.flask_response("Hello")

## OPTION 2

# class Response(ExtendedApiResource):
#     def fedapp_response(self, *args, **kwargs):
#         return self.flask_response("Hello")

# decorate.custom_response(Response().fedapp_response)


#####################################
class Catalog(ExtendedApiResource):

    _index_name = 'fedapp'

    # @auth.login_required
    @decorate.apimethod
    def get(self):

        hello = "Hello world"
        logger.info(hello)

        # ####################
        # # Test graph
        # graph = self.global_get_service('neo4j')
        # queryout = graph.cypher("MATCH (n) RETURN (n)")
        # print(queryout)

        # ####################
        # # Test elastic
        # es = self.global_get_service('elasticsearch')
        # print(es)
        # es.index_up(self._index_name)

        # ####################
        # # Testing returns
        return self.report_generic_error()
        # return self.force_response(errors="failed")
        # return {'errors': 'test', 'defined_content': None}
        # return self.response(hello)
        return hello
