from rdflib.term import URIRef
from spatial2ccf.namespace import DefinedNamespace, Namespace


class CCF(DefinedNamespace):
    """
    CCF Vocabulary
    """

    _fail = True

    # http://www.w3.org/2002/07/owl#ObjectProperty
    has_member: URIRef
    located_in: URIRef
    has_gene_marker: URIRef
    has_protein_marker: URIRef
    is_biomarker_of: URIRef
    is_gene_marker_of: URIRef
    is_protein_marker_of: URIRef
    has_characterizing_biomarker_set: URIRef
    is_characterizing_biomarker_set_of: URIRef
    belongs_to_extraction_set: URIRef
    extraction_set_for: URIRef
    has_placement_target: URIRef
    has_reference_organ: URIRef
    has_object_reference: URIRef
    has_placement: URIRef

    # http://www.w3.org/2002/07/owl#DataProperty
    title: URIRef
    creator_first_name: URIRef
    creator_last_name: URIRef
    creator_orcid: URIRef
    creation_date: URIRef
    organ_owner_sex: URIRef
    organ_side: URIRef
    x_dimension: URIRef
    y_dimension: URIRef
    z_dimension: URIRef
    dimension_unit: URIRef
    x_scaling: URIRef
    y_scaling: URIRef
    z_scaling: URIRef
    scaling_unit: URIRef
    x_rotation: URIRef
    y_rotation: URIRef
    z_rotation: URIRef
    rotation_order: URIRef
    rotation_unit: URIRef
    x_translation: URIRef
    y_translation: URIRef
    z_translation: URIRef
    translation_unit: URIRef
    file_name: URIRef
    file_url: URIRef
    file_subpath: URIRef
    file_format: URIRef
    rui_rank: URIRef
    representation_of: URIRef
    in_proximity_of: URIRef

    # http://www.w3.org/2002/07/owl#AnnotationProperty
    unit_of_measurement: URIRef
    is_ftu: URIRef

    # http://www.w3.org/2002/07/owl#Class
    characterizing_biomarker_set: URIRef
    extraction_set: URIRef
    spatial_entity: URIRef
    spatial_object_reference: URIRef
    spatial_placement: URIRef
    biomarker: URIRef

    _NS = Namespace("http://purl.org/ccf/")