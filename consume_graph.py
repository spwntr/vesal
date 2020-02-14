import json
import logging
from sys import stdout

from neobolt.diagnostics import watch
from neo4j import GraphDatabase

UNQUERYABLE = ['Left ventricle', 'Right ventricle', 'Right adrenal gland', 'Left adrenal gland', 'Ureter', 'Esophagus',
               'Myocardium of left atrium', 'Myocardium of right atrium', 'Myocardium of right ventricle',
               'Myocardium of left ventricle', 'Left atrium', 'Right atrium', 'Hippocampus proper', 'Clavicle',
               'Small intestine', 'Deltoid', 'Urinary bladder', 'Left kidney', 'Right kidney',
               'Anterior wall of right ventricle', 'Lung', 'Right clavicle', 'Left clavicle',
               'Superior segment of right kidney', 'Superior segment of left kidney', 'Superior segment of kidney',
               'Wall of tail of epididymis', 'Midbrain', 'Precentral gyrus', 'Postcentral gyrus', 'Kidney', ]
MYOCARDIAL_ZONE = 'Myocardial zone'
RENAL_SEGMENT = 'renal segment'

watch("neo4j.bolt", logging.DEBUG, stdout)


def query_for_blood_paths(tx, tissue):
    return tx.run(
        "MATCH ({ preferred_name: $tissue })-[:ARTERIAL_SUPPLY]->(n), "
        "(a { preferred_name: 'Aorta' }), "
        "p = shortestPath((a)-[:REGIONAL_PART_OF|:CONTINUOUS_DISTALLY_WITH|:BRANCH_OF*]-(n)) "
        "WHERE NONE(x IN NODES(p) WHERE x:Class AND x.preferred_name = 'Systemic arterial tree') "
        "RETURN extract(i IN NODES(p) | i.preferred_name)"
        , tissue=tissue
    )


def query_for_tissues_w_arterial_supply_defined(tx):
    return tx.run(
        "MATCH (n)-[:ARTERIAL_SUPPLY]->() "
        "WITH DISTINCT n "
        "RETURN collect(n.preferred_name)"
    )


def import_all_blood_paths():
    driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "pw4neo"))

    with driver.session() as session:
        tissues = session.write_transaction(query_for_tissues_w_arterial_supply_defined)

        counter = 1
        questions = []
        for tissue in tissues._records[0][0]:
            if not tissue.__contains__(RENAL_SEGMENT) and not tissue.__contains__(MYOCARDIAL_ZONE) \
                    and not UNQUERYABLE.__contains__(tissue):
                blood_paths = session.write_transaction(query_for_blood_paths, tissue)
                for path in blood_paths._records:
                    questions.append({
                        'id': counter,
                        'subject': tissue,
                        'blood_path': path[0]
                    })
                    counter += 1
                    print(counter)

    with open('data/questions.json', 'w') as file:
        json.dump(questions, file, indent=4)
