import logging
import time

from nldi_xstool.nldi_xstool import getXSAtPoint
from pygeoapi.process.base import BaseProcessor

LOGGER = logging.getLogger(__name__)

PROCESS_METADATA = {
    "version": "0.1.0",
    "id": "nldi-xsatpoint",
    "title": "NLDI xsatpoint process",
    "description": "NLDI xsatpoint process",
    "keywords": ["NLDI xsatpoint"],
    "links": [
        {
            "type": "text/html",
            "rel": "canonical",
            "title": "information",
            "href": "https://example.org/process",
            "hreflang": "en-US",
        }
    ],
    "inputs": [
        {
            "id": "lat",
            "title": "lat",
            "input": {
                "literalDataDomain": {
                    "dataType": "float",
                    "valueDefinition": {"anyValue": True},
                }
            },
            "minOccurs": 1,
            "maxOccurs": 1,
        },
        {
            "id": "lon",
            "title": "lon",
            "input": {
                "literalDataDomain": {
                    "dataType": "float",
                    "valueDefinition": {"anyValue": True},
                }
            },
            "minOccurs": 1,
            "maxOccurs": 1,
        },
        {
            "id": "width",
            "title": "width",
            "input": {
                "literalDataDomain": {
                    "dataType": "float",
                    "valueDefinition": {"anyValue": True},
                }
            },
            "minOccurs": 1,
            "maxOccurs": 1,
        },
        {
            "id": "numpts",
            "title": "numpts",
            "input": {
                "literalDataDomain": {
                    "dataType": "int",
                    "valueDefinition": {"anyValue": True},
                }
            },
            "minOccurs": 1,
            "maxOccurs": 1,
        },
    ],
    "outputs": [
        {
            "id": "nldi-xsatpoint-response",
            "title": "output nldi-xsatpoint",
            "output": {"formats": [{"mimeType": "application/json"}]},
        }
    ],
    "example": {
        "inputs": [
            {"id": "lat", "value": "40.2684", "type": "text/plain"},
            {"id": "lon", "value": "-103.80119", "type": "text/plain"},
            {"id": "width", "value": "1000.0", "type": "text/plain"},
            {"id": "numpts", "value": "101", "type": "text/plain"},
        ]
    },
}


class NLDIXSAtPointProcessor(BaseProcessor):
    """NLDI Split Catchment Processor"""

    def __init__(self, provider_def):
        """
        Initialize object
        :param provider_def: provider definition
        :returns: pygeoapi.process.nldi_delineate.NLDIDelineateProcessor
        """

        BaseProcessor.__init__(self, provider_def, PROCESS_METADATA)

    def execute(self, data):

        mimetype = "application/json"
        lat = float(data["lat"])
        lon = float(data["lon"])
        numpts = int(data["numpts"])
        width = float(data["width"])

        # print(lat, lon, width, numpts)

        timeBefore = time.perf_counter()

        # print("before function")
        results = getXSAtPoint((lon, lat), numpts, width)
        # print("after function")
        # print(results)

        timeAfter = time.perf_counter()
        totalTime = timeAfter - timeBefore
        print("Total Time:", totalTime)

        outputs = [{"id": "nldi-xsatpoint-response", "value": results.to_json()}]
        # print(results)
        return mimetype, results.to_json()

    def __repr__(self):
        return "<NLDIXSAtPointProcessor> {}".format(self.nldi - xsatpoint - response)
