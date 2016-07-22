# -*- coding: utf-8 -*-

""" Custom models for elastic search """

# from __future__ import absolute_import
# from ..logs import get_logger

from elasticsearch_dsl import DocType, String, Completion
from elasticsearch_dsl import analyzer, tokenizer


# my_analyzer = analyzer(
#     'my_analyzer',
#     tokenizer=tokenizer('trigram', 'nGram', min_gram=2, max_gram=3),
#     filter=['lowercase']
# )

# logger = get_logger(__name__)
# logger.info("Things to do")


class GenericDocument(DocType):

    title = Completion(payloads=True)
    # title = String(analyzer=my_analyzer)
    type = String()

    class Meta:
        index = 'myindex'
