import json
import re

import DataIO
import Strings

tag_rdf = 'rdf:type'
tag_sub_class_of = 'rdfs:subClassOf'

namespaces = [
    'owl:DatatypeProperty',
    # 'owl:AnnotationProperty',
    # 'owl:ObjectProperty',
    # 'owl:Class'
]


def extract_properties(namespace):
    elements = DataIO.get_dict_gz_as_json(namespace)

    print(json.dumps(elements, indent=4))

    count_tag = 'count'
    key_tally = {}
    distinct_items = set()
    # nested_distinct_keys = set()

    for element in elements:
        for key in element.keys():
            key_dict = {}
            if key_tally.keys().__contains__(key):
                key_dict = key_tally[key]
                key_dict[count_tag] += 1
            else:
                key_dict[count_tag] = 1
            if key.__eq__('@rdf:about'):
                about = element['@rdf:about']
                result = re.search(Strings.property_matcher, about)
                about = about if result is None else result.group()
                distinct_items.add(about)
            else:
                thing = element[key]
                typed = type(thing)
                if typed is dict:
                    stuff = thing.keys()
                elif typed is str:
                    stuff = []
                else:
                    stuff = thing
                for item in stuff:
                    additional_stuff = 0
                    if type(item) is str:
                        item = [item]
                    elif type(item) is dict:
                        item = list(item.keys())
                    for a in item:
                        if key_dict.keys().__contains__(a):
                            key_dict[a] += 1 + additional_stuff
                        else:
                            key_dict[a] = 1 + additional_stuff
            key_tally[key] = key_dict
            # if key.__eq__(tag_sub_class_of):
            #     nested_sub_class_of = element[tag_sub_class_of]
            #     if len(nested_sub_class_of).__eq__(1):
            #         nested_distinct_keys.add(list(nested_sub_class_of.keys())[0])
            #     else:
            #         for nested_sub_class in nested_sub_class_of:
            #             nested_distinct_keys.add(list(nested_sub_class.keys())[0])
    # print(distinct_items)
    print('\n\n')
    print(json.dumps(key_tally, indent=4))


for namespace in namespaces:
    extract_properties(namespace)
