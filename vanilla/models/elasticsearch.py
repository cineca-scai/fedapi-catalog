# -*- coding: utf-8 -*-

""" Custom models for elastic search """

# from __future__ import absolute_import
# from ..logs import get_logger

from elasticsearch_dsl import DocType, String, Completion
# Date, Nested, Boolean, \
# analyzer, InnerObjectWrapper,

# logger = get_logger(__name__)
# logger.info("Things to do")


class GenericDocument(DocType):

    title = String()
    title_suggest = Completion(payloads=True)

    class Meta:
        index = 'myindex'
