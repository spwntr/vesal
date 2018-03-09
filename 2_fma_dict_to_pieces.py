import DataIO

rdf_rdf = 'rdf:RDF'
owl_ontology = 'owl:Ontology'
owl_annotation_property = 'owl:AnnotationProperty'
owl_axiom = 'owl:Axiom'
rdf_description = 'rdf:Description'
owl_object_property = 'owl:ObjectProperty'
owl_datatype_property = 'owl:DatatypeProperty'
owl_named_individual = 'owl:NamedIndividual'
owl_class = 'owl:Class'


fma = DataIO.get_dict_gz_as_json('fma_v4.10.0')

namespace_array = [owl_ontology, owl_annotation_property, owl_axiom, rdf_description, owl_object_property,
                   owl_datatype_property, owl_named_individual, owl_class]

DataIO.write_fma_components(fma, rdf_rdf, namespace_array)
