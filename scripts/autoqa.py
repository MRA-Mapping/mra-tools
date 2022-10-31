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



"""
"""
print ("mratools autoqa: Loading Environment Variables")
server = environ.get("_AGIS_URL", "")
user = environ.get("_AGIS_USER", "")
pw = environ.get("_AGIS_PW", "")
SELECT = environ.get("_AGIS_SEL", "1=1")
layer_id = environ.get("_AGIS_LAYER", "ceea424c2f2149c38f1cb3be46653325")
print ("server:%s \nuser:%s \nSELECT:%s \nlayer_id:%s"%(server,user,SELECT,layer_id))


print ("mratools autoqa: opening arcgis connection")
gis = GIS(server, user, pw)

print ("mratools autoqa: fetching layer")
layer = gis.content.get(layer_id)

#SELECT="Date >= '2021-01-01 00:00:00' AND Date <= '2021-12-31 12:59:59'"

# Contruct the testing structure <layers>
layer_s = {'FeatureLayer': layer,
           'incidents':layer.layers[0],
           'points_found':layer.layers[1],
}


print ("mratools autoqa: selecting points by query")
layer_s['selected_incident_points']=layer_s['incidents'].query(where = SELECT)

# Run the tests
extra_tests = {'check': lambda x: False}

layer_s['selected_incident_results'] = [_ for _ in check_incidents(layer_s['selected_incident_points'], external_incident_tests = extra_tests )]

print(layer_s)


