# -*- coding: utf-8 -*-

"""
Graph DB abstraction from neo4j server.
These are custom models!

VERY IMPORTANT!
Imports and models have to be defined/used AFTER normal Graphdb connection.
"""

from __future__ import absolute_import
from neomodel import \
    DateTimeProperty, StringProperty, IntegerProperty, \
    StructuredNode, RelationshipTo, RelationshipFrom, \
    One, OneOrMore, ZeroOrMore

# from common.logs import get_logger
# logger = logging.get_logger(__name__)


##################
# MODELS
##################

class ProvidedUser(StructuredNode):
    username = StringProperty(required=True, unique_index=True)
    owning = RelationshipFrom(
        'DataObject', 'IS_OWNED_BY', cardinality=One)
    _fields_to_show = ['username']


class Location(StructuredNode):
    url = StringProperty(required=True, unique_index=True)
    created = DateTimeProperty()
    locating = RelationshipFrom(
        'DataObject', 'IS_LOCATED_TO', cardinality=OneOrMore)
    _fields_to_show = ['url', 'created']


class MetaData(StructuredNode):
    key = StringProperty(required=True, unique_index=True)
    value = StringProperty()
    describing = RelationshipFrom(
        'DataObject', 'DESCRIBED_BY', cardinality=ZeroOrMore)
    _fields_to_show = ['key', 'value']


class Tag(StructuredNode):
    name = StringProperty(required=True, unique_index=True)
    tagging = RelationshipFrom(
        'DataObject', 'TAGGED_WITH', cardinality=ZeroOrMore)
    _fields_to_show = ['name']


class DataObject(StructuredNode):
    id = StringProperty(required=True, unique_index=True)   # UUID

    logicalName = StringProperty(index=True)
    path = StringProperty()
    description = StringProperty()
    created = DateTimeProperty()
    updated = DateTimeProperty()
    size = IntegerProperty()
    # optional(s)
    checksum = StringProperty()
    format = StringProperty()

## TO FIX: add cardinality
    owned = RelationshipTo('ProvidedUser', 'IS_OWNED_BY')
    located = RelationshipTo('Location', 'IS_LOCATED_TO')
    tagged = RelationshipTo('Tag', 'TAGGED_WITH')
    described = RelationshipTo('MetaData', 'DESCRIBED_BY')

    _fields_to_show = ['location', 'logicalName', 'path', 'size', 'format']
    _relationships_to_follow = ['owned', 'located', 'tagged', 'described']
