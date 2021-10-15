from rdflib.term import URIRef
from rui2ccf.namespace import DefinedNamespace, Namespace


class OBO(DefinedNamespace):
    """
    OBO Vocabulary
    """

    _fail = True

    # http://www.w3.org/2002/07/owl#ObjectProperty

    # http://www.w3.org/2002/07/owl#DataProperty

    # http://www.w3.org/2002/07/owl#AnnotationProperty

    # http://www.w3.org/2002/07/owl#Class
    UO_0000016: URIRef  # millimeter
    UO_0000185: URIRef  # degree
    UO_0010006: URIRef  # ratio

    _NS = Namespace("http://purl.obolibrary.org/obo/")