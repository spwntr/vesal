import Strings
import XmlHandler


current_handler = None

key_handler_map = {
    # Strings.rdfs_range_key: XmlHandler.RangeKey(),
    # Strings.rdfs_domain_key: XmlHandler.DomainKey(),
    Strings.rdfs_sub_class_of_key:  XmlHandler.SubClassOfKey,
}


def get_handler(key, element):
    global current_handler
    handler = key_handler_map.__getitem__(key)(element) if key_handler_map.keys().__contains__(key) \
        else XmlHandler.SimpleHandler(key, element)
    current_handler = handler
    return handler


def get_value(key, element):
    return get_handler(key, element).get_value()


def get_properties(uid_about, key, element):
    return get_handler(key, element).get_properties(uid_about)


def get_additional_items_to_create():
    global current_handler
    return current_handler.get_additional_items_to_create()

