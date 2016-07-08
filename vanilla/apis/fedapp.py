# -*- coding: utf-8 -*-

from __future__ import absolute_import

import os
from commons.logs import get_logger
from commons.services.uuid import getUUID
from ..base import ExtendedApiResource
from .. import decorators as decorate

# # AUTH
# from ...auth import auth

logger = get_logger(__name__)


#####################################
class Catalog(ExtendedApiResource):

    # @auth.login_required
    @decorate.apimethod
    def get(self, uuid=None):

        hello = "Hello world"
        logger.info(hello)

        graph = self.global_get_service('neo4j')
        dobjs = []

        # Filter by uuid
        if uuid is not None:
            # Recover the node
            try:
                dobjs.append(graph.DataObject.nodes.get(id=uuid))
            except graph.ProvidedUser.DoesNotExist:
                return self.force_response(errors={uuid: 'could not be found'})
            logger.debug("Requested %s" % uuid)
        else:
            dobjs = graph.DataObject.nodes.all()

            ## Filter by user?
            pass

        data = []
        # Build response
        for dobj in dobjs:
            # print(dobj, dir(dobj))
            data.append(self.getJsonResponse(dobj, skip_missing_ids=True))

        return data

    # @auth.login_required
    @decorate.add_endpoint_parameter("owner", required=True)
    @decorate.apimethod
    def post(self):
        """ Register a UUID """

        # Create graph object
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

        # Match the user
        username = input_json.get(key)
        user = dobj.owned.all().pop()
        if user.username != username:
            return self.force_response(errors={key: 'not matching'})

        # Pop out relationships

        # Location
        key = 'locations'
        try:
            for location in input_json.pop(key):
                # Fix timestamps
                location['created'] = \
                    self.timestamp_from_string(location['created'])
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
                    metaobj = graph.MetaData.get_or_create(
                        {'key': k, 'value': v}).pop()
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
        input_json['created'] = \
            self.timestamp_from_string(input_json['created'])
        input_json['updated'] = \
            self.timestamp_from_string(input_json['updated'])
        input_json['id'] = uuid

        key = 'logicalName'
        if key not in input_json:
            input_json[key] = os.path.basename(input_json['path'])

        graph.DataObject.create_or_update(input_json)
        logger.debug("Updated obj %s" % dobj.id)

        # Return the UUID
        return uuid


class ElasticSearch(ExtendedApiResource):

    _index_name = 'fedapp'

    # @auth.login_required
    @decorate.apimethod
    def get(self):

        # ####################
        # # Test elastic
        # es = self.global_get_service('elasticsearch')
        # print(es)
        # es.index_up(self._index_name)

        return "Hello"
