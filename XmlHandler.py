import json
import re
import Strings


class SimpleHandler:
    def __init__(self, key, element):
        self.key = key
        self.element = element
        self.properties = set()
        self.additional_items_to_create = set()

    def get_properties(self, uid_about):
        element_type = type(self.element)
        if element_type is dict or element_type is str:
            self.element = [self.element]
        for item in self.element:
            value = self.get_value(item)
            self.properties.add((uid_about, self.get_classifier(), value))
        return self.properties

    def get_value(self, element=None):
        if element is None:
            element = self.element
        value = ''
        if type(element) is str:
            value = element
        elif element.__contains__(Strings.rdf_resource_key):
            value = element[Strings.rdf_resource_key]
        elif element.__contains__(Strings.text_key):
            value = element[Strings.text_key]
        if self.is_uri(value):
            value = self.get_formatted_value(value)
        return value

    def get_classifier(self):
        return self.get_key_without_prefix() if self.contains_prefix() else self.key

    def get_key_without_prefix(self):
        return re.search(Strings.name_matcher, self.key).group()

    def contains_prefix(self):
        return self.has_match(self.key, Strings.prefix_matcher)

    def is_uri(self, value):
        return self.has_match(value, Strings.uri_matcher)

    def has_match(self, string, matcher):
        return re.search(matcher, string) is not None

    def get_formatted_value(self, unformatted_value):
        result = re.search(Strings.property_matcher, unformatted_value)
        value = unformatted_value if result is None else result.group()
        return value

    def get_additional_items_to_create(self):
        return self.additional_items_to_create


class Restriction(SimpleHandler):
    def __init__(self, element):
        SimpleHandler.__init__(self, Strings.owl_restriction_key, element)

    def get_properties(self, uid_about):
        value = self.get_value()
        relation = self.get_classifier()
        return {(uid_about, relation, value)}

    def get_value(self, element=None):
        if element is None:
            element = self.element
        if element.__contains__('%s' % Strings.owl_some_values_from_key):
            element = element[Strings.owl_some_values_from_key]
        elif element.__contains__('%s' % Strings.owl_has_value_key):
            element = element[Strings.owl_has_value_key]
        else:
            print('no someValuesOf or hasValue keys for {}'.format(repr(element)))
        if type(element) is list and len(element) > 1:
            print('someValuesOf/hasValue returned a list for {}'.format(repr(element)))
        return SimpleHandler.get_value(self, element)

    def get_classifier(self):
        return SimpleHandler.get_value(self, self.element['owl:onProperty'])


class SubClassOfKey(SimpleHandler):
    def __init__(self, element):
        SimpleHandler.__init__(self, Strings.rdfs_sub_class_of_key, element)

    def get_properties(self, uid_about):
        element_type = type(self.element)
        if element_type is dict or element_type is str:
            self.element = [self.element]
        for item in self.element:
            if item.__contains__(Strings.owl_restriction_key):
                restriction = item[Strings.owl_restriction_key]
                restriction_handler = Restriction(restriction)
                self.properties |= restriction_handler.get_properties(uid_about)
            else:
                value = self.get_value(item)
                if value is not '':
                    self.properties.add((uid_about, self.get_classifier(), value))
                else:
                    print('{}\t{}\t{}'.format(uid_about, 'subClassOf', json.dumps(item, indent=4)))
        return self.properties


class SimpleKeyWithPossibleValueList(SimpleHandler):
    def __init__(self, key):
        SimpleHandler.__init__(self, key)

    def get_value(self, element=None):
        if element is None:
            element = self.element
        if element.__contains__(Strings.rdf_resource_key):
            return SimpleHandler.get_value(self, element)
        elif element.__contains__(Strings.owl_class_key):
            try:
                union_element_list = element[Strings.owl_class_key][Strings.owl_union_of_key][Strings.rdf_description_key]
            except KeyError:
                return ''
            uid_about_key_handler = SimpleHandler(Strings.uid_about_key)
            union_list = list()
            for item in union_element_list:
                union_list.append(uid_about_key_handler.get_value(item[Strings.uid_about_key]))
            return union_list
        elif element.__contains__(Strings.rdfs_datatype_key):
            one_of_element_list = element[Strings.rdfs_datatype_key][Strings.owl_one_of_key][Strings.rdf_description_key]
            text_value_handler = SimpleHandler('generic_key')
            one_of_list = list()
            while one_of_element_list.__contains__(Strings.rdf_rest_key):
                one_of_list.append(text_value_handler.get_value(one_of_element_list[Strings.rdf_first_key]))
                one_of_element_list = one_of_element_list[Strings.rdf_rest_key]
                if one_of_element_list.__contains__(Strings.rdf_description_key):
                    one_of_element_list = one_of_element_list[Strings.rdf_description_key]
            return one_of_list
        else:
            return ''

    def is_value_a_property(self):
        return False


class RangeKey(SimpleKeyWithPossibleValueList):
    def __init__(self):
        SimpleKeyWithPossibleValueList.__init__(self, Strings.rdfs_range_key)


class DomainKey(SimpleKeyWithPossibleValueList):
    def __init__(self):
        SimpleKeyWithPossibleValueList.__init__(self, Strings.rdfs_domain_key)

