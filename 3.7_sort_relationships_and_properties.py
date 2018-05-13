import json
from datetime import datetime

import DataIO
import HandlerService
import Strings


# elements = DataIO.get_dict_gz_as_json(Strings.owl_class_key)
data_key = Strings.owl_class_key
elements = DataIO.get_dict_gz_as_json(data_key)
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


def sort_properties(properties_to_create):
    sorted_data = {}
    for triplet in properties_to_create:
        if not sorted_data.keys().__contains__(triplet[1]):
            sorted_data[triplet[1]] = set()
        sorted_data[triplet[1]].add((triplet[0], triplet[2]))
    return sorted_data


sorted_data = sort_properties(properties_to_create)
for handle in sorted_data.keys():
    DataIO.write_csv(sorted_data[handle], data_key + '.' + handle, ['Subject', 'Object'], True)
