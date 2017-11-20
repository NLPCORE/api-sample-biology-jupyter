import ujson as json


class NodeAttribute:
    def __init__(self, group_name, properties):
        self.__group_name__ = group_name
        self.__properties__ = properties

    @property
    def group_name(self):
        return self.__group_name__

    @property
    def properties(self):
        return self.__properties__

    def __repr__(self):
        return "{Node Attribute:, group_name: %s}" % self.group_name


# to make the class inherently json serializable, it was inheritted from dict class
class Node(dict):
    __id__ = None
    __immutable__ = None
    __count__ = None
    __group__ = None
    __n_name__ = None
    __document_ids__ = None
    __inward_reference__ = None
    __outward_reference__ = None
    __attributes__ = None
    __links_id__ = None

    def __init__(self, name, id, document_id, link_ids, attributes=None, count=1, inward_reference=1,
                 outward_reference=1, immutable=False):
        # initialize an empty list for document_id(s)
        self.__document_ids__ = []
        self.count = count
        self.id = id
        self.name = name
        self.inward_reference = inward_reference
        self.outward_reference = outward_reference
        self.document_ids = document_id
        self['paper_id'] = self.document_ids
        self.attributes = attributes
        self.immutable = immutable
        self.__links_id__ = link_ids

    @property
    def id(self):
        return self.__id__

    @id.setter
    def id(self, value):
        self.__id__ = value
        self['id'] = value

    @property
    def immutable(self):
        return self.__immutable__

    @immutable.setter
    def immutable(self, value):
        self.__immutable__ = value

    @property
    def count(self):
        return self.__count__

    @count.setter
    def count(self, value):
        self.__count__ = value
        self['count'] = value

    @property
    def name(self):
        return self.__n_name__

    @name.setter
    def name(self, value):
        self.__n_name__ = value
        self['name'] = value

    @property
    def document_ids(self):
        return self.__document_ids__

    @document_ids.setter
    def document_ids(self, value):
        if value not in self.__document_ids__:
            self.__document_ids__.append(value)

    @property
    def inward_reference(self):
        return self.__inward_reference__

    @inward_reference.setter
    def inward_reference(self, value):
        self.__inward_reference__ = value
        self['inward_reference'] = value

    @property
    def outward_reference(self):
        return self.__outward_reference__

    @outward_reference.setter
    def outward_reference(self, value):
        self.__outward_reference__ = value
        self['outward_reference'] = value

    @property
    def attributes(self):
        return self.__attributes__

    @attributes.setter
    def attributes(self, value):
        self.__attributes__ = value
        self['attributes'] = value

    def has_attribute(self, attribute_name):
        for attr in self.__attributes__:
            if attribute_name in (attr['at'] or {}):
                return True
        return False

    def is_group_type(self, group_name):
        for attr in self.__attributes__:
            if attr['et'].lower() == group_name:
                return True
        return False

    def get_attributes(self) -> NodeAttribute:
        for attr in self.__attributes__:
            yield NodeAttribute(group_name=attr['et'], properties=attr['at'])

    @staticmethod
    def load_node(node_obj, link_ids):
        paper_ids = node_obj.pop('paper_id')
        node = None
        for paper_id in paper_ids:
            if node is None:
                node_obj['document_id'] = paper_id
                node = Node(**node_obj, link_ids=link_ids)
            else:
                node.document_ids = paper_id
        return node

    def get_references(self, api_loader):
        references = []
        for link_obj in self.__links_id__:
            references.extend(link_obj.load_references(api_loader))
        return references

    def __repr__(self):
        return json.dumps({'id': self.id, 'name': self.name, 'paper_id': self.document_ids, 'count': self.count,
                           'inward_reference': self.inward_reference, 'outward_reference': self.outward_reference,
                           'attributes': self.attributes})
