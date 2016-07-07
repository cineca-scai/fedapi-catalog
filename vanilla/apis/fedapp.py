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

        # Receive data
        input_json = self.get_input()

        # Verify if the user is available
        key = 'owner'
        if key not in input_json:
            return self.force_response(errors={key: 'missing JSON parameter'})

        # Connect the graph
        graph = self.global_get_service('neo4j')
        dobj = None
        user = None

        # Recover the node
        try:
            dobj = graph.DataObject.nodes.get(id=uuid)
        except graph.ProvidedUser.DoesNotExist:
            return self.force_response(errors={uuid: 'could not be found'})
        logger.debug("Requested %s" % dobj)

        # Match the user
        username = input_json.get(key)
        user = dobj.owned.all().pop()
        if user.username != username:
            return self.force_response(errors={key: 'not matching'})

        # Pop out relationships

        # Location
        key = 'locations'
        try:
            for location in input_json.pop(key):
                locobj = graph.Location.get_or_create(location).pop()
                dobj.located.connect(locobj)
        except Exception as e:
            logger.critical("Failed with %s: %s" % (key, e))
            return self.force_response(errors={key: 'invalid'})

        # Metadata
        key = 'metadata'
        for meta in input_json.pop(key):
            try:
                for k, v in meta.items():
                    metaobj = \
                        graph.MetaData.get_or_create({'key':k, 'value':v}).pop()
                    dobj.described.connect(metaobj)
            except Exception as e:
                logger.critical("Failed with %s: %s" % (key, e))
                return self.force_response(errors={key: 'invalid'})

        # Tags
        key = 'tags'
        for tag in input_json.pop(key):
            try:
                tagobj = \
                    graph.Tag.get_or_create({'name': tag}).pop()
                dobj.tagged.connect(tagobj)
            except Exception as e:
                logger.critical("Failed with %s: %s" % (key, e))
                return self.force_response(errors={key: 'invalid'})

        # Update the graph
        # people = Person.create_or_update({'name': 'Tim', 'age': 83})

        # Return the UUID
        return uuid
