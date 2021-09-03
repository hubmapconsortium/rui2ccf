from rdflib import Graph, Namespace, URIRef, Literal, BNode, XSD, RDF
from rdflib.extras.infixowl import OWL_NS, Ontology, Class, Property


class SPOntology:
    """CCF Spatial Ontology
    Represents the Spatial Ontology graph that can be mutated by supplying
    the HuBMAP RUI records
    """
    _CCF_BASE_IRI = "http://purl.org/ccf/"

    _CCF_NS = Namespace(_CCF_BASE_IRI)
    _DC_ELEMENTS_NS = Namespace("http://purl.org/dc/elements/1.1/")
    _DC_TERMS_NS = Namespace("http://purl.org/dc/terms/")
    _OBO_NS = Namespace("http://purl.obolibrary.org/obo/")

    def __init__(self, graph=None, **kwargs):
        self.graph = graph
        self.kwargs = kwargs

    @staticmethod
    def new(ontology_iri):
        g = Graph()
        g.bind('ccf', SPOntology._CCF_NS)
        g.bind('dc', SPOntology._DC_ELEMENTS_NS)
        g.bind('dcterms', SPOntology._DC_TERMS_NS)
        g.bind('obo', SPOntology._OBO_NS)
        g.bind('owl', OWL_NS)

        #################################################################
        # Classes
        #################################################################
        extraction_set =\
            Class(SPOntology._CCF_NS.extraction_set, graph=g)
        spatial_entity =\
            Class(SPOntology._CCF_NS.spatial_entity, graph=g)
        spatial_object_reference =\
            Class(SPOntology._CCF_NS.spatial_object_reference, graph=g)
        spatial_placement =\
            Class(SPOntology._CCF_NS.spatial_placement, graph=g)

        #################################################################
        # Object Properties
        #################################################################
        extraction_set_for =\
            Property(SPOntology._CCF_NS.extraction_set_for, graph=g)
        representation_of =\
            Property(SPOntology._CCF_NS.representation_of, graph=g)
        is_placement_of =\
            Property(SPOntology._CCF_NS.is_placement_of, graph=g)
        has_reference_organ =\
            Property(SPOntology._CCF_NS.has_reference_organ, graph=g)
        has_object_reference =\
            Property(SPOntology._CCF_NS.has_object_reference, graph=g)
        has_placement =\
            Property(SPOntology._CCF_NS.has_placement, graph=g)
        belongs_to_extraction_set =\
            Property(SPOntology._CCF_NS.belongs_to_extraction_set, graph=g)

        #################################################################
        # Data Properties
        #################################################################
        title =\
            Property(SPOntology._CCF_NS.title,
                     baseType=OWL_NS.DatatypeProperty, graph=g)
        x_dimension =\
            Property(SPOntology._CCF_NS.x_dimension,
                     baseType=OWL_NS.DatatypeProperty, graph=g)
        y_dimension =\
            Property(SPOntology._CCF_NS.y_dimension,
                     baseType=OWL_NS.DatatypeProperty, graph=g)
        z_dimension =\
            Property(SPOntology._CCF_NS.z_dimension,
                     baseType=OWL_NS.DatatypeProperty, graph=g)
        x_scaling =\
            Property(SPOntology._CCF_NS.x_scaling,
                     baseType=OWL_NS.DatatypeProperty, graph=g)
        y_scaling =\
            Property(SPOntology._CCF_NS.y_scaling,
                     baseType=OWL_NS.DatatypeProperty, graph=g)
        z_scaling =\
            Property(SPOntology._CCF_NS.z_scaling,
                     baseType=OWL_NS.DatatypeProperty, graph=g)
        x_rotation =\
            Property(SPOntology._CCF_NS.x_rotation,
                     baseType=OWL_NS.DatatypeProperty, graph=g)
        y_rotation =\
            Property(SPOntology._CCF_NS.y_rotation,
                     baseType=OWL_NS.DatatypeProperty, graph=g)
        z_rotation =\
            Property(SPOntology._CCF_NS.z_rotation,
                     baseType=OWL_NS.DatatypeProperty, graph=g)
        x_translation =\
            Property(SPOntology._CCF_NS.x_translation,
                     baseType=OWL_NS.DatatypeProperty, graph=g)
        y_translation =\
            Property(SPOntology._CCF_NS.y_translation,
                     baseType=OWL_NS.DatatypeProperty, graph=g)
        z_translation =\
            Property(SPOntology._CCF_NS.z_translation,
                     baseType=OWL_NS.DatatypeProperty, graph=g)
        file_name =\
            Property(SPOntology._CCF_NS.file_name,
                     baseType=OWL_NS.DatatypeProperty, graph=g)
        file_subpath =\
            Property(SPOntology._CCF_NS.file_subpath,
                     baseType=OWL_NS.DatatypeProperty, graph=g)
        file_format =\
            Property(SPOntology._CCF_NS.file_format,
                     baseType=OWL_NS.DatatypeProperty, graph=g)
        rui_rank =\
            Property(SPOntology._CCF_NS.rui_rank,
                     baseType=OWL_NS.DatatypeProperty, graph=g)

        #################################################################
        # Annotation Properties
        #################################################################
        creator =\
            Property(SPOntology._DC_ELEMENTS_NS.creator,
                     baseType=OWL_NS.AnnotationProperty, graph=g)
        creation_date =\
            Property(SPOntology._DC_TERMS_NS.created,
                     baseType=OWL_NS.AnnotationProperty, graph=g)
        unit_of_measurement =\
            Property(SPOntology._CCF_NS.unit_of_measurement,
                     baseType=OWL_NS.AnnotationProperty, graph=g)

        return SPOntology(
            g,
            ontology=Ontology(
                identifier=URIRef(ontology_iri),
                graph=g),
            extraction_set=extraction_set,
            spatial_entity=spatial_entity,
            spatial_object_reference=spatial_object_reference,
            spatial_placement=spatial_placement,
            extraction_set_for=extraction_set_for,
            representation_of=representation_of,
            is_placement_of=is_placement_of,
            has_reference_organ=has_reference_organ,
            has_object_reference=has_object_reference,
            has_placement=has_placement,
            belongs_to_extraction_set=belongs_to_extraction_set,
            title=title,
            x_dimension=x_dimension,
            y_dimension=y_dimension,
            z_dimension=z_dimension,
            x_scaling=x_scaling,
            y_scaling=y_scaling,
            z_scaling=z_scaling,
            x_rotation=x_rotation,
            y_rotation=y_rotation,
            z_rotation=z_rotation,
            x_translation=x_translation,
            y_translation=y_translation,
            z_translation=z_translation,
            file_name=file_name,
            file_subpath=file_subpath,
            file_format=file_format,
            rui_rank=rui_rank,
            creator=creator,
            creation_date=creation_date,
            unit_of_measurement=unit_of_measurement)

    def mutate(self, objects):
        """
        """
        for obj in objects:
            object_type = obj['@type']

            if object_type == "ExtractionSet":
                self._add_extraction_set(
                    self._expand(obj['@id']),
                    self._string(obj['label']),
                    self._expand(obj['extraction_set_for']),
                    self._integer(obj['rui_rank']))
            elif object_type == "SpatialEntity":
                self._add_spatial_entity(
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
                if 'object' in obj:
                    object_reference = obj['object']
                    self._add_object_reference(
                        self._expand(object_reference['@id']),
                        self._string(object_reference['file']),
                        self._string(object_reference['file_format']),
                        self._get_file_subpath(object_reference),
                        self._get_object_placement_id(object_reference))
                    if 'placement' in object_reference:
                        object_placement = object_reference['placement']
                        self._add_object_placement(
                            self._expand(object_placement['@id']),
                            self._expand(object_placement['target']),
                            self._decimal(object_placement['x_scaling']),
                            self._decimal(object_placement['y_scaling']),
                            self._decimal(object_placement['z_scaling']),
                            self._decimal(object_placement['x_rotation']),
                            self._decimal(object_placement['y_rotation']),
                            self._decimal(object_placement['z_rotation']),
                            self._decimal(object_placement['x_translation']),
                            self._decimal(object_placement['y_translation']),
                            self._decimal(object_placement['z_translation']),
                            self._date(object_placement['placement_date']))
                if 'placement' in obj:
                    for object_placement in obj['placement']:
                        self._add_object_placement(
                            self._expand(object_placement['@id']),
                            self._expand(object_placement['target']),
                            self._decimal(object_placement['x_scaling']),
                            self._decimal(object_placement['y_scaling']),
                            self._decimal(object_placement['z_scaling']),
                            self._decimal(object_placement['x_rotation']),
                            self._decimal(object_placement['y_rotation']),
                            self._decimal(object_placement['z_rotation']),
                            self._decimal(object_placement['x_translation']),
                            self._decimal(object_placement['y_translation']),
                            self._decimal(object_placement['z_translation']),
                            self._date(object_placement['placement_date']))
            elif object_type == "SpatialPlacement":
                self._add_object_placement(
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

        return SPOntology(self.graph, **self.kwargs)

    def _add_extraction_set(self, identifier, title, reference_organ,
                            rui_rank):
        self.graph.add((identifier, RDF.type, OWL_NS.NamedIndividual))
        self.graph.add((identifier, RDF.type, self._iri_of('extraction_set')))
        self.graph.add((identifier, self._iri_of('title'), title))
        self.graph.add((identifier, self._iri_of('extraction_set_for'),
                       reference_organ))
        self.graph.add((identifier, self._iri_of('rui_rank'), rui_rank))

    def _add_spatial_entity(self, identifier, title, x_dimension, y_dimension,
                            z_dimension, creator, creation_date,
                            object_reference, object_placements,
                            reference_organ, representation_of, extraction_set,
                            rui_rank):
        self.graph.add((identifier, RDF.type, OWL_NS.NamedIndividual))
        self.graph.add((identifier, RDF.type, self._iri_of('spatial_entity')))
        if representation_of is not None:
            bn = BNode()
            self.graph.add((identifier, RDF.type, bn))
            self.graph.add((bn, RDF.type, OWL_NS.Restriction))
            self.graph.add((bn, OWL_NS.onProperty, self._iri_of('representation_of')))
            self.graph.add((bn, OWL_NS.someValuesFrom, representation_of))
        self.graph.add((identifier, self._iri_of('title'), title))
        self._add_measurement(identifier, self._iri_of('x_dimension'), x_dimension,
                              self._OBO_NS.UO_0000016)  # millimeter
        self._add_measurement(identifier, self._iri_of('y_dimension'), y_dimension,
                              self._OBO_NS.UO_0000016)  # millimeter
        self._add_measurement(identifier, self._iri_of('z_dimension'), z_dimension,
                              self._OBO_NS.UO_0000016)  # millimeter
        self.graph.add((identifier, self._iri_of('creator'), creator))
        self.graph.add((identifier, self._iri_of('creation_date'), creation_date))
        if object_reference is not None:
            self.graph.add((identifier, self._iri_of('has_object_reference'),
                           object_reference))
        if object_placements is not None:
            for object_placement in object_placements:
                self.graph.add((identifier, self._iri_of('has_placement'),
                               object_placement))
        if reference_organ is not None:
            self.graph.add((identifier, self._iri_of('has_reference_organ'),
                           reference_organ))
        if extraction_set is not None:
            self.graph.add((identifier, self._iri_of(
                'belongs_to_extraction_set'), extraction_set))
        if rui_rank is not None:
            self.graph.add((identifier, self._iri_of('rui_rank'), rui_rank))

    def _add_object_reference(self, identifier, file_name, file_format,
                              file_subpath, object_placement):
        self.graph.add((identifier, RDF.type, OWL_NS.NamedIndividual))
        self.graph.add((identifier, RDF.type,
                       self._iri_of('spatial_object_reference')))
        self.graph.add((identifier, self._iri_of('file_name'), file_name))
        self.graph.add((identifier, self._iri_of('file_format'), file_format))
        if file_subpath is not None:
            self.graph.add((identifier, self._iri_of('file_subpath'),
                           file_subpath))
        if object_placement is not None:
            self.graph.add((identifier, self._iri_of('has_placement'),
                           object_placement))

    def _add_object_placement(self, identifier, spatial_entity,
                              x_scaling, y_scaling, z_scaling,
                              x_rotation, y_rotation, z_rotation,
                              x_translation, y_translation, z_translation,
                              placement_date):
        self.graph.add((identifier, RDF.type, OWL_NS.NamedIndividual))
        self.graph.add((identifier, RDF.type,
                       self._iri_of('spatial_placement')))
        self.graph.add((identifier, self._iri_of('is_placement_of'),
                       spatial_entity))
        self._add_measurement(identifier, self._iri_of('x_scaling'), x_scaling,
                              self._OBO_NS.UO_0010006)  # ratio
        self._add_measurement(identifier, self._iri_of('y_scaling'), y_scaling,
                              self._OBO_NS.UO_0010006)  # ratio
        self._add_measurement(identifier, self._iri_of('z_scaling'), z_scaling,
                              self._OBO_NS.UO_0010006)  # ratio
        self._add_measurement(identifier, self._iri_of('x_rotation'), x_rotation,
                              self._OBO_NS.UO_0000185)  # degree
        self._add_measurement(identifier, self._iri_of('y_rotation'), y_rotation,
                              self._OBO_NS.UO_0000185)  # degree
        self._add_measurement(identifier, self._iri_of('z_rotation'), z_rotation,
                              self._OBO_NS.UO_0000185)  # degree
        self._add_measurement(identifier, self._iri_of('x_translation'), x_translation,
                              self._OBO_NS.UO_0000016)  # millimeter
        self._add_measurement(identifier, self._iri_of('y_translation'), y_translation,
                              self._OBO_NS.UO_0000016)  # millimeter
        self._add_measurement(identifier, self._iri_of('z_translation'), z_translation,
                              self._OBO_NS.UO_0000016)  # millimeter
        self.graph.add((identifier, self._iri_of('creation_date'),
                       placement_date))

    def _add_measurement(self, identifier, measurement, value, unit):
        self.graph.add((identifier, measurement, value))
        # Add the unit of measurement annotation
        bn = BNode()
        self.graph.add((bn, RDF.type, OWL_NS.Axiom))
        self.graph.add((bn, OWL_NS.annotatedSource, identifier))
        self.graph.add((bn, OWL_NS.annotatedProperty, measurement))
        self.graph.add((bn, OWL_NS.annotatedTarget, value))
        self.graph.add((bn, self._iri_of('unit_of_measurement'), unit))

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
            return self._iri(obj['representation_of'])
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
            self._string(obj['file_subpath'])
        except KeyError:
            return None

    def _expand(self, str):
        return URIRef(self._CCF_BASE_IRI + str[1:])

    def _iri(self, str):
        return URIRef(str)

    def _string(self, str):
        return Literal(str)

    def _integer(self, str):
        return Literal(str, datatype=XSD.integer)

    def _decimal(self, str):
        return Literal(str, datatype=XSD.decimal)

    def _date(self, str):
        return Literal(str, datatype=XSD.date)

    def _iri_of(self, entity):
        return self.kwargs[entity].identifier

    def serialize(self, destination):
        """
        """
        self.graph.serialize(format='ttl', destination=destination)
