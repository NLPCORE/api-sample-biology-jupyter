def print_node_attributes(node):
    print("\t Node Properties:")
    for attribute in node.get_attributes():
        properties = attribute.properties or {}
        for attribute_name, property in properties.items():
            print("\t\t %s: %s" % (attribute_name, property))
        print("\n")

