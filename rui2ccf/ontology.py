from rui2ccf.namespace import CCF, OBO

from stringcase import snakecase
from rdflib import Graph, URIRef, Literal
from rdflib import OWL, XSD, RDF, RDFS, DC, DCTERMS
from rdflib.extras.infixowl import Ontology, Class, Property, BNode


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
        Class(CCF.extraction_set, graph=g)
        Class(CCF.spatial_entity, graph=g)
        Class(CCF.spatial_object_reference, graph=g)
        Class(CCF.spatial_placement, graph=g)
        Class(OBO.UO_0000016, graph=g)  # millimeter
        Class(OBO.UO_0000185, graph=g)  # degree
        Class(OBO.UO_0010006, graph=g)  # ratio

        Property(CCF.belongs_to_extraction_set, baseType=OWL.ObjectProperty, graph=g)
        Property(CCF.extraction_set_for, baseType=OWL.ObjectProperty, graph=g)
        Property(CCF.is_placement_of, baseType=OWL.ObjectProperty, graph=g)
        Property(CCF.has_reference_organ, baseType=OWL.ObjectProperty, graph=g)
        Property(CCF.has_object_reference, baseType=OWL.ObjectProperty, graph=g)
        Property(CCF.has_placement, baseType=OWL.ObjectProperty, graph=g)

        Property(CCF.title, baseType=OWL.DatatypeProperty, graph=g)
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
        Property(CCF.rotation_unit, baseType=OWL.DatatypeProperty, graph=g)
        Property(CCF.x_translation, baseType=OWL.DatatypeProperty, graph=g)
        Property(CCF.y_translation, baseType=OWL.DatatypeProperty, graph=g)
        Property(CCF.z_translation, baseType=OWL.DatatypeProperty, graph=g)
        Property(CCF.translation_unit, baseType=OWL.DatatypeProperty, graph=g)
        Property(CCF.file_name, baseType=OWL.DatatypeProperty, graph=g)
        Property(CCF.file_subpath, baseType=OWL.DatatypeProperty, graph=g)
        Property(CCF.file_format, baseType=OWL.DatatypeProperty, graph=g)
        Property(CCF.rui_rank, baseType=OWL.DatatypeProperty, graph=g)

        Property(CCF.unit_of_measurement, baseType=OWL.AnnotationProperty, graph=g)
        Property(DC.creator, baseType=OWL.AnnotationProperty, graph=g)
        Property(DCTERMS.created, baseType=OWL.AnnotationProperty, graph=g)

        return SPOntology(g)

    def mutate(self, objects):
        """
        """
        for obj in objects:
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
                    for object_placement in obj['placement']:
                        self._add_object_placement(object_placement)
            elif object_type == "SpatialPlacement":
                self._add_object_placement(object_placement)

        return SPOntology(self.graph)

    def _add_extraction_set(self, obj):
        self._add_extraction_set_to_graph(
            self._expand(obj['@id']),
            self._string(obj['label']),
            self._expand(obj['extraction_set_for']),
            self._integer(obj['rui_rank']))

    def _add_extraction_set_to_graph(self, subject, title, reference_organ,
                                     rui_rank):
        self.graph.add((subject, RDF.type, OWL.NamedIndividual))
        self.graph.add((subject, RDF.type, CCF.extraction_set))
        self.graph.add((subject, CCF.title, title))
        self.graph.add((subject, CCF.extraction_set_for, reference_organ))
        self.graph.add((subject, CCF.rui_rank, rui_rank))

    def _add_spatial_entity(self, obj):
        self._add_spatial_entity_to_graph(
            self._expand(obj['@id']),
            self._string(obj['label']),
            self._decimal(obj['x_dimension']),
            self._decimal(obj['y_dimension']),
            self._decimal(obj['z_dimension']),
            self._string(obj['creator']),
            self._date(obj['creation_date']),
            self._get_object_reference_id(obj),
            self._get_object_placement_ids(obj),
            self._get_reference_organ(obj),
            self._get_representation_of(obj),
            self._get_extraction_set(obj),
            self._get_rui_rank(obj))

    def _add_spatial_entity_to_graph(self, subject, title,
                                     x_dimension, y_dimension, z_dimension,
                                     creator, creation_date,
                                     object_reference, object_placements,
                                     reference_organ, representation_of,
                                     extraction_set, rui_rank):
        self.graph.add((subject, RDF.type, OWL.NamedIndividual))
        self.graph.add((subject, DC.creator, creator))
        self.graph.add((subject, DCTERMS.creation_date, creation_date))
        if representation_of is not None:
            c = URIRef(CCF._NS + "spatial_entity_of_" + snakecase(title))
            bn = BNode()
            self.graph.add((subject, RDF.type, c))
            self.graph.add((c, OWL.equivalentClass, bn))
            self.graph.add((bn, RDF.type, OWL.Restriction))
            self.graph.add((bn, OWL.onProperty, CCF.representation_of))
            self.graph.add((bn, OWL.someValuesFrom, representation_of))
            self.graph.add((c, RDFS.subClassOf, CCF.spatial_entity))
        else:
            self.graph.add((subject, RDF.type, CCF.spatial_entity))

        self.graph.add((subject, CCF.title, title))
        self.graph.add((subject, CCF.dimension_unit, Literal("millimeter")))
        self._measurement(subject, CCF.x_dimension, x_dimension, OBO.UO_0000016)
        self._measurement(subject, CCF.y_dimension, y_dimension, OBO.UO_0000016)
        self._measurement(subject, CCF.z_dimension, z_dimension, OBO.UO_0000016)

        if object_reference is not None:
            self.graph.add((subject, CCF.has_object_reference,
                           object_reference))
        if object_placements is not None:
            for object_placement in object_placements:
                self.graph.add((subject, CCF.has_placement,
                               object_placement))
        if reference_organ is not None:
            self.graph.add((subject, CCF.has_reference_organ,
                           reference_organ))
        if extraction_set is not None:
            self.graph.add((subject, CCF.belongs_to_extraction_set,
                           extraction_set))
        if rui_rank is not None:
            self.graph.add((subject, CCF.rui_rank, rui_rank))

    def _add_object_reference(self, obj):
        self._add_object_reference_to_graph(
            self._expand(obj['@id']),
            self._string(obj['file']),
            self._string(obj['file_format']),
            self._get_file_subpath(obj),
            self._get_object_placement_id(obj))

    def _add_object_reference_to_graph(self, subject, file_name, file_format,
                                       file_subpath, object_placement):
        self.graph.add((subject, RDF.type, OWL.NamedIndividual))
        self.graph.add((subject, RDF.type, CCF.spatial_object_reference))
        self.graph.add((subject, CCF.file_name, file_name))
        self.graph.add((subject, CCF.file_format, file_format))
        if file_subpath is not None:
            self.graph.add((subject, CCF.file_subpath, file_subpath))
        if object_placement is not None:
            self.graph.add((subject, CCF.has_placement, object_placement))

    def _add_object_placement(self, obj):
        self._add_object_placement_to_graph(
            self._expand(obj['@id']),
            self._expand(obj['target']),
            self._decimal(obj['x_scaling']),
            self._decimal(obj['y_scaling']),
            self._decimal(obj['z_scaling']),
            self._decimal(obj['x_rotation']),
            self._decimal(obj['y_rotation']),
            self._decimal(obj['z_rotation']),
            self._decimal(obj['x_translation']),
            self._decimal(obj['y_translation']),
            self._decimal(obj['z_translation']),
            self._date(obj['placement_date']))

    def _add_object_placement_to_graph(self, subject, spatial_entity,
                                       x_scaling, y_scaling, z_scaling,
                                       x_rotation, y_rotation, z_rotation,
                                       x_translation, y_translation, z_translation,
                                       placement_date):
        self.graph.add((subject, RDF.type, OWL.NamedIndividual))
        self.graph.add((subject, DCTERMS.creation_date, placement_date))

        self.graph.add((subject, RDF.type, CCF.spatial_placement))
        self.graph.add((subject, CCF.is_placement_of, spatial_entity))

        self.graph.add((subject, CCF.scaling_unit, Literal("ratio")))
        self._measurement(subject, CCF.x_scaling, x_scaling, OBO.UO_0010006)
        self._measurement(subject, CCF.y_scaling, y_scaling, OBO.UO_0010006)
        self._measurement(subject, CCF.z_scaling, z_scaling, OBO.UO_0010006)

        self.graph.add((subject, CCF.rotation_unit, Literal("degree")))
        self._measurement(subject, CCF.x_rotation, x_rotation, OBO.UO_0000185)
        self._measurement(subject, CCF.y_rotation, y_rotation, OBO.UO_0000185)
        self._measurement(subject, CCF.z_rotation, z_rotation, OBO.UO_0000185)

        self.graph.add((subject, CCF.translation_unit, Literal("millimeter")))
        self._measurement(subject, CCF.x_translation, x_translation, OBO.UO_0000016)
        self._measurement(subject, CCF.y_translation, y_translation, OBO.UO_0000016)
        self._measurement(subject, CCF.z_translation, z_translation, OBO.UO_0000016)

    def _measurement(self, identifier, measurement, value, unit):
        self.graph.add((identifier, measurement, value))
        # Add the unit of measurement annotation
        bn = BNode()
        self.graph.add((bn, RDF.type, OWL.Axiom))
        self.graph.add((bn, OWL.annotatedSource, identifier))
        self.graph.add((bn, OWL.annotatedProperty, measurement))
        self.graph.add((bn, OWL.annotatedTarget, value))
        self.graph.add((bn, CCF.unit_of_measurement, unit))

    def _get_object_reference_id(self, obj):
        try:
            return self._expand(obj['object']['@id'])
        except KeyError:
            return None

    def _get_object_placement_id(self, obj):
        try:
            return self._expand(obj['placement']['@id'])
        except KeyError:
            return None

    def _get_object_placement_ids(self, obj):
        try:
            return [self._expand(placement['@id'])
                    for placement in obj['placement']]
        except KeyError:
            return None

    def _get_reference_organ(self, obj):
        try:
            return self._expand(obj['reference_organ'])
        except KeyError:
            return None

    def _get_representation_of(self, obj):
        try:
            return URIRef(obj['representation_of'])
        except KeyError:
            return None

    def _get_extraction_set(self, obj):
        try:
            return self._expand(obj['extraction_set'])
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

    def _expand(self, str):
        return URIRef(CCF._NS + str[1:])

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
