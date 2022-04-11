from vt2pbf.config import EXTEND
from vt2pbf.exceptions import LayerExistError
from vt2pbf.mapbox import vector_tile_pb2
from vt2pbf.service.layer import Layer


class PBF:
    def __init__(self, extend: int = EXTEND):
        self.pbf = vector_tile_pb2.Tile()
        self.extend = extend
        self._layers = {}

    @staticmethod
    def parse_from_string(pbf_string: bytes):
        pbf = vector_tile_pb2.Tile()
        pbf.ParseFromString(pbf_string)
        return pbf

    def serialize_to_bytestring(self) -> bytes:
        return self.pbf.SerializeToString()

    def add_layer(self, name: str, features: list[dict]):
        if name in self._layers:
            raise LayerExistError('Layer with this name already exist in the tile')

        layer = Layer(self.pbf, name)
        for feature in features:
            layer.add_feature(feature)

        self._layers[name] = layer
