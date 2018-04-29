from typing import List

from .node_representation import Node


class Reference:
    def __init__(self, document_id, keys):
        self.__document_id__ = document_id
        self.__keys__ = keys

    @property
    def document_id(self):
        return self.__document_id__

    @property
    def keys(self):
        return self.__keys__


class Link:
    # keep a global list of references visited
    REFERENCE_CACHE_BUCKET = {}

    def __init__(self, id, target, source, references, value, graph, *args, **kwargs):
        self.__link_id__ = id
        self.__target__ = str(target)
        self.__source__ = str(source)
        self.__references__ = []
        self.__value__ = value
        self.__graph__ = graph

        for document_id, reference_list in references.items():
            self.__references__.append(Reference(document_id=document_id, keys=reference_list))

    @property
    def link_id(self):
        return self.__link_id__

    @property
    def target(self) -> Node:
        return self.__graph__.node_by_id(self.__target__)

    @property
    def source(self) -> Node:
        return self.__graph__.node_by_id(self.__source__)

    @property
    def references(self) -> List[Reference]:
        return self.__references__

    @property
    def value(self):
        return self.__value__

    @staticmethod
    def load_link(link_obj, graph):
        return Link(graph=graph, **link_obj)

    def load_references(self, api_loader):
        REFERENCE_CACHE_BUCKET = Link.REFERENCE_CACHE_BUCKET

        references = []

        for reference in self.references:
            document_id = reference.document_id

            try:
                reference_dict = REFERENCE_CACHE_BUCKET[document_id]
            except KeyError:
                reference_dict = {}
                REFERENCE_CACHE_BUCKET[document_id] = reference_dict

            all_keys = []
            for connected_words in reference.keys:
                if connected_words:
                    all_keys.extend(connected_words)
            all_keys = list(set(all_keys))
            for connected_words in all_keys:
                if connected_words in reference_dict:
                    continue
                text_reference = api_loader.get_entity_reference(document_id=document_id,
                                                                 connected_words=connected_words)
                reference_dict[connected_words] = text_reference

            for connected_words in reference.keys:
                if connected_words:
                    text_references = [reference_dict.get(connected_word) for connected_word in connected_words]
                    references.extend(text_references)
        return references


def load_link(link_obj, graph) -> Link:
    return Link.load_link(link_obj, graph)
