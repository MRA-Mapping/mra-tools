#!/bin/env python3
"""
Automatic Quality Assurance for MRA Dataset

Control Script

Copyright 2022 MRA Mapping Contributors

Environment Variables:
_AGIS_URL
_AGIS_PW
_AGIS_USER
"""
from arcgis.gis import GIS
from mratools import check_incidents, cmp_incidents, _get_attrs_
from os import environ


server = environ.get("_AGIS_URL", "")
user = environ.get("_AGIS_USER", "")
pw = environ.get("_AGIS_PW", "")

gis = GIS(server, user, pw)

MRA_Main="ceea424c2f2149c38f1cb3be46653325"
MRA_Archive="26403d6ce684434eb22e0fe6f164bc45"
CALOES_Main="4fe1f4dd817c4f44a993c748e0080437"

SELECT="Date >= '2021-01-01 00:00:00' AND Date <= '2021-12-31 12:59:59'"


LAYER_IDS=[
#        MRA_Main,
        MRA_Archive,
#        CALOES_Main,
]

# Contruct the testing structure <layers>
layers = {}

# <layer layer_id: ID >
for layer_id in LAYER_IDS:
    layers[layer_id] = {'FeatureLayer': gis.content.get(layer_id)}


for idx,layer in layers.items():
    layer['incidents']=layer['FeatureLayer'].layers[0]
    layer['points_found'] = layer['FeatureLayer'].layers[1]



for idx,layer in layers.items():
    layer['selected_incident_points']=layer['incidents'].query(where = SELECT)
    #layer['selected_found_points']=layer['points_found].query(where=SELECT)


# Run the tests
extra_tests = {'check': lambda x: False}

for idx,layer in layers.items():
    layer['selected_incident_results'] = [_ for _ in check_incidents(layer['selected_incident_points'], external_incident_tests = extra_tests )]

print(layers)


