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
class Node:
    __id__ = None
    __immutable__ = None
    __count__ = None
    __node_name__ = None

    __document_ids__ = None
    __inward_reference__ = None
    __outward_reference__ = None
    __attributes__ = None
    __proper_noun__ = None

    # Not to be serialized
    __unique_attributes__ = None

    def __init__(self, name=None, node_id=None, document_ids=None, attributes=None, count=1, inward_reference=1,
                 outward_reference=1, immutable=False, proper_noun=None, document_id=None, link_ids=None):
        self.__id__ = node_id
        self.__count__ = count
        self.__node_name__ = name
        self.__group__ = name
        self.__document_ids__ = document_ids or []
        if document_id:
            self.__document_ids__.append(document_id)

        self.__inward_reference__ = inward_reference
        self.__outward_reference__ = outward_reference
        self.__immutable__ = immutable

        self.__proper_noun__ = proper_noun
        self.__attributes__ = attributes or []
        self.__unique_attributes__ = set()
        self.__links_id__ = link_ids

    @property
    def id(self):
        return self.__id__

    @id.setter
    def id(self, new_id):
        self.__id__ = new_id

    @property
    def immutable(self):
        return self.__immutable__

    @immutable.setter
    def immutable(self, value):
        assert isinstance(value, bool), "Immutable value should be a boolean."
        self.__immutable__ = value

    @property
    def count(self):
        return self.__count__

    def increment_count(self, value=1):
        self.__count__ += 1

    @property
    def name(self):
        return self.__node_name__

    @property
    def document_ids(self):
        return self.__document_ids__

    @property
    def inward_reference(self):
        return self.__inward_reference__

    def increment_inward_reference(self, value=1):
        self.__inward_reference__ += value

    @property
    def outward_reference(self):
        return self.__outward_reference__

    def increment_outward_reference(self, value=1):
        self.__outward_reference__ += value

    @property
    def attributes(self):
        return self.__attributes__

    @attributes.setter
    def attributes(self, value):
        self.__attributes__ = value

    def add_attribute(self, attribute):
        add = self.__unique_attributes__.add
        if len(self.__unique_attributes__) == 0:
            [add(json.dumps(_attribute)) for _attribute in self.attributes]
        hash = json.dumps(attribute)
        if hash not in self.__unique_attributes__:
            self.__attributes__.append(attribute)
            self.__unique_attributes__.add(hash)

    @property
    def proper_noun(self):
        return self.__proper_noun__

    @staticmethod
    def from_object(obj, link_ids) -> 'Node':
        id = obj.pop('id')
        return Node(node_id=id, link_ids=link_ids, **obj)

    def to_object(self):
        return {'name': self.name, 'node_id': self.id, 'document_ids': self.document_ids, 'attributes': self.attributes,
                'count': self.count, 'inward_reference': self.inward_reference,
                'outward_reference': self.outward_reference, 'immutable': self.immutable,
                'proper_noun': self.proper_noun}

    def to_object_with_priority(self):
        obj = self.to_object()
        obj['id'] = obj.pop('node_id')
        return obj

    def get_references(self, api_loader):
        references = []
        for link_obj in self.__links_id__:
            references.extend(link_obj.load_references(api_loader))
        return references

    def __repr__(self):
        return json.dumps({'id': self.id, 'name': self.name, 'paper_id': self.document_ids, 'count': self.count,
                           'inward_reference': self.inward_reference, 'outward_reference': self.outward_reference,
                           'attributes': self.attributes})

    def has_attribute(self, attribute_name):
        for attr in self.__attributes__:
            if attribute_name in (attr['at'] or {}):
                return True
        return False

    def get_attributes(self) -> NodeAttribute:
        for attr in self.__attributes__:
            yield NodeAttribute(group_name=attr['et'], properties=attr['at'])

