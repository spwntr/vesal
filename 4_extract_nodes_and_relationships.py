import json
from datetime import datetime

import DataIO
import HandlerService
import Strings


elements = DataIO.get_dict_gz_as_json(Strings.owl_class_key)
# elements = elements[10110:10150]

unprocessed_properties_count = 0

start_time = datetime.now()
special_handler_keys = HandlerService.key_handler_map.keys()
items_to_create = set()
properties_to_create = set()
for element in elements:
    if element.__contains__(Strings.uid_about_key):
        uid_about = HandlerService.get_value(Strings.uid_about_key, element[Strings.uid_about_key])
        items_to_create.add(uid_about)
        for key, item in element.items():
            if not key.__eq__(Strings.uid_about_key):
                new_properties = HandlerService.get_properties(uid_about, key, item)
                for thing in new_properties:
                    if thing[2].__eq__(''):
                        unprocessed_properties_count += 1
                        # print('{}\t{}\t{}\t{}'.format(thing[0], key, thing[1], json.dumps(item, indent=4)))
                    else:
                        properties_to_create.add(thing)
                # properties_to_create |= new_properties
                new_items = HandlerService.get_additional_items_to_create()
                # if len(new_items) > 0:
                #     print('created additional items: {}'.format(repr(new_items)))
                items_to_create |= new_items

    # if len(items_to_create) % 1000 == 0:
    #     print('current process time: {}'.format(datetime.now() - start_time))
    #     print('So far added {} items and {} properties. Skipped {} properties.'
    #           .format(len(items_to_create), len(properties_to_create), unprocessed_properties_count))

print('process time: {}'.format(datetime.now() - start_time))
print('Added {} items.\nAdded {} properties.\nDid not process {} properties.'
      .format(len(items_to_create), len(properties_to_create), unprocessed_properties_count))
print('')

DataIO.write_csv(items_to_create, 'nodes', ['Item'])
DataIO.write_csv(properties_to_create, 'properties', ['Subject', 'Predicate', 'Object'])

"""
all
process time: 0:00:35.987963
Added 104523 items.
Added 671317 properties.
Did not process 1983 properties.
"""

"""
Data structure

Classes
+ contains all 3 subClassOf has Class:IntersectionOf
elements = elements[2380:2383]

+ contains all 2 FMAIDs as lists
elements = elements[51787:51789]
elements = elements[51902:51904]

fma14197	key: definition processing returned value: 		{'@rdf:datatype': 'http://www.w3.org/2001/XMLSchema#string'}
fma0325915	key: preferred_name processing returned value: 		{'@rdf:datatype': 'http://www.w3.org/2001/XMLSchema#string'}
fma0326951	key: rdfs:comment processing returned value: 		{'@rdf:datatype': 'http://www.w3.org/2001/XMLSchema#string'}
fma321270	key: FMAID processing returned value: 		[{'@rdf:datatype': 'http://www.w3.org/2001/XMLSchema#integer', '#text': '321270'}, {'@rdf:datatype': 'http://www.w3.org/2001/XMLSchema#string', '#text': 'Space of L5-S1 intervertebral compartment'}]
fma322277	key: preferred_name processing returned value: 		{'@rdf:datatype': 'http://www.w3.org/2001/XMLSchema#string'}
fma322603	key: preferred_name processing returned value: 		{'@rdf:datatype': 'http://www.w3.org/2001/XMLSchema#string'}

ObjectProperty (about is equivalent to label except as below)
+ branch__continuity_ for '@rdf:about' value has extra '_' between words and trailing '_' and for 'en' label has extra ' ' between words 
+ tributary__continuity_ for '@rdf:about' value has extra '_' between words and trailing '_' and for 'en' label has extra ' ' between words

+ 'matures from' has two '@xml:lang':'en', '#text':'*' labels, a) 'matures_from' b) 'matures from'
+ 'matures into' has two '@xml:lang':'en', '#text':'*' labels, a) 'matures_into' b) 'matures into'
"""
