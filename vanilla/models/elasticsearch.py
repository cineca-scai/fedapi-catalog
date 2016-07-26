# -*- coding: utf-8 -*-

""" Custom models for elastic search """

# from __future__ import absolute_import
# from ..logs import get_logger

from elasticsearch_dsl import DocType, String, Completion

# from elasticsearch_dsl import analyzer, tokenizer

# my_analyzer = analyzer(
#     'my_analyzer',
#     tokenizer=tokenizer('trigram', 'nGram', min_gram=2, max_gram=3),
#     filter=['lowercase']
# )


# logger = get_logger(__name__)
# logger.info("Things to do")


class GenericDocument(DocType):

    key = String()
    value = String()

    class Meta:
        index = 'generic'


class GenericSuggestion(DocType):

    suggestme = Completion(payloads=True)

    class Meta:
        index = 'suggestion'


class FedappCatalog(DocType):

    name = String()
    format = String()
    owner = String()

    locations = String()  # this is a list
    metadata = String()  # this is a list
    tags = String()  # this is a list

    # metadata = Nested(
    #     doc_class=Metadata,
    #     properties={
    #         'key': String()
    #     }
    # )

    class Meta:
        index = 'generic'
