import requests
from requests_file import FileAdapter
from rui2ccf.ontology import SPOntology


def run(args):
    """
    """
    session = requests.Session()
    session.mount('file://', FileAdapter())

    o = SPOntology.new(args.ontology_iri)
    for url in args.input_url:
        response = session.get(url)
        records = response.json()
        o = o.mutate(records)

    o.serialize(args.output)
