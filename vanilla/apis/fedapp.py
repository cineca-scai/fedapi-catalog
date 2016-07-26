# -*- coding: utf-8 -*-

from __future__ import absolute_import

import os
from commons.logs import get_logger
from commons.services.uuid import getUUID
from elasticsearch_dsl.query import MultiMatch
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

# // TO DISCUSS:
## Should we allow a filter by user?
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
        es = self.global_get_service('elasticsearch')

        # Create user if not exists
        username = self._args['owner']
        user = graph.ProvidedUser.get_or_create({'username': username}).pop()

        # Add user to elastic search suggestions
        es.get_or_create_suggestion(
            es.GenericSuggestion,
            text=username, payload={'type': 'user'})

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
        elastic_data = {}

        # Verify if the user is available
        key = 'owner'
        if key not in input_json:
            return self.force_response(errors={key: 'missing JSON parameter'})
        elastic_data[key] = input_json[key]

        # Connect services
        graph = self.global_get_service('neo4j')
        es = self.global_get_service('elasticsearch')
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
        elastic_data[key] = []
        try:
            for location in input_json.pop(key):

                # Fix timestamps
                location['created'] = \
                    self.timestamp_from_string(location['created'])
                locobj = graph.Location.get_or_create(location).pop()
                dobj.located.connect(locobj)
                elastic_data[key].append(location['url'])

                # Add to elastic search suggestions
                es.get_or_create_suggestion(
                    es.GenericSuggestion,
                    text=location['url'], payload={'type': key})

        except Exception as e:
            logger.critical("Failed with %s: %s" % (key, e))
            return self.force_response(errors={key: 'invalid'})

        # Metadata
        key = 'metadata'
        elastic_data[key] = []
        for meta in input_json.pop(key):
            try:
                for k, v in meta.items():
                    metaobj = graph.MetaData.get_or_create(
                        {'key': k, 'value': v}).pop()
                    dobj.described.connect(metaobj)
                    elastic_data[key].append(v)

                    # Add to elastic search suggestions
                    es.get_or_create_suggestion(
                        es.GenericSuggestion,
                        text=v, payload={'type': '[%s] %s' % (key, k)})

            except Exception as e:
                logger.critical("Failed with %s: %s" % (key, e))
                return self.force_response(errors={key: 'invalid'})

        # Tags
        key = 'tags'
        elastic_data[key] = []
        for tag in input_json.pop(key):
            try:
                tagobj = \
                    graph.Tag.get_or_create({'name': tag}).pop()
                dobj.tagged.connect(tagobj)
                elastic_data[key].append(tag)

                # Add to elastic search suggestions
                es.get_or_create_suggestion(
                    es.GenericSuggestion,
                    text=tag, payload={'type': key})
            except Exception as e:
                logger.critical("Failed with %s: %s" % (key, e))
                return self.force_response(errors={key: 'invalid'})

        # Update the graph
        input_json['created'] = \
            self.timestamp_from_string(input_json['created'])
        input_json['updated'] = \
            self.timestamp_from_string(input_json['updated'])
        input_json['id'] = uuid

        ###
        key = 'logicalName'
        if key not in input_json:
            input_json[key] = os.path.basename(input_json['path'])
        elastic_data['name'] = input_json[key]

        # Add logicalName to elastic search suggestions
        es.get_or_create_suggestion(
            es.GenericSuggestion, text=input_json[key], payload={'type': key})

        ###
        key = 'format'
        if key not in input_json \
           or input_json[key] is None or input_json[key].strip() == '':
            # If missing format, take the extension in upper case
            if '.' in input_json['logicalName']:
                pos = input_json['logicalName'].index('.')
                input_json[key] = input_json['logicalName'][pos:].upper()

        # Add format to elastic search suggestions
        if input_json[key].strip() != '':
            elastic_data[key] = input_json[key]
            es.get_or_create_suggestion(
                es.GenericSuggestion,
                text=input_json[key], payload={'type': key})

        ################
        # Save the main object to graph
        graph.DataObject.create_or_update(input_json)
        # Save the main object to elasticsearch
        es.get_or_create(es.FedappCatalog, elastic_data, forced_id=dobj.id)
        # Note: we are using the same ID inside the graph and elasticsearch

        logger.debug("Updated obj %s" % dobj.id)

        # Return the UUID
        return uuid

    # @auth.login_required
    @decorate.apimethod
    def delete(self, uuid):

        graph = self.global_get_service('neo4j')
        es = self.global_get_service('elasticsearch')

        # Delete elasticsearch document
        try:
            es.FedappCatalog.get(uuid).delete()
        except Exception as e:
            logger.info("Failed to delete elastic id '%s'\n%s" % (uuid, e))
            pass

        # Recover the graph node
        try:
            dobj = graph.DataObject.nodes.get(id=uuid)
        except graph.ProvidedUser.DoesNotExist:
            return self.force_response(errors={uuid: 'could not be found'})
        logger.debug("Requested %s" % dobj)

        # Delete elasticsearch suggested name
        try:
            out = es.GenericSuggestion.search() \
                .query('match', suggestme=dobj.logicalName).execute()
            for element in out.to_dict()['hits']['hits']:
                es.GenericSuggestion.get(element['_id']).delete()
        except Exception as e:
            logger.info("Failed to remove elastic suggestion\n%s" % e)
            pass

        # Delete this graph node
        dobj.delete()

        return uuid


class ElasticSearch(ExtendedApiResource):

    # @auth.login_required
    @decorate.apimethod
    def get(self, keyword=None):

        ####################
        es = self.global_get_service('elasticsearch')
        print(es._connection)

        #############
        # # Insert example
        # print(es.GenericDocument, es._connection)
        # obj = es.GenericDocument(title="Paolo", type="Donorio")
        # obj.save()

        # # Wait if you want to have all recent data
        # import time
        # time.sleep(2)

        #############
        # Normal Search
        output = []
## // TO FIX:
# move to elastic class
        results = es.FedappCatalog.search().execute().to_dict()
        for element in results['hits']['hits']:
            output.append(element['_source'])

        return output

    # @auth.login_required
    @decorate.apimethod
    def post(self):
## TO BE FIXED

        parameters = self.get_input()
        if len(parameters) < 1:
            return self.force_response(
                errors={'parameters': 'no filters specified'})

        ####################
        es = self.global_get_service('elasticsearch')
        doc = es.FedappCatalog

        ############
        key = '_all'
        output = []

## // TO FIX:
# move to elastic class

        # Search the keyword on all parameters
        if key in parameters:
            # Match on multiple fields
# // TO FIX:
# search dynamically all fields inside the doc attributes?
            fields = [
                'name', 'format', 'owner', 'locations', 'metadata', 'tags'
            ]
            m = MultiMatch(fields=fields, query=parameters[key])
            results = doc.search().query(m).execute().to_dict()
            for element in results['hits']['hits']:
                # print("TEST", element)
                output.append({
                    '_data': element['_source'],
                    '_meta': {'id': element['_id'], 'score': element['_score']}
                })

        else:
            results = doc.search() \
                .filter('term', **parameters).execute().to_dict()
            for element in results['hits']['hits']:
                # print("TEST", element)
                output.append(element['_source'])

        return output


class ElasticSuggest(ExtendedApiResource):

    # @auth.login_required
    @decorate.apimethod
    def get(self, keyword=None):

        if keyword is None:
            return self.force_response(errors={'suggest': 'empty query'})

        es = self.global_get_service('elasticsearch')

        def manipulate(single):
            """ Manipulate the elasticsearch-dsl output """
            tmp = {}
            if 'payload' in single:
                for element in single.payload:
                    tmp[element] = getattr(single.payload, element)
            tmp['suggested'] = single.text
            return tmp

        return es.search_suggestion(
            es.GenericSuggestion, keyword, manipulate_output=manipulate)
