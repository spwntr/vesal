import DataIO


tag_rdf = 'rdf:type'
tag_sub_class_of = 'rdfs:subClassOf'

elements = DataIO.get_dict_gz_as_json('owl:ObjectProperty')

distinct_keys = set()
nested_distinct_keys = set()

fma_id_count = 0
subclass_count = 0
pn_count = 0
classes = 0


for element in elements:
    # if dict(element).__contains__('FMAID'):
    #     fma_id_count += 1
    #     fmaid_text_ = str()
    #     if type(element['FMAID']) is dict:
    #         fmaid_text_ = element['FMAID']['#text'] if element['FMAID'].__contains__('#text') else element['FMAID']
    #     else:
    #         print('f')
    #         fmaid_text_ = element['FMAID'][0]['#text']
    #     if fmaid_text_.__eq__('7088'):
    #         print('n')
    #     if dict(element).__contains__(tag_sub_class_of):
    #         subclass_count += 1
    #         sub_class_of_ = element[tag_sub_class_of]
    #         i = len(sub_class_of_)
    #         pn_count += i
    #         if i > 2:
    #             print(fmaid_text_ + " " + str(i))
    #         if (sub_class_of_.__contains__('owl:Class')):
    #             classes += 1

    for key in element.keys():
        distinct_keys.add(key)
        print(element[tag_rdf]) if dict(element).__contains__(tag_rdf) \
            else print(element)
    if key.__eq__(tag_sub_class_of):
        nested_sub_class_of = element[tag_sub_class_of]
        if len(nested_sub_class_of).__eq__(1):
            nested_distinct_keys.add(list(nested_sub_class_of.keys())[0])
        else:
            for nested_sub_class in nested_sub_class_of:
                nested_distinct_keys.add(list(nested_sub_class.keys())[0])
print('s')
