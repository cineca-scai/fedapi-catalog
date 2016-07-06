# -*- coding: utf-8 -*-

from __future__ import absolute_import
from commons.logs import get_logger
from commons.services.uuid import getUUID
from ..base import ExtendedApiResource
from .. import decorators as decorate

# # AUTH
# from ...auth import auth

logger = get_logger(__name__)


#####################################
class Catalog(ExtendedApiResource):

    _index_name = 'fedapp'

    # @auth.login_required
    @decorate.apimethod
    def get(self, uuid=None):

        hello = "Hello world"
        logger.info(hello)

        graph = self.global_get_service('neo4j')

        # ####################
        # # Test elastic
        # es = self.global_get_service('elasticsearch')
        # print(es)
        # es.index_up(self._index_name)

        # ####################
        # # Testing returns
        # return self.report_generic_error()
        # return self.force_response(errors="failed")
        # return {'errors': 'test', 'defined_content': None}
        # return self.response(hello)

        return hello

    # @auth.login_required
    @decorate.apimethod
    def post(self):
        """ Register a UUID """

        # Create UUID
        uuid = getUUID()

        # Create graph object
        graph = self.global_get_service('neo4j')

        # Return the UUID
        return uuid

    # @auth.login_required
    @decorate.apimethod
    def put(self, uuid):
        """ Update data with some """

        # Receive data
        input_json = self.get_input()
        print("INPUT", input_json)

        # Update the graph

        # Return the UUID
        return input_json
