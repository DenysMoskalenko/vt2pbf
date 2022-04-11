from vt2pbf.service.pbf import PBF

TILE_DATA = {
    "features": [
        {
            "geometry": [[[3185.0, 4121.0], [3189.0, 4119.0]]],
            "type": 2,
            "tags": {
                "value": 8,
                "error": 0.295,
                "quality": 0,
                "lastSampleTimestampMillisecondsUtc": 1624348345924,
                "calculationTimeMillisecondsUtc": 1624348346924,
                "roadClass": 3
            }
        },
        {
            "geometry": [[[3203.0, 4114.0], [3207.0, 4113.0]]],
            "type": 2,
            "tags": {
                "value": 9,
                "error": 0.29,
                "quality": 0,
                "lastSampleTimestampMillisecondsUtc": 1624035510901,
                "calculationTimeMillisecondsUtc": 1624035511901,
                "roadClass": 3
            }
        }
    ],
    "numPoints": 4,
    "numSimplified": 4,
    "numFeatures": 2,
    "source": [
        {
            "id": "None",
            "type": "LineString",
            "geometry": [0.5320093631744385, 0.34668564796447765, 1, 0.5320103168487549, 0.34668517112731934, 1.0],
            "tags": {
                "value": 8,
                "error": 0.295,
                "quality": 0,
                "lastSampleTimestampMillisecondsUtc": 1624348345924,
                "calculationTimeMillisecondsUtc": 1624348346924,
                "roadClass": 3
            },
            "minX": 0.5320093631744385,
            "minY": 0.34668517112731934,
            "maxX": 0.5320103168487549,
            "maxY": 0.34668564796447765
        },
        {
            "id": "None",
            "type": "LineString",
            "geometry": [0.5320136547088623, 0.34668397903442383, 1, 0.5320146083831787, 0.3466837406158447, 1.0],
            "tags": {
                "value": 9,
                "error": 0.29,
                "quality": 0,
                "lastSampleTimestampMillisecondsUtc": 1624035510901,
                "calculationTimeMillisecondsUtc": 1624035511901,
                "roadClass": 3
            },
            "minX": 0.5320136547088623,
            "minY": 0.3466837406158447,
            "maxX": 0.5320146083831787,
            "maxY": 0.34668397903442383
        }
    ],
    "x": 544,
    "y": 354,
    "z": 10,
    "transformed": True,
    "minX": 0.5320093631744385,
    "minY": 0.3466837406158447,
    "maxX": 0.5320146083831787,
    "maxY": 0.34668564796447765
}


def vt2pbf(vector_tile: dict, name: str = 'geojsonLayer'):
    tile = PBF()
    tile.add_layer(name, features=vector_tile['features'])
    pbf_string = tile.serialize_to_bytestring()
    return pbf_string


if __name__ == '__main__':
    pbf = vt2pbf(TILE_DATA)
    print(pbf)
