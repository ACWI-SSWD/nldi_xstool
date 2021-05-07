'''
    File name: dem_query.py
    Author: Anders Hopkins, Richard McDonald
'''


import requests
# import json
from shapely.geometry import Point, LineString, Polygon

# Resolution types and their respective IDs for the Rest Service
res_types = {'res_1m': 18, 'res_3m': 19, 'res_5m': 20, 'res_10m': 21, 'res_30m': 22, 'res_60m': 23}
# res_types = {'res_1m': 1, 'res_3m': 2, 'res_5m': 3, 'res_10m': 4, 'res_30m': 5, 'res_60m': 6}
dim_order = {'latlon': 0, 'lonlat': 1}
# Create a bounding box from any geo type
# 'width' is in meters. It is the width of the buffer to place around the input geometry


def make_bbox(shape_type, coords, width):
    if shape_type == 'point':
        shape = Point(coords)

    elif shape_type == 'line':
        shape = LineString(coords)

    elif shape_type == 'polygon':
        shape = Polygon(coords)

    converted_width = convert_width(width)
    buff_shape = shape.buffer(converted_width)
    return buff_shape.bounds

# Convert the width of the buffer from meters to 'degree'
# This is NOT a precise conversion, just a quick overestimation
# Maybe fix this later


def convert_width(width):
    factor = 1/70000
    dist = factor*width
    return dist

# Get request from arcgis Rest Services


def get_dem(bbox, res_type):
    minx = str(bbox[0])
    miny = str(bbox[1])
    maxx = str(bbox[2])
    maxy = str(bbox[3])
    res_id = res_types[res_type]

    url = f'https://index.nationalmap.gov/arcgis/rest/services/3DEPElevationIndex/MapServer/{res_id}/query'
    payload = {
        # "where": "",
        # "text": "",
        # "objectIds": "",
        # "time": "",
        "geometry": "{xmin:\""+minx+"\",ymin:\""+miny+"\",xmax:\""+maxx+"\",ymax:\""+maxy+"\",spatialReference:{wkid:4326}}",
        "geometryType": "esriGeometryEnvelope",
        "inSR": "EPSG:4326",
        "spatialRel": "esriSpatialRelIntersects",
        # "relationParam": "",
        # "outFields": "",
        "returnGeometry": "true",
        # "returnTrueCurves": "false",
        "maxAllowableOffset": "100",
        "geometryPrecision": "3",
        "outSR": "EPSG:4326",
        # "having": "",
        # "returnIdsOnly": "false",
        # "returnCountOnly": "false",
        # "orderByFields": "",
        # "groupByFieldsForStatistics": "",
        # "outStatistics": "",
        # "returnZ": "false",
        # "returnM": "false",
        # "gdbVersion": "",
        # "historicMoment": "",
        # "returnDistinctValues": "false",
        # "resultOffset": "",
        # "resultRecordCount": "",
        # "queryByDistance": "",
        # "returnExtentOnly": "false",
        # "datumTransformation": "",
        # "parameterValues": "",
        # "rangeValues": "",
        # "quantizationParameters": "",
        "featureEncoding": "esriDefault",
        "f": "geojson"
        }

    r = requests.get(url, params=payload)
    resp = r.json()

    # If the Rest Services has a 200 response
    if 'features' in resp:
        # If the features are not empty, then the DEM exist
        if resp['features'] != []:
            return True
        # If features are empty, then no DEM
        if resp['features'] == []:
            return False
    # If 'error', then there was an unsuccessful request
    if 'error' in resp:
        return 'Error!'

# The function to loop thru all resolutions and submit queries


def query_dems(shape_type, coords, width=100):
    """
    Queries 3DEP 3DEPElevationIndex and returns of dictionary of available
    resolutions for shapes bounding box.

    Args:
        shape_type (Shapely geometric object in [Point, LineString, Polygon]): [description]
        coords (List of tuples): For example, [(x,y), (x,y)]
        width (int, optional): [width to buffer bounding box of shape]. Defaults to 100.
    """
    resp = {}  # Create an empty dictionary for the response
    bbox = make_bbox(shape_type, coords, width)  # Make the bbox
    print(bbox)
    for res_type in res_types:   # Loop thru all resolutions and submit a query for each one
        resp[res_type] = (get_dem(bbox, res_type))  # Add the response to the dictionary

    # print(resp)
    return(resp)


def query_dems_shape(bbox):
    resp = {}

    for res_type in res_types:
        resp[res_type] = (get_dem(bbox, res_type))
    return resp

# Tests #########
# query_dems('point', [(-96, 39)])
# query_dems('line', [(-96.0001, 39), (-96, 39)])
# query_dems('polygon', [(-96.0008, 39), (-96, 39), ( -96, 39.0008)])
