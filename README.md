# RUI-to-CCF
A Python tool to convert HuBMAP RUI objects to CCF Spatial Ontology.

The CCF Spatial Ontology (CCF-SPO) describes the 2D and 3D shapes of entities and their physical locations and orientations. At the moment, the spatial entity represents only the 3D model of the anatomical entities. The spatial entity will have the spatial object reference that holds the 3D object information and the spatial placement that holds the object coordinate and transformation information (i.e., scaling, rotation and translation).

The [HuBMAP CCF Registration User Interface](https://hubmapconsortium.github.io/ccf-ui/rui/) (RUI) provides an interactive tissue registration system using 3D human organ models. It captures some metadata about the donor, tissue location and tissue slices.

## Installing the tool

You can install the application using `pip` after you clone the repository.
```
$ cd rui2ccf
$ pip install .
```

## Using the tool

1. Download the RUI records from the HuBMAP project repository. You may need to request access to the HuBMAP development team to get the RUI records.

2. Run the tool
   ```
   $ rui2ccf rui.jsonld --ontology-iri http://purl.org/ccf/data/spatial_entities.owl -o spatial_entities.owl
   ```

3. Open the resulting output file using [Protégé](https://protege.stanford.edu/)

<img width="950" alt="Screen Shot 2021-08-05 at 2 01 28 PM" src="https://user-images.githubusercontent.com/5062950/128420697-a4aed303-5395-45db-b463-4c82ef5c860d.png">
