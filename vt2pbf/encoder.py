from vt2pbf.mapbox import vector_tile_pb2

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


class Point:
    def __init__(self, x, y):
        self.x = int(x)
        self.y = int(y)


def command(cmd, length):
    return (length << 3) | (cmd & 0x7)


def zigzag(delta):
    return (delta << 1) ^ (delta >> 31)


class LayerExistError(Exception):
    pass


class InvalidFeatureError(Exception):
    pass


EXTEND = 4096
VERSION = 2


class FeaturePbf1:
    REQUIRED_FIELDS = {'geometry', 'type', 'tags'}

    def __init__(self, layer, feature: dict):
        self._layer = layer
        self.feature = self._create_feature(feature)

    def _create_feature(self, feature_info: dict):
        if not self.REQUIRED_FIELDS.issubset(feature_info):
            raise InvalidFeatureError(f'Feature must have all required fields: {self.REQUIRED_FIELDS}')


class Layer:
    def __init__(self, tile_pbf, name: str):
        self._tile_pbf = tile_pbf
        self.layer_pbf = self._create_layer(name)
        self.last_key_idx = 0
        self.last_value_idx = 0
        self.key_indices = {}
        self.value_indices = {}

    def _create_layer(self, name: str):
        layer = self._tile_pbf.layers.add()
        layer.name = name
        layer.version = VERSION  # TODO: check
        layer.extent = EXTEND
        return layer

    def add_feature(self, feature_info: dict, feature_id: int = None):
        feature = Feature(layer=self, feature_type=feature_info['type'], feature_id=feature_id)
        feature.add_tags(tags=feature_info['tags'])
        feature.add_geometry(geometry=feature_info['geometry'])


class Feature:
    def __init__(self, layer: Layer, feature_type: int, feature_id: int = None):
        """
            Leading the mapbox proto spec feature type must follow next schema:
                 UNKNOWN = 0;
                 POINT = 1;
                 LINESTRING = 2;
                 POLYGON = 3;
        """
        self._layer = layer
        self._layer_pbf = layer.layer_pbf
        self.feature_type = feature_type
        self.feature = self._create_feature(feature_id)

    def _create_feature(self, feature_id: int = None):
        feature = self._layer_pbf.features.add()
        if feature_id is not None:
            feature.id = feature_id
        feature.type = self.feature_type
        return feature

    def add_geometry(self, geometry: list[list[list[int]]]):
        geometry = self._encode_feature_geometry(geometry)
        self.feature.geometry.extend(geometry)

    def _encode_feature_geometry(self, raw_geometry: list[list[list[int]]]) -> list[int]:
        geometry = self._load_geometry(raw_geometry)
        x = 0
        y = 0
        rings = len(geometry)
        geom = []
        for r in range(rings):
            ring = geometry[r]
            count = 1
            if self.feature_type == 1:
                count = len(ring)
            geom.append(command(1, count))
            line_count = len(ring) - 1 if self.feature_type == 3 else len(ring)
            for i in range(line_count):
                if i == 1 and self.feature_type != 1:
                    geom.append(command(2, line_count - 1))
                dx = ring[i].x - x
                dy = ring[i].y - y
                geom.append(zigzag(dx))
                geom.append(zigzag(dy))
                x += dx
                y += dy
            if self.feature_type == 3:
                geom.append(command(7, 1))  # closepath
        return geom

    @staticmethod
    def _load_geometry(raw_geometry: list) -> list[list[Point]]:
        rings = raw_geometry
        geometry = []
        for i in range(len(rings)):
            ring = rings[i]
            new_ring = []
            for j in range(len(ring)):
                new_ring.append(Point(x=ring[j][0], y=ring[j][1]))
            geometry.append(new_ring)
        return geometry

    def add_tags(self, tags: dict):
        for k, v in tags.items():
            if v is None:
                continue

            if k not in self._layer.key_indices:
                self._layer.key_indices[k] = self._layer.last_key_idx
                self._layer.last_key_idx += 1
                self._layer_pbf.keys.append(k)
            self.feature.tags.append(self._layer.key_indices[k])

            if v not in self._layer.value_indices:
                self._layer.value_indices[v] = self._layer.last_value_idx
                self._layer.last_value_idx += 1
                value = self._layer_pbf.values.add()
                if isinstance(v, bool):
                    value.bool_value = v
                elif isinstance(v, str):
                    value.string_value = v
                elif isinstance(v, int):
                    # value.int_value = v
                    if v < 0:
                        value.sint_value = v
                    else:
                        value.uint_value = v
                elif isinstance(v, float):
                    value.double_value = v
            self.feature.tags.append(self._layer.value_indices[v])


class Tile:
    def __init__(self, extend: int = EXTEND):
        self.tile_pbf = vector_tile_pb2.Tile()
        self.extend = extend
        self._layers = {}

    @staticmethod
    def parse_from_string(pbf_string: bytes):
        tile_pbf = vector_tile_pb2.Tile()
        tile_pbf.ParseFromString(pbf_string)
        return tile_pbf

    def serialize_to_bytestring(self) -> bytes:
        return self.tile_pbf.SerializeToString()

    def add_layer(self, name: str, features: list[dict]):
        if name in self._layers:
            raise LayerExistError('Layer with this name already exist in the tile')

        layer = Layer(self.tile_pbf, name)
        for feature in features:
            layer.add_feature(feature)

        self._layers[name] = layer


def vt2pbf(vector_tile: dict, name: str = 'geojsonLayer'):
    tile = Tile()
    tile.add_layer(name, features=vector_tile['features'])
    pbf_string = tile.serialize_to_bytestring()
    return pbf_string


if __name__ == '__main__':
    pbf = vt2pbf(TILE_DATA)
    print(pbf)
