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

        # Filter by uuid

        # Filter by user?

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
    @decorate.add_endpoint_parameter("owner", required=True)
    @decorate.apimethod
    def post(self):
        """ Register a UUID """

        # Create graph object
        graph = self.global_get_service('neo4j')

        # Create user if not exists
        username = self._args['owner']
        user = graph.ProvidedUser.get_or_create({'username': username}).pop()

        # Create and link UUID
        dobj = graph.DataObject(id=getUUID())
        dobj.save()
        dobj.owned.connect(user)

        # Return the UUID
        return dobj.id

    # @auth.login_required
    @decorate.apimethod
    def put(self, uuid):
        """ Update metadata for a registerd object """

        # Verify if the user matches!

        # Receive data
        input_json = self.get_input()
        print("INPUT", input_json)

        # Update the graph
            # http://j.mp/29o1qk0

        # Return the UUID
        return input_json
