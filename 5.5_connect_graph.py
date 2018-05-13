import logging
import os
import re
from _datetime import datetime
from sys import stdout

from neo4j.util import watch
from neo4j.v1 import GraphDatabase

SORTED_DATA_PATH = os.getcwd() + '/data/sorted'

watch("neo4j.bolt", logging.DEBUG, stdout)

NEO4J_LOAD_CSV_W_HEADERS = "LOAD CSV WITH HEADERS "

project_dir = os.getcwd()

start_time = datetime.now()

driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "pw4neo"))

label_properties = ['FMAID', 'label', 'has_boundary', 'has_dimension', 'has_inherent_3-D_shape', 'has_mass', 'preferred_name', 'synonym', 'slot_synonym']
text_properties = ['range', 'comment', 'cell_appendage_type', 'days_post-fertilization', 'definition', 'dimension', 'Eponym', 'fma0329122', 'has_direct_cell_layer', 'has_direct_number_of_pairs_per_nucleus', 'has_direct_ploidy', 'has_direct_shape_type', 'JHU_DTI-81', 'JHU_White-Matter_Tractography_Atlas', 'non-English_equivalent', 'physical_state', 'polarity', 'species', 'state_of_determination', 'type', ]
id_properties = ['AAL', 'CMA_label', 'DK__Freesurfer', 'EuProstate16', 'EuProstate27', 'Neurolex', 'PIRADSv2', 'RadLex_ID', 'Talairach', ]

obj_pro_label_properties = ['FMAID', 'label', 'slot_synonym', 'synonym', ]
obj_pro_text_properties = ['definition', 'type', ]
obj_pro_id_properties = ['RO_ID']


def get_file_path(filename):
    return 'file:///{}/data/sorted/{}'.format(project_dir, filename)


def import_label_properties(tx, csv_filename, label, label_property):
    tx.run(NEO4J_LOAD_CSV_W_HEADERS +
        "FROM $file AS line "
        "MATCH (subject:" + label + " { about: line.Subject }) "
        "SET subject." + label_property + " = line.Object",
           file=csv_filename)


def import_text_properties(tx, csv_filename, label, object_property):
    tx.run(NEO4J_LOAD_CSV_W_HEADERS +
        "FROM $file AS line "
        "MATCH (subject:" + label + " { about: line.Subject }) "
        "MERGE (object:" + object_property + " { text: line.Object }) "
        "MERGE (subject)-[r:HAS_" + object_property.upper() + "]->(object)",
           file=csv_filename)


def import_id_properties(tx, csv_filename, label, object_property):
    tx.run(NEO4J_LOAD_CSV_W_HEADERS +
        "FROM $file AS line "
        "MATCH (subject:" + label + " { about: line.Subject }) "
        "MERGE (object:" + object_property + " { id: line.Object }) "
        "MERGE (subject)-[r:HAS_" + object_property.upper() + "]->(object)",
           file=csv_filename)


def import_relationships(tx, csv_filename, label, relationship):
    tx.run(NEO4J_LOAD_CSV_W_HEADERS +
        "FROM $file AS line "
        "MATCH (subject:" + label + " { about: line.Subject }), (object { about: line.Object }) "
        "MERGE (subject)-[r:" + relationship.upper() + "]->(object)",
           file=csv_filename)


files_to_import = os.listdir(SORTED_DATA_PATH)
counter = 0
with driver.session() as session:
    for filename in files_to_import:
        counter += 1
        trim_has = True
        import_function = import_relationships
        split_filename = re.sub('owl__', '', filename).split('.')
        label = split_filename[0]
        descriptor = split_filename[1]
        if label.__eq__('ObjectProperty'):
            if obj_pro_label_properties.__contains__(descriptor):
                import_function = import_label_properties
                trim_has = False
            elif obj_pro_text_properties.__contains__(descriptor):
                import_function = import_text_properties
            elif obj_pro_id_properties.__contains__(descriptor):
                import_function = import_id_properties
        else:
            if label_properties.__contains__(descriptor):
                import_function = import_label_properties
            elif text_properties.__contains__(descriptor):
                import_function = import_text_properties
            elif id_properties.__contains__(descriptor):
                import_function = import_id_properties

        if trim_has:
            descriptor = re.sub('^has_', '', descriptor)

        descriptor = re.sub('-', '', descriptor)

        session.write_transaction(import_function, get_file_path(filename), label, descriptor)

        print('{}:\t{}:\t{}'.format(counter, label, descriptor))

print('process time: {}'.format(datetime.now() - start_time))
