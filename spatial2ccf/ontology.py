import re

from spatial2ccf.namespace import CCF

from rdflib import Graph, URIRef, Literal
from rdflib import OWL, XSD, RDF, DC, DCTERMS
from rdflib.extras.infixowl import Ontology, Class, Property


class SPOntology:
    """CCF Spatial Ontology
    Represents the Spatial Ontology graph that can be mutated by supplying
    the HuBMAP RUI records
    """
    def __init__(self, graph=None):
        self.graph = graph

    @staticmethod
    def new(ontology_iri):
        g = Graph()
        g.bind('ccf', CCF)
        g.bind('owl', OWL)
        g.bind('dc', DC)
        g.bind('dcterms', DCTERMS)

        # Ontology properties
        Ontology(identifier=URIRef(ontology_iri), graph=g)

        # Declaration axioms
        Property(CCF.belongs_to_extraction_set, baseType=OWL.ObjectProperty, graph=g)
        Property(CCF.extraction_set_for, baseType=OWL.ObjectProperty, graph=g)
        Property(CCF.has_placement_target, baseType=OWL.ObjectProperty, graph=g)
        Property(CCF.has_reference_organ, baseType=OWL.ObjectProperty, graph=g)
        Property(CCF.has_object_reference, baseType=OWL.ObjectProperty, graph=g)
        Property(CCF.has_placement, baseType=OWL.ObjectProperty, graph=g)

        Property(CCF.title, baseType=OWL.DatatypeProperty, graph=g)
        Property(CCF.creator_first_name, baseType=OWL.DatatypeProperty, graph=g)
        Property(CCF.creator_last_name, baseType=OWL.DatatypeProperty, graph=g)
        Property(CCF.creator_orcid, baseType=OWL.DatatypeProperty, graph=g)
        Property(CCF.creation_date, baseType=OWL.DatatypeProperty, graph=g)
        Property(CCF.organ_owner_sex, baseType=OWL.DatatypeProperty, graph=g)
        Property(CCF.organ_side, baseType=OWL.DatatypeProperty, graph=g)
        Property(CCF.x_dimension, baseType=OWL.DatatypeProperty, graph=g)
        Property(CCF.y_dimension, baseType=OWL.DatatypeProperty, graph=g)
        Property(CCF.z_dimension, baseType=OWL.DatatypeProperty, graph=g)
        Property(CCF.dimension_unit, baseType=OWL.DatatypeProperty, graph=g)
        Property(CCF.x_scaling, baseType=OWL.DatatypeProperty, graph=g)
        Property(CCF.y_scaling, baseType=OWL.DatatypeProperty, graph=g)
        Property(CCF.z_scaling, baseType=OWL.DatatypeProperty, graph=g)
        Property(CCF.scaling_unit, baseType=OWL.DatatypeProperty, graph=g)
        Property(CCF.x_rotation, baseType=OWL.DatatypeProperty, graph=g)
        Property(CCF.y_rotation, baseType=OWL.DatatypeProperty, graph=g)
        Property(CCF.z_rotation, baseType=OWL.DatatypeProperty, graph=g)
        Property(CCF.rotation_order, baseType=OWL.DatatypeProperty, graph=g)
        Property(CCF.rotation_unit, baseType=OWL.DatatypeProperty, graph=g)
        Property(CCF.x_translation, baseType=OWL.DatatypeProperty, graph=g)
        Property(CCF.y_translation, baseType=OWL.DatatypeProperty, graph=g)
        Property(CCF.z_translation, baseType=OWL.DatatypeProperty, graph=g)
        Property(CCF.translation_unit, baseType=OWL.DatatypeProperty, graph=g)
        Property(CCF.file_url, baseType=OWL.DatatypeProperty, graph=g)
        Property(CCF.file_name, baseType=OWL.DatatypeProperty, graph=g)
        Property(CCF.file_subpath, baseType=OWL.DatatypeProperty, graph=g)
        Property(CCF.file_format, baseType=OWL.DatatypeProperty, graph=g)
        Property(CCF.rui_rank, baseType=OWL.DatatypeProperty, graph=g)
        Property(CCF.representation_of, baseType=OWL.DatatypeProperty, graph=g)
        Property(CCF.in_proximity_of, baseType=OWL.DatatypeProperty, graph=g)

        return SPOntology(g)

    def mutate(self, data):
        """
        """
        if isinstance(data, list):
            self._mutate_rui(data)
        elif isinstance(data, dict):
            if '@graph' in data:
                self._mutate_specimen(data['@graph'])
        return SPOntology(self.graph)

    def _mutate_rui(self, data):
        for obj in data:
            self._parse_object(obj)

    def _mutate_specimen(self, graph):
        for obj in graph:
            if 'samples' in obj:
                for sample in obj['samples']:
                    if 'rui_location' in sample:
                        self._parse_object(sample['rui_location'])

    def _parse_object(self, obj):
        object_type = obj['@type']
        if object_type == "ExtractionSet":
            self._add_extraction_set(obj)
        elif object_type == "SpatialEntity":
            self._add_spatial_entity(obj)
            if 'object' in obj:
                object_reference = obj['object']
                self._add_object_reference(object_reference)
                if 'placement' in object_reference:
                    object_placement = object_reference['placement']
                    self._add_object_placement(object_placement)
            if 'placement' in obj:
                if isinstance(obj['placement'], list):
                    for object_placement in obj['placement']:
                        self._add_object_placement(object_placement)
                else:
                    self._add_object_placement(obj['placement'])
        elif object_type == "SpatialPlacement":
            self._add_object_placement(obj)

    def _add_extraction_set(self, obj):
        self._add_extraction_set_to_graph(
            self._expand_instance_id(obj['@id']),
            self._string(obj['label']),
            self._expand_instance_id(obj['extraction_set_for']),
            self._integer(obj['rui_rank']))

    def _add_extraction_set_to_graph(self, subject, label, reference_organ,
                                     rui_rank):
        self.graph.add((subject, RDF.type, OWL.NamedIndividual))
        self.graph.add((subject, RDF.type, CCF.extraction_set))
        self.graph.add((subject, CCF.title, label))
        self.graph.add((subject, CCF.extraction_set_for, reference_organ))
        self.graph.add((subject, CCF.rui_rank, rui_rank))

    def _add_spatial_entity(self, obj):
        self._add_spatial_entity_to_graph(
            self._expand_instance_id(obj['@id']),
            self._get_label(obj),
            self._string(obj['creator_first_name']),
            self._string(obj['creator_last_name']),
            self._get_creator_orcid(obj),
            self._date(obj['creation_date']),
            self._get_annotations(obj),
            self._decimal(obj['x_dimension']),
            self._decimal(obj['y_dimension']),
            self._decimal(obj['z_dimension']),
            self._string(obj['dimension_units']),
            self._get_organ_owner_sex(obj),
            self._get_organ_side(obj),
            self._get_object_reference_id(obj),
            self._get_object_placement_id_list(obj),
            self._get_reference_organ(obj),
            self._get_representation_of(obj),
            self._get_extraction_set(obj),
            self._get_rui_rank(obj))

    def _add_spatial_entity_to_graph(self, subject, label, creator_first_name,
                                     creator_last_name, creator_orcid,
                                     creation_date, annotations,
                                     x_dimension, y_dimension, z_dimension,
                                     dimension_unit,
                                     organ_owner_sex, organ_side,
                                     object_reference, object_placements,
                                     reference_organ, representation_of,
                                     extraction_set, rui_rank):
        self.graph.add((subject, RDF.type, OWL.NamedIndividual))
        self.graph.add((subject, RDF.type, CCF.spatial_entity))
        if label is not None:
            self.graph.add((subject, CCF.title, label))
        self.graph.add((subject, CCF.creator_first_name, creator_first_name))
        self.graph.add((subject, CCF.creator_last_name, creator_last_name))
        if creator_orcid is not None:
            self.graph.add((subject, CCF.creator_orcid, creator_orcid))
        self.graph.add((subject, CCF.creation_date, creation_date))

        if annotations is not None:
            for annotation in annotations:
                self.graph.add((subject, CCF.in_proximity_of, annotation))

        self.graph.add((subject, CCF.x_dimension, x_dimension))
        self.graph.add((subject, CCF.y_dimension, y_dimension))
        self.graph.add((subject, CCF.z_dimension, z_dimension))
        self.graph.add((subject, CCF.dimension_unit, Literal("millimeter")))

        if organ_owner_sex is not None:
            self.graph.add((subject, CCF.organ_owner_sex, organ_owner_sex))

        if organ_side is not None:
            self.graph.add((subject, CCF.organ_side, organ_side))

        if object_reference is not None:
            self.graph.add((subject, CCF.has_object_reference,
                           object_reference))

        if object_placements is not None:
            for object_placement in object_placements:
                self.graph.add((subject, CCF.has_placement, object_placement))

        if reference_organ is not None:
            self.graph.add((subject, CCF.has_reference_organ,
                           reference_organ))

        if representation_of is not None:
            self.graph.add((subject, CCF.representation_of, representation_of))

        if extraction_set is not None:
            self.graph.add((subject, CCF.belongs_to_extraction_set,
                           extraction_set))

        if rui_rank is not None:
            self.graph.add((subject, CCF.rui_rank, rui_rank))

    def _add_object_reference(self, obj):
        self._add_object_reference_to_graph(
            self._expand_instance_id(obj['@id']),
            self._string(obj['file']),
            self._string(obj['file_format']),
            self._get_file_subpath(obj),
            self._get_object_placement_id(obj['placement']))

    def _add_object_reference_to_graph(self, subject, file_url, file_format,
                                       file_subpath, object_placement):
        self.graph.add((subject, RDF.type, OWL.NamedIndividual))
        self.graph.add((subject, RDF.type, CCF.spatial_object_reference))
        self.graph.add((subject, CCF.file_url, file_url))
        file_name = file_url.split("/")[-1]
        self.graph.add((subject, CCF.file_name, self._string(file_name)))
        self.graph.add((subject, CCF.file_format, file_format))
        if file_subpath is not None:
            self.graph.add((subject, CCF.file_subpath, file_subpath))
        if object_placement is not None:
            self.graph.add((subject, CCF.has_placement, object_placement))

    def _add_object_placement(self, obj):
        self._add_object_placement_to_graph(
            self._expand_instance_id(obj['@id']),
            self._expand_instance_id(obj['target']),
            self._decimal(obj['x_scaling']),
            self._decimal(obj['y_scaling']),
            self._decimal(obj['z_scaling']),
            self._string(obj['scaling_units']),
            self._decimal(obj['x_rotation']),
            self._decimal(obj['y_rotation']),
            self._decimal(obj['z_rotation']),
            self._string(obj['rotation_units']),
            self._get_rotation_order(obj),
            self._decimal(obj['x_translation']),
            self._decimal(obj['y_translation']),
            self._decimal(obj['z_translation']),
            self._string(obj['translation_units']),
            self._date(obj['placement_date']))

    def _add_object_placement_to_graph(self, subject, spatial_entity,
                                       x_scaling, y_scaling, z_scaling,
                                       scaling_unit,
                                       x_rotation, y_rotation, z_rotation,
                                       rotation_unit, rotation_order,
                                       x_translation, y_translation,
                                       z_translation, translation_unit,
                                       placement_date):
        self.graph.add((subject, RDF.type, OWL.NamedIndividual))
        self.graph.add((subject, CCF.creation_date, placement_date))

        self.graph.add((subject, RDF.type, CCF.spatial_placement))
        self.graph.add((subject, CCF.has_placement_target, spatial_entity))

        self.graph.add((subject, CCF.x_scaling, x_scaling))
        self.graph.add((subject, CCF.y_scaling, y_scaling))
        self.graph.add((subject, CCF.z_scaling, z_scaling))
        self.graph.add((subject, CCF.scaling_unit, scaling_unit))

        self.graph.add((subject, CCF.x_rotation, x_rotation))
        self.graph.add((subject, CCF.y_rotation, y_rotation))
        self.graph.add((subject, CCF.z_rotation, z_rotation))
        self.graph.add((subject, CCF.rotation_unit, rotation_unit))
        if rotation_order is not None:
            self.graph.add((subject, CCF.rotation_order, rotation_order))

        self.graph.add((subject, CCF.x_translation, x_translation))
        self.graph.add((subject, CCF.y_translation, y_translation))
        self.graph.add((subject, CCF.z_translation, z_translation))
        self.graph.add((subject, CCF.translation_unit, translation_unit))

    def _get_label(self, obj):
        try:
            return self._string(obj['label'])
        except KeyError:
            return None

    def _get_object_reference_id(self, obj):
        try:
            return self._get_instance_id(obj['object'])
        except KeyError:
            return None

    def _get_object_placement_id(self, obj):
        try:
            return self._get_instance_id(obj['placement'])
        except KeyError:
            return None

    def _get_object_placement_id_list(self, obj):
        try:
            placement = obj['placement']
            if isinstance(placement, list):
                return [self._get_instance_id(placement_item)
                        for placement_item in placement]
            else:
                return [self._get_instance_id(placement)]
        except KeyError:
            return None

    def _get_instance_id(self, obj):
        try:
            return self._expand_instance_id(obj['@id'])
        except KeyError:
            return None

    def _get_reference_organ(self, obj):
        try:
            return self._expand_instance_id(obj['reference_organ'])
        except KeyError:
            return None

    def _get_extraction_set(self, obj):
        try:
            return self._expand_instance_id(obj['extraction_set'])
        except KeyError:
            return None

    def _expand_instance_id(self, id_string):
        if "http://" not in id_string:
            return URIRef(CCF._NS + "latest/ccf.owl#" + id_string[1:])
        else:
            return URIRef(id_string)

    def _get_representation_of(self, obj):
        try:
            entity_id = obj['representation_of']
            reference_of = self._expand_anatomical_entity_id(entity_id)
            return self._string(reference_of)
        except KeyError:
            return None

    def _get_rui_rank(self, obj):
        try:
            return self._integer(obj['rui_rank'])
        except KeyError:
            return None

    def _get_file_subpath(self, obj):
        try:
            return self._string(obj['file_subpath'])
        except KeyError:
            return None

    def _get_rotation_order(self, obj):
        try:
            return self._string(obj['rotation_order'])
        except KeyError:
            return None

    def _get_creator_orcid(self, obj):
        try:
            return self._string(obj['creator_orcid'])
        except KeyError:
            return None

    def _get_organ_owner_sex(self, obj):
        try:
            return self._string(obj['sex'])
        except KeyError:
            return None

    def _get_organ_side(self, obj):
        try:
            return self._string(obj['side'])
        except KeyError:
            return None

    def _get_annotations(self, obj):
        try:
            arr = []
            for annotation in obj['ccf_annotations']:
                arr.append(self._string(annotation))
            return arr
        except KeyError:
            return None

    def _expand_anatomical_entity_id(self, str):
        if "obo:" in str:
            obo_pattern = re.compile("obo:", re.IGNORECASE)
            return obo_pattern.sub(
                "http://purl.obolibrary.org/obo/", str)
        elif "UBERON:" in str:
            uberon_pattern = re.compile("CL:", re.IGNORECASE)
            return uberon_pattern.sub(
                "http://purl.obolibrary.org/obo/UBERON_", str)
        elif "http://purl.obolibrary.org/obo/FMA_" in str:
            fmaobo_pattern = re.compile(
                "http://purl.obolibrary.org/obo/FMA_", re.IGNORECASE)
            return fmaobo_pattern.sub(
                "http://purl.org/sig/ont/fma/fma", str)
        else:
            return str

    def _string(self, str):
        return Literal(str)

    def _integer(self, str):
        return Literal(str, datatype=XSD.integer)

    def _decimal(self, str):
        return Literal(str, datatype=XSD.decimal)

    def _date(self, str):
        return Literal(str, datatype=XSD.date)

    def serialize(self, destination):
        """
        """
        self.graph.serialize(format='ttl',
                             destination=destination)
