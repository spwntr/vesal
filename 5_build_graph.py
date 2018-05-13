import logging
import os
from _datetime import datetime
from sys import stdout

from neo4j.util import watch
from neo4j.v1 import GraphDatabase

watch("neo4j.bolt", logging.DEBUG, stdout)

neo4j_load_csv_w_headers = "LOAD CSV WITH HEADERS "

data_labels = [
    {"file_label": "dat_pro_",
     "neo_node_label": "DatatypeProperty"},
    {"file_label": "obj_pro_",
     "neo_node_label": "ObjectProperty"},
    {"file_label": "ann_pro_",
     "neo_node_label": "AnnotationProperty"},
    {"file_label": "",
     "neo_node_label": "Class"},
]

project_dir = os.getcwd()

start_time = datetime.now()

driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "pw4neo"))


def set_unique_constraint_on_about_for_type(tx, label_type):
    tx.run("CREATE CONSTRAINT ON (n:" + label_type + ") ASSERT n.about IS UNIQUE")


def import_nodes(tx, csv_location, label):
    tx.run(neo4j_load_csv_w_headers
           + "FROM $file AS line "
             "MERGE (:" + label + " { about: line.Item })",
           file=csv_location)


with driver.session() as session:
    session.write_transaction(set_unique_constraint_on_about_for_type, 'Class')
    session.write_transaction(set_unique_constraint_on_about_for_type, 'ObjectProperty')
    session.write_transaction(set_unique_constraint_on_about_for_type, 'AnnotationProperty')
    session.write_transaction(set_unique_constraint_on_about_for_type, 'DatatypeProperty')

    for label in data_labels:
        nodes_csv = "file:///{}/data/{}nodes.csv".format(project_dir, label.get("file_label"))
        properties_csv = "file:///{}/data/{}properties.csv".format(project_dir, label.get("file_label"))

        session.write_transaction(import_nodes, nodes_csv, label.get("neo_node_label"))


print('process time: {}'.format(datetime.now() - start_time))
