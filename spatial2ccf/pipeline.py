import requests
from requests_file import FileAdapter
from spatial2ccf.ontology import SPOntology


def run(args):
    """
    """
    session = requests.Session()
    session.mount('file://', FileAdapter())

    o = SPOntology.new(args.ontology_iri)
    for url in args.input_url:
        response = session.get(url)
        data = response.json()
        o = o.mutate(data)

    o.serialize(args.output)
