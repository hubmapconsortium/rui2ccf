import re

from spatial2ccf.namespace import CCF

from rdflib import Graph, URIRef, Literal
from rdflib import OWL, XSD, RDF, RDFS, DC, DCTERMS
from rdflib.extras.infixowl import Ontology, Property


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

        return SPOntology(g)

    def mutate(self, data):
        """
        """
        if isinstance(data, list):
            for obj in data:
                object_type = obj['@type']
                if object_type == "SpatialEntity":
                    self._add_spatial_entity(obj)
                elif object_type == "RetiredSpatialEntity":
                    self._add_retired_spatial_entity(obj)
                elif object_type == "SpatialPlacement":
                    self._add_spatial_placement(obj)
                elif object_type == "ExtractionSet":
                    self._add_extraction_set(obj)
                elif object_type == "Donor":
                    self._add_sample_registration_location(obj)
                else:
                    raise ValueError("Unknown object_type <" +
                                     object_type + ">")
        elif isinstance(data, dict):
            for obj in data['@graph']:
                object_type = obj['@type']
                if object_type == "Donor":
                    self._add_sample_registration_location(obj)
                else:
                    raise ValueError("Unknown object_type <" +
                                     object_type + ">")
        return SPOntology(self.graph)

    def _add_sample_registration_location(self, obj):
        publisher = self._get_publisher(obj)
        if 'samples' in obj:
            for sample in obj['samples']:
                if 'rui_location' not in sample:
                    continue
                sample_id = self._iri(sample['@id'])
                registration_location = sample['rui_location']
                self._add_registration_location(sample_id,
                                                registration_location,
                                                publisher)

    def _add_registration_location(self, sample_id, registration_location,
                                   publisher):
        reg_location_iri = self._iri(registration_location['@id'])
        self.graph.add((reg_location_iri, CCF.represents_bbox_of, sample_id))
        self._add_spatial_entity(registration_location, publisher)

    def _add_extraction_set(self, obj):
        self._add_extraction_set_to_graph(
            self._expand_instance_id(obj['@id']),
            self._string(obj['label']),  # consortium name
            self._expand_instance_id(obj['extraction_set_for']),
            self._integer(obj['rui_rank']))

    def _add_extraction_set_to_graph(self, subject, consortium_name,
                                     reference_organ_iri, rui_rank):
        self.graph.add((subject, RDF.type, OWL.NamedIndividual))
        self.graph.add((subject, RDF.type, CCF.ExtractionSet))
        self.graph.add((subject, RDFS.label, consortium_name))
        self.graph.add((subject, CCF.consortium_name, consortium_name))
        self.graph.add((subject, CCF.extraction_set_for, reference_organ_iri))
        self.graph.add((subject, CCF.rui_rank, rui_rank))

    def _add_retired_spatial_entity(self, obj, publisher=None):
        spatial_entity_id = self._expand_instance_id(obj['@id'])
        self._add_retired_spatial_entity_to_graph(
            spatial_entity_id,
            self._get_representation_of(obj))

    def _add_spatial_entity(self, obj, publisher=None):
        spatial_entity_id = self._expand_instance_id(obj['@id'])
        self._add_spatial_entity_to_graph(
            spatial_entity_id,
            self._get_label(obj),
            self._string(obj['creator_first_name']),
            self._string(obj['creator_last_name']),
            self._get_creator_orcid(obj),
            self._date(obj['creation_date']),
            self._get_collides_with_annotations(obj),
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
            self._get_rui_rank(obj),
            publisher)

        if 'object' in obj:
            # Only RUI data have 'spatial object reference' information
            self._add_object_reference(obj['object'])
        if 'placement' in obj:
            object_placements = obj['placement']
            if isinstance(object_placements, dict):
                object_placements = [object_placements]
            for object_placement in object_placements:
                self._add_spatial_placement(object_placement,
                                            spatial_entity_id,
                                            publisher)

    def _add_retired_spatial_entity_to_graph(self, spatial_entity_id,
                                             representation_of):
        self.graph.add((spatial_entity_id, RDF.type, OWL.NamedIndividual))
        self.graph.add((spatial_entity_id, RDF.type,
                        CCF.RetiredSpatialEntity))
        self.graph.add((spatial_entity_id, CCF.representation_of,
                        representation_of))

    def _add_spatial_entity_to_graph(self, spatial_entity_id, label,
                                     creator_first_name, creator_last_name,
                                     creator_orcid, creation_date, annotations,
                                     x_dimension, y_dimension, z_dimension,
                                     dimension_unit, organ_owner_sex,
                                     organ_side, object_reference,
                                     object_placements, reference_organ,
                                     representation_of, extraction_set,
                                     rui_rank, publisher):
        self.graph.add((spatial_entity_id, RDF.type, OWL.NamedIndividual))
        self.graph.add((spatial_entity_id, RDF.type, CCF.SpatialEntity))
        if representation_of:
            self.graph.add((spatial_entity_id, RDF.type, representation_of))

        if label:
            self.graph.add((spatial_entity_id, RDFS.label, label))

        self.graph.add((spatial_entity_id, CCF.creator_first_name,
                        creator_first_name))
        self.graph.add((spatial_entity_id, CCF.creator_last_name,
                        creator_last_name))
        self.graph.add((spatial_entity_id, DCTERMS.creator,
                        Literal(str(creator_first_name) + " " +
                                str(creator_last_name))))
        if creator_orcid:
            self.graph.add((spatial_entity_id, CCF.creator_orcid,
                            creator_orcid))
        self.graph.add((spatial_entity_id, DCTERMS.created, creation_date))

        if annotations:
            for annotation in annotations:
                self.graph.add((spatial_entity_id, CCF.collides_with,
                                annotation))

        self.graph.add((spatial_entity_id, CCF.x_dimension, x_dimension))
        self.graph.add((spatial_entity_id, CCF.y_dimension, y_dimension))
        self.graph.add((spatial_entity_id, CCF.z_dimension, z_dimension))
        self.graph.add((spatial_entity_id, CCF.dimension_unit, dimension_unit))

        if organ_owner_sex:
            self.graph.add((spatial_entity_id, CCF.organ_owner_sex,
                            organ_owner_sex))
        if organ_side:
            self.graph.add((spatial_entity_id, CCF.organ_side, organ_side))

        if object_reference:
            self.graph.add((spatial_entity_id, CCF.has_object_reference,
                           object_reference))
        if object_placements:
            for object_placement in object_placements:
                self.graph.add((spatial_entity_id, CCF.has_placement,
                                object_placement))
        if reference_organ:
            self.graph.add((spatial_entity_id, CCF.has_reference_organ,
                           reference_organ))
        if representation_of:
            self.graph.add((spatial_entity_id, CCF.representation_of,
                            representation_of))
        if extraction_set:
            self.graph.add((spatial_entity_id, CCF.has_extraction_set,
                           extraction_set))
        if rui_rank:
            self.graph.add((spatial_entity_id, CCF.rui_rank, rui_rank))

        if publisher:
            self.graph.add((spatial_entity_id, DCTERMS.publisher, publisher))

    def _add_object_reference(self, object_reference):
        obj_ref_id = self._expand_instance_id(object_reference['@id'])
        self._add_object_reference_to_graph(
            obj_ref_id,
            self._string(object_reference['file']),
            self._string(object_reference['file_format']),
            self._get_file_subpath(object_reference),
            self._get_object_placement_id(object_reference['placement']))
        if 'placement' in object_reference:
            object_placement = object_reference['placement']
            self._add_spatial_placement(object_placement, obj_ref_id)

    def _add_object_reference_to_graph(self, obj_ref_id, file_url, file_format,
                                       file_subpath, object_placement):
        self.graph.add((obj_ref_id, RDF.type, OWL.NamedIndividual))
        self.graph.add((obj_ref_id, RDF.type, CCF.SpatialObjectReference))
        self.graph.add((obj_ref_id, CCF.file_url, file_url))
        file_name = file_url.split("/")[-1]
        self.graph.add((obj_ref_id, CCF.file_name, self._string(file_name)))
        self.graph.add((obj_ref_id, CCF.file_format, file_format))
        if file_subpath:
            self.graph.add((obj_ref_id, CCF.file_subpath, file_subpath))
        if object_placement:
            self.graph.add((obj_ref_id, CCF.has_placement, object_placement))

    def _add_spatial_placement(self, object_placement, source_spatial_id=None,
                               publisher=None):
        if not source_spatial_id:
            source_spatial_id = self._get_source_placement(object_placement)
        self._add_object_placement_to_graph(
            self._expand_instance_id(object_placement['@id']),
            self._get_target_placement(object_placement),
            source_spatial_id,
            self._decimal(object_placement['x_scaling']),
            self._decimal(object_placement['y_scaling']),
            self._decimal(object_placement['z_scaling']),
            self._string(object_placement['scaling_units']),
            self._decimal(object_placement['x_rotation']),
            self._decimal(object_placement['y_rotation']),
            self._decimal(object_placement['z_rotation']),
            self._string(object_placement['rotation_units']),
            self._get_rotation_order(object_placement),
            self._decimal(object_placement['x_translation']),
            self._decimal(object_placement['y_translation']),
            self._decimal(object_placement['z_translation']),
            self._string(object_placement['translation_units']),
            self._date(object_placement['placement_date']),
            publisher)

    def _add_object_placement_to_graph(self, obj_pmnt_id,
                                       target_spatial_id,
                                       source_spatial_id,
                                       x_scaling, y_scaling,
                                       z_scaling, scaling_unit,
                                       x_rotation, y_rotation, z_rotation,
                                       rotation_unit, rotation_order,
                                       x_translation, y_translation,
                                       z_translation, translation_unit,
                                       placement_date, publisher):
        self.graph.add((obj_pmnt_id, RDF.type, OWL.NamedIndividual))
        self.graph.add((obj_pmnt_id, RDF.type, CCF.SpatialPlacement))
        self.graph.add((obj_pmnt_id, CCF.placement_relative_to,
                        target_spatial_id))
        self.graph.add((obj_pmnt_id, CCF.placement_for,
                        source_spatial_id))

        self.graph.add((obj_pmnt_id, CCF.x_scaling, x_scaling))
        self.graph.add((obj_pmnt_id, CCF.y_scaling, y_scaling))
        self.graph.add((obj_pmnt_id, CCF.z_scaling, z_scaling))
        self.graph.add((obj_pmnt_id, CCF.scaling_unit, scaling_unit))

        self.graph.add((obj_pmnt_id, CCF.x_rotation, x_rotation))
        self.graph.add((obj_pmnt_id, CCF.y_rotation, y_rotation))
        self.graph.add((obj_pmnt_id, CCF.z_rotation, z_rotation))
        self.graph.add((obj_pmnt_id, CCF.rotation_unit, rotation_unit))
        if rotation_order:
            self.graph.add((obj_pmnt_id, CCF.rotation_order, rotation_order))

        self.graph.add((obj_pmnt_id, CCF.x_translation, x_translation))
        self.graph.add((obj_pmnt_id, CCF.y_translation, y_translation))
        self.graph.add((obj_pmnt_id, CCF.z_translation, z_translation))
        self.graph.add((obj_pmnt_id, CCF.translation_unit, translation_unit))

        self.graph.add((obj_pmnt_id, DCTERMS.created, placement_date))
        if publisher:
            self.graph.add((obj_pmnt_id, DCTERMS.publisher, publisher))

    def _get_publisher(self, obj):
        try:
            return self._string(obj['consortium_name'])
        except KeyError:
            return None

    def _get_target_placement(self, obj):
        try:
            return self._expand_instance_id(obj['target'])
        except KeyError:
            return None

    def _get_source_placement(self, obj):
        try:
            return self._expand_instance_id(obj['source'])
        except KeyError:
            return self._expand_instance_id(obj['target'])

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
            while id_string[0] == "#":
                id_string = id_string[1:]
            return self._iri(CCF._NS + "latest/ccf.owl#" + id_string)
        else:
            return self._iri(id_string)

    def _get_representation_of(self, obj):
        try:
            entity_id = obj['representation_of']
            representation_of = self._expand_anatomical_entity_id(entity_id)
            return representation_of
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

    def _get_collides_with_annotations(self, obj):
        try:
            arr = []
            for annotation in obj['ccf_annotations']:
                arr.append(self._iri(annotation))
            return arr
        except KeyError:
            return None

    def _expand_anatomical_entity_id(self, str):
        id_string = str
        if "obo:" in str:
            obo_pattern = re.compile("obo:", re.IGNORECASE)
            id_string = obo_pattern.sub(
                "http://purl.obolibrary.org/obo/", str)
        elif "UBERON:" in str:
            uberon_pattern = re.compile("UBERON:", re.IGNORECASE)
            id_string = uberon_pattern.sub(
                "http://purl.obolibrary.org/obo/UBERON_", str)
        elif "http://purl.obolibrary.org/obo/FMA_" in str:
            fmaobo_pattern = re.compile(
                "http://purl.obolibrary.org/obo/FMA_", re.IGNORECASE)
            id_string = fmaobo_pattern.sub(
                "http://purl.org/sig/ont/fma/fma", str)
        return self._iri(id_string)

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

    def serialize(self, destination):
        """
        """
        self.graph.serialize(format='ttl',
                             destination=destination)
